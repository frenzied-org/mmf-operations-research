"""Mean-Variance Optimization for Project 1."""

from __future__ import annotations

import cvxpy as cp
import numpy as np


WEIGHT_TOLERANCE = 1.0e-10
TARGET_TOLERANCE = 1.0e-10
CVXPY_SOLVERS = ("CLARABEL", "OSQP", "SCS")


def MVO(mu: object, Q: object, targetRet: float) -> np.ndarray:
    """Construct a long-only minimum-variance portfolio.

    Parameters
    ----------
    mu:
        One-dimensional vector of estimated monthly expected excess returns.
    Q:
        Square covariance matrix of monthly asset excess returns.
    targetRet:
        Minimum expected excess return required by the assignment. This is
        the geometric mean of the market excess return over the calibration
        window.

    Returns
    -------
    np.ndarray
        One-dimensional vector of portfolio weights. The weights sum to one,
        are non-negative, and target at least ``targetRet``.

    Raises
    ------
    ValueError
        Raised when the long-only target return is infeasible or when the
        convex optimization solver cannot find an optimal portfolio.
    """

    expected_returns = np.asarray(mu, dtype=float).reshape(-1)
    covariance = np.asarray(Q, dtype=float)
    covariance = 0.5 * (covariance + covariance.T)
    asset_count = expected_returns.shape[0]

    if float(targetRet) > float(np.max(expected_returns)) + TARGET_TOLERANCE:
        raise ValueError("MVO target return is infeasible under long-only weights.")

    weights_variable = cp.Variable(asset_count)
    portfolio_variance = cp.quad_form(weights_variable, cp.psd_wrap(covariance))
    constraints = [
        cp.sum(weights_variable) == 1.0,
        weights_variable >= 0.0,
        expected_returns @ weights_variable >= float(targetRet),
    ]
    problem = cp.Problem(cp.Minimize(portfolio_variance), constraints)

    last_error: Exception | None = None
    installed_solvers = set(cp.installed_solvers())
    for solver_name in CVXPY_SOLVERS:
        if solver_name not in installed_solvers:
            continue
        try:
            problem.solve(solver=solver_name, verbose=False)
        except cp.error.SolverError as error:
            last_error = error
            continue

        if problem.status in {cp.OPTIMAL, cp.OPTIMAL_INACCURATE}:
            weights = np.asarray(weights_variable.value, dtype=float).reshape(-1)
            weights[np.abs(weights) < WEIGHT_TOLERANCE] = 0.0
            weights = np.maximum(weights, 0.0)
            weights = weights / np.sum(weights)

            return weights

    if last_error is not None:
        raise ValueError("MVO cvxpy solve failed.") from last_error

    raise ValueError(
        f"MVO cvxpy solve ended with status {problem.status!r} for target return."
    )
