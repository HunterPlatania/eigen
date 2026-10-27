# EIGEN Phase 1 Results

## Data (1.1)

I downloaded daily adjusted closing prices for 104 large US stocks from Yahoo Finance via yfinance covering 2010-01-01 through September 2026. Adjusted prices fix split and dividend jumps (like Apple's 4-for-1 split) so charts show actual financial gains instead of artificial drops. I converted these into daily log returns, ln(today/yesterday). After failed downloads for BK and EA, I kept stocks with 99%+ complete data, then dropped the few remaining days with gaps, because protecting the number of time steps matters more than losing two stocks. The cached returns.parquet dataset holds T=4205 days and N=102 stocks (T/N approx 41).

## Spectrum (1.2)

I built a 102 x 102 correlation matrix on standardized returns across all pairs simultaneously. The top eigenvalue reached 38.06 out of 102, showing a single broad market factor carries roughly 37% of all stock movement. At q = N/T = 0.024, the Marchenko-Pastur threshold puts pure random noise between 0.71 and 1.34, meaning anything over 1.34 is genuine signal. Synthetic random returns of the same 4205 x 102 size topped out at 1.32, confirming the noise ceiling. Exactly eight eigenvalues beat 1.34 (38.06, 6.67, 4.73, 2.65, 2.20, 2.02, 1.62, 1.46), while the noise bulk sits to the left of the MP band as pictured in figures/spectrum.png.

## Removing the market mode (1.3)

I calculated each day's market factor and each stock's beta sensitivity, then subtracted factor x beta from every stock to keep only residual returns. This removes the main reason everything moves together so quieter patterns can show up. The new top eigenvalues dropped to 10.19, 7.81, 4.81, 3.21, and 3.14, re-normalizing the sum to 102 while pushing the bulk right onto the MP curve now that the market mode stops eating the budget, as seen in figures/spectrum_clean.png. Matching these remaining patterns to sector labels was cut for time; I moved straight into covariance matrix construction and eigenvalue cleaning, and sector matching is planned for later.

## Covariance (1.5)

Correlation throws away each stock's individual volatility, but the optimizer needs actual variance to size positions properly, so I converted correlation into covariance by multiplying each pair's correlation by both stocks' volatilities. The calmest stocks were JNJ, KO, and PG, at about 17% a year, and the wildest were FCX, MU, and AMD, at 49 to 56% a year. My covariance matrix matched pandas' own covariance calculation exactly.

## Cleaning the matrix (1.6)

The luck line is the upper bound of the Marchenko-Pastur noise distribution, 1.34 for my data, and 8 eigenvalues cleared it. I left those 8 alone and replaced the remaining 94 bulk noise eigenvalues with their average, 0.453. I used the average instead of zero for two reasons: it keeps the trace equal to 102 so total variance is preserved (zeros would drop it to 59.41), and a zero eigenvalue can't be inverted, since dividing by zero is undefined. I then rebuilt the matrix from the same eigenvectors with the new eigenvalues. For example, the correlation between stocks 0 and 1 changed from 0.367 to 0.394.

## Minimum-variance portfolios (1.7)

A minimum-variance portfolio is a portfolio of stocks weighted to make the total price swing as small as possible. Building one requires inverting the covariance matrix, and inverting flips a small eigenvalue like 0.05 upside down into a massive number like 20, blowing up its weight. That means noisy random patterns get inverted into huge weights, so the optimizer ends up betting heavily on noise. The raw matrix had a condition number of 650 versus 258 for the cleaned one, and its biggest short was -0.103 versus -0.055. The cleaned matrix is much better behaved and less prone to extreme short bets, even though raw still wins out-of-sample risk performance.

## Backtest and verdict (1.9 to 1.10)

![Predicted vs realized portfolio risk](figures/headline.png)

The test looked back over 504 trading days (about 2 years), rebuilt the portfolios every 21 trading days (monthly), and rebalanced 176 times, always testing on days the portfolio had never seen. Raw had the lowest realized risk: Raw 13.01%, Clipped 14.59%, Clipped-adjusted 13.39%.

Plain clipping lost because it didn't account for the market mode. The luck line sat too high (2.1), so it cut into real signal instead of just noise. Correcting the luck line for the market mode got it down to 13.39%, which closed most of the gap from 14.59%, but it still did not get below raw's 13.01%. Before running it, I predicted the corrected version would beat raw. It did not.

**Verdict: on this data, cleaning does not beat the raw matrix.**

All three matrices also promised too little risk. Every realized number came in about 50% higher than predicted (ratios 1.50 to 1.63), so a 2-year look-back underestimated real volatility no matter how the matrix was cleaned.
