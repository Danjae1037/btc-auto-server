import pandas as pd

def load_data(filepath):
    df = pd.read_csv(filepath)
    # timestamp, open, high, low, close 컬럼은 필수
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    return df
