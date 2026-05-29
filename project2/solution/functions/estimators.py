"""Return and risk estimators for MMF1921 Project 2.

The project data are monthly. Asset returns are excess returns, meaning the
monthly risk-free rate has already been subtracted before these functions are
called. Factor returns exclude the risk-free-rate column.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


RIDGE_EPSILON = 1.0e-6
MINIMUM_VARIANCE = 1.0e-8


@dataclass
class EstimateResult:
    """Estimated inputs for portfolio optimization.

    Parameters
    ----------
    expected_returns:
        One-dimensional vector of monthly expected excess returns for each
        asset.
    covariance:
        Square covariance matrix of monthly asset excess returns.
    residual_variance:
        One-dimensional vector containing each asset's regression residual
        variance.
    """

    expected_returns: np.ndarray
    covariance: np.ndarray
    residual_variance: np.ndarray


def _as_float_matrix(values: np.ndarray) -> np.ndarray:
    """Convert input values to a two-dimensional ``float`` NumPy array."""

    matrix = np.asarray(values, dtype=float)
    if matrix.ndim != 2:
        raise ValueError("Expected a two-dimensional matrix.")

    return matrix


def estimate_ols_factor_model(
    asset_returns: np.ndarray,
    factor_returns: np.ndarray,
) -> EstimateResult:
    """Estimate expected returns and covariance with an ordinary least squares model.

    Parameters
    ----------
    asset_returns:
        Matrix with shape ``(months, assets)`` containing monthly asset excess
        returns.
    factor_returns:
        Matrix with shape ``(months, factors)`` containing monthly factor
        returns, excluding the risk-free rate.

    Returns
    -------
    EstimateResult
        Expected excess returns and covariance matrix implied by the fitted
        factor model.
    """

    returns = _as_float_matrix(asset_returns)
    factors = _as_float_matrix(factor_returns)
    observation_count, factor_count = factors.shape

    if returns.shape[0] != observation_count:
        raise ValueError("Asset returns and factor returns must have matching rows.")
    if observation_count <= factor_count + 1:
        raise ValueError("Not enough observations for the factor model.")

    intercept = np.ones((observation_count, 1), dtype=float)
    design = np.column_stack([intercept, factors])

    # A tiny ridge term handles near-collinearity without changing the model's
    # economic interpretation. It stabilizes the normal equations on all three
    # training datasets.
    gram = design.T @ design
    ridge = RIDGE_EPSILON * np.eye(gram.shape[0])
    coefficients = np.linalg.solve(gram + ridge, design.T @ returns)

    alpha = coefficients[0, :]
    factor_loadings = coefficients[1:, :]

    fitted_returns = design @ coefficients
    residuals = returns - fitted_returns
    degrees_of_freedom = max(observation_count - factor_count - 1, 1)
    residual_variance = np.sum(residuals * residuals, axis=0) / degrees_of_freedom
    residual_variance = np.maximum(residual_variance, MINIMUM_VARIANCE)

    factor_mean = np.mean(factors, axis=0)
    factor_covariance = np.cov(factors, rowvar=False)
    if factor_covariance.ndim == 0:
        factor_covariance = np.array([[float(factor_covariance)]])

    expected_returns = alpha + factor_loadings.T @ factor_mean
    covariance = factor_loadings.T @ factor_covariance @ factor_loadings
    covariance = covariance + np.diag(residual_variance)

    # Numerical solvers expect an exactly symmetric covariance matrix.
    covariance = (covariance + covariance.T) / 2.0

    return EstimateResult(
        expected_returns=np.asarray(expected_returns, dtype=float),
        covariance=np.asarray(covariance, dtype=float),
        residual_variance=np.asarray(residual_variance, dtype=float),
    )


def shrink_expected_returns(
    expected_returns: np.ndarray,
    shrinkage_weight: float,
) -> np.ndarray:
    """Shrink expected returns toward their cross-sectional average.

    Parameters
    ----------
    expected_returns:
        Raw monthly expected excess returns.
    shrinkage_weight:
        Weight on the cross-sectional average. A value of ``0`` leaves the
        vector unchanged. A value of ``1`` replaces every asset estimate by the
        same average.

    Returns
    -------
    np.ndarray
        Shrunk expected-return vector.
    """

    raw_returns = np.asarray(expected_returns, dtype=float).reshape(-1)
    average_return = float(np.mean(raw_returns))
    average_vector = np.full(raw_returns.shape, average_return, dtype=float)

    return (1.0 - shrinkage_weight) * raw_returns + shrinkage_weight * average_vector
