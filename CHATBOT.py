# -*- coding: utf-8 -*-
"""
Created on Mon Apr 21 11:44:49 2025

@author: manan
"""

# dashboard_app.py
import streamlit as st
import yfinance as yf
from textblob import TextBlob
import matplotlib.pyplot as plt

# Setup
st.set_page_config(page_title="Stock Dashboard", layout="wide")
st.markdown("<h1 style='text-align: center;'>📊 Stock Insights</h1>", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("📘 Stock Dashboard")
stock_symbol = st.sidebar.text_input("Stock Ticker:", value="", max_chars=5)

if "portfolio" not in st.session_state:
    st.session_state.portfolio = []

if "stock_data" not in st.session_state:
    st.session_state.stock_data = None

def fetch_data(symbol):
    try:
        stock = yf.Ticker(symbol)
        data = stock.history(period="6mo")
        info = stock.info
        return stock, data, info
    except:
        return None, None, None

def analyze_sentiment(text):
    return TextBlob(text).sentiment.polarity

def show_chart(data, symbol):
    st.subheader(f"{symbol.upper()} - 6 Month Price Chart")
    fig, ax = plt.subplots()
    ax.plot(data.index, data["Close"], label="Close Price", color="cyan")
    ax.set_xlabel("Date")
    ax.set_ylabel("Price ($)")
    ax.legend()
    st.pyplot(fig)

# Sidebar Buttons
if st.sidebar.button("📊 Analyze Stock"):
    if stock_symbol:
        stock, data, info = fetch_data(stock_symbol.upper())
        if data is not None:
            st.session_state.stock_data = (stock, data, info)
            st.success(f"Analyzed {stock_symbol.upper()} successfully!")
        else:
            st.error("Invalid stock symbol!")

if st.sidebar.button("⏱ View Chart"):
    if st.session_state.stock_data:
        _, data, _ = st.session_state.stock_data
        show_chart(data, stock_symbol)
    else:
        st.warning("Analyze stock first.")

if st.sidebar.button("🔍 Get Insight"):
    if st.session_state.stock_data:
        stock, _, info = st.session_state.stock_data
        st.markdown(f"**Name:** {info.get('shortName', 'N/A')}")
        st.markdown(f"**Current Price:** ${info.get('currentPrice', 'N/A')}")
        st.markdown(f"**50-Day Avg:** ${info.get('fiftyDayAverage', 'N/A')}")
    else:
        st.warning("Analyze stock first.")

if st.sidebar.button("💵 Buy/Sell Advice"):
    if st.session_state.stock_data:
        _, _, info = st.session_state.stock_data
        price = info.get("currentPrice", 0)
        avg = info.get("fiftyDayAverage", 0)
        if isinstance(price, (int, float)) and isinstance(avg, (int, float)):
            if price < avg:
                st.success("📉 Price is below average — Might be a good time to BUY!")
            else:
                st.warning("📈 Price is high — Consider waiting or SELLING.")
        else:
            st.error("Price data not available.")
    else:
        st.warning("Analyze stock first.")

if st.sidebar.button("➕ Add to Portfolio"):
    if stock_symbol:
        st.session_state.portfolio.append(stock_symbol.upper())
        st.success(f"{stock_symbol.upper()} added to your portfolio.")
    else:
        st.warning("Enter a stock symbol first.")

# Portfolio Section
st.sidebar.markdown("---")
st.sidebar.subheader("📁 Portfolio")
if st.session_state.portfolio:
    st.sidebar.markdown(", ".join(st.session_state.portfolio))
else:
    st.sidebar.markdown("No stocks added yet")

# NLP Chat Section
st.markdown("### 💬 Chat with StockBot")
user_input = st.text_input("Ask something like 'Price of AAPL' or 'Should I buy TSLA?'")

if user_input:
    if "created by" in user_input.lower():
        st.info("👨‍💻 Created by: 12306419, 12300914, 12309825")
    else:
        sentiment = analyze_sentiment(user_input)
        symbol = user_input.upper().split()[-1]
        stock, data, info = fetch_data(symbol)
        if stock and info:
            if "price" in user_input.lower():
                st.success(f"{symbol} is currently at ${info.get('currentPrice', 'N/A')}")
            elif "buy" in user_input.lower():
                current = info.get("currentPrice", 0)
                avg = info.get("fiftyDayAverage", 0)
                if current < avg:
                    st.success("📉 Looks like a good BUY.")
                else:
                    st.warning("📈 Price is high, maybe wait.")
            elif "chart" in user_input.lower():
                show_chart(data, symbol)
            else:
                if sentiment > 0:
                    st.success("👍 Positive sentiment detected.")
                elif sentiment < 0:
                    st.warning("👎 Negative sentiment detected.")
                else:
                    st.info("😐 Neutral sentiment.")
        else:
            st.error("Couldn't analyze your input. Try something like 'Price of AAPL'.")
