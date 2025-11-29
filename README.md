# Forex Backtest Web App

Kompletny projekt do logowania transakcji Forex w backtestingu.
Gotowy do wrzucenia na GitHub i deployowania na Render / Railway / Heroku.

## Funkcje
- zapisywanie transakcji: long/short, powód wejścia, wynik
- automatyczna krzywa kapitału
- wykres equity
- kalendarz transakcji
- statystyki: winrate, expectancy, liczba transakcji
- eksport CSV

## Uruchomienie lokalne
```bash
pip install -r requirements.txt
python app.py
```

Aplikacja pojawi się pod adresem:
http://127.0.0.1:5000

## Deploy na Render (najprostszy)
1. Wgraj repozytorium na GitHub
2. Wejdź na https://render.com
3. New → Web Service
4. Build Command:
   pip install -r requirements.txt
5. Start Command:
   gunicorn app:app
