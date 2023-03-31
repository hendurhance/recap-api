from app.core.redis_conn import create_redis_connection
import json


redis_con = create_redis_connection()

def cache_response(key: str, data: dict, ex: int = 60):
    redis_con.set(key, json.dumps(data), ex=ex)

def get_cached_response(key: str):
    cached_data = redis_con.get(key)
    if cached_data:
        return json.loads(cached_data)
    return None