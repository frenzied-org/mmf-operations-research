"""Fama-French three-factor model for Project 1."""

from __future__ import annotations

from model_utils import FactorModelResult, fit_least_squares_model


def FF(
    returns: object,
    factRet: object,
    lambda_: float,
    K: int,
) -> FactorModelResult:
    """Estimate returns and covariance with the first three factors.

    Parameters
    ----------
    returns:
        Matrix of monthly asset excess returns. Rows are months and columns
        are assets.
    factRet:
        Matrix of monthly factor returns. The first three columns are
        interpreted as market excess return, size, and value.
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

    factor_names = ["Mkt_RF", "SMB", "HML"]

    return fit_least_squares_model(
        returns=returns,
        factors=factRet,
        factor_indices=[0, 1, 2],
        factor_names=factor_names,
        model_name="FF",
    )
