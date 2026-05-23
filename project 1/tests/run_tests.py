"""Small behavioral tests for Project 1 factor-model code.

The tests use direct assertions instead of pytest so they can run in the
provided course environment without adding any packages beyond NumPy and
SciPy.
"""

from __future__ import annotations

from pathlib import Path
import sys

import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[1]
FUNCTIONS_DIR = PROJECT_ROOT / "solution" / "functions"
sys.path.insert(0, str(FUNCTIONS_DIR))

from BSS import BSS  # noqa: E402
from FF import FF  # noqa: E402
from LASSO import LASSO  # noqa: E402
from MVO import MVO  # noqa: E402
from model_utils import adjusted_r_squared  # noqa: E402
from OLS import OLS  # noqa: E402


def make_linear_sample() -> tuple[np.ndarray, np.ndarray]:
    """Create a small exact factor-model data set.

    Returns
    -------
    tuple[np.ndarray, np.ndarray]
        The first array is a 6-by-2 matrix of asset excess returns. The
        second array is a 6-by-8 matrix of factor returns.
    """

    factor_one = np.array([-0.03, -0.02, -0.01, 0.01, 0.02, 0.03])
    factor_two = np.array([0.02, -0.01, 0.03, -0.02, 0.01, -0.03])
    factors = np.zeros((6, 8))
    factors[:, 0] = factor_one
    factors[:, 1] = factor_two

    first_asset = 0.01 + 2.0 * factor_one
    second_asset = -0.005 + 0.5 * factor_two
    returns = np.column_stack([first_asset, second_asset])

    return returns, factors


def test_ols_returns_expected_mean_and_covariance() -> None:
    """OLS should recover exact linear means and near-zero residual risk."""

    returns, factors = make_linear_sample()

    result = OLS(returns, factors, lambda_=0.01, K=4)

    assert result.mu.shape == (2,)
    assert result.Q.shape == (2, 2)
    assert np.allclose(result.mu, returns.mean(axis=0), atol=1e-10)
    assert np.all(np.diag(result.Q) >= -1e-12)
    assert np.allclose(result.adjusted_r2, np.ones(2), atol=1e-10)


def test_ff_uses_first_three_factors() -> None:
    """FF should estimate a valid two-asset covariance matrix."""

    returns, factors = make_linear_sample()

    result = FF(returns, factors, lambda_=0.01, K=4)

    assert result.mu.shape == (2,)
    assert result.Q.shape == (2, 2)
    assert np.all(np.linalg.eigvalsh(result.Q) > -1e-10)


def test_lasso_and_bss_return_sparse_metadata() -> None:
    """Sparse models should expose selected coefficient counts."""

    returns, factors = make_linear_sample()

    lasso_result = LASSO(returns, factors, lambda_=0.001, K=4)
    bss_result = BSS(returns, factors, lambda_=0.001, K=4)

    assert lasso_result.selected_counts.shape == (2,)
    assert bss_result.selected_counts.shape == (2,)
    assert np.all(lasso_result.selected_counts <= 9)
    assert np.all(bss_result.selected_counts <= 4)
    assert np.all(np.linalg.eigvalsh(bss_result.Q) > -1e-10)


def test_adjusted_r_squared_counts_selected_factors_not_intercept() -> None:
    """Adjusted R2 should penalize selected factors, not assume an intercept."""

    observations = np.array([[1.0], [2.0], [3.0], [4.0], [5.0]])
    fitted = np.array([[1.0], [2.1], [2.9], [4.1], [4.9]])
    selected_counts = np.array([2])
    intercept_selected = np.array([False])

    adjusted_values = adjusted_r_squared(
        observed_returns=observations,
        fitted_returns=fitted,
        selected_counts=selected_counts,
        intercept_selected=intercept_selected,
    )

    residual_sum_squares = float(np.sum((observations - fitted) ** 2))
    centered = observations - observations.mean(axis=0)
    total_sum_squares = float(np.sum(centered**2))
    r_squared = 1.0 - residual_sum_squares / total_sum_squares
    expected_adjusted = 1.0 - (1.0 - r_squared) * (5 - 1) / (5 - 2 - 1)

    assert np.allclose(adjusted_values, np.array([expected_adjusted]))


def test_mvo_respects_budget_target_and_no_short_sales() -> None:
    """MVO weights should sum to one and satisfy no-short-sale constraints."""

    mu = np.array([0.02, 0.01, 0.03])
    Q = np.array(
        [
            [0.04, 0.01, 0.00],
            [0.01, 0.03, 0.00],
            [0.00, 0.00, 0.05],
        ]
    )

    weights = MVO(mu, Q, targetRet=0.018)

    assert weights.shape == (3,)
    assert np.all(weights >= -1e-8)
    assert np.isclose(weights.sum(), 1.0, atol=1e-8)
    assert weights @ mu >= 0.018 - 1e-8


def test_mvo_reports_infeasible_target_instead_of_relaxing_it() -> None:
    """MVO should not silently lower the assignment's target return."""

    mu = np.array([0.01, 0.02])
    Q = np.eye(2)

    try:
        MVO(mu, Q, targetRet=0.03)
    except ValueError as error:
        assert "target return" in str(error)
    else:
        raise AssertionError("MVO should reject infeasible target returns.")


def test_notebook_uses_portable_project_root() -> None:
    """The submitted notebook should not contain a machine-specific path."""

    notebook_path = PROJECT_ROOT / "MMF1921_Project_1_Solution.ipynb"
    notebook_text = notebook_path.read_text()

    assert "/Users/gwh/" not in notebook_text


def main() -> None:
    """Run all tests in this module."""

    test_ols_returns_expected_mean_and_covariance()
    test_ff_uses_first_three_factors()
    test_lasso_and_bss_return_sparse_metadata()
    test_adjusted_r_squared_counts_selected_factors_not_intercept()
    test_mvo_respects_budget_target_and_no_short_sales()
    test_mvo_reports_infeasible_target_instead_of_relaxing_it()
    test_notebook_uses_portable_project_root()
    print("All Project 1 tests passed.")


if __name__ == "__main__":
    main()
