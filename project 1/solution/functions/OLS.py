"""Ordinary least squares factor model for Project 1."""

from __future__ import annotations

from model_utils import FactorModelResult, fit_least_squares_model


def OLS(
    returns: object,
    factRet: object,
    lambda_: float,
    K: int,
) -> FactorModelResult:
    """Estimate returns and covariance with all eight factors.

    Parameters
    ----------
    returns:
        Matrix of monthly asset excess returns. Rows are months and columns
        are assets.
    factRet:
        Matrix of monthly factor returns. The model uses all columns.
    lambda_:
        Unused LASSO tuning parameter, kept for template compatibility.
    K:
        Unused Best Subset Selection cardinality, kept for template
        compatibility.

    Returns
    -------
    model_utils.FactorModelResult
        Result object containing ``mu`` and ``Q`` plus fit diagnostics. The
        object can also be unpacked as ``mu, Q``.
    """

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

    return fit_least_squares_model(
        returns=returns,
        factors=factRet,
        factor_indices=None,
        factor_names=factor_names,
        model_name="OLS",
    )
