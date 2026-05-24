# MMF1921 Project 1: Factor Models and Mean-Variance Optimization

## Introduction

I compare four linear factor models for a 20-stock U.S. equity universe: ordinary least squares (OLS), Fama-French three-factor regression (FF), least absolute shrinkage and selection operator (LASSO), and Best Subset Selection (BSS). Each model estimates monthly expected excess returns and covariance matrices. I then use those estimates in a long-only mean-variance optimization strategy tested from January 2012 through December 2016.

An excess return is an asset return minus the risk-free rate. I use excess returns because the factor data provides a monthly risk-free rate and the regressions are specified in excess-return form.

## Data

The stock data contains monthly adjusted close prices for 20 stocks from 31-Dec-2005 to 31-Dec-2016. I compute monthly stock returns from adjacent adjusted close prices. The factor data contains eight monthly factor returns and the risk-free rate from 31-Jan-2006 to 31-Dec-2016. Once the stock returns are computed, their dates match the factor-return dates exactly.

## Methodology

At each annual rebalance, I calibrate the models on the immediately preceding four years. For example, the January 2012 portfolio uses data from January 2008 through December 2011. The out-of-sample test covers five years: 2012 through 2016.

For asset $i$, monthly excess return is

$$
r_i - r_f
$$

where $r_i$ is the monthly stock return and $r_f$ is the monthly risk-free rate.

The OLS model uses all eight factors:

$$
r_i - r_f = \alpha_i + \sum_{k=1}^8 \beta_{ik} f_k + \epsilon_i
$$

where $\alpha_i$ is the intercept, $\beta_{ik}$ is asset $i$'s loading on factor $k$, $f_k$ is factor $k$'s return, and $\epsilon_i$ is the residual.

The FF model uses only market excess return, size, and value. LASSO solves a penalized least-squares problem:

$$
\min_B \|y - X B\|_2^2 + \lambda \|B\|_1
$$

where $y$ is the asset excess-return vector, $X$ is the intercept-plus-factor matrix, $B$ is the coefficient vector, and $\lambda$ is the penalty weight. I used $\lambda = 0.04$. Across all assets and calibration windows, this setting selects about three coefficients on average while retaining useful explanatory power. The Python code formulates the LASSO objective directly in `cvxpy`. The absolute-value penalty is therefore part of a convex optimization problem, rather than an ordinary smooth least-squares regression.

BSS solves the same least-squares fit subject to at most $K$ non-zero coefficients:

$$
\min_B \|y - X B\|_2^2 \quad \text{subject to} \quad \|B\|_0 \le K
$$

where $\|B\|_0$ counts non-zero coefficients. I used the assignment baseline $K = 4$. There are only nine possible coefficients: one intercept and eight factor loadings. The Python implementation can therefore search every subset of size at most four and obtain the exact best subset for this problem, with no heuristic approximation.

For each model, the expected excess-return vector $\mu$ is the fitted model's mean prediction over the calibration window. The covariance matrix $Q$ is

$$
Q = B_f^T \Sigma_f B_f + D_\epsilon
$$

where $B_f$ is the factor-loading matrix without the intercept row, $\Sigma_f$ is the factor covariance matrix, and $D_\epsilon$ is the diagonal matrix of residual variances.

The portfolio optimization is long-only mean-variance optimization:

$$
\min_x x^T Q x
$$

subject to

$$
\sum_i x_i = 1, \quad x_i \ge 0, \quad \mu^T x \ge r_{target}
$$

where $x$ is the portfolio-weight vector and $r_{target}$ is the geometric mean of the market factor over the calibration window.

I also solve the mean-variance optimization problem with `cvxpy`. If a target return were infeasible under long-only weights, the implementation would report infeasibility rather than silently lower the target. All five calibration-window targets were feasible under each of the four factor-model estimates.

## In-Sample Results

The adjusted $R^2$ statistic measures fit while penalizing models that use more explanatory variables. For the sparse models, the penalty counts only selected factor coefficients. The intercept is excluded from that count because BSS and LASSO may omit it. The table reports the average of the period-level mean adjusted $R^2$ values over the five calibration windows.

| Model | Mean adjusted R2 | Mean selected coefficients |
| --- | --- | --- |
| OLS | 0.4459 | 9.00 |
| FF | 0.3605 | 4.00 |
| LASSO | 0.3063 | 2.74 |
| BSS | 0.4660 | 4.00 |

Full period-level fit output is saved in `outputs/tables/in_sample_fit_summary.csv`.

BSS produces the highest average adjusted $R^2$ despite its four-coefficient limit. Its selected factor combinations fit the calibration data better, after the complexity penalty, than the full eight-factor OLS model. OLS ranks second: it can use all eight factors, but adjusted $R^2$ penalizes that additional flexibility. FF omits profitability, investment, momentum, and reversal factors, and its fit is lower. LASSO selects the fewest coefficients on average and accepts lower in-sample fit in exchange for stronger shrinkage.

## Out-of-Sample Results

| model | average_monthly_return | monthly_volatility | annualized_return | annualized_volatility | sharpe_ratio | final_value |
| --- | --- | --- | --- | --- | --- | --- |
| OLS | 0.006760 | 0.026172 | 0.084202 | 0.090664 | 0.9287 | 146850.71 |
| FF | 0.006745 | 0.026251 | 0.084011 | 0.090935 | 0.9239 | 146699.53 |
| LASSO | 0.006768 | 0.026657 | 0.084303 | 0.092342 | 0.9129 | 146806.37 |
| BSS | 0.005538 | 0.026318 | 0.068518 | 0.091170 | 0.7515 | 136494.01 |

The figure below plots the wealth paths.

![Portfolio wealth evolution](outputs/figures/wealth_evolution.svg)

The next figure shows the BSS rebalance weights as an example of a sparse-model allocation.

![BSS portfolio weights](outputs/figures/bss_weights.svg)

OLS, FF, and LASSO end at very similar wealth levels. LASSO has the highest annualized return in this run, along with the highest annualized volatility, leaving its Sharpe ratio below those of OLS and FF. OLS has the highest Sharpe ratio of the four models. BSS, despite its leading in-sample adjusted fit, performs worst out of sample. Fitting the calibration window closely did not translate into better weights for future returns.

## Discussion

OLS uses all eight factors, giving it the widest unrestricted factor exposure. That flexibility can improve fit within the calibration sample, but the sample contains only 48 monthly observations. Estimating many coefficients from a short window raises the risk of fitting noise. FF is easier to interpret because it uses three factors, but it omits effects captured by profitability, investment, momentum, and reversal factors.

LASSO and BSS impose sparsity, meaning that many coefficients are set to zero. Fewer active factor exposures can reduce estimation noise and simplify interpretation, but they may also discard weaker factors that would help forecast returns or covariance. For this small coefficient set, BSS is exact because every permitted subset can be evaluated.

The out-of-sample performance table should be read together with the allocation plots. High final wealth paired with concentrated weights can indicate greater stock-specific risk. An investor seeking steadier wealth might prefer lower volatility to the highest final portfolio value. Here, the model with the best in-sample factor fit is not the best portfolio model out of sample. Mean-variance optimization uses both estimated returns and estimated covariances, and small errors in either estimate can materially change the optimal weights.

## Conclusion

Each factor model supplies the expected-return vector and covariance matrix needed for mean-variance optimization, but the resulting portfolios differ. In this run, OLS and FF have the best risk-adjusted out-of-sample performance. LASSO ends at a similar final value with greater volatility. BSS has the strongest in-sample adjusted fit and the weakest out-of-sample wealth, showing that calibration fit alone is not a sufficient model-selection criterion. A choice among these models must reflect the investor's priority: interpretability, diversification, final wealth, or risk-adjusted performance.

## Reproducibility

Run the project from the `project 1` folder:

```bash
uv run python tests/run_tests.py
```

Then open and run `MMF1921_Project_1_Solution.ipynb`.

The notebook uses Python and the supplied data in `source/Python/`.
