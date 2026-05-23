"""Least absolute shrinkage and selection operator model for Project 1."""

from __future__ import annotations

import numpy as np
from scipy.optimize import minimize

from model_utils import (
    SELECTED_COEFFICIENT_TOLERANCE,
    as_numeric_matrix,
    covariance_from_factor_model,
    make_design_matrix,
)


def _fit_lasso_for_asset(
    design_matrix: np.ndarray,
    asset_returns: np.ndarray,
    lambda_: float,
) -> np.ndarray:
    """Solve the penalized LASSO problem for one asset.

    The objective is ``sum((y - X b)^2) + lambda * sum(abs(b))``. The
    intercept is included in ``b`` and is penalized because the assignment
    asks the model to decide whether to include it.
    """

    initial_coefficients = np.linalg.lstsq(design_matrix, asset_returns, rcond=None)[0]

    def objective(coefficients: np.ndarray) -> float:
        """Return the LASSO objective value for SciPy's optimizer."""

        residuals = asset_returns - design_matrix @ coefficients
        squared_error = float(residuals @ residuals)
        absolute_penalty = float(lambda_ * np.sum(np.abs(coefficients)))

        return squared_error + absolute_penalty

    result = minimize(
        objective,
        initial_coefficients,
        method="BFGS",
        options={"gtol": 1.0e-8, "maxiter": 2000},
    )

    if result.success:
        coefficients = result.x
    else:
        # The BFGS optimizer can report precision loss near the L1 kink even
        # when the returned coefficients are usable. Keep the best available
        # vector instead of failing the full experiment.
        coefficients = result.x

    coefficients[np.abs(coefficients) < SELECTED_COEFFICIENT_TOLERANCE] = 0.0

    return coefficients


def LASSO(returns, factRet, lambda_, K):
    """Estimate returns and covariance with a LASSO factor model.

    Parameters
    ----------
    returns:
        Matrix of monthly asset excess returns. Rows are months and columns
        are assets.
    factRet:
        Matrix of monthly factor returns. The model uses all eight factors.
    lambda_:
        Non-negative penalty weight. Larger values create sparser models by
        shrinking small coefficients to zero.
    K:
        Unused Best Subset Selection cardinality, kept for template
        compatibility.

    Returns
    -------
    model_utils.FactorModelResult
        Result object containing ``mu`` and ``Q`` plus fit diagnostics. The
        object can also be unpacked as ``mu, Q``.
    """

    observed_returns = as_numeric_matrix(returns)
    design_matrix = make_design_matrix(factRet)
    coefficients = np.zeros((design_matrix.shape[1], observed_returns.shape[1]))

    for asset_index in range(observed_returns.shape[1]):
        asset_returns = observed_returns[:, asset_index]
        coefficients[:, asset_index] = _fit_lasso_for_asset(
            design_matrix=design_matrix,
            asset_returns=asset_returns,
            lambda_=float(lambda_),
        )

    selected_counts = np.sum(
        np.abs(coefficients) > SELECTED_COEFFICIENT_TOLERANCE,
        axis=0,
    )

    factor_names = [
        "Mkt_RF",
        "SMB",
        "HML",
        "RMW",
        "CMA",
        "Mom",
        "ST_Rev",
        "LT_Rev",
    ]

    return covariance_from_factor_model(
        design_matrix=design_matrix,
        coefficients=coefficients,
        observed_returns=observed_returns,
        selected_counts=selected_counts,
        factor_names=factor_names,
        model_name="LASSO",
    )
