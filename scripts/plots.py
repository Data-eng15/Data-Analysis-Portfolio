import matplotlib.pyplot as plt

def plot_stock_trend(df, symbol):
    stock_df = df[df['Symbol'] == symbol]
    plt.figure(figsize=(14, 6))
    plt.plot(stock_df['Date'], stock_df['Close'], label='Close')
    if 'MA_50' in stock_df:
        plt.plot(stock_df['Date'], stock_df['MA_50'], label='50-Day MA')
    if 'MA_200' in stock_df:
        plt.plot(stock_df['Date'], stock_df['MA_200'], label='200-Day MA')
    if 'Bollinger_Upper' in stock_df:
        plt.plot(stock_df['Date'], stock_df['Bollinger_Upper'], linestyle='--', label='Bollinger Upper')
        plt.plot(stock_df['Date'], stock_df['Bollinger_Lower'], linestyle='--', label='Bollinger Lower')
    plt.title(f"{symbol} Price Trend")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def plot_macd(df, symbol):
    stock_df = df[df['Symbol'] == symbol]
    plt.figure(figsize=(14, 6))
    plt.plot(stock_df['Date'], stock_df['MACD'], label='MACD', color='blue')
    plt.plot(stock_df['Date'], stock_df['MACD_Signal'], label='Signal Line', color='orange')
    plt.axhline(0, color='gray', linestyle='--', linewidth=1)
    plt.title(f"MACD for {symbol}")
    plt.xlabel("Date")
    plt.ylabel("MACD Value")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()