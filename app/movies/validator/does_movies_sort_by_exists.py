from app.utils.handle_json_file import read_json_file
import os
from fastapi import HTTPException, status

SORT_BY = {
    "RANKING" : "rk",
    "IMDB_RATING" : "ir",
    "RELEASE_DATE" : "us",
    "NUMBER_OF_RATING": "nv",
    "YOUR_RATING": "ur",
}

def validate(sort: str):
    # Load countries from json file in app/movies/validator/countries.json
    sort_upper = sort.upper()
    for s in SORT_BY:
        if s == sort_upper:
            return True
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid sort")
