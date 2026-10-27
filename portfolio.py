import numpy as np


def min_variance(cov):
    cov = np.asarray(cov)
    ones = np.ones(cov.shape[0])
    raw = np.linalg.solve(cov, ones)
    return raw / raw.sum()


def predicted_vol(w, cov):
    return np.sqrt(w @ np.asarray(cov) @ w)


if __name__ == "__main__":
    import pandas as pd
    from spectrum import correlation
    from clean import clip, to_covariance

    returns = pd.read_parquet("returns.parquet")
    corr = correlation(returns)
    cleaned = clip(corr, len(returns))
    vols = returns.std()
    cov_raw = to_covariance(corr, vols)
    cov_clean = to_covariance(cleaned, vols)

    for name, cov in [("RAW", cov_raw), ("CLEAN", cov_clean)]:
        w = min_variance(cov)
        print(name)
        print("  weights sum:", round(w.sum(), 3))
        print("  biggest bet:", round(w.max(), 3), " biggest short:", round(w.min(), 3))
        print("  stocks shorted:", (w < 0).sum(), "of", len(w))
        print("  predicted annual vol:", round(predicted_vol(w, cov) * np.sqrt(252), 4))
        print("  condition number:", round(np.linalg.cond(cov)))