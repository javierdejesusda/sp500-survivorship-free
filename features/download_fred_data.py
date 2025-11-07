import os
import pandas as pd
from fredapi import Fred
from dotenv import load_dotenv
from datetime import date

SERIES_CONFIG = {
    'sp500_price': 'SP500',
    'vix_close': 'VIXCLS',
    'treasury_yield_10y': 'DGS10',
    'treasury_yield_2y': 'DGS2',
    'federal_funds_rate': 'FEDFUNDS',
    'breakeven_inflation_10y': 'T10YIE',
    'cpi': 'CPIAUCSL',
    'wti_oil_price': 'DCOILWTICO',
    'trade_weighted_dollar_index': 'DTWEXBGS',
    'unemployment_rate': 'UNRATE',
    'industrial_production_index': 'INDPRO'
}

START_DATE = '1990-01-01'
END_DATE = date.today().strftime('%Y-%m-%d')

OUTPUT_CSV_PATH = 'macro_data_fred.csv'


def initialize_fred_client():
    """
    Inicializa el cliente de la API de Fred usando una clave de API de las variables de entorno.
    
    Retorna:
        Fred: Una instancia del cliente Fred.
    
    Lanza (Raises):
        ValueError: Si la FRED_API_KEY no se encuentra en las variables de entorno.
    """
    load_dotenv()
    api_key = os.getenv('FRED_API_KEY')
    if not api_key:
        raise ValueError("FRED_API_KEY not found in environment variables.")
    
    try:
        return Fred(api_key=api_key)
    except Exception as e:
        print(f"Error al inicializar el cliente FRED: {e}")
        exit()


def download_fred_series(fred_client, series_dict, start, end):
    """
    Descarga múltiples series de FRED y las combina en un único DataFrame.

    Args:
        fred_client (Fred): El cliente Fred inicializado.
        series_dict (dict): Un diccionario que mapea los nombres de columna a los IDs de serie de FRED.
        start (str): La fecha de inicio para la descarga de datos (YYYY-MM-DD).
        end (str): La fecha de finalización para la descarga de datos (YYYY-MM-DD).

    Retorna:
        pd.DataFrame: Un DataFrame que contiene todas las series descargadas, unidas.
    """
    print(f"Descargando datos desde {start} hasta {end}...")
    
    all_series = []
    for column_name, series_id in series_dict.items():
        try:
            series_data = fred_client.get_series(series_id, observation_start=start, observation_end=end)
            df_series = series_data.to_frame(name=column_name)
            all_series.append(df_series)
            print(f" Descargado exitosamente '{series_id}' como '{column_name}'.")
        except Exception as e:
            print(f"No se pudo descargar {series_id}. Error: {e}")
            
    if not all_series:
        print("No se descargó ningún dato. Saliendo.")
        return pd.DataFrame()

    return pd.concat(all_series, axis=1, join='outer')


def process_and_clean_data(df):
    """
    Procesa y limpia los datos macroeconómicos combinados. Esto incluye configurar el
    índice y rellenar los valores faltantes hacia adelante y hacia atrás.

    Args:
        df (pd.DataFrame): El DataFrame bruto con datos de FRED.

    Retorna:
        pd.DataFrame: Un DataFrame limpio y procesado.
    """
    if df.empty:
        return df
        
    df.index = pd.to_datetime(df.index)
    df.index.name = 'date'
    
    df_processed = df.ffill()
    
    df_processed = df_processed.bfill()
    
    df_processed = df_processed.dropna()
    
    return df_processed


def main():
    fred_client = initialize_fred_client()
    
    raw_df = download_fred_series(fred_client, SERIES_CONFIG, START_DATE, END_DATE)
    
    if raw_df.empty:
        return
        
    cleaned_df = process_and_clean_data(raw_df)

    if cleaned_df.empty:
        print("El DataFrame está vacío después de la limpieza. No se guardará ningún archivo.")
        return

    try:
        cleaned_df.to_csv(OUTPUT_CSV_PATH)
        print(f"\nDatos guardados exitosamente en: {OUTPUT_CSV_PATH}")
    except Exception as e:
        print(f"\nERROR: No se pudo guardar el archivo CSV. Error: {e}")


if __name__ == "__main__":
    main()