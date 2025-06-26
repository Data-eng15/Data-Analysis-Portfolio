import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import sys
import os

# Set up paths
sys.path.append('scripts')

from loader import load_and_clean_data
from technicals import moving_averages, rsi, macd, bollinger_bands
from plots import plot_stock_trend, plot_macd

# Page config
st.set_page_config(page_title="NIFTY50 Dashboard", layout="wide")

# Title
st.title("📊 NIFTY50 Stock Dashboard (2000–2021)")

# Load data
@st.cache_data
def load_data():
    df = load_and_clean_data('data/NIFTY50_all.csv')
    df = moving_averages(df)
    df = rsi(df)
    df = macd(df)
    df = bollinger_bands(df)
    return df

df = load_data()
symbols = df['Symbol'].unique()

# Sidebar
st.sidebar.header("Select Stock")
selected_symbol = st.sidebar.selectbox("Symbol", sorted(symbols))

# Date Range
min_date = df['Date'].min()
max_date = df['Date'].max()
date_range = st.sidebar.date_input("Date Range", [min_date, max_date], min_value=min_date, max_value=max_date)

filtered_df = df[(df['Symbol'] == selected_symbol) & 
                 (df['Date'] >= pd.to_datetime(date_range[0])) & 
                 (df['Date'] <= pd.to_datetime(date_range[1]))]

# Tabs for visualizations
tab1, tab2 = st.tabs(["📈 Price + Indicators", "📉 MACD"])

with tab1:
    st.subheader(f"{selected_symbol} Price & Technical Indicators")
    fig, ax = plt.subplots(figsize=(14, 6))
    ax.plot(filtered_df['Date'], filtered_df['Close'], label='Close Price')
    if 'MA_50' in filtered_df.columns:
        ax.plot(filtered_df['Date'], filtered_df['MA_50'], label='50-Day MA')
    if 'MA_200' in filtered_df.columns:
        ax.plot(filtered_df['Date'], filtered_df['MA_200'], label='200-Day MA')
    if 'Bollinger_Upper' in filtered_df.columns:
        ax.plot(filtered_df['Date'], filtered_df['Bollinger_Upper'], linestyle='--', label='Bollinger Upper')
        ax.plot(filtered_df['Date'], filtered_df['Bollinger_Lower'], linestyle='--', label='Bollinger Lower')
    ax.set_title(f"{selected_symbol} Price Trend")
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)

with tab2:
    st.subheader(f"{selected_symbol} MACD Indicator")
    fig2, ax2 = plt.subplots(figsize=(14, 6))
    ax2.plot(filtered_df['Date'], filtered_df['MACD'], label='MACD', color='blue')
    ax2.plot(filtered_df['Date'], filtered_df['MACD_Signal'], label='Signal Line', color='orange')
    ax2.axhline(0, color='gray', linestyle='--', linewidth=1)
    ax2.set_title(f"MACD for {selected_symbol}")
    ax2.set_xlabel("Date")
    ax2.set_ylabel("MACD Value")
    ax2.legend()
    ax2.grid(True)
    st.pyplot(fig2)