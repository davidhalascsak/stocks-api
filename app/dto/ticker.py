from pydantic import BaseModel, Field


class TickerListResponse(BaseModel):
    count: int = Field(..., ge=0)
    tickers: list[str]
