import requests
from bs4 import BeautifulSoup
from app.core.config import settings
from fastapi import HTTPException, status
import app.utils.http_response as http_response
import random
from app.movies.validator.does_countries_exists import validate as validate_country
from app.movies.validator.does_movie_type_exists import validate as validate_movie_type
from app.movies.validator.does_movies_sort_by_exists import validate as validate_movie_sort_by

def scrape_upcoming_movies(skip: int, limit: int, country: str, type: str):
    # Validate the country & type
    country_exists = validate_country(country)
    type_exists = validate_movie_type(type)
    try:
        imdb_url = settings.IMDB_BASE_URL + f"/calendar/?ref_=rlm&region={country}&type={type}"
        imdb_response = requests.get(imdb_url, headers=settings.IMDB_HEADERS)
        imdb_soup = BeautifulSoup(imdb_response.content, "html.parser")

        articles = imdb_soup.find_all("article", {"data-testid": "calendar-section"})
        movies_info = []
        for article in articles:
            date = article.find("div", {"data-testid": "release-date"})
            movies_data = article.find_all("li", {"data-testid": "coming-soon-entry"})
            for movies in movies_data:
                image = movies.find("img", {"class": "ipc-image"})
                link = movies.find("a", {"class": "ipc-metadata-list-summary-item__t"})
                title = link.text.strip()

            category_wrapper = movies.find("ul", {"class": "ipc-inline-list ipc-inline-list--show-dividers ipc-inline-list--no-wrap ipc-inline-list--inline ipc-metadata-list-summary-item__tl base"})
            categories = []
            if category_wrapper:
                for category in category_wrapper.find_all("li", {"class": "ipc-inline-list__item"}):
                    categories.append(category.text.strip())
            actor_wrapper = movies.find("ul", {"class", "ipc-inline-list ipc-inline-list--show-dividers ipc-inline-list--no-wrap ipc-inline-list--inline ipc-metadata-list-summary-item__stl base"})
            actors = []
            if actor_wrapper:
                for actor in actor_wrapper.find_all("li", {"class": "ipc-inline-list__item"}):
                    actors.append(actor.text.strip())
            
            if link and image:
                movies_info.append({"title": title, "url": 'https://www.imdb.com' + link["href"], "image": image["src"], "date": date.text.strip(), "categories": categories, "actors": actors})
        if len(movies_info) == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No movies found")
        else:
            return movies_info[skip:limit]
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Something went wrong")

def scrape_top_rated_movies(skip: int, limit: int, sort_by: str, sort_type: str, page: int):
    # Validate the sort by
    sort_by_exists = validate_movie_sort_by(sort_by)
    # try:
    #     imdb_url = settings.IMDB_BASE_URL + f"/chart/top/?sort={sort_by},{sort_type}&mode=simple&page={page}"
    #     imdb_response = requests.get(imdb_url, headers=settings.IMDB_HEADERS)
    #     imdb_soup = BeautifulSoup(imdb_response.content, "html.parser")

    #     movies_data = imdb_soup.find("tbody", {"class": "lister-list"})
    #     movies_info = []
    #     for movies in movies_data.find_all("tr"):
    #         # 