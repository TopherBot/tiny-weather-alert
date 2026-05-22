#!/usr/bin/env bash
# Simple setup script – creates a virtual‑env and installs deps
set -e

# Create venv if missing
if [ ! -d venv ]; then
  python3 -m venv venv
fi

# Activate venv
source venv/bin/activate

# Upgrade pip and install requirements
pip install --upgrade pip
pip install -r requirements.txt

echo "✅ Setup complete. Activate with 'source venv/bin/activate' and run 'python -m weather_alert'"
