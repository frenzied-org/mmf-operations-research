"""Submission-facing Project 2 allocation function."""

from __future__ import annotations

import numpy as np

from functions.strategies import project_function as _project_function


def project_function(
    periodReturns: np.ndarray,
    periodFactRet: np.ndarray,
    x0: np.ndarray | None = None,
) -> np.ndarray:
    """Return the portfolio allocation for the next six-month period.

    Parameters
    ----------
    periodReturns:
        Growing matrix of monthly asset excess returns observed so far.
    periodFactRet:
        Growing matrix of monthly factor returns observed so far, excluding the
        risk-free-rate column.
    x0:
        Optional current portfolio weights before rebalancing. The Project 2
        Python template passes this argument, so it is accepted for
        compatibility.

    Returns
    -------
    np.ndarray
        Long-only fully invested portfolio weights.
    """

    previous_weights = None
    if x0 is not None:
        candidate = np.asarray(x0, dtype=float)
        if candidate.ndim == 2:
            column_sums = np.sum(np.maximum(candidate, 0.0), axis=0)
            populated_columns = np.where(column_sums > 0.0)[0]
            if populated_columns.size > 0:
                previous_weights = candidate[:, int(populated_columns[-1])]
        else:
            previous_weights = candidate.reshape(-1)

    return _project_function(periodReturns, periodFactRet, previous_weights)
