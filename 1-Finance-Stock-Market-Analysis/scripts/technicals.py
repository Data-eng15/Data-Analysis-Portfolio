def moving_averages(df, windows=[50, 200]):
    for window in windows:
        df[f"MA_{window}"] = df.groupby('Symbol')['Close'].transform(lambda x: x.rolling(window).mean())
    return df

def rsi(df, window=14):
    delta = df['Close'].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(window).mean()
    avg_loss = loss.rolling(window).mean()
    rs = avg_gain / avg_loss
    df['RSI'] = 100 - (100 / (1 + rs))
    return df

def bollinger_bands(df, window=20):
    ma = df['Close'].rolling(window).mean()
    std = df['Close'].rolling(window).std()
    df['Bollinger_Upper'] = ma + 2 * std
    df['Bollinger_Lower'] = ma - 2 * std
    return df

def macd(df, short_window=12, long_window=26, signal_window=9):
    df['EMA_12'] = df.groupby('Symbol')['Close'].transform(lambda x: x.ewm(span=short_window, adjust=False).mean())
    df['EMA_26'] = df.groupby('Symbol')['Close'].transform(lambda x: x.ewm(span=long_window, adjust=False).mean())
    df['MACD'] = df['EMA_12'] - df['EMA_26']
    df['MACD_Signal'] = df.groupby('Symbol')['MACD'].transform(lambda x: x.ewm(span=signal_window, adjust=False).mean())
    return df

def calculate_volatility(df, symbol):
    stock = df[df['Symbol'] == symbol].copy()
    stock['Return'] = stock['Close'].pct_change()
    volatility = stock['Return'].std() * (252 ** 0.5) * 100  # Annualized volatility in %
    return round(volatility, 2)


def calculate_cagr(df, symbol):
    stock = df[df['Symbol'] == symbol].copy()
    stock = stock.sort_values('Date')
    start_price = stock['Close'].iloc[0]
    end_price = stock['Close'].iloc[-1]
    n_years = (stock['Date'].iloc[-1] - stock['Date'].iloc[0]).days / 365
    cagr = ((end_price / start_price) ** (1 / n_years) - 1) * 100
    return round(cagr, 2)
