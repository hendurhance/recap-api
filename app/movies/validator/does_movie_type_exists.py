import os
from fastapi import HTTPException, status

TYPES = ["MOVIE", "TV", "TV_EPISODE"]

def validate(type: str):
    if type not in TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid type")
    return True