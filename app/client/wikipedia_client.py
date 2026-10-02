from __future__ import annotations

import httpx

from app.client import USER_AGENT

SP500_URL = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
USER_AGENT = "StockAPI/0.1 (https://github.com/davidhalascsak/stocks-api)"


async def fetch_sp500_page() -> str:
    """Fetch the S&P 500 Wikipedia page HTML."""
    async with httpx.AsyncClient(
        timeout=30.0,
        headers={"User-Agent": USER_AGENT},
    ) as client:
        response = await client.get(SP500_URL)
        response.raise_for_status()

    return response.text
