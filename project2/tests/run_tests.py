"""Behavioral tests for the Project 2 Python implementation.

The tests use direct assertions so they can run with ``uv run python`` without
requiring a separate test runner. They focus on the reusable code that will be
submitted: data alignment, portfolio constraints, and backtest outputs.
"""

from __future__ import annotations

import json
from pathlib import Path
import sys

import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SOLUTION_DIR = PROJECT_ROOT / "solution"
NOTEBOOK_PATH = PROJECT_ROOT / "MMF1921_Project_2_Solution.ipynb"
REPORT_PATH = PROJECT_ROOT / "MMF1921_Project_2_Final_Report.md"
sys.path.insert(0, str(SOLUTION_DIR))

from project2_core import load_project_dataset, run_all_experiments, run_backtest  # noqa: E402
from project_function import project_function  # noqa: E402
from functions.strategies import ShrinkageFactorStrategy  # noqa: E402


def test_loaded_dataset_aligns_excess_returns_and_factors() -> None:
    """Computed asset excess returns should align exactly with factor dates."""

    dataset = load_project_dataset(dataset_id=1)

    assert dataset.asset_returns.shape == (180, 20)
    assert dataset.factor_returns.shape == (180, 8)
    assert dataset.risk_free.shape == (180,)
    assert dataset.return_dates == dataset.factor_dates
    assert dataset.return_dates[0] == "2002-01-31"
    assert dataset.asset_names[0] == "F"


def test_strategy_returns_long_only_fully_invested_weights() -> None:
    """The final strategy should produce valid weights for arbitrary asset counts."""

    rng = np.random.default_rng(7)
    asset_returns = rng.normal(loc=0.006, scale=0.04, size=(72, 17))
    factor_returns = rng.normal(loc=0.003, scale=0.03, size=(72, 8))
    previous_weights = np.full(17, 1.0 / 17.0)

    strategy = ShrinkageFactorStrategy(estimation_months=60, blend=0.35)
    weights = strategy.allocate(asset_returns, factor_returns, previous_weights)

    assert weights.shape == (17,)
    assert np.all(weights >= -1e-10)
    assert np.isclose(weights.sum(), 1.0, atol=1e-8)


def test_project_function_uses_latest_populated_weight_column() -> None:
    """The template-style weight history should preserve turnover control."""

    rng = np.random.default_rng(9)
    asset_returns = rng.normal(loc=0.005, scale=0.035, size=(72, 12))
    factor_returns = rng.normal(loc=0.002, scale=0.025, size=(72, 8))
    weight_history = np.zeros((12, 5))
    weight_history[0, 2] = 1.0

    weights = project_function(asset_returns, factor_returns, weight_history)

    assert weights[0] > 0.55
    assert np.isclose(weights.sum(), 1.0, atol=1e-8)


def test_backtest_produces_metrics_tables_and_weight_history() -> None:
    """A complete dataset backtest should return metrics and period weights."""

    dataset = load_project_dataset(dataset_id=3)
    result = run_backtest(dataset)

    assert result.dataset_id == 3
    assert result.metrics["period_count"] > 0
    assert np.isfinite(result.metrics["sharpe_ratio"])
    assert 0.0 <= result.metrics["average_turnover"] <= 2.0
    assert len(result.weight_rows) == result.metrics["period_count"] * len(
        dataset.asset_names
    )
    assert len(result.wealth_rows) > result.metrics["period_count"]


def test_all_experiments_cover_three_training_datasets() -> None:
    """The experiment runner should evaluate all supplied Project 2 datasets."""

    results = run_all_experiments()

    assert sorted(results) == [1, 2, 3]
    for dataset_id, result in results.items():
        assert result.dataset_id == dataset_id
        assert result.metrics["final_value"] > 0.0


def test_solution_notebook_executes_and_final_report_exists() -> None:
    """The student-facing notebook and final write-up should both run cleanly."""

    assert NOTEBOOK_PATH.exists()
    notebook_text = NOTEBOOK_PATH.read_text()
    assert "/Users/" not in notebook_text
    assert "MATLAB" not in notebook_text

    notebook = json.loads(notebook_text)
    namespace: dict[str, object] = {"__name__": "__notebook_test__"}
    for cell in notebook["cells"]:
        if cell["cell_type"] != "code":
            continue

        source = "".join(cell["source"])
        compiled_cell = compile(source, str(NOTEBOOK_PATH), "exec")
        exec(compiled_cell, namespace)

    report_text = REPORT_PATH.read_text()
    assert "## Conclusion" in report_text
    assert "TBD" not in report_text
    assert "TODO" not in report_text


def main() -> None:
    """Run all Project 2 tests."""

    test_loaded_dataset_aligns_excess_returns_and_factors()
    test_strategy_returns_long_only_fully_invested_weights()
    test_project_function_uses_latest_populated_weight_column()
    test_backtest_produces_metrics_tables_and_weight_history()
    test_all_experiments_cover_three_training_datasets()
    test_solution_notebook_executes_and_final_report_exists()
    print("All Project 2 tests passed.")


if __name__ == "__main__":
    main()
