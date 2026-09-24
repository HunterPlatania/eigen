import numpy as np
import pandas as pd
import yfinance as yf

SECTOR = {
    # tech
    "AAPL":"tech","MSFT":"tech","NVDA":"tech","ORCL":"tech","IBM":"tech",
    "INTC":"tech","CSCO":"tech","TXN":"tech","QCOM":"tech","ADBE":"tech",
    "CRM":"tech","AMD":"tech","MU":"tech","AMAT":"tech","ADI":"tech",
    "KLAC":"tech","LRCX":"tech","INTU":"tech",
    # communication / media
    "GOOGL":"comm","T":"comm","VZ":"comm","CMCSA":"comm","DIS":"comm",
    "NFLX":"comm","EA":"comm",
    # financials
    "JPM":"fin","BAC":"fin","WFC":"fin","C":"fin","GS":"fin","MS":"fin",
    "AXP":"fin","BLK":"fin","SCHW":"fin","USB":"fin","PNC":"fin","BK":"fin",
    "COF":"fin","MET":"fin","AIG":"fin",
    # healthcare
    "JNJ":"health","PFE":"health","MRK":"health","ABT":"health","LLY":"health",
    "BMY":"health","AMGN":"health","GILD":"health","UNH":"health","CVS":"health",
    "MDT":"health","TMO":"health","SYK":"health","ISRG":"health","VRTX":"health",
    # consumer staples
    "PG":"staples","KO":"staples","PEP":"staples","WMT":"staples","COST":"staples",
    "CL":"staples","KMB":"staples","GIS":"staples","MO":"staples","EL":"staples",
    # consumer discretionary
    "AMZN":"disc","HD":"disc","MCD":"disc","NKE":"disc","SBUX":"disc",
    "LOW":"disc","TJX":"disc","YUM":"disc","ROST":"disc","F":"disc",
    # industrials
    "GE":"indu","CAT":"indu","HON":"indu","UPS":"indu","UNP":"indu","BA":"indu",
    "MMM":"indu","DE":"indu","LMT":"indu","EMR":"indu","CSX":"indu","FDX":"indu",
    # energy
    "XOM":"energy","CVX":"energy","COP":"energy","SLB":"energy","EOG":"energy",
    "HAL":"energy","DVN":"energy",
    # materials
    "NEM":"mat","FCX":"mat","APD":"mat","ECL":"mat","SHW":"mat",
    # utilities
    "NEE":"util","DUK":"util","SO":"util","D":"util","AEP":"util",
}
TICKERS = list(SECTOR)

def download_returns(start="2010-01-01", path="returns.parquet"):
    # 1) fetch: daily adjusted closing prices for all 104 tickers since 2010
    prices = yf.download(TICKERS, start=start, auto_adjust=True)["Close"]

    # keep stocks with at least 99% of days present, then drop the rare leftover days with a hole anywhere
    good = prices.columns[prices.isna().mean() < 0.01]
    prices = prices[good].dropna(axis=0)

    # 3) convert: prices -> daily log returns. shift(1) is "yesterday's table",
    #    so prices/prices.shift(1) is today-vs-yesterday for every cell at once.
    #    The first row has no yesterday, comes out all NaN, and dropna deletes it
    rets = np.log(prices / prices.shift(1)).dropna()

    # 4) cache: save to disk so Yahoo is never needed again
    rets.to_parquet(path)

    # 5) report: T days, N survivors, and the evidence ratio
    print(f"T={len(rets)} days, N={rets.shape[1]} stocks, T/N={len(rets)/rets.shape[1]:.1f}")
    return rets

def load_returns(path="returns.parquet"):
    # every later task starts here: instant reload of the finished table
    return pd.read_parquet(path)

#python -c "from data import download_returns; download_returns()"
#python -c "import yfinance as yf; from data import TICKERS; p = yf.download(TICKERS, start='2010-01-01', auto_adjust=True)['Close']; print(p.isna().sum().sort_values(ascending=False).head(10))"