from app.utils.handle_json_file import read_json_file
import os
from fastapi import HTTPException, status

def validate(country: str):
    # Load countries from json file in app/movies/validator/countries.json
    countries = read_json_file("countries.json", os.path.join(
        os.getcwd(), "app", "movies", "validator"))
    country_upper = country.upper()
    for c in countries:
        if c["code"] == country_upper:
            return True
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid country")

    