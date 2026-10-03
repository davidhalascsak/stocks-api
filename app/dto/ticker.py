from pydantic import BaseModel


class TickerListResponse(BaseModel):
    tickers: list[str]
