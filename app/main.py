from fastapi import FastAPI
import redis
from app.core.config import settings
from app.router.api import api_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_VERSION}/openapi.json",
    version=settings.PROJECT_VERSION, debug=True
)

r = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)

app.include_router(api_router, prefix=settings.API_VERSION)


@app.get("/", tags=["Health Check"])
def health_check():
    return {
        "name": "Recap API",
        "type": "recap-api",
        "description": "Recap API is a REST API based on data scraping built with FastAPI and Redis",
        "documentation": "/docs",
        "version": settings.PROJECT_VERSION,
    }
