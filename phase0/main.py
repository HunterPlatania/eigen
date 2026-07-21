import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

tickers = ["AAPL","MSFT","GOOGL","AMZN","META","NVDA","TSLA","JPM","BAC",
  "WFC","GS","MS","C","XOM","CVX","COP","SLB","JNJ","PFE","MRK","ABBV",
  "UNH","PG","KO","PEP","WMT","COST","MCD","HD","LOW","DIS","NFLX","V",
  "MA","INTC","AMD","QCOM","TXN","CSCO","ORCL","IBM","CAT","DE","BA",
  "HON","GE","T","VZ","NEE","DUK","LIN","UPS","ADBE","CRM","ABT"]

raw = yf.download(tickers, start="2015-01-01", end="2025-01-01",
                  auto_adjust=True)["Close"]
prices = raw.dropna(axis=1)   # drop any ticker with gaps
print(prices.shape)           # expecting roughly (2500, 55)

# prices and returns ---

rets = prices.pct_change().dropna()
#print(rets.shape)
#print(rets.head())

# correlations ---

C = rets.corr().values      # a 55x55 grid of correlations
print(C.shape)
print("diagonal:", np.diag(C)[:5])   # all 1.0 - a stock is perfectly
                                     # correlated with itself

# eigen values---

eig = np.linalg.eigvalsh(C)   # 55 eigenvalues, sorted low -> high
print("smallest:", eig[0].round(3))
print("largest: ", eig[-1].round(3))
print("sum:     ", eig.sum().round(1))   # equals the # of stocks


# plot ---

T, N = rets.shape          # days, stocks
Q = T / N

# edges of the "pure noise" zone
lam_min = (1 - np.sqrt(1/Q))**2
lam_max = (1 + np.sqrt(1/Q))**2

# the Marchenko-Pastur noise curve
x  = np.linspace(lam_min, lam_max, 500)
mp = (Q / (2*np.pi)) * np.sqrt((lam_max - x)*(x - lam_min)) / x

plt.figure(figsize=(9,5))
plt.hist(eig, bins=80, range=(0,3), density=True, alpha=0.6,
         label="real eigenvalues")
plt.plot(x, mp, "r", lw=2, label="Marchenko-Pastur (pure noise)")
plt.axvline(lam_max, ls="--", color="gray")
plt.xlim(0, 3)
plt.xlabel("eigenvalue"); plt.ylabel("density"); plt.legend()
plt.title(f"largest eigenvalue = {eig[-1]:.1f}  (the market, off the chart ->)")
plt.savefig("eigen_phase0.png", dpi=150, bbox_inches="tight")
plt.show()
