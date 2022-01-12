import yfinance as yf
import streamlit as st
import pandas as pd
import pandas_ta as ta
from matplotlib import pyplot as plt

# “1m”, “2m”, “5m”, “15m”, “30m”, “60m”, “90m”, “1h”, “1d”, “5d”, “1wk”, “1mo”, “3mo”

# Important Info
ticker = "XRP-USD"
rsiPeriod = 14
chartPeriod = "600d"
interval = "1h"
initialBalance = 10000

#Variables
rsi = []
price = []
buyPrice = None
sellPrice = None
balance = initialBalance
buyPrices = []
sellPrices = []

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
showTrades = st.checkbox('Show trades')

balance_track = []
tickerPrice(price)
RSI(rsi)

trades = 0
inPosition = False
for i in range(len(price)):
    if(rsi[i] < buyLimit):
        # want to buy
        if(inPosition):
            pass
        else:
            inPosition = True
            buyPrice = price[i]
            buyPrices += [buyPrice]
    if(rsi[i] > sellLimit):
        #want to sell
        if(inPosition):
            inPosition = False
            sellPrice = price[i]
            sellPrices += [sellPrice]
            trades += 1
            balance = balance * sellPrice / buyPrice
            balance_track += [balance]

st.write("""
#### -Price of {ticker}
""".format(ticker=ticker))

st.line_chart(price)
st.write("#### -Trading Bot Portfolio Overtime")
st.line_chart(balance_track)

st.write("##### The final balance is " + str(round(balance)))
st.write("##### That is " +str(round(balance-initialBalance)) + "$ in " + chartPeriod + " (" + str(round((balance-initialBalance)/initialBalance*100,1)) + "%). This ticker did " + str(round((price[-1]-price[0])/price[0]*100,1)) + "% in that time.")

if(balance<initialBalance):
    st.error('This stategy is not profitable :(')
else:
    st.success('This strategy is profitable!')
    st.balloons()
    

if showTrades:
    for i in range(len(sellPrices)):
        st.write("Buy at " + str(buyPrices[i]) + " Sell at " + str(sellPrices[i]) + " Current balance: " + str(balance_track[i]) + " (" + str(sellPrices[i]/buyPrices[i]*100-100) + "%)" )
st.write("Total trades: " + str(len(sellPrices)))
