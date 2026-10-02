from __future__ import annotations

from bs4 import BeautifulSoup

from app.client.wikipedia_client import fetch_sp500_page
from app.dto.ticker import TickerListResponse


async def fetch_sp500_tickers() -> TickerListResponse:
    """Fetch and map the current S&P 500 ticker list from Wikipedia."""
    page_html = await fetch_sp500_page()
    soup = BeautifulSoup(page_html, "html.parser")
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
