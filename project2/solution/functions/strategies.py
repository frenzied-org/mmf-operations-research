"""Trading strategies for MMF1921 Project 2."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from functions.estimators import estimate_ols_factor_model, shrink_expected_returns
from functions.optimization import equal_weight, minimum_variance_with_return_tilt


@dataclass
class ShrinkageFactorStrategy:
    """Factor-model strategy with return shrinkage and turnover control.

    Parameters
    ----------
    estimation_months:
        Number of most recent monthly observations used at each rebalance.
    return_shrinkage:
        Weight used to shrink asset expected returns toward their average.
    blend:
        Weight on the newly optimized portfolio. The remaining weight stays in
        the previous portfolio, which directly lowers turnover.
    risk_aversion:
        Strength of the expected-return tilt in the mean-variance objective.
    max_weight:
        Maximum weight allowed in one asset.
    """

    estimation_months: int = 60
    return_shrinkage: float = 0.60
    blend: float = 0.40
    risk_aversion: float = 3.0
    max_weight: float = 0.20

    def allocate(
        self,
        asset_returns: np.ndarray,
        factor_returns: np.ndarray,
        previous_weights: np.ndarray | None = None,
    ) -> np.ndarray:
        """Return long-only portfolio weights for the next investment period."""

        returns = np.asarray(asset_returns, dtype=float)
        factors = np.asarray(factor_returns, dtype=float)
        asset_count = returns.shape[1]

        if returns.shape[0] < 12:
            return equal_weight(asset_count)

        window_size = min(self.estimation_months, returns.shape[0])
        recent_returns = returns[-window_size:, :]
        recent_factors = factors[-window_size:, :]

        estimate = estimate_ols_factor_model(recent_returns, recent_factors)
        expected_returns = shrink_expected_returns(
            estimate.expected_returns,
            shrinkage_weight=self.return_shrinkage,
        )
        optimized_weights = minimum_variance_with_return_tilt(
            expected_returns=expected_returns,
            covariance=estimate.covariance,
            risk_aversion=self.risk_aversion,
            max_weight=min(self.max_weight, 1.0),
        )

        if previous_weights is None:
            return optimized_weights

        previous = np.asarray(previous_weights, dtype=float).reshape(-1)
        if previous.shape != optimized_weights.shape or previous.sum() <= 0.0:
            return optimized_weights

        previous = np.maximum(previous, 0.0)
        previous = previous / previous.sum()
        blended_weights = self.blend * optimized_weights
        blended_weights = blended_weights + (1.0 - self.blend) * previous
        blended_weights = np.maximum(blended_weights, 0.0)

        return blended_weights / blended_weights.sum()


def project_function(
    period_returns: np.ndarray,
    period_factor_returns: np.ndarray,
    previous_weights: np.ndarray | None = None,
) -> np.ndarray:
    """Assignment-compatible portfolio allocation function.

    The supplied notebook passes growing historical return windows into this
    function. The function accepts NumPy arrays and also works with objects
    such as pandas DataFrames because ``np.asarray`` converts them to arrays.
    """

    strategy = ShrinkageFactorStrategy()

    return strategy.allocate(
        asset_returns=np.asarray(period_returns, dtype=float),
        factor_returns=np.asarray(period_factor_returns, dtype=float),
        previous_weights=previous_weights,
    )
