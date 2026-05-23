# MMF1921 Project 1: Factor Models and Mean-Variance Optimization

## Introduction

This project compares four linear factor models for a 20-stock U.S. equity universe: ordinary least squares (OLS), Fama-French three-factor regression (FF), least absolute shrinkage and selection operator (LASSO), and Best Subset Selection (BSS). The models estimate monthly expected excess returns and covariance matrices, then those estimates feed a long-only mean-variance optimization strategy from January 2012 through December 2016.

An excess return is an asset return minus the risk-free rate. The project uses excess returns because the factor data includes the monthly risk-free rate, and the factor models are written in excess-return form.

## Data

The stock data contains monthly adjusted close prices for 20 stocks from 31-Dec-2005 to 31-Dec-2016. Monthly stock returns are computed from adjacent adjusted close prices. The factor data contains eight monthly factor returns plus the risk-free rate from 31-Jan-2006 to 31-Dec-2016. After computing returns, the stock-return dates and factor-return dates align exactly.

## Methodology

For each annual rebalance, the calibration window is the immediately preceding four years. For example, the January 2012 portfolio uses data from January 2008 through December 2011. The five out-of-sample test years are 2012, 2013, 2014, 2015, and 2016.

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

where $y$ is the asset excess-return vector, $X$ is the intercept-plus-factor matrix, $B$ is the coefficient vector, and $\lambda$ is the penalty weight. I used $\lambda = 0.04$. This value keeps the model sparse, with about three selected coefficients on average across all assets and calibration windows, while still retaining useful explanatory power. The Python code formulates the LASSO objective directly in `cvxpy`, so the absolute-value penalty is handled as a convex optimization problem rather than as an ordinary smooth least-squares regression.

BSS solves the same least-squares fit subject to at most $K$ non-zero coefficients:

$$
\min_B \|y - X B\|_2^2 \quad \text{subject to} \quad \|B\|_0 \le K
$$

where $\|B\|_0$ counts non-zero coefficients. I used the assignment baseline $K = 4$. Since there are only nine possible coefficients, one intercept plus eight factor loadings, the Python implementation uses exact exhaustive search over all subsets of size at most four. This gives the true best subset for this small project instance, rather than a heuristic approximation.

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

The MVO problem is also solved with `cvxpy`. If a target return were infeasible under long-only weights, the implementation would report the infeasibility instead of silently lowering the target. In this experiment, all five calibration-window targets were feasible for all four factor-model estimates.

## In-Sample Results

The adjusted $R^2$ statistic measures fit while penalizing models that use more explanatory variables. In the sparse models, the penalty counts selected factor coefficients only. The intercept is not treated as an explanatory factor because BSS and LASSO are allowed to omit it. The table below averages the period-level mean adjusted $R^2$ values across the five calibration windows.

| Model | Mean adjusted R2 | Mean selected coefficients |
| --- | --- | --- |
| OLS | 0.4459 | 9.00 |
| FF | 0.3605 | 4.00 |
| LASSO | 0.3063 | 2.74 |
| BSS | 0.4660 | 4.00 |

Full period-level fit output is saved in `outputs/tables/in_sample_fit_summary.csv`.

BSS has the strongest average adjusted $R^2$ even though it is limited to four non-zero coefficients. This means the exact subset search found compact factor combinations that fit the calibration data better than the full eight-factor OLS model after the adjustment penalty. OLS is second, which is expected because it has the most raw flexibility but pays the largest adjusted-$R^2$ penalty. FF has lower fit because it ignores profitability, investment, momentum, and reversal factors. LASSO is the sparsest model on average, so its lower in-sample fit is the cost of stronger shrinkage.

## Out-of-Sample Results

| model | average_monthly_return | monthly_volatility | annualized_return | annualized_volatility | sharpe_ratio | final_value |
| --- | --- | --- | --- | --- | --- | --- |
| OLS | 0.006760 | 0.026172 | 0.084202 | 0.090664 | 0.9287 | 146850.71 |
| FF | 0.006745 | 0.026251 | 0.084011 | 0.090935 | 0.9239 | 146699.53 |
| LASSO | 0.006768 | 0.026657 | 0.084303 | 0.092342 | 0.9129 | 146806.37 |
| BSS | 0.005538 | 0.026318 | 0.068518 | 0.091170 | 0.7515 | 136494.01 |

The wealth paths are shown below.

![Portfolio wealth evolution](outputs/figures/wealth_evolution.svg)

The BSS model's rebalance weights are shown below as a representative sparse-model allocation plot.

![BSS portfolio weights](outputs/figures/bss_weights.svg)

OLS, FF, and LASSO finish with very similar wealth. LASSO has the highest annualized return in this run, but it also has the highest annualized volatility, so its Sharpe ratio remains below OLS and FF. OLS has the highest Sharpe ratio among the four models. BSS has the best in-sample adjusted fit, but it performs worst out of sample. That is a useful warning: a factor model can explain the calibration window well and still produce less attractive portfolio weights for future returns.

## Discussion

OLS has the most flexible unrestricted factor exposure because it uses all eight factors. That can improve in-sample fit, but it also increases the risk that the model fits noise in a four-year monthly window. A four-year monthly calibration window has only 48 observations, so estimating many coefficients can be noisy. FF is simpler and easier to interpret, but it can miss effects captured by profitability, investment, momentum, and reversal factors.

LASSO and BSS are sparse approaches. Sparse means many coefficients are forced to zero. This can reduce estimation noise and make factor exposures easier to interpret. The tradeoff is that sparsity can omit useful but weaker factors. BSS is especially direct here because the exhaustive search is exact for this small problem.

The out-of-sample performance table should be read together with the allocation plots. A model with strong final wealth but high concentration may be taking more stock-specific risk. A lower-volatility model may be preferable if the goal is stable wealth rather than only final portfolio value. The main empirical lesson is that the best in-sample factor fit is not automatically the best portfolio model. Portfolio optimization depends on both estimated returns and estimated covariances, and small estimation errors can have a large effect on optimal weights.

## Conclusion

All four factor models can be used to produce the expected returns and covariance matrices required by mean-variance optimization. The experiment shows how estimation choices flow into portfolio construction: unrestricted models can fit more in sample, while sparse models create cleaner and more interpretable factor exposures. In this run, OLS and FF delivered the best risk-adjusted out-of-sample performance, LASSO delivered a similar final value with more volatility, and BSS showed that strong in-sample fit does not guarantee strong out-of-sample wealth. The best model depends on whether the investor values interpretability, diversification, final wealth, or risk-adjusted performance most.

## Reproducibility

Run the project from the `project 1` folder:

```bash
uv run python tests/run_tests.py
```

Then open and run `MMF1921_Project_1_Solution.ipynb`.

The notebook uses only Python and the data supplied in `source/Python/`.
