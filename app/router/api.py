from fastapi import APIRouter
from app.crypto import api as crypto_api
from app.news import api as news_api

api_router = APIRouter()

api_router.include_router(crypto_api.router, prefix="/crypto", tags=["Crypto"])
api_router.include_router(news_api.router, prefix="/news", tags=["News"])
