import pandas as pd
import requests
import sys
import yfinance as yf
from io import StringIO
from datetime import datetime

import config
from utils import categorize_change

def scrape_wikipedia_data():
    """
    Obtiene la lista actual de compañías del S&P 500 y el historial de cambios
    desde Wikipedia. También categoriza los cambios.
    
    Retorna:
        - df_changes (pd.DataFrame): DataFrame de cambios históricos.
        - all_tickers_ever (set): Un set con todos los tickers que han estado en el índice.
    """
    try:
        response = requests.get(config.WIKIPEDIA_URL, headers=config.REQUEST_HEADERS)
        response.raise_for_status() 
        html_content = response.text
        
        df_current = pd.read_html(StringIO(html_content), header=0)[0]
        df_changes = pd.read_html(StringIO(html_content), header=[0, 1])[1]
        
        current_tickers = set(df_current['Symbol'].tolist())
        
        original_cols = df_changes.columns
        new_cols = []
        for col in original_cols:
            if 'Date' in col[0]: 
                new_cols.append('Date')
            elif 'Added' in col[0]: 
                new_cols.append(f'Added_{col[1]}')
            elif 'Removed' in col[0]: 
                new_cols.append(f'Removed_{col[1]}')
            elif 'Reason' in col[0]: 
                new_cols.append('Reason')
            else: 
                new_cols.append('_'.join(col).strip())
        df_changes.columns = new_cols

        if 'Reason' not in df_changes.columns:
            for new_col_name in new_cols:
                if 'Reason' in new_col_name or 'Note' in new_col_name:
                    df_changes.rename(columns={new_col_name: 'Reason'}, inplace=True)
                    break
        if 'Reason' not in df_changes.columns:
             df_changes['Reason'] = pd.NA

        df_changes['Category'] = df_changes['Reason'].apply(categorize_change)
        
        df_changes['Date'] = pd.to_datetime(df_changes['Date'], errors='coerce')
        df_changes = df_changes.dropna(subset=['Date'])
        
        added = set(df_changes['Added_Ticker'].dropna().unique())
        removed = set(df_changes['Removed_Ticker'].dropna().unique())
        all_tickers_ever = current_tickers.union(added).union(removed)
        
        return df_changes, all_tickers_ever
    
    except Exception as e:
        return None, None

def load_and_preprocess_quandl(csv_path):
    """
    Carga y pre-procesa el archivo CSV masivo de Quandl en un diccionario
    para acceso rápido.
    
    Args:
        csv_path (str): Ruta al archivo WIKI_PRICES.csv
        
    Retorna:
        - quandl_data_dict (dict): Diccionario donde {ticker: DataFrame}
    """
    try:
        df_quandl = pd.read_csv(
            csv_path,
            parse_dates=['date'],
            usecols=['ticker', 'date', 'adj_open', 'adj_high', 'adj_low', 'adj_close', 'adj_volume']
        )
        df_quandl.rename(columns={
            'adj_open': 'Open',
            'adj_high': 'High',
            'adj_low': 'Low',
            'adj_close': 'Adj Close',
            'adj_volume': 'Volume'
        }, inplace=True)
        
        df_quandl.set_index('date', inplace=True) 
        
        quandl_data_dict = dict(tuple(df_quandl.groupby('ticker')))
        
        return quandl_data_dict
        
    except FileNotFoundError:
        return None
    except Exception as e:
        return None

def get_yfinance_data(ticker, start_date):
    """
    Obtiene datos de yfinance Y ESTANDARIZA el nombre del índice a 'date'.
    
    Args:
        ticker (str): Ticker a consultar.
        start_date (str o datetime): Fecha de inicio para la consulta.
        
    Retorna:
        - df (pd.DataFrame): DataFrame con los datos, o None si falla.
    """
    try:
        start_date_str = (pd.to_datetime(start_date) + pd.Timedelta(days=1)).strftime('%Y-%m-%d')
        
        df = yf.download(
            ticker,
            start=start_date_str,
            auto_adjust=False,
            progress=False
        )
        
        if df.empty:
            return None
        
        df.index.name = 'date' 
        
        df = df[['Open', 'High', 'Low', 'Adj Close', 'Volume']]
        return df
        
    except Exception as e:
        return None