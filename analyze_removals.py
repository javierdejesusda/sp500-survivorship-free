import pandas as pd
from data_fetchers import scrape_wikipedia_data

def extract_company_info(tickers_to_find):
    """
    Extrae información sobre empresas específicas del historial de cambios del S&P 500.

    Args:
        tickers_to_find (list): Una lista de tickers a buscar.
    """
    df_changes, _ = scrape_wikipedia_data()

    if df_changes is None:
        print("No se pudo obtener el historial de cambios de Wikipedia.")
        return

    print("Información de las empresas:")
    for ticker in tickers_to_find:
        removal_info = df_changes[df_changes['Removed_Ticker'] == ticker]
        if not removal_info.empty:
            removal_date = removal_info['Date'].iloc[0]
            reason = removal_info['Reason'].iloc[0]
            company_name = removal_info['Removed_Security'].iloc[0]

            addition_info = df_changes[df_changes['Added_Ticker'] == ticker]
            addition_date = addition_info['Date'].iloc[0] if not addition_info.empty else "No encontrado"

            print(f"\nTicker: {ticker}")
            print(f"  Empresa: {company_name}")
            if isinstance(addition_date, pd.Timestamp):
                print(f"  Periodo en S&P 500: {addition_date.strftime('%Y-%m-%d')} a {removal_date.strftime('%Y-%m-%d')}")
            else:
                print(f"  Fecha de entrada: {addition_date}")
                print(f"  Fecha de salida: {removal_date.strftime('%Y-%m-%d')}")
            print(f"  Razón de la salida: {reason}")
        else:
            print(f"\nTicker: {ticker}")
            print("  No se encontró información sobre su salida.")

if __name__ == "__main__":
    tickers = ['BJS', 'BS', 'FSR', 'LDW', 'LEH', 'NOVL']
    extract_company_info(tickers)