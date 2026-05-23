"""Shared factor-model utilities for MMF1921 Project 1.

The project estimates monthly excess stock returns with linear factor
models. All arrays use rows for months and columns for assets or factors.
The helper functions in this file keep the model implementations short and
consistent.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations

import numpy as np


RIDGE_EPSILON = 1.0e-8
R2_EPSILON = 1.0e-12
SELECTED_COEFFICIENT_TOLERANCE = 1.0e-6


@dataclass
class FactorModelResult:
    """Container for factor-model outputs.

    Parameters
    ----------
    mu:
        One-dimensional vector of estimated monthly expected excess returns,
        one value per asset.
    Q:
        Square covariance matrix of estimated monthly asset excess returns.
    coefficients:
        Matrix of fitted regression coefficients. Rows are intercept and
        factor coefficients. Columns are assets.
    fitted_returns:
        Matrix of fitted in-sample excess returns with the same shape as the
        observed return matrix.
    residuals:
        Matrix of fitted residuals, equal to observed returns minus fitted
        returns.
    adjusted_r2:
        One-dimensional vector of adjusted R-squared values, one per asset.
    selected_counts:
        One-dimensional vector with the number of non-zero coefficients used
        by each asset model. For ordinary least squares this is the full
        number of coefficients.
    intercept_selected:
        Boolean vector indicating whether each asset model uses a non-zero
        intercept. This is needed because sparse models may omit the
        intercept, and adjusted R-squared only penalizes explanatory factors.
    factor_names:
        Names of the factor columns used by the model.
    model_name:
        Short model label used in tables and reports.
    """

    mu: np.ndarray
    Q: np.ndarray
    coefficients: np.ndarray
    fitted_returns: np.ndarray
    residuals: np.ndarray
    adjusted_r2: np.ndarray
    selected_counts: np.ndarray
    intercept_selected: np.ndarray
    factor_names: list[str]
    model_name: str

    def __iter__(self):
        """Allow legacy unpacking as ``mu, Q = model(...)``."""

        yield self.mu
        yield self.Q


def as_numeric_matrix(values: object) -> np.ndarray:
    """Convert NumPy, pandas, or list-like input to a float matrix.

    Parameters
    ----------
    values:
        Data supplied by a script, notebook, or test. Pandas objects are
        accepted through their ``to_numpy`` method.

    Returns
    -------
    np.ndarray
        Two-dimensional float matrix.
    """

    if hasattr(values, "to_numpy"):
        matrix = values.to_numpy(dtype=float)
    else:
        matrix = np.asarray(values, dtype=float)

    if matrix.ndim == 1:
        matrix = matrix.reshape(-1, 1)

    return matrix


def make_design_matrix(
    factors: object, factor_indices: list[int] | None = None
) -> np.ndarray:
    """Build a regression design matrix with an intercept column.

    Parameters
    ----------
    factors:
        Monthly factor-return matrix.
    factor_indices:
        Zero-based columns to keep. ``None`` keeps every factor.

    Returns
    -------
    np.ndarray
        Matrix whose first column is all ones and whose remaining columns
        are selected factor returns.
    """

    factor_matrix = as_numeric_matrix(factors)
    if factor_indices is not None:
        factor_matrix = factor_matrix[:, factor_indices]

    intercept = np.ones((factor_matrix.shape[0], 1))
    design_matrix = np.column_stack([intercept, factor_matrix])

    return design_matrix


def adjusted_r_squared(
    observed_returns: np.ndarray,
    fitted_returns: np.ndarray,
    selected_counts: np.ndarray,
    intercept_selected: np.ndarray | None = None,
) -> np.ndarray:
    """Calculate adjusted R-squared for each asset.

    Adjusted R-squared is
    ``1 - (1 - R2) * (T - 1) / (T - p - 1)``, where ``T`` is the number of
    monthly observations and ``p`` is the number of selected factor
    coefficients excluding the intercept.
    """

    observations = observed_returns.shape[0]
    residuals = observed_returns - fitted_returns
    residual_sum_squares = np.sum(residuals**2, axis=0)

    centered_returns = observed_returns - observed_returns.mean(axis=0)
    total_sum_squares = np.sum(centered_returns**2, axis=0)
    safe_total_sum_squares = np.maximum(total_sum_squares, R2_EPSILON)
    r_squared = 1.0 - residual_sum_squares / safe_total_sum_squares

    if intercept_selected is None:
        intercept_flags = np.ones_like(selected_counts, dtype=bool)
    else:
        intercept_flags = np.asarray(intercept_selected, dtype=bool)

    intercept_counts = intercept_flags.astype(int)
    predictor_counts = np.maximum(selected_counts - intercept_counts, 0)
    denominator = np.maximum(observations - predictor_counts - 1, 1)
    adjustment = (observations - 1) / denominator
    adjusted_values = 1.0 - (1.0 - r_squared) * adjustment

    return adjusted_values


def covariance_from_factor_model(
    design_matrix: np.ndarray,
    coefficients: np.ndarray,
    observed_returns: np.ndarray,
    selected_counts: np.ndarray,
    factor_names: list[str],
    model_name: str,
    intercept_selected: np.ndarray | None = None,
) -> FactorModelResult:
    """Convert fitted regression coefficients into ``mu`` and ``Q``.

    The factor covariance contribution is ``B' Sigma_f B``. Here ``B`` is
    the factor-loading matrix and ``Sigma_f`` is the sample covariance
    matrix of factor returns. Residual asset-specific variance is added on
    the diagonal.
    """

    fitted_returns = design_matrix @ coefficients
    residuals = observed_returns - fitted_returns

    factor_matrix = design_matrix[:, 1:]
    factor_loadings = coefficients[1:, :]

    if factor_matrix.shape[1] == 0:
        factor_covariance = np.zeros((0, 0))
    else:
        factor_covariance = np.cov(factor_matrix, rowvar=False, ddof=1)
        factor_covariance = np.atleast_2d(factor_covariance)

    residual_variance = np.var(residuals, axis=0, ddof=1)
    residual_covariance = np.diag(np.maximum(residual_variance, 0.0))

    mu = design_matrix.mean(axis=0) @ coefficients
    Q = factor_loadings.T @ factor_covariance @ factor_loadings
    Q = Q + residual_covariance

    # A tiny ridge term prevents numerical roundoff from making the
    # covariance matrix appear non-positive-semidefinite to optimizers.
    Q = 0.5 * (Q + Q.T)
    Q = Q + RIDGE_EPSILON * np.eye(Q.shape[0])

    if intercept_selected is None:
        intercept_selected = np.abs(coefficients[0, :]) > SELECTED_COEFFICIENT_TOLERANCE

    adjusted_r2 = adjusted_r_squared(
        observed_returns=observed_returns,
        fitted_returns=fitted_returns,
        selected_counts=selected_counts,
        intercept_selected=intercept_selected,
    )

    return FactorModelResult(
        mu=np.asarray(mu, dtype=float),
        Q=np.asarray(Q, dtype=float),
        coefficients=np.asarray(coefficients, dtype=float),
        fitted_returns=np.asarray(fitted_returns, dtype=float),
        residuals=np.asarray(residuals, dtype=float),
        adjusted_r2=np.asarray(adjusted_r2, dtype=float),
        selected_counts=np.asarray(selected_counts, dtype=int),
        intercept_selected=np.asarray(intercept_selected, dtype=bool),
        factor_names=factor_names,
        model_name=model_name,
    )


def fit_least_squares_model(
    returns: object,
    factors: object,
    factor_indices: list[int] | None,
    factor_names: list[str],
    model_name: str,
) -> FactorModelResult:
    """Fit a linear factor model by ordinary least squares."""

    observed_returns = as_numeric_matrix(returns)
    design_matrix = make_design_matrix(factors, factor_indices)
    coefficients = np.linalg.lstsq(design_matrix, observed_returns, rcond=None)[0]
    selected_counts = np.full(observed_returns.shape[1], design_matrix.shape[1])
    intercept_selected = np.ones(observed_returns.shape[1], dtype=bool)

    return covariance_from_factor_model(
        design_matrix=design_matrix,
        coefficients=coefficients,
        observed_returns=observed_returns,
        selected_counts=selected_counts,
        intercept_selected=intercept_selected,
        factor_names=factor_names,
        model_name=model_name,
    )


def all_subsets(max_size: int, coefficient_count: int) -> list[tuple[int, ...]]:
    """List all coefficient-index subsets up to a maximum cardinality."""

    subsets: list[tuple[int, ...]] = []
    for size in range(1, max_size + 1):
        subsets.extend(combinations(range(coefficient_count), size))

    return subsets
