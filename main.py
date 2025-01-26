from fastapi import FastAPI, HTTPException
import requests
from bs4 import BeautifulSoup
import logging

logging.basicConfig(level=logging.INFO)

app = FastAPI()

currencies = {
    "USD (US Dollar)": "price_dollar_rl",
    "EUR (Euro)": "price_eur",
    "AED (UAE Dirham)": "price_aed",
    "GBP (British Pound)": "price_gbp",
    "TRY (Turkish Lira)": "price_try",
    "CHF (Swiss Franc)": "price_chf",
    "CNY (Chinese Yuan)": "price_cny",
    "JPY (Japanese Yen)": "price_jpy",
    "KRW (South Korean Won)": "price_krw",
    "CAD (Canadian Dollar)": "price_cad",
    "AUD (Australian Dollar)": "price_aud",
    "NZD (New Zealand Dollar)": "price_nzd",
    "SGD (Singapore Dollar)": "price_sgd",
    "INR (Indian Rupee)": "price_inr",
    "PKR (Pakistani Rupee)": "price_pkr",
    "IQD (Iraqi Dinar)": "price_iqd",
    "SYP (Syrian Pound)": "price_syp",
    "AFN (Afghan Afghani)": "price_afn",
    "DKK (Danish Krone)": "price_dkk",
    "SEK (Swedish Krona)": "price_sek",
    "NOK (Norwegian Krone)": "price_nok",
    "SAR (Saudi Riyal)": "price_sar",
    "QAR (Qatari Riyal)": "price_qar",
    "OMR (Omani Rial)": "price_omr",
    "KWD (Kuwaiti Dinar)": "price_kwd",
    "BHD (Bahraini Dinar)": "price_bhd",
    "MYR (Malaysian Ringgit)": "price_myr",
    "THB (Thai Baht)": "price_thb",
    "HKD (Hong Kong Dollar)": "price_hkd",
    "RUB (Russian Ruble)": "price_rub",
    "AZN (Azerbaijani Manat)": "price_azn",
    "AMD (Armenian Dram)": "price_amd",
    "GEL (Georgian Lari)": "price_gel",
    "KGS (Kyrgyzstani Som)": "price_kgs",
    "TJS (Tajikistani Somoni)": "price_tjs",
    "TMT (Turkmenistani Manat)": "price_tmt"
}

currency_code_to_name = {
    "USD": "USD (US Dollar)",
    "EUR": "EUR (Euro)",
    "AED": "AED (UAE Dirham)",
    "GBP": "GBP (British Pound)",
    "TRY": "TRY (Turkish Lira)",
    "CHF": "CHF (Swiss Franc)",
    "CNY": "CNY (Chinese Yuan)",
    "JPY": "JPY (Japanese Yen)",
    "KRW": "KRW (South Korean Won)",
    "CAD": "CAD (Canadian Dollar)",
    "AUD": "AUD (Australian Dollar)",
    "NZD": "NZD (New Zealand Dollar)",
    "SGD": "SGD (Singapore Dollar)",
    "INR": "INR (Indian Rupee)",
    "PKR": "PKR (Pakistani Rupee)",
    "IQD": "IQD (Iraqi Dinar)",
    "SYP": "SYP (Syrian Pound)",
    "AFN": "AFN (Afghan Afghani)",
    "DKK": "DKK (Danish Krone)",
    "SEK": "SEK (Swedish Krona)",
    "NOK": "NOK (Norwegian Krone)",
    "SAR": "SAR (Saudi Riyal)",
    "QAR": "QAR (Qatari Riyal)",
    "OMR": "OMR (Omani Rial)",
    "KWD": "KWD (Kuwaiti Dinar)",
    "BHD": "BHD (Bahraini Dinar)",
    "MYR": "MYR (Malaysian Ringgit)",
    "THB": "THB (Thai Baht)",
    "HKD": "HKD (Hong Kong Dollar)",
    "RUB": "RUB (Russian Ruble)",
    "AZN": "AZN (Azerbaijani Manat)",
    "AMD": "AMD (Armenian Dram)",
    "GEL": "GEL (Georgian Lari)",
    "KGS": "KGS (Kyrgyzstani Som)",
    "TJS": "TJS (Tajikistani Somoni)",
    "TMT": "TMT (Turkmenistani Manat)"
}

def get_live_price(currency_row):
    price_cell = currency_row.find('td', {'class': 'nf'})
    if price_cell:
        live_price = price_cell.text.strip()
        return float(live_price.replace(',', '')) / 10
    return None

@app.get("/currency-prices")
def fetch_currency_prices():
    url = "https://www.tgju.org/currency"
    headers = {
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching currency data: {e}")
        raise HTTPException(status_code=500, detail="Error fetching currency data")

    soup = BeautifulSoup(response.text, 'html.parser')
    live_prices = {}

    for currency_name, market_row in currencies.items():
        currency_row = soup.find('tr', {'data-market-row': market_row})
        if currency_row:
            live_prices[currency_name] = get_live_price(currency_row)
        else:
            live_prices[currency_name] = None

    return live_prices

@app.get("/exchange-rate")
def calculate_exchange_rate(currency1: str, currency2: str):
    if currency1 in currency_code_to_name:
        currency1 = currency_code_to_name[currency1]
    if currency2 in currency_code_to_name:
        currency2 = currency_code_to_name[currency2]

    if currency1 not in currencies or currency2 not in currencies:
        raise HTTPException(status_code=404, detail="Currency not found. Use /currencies to see available currencies.")

    prices = fetch_currency_prices()

    price1 = prices.get(currency1)
    price2 = prices.get(currency2)

    if price1 is None or price2 is None:
        raise HTTPException(status_code=404, detail="Could not fetch prices for the selected currencies.")

    exchange_rate = price1 / price2
    return {"exchange_rate": exchange_rate}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)