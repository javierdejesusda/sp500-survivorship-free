QUANDL_FILE_PATH = "WIKI_PRICES.csv"
FINAL_OUTPUT_PATH = "sp500_precios_completos.csv"

WIKIPEDIA_URL = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
REQUEST_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}

TICKER_CORRECTION_MAP = {
    "BF.B": {"quandl": "BF_B", "yfinance": "BF-B"},
    "BRK.B": {"quandl": "BRK_B", "yfinance": "BRK-B"},

    "FNM": {"yfinance": "FNMA"},
    "FRE": {"yfinance": "FMCC"},
    "JOYG": {"quandl": "JOY", "yfinance": "JOY"},
    "SAI": {"yfinance": "SAIC"},
    "CCR": {"yfinance": "CCR.L"},
    "TSG": {"yfinance": "SABR"},
    
    # Comprada 
    # "PGN": {"yfinance": "DUK"},
    # "NVLS": {"yfinance": "LRCX"},
    # "GENZ": {"yfinance": "SNY"},
    # "DJ": {"yfinance": "NWSA"},
    # "SMS": {"yfinance": "SLB"},
    # "XTO": {"yfinance": "XOM"},
    # "CEPH": {"yfinance": "TEVA"},
    # "BJS": {"yfinance": "BKR"},
    # Merger
    # "QTRN": {"yfinance": "IQV"},
    # "CDAY": {"yfinance": "DAY"},
    
    # Omitir esta
    # "WYE": {"yfinance": "PFE"},
    # "EDS": {"yfinance": "HPQ"},
    # "AABA": {"yfinance": "VZ"},

    # Bancarrotas / Casos especiales (el historial puede no ser continuo)
    "EK": {"yfinance": "KODK"}, # El historial de EK no es continuo con KODK
    "HPH": {"yfinance": "HLT"},
    "LEH": {"yfinance": "LEHKQ"},
    
    # Caso KRFT se dividió en dos
    "KRFT": {"yfinance": "KHC"}, # KRFT (post-spin-off) se convirtió en Kraft Heinz
    "KFT": {"yfinance": "MDLZ"}
}

# Resultado de ejecución actual: 
# Datos NO encontrados para 14 tickers.
# Tickers no encontrados:
# ['BJS', 'BS', 'CDAY', 'CEPH', 'DJ', 'FSR', 'GENZ', 'LDW', 'NOVL', 'NVLS', 'PGN', 'QTRN', 'SMS', 'XTO']