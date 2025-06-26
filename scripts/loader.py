import pandas as pd

def load_and_clean_data(filepath):
    df = pd.read_csv(filepath, parse_dates=['Date'])
    df = df[df['Series'] == 'EQ']
    df.sort_values(by=['Symbol', 'Date'], inplace=True)
    df.reset_index(drop=True, inplace=True)
    numeric_cols = ['Prev Close', 'Open', 'High', 'Low', 'Last', 'Close',
                    'VWAP', 'Volume', 'Turnover', 'Trades', 'Deliverable Volume', '%Deliverble']
    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')
    df.dropna(inplace=True)
    return df