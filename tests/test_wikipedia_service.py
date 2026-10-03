from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from app.dto.ticker import TickerListResponse
from app.services.wikipedia_service import fetch_sp500_tickers


@pytest.mark.asyncio
async def test_fetch_sp500_tickers_extracts_symbols(monkeypatch):
    monkeypatch.setattr(
        "app.services.wikipedia_service.fetch_sp500_page",
        AsyncMock(
            return_value="""
            <table class="wikitable">
              <tr><th>Company</th><th>Symbol</th></tr>
              <tr><td>Apple</td><td>AAPL</td></tr>
              <tr><td>Microsoft</td><td>MSFT</td></tr>
              <tr><td>Apple</td><td> AAPL </td></tr>
            </table>
            """
        ),
    )

    tickers = await fetch_sp500_tickers()

    assert tickers == TickerListResponse(tickers=["AAPL", "MSFT"])
