Instrukcja uruchomienia lokalnie:

1) Stwórz virtualenv i aktywuj:
   python -m venv venv
   source venv/bin/activate   # macOS/Linux
   venv\Scripts\activate    # Windows

2) Zainstaluj wymagania:
   pip install -r requirements.txt

3) Uruchom aplikację:
   python app.py

4) Otwórz w przeglądarce:
   http://127.0.0.1:5000

Aby otworzyć na iPhonie, upewnij się, że iPhone jest w tej samej sieci Wi‑Fi i użyj adresu http://<IP_KOMPUTERA>:5000

Szybkie wystawienie publicznie — ngrok:
   ngrok http 5000

Plik trades.db (SQLite) zostanie utworzony automatycznie w katalogu projektu.
