from fastapi import APIRouter

from app.dto.stock import StockDetailsListResponse
from app.services.yahoo_finance_service import fetch_yahoo_finance_details

router = APIRouter(prefix="/api", tags=["stocks"])

@router.get("/stocks", response_model=StockDetailsListResponse)
async def list_stock_details() -> StockDetailsListResponse:
    return await fetch_yahoo_finance_details()
