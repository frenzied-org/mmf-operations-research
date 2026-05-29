"""Portfolio optimization routines for MMF1921 Project 2."""

from __future__ import annotations

import numpy as np

try:
    import cvxpy as cp
except ImportError:  # pragma: no cover - cvxpy is available in this project.
    cp = None


MINIMUM_DIAGONAL_RISK = 1.0e-8


def _project_to_simplex(values: np.ndarray) -> np.ndarray:
    """Project a vector onto the long-only fully invested simplex.

    The simplex is the set of weights ``x`` such that every weight is
    non-negative and all weights sum to one.
    """

    vector = np.asarray(values, dtype=float).reshape(-1)
    if vector.size == 0:
        raise ValueError("Cannot project an empty vector.")

    sorted_values = np.sort(vector)[::-1]
    cumulative_sum = np.cumsum(sorted_values)
    candidate_indices = np.arange(1, vector.size + 1)
    support = sorted_values - (cumulative_sum - 1.0) / candidate_indices > 0.0

    if not np.any(support):
        return np.full(vector.size, 1.0 / vector.size)

    last_support_index = int(np.where(support)[0][-1])
    threshold = (cumulative_sum[last_support_index] - 1.0) / (last_support_index + 1)
    projected = np.maximum(vector - threshold, 0.0)

    return projected / projected.sum()


def equal_weight(asset_count: int) -> np.ndarray:
    """Return a long-only equal-weight portfolio."""

    if asset_count <= 0:
        raise ValueError("asset_count must be positive.")

    return np.full(asset_count, 1.0 / asset_count, dtype=float)


def minimum_variance_with_return_tilt(
    expected_returns: np.ndarray,
    covariance: np.ndarray,
    risk_aversion: float,
    max_weight: float,
) -> np.ndarray:
    """Solve a conservative long-only mean-variance allocation.

    The objective is ``0.5 * x'Qx - risk_aversion * mu'x``. Here ``x`` is the
    portfolio weight vector, ``Q`` is the covariance matrix, and ``mu`` is the
    expected excess-return vector. The upper bound prevents a noisy expected
    return from concentrating the portfolio in one asset.
    """

    expected = np.asarray(expected_returns, dtype=float).reshape(-1)
    risk = np.asarray(covariance, dtype=float)
    asset_count = expected.size

    if risk.shape != (asset_count, asset_count):
        raise ValueError("covariance shape must match expected_returns.")

    risk = (risk + risk.T) / 2.0
    risk = risk + MINIMUM_DIAGONAL_RISK * np.eye(asset_count)

    if cp is None:
        inverse_variance = 1.0 / np.maximum(np.diag(risk), MINIMUM_DIAGONAL_RISK)
        tilted = inverse_variance + risk_aversion * expected
        return _project_to_simplex(tilted)

    weights = cp.Variable(asset_count)
    objective = cp.Minimize(
        0.5 * cp.quad_form(weights, risk) - risk_aversion * expected @ weights
    )
    constraints = [
        cp.sum(weights) == 1.0,
        weights >= 0.0,
        weights <= max_weight,
    ]
    problem = cp.Problem(objective, constraints)
    problem.solve(verbose=False)

    if weights.value is None or problem.status not in {"optimal", "optimal_inaccurate"}:
        inverse_variance = 1.0 / np.maximum(np.diag(risk), MINIMUM_DIAGONAL_RISK)
        return _project_to_simplex(inverse_variance)

    cleaned_weights = np.asarray(weights.value, dtype=float).reshape(-1)
    cleaned_weights = np.minimum(np.maximum(cleaned_weights, 0.0), max_weight)

    return _project_to_simplex(cleaned_weights)
