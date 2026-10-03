from __future__ import annotations

import asyncio
import logging
from datetime import UTC, datetime
from typing import Any

from curl_cffi.requests.exceptions import RequestException
from pydantic import ValidationError
from yfinance.exceptions import YFException

from app.dto.stock import (
    StockDetails,
    StockDetailsListResponse,
    StockFetchFailure,
)
from app.client.yahoo_finance_client import fetch_yahoo_finance_info
from app.services.wikipedia_service import fetch_sp500_tickers

MAX_CONCURRENT_REQUESTS = 5

logger = logging.getLogger(__name__)


async def fetch_yahoo_finance_details() -> StockDetailsListResponse:
    """Fetch and assemble Yahoo Finance details for Wikipedia's current tickers."""
    ticker_list = await fetch_sp500_tickers()
    tickers = ticker_list.tickers
    semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)

    tasks = [
        asyncio.create_task(_fetch_ticker_details(ticker, semaphore))
        for ticker in tickers
    ]
    results_by_ticker: dict[str, StockDetails | StockFetchFailure] = {}
    try:
        for completed_task in asyncio.as_completed(tasks):
            result = await completed_task
            results_by_ticker[result.ticker] = result
    finally:
        for task in tasks:
            if not task.done():
                task.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)

    results = [
        results_by_ticker.get(
            ticker, 
            StockFetchFailure(ticker=ticker, message="Task was aborted or cancelled.")
        ) 
        for ticker in tickers
    ]
    stocks = [result for result in results if isinstance(result, StockDetails)]
    failures = [result for result in results if isinstance(result, StockFetchFailure)]
    return StockDetailsListResponse(
        stocks=stocks,
        failures=failures,
    )


async def _fetch_ticker_details(
    ticker: str,
    semaphore: asyncio.Semaphore,
) -> StockDetails | StockFetchFailure:
    async with semaphore:
        try:
            payload = await fetch_yahoo_finance_info(ticker)
            return _parse_yahoo_response(ticker, payload)
        except (RequestException, YFException) as error:
            logger.warning("Yahoo Finance request failed for %s: %s", ticker, error)
            return StockFetchFailure(
                ticker=ticker,
                message="Yahoo Finance request failed.",
            )
        except (ValueError, ValidationError, OverflowError, OSError) as error:
            logger.warning("Invalid Yahoo Finance response for %s: %s", ticker, error)
            return StockFetchFailure(
                ticker=ticker,
                message="Invalid response from Yahoo Finance.",
            )


def _parse_yahoo_response(ticker: str, payload: Any) -> StockDetails:
    if not isinstance(payload, dict):
        raise ValueError("Response body is not an object.")
    if not payload:
        raise ValueError("Yahoo Finance returned no quote details.")

    market_time = _parse_market_time(payload.get("regularMarketTime"))

    return StockDetails(
        ticker=ticker,
        name=payload.get("longName") or payload.get("shortName"),
        exchange=payload.get("exchange"),
        currency=payload.get("currency"),
        quote_type=payload.get("quoteType"),
        price=payload.get("currentPrice") or payload.get("regularMarketPrice"),
        previous_close=payload.get("previousClose"),
        market_cap=payload.get("marketCap"),
        pe_ratio=payload.get("trailingPE"),
        forward_pe=payload.get("forwardPE"),
        day_high=payload.get("dayHigh"),
        day_low=payload.get("dayLow"),
        volume=payload.get("volume") or payload.get("regularMarketVolume"),
        market_time=market_time,
    )


def _parse_market_time(value: Any) -> datetime | None:
    if value is None:
        return None
    if isinstance(value, datetime):
        return value
    if isinstance(value, str):
        return datetime.fromisoformat(value)
    if isinstance(value, int | float):
        return datetime.fromtimestamp(value, tz=UTC)
    raise ValueError("Yahoo Finance returned an invalid market time.")
