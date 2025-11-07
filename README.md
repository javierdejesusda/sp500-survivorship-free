# S&P 500 Dataset (Survivorship-Bias Free)

![Status](https://img.shields.io/badge/status-in%20development-yellow.svg)

## Description

The main goal of this project is to create a historical price dataset for **all** companies that have been part of the S&P 500 index, not just those currently in it.

The objective is to mitigate **survivorship bias**, a common problem in *backtesting* analyses where only the "winning" companies (those that survived in the index) are included, which can artificially inflate a strategy's results.

## How it Works

The script follows a data cascade methodology to build the dataset:

1.  **Wikipedia Scraping**: It starts by scraping the [Wikipedia page of S&P 500 companies](https://en.wikipedia.org/wiki/List_of_S%26P_500_companies) to get two key pieces of information:
    *   The current list of S&P 500 constituents.
    *   The historical table of additions and removals, which provides a universe of all tickers that have ever been in the index.

2.  **Local Data First**: The script checks for any pre-existing historical data in the `data/` directory. This is useful for manual additions or corrections.

3.  **Historical Baseline (Quandl)**: It uses a massive, static database from Quandl (`WIKI_PRICES.csv`) containing US stock price data up to 2018. This serves as the historical base for a large number of tickers.

4.  **Recent Data (yfinance)**: For each ticker, the script determines the last available date from the Quandl data and uses the `yfinance` library to download the most recent price data, filling the gap from 2018 to the present day.

5.  **Data Consolidation**: All data is merged and saved into a single CSV file (`sp500_precios_completos.csv`), ready for analysis.

## Main Data Source

This script depends on a large data file that **is not included** in this repository due to its size.

**You must download the `WIKI_PRICES.csv` file from the following link:**

*   **Download Link:** [**Quandl WIKI Prices US Equities on Kaggle**](https://www.kaggle.com/datasets/marketneutral/quandl-wiki-prices-us-equites)

This dataset contains historical prices up to April 11, 2018. The script is designed to take this database and complete it with the most recent data.

**Place the `WIKI_PRICES.csv` file (1.8 GB) in the `data/` directory before running.**

## Features

*   **Survivorship-Bias Free**: Includes all historical tickers, not just current ones.
*   **Change Categorization**: Classifies why a company left the index (e.g., Merger/Acquisition, Spin-off).
*   **Ticker Mapping**: Includes a manual correction map in `config.py` to handle symbol discrepancies between different data sources (e.g., `BF.B` vs `BF_B` vs `BF-B`).
*   **Modular Code**: The project is organized into modules with clear responsibilities: configuration (`config.py`), data fetching (`data_fetchers.py`), constituent management (`manage_constituents.py`), local data processing (`process_local_data.py`), feature engineering (`features/`), and a main orchestrator (`main.py`).
*   **Verbose Logging**: A `--verbose` flag is available to get detailed, real-time feedback on the processing of each ticker.

## Requirements

*   Python 3.8+
*   The `WIKI_PRICES.csv` file (see "Main Data Source" section).
*   A FRED API Key for downloading macroeconomic data.

## Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/your-username/your-repo-name.git
    cd your-repo-name
    ```

2.  Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Download `WIKI_PRICES.csv`** from the [Kaggle link](https://www.kaggle.com/datasets/marketneutral/quandl-wiki-prices-us-equites) and place it in the `data/` directory.

4.  **Set up FRED API Key**:
    *   Create a file named `.env` in the root of the project.
    *   Add your FRED API key to this file as follows:
        ```
        FRED_API_KEY='your_api_key_here'
        ```

## Usage

### Main Data Pipeline

To run the main data collection and processing pipeline, execute the `main.py` script. This will generate the final `data/sp500_precios_completos.csv` file.

```bash
python main.py
```

For detailed logging, use the `--verbose` or `-v` flag:

```bash
python main.py --verbose
```

### Constituent Data Management

To generate or update the files related to the S&P 500 constituents (current list, historical changes, and ticker dates), use the `manage_constituents.py` script.

```bash
python manage_constituents.py
```

If you only need to update the current list of constituents, use the `--current-only` flag:
```bash
python manage_constituents.py --current-only
```

### Macroeconomic Feature Generation

To download a dataset of macroeconomic features from the FRED database, run the script inside the `features` directory. This will generate the `features/macro_data_fred.csv` file.

```bash
python features/download_fred_data.py
```

### Execution Phases

The script will run several phases:

1.  **Wikipedia Scraping**: Quick.
2.  **Quandl Load**: May take several minutes to load and process the `WIKI_PRICES.csv` file into memory.
3.  **Data Cascade**: This is the longest part. The script will query the `yfinance` API for hundreds of tickers. This can take a considerable amount of time (possibly hours).

At the end of the execution, a final report will be displayed with the count of successfully processed tickers and a list of any tickers for which data could not be found.

The final output will be saved incrementally to `data/sp500_precios_completos.csv`.