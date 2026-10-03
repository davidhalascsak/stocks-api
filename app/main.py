from fastapi import FastAPI

from app.api.stocks import router as stocks_router
from app.api.tickers import router as tickers_router
from app.config.logging import configure_logging

configure_logging()

app = FastAPI()

app.include_router(tickers_router)
app.include_router(stocks_router)
