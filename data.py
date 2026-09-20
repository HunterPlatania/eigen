import numpy as np
import pandas as pd
import yfinance as yf

# Start from 55 and extend to ~100 tickers with full history since 2010.

# ~104 large caps, all trading under the same ticker since before 2010,
# grouped by sector so 1.4 can check the modes against reality.
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
    prices = yf.download(TICKERS, start=start, auto_adjust=True)["Close"]
    prices = prices.dropna(axis=1) # drop tickers with any gap
    rets = np.log(prices / prices.shift(1)).dropna()
    rets.to_parquet(path)
    print(f"T={len(rets)} days, N={rets.shape[1]} stocks, T/N={len(rets)/rets.shape[1]:.1f}")
    return rets

def load_returns(path="returns.parquet"):
    return pd.read_parquet(path)