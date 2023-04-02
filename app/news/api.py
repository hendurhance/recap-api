from fastapi import APIRouter, status
import app.news.controller as news_controller
from fastapi.requests import Request
from typing import Annotated
import app.utils.http_response as http_response
from app.core.redis_cache import cache_response, get_cached_response


router = APIRouter()

"""
    * This is the router for the crypto module
    * This route is mounted on /api/v1/news
"""

@router.get("/current")
async def get_current_news(limit: Annotated[int, 100] = 10):
    response = news_controller.get_current_news(limit)
    return http_response.success_response(response, "Successfully fetched latest news")

@router.get("/categories")
async def get_categories():
    response = news_controller.get_categories()
    return http_response.success_response(response, "Successfully fetched categories")

@router.get("/category/{category}")
async def get_news_by_category(category: str, limit: Annotated[int, 100] = 10):
    response = news_controller.get_news_by_category(category, limit)
    return http_response.success_response(response, "Successfully fetched news by category")
