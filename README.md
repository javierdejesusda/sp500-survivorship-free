# S&P 500 Dataset (Survivorship-Bias Free)

![Status](https://img.shields.io/badge/status-in%20development-yellow.svg)

## Description

The main goal of this project is to create a historical price dataset for **all** companies that have been part of the S&P 500 index, not just those currently in it.

The objective is to mitigate **survivorship bias**, a common problem in *backtesting* analyses where only the "winning" companies (those that survived in the index) are included, which can artificially inflate a strategy's results.

## Methodology

The process is divided into three main steps:

1.  **Wikipedia Scraping**: Obtains the current list of S&P 500 members and, most importantly, the table of **historical changes** (companies added and removed). This gives us a complete universe of all tickers that have belonged to the index.
2.  **Historical Load (Quandl)**: Uses a massive, static database from Quandl containing US stock price data up to 2018. This will be our historical base.
3.  **Data Cascade (yfinance)**: For each ticker, the script loads the data from Quandl (up to 2018) and then uses `yfinance` to fill in the data from 2018 to the current date.
4.  **Combination**: The data is merged and saved into a single CSV file (`sp500_precios_completos.csv`), ready for analysis.

## Main Data Source

This script depends on a massive data file that **is not included** in this repository due to its size.

**You must download the `WIKI_PRICES.csv` file from the following link:**

* **Download Link:** [**Quandl WIKI Prices US Equities on Kaggle**](https://www.kaggle.com/datasets/marketneutral/quandl-wiki-prices-us-equites)

This dataset contains historical prices up to April 11, 2018. The script is specifically designed to take this database and complete it with the most recent data.

**Place the `WIKI_PRICES.csv` file (1.8 GB) in the project's root folder before running.**

## Features

* **Survivorship-Bias Free**: Includes all historical tickers, not just current ones.
* **Change Categorization**: Classifies why a company left the index (Merger/Acquisition, Spin-off, etc.).
* **Ticker Mapping**: Includes a manual correction map in `config.py` to handle discrepancies between sources (e.g., `BF.B` vs `BF_B` vs `BF-B`).
* **Modular**: The code is separated into configuration (`config.py`), data fetching (`data_fetchers.py`), utilities (`utils.py`), and the main orchestrator (`main.py`).

## Requirements

* Python 3.8+
* The `WIKI_PRICES.csv` file (see "Main Data Source" section).

## Installation

1.  Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Download `WIKI_PRICES.csv`** from the [Kaggle link](https://www.kaggle.com/datasets/marketneutral/quandl-wiki-prices-us-equites) and place it in this project's root folder.

## Usage

Once `WIKI_PRICES.csv` is in place and the dependencies are installed, simply run the main script:

```bash
python main.py
```

## The script will run several phases:

Wikipedia Scraping: Quick.

Quandl Load: May take several minutes to load and process the WIKI_PRICES.csv file into memory.

Data Cascade: This is the longest part. The script will query the yfinance API for hundreds of tickers. This can take a considerable amount of time (possibly hours).

The final output will be saved incrementally to sp500_precios_completos.csv.

## Project Status
This project is still in development. The core logic for data collection is implemented, but data cleaning and subsequent analysis are the next steps.
