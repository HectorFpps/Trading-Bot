import yfinance as yf
import streamlit as st
import pandas as pd
import pandas_ta as ta
from matplotlib import pyplot as plt

# “1m”, “2m”, “5m”, “15m”, “30m”, “60m”, “90m”, “1h”, “1d”, “5d”, “1wk”, “1mo”, “3mo”

# Important Info
ticker = "XRP-USD"
rsiPeriod = 14
chartPeriod = "25d"
interval = "15m"
initialBalance = 10000

#Variables
rsi = []
price = []
buyPrice = None
sellPrice = None
balance = initialBalance

def tickerPrice(price):
    df = pd.DataFrame()
    df = df.ta.ticker(ticker, period=chartPeriod, interval=interval)
    df = df.values.tolist()
    for i in range(len(df)):
        price += [df[i][3]]

def RSI(rsi):
    df = pd.DataFrame()
    df = df.ta.ticker(ticker, period=chartPeriod, interval=interval)
    rsii = df.ta.rsi(length=rsiPeriod).to_frame()
    rsii = rsii.values.tolist()

    for i in range(len(rsii)):
        rsi += [rsii[i][0]]


################################################################################################################################################################################################################################################

st.write("""# Trading Bot""")

ticker = str(st.text_input("-Input Desired Ticker (Yahoo Finance)"))
rsiPeriod = int(st.text_input("-Input Desired Rsi Period"))
buyLimit = int(st.text_input("-Input Desired Buy Limit"))
sellLimit = int(st.text_input("-Input Desired Sell Limit"))

balance_track = []
tickerPrice(price)
RSI(rsi)



inPosition = False
for i in range(len(price)):
    if(rsi[i] < buyLimit):
        # want to buy
        if(inPosition):
            pass
        else:
            inPosition = True
            buyPrice = price[i]
            #print("Buy at " + str(buyPrice))
    if(rsi[i] > sellLimit):
        #want to sell
        if(inPosition):
            inPosition = False
            sellPrice = price[i]
            #print("Selling at " + str(sellPrice))
            balance = balance * sellPrice / buyPrice
            balance_track += [balance]

st.write("#### -Trading Bot Portfolio Overtime")("The final balance is " + str(balance))
st.write("#### -Trading Bot Portfolio Overtime")("That is " +str(balance-initialBalance) + " in " + chartPeriod + " " + str((balance-initialBalance)/initialBalance*100) + "%. This ticker did " + str((price[-1]-price[0])/price[0]*100) + "% in that time.")



st.write("""
#### -Price of {ticker}
""".format(ticker=ticker))

st.line_chart(price)
st.write("#### -Trading Bot Portfolio Overtime")
st.line_chart(balance_track)
