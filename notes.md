# EIGEN Phase 1: study notes

## Data (1.1)
- **102 stocks** (started with 104; BK and EA failed), **4,205 days** (2010 to Sep 2026)
- **T/N ≈ 41**: about 41 days of evidence per stock

## Spectrum (1.2)
- **Market mode: 38.06** out of 102, so one pattern carries about **37%** of all movement
- **Luck line: 1.34**. Pure noise can't go higher. Fake-data test topped out at **1.32**
- **8 real** eigenvalues: 38.06, 6.67, 4.73, 2.65, 2.20, 2.02, 1.62, 1.46
- With only 1,000 days, the line would rise to **1.74**: less data means noise can fake bigger patterns

## Market mode removed (1.3)
- New top 5: **10.19, 7.81, 4.81, 3.21, 3.14**; the sum stays 102
- The bulk moved onto the MP curve once the market mode stopped eating the variance

## Covariance (1.5)
- Correlation = *whether* stocks move together. Covariance = *how much*
- Calmest: **JNJ, KO, PG, about 17%/yr**. Wildest: **FCX, MU, AMD, 49 to 56%/yr**
- Check: matched pandas' own covariance exactly

## Cleaning (1.6)
- Kept the 8 above **1.34**; replaced the other 94 with their average, **0.453**
- **Why not zero:** (1) the total must stay **102**, since zeros would give 59.41; (2) zero can't be inverted, because dividing by zero is **undefined**
- **Trace** = the sum of the diagonal = the sum of the eigenvalues = 102
- Example: stocks 0 and 1 went from **0.367 to 0.394**

## Portfolios (1.7)
- Minimum-variance: the mix that swings the least, ignoring returns
- **The keystone:** inverting flips small into huge: 1/0.05 = **20**. The noisy patterns get the biggest say, so the optimizer bets on noise
- **Condition number** (how close to breaking when inverted): **raw 650, clean 258**
- **Biggest short:** raw **-0.103**, clean **-0.055**
- Watch out: clean's biggest *long* was larger (0.15 vs 0.118), and clean shorted more stocks (42 vs 39)

## Backtest and verdict (1.9 to 1.10)
- **504-day** look-back (2 years), rebuilt every **21 days**, **176** rebalances, tested only on unseen days
- With 504 days the luck line rises to **2.1**; adjusted for the market mode it's about **1.3**
- **Realized vol:** raw **13.01%**, clipped **14.59%**, clipped-adjusted **13.39%**
- **Ratios** (realized / predicted): **1.52 / 1.63 / 1.50**
- My prediction: the adjusted version would beat raw. **Wrong.**
- **Verdict: on this data, cleaning does not beat the raw matrix**
- All three **underestimated** risk by about 50%

## The six numbers to know cold for the gate
38.06 · 1.34 · 8 · 0.453 · 650 vs 258 · 13.01 vs 13.39 vs 14.59