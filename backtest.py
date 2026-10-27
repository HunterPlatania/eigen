import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

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


def plot_headline(realized, predicted, path="figures/headline.png"):
    os.makedirs("figures", exist_ok=True)
    pred = [np.mean(predicted[n]) * np.sqrt(252) * 100 for n in NAMES]
    real = [np.concatenate(realized[n]).std() * np.sqrt(252) * 100 for n in NAMES]

    x = np.arange(len(NAMES))
    width = 0.36
    fig, ax = plt.subplots(figsize=(7, 4.2))
    b1 = ax.bar(x - width / 2 - 0.01, pred, width, label="Predicted", color="#2a78d6")
    b2 = ax.bar(x + width / 2 + 0.01, real, width, label="Realized (unseen days)", color="#eb6834")
    ax.bar_label(b1, fmt="%.1f%%", padding=3, fontsize=9, color="#52514e")
    ax.bar_label(b2, fmt="%.1f%%", padding=3, fontsize=9, color="#52514e")

    for i in range(len(NAMES)):
        ax.text(x[i], max(pred[i], real[i]) + 1.4, f"ratio {real[i] / pred[i]:.2f}",
                ha="center", fontsize=9, color="#0b0b0b")

    ax.set_xticks(x, ["Raw", "Clipped", "Clipped,\nmarket-adjusted"])
    ax.set_ylabel("Annualized volatility (%)")
    ax.set_ylim(0, max(real) * 1.45)
    ax.set_title("Predicted vs realized portfolio risk, 176 monthly rebalances",
                 loc="left", fontsize=11)
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", color="#e5e4e0", linewidth=0.8)
    ax.set_axisbelow(True)
    ax.legend(frameon=False, loc="upper right", ncol=2, fontsize=9)
    fig.tight_layout()
    fig.savefig(path, dpi=200)
    print("saved", path)


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

    plot_headline(realized, predicted)