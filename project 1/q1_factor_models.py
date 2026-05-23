"""Question 1 script: fit and summarize the four factor models.

Run this file from any working directory with
``uv run python "project 1/q1_factor_models.py"`` or from inside
``project 1`` with ``uv run python q1_factor_models.py``.
"""

from __future__ import annotations

from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parent
SOURCE_DIR = PROJECT_ROOT / "source" / "Python"
sys.path.insert(0, str(SOURCE_DIR))

from project1_core import run_experiment, write_experiment_tables  # noqa: E402


def main() -> None:
    """Fit factor models and write in-sample result tables."""

    results = run_experiment()
    write_experiment_tables(results)
    print("Wrote factor-model tables to outputs/tables/.")


if __name__ == "__main__":
    main()
