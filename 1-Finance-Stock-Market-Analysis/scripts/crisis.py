def crisis_impact(df, symbol, start_date, end_date):
    stock_df = df[(df['Symbol'] == symbol) & (df['Date'] >= start_date) & (df['Date'] <= end_date)].copy()
    stock_df['Returns'] = stock_df['Close'].pct_change()
    return stock_df[['Date', 'Close', 'Returns']]