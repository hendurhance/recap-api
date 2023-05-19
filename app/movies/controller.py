import app.movies.service as service
from app.core.redis_cache import cache_response, get_cached_response

'''
    @brief: This file is used from the movies routes to interact with the services
'''

def get_upcoming_movies(skip: int = 0, limit: int = 10, country: str = "US", type: str = "MOVIE"):
    redis_key = f"upcoming_movies:{skip}:{limit}:{country}:{type}"
    cached_data = get_cached_response(redis_key)
    if cached_data is None:
        response = service.scrape_upcoming_movies(skip, limit, country, type)
        cache_response(redis_key, response, 60 * 60 * 24)
        return response
    return cached_data

def get_top_rated_movies(skip: int = 0, limit: int = 10, sort_by : str = "RANKING", sort_type: str = "asc", page: int = 1):
    redis_key = f"top_rated_movies:{skip}:{limit}:{sort_by}:{sort_type}:{page}"
    cached_data = get_cached_response(redis_key)
    if cached_data is None:
        response = service.scrape_top_rated_movies(skip, limit, sort_by, sort_type, page)
        cache_response(redis_key, response, 60 * 60 * 24)
        return response
    return cached_data

def get_movie_details(movie_id: str):
    redis_key = f"movie_details:{movie_id}"
    cached_data = get_cached_response(redis_key)
    if cached_data is None:
        response = service.scrape_movie_details(movie_id)
        cache_response(redis_key, response, 60 * 60 * 24)
        return response
    return cached_data

def get_movie_news():
    redis_key = f"movie_news"
    cached_data = get_cached_response(redis_key)
    if cached_data is None:
        response = service.scrape_movie_news()
        cache_response(redis_key, response, 60 * 60 * 24)
        return response
    return cached_data

def get_box_office():
    redis_key = f"box_office"
    cached_data = get_cached_response(redis_key)
    if cached_data is None:
        response = service.scrape_box_office()
        cache_response(redis_key, response, 60 * 60 * 24)
        return response
    return cached_data