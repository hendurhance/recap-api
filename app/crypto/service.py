import requests
from bs4 import BeautifulSoup
from app.core.config import settings
from fastapi import HTTPException, status
import app.utils.http_response as http_response


def scrape_top_crypto_prices(skip=0, limit=10):
    try:
        url = settings.CRYPTO_URL
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        table = soup.find(
            "table", {"class": "sort table mb-0 text-sm text-lg-normal table-scrollable"})
        rows = table.find_all("tr")[1:]

        rows = rows[skip:skip+limit]

        crypto_list = []
        for row in rows:
            cells = row.find_all("td")
            name = cells[2].text.strip()
            name_symbol = cells[2].find_all("span")
            name = name_symbol[0].text.strip()
            symbol = name_symbol[1].text.strip()
            price = cells[3].text.strip()
            change = cells[4].text.strip()
            crypto_list.append({
                "name": name,
                "symbol": symbol,
                "price": price,
                "change": change
            })

        return crypto_list
    except Exception as e:
        http_response.service_unavailable_response(message=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


def scrape_coin_details(symbol):
    try:
        url = f"{settings.CRYPTO_URL}/en/coins/{symbol}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        icon = soup.find("img", {"class": "tw-rounded-full"})["src"]
        name_and_symbol = soup.find("h1", {"class": "tw-m-0 tw-text-base"}).find_all("span")
        name = name_and_symbol[0].text.strip()
        symbol = name_and_symbol[1].text.strip()

        price_data = soup.find("div", {"class": "tw-text-4xl tw-font-bold tw-my-2 tw-flex tw-items-center"}).find_all("span")
        price = price_data[0].text.strip()
        change = price_data[2].find("span").text.strip()
        
        return {
            "icon": icon,
            "name": name,
            "symbol": symbol,
            "price": price,
            "change": change
        }
    except Exception as e:
        http_response.service_unavailable_response(
            message="Something went wrong, or the coin you are looking for does not exist",
            status_code=status.HTTP_400_BAD_REQUEST
        )