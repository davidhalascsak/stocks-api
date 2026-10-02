from __future__ import annotations

import httpx
from bs4 import BeautifulSoup

from app.models.ticker import TickerListResponse

SP500_URL = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
USER_AGENT = "StockAPI/0.1 (https://github.com/davidhalascsak/stocks-api)"


async def fetch_sp500_tickers() -> TickerListResponse:
    """Fetch and map the current S&P 500 ticker list from Wikipedia."""
    async with httpx.AsyncClient(
        timeout=30.0,
        headers={"User-Agent": USER_AGENT},
    ) as client:
        response = await client.get(SP500_URL)
        response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table", class_="wikitable")
    if table is None:
        raise ValueError("No HTML tables were found on the S&P 500 page.")

    rows = table.find_all("tr")
    if not rows:
        raise ValueError("The Wikipedia table does not include the expected 'Symbol' column.")
    headers = rows[0].find_all(["th", "td"], recursive=False)
    header_names = [header.get_text(strip=True) for header in headers]
    if "Symbol" not in header_names:
        raise ValueError("The Wikipedia table does not include the expected 'Symbol' column.")

    symbol_index = header_names.index("Symbol")
    tickers = []
    for row in rows[1:]:
        cells = row.find_all("td", recursive=False)
        if len(cells) <= symbol_index:
            continue
        ticker = "".join(cells[symbol_index].stripped_strings)
        if ticker:
            tickers.append(ticker)

    unique_tickers = sorted(set(tickers))
    return TickerListResponse(count=len(unique_tickers), tickers=unique_tickers)
