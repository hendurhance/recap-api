from fastapi import APIRouter
from app.crypto import api as crypto_api

api_router = APIRouter()

api_router.include_router(crypto_api.router, prefix="/crypto", tags=["Crypto"])