import requests
from bs4 import BeautifulSoup
from app.core.config import settings
from fastapi import HTTPException, status
import app.utils.http_response as http_response
import random
from app.movies.validator.does_countries_exists import validate as validate_country
from app.movies.validator.does_movie_type_exists import validate as validate_movie_type
from app.movies.validator.does_movies_sort_by_exists import validate as validate_movie_sort_by, get_sort


def scrape_upcoming_movies(skip: int, limit: int, country: str, type: str):
    # Validate the country & type
    country_exists = validate_country(country)
    type_exists = validate_movie_type(type)
    try:
        imdb_url = settings.IMDB_BASE_URL + \
            f"/calendar/?ref_=rlm&region={country}&type={type}"
        imdb_response = requests.get(imdb_url, headers=settings.IMDB_HEADERS)
        imdb_soup = BeautifulSoup(imdb_response.content, "html.parser")

        articles = imdb_soup.find_all(
            "article", {"data-testid": "calendar-section"})
        movies_info = []
        for article in articles:
            date = article.find("div", {"data-testid": "release-date"})
            movies_data = article.find_all(
                "li", {"data-testid": "coming-soon-entry"})
            for movies in movies_data:
                image = movies.find("img", {"class": "ipc-image"})
                link = movies.find(
                    "a", {"class": "ipc-metadata-list-summary-item__t"})
                title = link.text.strip()

            category_wrapper = movies.find(
                "ul", {"class": "ipc-inline-list ipc-inline-list--show-dividers ipc-inline-list--no-wrap ipc-inline-list--inline ipc-metadata-list-summary-item__tl base"})
            categories = []
            if category_wrapper:
                for category in category_wrapper.find_all("li", {"class": "ipc-inline-list__item"}):
                    categories.append(category.text.strip())
            actor_wrapper = movies.find(
                "ul", {"class", "ipc-inline-list ipc-inline-list--show-dividers ipc-inline-list--no-wrap ipc-inline-list--inline ipc-metadata-list-summary-item__stl base"})
            actors = []
            if actor_wrapper:
                for actor in actor_wrapper.find_all("li", {"class": "ipc-inline-list__item"}):
                    actors.append(actor.text.strip())

            if link and image:
                movies_info.append({"title": title, "url": 'https://www.imdb.com' +
                                   link["href"], "image": image["src"], "date": date.text.strip(), "categories": categories, "actors": actors})
        if len(movies_info) == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="No movies found")
        else:
            return movies_info[skip:limit]
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Something went wrong")


def scrape_top_rated_movies(skip: int, limit: int, sort_by: str, sort_type: str, page: int):
    # Validate the sort by
    sort_by_exists = validate_movie_sort_by(sort_by)
    sort_by = get_sort(sort_by)
    try:
        imdb_url = settings.IMDB_BASE_URL + \
            f"/chart/top/?sort={sort_by},{sort_type}&mode=simple&page={page}"
        imdb_response = requests.get(imdb_url, headers=settings.IMDB_HEADERS)
        imdb_soup = BeautifulSoup(imdb_response.content, "html.parser")

        movies_data = imdb_soup.find("tbody", {"class": "lister-list"})
        movies_info = []
        for movie in movies_data.find_all("tr"):
            image_base = movie.find("td", {"class": "posterColumn"})
            image = image_base.find("a").find("img")
            url = image_base.find("a")["href"].split("?")[0]
            title_base = movie.find("td", {"class": "titleColumn"})
            title = title_base.find("a").text.strip()
            year = title_base.find(
                "span", {"class": "secondaryInfo"}).text.strip()[1:-1]
            rating_base = movie.find(
                "td", {"class": "ratingColumn imdbRating"})
            rating = rating_base.find("strong").text.strip()
            if image is not None:
                movies_info.append({"title": title, "url": 'https://www.imdb.com' +
                                   url, "image": image["src"], "release_year": year, "rating": rating})
        if len(movies_info) == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="No movies found")
        else:
            return movies_info[skip:limit]
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Something went wrong")


def scrape_movie_details(movie_id: str):
    imdb_url = settings.IMDB_BASE_URL + f"/title/{movie_id}/"
    imdb_response = requests.get(imdb_url, headers=settings.IMDB_HEADERS)
    imdb_soup = BeautifulSoup(imdb_response.content, "html.parser")
    try:
        title_base = imdb_soup.find("h1", {"data-testid": "hero__pageTitle"})
        title = title_base.find("span").text.strip()
        image = image = imdb_soup.find("img", {"class": "ipc-image"})["src"]
        categories_base = imdb_soup.find_all(
            "a", {"class": "ipc-chip ipc-chip--on-baseAlt"})
        categories = []
        for category in categories_base:
            categories.append(category.find("span").text.strip())
        plot_base = imdb_soup.find("p", {"data-testid": "plot"})
        plot = plot_base.find("span", {"data-testid": "plot-xl"})
        principal_base = imdb_soup.find_all(
            "a", {"class": "ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link"})

        principals = []
        for pri in principal_base:
            principals.append(pri.text.strip())

        return {"title": title, "image": image, "categories": categories, "plot": plot.text.strip(), "tags": principals}
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Something went wrong")


def scrape_box_office():
    try:
        imdb_url = settings.IMDB_BASE_URL + "/chart/boxoffice"
        imdb_response = requests.get(imdb_url, headers=settings.IMDB_HEADERS)
        imdb_soup = BeautifulSoup(imdb_response.content, "html.parser")

        movies_data = imdb_soup.find("table", {"class": "chart full-width"})
        movies_info = []
        
        if movies_data is not None:
            movies_body = movies_data.find_all("tbody")

            for movie in movies_body[0].find_all("tr"):
                image_base = movie.find("td", {"class": "posterColumn"})
                image = image_base.find("a").find("img")
                url = image_base.find("a")["href"].split("?")[0]
                title_base = movie.find("td", {"class": "titleColumn"})
                title = title_base.find("a").text.strip()
                amount_base = movie.find_all("td", {"class": "ratingColumn"})
                amount = amount_base[0].text.strip()
                weeks = movie.find("td", {"class": "weeksColumn"}).text.strip()
                if image is not None:
                    movies_info.append({"image": image["src"], "url": 'https://www.imdb.com' + url, "title": title, "amount": amount, "weeks": weeks})

        if len(movies_info) == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="No movies found")
        else:
            return movies_info
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Something went wrong")
