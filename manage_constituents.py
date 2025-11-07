import pandas as pd
import argparse
import config
from data_fetchers import scrape_sp500_data

def generate_files(current_only=False):
    """
    Genera archivos CSV relacionados con los constituyentes del S&P 500.

    Args:
        current_only (bool): Si es True, solo extrae y guarda los 
                             constituyentes actuales. Si es False, genera
                             los archivos completos de cambios históricos
                             y fechas de tickers.
    """
    df_current, df_changes, all_tickers_ever = scrape_sp500_data()

    if df_current is None:
        print("No se pudieron extraer los datos")
        return

    df_current.to_csv(config.CONSTITUENTS_PATH, index=False)
    print(f"Constituyentes actuales del S&P 500 guardados en {config.CONSTITUENTS_PATH}")

    if current_only:
        return

    df_changes.to_csv(config.HISTORICAL_CHANGES_PATH, index=False)
    print(f"Cambios históricos brutos guardados en {config.HISTORICAL_CHANGES_PATH}")

    current_tickers = set(df_current['Symbol'])

    additions = df_changes[df_changes['Added_Ticker'].notna()][['Date', 'Added_Ticker']].rename(
        columns={'Date': 'start_date', 'Added_Ticker': 'ticker'}
    )
    start_dates = additions.groupby('ticker')['start_date'].min()

    removals = df_changes[df_changes['Removed_Ticker'].notna()][['Date', 'Removed_Ticker']].rename(
        columns={'Date': 'end_date', 'Removed_Ticker': 'ticker'}
    )
    end_dates = removals.groupby('ticker')['end_date'].max()

    all_tickers_df = pd.DataFrame(list(all_tickers_ever), columns=['ticker'])
    final_df = pd.merge(all_tickers_df, start_dates, on='ticker', how='left')
    final_df = pd.merge(final_df, end_dates, on='ticker', how='left')

    final_df.loc[final_df['ticker'].isin(current_tickers), 'end_date'] = pd.NaT

    final_df = final_df.sort_values(by='ticker').reset_index(drop=True)
    final_df.to_csv(config.TICKER_DATES_PATH, index=False, date_format='%Y-%m-%d')

    print(f"Archivo de fechas de tickers generado: {config.TICKER_DATES_PATH}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generar archivos de datos de constituyentes del S&P 500 desde Wikipedia."
    )
    parser.add_argument(
        '--current-only',
        action='store_true',
        help="Si se establece, solo extrae y guarda los constituyentes actuales del S&P 500."
    )
    args = parser.parse_args()

    generate_files(args.current_only)