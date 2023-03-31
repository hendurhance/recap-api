import app.crypto.service as service
from app.crypto.validators.get_coin_historical_data import validate as validate_get_coin_historical_data
from app.core.redis_cache import cache_response, get_cached_response

'''
    @brief: This class is used from the routes to interact with the servicers
'''

def get_top_crypto_prices(skip: int = 0, limit: int = 10):
    redis_key = f"top_crypto_prices:{skip}:{limit}"
    cached_data = get_cached_response(redis_key)
    if cached_data is None:
        response = service.scrape_top_crypto_prices(skip, limit)
        cache_response(redis_key, response, 60 * 5)
        return response
    return cached_data

def get_coin_details(symbol: str):
    redis_key = f"coin_details:{symbol}"
    cached_data = get_cached_response(redis_key)
    if cached_data is None:
        response = service.scrape_coin_details(symbol)
        cache_response(redis_key, response, 60 * 60 * 24)
        return response
    return cached_data

def get_coin_historical_data(symbol: str, start_date: str = None, end_date: str = None):
    validate_get_coin_historical_data(start_date, end_date)
    redis_key = f"coin_historical_data:{symbol}:{start_date}:{end_date}"
    cached_data = get_cached_response(redis_key)
    if cached_data is None:
        response = service.scrape_coin_historical_data(symbol, start_date, end_date)
        cache_response(redis_key, response, 60 * 60 * 24)
        return response
    return cached_data