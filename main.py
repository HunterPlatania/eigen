# main.py  -- reruns everything, in order (this is what 1.13 executes)
import os
from data import load_returns, SECTOR               # download_returns() the first time
from spectrum import plot_spectrum, remove_market_mode, print_modes
from portfolio import lw_cov
from backtest import backtest, naive_cov, clipped_cov, headline

os.makedirs("figures", exist_ok=True)

rets = load_returns()
labels = {k: v for k, v in SECTOR.items() if k in rets.columns}   # survivors only
plot_spectrum(rets)                                 # 1.2
resid = remove_market_mode(rets)                    # 1.3
plot_spectrum(resid, fname="figures/spectrum_clean.png")
print_modes(resid, labels=labels)                   # 1.4
results = {
    "naive": backtest(rets, naive_cov),             # 1.9
    "clipped": backtest(rets, clipped_cov),
    "ledoit-wolf": backtest(rets, lw_cov),
}
headline(results)                                   # 1.10
for name, df in results.items():
    print(name, " realized/predicted =", round((df.realized / df.predicted).mean(), 2))