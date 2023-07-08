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

## API Endpoints

The following API endpoints are available:

<!-- In Progress -->

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