import pandas as pd

def load_data(filepath="data/btc_1min.csv"):
    return pd.read_csv(filepath)
