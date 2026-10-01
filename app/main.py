from fastapi import FastAPI

from app.config.logging import configure_logging

configure_logging()

app = FastAPI()
