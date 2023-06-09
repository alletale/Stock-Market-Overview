import yfinance as yf
import datetime as dt
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#*********************************************

def download_data(ticker):
    """
    Download data from yahoo finance
    """
    df = yf.download(tickers = ticker, start = start, end = end, progress = False)
    df = pd.DataFrame(df)
    
    return df

def weekly_change(df):
    """
    Do a weekly resample of daily stock price and calculate the weekly percentage change

    """
    df = df.resample("W-Fri").agg({"Open":"first",
                                         "High":"max",
                                         "Low":"min",
                                         "Close":"last"})
    df.index = df.index - to_offset("4d")
    df['pct_change'] = df.Close.pct_change()
    df.dropna(inplace = True)
    last_row = df.iloc[-1] #get the last row of the df
    value = round(last_row[-1]*100, 2)
    
    return value

def pct_change(df):
    """
    Get the latest pct change from the df and transform to a list.
    Then make it round to 2 digits.
    """
    df = df.iloc[-1] #get the last row of the df
    value = round(df[-1]*100, 2)
    
    return value

def monthly_change(df):
    """
    Do a weekly resample of daily stocks price and calculate the weekly pct change
    """
    df = df.resample("M").agg({"Open":"first",
                              "High":"max",
                              "Low":"min",
                               "Close":"last"})
    df['pct_change'] = df.Close.pct_change()
    df.dropna(inplace = True)
    last_row = df.iloc[-1] #get the last row of the df
    value = round(last_row[-1]*100, 2)
    
    return value

def quarterly_change(df):
    """
    Do a quarterly resample of daily stocks price and calculate the quarterly pct change
    """
    df = df.resample("Q").agg({"Open":"first",
                              "High":"max",
                              "Low":"min",
                               "Close":"last"})
    df['pct_change'] = df.Close.pct_change()
    df.dropna(inplace = True)
    last_row = df.iloc[-1] #get the last row of the df
    value = round(last_row[-1]*100, 2)
    
    return value

def annually_change(df):
    """
    Do a annually resample of daily stocks price and calculate the annually pct change
    """
    df = df.resample("A").agg({"Open":"first",
                              "High":"max",
                              "Low":"min",
                               "Close":"last"})
    df['pct_change'] = df.Close.pct_change()
    df.dropna(inplace = True)
    last_row = df.iloc[-1] #get the last row of the df
    value = round(last_row[-1]*100, 2)
    
    return value


##########################################

index_tickers = ["^GSPC", "^NDX","^RUT","^STOXX", "^GDAXI", "FTSEMIB.MI", "EURUSD=X", "DX-Y.NYB", "^TNX", "BTP10.MI", "CL=F", "GLD"]

start = dt.datetime(1990, 1, 1)
end = dt.datetime.now()

data = []

for ticker in index_tickers:
    daily = download_data(ticker)
    weekly = weekly_change(daily)
    monthly = monthly_change(daily)
    quarterly = quarterly_change(daily)
    annually = annually_change(daily)
    ticker_list = list([weekly, monthly,quarterly, annually])
    data.append(ticker_list)
    
#******************************************************    

index_tickers_list = ['SP500', 'NQ 100', 'RS 2k','ES 600', 'DAX','F-MIB','EUR/USD', 'DolIdx', 'TNote10Y', 'BTP10Y', 'CrudeOil', 'Gold']

index_percentages = ['WTD', 'MTD','QTD','YTD']

index_overview = pd.DataFrame(data, index_tickers_list, index_percentages)

index_tickers_tpl = ('SP500', 'NQ 100', 'RS 2k','ES 600', 'DAX','F-MIB','EUR/USD', 'DolIdx', 'TNote10Y', 'BTP10Y', 'CrudeOil', 'Gold')

#******************************************************
# Function that plot the bar chart

fig, ax = plt.subplots(figsize = (12, 6), dpi =300)

ytd_label = np.arange(len(index_tickers_list))
bar_width = 0.35
opacity = 1

#bar_container = ax.bar(index, index_overview.YTD)

rect1 = ax.bar(ytd_label, 
               index_overview.YTD,
               bar_width, 
               alpha = opacity, 
               label = "YTD % Change")

rect2 = ax.bar(ytd_label + bar_width, 
               index_overview.QTD,
               bar_width, 
               alpha = opacity, 
               label = "QTD % Change")

ax.set_xticks(ytd_label + bar_width, index_tickers_tpl)
ax.set_ylabel("Percentage Change")
ax.bar_label(rect1, label_type='edge', fmt='%r')
ax.bar_label(rect2, label_type='edge', fmt='%r')
ax.legend()

plt.grid()
plt.show()
