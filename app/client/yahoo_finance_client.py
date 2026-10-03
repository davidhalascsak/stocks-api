from __future__ import annotations

import asyncio
from typing import Any

import yfinance


def _get_ticker_info(ticker: str) -> dict[str, Any]:
    return yfinance.Ticker(ticker).get_info()


async def fetch_yahoo_finance_info(ticker: str) -> dict[str, Any]:
    return await asyncio.to_thread(_get_ticker_info, ticker)
