import pandas as pd
import numpy as np

def calculate_beta(df, stock_symbol, index_symbol="NIFTY 50"):
    stock_df = df[df['Symbol'] == stock_symbol].copy()
    index_df = df[df['Symbol'] == index_symbol].copy()

    if stock_df.empty or index_df.empty:
        return None

    # Ensure date alignment
    merged = pd.merge(
        stock_df[['Date', 'Close']].rename(columns={'Close': 'Stock_Close'}),
        index_df[['Date', 'Close']].rename(columns={'Close': 'Index_Close'}),
        on='Date', how='inner'
    )

    merged['Stock_Return'] = merged['Stock_Close'].pct_change()
    merged['Index_Return'] = merged['Index_Close'].pct_change()

    covariance = np.cov(merged['Stock_Return'].dropna(), merged['Index_Return'].dropna())[0][1]
    variance = np.var(merged['Index_Return'].dropna())

    beta = covariance / variance if variance != 0 else np.nan
    return round(beta, 3)

def correlation_matrix(df, top_n=10):
    pivot = df.pivot_table(index='Date', columns='Symbol', values='Close')
    returns = pivot.pct_change()
    corr_matrix = returns.corr().round(2)
    return corr_matrix