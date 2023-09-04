#!/usr/bin/env python
# coding: utf-8

# In[1]:


import yfinance as yf
import pandas as pd
import talib

# list all stocks
url = "ftp://ftp.nasdaqtrader.com/SymbolDirectory/nasdaqlisted.txt"
df = pd.read_csv(url, sep="|")
common_stock_df = df.loc[df['Market Category'] == 'S']  # filter by common stocks
print(common_stock_df.head())
print(common_stock_df['Symbol'].head())
print(len(common_stock_df['Symbol']))

def lookup_fn(df, key_row, key_col):
    try:
        return df.iloc[key_row][key_col]
    except IndexError:
        return 0

movementlist = []

for stock in common_stock_df['Symbol']:  # iterate over the common stocks
    # get history
    thestock = yf.Ticker(stock)
    hist = thestock.history(period="1mo")
    # print(stock)
    low = float(10000)
    high = float(0)
    # print(thestock.info)
    for day in hist.itertuples(index=True, name='Pandas'):
        if day.Low < low:
            low = day.Low
        if high < day.High:
            high = day.High

    deltapercent = 100 * (high - low) / low
    Open = lookup_fn(hist, 0, "Open")
    # some error handling: 
    if len(hist) >= 5:
        Close = lookup_fn(hist, 4, "Close")
    else:
        Close = Open
    if Open == 0:
        deltaprice = 0
    else:
        deltaprice = 100 * (Close - Open) / Open
    # Calculate Stochastic
    stoch_k, stoch_d = talib.STOCH(hist['High'], hist['Low'], hist['Close'], fastk_period=14, slowk_period=3, slowd_period=3)
    if stoch_d.iloc[-1] < 50:
        print(stock + " " + str(deltapercent) + " " + str(deltaprice) + " StochD: " + str(stoch_d.iloc[-1]))
        pair = [stock, deltapercent, deltaprice, stoch_d.iloc[-1]]
        movementlist.append(pair)

for entry in movementlist:
    if entry[1] > float(100):
        print(entry)


# In[6]:


# write results to a CSV file
df_results = pd.DataFrame(movementlist, columns=['Symbol', 'DeltaPercent', 'DeltaPrice', 'StochD'])
df_results.to_csv('results.csv', index=False)


# In[ ]:




