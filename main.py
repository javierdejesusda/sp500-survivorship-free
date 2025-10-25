import sys
import pandas as pd
from datetime import datetime

import config
from data_fetchers import (
    scrape_wikipedia_data, 
    load_and_preprocess_quandl, 
    get_yfinance_data
)

def process_and_save_data(all_tickers, quandl_dict, output_path, correction_map):
    """
    Función principal que implementa la "cascada" de datos:
    1. Intenta Quandl
    2. Rellena/Extiende con yfinance
    3. Guarda incrementalmente en el archivo de salida.
    
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
                
                ticker_q = correction_map.get(ticker_wiki, {}).get("quandl", ticker_wiki)
                ticker_yf = correction_map.get(ticker_wiki, {}).get("yfinance", ticker_wiki)
                    
                df_quandl = quandl_dict.get(ticker_q, pd.DataFrame()).copy()
                
                df_yfinance = None
                if not df_quandl.empty:
                    last_quandl_date = df_quandl.index.max()
                    if last_quandl_date < datetime.now() - pd.Timedelta(days=1):
                        df_yfinance = get_yfinance_data(ticker_yf, last_quandl_date)
                else:
                    df_yfinance = get_yfinance_data(ticker_yf, '1990-01-01')
                    
                if not df_quandl.empty or (df_yfinance is not None and not df_yfinance.empty):
                    
                    full_data = pd.concat([df_quandl, df_yfinance])
                    
                    full_data = full_data[~full_data.index.duplicated(keep='first')]
                    full_data.sort_index(inplace=True)
                    
                    full_data['ticker'] = ticker_yf 
                    full_data.reset_index(inplace=True) 
                    
                    cols = ['ticker', 'date', 'Open', 'High', 'Low', 'Adj Close', 'Volume']
                    full_data = full_data[cols]
                    
                    full_data.to_csv(f, header=(not header_written), index=False, mode='a')
                    
                    header_written = True 
                    tickers_encontrados += 1
                    
                else:
                    failed_tickers.append(ticker_wiki)
        
        return failed_tickers, tickers_encontrados

    except Exception as e:
        return failed_tickers, tickers_encontrados 

def main():
    """
    Función principal que ejecuta todos los pasos.
    """
    
    df_cambios, all_tickers_ever = scrape_wikipedia_data()
    
    quandl_data_dict = load_and_preprocess_quandl(config.QUANDL_FILE_PATH)
    
    if df_cambios is None or quandl_data_dict is None or all_tickers_ever is None:
        print("Error en los pasos iniciales (Wikipedia o Quandl). Saliendo del script.")
        sys.exit(1)
        
    failed_tickers, found_count = process_and_save_data(
        all_tickers_ever,
        quandl_data_dict,
        config.FINAL_OUTPUT_PATH,
        config.TICKER_CORRECTION_MAP
    )
    
    print(f"\n--- REPORTE FINAL ---")
    print(f"Datos encontrados y guardados para {found_count} tickers.")
    print(f"Dataset completo guardado exitosamente en '{config.FINAL_OUTPUT_PATH}'.")

    if failed_tickers:
        print(f"\nDatos NO encontrados para {len(failed_tickers)} tickers.")
        print("Tickers no encontrados (nomenclatura Wikipedia):")
        print(sorted(failed_tickers))
    
    print("\nProceso finalizado.")

if __name__ == "__main__":
    main()