import os
from pathlib import Path

import pytest

# Import the module under test
from weather_alert import core

# --- Fixtures -----------------------------------------------------------
@pytest.fixture(autouse=True)
def set_env(monkeypatch, tmp_path):
    # Provide dummy but syntactically valid env vars for isolated runs
    monkeypatch.setenv("CITY", "London")
    monkeypatch.setenv("WEATHER_API_KEY", "test-key")
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "987654321")

# --- Unit Tests --------------------------------------------------------
def test_get_weather_handles_error(monkeypatch):
    """When the HTTP request fails, the function should exit with a message."""
    class DummyResp:
        def raise_for_status(self):
            raise Exception("boom")
    def fake_get(*args, **kwargs):
        return DummyResp()
    monkeypatch.setattr(core, "httpx", type("obj", (), {"get": fake_get}))
    with pytest.raises(SystemExit) as exc:
        core.get_weather("Nowhere", "bad-key")
    assert "Weather request failed" in str(exc.value)

def test_send_telegram_handles_error(monkeypatch):
    class DummyResp:
        def raise_for_status(self):
            raise Exception("boom")
    def fake_post(*args, **kwargs):
        return DummyResp()
    monkeypatch.setattr(core, "httpx", type("obj", (), {"post": fake_post}))
    with pytest.raises(SystemExit) as exc:
        core.send_telegram("msg", "token", "chat")
    assert "Telegram send failed" in str(exc.value)

def test_run_exits_on_missing_env(monkeypatch):
    # Remove a required variable
    monkeypatch.delenv("CITY", raising=False)
    with pytest.raises(SystemExit) as exc:
        core.run()
    assert "Missing environment variables" in str(exc.value)
