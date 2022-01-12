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
balance_track = []

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
        
def calculatePrices(buyPrices,buyPrice,sellPrices,sellPrice,balance,balance_track):
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


################################################################################################################################################################################################################################################

st.write("""# Trading Bot""")

ticker = st.selectbox(
     'Which ticker are you looking for?',
     ('eth-usd', 'ada-usd', 'btc-usd','xrp-usd','doge-usd','shib-usd','mana-usd','rose-usd','avax-usd','ltc-usd','^VIX'))
selfTrade = st.checkbox('I want a different ticker')
if(selfTrade):
    ticker = str(st.text_input("-Input Desired Ticker (Yahoo Finance)"))
    
interval = st.selectbox(
     'What candlestick inverval?',
     ('1m', '2m', '5m','15m','30m','60m','90m','1h','1d','5d','1wk','1mo','3mo'))

chartPeriod = st.selectbox(
     'How many days shoud the test last?',
     ('1h','2h','12h','1d','2d', '5d','15d','30d','60d','100d','200d','300d','400d','600d','800d'))

rsiPeriod = int(st.text_input("-Input Desired Rsi Period"))
buyLimit = int(st.text_input("-Input Desired Buy Limit"))
sellLimit = int(st.text_input("-Input Desired Sell Limit"))
showTrades = st.checkbox('Show trades')

calculatePrices(buyPrices,buyPrice,sellPrices,sellPrice,balance,balance_track)

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
    #st.balloons()
    

if showTrades:
    for i in range(len(sellPrices)):
        st.write("Buy at " + str(round(buyPrices[i])) + " Sell at " + str(round(sellPrices[i])) + " Current balance: " + str(round(balance_track[i])) + " (" + str(round(sellPrices[i]/buyPrices[i]*100-100,1)) + "%)" )
st.write("Total trades: " + str(len(sellPrices)))
