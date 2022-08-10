import yfinance as yf
import streamlit as st
import datetime
import plotly.graph_objects as go

st.title("주식 차트")

ticker = st.text_input("티커 입력 > ")
data = yf.Ticker(ticker)
today = datetime.datetime.today().strftime("%Y-%m-%d")
df = data.history(period="1mo", start="2015-01-01", end=today)

st.dataframe(df)
st.write("## 종가 기준")
st.line_chart(df["Close"])

st.write("## 거래량 기준")
st.bar_chart(df["Volume"])

st.write("## 종합")
candle = go.Candlestick(x=df.index, open=df["Open"],
                        close=df["Close"], high=df["High"],
                        low=df["Low"])
layout = go.Layout(yaxis={"fixedrange": False})
fig = go.Figure(data=[candle], layout=layout)
st.plotly_chart(fig)
