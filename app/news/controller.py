import app.news.service as service
from app.crypto.validators.get_coin_historical_data import validate as validate_get_coin_historical_data
from app.core.redis_cache import cache_response, get_cached_response
from app.utils.handle_json_file import write_json_file
import os
'''
    @brief: This file is used from the routes to interact with the services
'''

def get_current_news(limit: int):
    redis_key = f"news:current:{limit}"
    cached_response = get_cached_response(redis_key)
    if cached_response is None:
        response = service.scrape_current_news(limit)
        cache_response(redis_key, response, 60 * 60)
        return response
    return cached_response
    
def get_categories():
    redis_key = f"news:categories"
    cached_response = get_cached_response(redis_key)
    if cached_response is None:
        response = service.scrape_categories()
        cache_response(redis_key, response, 60 * 60)
        # Save to file
        write_json_file("categories.json", os.path.join(os.getcwd(), "app", "news", "validator") , response)
        return response
    return cached_response

def get_news_by_category(category: str, limit: int):
    redis_key = f"news:category:{category}:{limit}"
    cached_response = get_cached_response(redis_key)
    if cached_response is None:
        response = service.scrape_news_by_category(category, limit)
        cache_response(redis_key, response, 60 * 60)
        return response
    return cached_response