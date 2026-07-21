# EIGEN

Using random matrix theory to figure out how much of a stock correlation matrix is real information and how much is just noise.

## Phase 0

I pulled 10 years of daily prices (2015-2025) for 55 large US companies and turned them into daily returns. From those I built a correlation matrix, which measures whether the stocks move together, and then took its eigenvalues.

An eigenvalue tells you how much unity there is in the stocks' movement - how much of the total movement one shared pattern explains. The eigenvalues always add up to the number of stocks, so with 55 stocks, if all of them moved together perfectly the largest eigenvalue would be 55.

## What I found

- Smallest eigenvalue: 0.093
- Largest eigenvalue: 22.113
- Sum: 55.0

The largest eigenvalue is 22.1 out of 55, so one shared pattern explains about 40 percent of everything these 55 companies do. That pattern is the market itself. It is strong, but nowhere near total.

I plotted the eigenvalues against the Marchenko-Pastur distribution, which is the shape you would get if the stocks had no real relationships at all and every correlation was luck. Anything inside that curve could be noise. A few eigenvalues sit past the edge (about 1.32) and are real - those are sectors. The largest one is 17 times past the edge, so it is off the chart entirely.

One thing I did not expect: the bulk of my eigenvalues sits to the left of the Marchenko-Pastur curve instead of under it. The market eigenvalue takes 22.1 of the 55 units, which leaves less for everything else and squeezes them down. Removing the market mode first is a Phase 1 task.

## Notes

Phase 0 reproduces a known result (Laloux, Cizeau, Bouchaud and Potters, 1999). Nothing here is new. The point was to build it myself and understand it.

## Next

- Learn the linear algebra behind eigenvalues properly
- Remove the market mode and re-test the noise fit
- Compare cleaned and uncleaned correlation matrices in a portfolio backtest
