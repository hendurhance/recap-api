import requests
from bs4 import BeautifulSoup
from app.core.config import settings
from fastapi import HTTPException, status
import app.utils.http_response as http_response


def scrape_top_crypto_prices(skip=0, limit=10):
    try:
        url = settings.COINGECKO_BASE_URL
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
        url = f"{settings.COINGECKO_BASE_URL}/en/coins/{symbol}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        icon = soup.find("img", {"class": "tw-rounded-full"})["src"]
        name_and_symbol = soup.find("h1", {"class": "tw-m-0 tw-text-base"}).find_all("span")
        name = name_and_symbol[0].text.strip()
        symbol = name_and_symbol[1].text.strip()

        price_data = soup.find("div", {"class": "tw-text-4xl tw-font-bold tw-my-2 tw-flex tw-items-center"}).find_all("span")
        price = price_data[0].text.strip()
        change = price_data[2].find("span").text.strip()
        coin_statistics = soup.find("table", {"class": "table b-b"}).find_all("tr")
        market_cap = coin_statistics[5].find_all("td")[0].text.strip()
        market_cap_rank = coin_statistics[4].find_all("td")[0].text.strip()
        coin_info = soup.find("div", {"class": "tw-col-span-8 md:tw-pr-8 tw-mt-5 tw-mb-6 md:tw-mb-2 post-body tw-order-3"}).find_all("p")
        coin_today_summary = coin_info[0].text.strip()
        coin_detail = coin_info[1].text.strip()
        return {
            "icon": icon,
            "name": name,
            "symbol": symbol,
            "price": price,
            "change": change,
            "market_cap_rank": market_cap_rank,
            "market_cap": market_cap,
            "today_summary": coin_today_summary,
            "detail": coin_detail
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Coin with symbol {symbol} not found, please try again")


def scrape_coin_historical_data(symbol, start_date, end_date):
    try:
        url = f"{settings.COINGECKO_BASE_URL}/en/coins/{symbol}/historical_data?start_date={start_date}&end_date={end_date}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        table = soup.find("table", {"class": "table table-striped text-sm text-lg-normal"})
        rows = table.find_all("tr")[1:]

        historical_data = []
        for row in rows:
            dates = row.find_all("th", {"scope": "row"})
            columns = row.find_all("td")
            date = dates[0].text.strip()
            market_cap = columns[0].text.strip()
            volume = columns[1].text.strip()
            opening = columns[2].text.strip()
            closing = columns[3].text.strip()
            historical_data.append({
                "date": date,
                "market_cap": market_cap,
                "volume": volume,
                "opening": opening,
                "closing": closing
            })

        return historical_data
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Coin with symbol {symbol} not found, please try again")