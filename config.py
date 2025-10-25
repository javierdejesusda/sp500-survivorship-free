QUANDL_FILE_PATH = "WIKI_PRICES.csv"
FINAL_OUTPUT_PATH = "sp500_precios_completos.csv"

WIKIPEDIA_URL = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
REQUEST_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}

TICKER_CORRECTION_MAP = {
    "BF.B": {
        "quandl": "BF_B",
        "yfinance": "BF-B"
    },
    "BRK.B": {
        "quandl": "BRK_B",
        "yfinance": "BRK-B"
    }
}