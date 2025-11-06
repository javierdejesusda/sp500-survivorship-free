import pandas as pd
import os
import glob

def parse_volume(volume_str):
    """Convierte el volumen de formato '1.21M' a 1210000."""
    if isinstance(volume_str, str):
        volume_str = volume_str.strip()
        if volume_str.endswith('M'):
            return float(volume_str[:-1]) * 1_000_000
        elif volume_str.endswith('K'):
            return float(volume_str[:-1]) * 1_000
        elif volume_str == '' or volume_str == '-':
            return 0
    return float(volume_str)

def load_and_process_local_data(data_dir):
    """
    Carga y procesa archivos de datos locales desde el directorio especificado.
    """
    local_data_dict = {}
    file_mapping = {
        "Avaya Stock Price History.csv": "AV",
        "Catalent Inc Stock Price History.csv": "CTLT",
        "First Data Corp Stock Price History.csv": "FDC",
        "NYSE Euronext Stock Price History.csv": "NYX"
    }

    for filename, ticker in file_mapping.items():
        file_path = os.path.join(data_dir, filename)
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            
            df.rename(columns={
                'Date': 'date',
                'Price': 'Adj Close',
                'Vol.': 'Volume'
            }, inplace=True)

            df['date'] = pd.to_datetime(df['date'], format='%m/%d/%Y')
            df.set_index('date', inplace=True)
            
            df['Volume'] = df['Volume'].apply(parse_volume)

            for col in ['Open', 'High', 'Low', 'Adj Close', 'Volume']:
                df[col] = pd.to_numeric(df[col], errors='coerce')

            df = df[['Open', 'High', 'Low', 'Adj Close', 'Volume']]
            
            local_data_dict[ticker] = df

    return local_data_dict
