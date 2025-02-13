import requests
import os
from dotenv import load_dotenv
import locale

# 📌 Umgebungsvariablen laden
load_dotenv("Auth.env")

COINBASE_API_URL = "https://api.exchange.coinbase.com/products"
FX_API_URL = "https://api.exchangerate-api.com/v4/latest/USD"

# Zahlenformatierung setzen (Tausendertrennzeichen, Dezimaltrennzeichen)
locale.setlocale(locale.LC_ALL, 'de_DE.UTF-8')

def format_number(value):
    """Formatiert eine Zahl mit Tausendertrennzeichen und 6 Dezimalstellen."""
    try:
        return locale.format_string("%.6f", float(value), grouping=True)
    except ValueError:
        return "N/A"

def get_coinbase_price(currency):
    """Holt den aktuellen Preis und das Handelsvolumen einer Kryptowährung."""
    currency = currency.upper()
    price_eur_url = f"{COINBASE_API_URL}/{currency}-EUR/ticker"
    price_usd_url = f"{COINBASE_API_URL}/{currency}-USD/ticker"

    # 1️⃣ Direkte EUR-Abfrage
    response = requests.get(price_eur_url)
    if response.status_code == 200:
        data = response.json()
        return {
            "price": format_number(data.get("price", 0)),
            "volume": format_number(data.get("volume", 0))
        }

    # 2️⃣ Falls nicht gefunden → USD-Abfrage + Währungsumrechnung
    response = requests.get(price_usd_url)
    if response.status_code == 200:
        data = response.json()
        price_usd = float(data.get("price", 0))
        volume_usd = float(data.get("volume", 0))

        # Umrechnung in EUR
        fx_response = requests.get(FX_API_URL)
        if fx_response.status_code == 200:
            fx_rate = fx_response.json().get("rates", {}).get("EUR", 1)
            return {
                "price": format_number(price_usd * fx_rate),
                "volume": format_number(volume_usd * fx_rate)
            }

    # 3️⃣ Falls gar keine Werte → Notfalllösung
    return {"price": "N/A", "volume": "N/A"}


FX_API_URL = "https://api.exchangerate-api.com/v4/latest/USD"


def get_multiple_prices(crypto_list):
    """Holt die Preise für mehrere Kryptowährungen gleichzeitig"""

    price_data = {}

    # 1️⃣ Wechselkurs holen (USD → EUR)
    fx_response = requests.get(FX_API_URL)
    fx_rate = 1  # Falls API nicht funktioniert, bleibt der Standard EUR=EUR
    if fx_response.status_code == 200:
        fx_rate = fx_response.json().get("rates", {}).get("EUR", 1)

    for currency in crypto_list:
        currency = currency.upper().strip()
        price_url_eur = f"{COINBASE_API_URL}/{currency}-EUR/ticker"
        price_url_usd = f"{COINBASE_API_URL}/{currency}-USD/ticker"

        response = requests.get(price_url_eur)
        if response.status_code == 200:
            data = response.json()
            price_data[currency] = {
                "price": format_number(data.get("price", "N/A")),
                "volume": format_number(data.get("volume", "N/A"))
            }
        else:
            # 🟠 Falls keine EUR-Daten → USD-Daten abrufen und umrechnen
            response = requests.get(price_url_usd)
            if response.status_code == 200:
                data = response.json()
                price_usd = float(data.get("price", 0)) * fx_rate
                volume_usd = float(data.get("volume", 0)) * fx_rate
                price_data[currency] = {
                    "price": format_number(price_usd),
                    "volume": format_number(volume_usd)
                }
            else:
                print(f"❌ Fehler bei {currency}: {response.status_code}")
                price_data[currency] = {"price": "N/A", "volume": "N/A"}

    return price_data  # Speichert alles als Dictionary


def get_coinbase_historical_data(currency, granularity):
    """Holt historische Kursdaten von Coinbase für verschiedene Zeiträume."""
    url = f"{COINBASE_API_URL}/{currency}-EUR/candles?granularity={granularity}"
    response = requests.get(url, timeout=5)

    if response.status_code == 200:
        return response.json()[::-1]  # Älteste zuerst
    return []

def buy_crypto(currency, amount):
    """Simuliert den Kauf einer Kryptowährung (Coinbase API erforderlich)."""
    return {"status": "success", "message": f"{amount} {currency} gekauft."}

def sell_crypto(currency, amount):
    """Simuliert den Verkauf einer Kryptowährung (Coinbase API erforderlich)."""
    return {"status": "success", "message": f"{amount} {currency} verkauft."}

# 📌 Sicherstellen, dass alle Funktionen exportiert werden
__all__ = ["get_coinbase_price", "get_multiple_prices", "get_coinbase_historical_data", "buy_crypto", "sell_crypto"]
