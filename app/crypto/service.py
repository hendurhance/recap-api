import requests
from bs4 import BeautifulSoup
from app.core.config import settings


def scrape_top_crypto_prices(skip=0, limit=10):
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
