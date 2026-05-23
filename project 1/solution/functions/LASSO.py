"""Least absolute shrinkage and selection operator model for Project 1."""

from __future__ import annotations

import cvxpy as cp
import numpy as np

from model_utils import (
    FactorModelResult,
    SELECTED_COEFFICIENT_TOLERANCE,
    as_numeric_matrix,
    covariance_from_factor_model,
    make_design_matrix,
)


CVXPY_SOLVERS = ("CLARABEL", "OSQP", "SCS")


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

    coefficient_count = design_matrix.shape[1]
    coefficient_variable = cp.Variable(coefficient_count)
    residuals = asset_returns - design_matrix @ coefficient_variable
    squared_error = cp.sum_squares(residuals)
    absolute_penalty = float(lambda_) * cp.norm1(coefficient_variable)
    problem = cp.Problem(cp.Minimize(squared_error + absolute_penalty))

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
            coefficients = np.asarray(coefficient_variable.value, dtype=float)
            coefficients[np.abs(coefficients) < SELECTED_COEFFICIENT_TOLERANCE] = 0.0

            return coefficients

    if last_error is not None:
        raise RuntimeError("LASSO cvxpy solve failed.") from last_error

    raise RuntimeError(f"LASSO cvxpy solve ended with status {problem.status!r}.")


def LASSO(
    returns: object,
    factRet: object,
    lambda_: float,
    K: int,
) -> FactorModelResult:
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
    intercept_selected = np.abs(coefficients[0, :]) > SELECTED_COEFFICIENT_TOLERANCE

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
        intercept_selected=intercept_selected,
        factor_names=factor_names,
        model_name="LASSO",
    )
