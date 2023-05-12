from fastapi import APIRouter, status
import app.movies.controller as movies_controller
from fastapi.requests import Request
from typing import Annotated
import app.utils.http_response as http_response
import datetime

router = APIRouter()

"""
    * This is the router for the movies module
    * This route is mounted on /api/v1/movies
"""

@router.get("/upcoming")
async def get_upcoming_movies(skip: Annotated[int, 0] = 0, limit: Annotated[int, 100] = 10, country: Annotated[str, "US"] = "US", type: Annotated[str, "MOVIE"] = "MOVIE"):
    response = movies_controller.get_upcoming_movies(skip, limit, country, type)
    return http_response.success_response(response, "Successfully fetched upcoming movies")

@router.get("/top_rated")
async def get_top_rated_movies(skip: Annotated[int, 0] = 0, limit: Annotated[int, 100] = 10, sort_by : Annotated[str, "RANKING"] = "RANKING", sort_type: Annotated[str, "asc"] = "asc", page: Annotated[int, 1] = 1):
    response = movies_controller.get_top_rated_movies(skip, limit, sort_by, sort_type, page)
    return http_response.success_response(response, "Successfully fetched top rated movies")