import app.crypto.service as service
from app.crypto.validators.get_coin_historical_data import validate as validate_get_coin_historical_data

'''
    @brief: This class is used from the routes to interact with the servicers
'''

def get_top_crypto_prices(skip: int = 0, limit: int = 10):
    return service.scrape_top_crypto_prices(skip, limit)

def get_coin_details(symbol: str):
    return service.scrape_coin_details(symbol)

def get_coin_historical_data(symbol: str, start_date: str = None, end_date: str = None):
    validate_get_coin_historical_data(start_date, end_date)
    return service.scrape_coin_historical_data(symbol, start_date, end_date)