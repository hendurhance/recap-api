import redis
from app.core.config import settings


def create_redis_connection():
    try:
        r = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
        r.ping()
        print("Connected to Redis successfully!")
        return r
    except redis.exceptions.ConnectionError as e:
        print(f"Failed to connect to Redis: {e}")