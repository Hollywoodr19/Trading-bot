import os
import requests
from flask import Blueprint, redirect, request, session, url_for, flash
from dotenv import load_dotenv

# 📌 Umgebungsvariablen laden
load_dotenv("Auth.env")

COINBASE_CLIENT_ID = os.getenv("COINBASE_CLIENT_ID")
COINBASE_CLIENT_SECRET = os.getenv("COINBASE_CLIENT_SECRET")
COINBASE_REDIRECT_URI = os.getenv("COINBASE_REDIRECT_URI")
COINBASE_API_URL = "https://api.coinbase.com/v2"

coinbase_bp = Blueprint("coinbase", __name__)

# 📌 Coinbase Login-Route
@coinbase_bp.route("/login_coinbase")
def login_coinbase():
    """Weiterleitung zur Coinbase OAuth-Authentifizierung."""
    auth_url = (
        f"https://www.coinbase.com/oauth/authorize"
        f"?client_id={COINBASE_CLIENT_ID}"
        f"&redirect_uri={COINBASE_REDIRECT_URI}"
        f"&response_type=code"
        f"&scope=wallet:accounts:read,wallet:transactions:read,wallet:buys:create,wallet:sells:create"
    )
    return redirect(auth_url)

# 📌 Coinbase Callback-Route
@coinbase_bp.route("/callback")
def coinbase_callback():
    """Empfängt den Coinbase OAuth-Callback und speichert das Access Token."""
    code = request.args.get("code")

    if not code:
        flash("Coinbase-Authentifizierung fehlgeschlagen.", "error")
        return redirect(url_for("dashboard"))

    token_url = "https://api.coinbase.com/oauth/token"
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "client_id": COINBASE_CLIENT_ID,
        "client_secret": COINBASE_CLIENT_SECRET,
        "redirect_uri": COINBASE_REDIRECT_URI,
    }

    try:
        response = requests.post(token_url, data=data)
        token_data = response.json()

        if "access_token" in token_data:
            session["coinbase_access_token"] = token_data["access_token"]
            session["coinbase_refresh_token"] = token_data.get("refresh_token")
            flash("✅ Erfolgreich mit Coinbase verbunden!", "success")
        else:
            flash("❌ Fehler beim Abrufen des Access Tokens.", "error")

    except requests.RequestException as e:
        flash(f"❌ API-Fehler: {e}", "error")

    return redirect(url_for("dashboard"))

# 📌 Coinbase Wallet-/Portfolio-Abfrage
def get_coinbase_accounts():
    """Holt die Liste der Coinbase-Wallets des Nutzers."""
    if "coinbase_access_token" not in session:
        flash("⚠ Bitte zuerst Coinbase verbinden!", "error")
        return []

    url = f"{COINBASE_API_URL}/accounts"
    headers = {"Authorization": f"Bearer {session['coinbase_access_token']}"}

    print(f"🔍 API-Abfrage für Wallets: {url}")  # Debugging

    try:
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Wallet-Daten erhalten: {data}")  # Debug-Log
            return data.get("data", [])
        else:
            print(f"❌ API-Fehler: {response.status_code} - {response.text}")
            return []

    except requests.RequestException as e:
        print(f"❌ API-Fehler: {e}")
        return []
