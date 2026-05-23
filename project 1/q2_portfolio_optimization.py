"""Question 2 script: run annual mean-variance portfolio optimization."""

from __future__ import annotations

from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parent
SOURCE_DIR = PROJECT_ROOT / "source" / "Python"
sys.path.insert(0, str(SOURCE_DIR))

from project1_core import run_experiment, write_experiment_tables, write_figures  # noqa: E402


def main() -> None:
    """Run the full portfolio experiment and write tables and figures."""

    results = run_experiment()
    write_experiment_tables(results)
    write_figures(results)
    print("Wrote portfolio tables to outputs/tables/ and figures to outputs/figures/.")


if __name__ == "__main__":
    main()
