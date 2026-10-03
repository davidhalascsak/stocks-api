from __future__ import annotations

from unittest.mock import AsyncMock

import pytest
from yfinance.exceptions import YFException

from app.dto.stock import StockDetailsListResponse
from app.dto.ticker import TickerListResponse
from app.services.yahoo_finance_service import (
    fetch_yahoo_finance_details,
)


@pytest.mark.asyncio
async def test_fetch_yahoo_finance_details_maps_metadata_and_symbol_format(monkeypatch):
    mock_fetch_tickers = AsyncMock(
        return_value=TickerListResponse(tickers=["BRK.B"])
    )
    monkeypatch.setattr(
        "app.services.yahoo_finance_service.fetch_sp500_tickers",
        mock_fetch_tickers,
    )
    yahoo_info = {
        "longName": "Berkshire Hathaway Inc.",
        "exchange": "NYSE",
        "currency": "USD",
        "quoteType": "EQUITY",
        "currentPrice": 500.0,
        "previousClose": 495.0,
        "volume": 1000,
        "regularMarketTime": 1_700_000_000,
        "marketCap": 500_000_000_000.0,
        "trailingPE": 10.5,
        "forwardPE": 9.8,
        "dayHigh": 501.0,
        "dayLow": 490.0,
    }

    mock_fetch_yahoo_finance_info = AsyncMock(return_value=yahoo_info)
    monkeypatch.setattr(
        "app.services.yahoo_finance_service.fetch_yahoo_finance_info",
        mock_fetch_yahoo_finance_info,
    )

    stocks = await fetch_yahoo_finance_details()

    mock_fetch_tickers.assert_awaited_once_with()
    mock_fetch_yahoo_finance_info.assert_awaited_once_with("BRK.B")
    assert isinstance(stocks, StockDetailsListResponse)
    assert stocks.failures == []
    assert stocks.stocks[0].ticker == "BRK.B"
    assert stocks.stocks[0].name == "Berkshire Hathaway Inc."
    assert stocks.stocks[0].price == 500.0
    assert stocks.stocks[0].volume == 1000
    assert stocks.stocks[0].market_cap == 500_000_000_000.0
    assert stocks.stocks[0].pe_ratio == 10.5
    assert stocks.stocks[0].forward_pe == 9.8
    assert not hasattr(stocks.stocks[0], "error")


@pytest.mark.asyncio
async def test_fetch_yahoo_finance_details_reports_individual_request_failures(monkeypatch):
    monkeypatch.setattr(
        "app.services.yahoo_finance_service.fetch_sp500_tickers",
        AsyncMock(
            return_value=TickerListResponse(
                tickers=["AAPL", "MSFT", "GOOG", "NVDA"],
            )
        ),
    )

    async def fetch_info(ticker: str):
        if ticker == "AAPL":
            return {}
        if ticker == "MSFT":
            raise YFException("rate limit")
        if ticker == "GOOG":
            raise ValueError("No quote data")
        return {"shortName": "NVIDIA Corporation"}

    mock_fetch_yahoo_finance_info = AsyncMock(side_effect=fetch_info)
    monkeypatch.setattr(
        "app.services.yahoo_finance_service.fetch_yahoo_finance_info",
        mock_fetch_yahoo_finance_info,
    )

    stocks = await fetch_yahoo_finance_details()

    assert [stock.ticker for stock in stocks.stocks] == ["NVDA"]
    assert [(failure.ticker, failure.message) for failure in stocks.failures] == [
        ("AAPL", "Invalid response from Yahoo Finance."),
        ("MSFT", "Yahoo Finance request failed."),
        ("GOOG", "Invalid response from Yahoo Finance."),
    ]
