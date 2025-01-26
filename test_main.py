import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_fetch_currency_prices_success(requests_mock):
    """Test that fetching currency prices works correctly."""
    requests_mock.get(
        "https://www.tgju.org/currency",
        text="""
        <html>
        <body>
        <tr data-market-row="price_dollar_rl"><td class="nf">300,000</td></tr>
        <tr data-market-row="price_eur"><td class="nf">320,000</td></tr>
        </body>
        </html>
        """
    )

    response = client.get("/currency-prices")
    assert response.status_code == 200
    data = response.json()
    assert data["USD (US Dollar)"] == 30000.0
    assert data["EUR (Euro)"] == 32000.0

def test_fetch_currency_prices_failure(requests_mock):
    """Test that API returns an error if the currency website is down."""
    requests_mock.get("https://www.tgju.org/currency", status_code=500)
    response = client.get("/currency-prices")
    assert response.status_code == 500
    assert response.json()["detail"] == "Error fetching currency data"

def test_calculate_exchange_rate_success(requests_mock):
    """Test the exchange rate calculation."""
    requests_mock.get(
        "https://www.tgju.org/currency",
        text="""
        <html>
        <body>
        <tr data-market-row="price_dollar_rl"><td class="nf">300,000</td></tr>
        <tr data-market-row="price_eur"><td class="nf">320,000</td></tr>
        </body>
        </html>
        """
    )

    response = client.get("/exchange-rate?currency1=USD&currency2=EUR")
    assert response.status_code == 200
    data = response.json()
    assert data["exchange_rate"] == pytest.approx(30000.0 / 32000.0, rel=1e-2)

def test_calculate_exchange_rate_missing_params():
    """Test that missing parameters are handled correctly."""
    response = client.get("/exchange-rate")
    assert response.status_code == 422

def test_calculate_exchange_rate_invalid_currency():
    """Test that invalid currencies are handled correctly."""
    response = client.get("/exchange-rate?currency1=INVALID&currency2=USD")
    assert response.status_code == 404
    assert response.json()["detail"] == "Currency not found. Use /currencies to see available currencies."

def test_accuracy_of_exchange_rate(requests_mock):
    """Test the accuracy of exchange rate calculation."""
    requests_mock.get(
        "https://www.tgju.org/currency",
        text="""
        <html>
        <body>
        <tr data-market-row="price_dollar_rl"><td class="nf">300,000</td></tr>
        <tr data-market-row="price_eur"><td class="nf">320,000</td></tr>
        </body>
        </html>
        """
    )

    response = client.get("/exchange-rate?currency1=USD&currency2=EUR")
    assert response.status_code == 200
    data = response.json()
    assert data["exchange_rate"] == pytest.approx(0.9375, rel=1e-2)