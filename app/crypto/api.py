from fastapi import APIRouter
import app.crypto.controller as crypto_controller

router = APIRouter()

'''
    * This is the router for the crypto module
    * This router is mounted on /api/v1/crypto
'''

@router.get("/current")
async def get_current_price(skip: int = 0, limit: int = 10):
    return crypto_controller.get_top_crypto_prices(skip, limit)