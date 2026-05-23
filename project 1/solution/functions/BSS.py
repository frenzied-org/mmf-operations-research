"""Best Subset Selection factor model for Project 1."""

from __future__ import annotations

import numpy as np

from model_utils import (
    as_numeric_matrix,
    all_subsets,
    covariance_from_factor_model,
    make_design_matrix,
)


def _fit_best_subset_for_asset(
    design_matrix: np.ndarray,
    asset_returns: np.ndarray,
    K: int,
) -> np.ndarray:
    """Fit the best at-most-``K`` coefficient subset for one asset.

    The project has only nine possible coefficients: one intercept plus
    eight factor loadings. Exhaustive search is therefore exact and small:
    for ``K = 4`` there are 255 non-empty candidate subsets.
    """

    coefficient_count = design_matrix.shape[1]
    best_sse = np.inf
    best_coefficients = np.zeros(coefficient_count)

    for subset in all_subsets(max_size=K, coefficient_count=coefficient_count):
        subset_columns = list(subset)
        subset_design = design_matrix[:, subset_columns]
        subset_coefficients = np.linalg.lstsq(
            subset_design,
            asset_returns,
            rcond=None,
        )[0]

        fitted_returns = subset_design @ subset_coefficients
        residuals = asset_returns - fitted_returns
        sse = float(residuals @ residuals)

        if sse < best_sse:
            full_coefficients = np.zeros(coefficient_count)
            full_coefficients[subset_columns] = subset_coefficients
            best_sse = sse
            best_coefficients = full_coefficients

    return best_coefficients


def BSS(returns, factRet, lambda_, K):
    """Estimate returns and covariance with Best Subset Selection.

    Parameters
    ----------
    returns:
        Matrix of monthly asset excess returns. Rows are months and columns
        are assets.
    factRet:
        Matrix of monthly factor returns. The model uses all eight factors.
    lambda_:
        Unused LASSO tuning parameter, kept for template compatibility.
    K:
        Maximum number of non-zero coefficients, counting the intercept.

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
        coefficients[:, asset_index] = _fit_best_subset_for_asset(
            design_matrix=design_matrix,
            asset_returns=asset_returns,
            K=int(K),
        )

    selected_counts = np.sum(coefficients != 0.0, axis=0)
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
        model_name="BSS",
    )
