import app.crypto.service as service

'''
    @brief: This class is used from the routes to interact with the servicers
'''

def get_top_crypto_prices(skip: int = 0, limit: int = 10):
    return service.scrape_top_crypto_prices(skip, limit)