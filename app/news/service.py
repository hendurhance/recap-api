import requests
from bs4 import BeautifulSoup
from app.core.config import settings
from fastapi import HTTPException, status
import app.utils.http_response as http_response
import random
from app.news.validator.does_category_exists import validate, get_source_and_url


def scrape_current_news(limit: int):
    try:
        #Fox News
        fox_url = settings.FOX_NEWS_BASE_URL
        fox_response = requests.get(fox_url)
        fox_soup = BeautifulSoup(fox_response.content, "html.parser")

        fox_headlines = []
        for article in fox_soup.find_all("article"):
            info = article.find("div", {"class": "info"})
            if info:
                header = info.find("header", {"class": "info-header"})
                if header:
                    link = header.find("a")
                    headline = link.text.strip()
                    url = link["href"].split("//")[-1].split("?")[0]
                    fox_headlines.append({"headline": headline, "url": url, "source": "Fox News"})

        # The Guardian
        guardian_url = settings.GUARDIAN_NEWS_BASE_URL
        guardian_response = requests.get(guardian_url)
        guardian_soup = BeautifulSoup(guardian_response.content, "html.parser")

        guardian_headlines = []
        for link in guardian_soup.find_all("a", {"data-link-name": "article"}):
            headline = link.text.strip()
            headline = " ".join(headline.split())
            url = link["href"]
            guardian_headlines.append({"headline": headline, "url": url, "source": "The Guardian"})
        
        #ABC News
        abc_url = settings.ABC_NEWS_BASE_URL
        abc_response = requests.get(abc_url)
        abc_soup = BeautifulSoup(abc_response.content, "html.parser")

        abc_headlines = []
        for link in abc_soup.find_all("a", {"class": "AnchorLink News__Item external flex flex-row"}):
            headline = link.text.strip()
            url = link["href"]
            abc_headlines.append({"headline": headline, "url": url, "source": "ABC News"})

        # Combine and return
        all_headlines = fox_headlines + guardian_headlines + abc_headlines
        random.shuffle(all_headlines)
        return all_headlines[:limit]
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error scraping news: {e}")

def scrape_categories():
    try:
        fox_url = settings.FOX_NEWS_BASE_URL
        fox_response = requests.get(fox_url)
        fox_soup = BeautifulSoup(fox_response.content, "html.parser")

        fox_wrapper = fox_soup.find("nav", {"id": "main-nav"})

        fox_categories = []
        for link in fox_wrapper.find_all("li", {"class": "menu-item"}):
            category = link.find("a").text.strip()
            url = link.find("a").get("href")
            fox_categories.append({"category": category, "url": url, "source": "Fox News"})

        guardian_url = settings.GUARDIAN_NEWS_BASE_URL
        guardian_response = requests.get(guardian_url)
        guardian_soup = BeautifulSoup(guardian_response.content, "html.parser")

        guardian_categories = []

        guardian_wrappers = guardian_soup.find("ul", {"class": "menu-group menu-group--primary"})

        for link in guardian_wrappers.find_all("a", {"class": "menu-item__title", "role": "menuitem"}):
            category = link.text.strip()
            url = link.get("href")
            guardian_categories.append({"category": category, "url": url, "source": "Guardian News"})

        all_categories = fox_categories + guardian_categories
        return all_categories
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error scraping news categories: {e}")


def scrape_news_by_category(category: str, limit: int):
    # Check if category is valid
    exists = validate(category)
    source, url = get_source_and_url(category)['source'], get_source_and_url(category)['url']
    # Check if source is Fox News
    if source == "Fox News":
        try:
            fox_response = requests.get(url)
            fox_soup = BeautifulSoup(fox_response.content, "html.parser")
            fox_headlines = []
            for article in fox_soup.find_all("article"):
                titles = article.find_all("h4", {"class": "title"})
                for title in titles:
                    headline = title.find("a").get_text()
                    href = title.find("a")["href"]
                    if href.startswith("http"):
                        url = href.split("//")[-1].split("?")[0]
                    else:
                        url = f"{settings.FOX_NEWS_BASE_URL}{href}"
                    fox_headlines.append({"headline": headline, "url": str(url), "source": "Fox News"})
            return fox_headlines[:limit]
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error scraping news: {e}")
    # Check if source is The Guardian
    elif source == "Guardian News":
        try:
            guardian_response = requests.get(url)
            guardian_soup = BeautifulSoup(guardian_response.content, "html.parser")
            guardian_headlines = []
            for link in guardian_soup.find_all("a", {"data-link-name": "article"}):
                headline = link.text.strip()
                headline = " ".join(headline.split())
                url = link["href"]
                guardian_headlines.append({"headline": headline, "url": url, "source": "The Guardian"})
            return guardian_headlines[:limit]
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error scraping news: {e}")
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Category not found: {category}")