import numpy as np
import pandas as pd
from spectrum import correlation
from clean import clip, to_covariance
from portfolio import min_variance, predicted_vol

WINDOW = 504
HOLD = 21
NAMES = ["RAW", "CLEAN", "CLEAN_ADJ"]


def run_backtest(returns, window=WINDOW, hold=HOLD):
    realized = {name: [] for name in NAMES}
    predicted = {name: [] for name in NAMES}

    for start in range(window, len(returns) - hold + 1, hold):
        train = returns.iloc[start - window:start]
        test = returns.iloc[start:start + hold]

        corr = correlation(train)
        vols = train.std()
        covs = {"RAW": to_covariance(corr, vols),
                "CLEAN": to_covariance(clip(corr, window), vols),
                "CLEAN_ADJ": to_covariance(clip(corr, window, adjust=True), vols)}

        for name, cov in covs.items():
            w = min_variance(cov)
            predicted[name].append(predicted_vol(w, cov))
            realized[name].append(test.values @ w)

    return realized, predicted


if __name__ == "__main__":
    returns = pd.read_parquet("returns.parquet")
    realized, predicted = run_backtest(returns)
    print("rebalances:", len(predicted["RAW"]))

    for name in NAMES:
        daily = np.concatenate(realized[name])
        real_vol = daily.std() * np.sqrt(252)
        pred_vol = np.mean(predicted[name]) * np.sqrt(252)
        print(name)
        print("  predicted vol:", round(pred_vol, 4))
        print("  realized vol: ", round(real_vol, 4))
        print("  realized / predicted:", round(real_vol / pred_vol, 2))