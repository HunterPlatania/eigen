import numpy as np


def clip(corr, T):
    C = np.asarray(corr)
    N = C.shape[0]
    q = N / T
    ceiling = (1 + np.sqrt(q)) ** 2

    vals, vecs = np.linalg.eigh(C)
    signal = vals > ceiling
    print("ceiling:", round(ceiling, 2))
    print("above ceiling:", signal.sum())

    noise_avg = vals[~signal].mean()
    print("noise average:", round(noise_avg, 3))
    new_vals = np.where(signal, vals, noise_avg)

    cleaned = vecs @ np.diag(new_vals) @ vecs.T
    d = np.sqrt(np.diag(cleaned))
    cleaned = cleaned / np.outer(d, d)
    return cleaned


if __name__ == "__main__":
    import pandas as pd
    from spectrum import correlation

    returns = pd.read_parquet("returns.parquet")
    corr = correlation(returns)
    cleaned = clip(corr, len(returns))

    print("diagonal all 1:", np.allclose(np.diag(cleaned), 1))
    print("sum of eigenvalues:", round(np.linalg.eigvalsh(cleaned).sum(), 1))
    print("stocks 0 & 1, before:", round(np.asarray(corr)[0, 1], 3),
          "after:", round(cleaned[0, 1], 3))