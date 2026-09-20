import numpy as np
import matplotlib.pyplot as plt

def correlation(returns):
    return np.corrcoef(returns.values, rowvar=False)

def spectrum(returns):
    C = correlation(returns)
    return np.sort(np.linalg.eigvalsh(C))[::-1] # largest first

def mp_density(lam, q):
    """Density of eigenvalues if the data were pure noise. q = N/T."""
    lam_plus = (1 + np.sqrt(q)) ** 2
    lam_minus = (1 - np.sqrt(q)) ** 2
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
    ax.hist(vals, bins=60, density=True, alpha=0.6, label="observed eigenvalues")
    ax.plot(grid, mp_density(grid, q), lw=2, label=f"pure noise (MP, q={q:.2f})")
    ax.set_xlim(0, zoom) # the market mode is far right
    ax.set_xlabel("eigenvalue"); ax.set_ylabel("density"); ax.legend()
    fig.savefig(fname, dpi=150, bbox_inches="tight")
    return vals