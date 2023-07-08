# Recap API

Recap API is a REST API based on data scraping built with FastAPI and Redis. The API scrapes data from [CoinGecko](https://www.coingecko.com) for crypto, and [NBC News](https://www.nbcnews.com) for news articles. The scraped data is stored in Redis for fast retrieval.

## Getting Started

### Installation

To install the dependencies for this project, run the following command:
    
```bash
 pip install -r requirements.txt
```

### Running the API

To run the API, run the following command:
        
```bash
uvicorn app.main:app --reload
```


This will start the API server on `http://localhost:8000.`

## API Endpoints | [Swagger Documentation](http://localhost:8000/docs)

### Crypto
| Endpoint | Query Parameters | Description |
| --- | --- | --- |
| `/api/v1/crypto/current` | `limit` & `skip` | Returns a list of the current top 100 cryptocurrencies. |
| `/api/v1/crypto/coins/{symbol}` | - | Fetches the details of a specific cryptocurrency by symbol. |
| `/api/v1/crypto/coins/{symbol}/historical` | `start_date` & `end_date` | Fetches the historical data of a specific cryptocurrency by symbol. |

### Movies
| Endpoint | Query Parameters | Description |
| --- | --- | --- |
| `/api/v1/movies/upcoming` | `skip`, `limit`, `country` & `type` | Returns a list of upcoming movies based on the country and type. |
| `/api/v1/movies/top_rated` | `skip`, `limit`, `sort_type` & `sort_by` | Returns a list of top rated movies based on the sort type like rating, popularity, and sort by like ascending or descending. |
| `/api/v1/movies/movies/{movie_id}` | - | Fetches the details of a specific movie by ID using (IMDB ID). |
| `/api/v1/movies/news` | - | Returns a list of the latest news articles on movies. |
| `/api/v1/movies/box_office` | - | Returns a list of the latest box office movies. |

### News
| Endpoint | Query Parameters | Description |
| --- | --- | --- |
| `/api/v1/news/current` | `limit` | Returns a list of the latest news articles. |
| `/api/v1/news/categories` | - | Returns a list of the news categories. |
| `/api/v1/news/categories/{category}` | `limit` | Returns a list of the latest news articles by category. |


## Configuration

The API configuration is stored in the `app/core/config.py` file. You can modify the configuration by changing the values in this file or environment variables `env` file. The following configuration options are available:

```bash
cp .env.example .env
```

- `PROJECT_NAME`: The name of the project.
- `PROJECT_VERSION`: The version of the project.
- `API_VERSION`: The version of the API.
- `REDIS_HOST`: The host name or IP address of the Redis server.
- `REDIS_PORT`: The port number on which Redis is listening.
- `COINGECKO_BASE_URL`: The base URL of the CoinGecko API.

## Redis

This API uses Redis as a caching layer to improve performance. The Redis connection is created using the `redis_conn.py` module, which defines a `create_redis_connection` function that creates the Redis connection and returns the Redis client object. If the connection is successful, a success message is printed to the console. If the connection fails, an error message is logged to the console.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.