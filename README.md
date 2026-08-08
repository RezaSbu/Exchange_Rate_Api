# Exchange Rate API 💱

A lightweight **FastAPI** service that scrapes **live currency prices** and computes **exchange rates** between any two currencies.

## Features

- Live prices for 36+ currencies (scraped from tgju.org)
- Currency-to-currency exchange rate calculation
- Built-in tests

## Tech Stack

- Python
- FastAPI
- BeautifulSoup (web scraping)
- pytest

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/currency-prices` | Live price for every supported currency |
| `GET` | `/exchange-rate?currency1=USD&currency2=EUR` | Exchange rate between two currencies (accepts names or codes) |

## Run Locally

```bash
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```

Interactive docs are available at `http://localhost:8000/docs`.

## Run Tests

```bash
pytest
```

## License

Free to use and modify.
