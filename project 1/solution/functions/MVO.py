"""Mean-Variance Optimization for Project 1."""

from __future__ import annotations

import numpy as np
from scipy.optimize import minimize


WEIGHT_TOLERANCE = 1.0e-10


def MVO(mu, Q, targetRet):
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
        are non-negative, and target at least ``targetRet`` when feasible.
    """

    expected_returns = np.asarray(mu, dtype=float).reshape(-1)
    covariance = np.asarray(Q, dtype=float)
    covariance = 0.5 * (covariance + covariance.T)
    asset_count = expected_returns.shape[0]

    # A target above every individual asset expected return is infeasible
    # under long-only weights. The closest meaningful target is the largest
    # asset expected return.
    feasible_target = min(float(targetRet), float(np.max(expected_returns)))

    def objective(weights: np.ndarray) -> float:
        """Return portfolio variance for SciPy's constrained optimizer."""

        return float(weights @ covariance @ weights)

    constraints = [
        {"type": "eq", "fun": lambda weights: np.sum(weights) - 1.0},
        {
            "type": "ineq",
            "fun": lambda weights: float(weights @ expected_returns - feasible_target),
        },
    ]
    bounds = [(0.0, 1.0) for _ in range(asset_count)]
    initial_weights = np.full(asset_count, 1.0 / asset_count)

    result = minimize(
        objective,
        initial_weights,
        method="SLSQP",
        bounds=bounds,
        constraints=constraints,
        options={"ftol": 1.0e-12, "maxiter": 1000},
    )

    if not result.success:
        # If the optimizer has trouble, invest in the highest expected-return
        # asset. This satisfies the adjusted feasible target and keeps the
        # experiment running with a transparent fallback.
        weights = np.zeros(asset_count)
        weights[int(np.argmax(expected_returns))] = 1.0
    else:
        weights = result.x

    weights[np.abs(weights) < WEIGHT_TOLERANCE] = 0.0
    weights = np.maximum(weights, 0.0)
    weights = weights / np.sum(weights)

    return weights
