import numpy as np
from sklearn.covariance import LedoitWolf


def min_var_weights(Sigma):
    ones = np.ones(len(Sigma))
    x = np.linalg.solve(Sigma, ones) # NEVER np.linalg.inv
    w = x / (ones @ x)
    assert np.isclose(w.sum(), 1.0)
    return w

def lw_cov(returns):
    return LedoitWolf().fit(returns.values).covariance_ * 252   # annualize daily cov