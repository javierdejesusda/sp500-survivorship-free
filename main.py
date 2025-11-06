import sys
import pandas as pd
from datetime import datetime
import argparse

import config
from data_fetchers import (
    scrape_wikipedia_data, 
    load_and_preprocess_quandl, 
    get_yfinance_data
)
from process_local_data import load_and_process_local_data

def process_and_save_data(all_tickers, quandl_dict, local_dict, output_path, correction_map, verbose=False):
    """
    Función principal que implementa la "cascada" de datos:
    1. Intenta con datos locales.
    2. Intenta Quandl.
    3. Rellena/Extiende con yfinance.
    4. Guarda incrementalmente en el archivo de salida.
    
    Retorna:
        - failed_tickers (list): Lista de tickers que no se pudieron encontrar.
        - tickers_encontrados (int): Conteo de tickers exitosos.
    """
    
    failed_tickers = []
    tickers_encontrados = 0
    
    try:
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            
            header_written = False 
            
            for i, ticker_wiki in enumerate(sorted(list(all_tickers))):
                
                full_data = None
                ticker_yf = correction_map.get(ticker_wiki, {}).get("yfinance", ticker_wiki)

                if ticker_wiki in local_dict:
                    if verbose:
                        print(f"[DEBUG] Ticker {ticker_wiki}: Encontrado en datos locales.")
                    full_data = local_dict[ticker_wiki].copy()
                
                else:
                    ticker_q = correction_map.get(ticker_wiki, {}).get("quandl", ticker_wiki)
                    df_quandl = quandl_dict.get(ticker_q, pd.DataFrame()).copy()
                    
                    df_yfinance = None
                    if not df_quandl.empty:
                        if verbose:
                            print(f"[DEBUG] Ticker {ticker_wiki}: Encontrado en Quandl.")
                        last_quandl_date = df_quandl.index.max()
                        if last_quandl_date < datetime.now() - pd.Timedelta(days=1):
                            if verbose:
                                print(f"[DEBUG] Ticker {ticker_wiki}: Intentando complementar la información con yfinance...")
                            df_yfinance = get_yfinance_data(ticker_yf, last_quandl_date, verbose)
                    else:
                        if verbose:
                            print(f"[DEBUG] Ticker {ticker_wiki}: No encontrado en Quandl. Intentando descargar la información completa con yfinance.")
                        df_yfinance = get_yfinance_data(ticker_yf, '1990-01-01', verbose)
                        
                    if not df_quandl.empty or (df_yfinance is not None and not df_yfinance.empty):
                        full_data = pd.concat([df_quandl, df_yfinance])
                        full_data = full_data[~full_data.index.duplicated(keep='first')]
                        full_data.sort_index(inplace=True)
                        if verbose and df_yfinance is not None and not df_yfinance.empty:
                            print(f"[DEBUG] Ticker {ticker_wiki}: Descargando la información completa. Datos desde {full_data.index.min().strftime('%Y-%m-%d')} hasta {full_data.index.max().strftime('%Y-%m-%d')}.")

                if full_data is not None and not full_data.empty:
                    full_data['ticker'] = ticker_yf 
                    full_data.reset_index(inplace=True) 
                    
                    cols = ['ticker', 'date', 'Open', 'High', 'Low', 'Adj Close', 'Volume']
                    
                    for col in cols:
                        if col not in full_data.columns:
                            full_data[col] = pd.NA

                    full_data = full_data[cols]
                    
                    full_data.to_csv(f, header=(not header_written), index=False, mode='a')
                    
                    header_written = True 
                    tickers_encontrados += 1
                    if verbose:
                        print(f"[INFO]: Ticker {ticker_wiki} Procesado correctamente.")
                    
                else:
                    if verbose:
                        print(f"[DEBUG] Ticker {ticker_wiki}: Falló el análisis con Quandl y yfinance.")
                    failed_tickers.append(ticker_wiki)
                if verbose:
                    print("\n")
        
        return failed_tickers, tickers_encontrados

    except Exception as e:
        if verbose:
            print(f"[ERROR] Ocurrió un error procesando los datos: {e}")
        return failed_tickers, tickers_encontrados 

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='store_true', help='Activa el modo verbose para depuración.')
    args = parser.parse_args()

    df_cambios, all_tickers_ever = scrape_wikipedia_data()
    
    quandl_data_dict = load_and_preprocess_quandl(config.QUANDL_FILE_PATH)
    local_data_dict = load_and_process_local_data('data')

    if df_cambios is None or quandl_data_dict is None or all_tickers_ever is None:
        print("Error en los pasos iniciales (Wikipedia o Quandl). Saliendo del script.")
        sys.exit(1)
        
    failed_tickers, found_count = process_and_save_data(
        all_tickers_ever,
        quandl_data_dict,
        local_data_dict,
        config.FINAL_OUTPUT_PATH,
        config.TICKER_CORRECTION_MAP,
        args.verbose
    )
    
    print(f"\nREPORTE FINAL")
    print(f"Datos encontrados y guardados para {found_count} tickers.")
    print(f"Dataset completo guardado en '{config.FINAL_OUTPUT_PATH}'.")

    if failed_tickers:
        print(f"\nDatos NO encontrados para {len(failed_tickers)} tickers.")
        print("Tickers no encontrados:")
        print(sorted(failed_tickers))
        
if __name__ == "__main__":
    main()