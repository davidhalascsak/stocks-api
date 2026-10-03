from datetime import datetime

from pydantic import BaseModel


class StockDetails(BaseModel):
    ticker: str
    name: str | None = None
    exchange: str | None = None
    currency: str | None = None
    quote_type: str | None = None
    price: float | None = None
    previous_close: float | None = None
    market_cap: float | None = None
    pe_ratio: float | None = None
    forward_pe: float | None = None
    day_high: float | None = None
    day_low: float | None = None
    volume: int | None = None
    market_time: datetime | None = None


class StockFetchFailure(BaseModel):
    ticker: str
    message: str


class StockDetailsListResponse(BaseModel):
    stocks: list[StockDetails]
    failures: list[StockFetchFailure]
