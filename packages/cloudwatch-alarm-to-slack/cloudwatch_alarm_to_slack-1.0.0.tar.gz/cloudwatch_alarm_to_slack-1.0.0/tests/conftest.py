"""Pytest config file."""


import pytest


@pytest.fixture(autouse=True)
def default_env_vars(monkeypatch):
    """Set default environment variables."""
    monkeypatch.setenv('SLACK_BOT_TOKEN', 'test_slack_bot_token')
    monkeypatch.setenv('SLACK_CHANNEL', 'test_slack_channel')
