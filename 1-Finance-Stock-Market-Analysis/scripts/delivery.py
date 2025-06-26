def top_deliverable_stocks(df, top_n=10):
    return df.groupby('Symbol')['%Deliverble'].mean().sort_values(ascending=False).head(top_n)

def compare_volume_delivery(df, symbol):
    stock_df = df[df['Symbol'] == symbol]
    return stock_df[['Date', 'Volume', 'Deliverable Volume', '%Deliverble']]