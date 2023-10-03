import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')
from tabulate import tabulate
import streamlit as st

# Assume you have a dictionary named stock_data_dict where you store stock data
sectors = {
    "Information Technology": ["AAPL", "MSFT", "NVDA", "TSM", "AVGO", "ORCL"],
    "Health Care": ["LLY", "UNH", "NVO", "JNJ", "ABBV", "MRK"],
    "Financials": ["BRK-B", "JPM", "V", "MA", "BAC", "WFC"],
    "Communication Services": ["GOOGL", "META", "CMCSA", "NFLX", "TMUS", "DIS"],
    "Consumer Discretionary": ["TSLA", "AMZN", "NKE", "HD", "TM", "MCD"]
}

# Fetch stock data and store in dictionary
stock_data_dict = {}
for sector, tickers in sectors.items():
    for ticker in tickers:
        stock_data = yf.download(ticker, start="2013-01-01", end="2023-01-01")
        stock_data_dict[f"{sector}_{ticker}"] = stock_data

# Function to calculate daily returns
def calculate_daily_returns(stock_df):
    stock_df['Daily_Return'] = stock_df['Close'].pct_change()
    return stock_df.dropna()

# Streamlit App
st.title('Stock Analysis Dashboard')

# Sidebar
st.sidebar.header('User Input Features')
selected_sector = st.sidebar.selectbox('Select Sector', ['All'] + list(set(stock_data_dict.keys())))

# Main
st.header('Daily and Cumulative Returns')

# Initialize an empty DataFrame for final cumulative returns
final_cumulative_returns_df = pd.DataFrame(columns=['Sector', 'Ticker', 'Final_Cumulative_Return'])

# Generate Plots and Tables
for key, stock_df in stock_data_dict.items():
    sector, ticker = key.split("_")

    if selected_sector == 'All' or selected_sector == key:
        stock_df = calculate_daily_returns(stock_df)

        # Calculate Cumulative Return and add to DataFrame
        stock_df['Cumulative_Return'] = (1 + stock_df['Daily_Return']).cumprod()
        final_cumulative_return = stock_df['Cumulative_Return'].iloc[-1]
        final_cumulative_returns_df = pd.concat(
            [final_cumulative_returns_df, pd.DataFrame([[sector, ticker, final_cumulative_return]], 
            columns=['Sector', 'Ticker', 'Final_Cumulative_Return'])],
            ignore_index=True
        )

        # Plotting
        # Plotting
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.set_title(f'Daily Returns for {ticker}')
        ax.plot(stock_df.index, stock_df['Daily_Return'])
        ax.set_xlabel('Date')
        ax.set_ylabel('Daily Return')
        st.pyplot(fig)


# Show Cumulative Returns Table
st.header('Final Cumulative Returns by Sector and Ticker')
final_cumulative_returns_df['Final_Cumulative_Return'] = final_cumulative_returns_df['Final_Cumulative_Return'].map("{:.4f}".format)
st.table(final_cumulative_returns_df)
