from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import pytest

from app.client import USER_AGENT
from app.client.wikipedia_client import fetch_sp500_page


@pytest.mark.asyncio
async def test_fetch_sp500_page_makes_async_request(monkeypatch):
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
    monkeypatch.setattr("app.client.wikipedia_client.httpx.AsyncClient", mock_async_client)

    page_html = await fetch_sp500_page()

    mock_async_client.assert_called_once_with(
        timeout=30.0,
        headers={"User-Agent": USER_AGENT},
    )
    mock_client.get.assert_awaited_once()
    assert page_html == mock_response.text
