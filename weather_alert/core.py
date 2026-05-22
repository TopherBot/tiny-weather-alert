import os
import sys
from pathlib import Path

import httpx
from dotenv import load_dotenv

# Load .env from project root (or inherited env)
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

def get_weather(city: str, api_key: str) -> str:
    """Fetch current temperature (C) and weather description.
    Uses OpenWeatherMap's *current weather* endpoint.
    """
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": api_key, "units": "metric"}
    try:
        resp = httpx.get(url, params=params, timeout=10.0)
        resp.raise_for_status()
    except httpx.HTTPError as exc:
        sys.exit(f"❌ Weather request failed: {exc}")
    data = resp.json()
    temp = data["main"]["temp"]
    desc = data["weather"][0]["description"]
    return f"{temp:.1f}°C, {desc}"

def send_telegram(message: str, token: str, chat_id: str) -> None:
    """Push *message* to *chat_id* via Bot API."""
    api_url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message}
    try:
        resp = httpx.post(api_url, json=payload, timeout=10.0)
        resp.raise_for_status()
    except httpx.HTTPError as exc:
        sys.exit(f"❌ Telegram send failed: {exc}")
    # Telegram returns JSON with ok flag – we trust the status code.

def run() -> None:
    # Pull env vars – exit early if missing
    city = os.getenv("CITY")
    weather_key = os.getenv("WEATHER_API_KEY")
    tg_token = os.getenv("TELEGRAM_BOT_TOKEN")
    tg_chat = os.getenv("TELEGRAM_CHAT_ID")

    missing = [name for name, val in {
        "CITY": city,
        "WEATHER_API_KEY": weather_key,
        "TELEGRAM_BOT_TOKEN": tg_token,
        "TELEGRAM_CHAT_ID": tg_chat,
    }.items() if not val]
    if missing:
        sys.exit(f"❌ Missing environment variables: {', '.join(missing)}")

    weather = get_weather(city, weather_key)
    message = f"🌤️ {city}: {weather}"
    send_telegram(message, tg_token, tg_chat)
    print(f"✅ Sent: {message}")
