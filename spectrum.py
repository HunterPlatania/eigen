import numpy as np
import matplotlib.pyplot as plt

def correlation(returns):
    # the whole 102x102 grid in one call; rowvar=False says
    # "my stocks are columns, my days are rows"
    return np.corrcoef(returns.values, rowvar=False)

#python -c "from data import load_returns; print(load_returns()[['JPM','BAC','XOM','NEM']].corr().round(2))"

def spectrum(returns):
    C = correlation(returns)
    return np.sort(np.linalg.eigvalsh(C))[::-1]

#python -c "from data import load_returns; from spectrum import spectrum; v = spectrum(load_returns()); print(round(v[0],1), round(v.sum(),1))"
# TEST WITH GRID IF PURE RANDM VALUES
#python -c "import numpy as np, pandas as pd; from spectrum import spectrum; fake = pd.DataFrame(np.random.randn(4205, 102)); v = spectrum(fake); print(round(v[0],2), round(v[-1],2))"

def mp_density(lam, q):
    # the exact shape of luck: where fake-team scores pile up, for evidence-thinness q
    lam_plus = (1 + np.sqrt(q)) ** 2      # the ceiling, your 1.34
    lam_minus = (1 - np.sqrt(q)) ** 2     # the floor, your 0.71
    rho = np.zeros_like(lam, dtype=float)
    inside = (lam > lam_minus) & (lam < lam_plus)
    rho[inside] = np.sqrt((lam_plus - lam[inside]) * (lam[inside] - lam_minus)) \
                  / (2 * np.pi * q * lam[inside])
    return rho

def plot_spectrum(returns, fname="figures/spectrum.png", zoom=3.5):
    vals = spectrum(returns)
    q = returns.shape[1] / len(returns)
    grid = np.linspace(0.001, zoom, 600)
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.hist(vals, bins=np.linspace(0, zoom, 70), density=True, alpha=0.6,label="observed eigenvalues")
    ax.plot(grid, mp_density(grid, q), lw=2, label=f"pure luck (MP, q={q:.3f})")
    ax.set_xlim(0, zoom)   # zoom on the band; the 38.1 monster sits far off-screen right
    ax.set_xlabel("eigenvalue (points out of 102)"); ax.set_ylabel("density"); ax.legend()
    fig.savefig(fname, dpi=150, bbox_inches="tight")
    return vals

#PLOT
#python -c "from data import load_returns; from spectrum import plot_spectrum; plot_spectrum(load_returns())"

# how many beat luck's ceiling, top ten
#python -c "from data import load_returns; from spectrum import spectrum; v = spectrum(load_returns()); print('above ceiling:', int((v > 1.34).sum())); print([round(x,2) for x in v[:10]])"