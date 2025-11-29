from flask import Flask, jsonify, request, render_template, make_response
from flask_cors import CORS
from models import Trade, session, init_db
from datetime import datetime
import io, csv

# inicjalizacja bazy
init_db()

app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app)

# ustawienie początkowego kapitału (można zmieniać)
INITIAL_BALANCE = 10000.0

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/trades", methods=["GET"])
def get_trades():
    trades = session.query(Trade).order_by(Trade.timestamp).all()
    data = [{
        "id": t.id,
        "timestamp": t.timestamp.isoformat(),
        "position": t.position,
        "entry_reason": t.entry_reason,
        "profit": t.profit,
        "win": t.win,
        "balance_after": t.balance_after
    } for t in trades]
    return jsonify(data)

@app.route("/api/trades", methods=["POST"])
def add_trade():
    payload = request.json
    try:
        ts = payload.get("timestamp")
        if ts:
            ts = datetime.fromisoformat(ts)
        else:
            ts = datetime.utcnow()
        position = payload["position"].upper()
        entry_reason = payload.get("entry_reason", "")
        profit = float(payload["profit"])
    except Exception as e:
        return jsonify({"error": "Błędne dane: " + str(e)}), 400

    last = session.query(Trade).order_by(Trade.timestamp.desc()).first()
    balance_before = last.balance_after if last else INITIAL_BALANCE
    balance_after = balance_before + profit
    win = "WIN" if profit > 0 else "LOSS"

    trade = Trade(timestamp=ts, position=position, entry_reason=entry_reason,
                  profit=profit, win=win, balance_after=balance_after)
    session.add(trade)
    session.commit()
    return jsonify({"status": "ok", "id": trade.id}), 201

@app.route("/api/summary", methods=["GET"])
def summary():
    trades = session.query(Trade).all()
    total = len(trades)
    wins = sum(1 for t in trades if t.profit > 0)
    losses = total - wins
    final_bal = trades[-1].balance_after if trades else INITIAL_BALANCE
    winrate = (wins / total * 100) if total else 0.0
    expectancy = None
    if total:
        avg_win = sum(t.profit for t in trades if t.profit>0)/max(1, sum(1 for t in trades if t.profit>0))
        avg_loss = sum(t.profit for t in trades if t.profit<=0)/max(1, sum(1 for t in trades if t.profit<=0))
        expectancy = ( (avg_win * (wins/total)) + (avg_loss * (losses/total)) )
    return jsonify({
        "total": total,
        "wins": wins,
        "losses": losses,
        "winrate": round(winrate, 2),
        "final_balance": round(final_bal, 2),
        "expectancy": round(expectancy, 4) if expectancy is not None else None
    })

@app.route("/api/export_csv", methods=["GET"])
def export_csv():
    trades = session.query(Trade).order_by(Trade.timestamp).all()
    si = io.StringIO()
    cw = csv.writer(si)
    cw.writerow(["id","timestamp","position","entry_reason","profit","win","balance_after"])
    for t in trades:
        cw.writerow([t.id, t.timestamp.isoformat(), t.position, t.entry_reason, t.profit, t.win, t.balance_after])
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=backtest_trades.csv"
    output.headers["Content-type"] = "text/csv"
    return output

@app.route("/api/load_sample", methods=["POST"])
def load_sample():
    sample = [
        {"timestamp":"2025-01-12T14:30:00","position":"LONG","entry_reason":"SMA50 x SMA200","profit":120},
        {"timestamp":"2025-01-12T16:45:00","position":"SHORT","entry_reason":"odbicie od oporu H1","profit":-40},
        {"timestamp":"2025-01-13T10:15:00","position":"LONG","entry_reason":"RSI oversold","profit":80},
        {"timestamp":"2025-01-14T09:20:00","position":"SHORT","entry_reason":"break suport","profit":-60},
        {"timestamp":"2025-01-15T11:00:00","position":"LONG","entry_reason":"divergencja MACD","profit":200},
    ]
    session.query(Trade).delete()
    session.commit()
    for s in sample:
        ts = datetime.fromisoformat(s["timestamp"])
        last = session.query(Trade).order_by(Trade.timestamp.desc()).first()
        balance_before = last.balance_after if last else INITIAL_BALANCE
        balance_after = balance_before + s["profit"]
        win = "WIN" if s["profit"]>0 else "LOSS"
        trade = Trade(timestamp=ts, position=s["position"], entry_reason=s["entry_reason"],
                      profit=s["profit"], win=win, balance_after=balance_after)
        session.add(trade)
    session.commit()
    return jsonify({"status":"ok","loaded":len(sample)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
