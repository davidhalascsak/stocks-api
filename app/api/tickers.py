from fastapi import APIRouter

from app.models.ticker import TickerListResponse
from app.services.wikipedia_service import fetch_sp500_tickers

router = APIRouter(prefix="/api", tags=["tickers"])


@router.get("/tickers", response_model=TickerListResponse)
async def list_tickers() -> TickerListResponse:
    return await fetch_sp500_tickers()
