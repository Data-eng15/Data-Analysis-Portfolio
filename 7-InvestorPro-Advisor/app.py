import streamlit as st
import pandas as pd
import numpy as np
import sys
import os
import plotly.express as px
import plotly.figure_factory as ff
from io import BytesIO

sys.path.append('scripts')
from loader import load_and_clean_data
from technicals import calculate_volatility, calculate_cagr
from advanced import calculate_beta, correlation_matrix
from scripts.pdf_export import InvestmentPDF

st.set_page_config(page_title="📊 InvestorPro Dashboard", layout="wide")

@st.cache_data
def load_data():
    df = load_and_clean_data('data/NIFTY50_all.csv')
    df['Year'] = df['Date'].dt.year
    return df

df = load_data()

st.title("🧠 InvestorPro Dashboard")
level = st.sidebar.selectbox("🎚️ Choose Your Experience Level", ["Beginner", "Intermediate", "Advanced"])
st.sidebar.markdown("---")

if level == "Beginner":
    st.header("🟢 Beginner Mode")
    risk_level = st.sidebar.radio("Risk Type", ["Conservative", "Moderate", "Aggressive"])
    years = st.sidebar.slider("Investment Duration", 1, 10, 5)
    capital = st.sidebar.number_input("💰 Amount", 1000, value=100000)
    submit = st.sidebar.button("Analyze")

    risk_map = {
        "Conservative": ["HDFCBANK", "ITC", "ASIANPAINT"],
        "Moderate": ["INFY", "TCS", "RELIANCE"],
        "Aggressive": ["ADANIENT", "BAJFINANCE", "ADANIPORTS"]
    }

    if submit:
        output = []
        for sym in risk_map[risk_level]:
            cagr = calculate_cagr(df, sym)
            projected = capital * ((1 + cagr / 100) ** years)
            output.append((sym, f"{cagr:.2f}%", f"₹{projected:,.0f}"))

        st.subheader("📈 Suggestions")
        for sym, cagr, proj in output:
            st.markdown(f"**{sym}** → CAGR: {cagr}, Return in {years}y: {proj}")

        if st.button("📥 Download PDF Summary"):
            pdf = InvestmentPDF("Beginner Investment Summary")
            pdf.add_section("Profile Info")
            pdf.add_key_value("Risk Level", risk_level)
            pdf.add_key_value("Capital", f"₹{capital}")
            pdf.add_key_value("Duration", f"{years} years")
            pdf.add_section("Recommendations")
            for sym, cagr, proj in output:
                pdf.add_key_value(sym, f"CAGR: {cagr}, Projected: {proj}")
            st.download_button("Download PDF", data=pdf.export(), file_name="Beginner_Summary.pdf", mime="application/pdf")

elif level == "Intermediate":
    st.header("🟡 Intermediate Mode")
    symbols = df['Symbol'].unique().tolist()
    symbol = st.sidebar.selectbox("Choose Stock", symbols)
    years = st.sidebar.slider("Years", 1, 10, 5)
    capital = st.sidebar.number_input("Capital", 1000, value=100000)

    cagr = calculate_cagr(df, symbol)
    vol = calculate_volatility(df, symbol)
    proj = capital * ((1 + cagr / 100) ** years)

    st.metric("CAGR", f"{cagr:.2f}%")
    st.metric("Volatility", f"{vol:.2f}%")
    st.metric("Expected Return", f"₹{proj:,.0f}")

    if st.button("📥 Download PDF Summary"):
        pdf = InvestmentPDF("Intermediate Investment Summary")
        pdf.add_section("Selection Info")
        pdf.add_key_value("Stock", symbol)
        pdf.add_key_value("CAGR", f"{cagr:.2f}%")
        pdf.add_key_value("Volatility", f"{vol:.2f}%")
        pdf.add_key_value("Projected Return", f"₹{proj:,.0f}")
        st.download_button("Download PDF", data=pdf.export(), file_name="Intermediate_Summary.pdf", mime="application/pdf")

elif level == "Advanced":
    st.header("🔴 Advanced Mode")
    symbols = sorted(df['Symbol'].unique().tolist())
    selected = st.sidebar.selectbox("Stock", symbols)
    capital = st.sidebar.number_input("Capital", 1000, value=100000)
    years = st.sidebar.slider("Years", 1, 10, 5)

    cagr = calculate_cagr(df, selected)
    vol = calculate_volatility(df, selected)
    beta = calculate_beta(df, selected)
    proj = capital * ((1 + cagr / 100) ** years)

    st.metric("CAGR", f"{cagr:.2f}%")
    st.metric("Volatility", f"{vol:.2f}%")
    st.metric("Beta vs NIFTY", f"{beta}")
    st.metric("Expected Value", f"₹{proj:,.0f}")

    st.subheader("Correlation Matrix")
    top10 = df['Symbol'].value_counts().head(10).index.tolist()
    corr_df = correlation_matrix(df[df['Symbol'].isin(top10)], top_n=10)
    fig_corr = ff.create_annotated_heatmap(z=corr_df.values, x=corr_df.columns.tolist(), y=corr_df.index.tolist(), colorscale="Viridis")
    st.plotly_chart(fig_corr, use_container_width=True)

    if st.button("📥 Download PDF Summary"):
        pdf = InvestmentPDF("Advanced Investment Summary")
        pdf.add_section("Analysis")
        pdf.add_key_value("Stock", selected)
        pdf.add_key_value("CAGR", f"{cagr:.2f}%")
        pdf.add_key_value("Volatility", f"{vol:.2f}%")
        pdf.add_key_value("Beta", f"{beta}")
        pdf.add_key_value("Projected Value", f"₹{proj:,.0f}")
        pdf.add_spacer()
        pdf.add_key_value("Correlation", "See dashboard heatmap")
        st.download_button("Download PDF", data=pdf.export(), file_name="Advanced_Summary.pdf", mime="application/pdf")