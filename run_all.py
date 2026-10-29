# run_all.py  -- reruns Phase 1 start to finish. This is what a stranger runs.
import os
import numpy as np

from data import load_returns
from spectrum import plot_spectrum, remove_market_mode
from backtest import run_backtest, plot_headline, NAMES

os.makedirs("figures", exist_ok=True)

returns = load_returns()                                      # 1.1 (downloads first time)
print("data:", returns.shape[1], "stocks,", returns.shape[0], "days")

plot_spectrum(returns)                                        # 1.2  figures/spectrum.png
resid = remove_market_mode(returns)                           # 1.3
plot_spectrum(resid, fname="figures/spectrum_clean.png")      # 1.3  figures/spectrum_clean.png

realized, predicted = run_backtest(returns)                   # 1.5, 1.6, 1.7, 1.9
print("rebalances:", len(predicted["RAW"]))
for name in NAMES:
    real_vol = np.concatenate(realized[name]).std() * np.sqrt(252)
    pred_vol = np.mean(predicted[name]) * np.sqrt(252)
    print(f"{name:10s} realized/predicted = {real_vol / pred_vol:.2f}")

plot_headline(realized, predicted)                            # 1.10 figures/headline.png