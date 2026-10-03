from __future__ import annotations

from threading import get_ident
from unittest.mock import MagicMock

import pytest

from app.client.yahoo_finance_client import fetch_yahoo_finance_info


@pytest.mark.asyncio
async def test_fetch_yahoo_finance_info_runs_yfinance_off_event_loop(monkeypatch):
    info = {"currentPrice": 500.0, "marketCap": 500_000_000_000}
    caller_thread_id = get_ident()
    info_thread_ids: list[int] = []
    mock_ticker = MagicMock()

    def get_info():
        info_thread_ids.append(get_ident())
        return info

    mock_ticker.get_info.side_effect = get_info
    mock_ticker_factory = MagicMock(return_value=mock_ticker)
    monkeypatch.setattr(
        "app.client.yahoo_finance_client.yfinance.Ticker",
        mock_ticker_factory,
    )

    result = await fetch_yahoo_finance_info("BRK.B")

    mock_ticker_factory.assert_called_once_with("BRK.B")
    mock_ticker.get_info.assert_called_once_with()
    assert info_thread_ids[0] != caller_thread_id
    assert result == info
