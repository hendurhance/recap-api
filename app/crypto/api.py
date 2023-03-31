from fastapi import APIRouter, status
import app.crypto.controller as crypto_controller
from fastapi.requests import Request
from typing import Annotated
import app.utils.http_response as http_response
import datetime

router = APIRouter()

"""
    * This is the router for the crypto module
    * This route is mounted on /api/v1/crypto
"""

@router.get("/current")
async def get_current_price(skip: Annotated[int, 0] = 0, limit: Annotated[int, 100] = 10):
    response = crypto_controller.get_top_crypto_prices(skip, limit)
    return http_response.success_response(response, "Successfully fetched top crypto prices")

@router.get("/coins/{symbol}")
async def get_coin_details(symbol: str):
    response = crypto_controller.get_coin_details(symbol)
    return http_response.success_response(response, "Successfully fetched coin details")

@router.get("/coins/{symbol}/historical")
async def get_coin_historical_data(symbol: str, start_date: str = (datetime.datetime.now() - datetime.timedelta(days=7)).strftime('%Y-%m-%d'), end_date: str = datetime.datetime.now().strftime('%Y-%m-%d')):
    response = crypto_controller.get_coin_historical_data(symbol, start_date, end_date)
    return http_response.success_response(response, "Successfully fetched coin historical data")


