# tiny‑weather‑alert

A **tiny** Python project that:

1. Reads a `CITY` and a Telegram bot token from a `.env` file.
2. Calls the free Open‑WeatherMap API (or any HTTP weather endpoint).
3. Sends a short message (e.g., `🌤️ London: 13°C, light rain`) to a Telegram chat via the Bot API.
4. Runs on every push via GitHub Actions to prove CI works.

## Why this repo?
- **Instant launch** – clone, `./setup.sh`, and you have a working alert bot.
- **Proactive notification** – the CI workflow can be extended to push alerts on failures.
- **Best‑practice scaffold** – includes `.gitignore`, `LICENSE`, CI, pre‑commit hooks, and a `.env.example`.

## Quick start
```bash
# 1️⃣ Clone & enter
git clone https://github.com/your‑user/tiny-weather-alert && cd tiny-weather-alert

# 2️⃣ Install dependencies (uses a virtual‑env script)
./setup.sh

# 3️⃣ Create .env (copy from .env.example) and fill in your keys
cp .env.example .env
# edit .env → set WEATHER_API_KEY, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, CITY

# 4️⃣ Run the script locally
python -m weather_alert
```

## GitHub Actions CI
The workflow (`.github/workflows/ci.yml`) runs on every push and pull request:
- Installs Python 3.11
- Caches `pip` packages
- Lints the code with **ruff**
- Executes a minimal test suite (`pytest`)
- Checks that the script can import without errors.

## License
MIT – see `LICENSE`.

---
*Created by TopherBot – rapid‑repo‑creation enthusiast.*