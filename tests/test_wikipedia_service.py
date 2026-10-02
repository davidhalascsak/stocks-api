from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import pytest

from app.services.wikipedia_service import USER_AGENT, fetch_sp500_tickers


@pytest.mark.asyncio
async def test_fetch_sp500_tickers_extracts_symbols(monkeypatch):
    mock_response = MagicMock()
    mock_response.text = """
    <table class="wikitable">
      <tr><th>Company</th><th>Symbol</th></tr>
      <tr><td>Apple</td><td>AAPL</td></tr>
      <tr><td>Microsoft</td><td>MSFT</td></tr>
      <tr><td>Apple</td><td> AAPL </td></tr>
    </table>
    """

    mock_client = MagicMock()
    mock_client.__aenter__.return_value = mock_client
    mock_client.__aexit__.return_value = None
    mock_client.get = AsyncMock(return_value=mock_response)
    mock_response.raise_for_status = MagicMock()

    mock_async_client = MagicMock(return_value=mock_client)
    monkeypatch.setattr("app.services.wikipedia_service.httpx.AsyncClient", mock_async_client)

    tickers = await fetch_sp500_tickers()

    mock_async_client.assert_called_once_with(
        timeout=30.0,
        headers={"User-Agent": USER_AGENT},
    )
    assert tickers.count == 2
    assert tickers.tickers == ["AAPL", "MSFT"]
