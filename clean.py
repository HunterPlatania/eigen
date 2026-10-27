import numpy as np


def clip(corr, T, verbose=False, adjust=False):
    C = np.asarray(corr)
    N = C.shape[0]
    q = N / T
    vals, vecs = np.linalg.eigh(C)

    ceiling = (1 + np.sqrt(q)) ** 2
    if adjust:
        ceiling = ceiling * (1 - vals[-1] / N)

    signal = vals > ceiling
    noise_avg = vals[~signal].mean()
    if verbose:
        print("ceiling:", round(ceiling, 2))
        print("above ceiling:", signal.sum())
        print("noise average:", round(noise_avg, 3))
    new_vals = np.where(signal, vals, noise_avg)

    cleaned = vecs @ np.diag(new_vals) @ vecs.T
    d = np.sqrt(np.diag(cleaned))
    cleaned = cleaned / np.outer(d, d)
    return cleaned


def to_covariance(corr, vols):
    vols = np.asarray(vols)
    return np.asarray(corr) * np.outer(vols, vols)


if __name__ == "__main__":
    import pandas as pd
    from spectrum import correlation

    returns = pd.read_parquet("returns.parquet")
    corr = correlation(returns)
    cleaned = clip(corr, len(returns), verbose=True)

    print("diagonal all 1:", np.allclose(np.diag(cleaned), 1))
    print("sum of eigenvalues:", round(np.linalg.eigvalsh(cleaned).sum(), 1))
    print("stocks 0 & 1, before:", round(np.asarray(corr)[0, 1], 3),
          "after:", round(cleaned[0, 1], 3))

    vols = returns.std()
    cov_raw = to_covariance(corr, vols)
    cov_clean = to_covariance(cleaned, vols)

    annual = vols * np.sqrt(252)
    print("calmest 3:", annual.sort_values().head(3).round(3).to_dict())
    print("wildest 3:", annual.sort_values().tail(3).round(3).to_dict())
    print("raw matches pandas:", np.allclose(cov_raw, returns.cov()))