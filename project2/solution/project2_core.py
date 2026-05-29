"""Core experiment code for MMF1921 Project 2.

This module mirrors the Project 1 structure while respecting Project 2's
competition rules. It loads the three supplied training datasets, runs a
six-month rolling backtest after the first five years, writes result tables,
and generates simple SVG figures without modifying the source templates.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import csv
import math
import sys
import time

import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SOURCE_DATA_DIR = PROJECT_ROOT / "source" / "Data"
OUTPUT_DIR = PROJECT_ROOT / "outputs"
TABLE_DIR = OUTPUT_DIR / "tables"
FIGURE_DIR = OUTPUT_DIR / "figures"
REPORT_PATH = PROJECT_ROOT / "MMF1921_Project_2_Final_Report.md"
FUNCTIONS_DIR = PROJECT_ROOT / "solution" / "functions"

if str(FUNCTIONS_DIR.parent) not in sys.path:
    sys.path.insert(0, str(FUNCTIONS_DIR.parent))

from functions.strategies import ShrinkageFactorStrategy  # noqa: E402


INITIAL_PORTFOLIO_VALUE = 100_000.0
CALIBRATION_MONTHS = 60
INVESTMENT_MONTHS = 6
MONTHS_PER_YEAR = 12
DATASET_IDS = [1, 2, 3]


@dataclass
class ProjectDataset:
    """Clean Project 2 market data.

    Parameters
    ----------
    dataset_id:
        Identifier from the supplied filenames: 1, 2, or 3.
    price_dates:
        Month-end dates for adjusted close prices.
    return_dates:
        Month-end dates for computed asset returns.
    factor_dates:
        Month-end dates for factor returns.
    asset_names:
        Asset labels from the price file.
    factor_names:
        Factor labels excluding the risk-free rate.
    prices:
        Adjusted close price matrix after dropping the first price row, so its
        rows align with ``return_dates``.
    asset_returns:
        Monthly asset excess-return matrix.
    factor_returns:
        Monthly factor-return matrix, excluding the risk-free rate.
    risk_free:
        Monthly risk-free-rate vector.
    """

    dataset_id: int
    price_dates: list[str]
    return_dates: list[str]
    factor_dates: list[str]
    asset_names: list[str]
    factor_names: list[str]
    prices: np.ndarray
    asset_returns: np.ndarray
    factor_returns: np.ndarray
    risk_free: np.ndarray


@dataclass
class BacktestResult:
    """Backtest output for one Project 2 dataset."""

    dataset_id: int
    metrics: dict[str, float]
    wealth_rows: list[list[object]]
    weight_rows: list[list[object]]
    turnover_rows: list[list[object]]


def read_csv_table(path: Path) -> tuple[list[str], list[list[str]]]:
    """Read a CSV file as a header row and data rows."""

    with path.open(newline="") as file:
        reader = csv.reader(file)
        header = next(reader)
        rows = list(reader)

    return header, rows


def _parse_numeric_matrix(rows: list[list[str]], start_column: int) -> np.ndarray:
    """Parse numeric CSV columns into a floating-point matrix."""

    return np.array(
        [[float(value) for value in row[start_column:]] for row in rows],
        dtype=float,
    )


def load_project_dataset(dataset_id: int) -> ProjectDataset:
    """Load and align one supplied Project 2 dataset."""

    price_path = SOURCE_DATA_DIR / f"MMF1921_AssetPrices_{dataset_id}.csv"
    factor_path = SOURCE_DATA_DIR / f"MMF1921_FactorReturns_{dataset_id}.csv"

    price_header, price_rows = read_csv_table(price_path)
    factor_header, factor_rows = read_csv_table(factor_path)

    raw_price_dates = [row[0] for row in price_rows]
    asset_names = price_header[1:]
    raw_prices = _parse_numeric_matrix(price_rows, start_column=1)

    factor_dates = [row[0] for row in factor_rows]
    cleaned_factor_header = [name.strip() for name in factor_header]
    risk_free_index = cleaned_factor_header.index("RF")
    factor_indices = [
        index
        for index in range(1, len(cleaned_factor_header))
        if index != risk_free_index
    ]
    factor_names = [cleaned_factor_header[index] for index in factor_indices]
    factor_returns = np.array(
        [[float(row[index]) for index in factor_indices] for row in factor_rows],
        dtype=float,
    )
    risk_free = np.array(
        [float(row[risk_free_index]) for row in factor_rows],
        dtype=float,
    )

    simple_returns = raw_prices[1:, :] / raw_prices[:-1, :] - 1.0
    asset_returns = simple_returns - risk_free.reshape(-1, 1)
    aligned_prices = raw_prices[1:, :]
    return_dates = raw_price_dates[1:]

    if return_dates != factor_dates:
        raise ValueError(f"Dataset {dataset_id} price and factor dates do not align.")

    return ProjectDataset(
        dataset_id=dataset_id,
        price_dates=raw_price_dates,
        return_dates=return_dates,
        factor_dates=factor_dates,
        asset_names=asset_names,
        factor_names=factor_names,
        prices=aligned_prices,
        asset_returns=asset_returns,
        factor_returns=factor_returns,
        risk_free=risk_free,
    )


def _portfolio_drift_weights(
    prices: np.ndarray,
    shares: np.ndarray,
    fallback_asset_count: int,
) -> tuple[float, np.ndarray]:
    """Calculate current value and pre-trade weights from shares and prices."""

    if shares is None:
        equal = np.full(fallback_asset_count, 1.0 / fallback_asset_count)
        return INITIAL_PORTFOLIO_VALUE, equal

    current_value = float(prices @ shares)
    if current_value <= 0.0:
        equal = np.full(fallback_asset_count, 1.0 / fallback_asset_count)
        return INITIAL_PORTFOLIO_VALUE, equal

    current_weights = prices * shares / current_value
    current_weights = np.maximum(current_weights, 0.0)

    return current_value, current_weights / current_weights.sum()


def run_backtest(
    dataset: ProjectDataset,
    strategy: ShrinkageFactorStrategy | None = None,
) -> BacktestResult:
    """Run the Project 2 rolling six-month portfolio experiment."""

    selected_strategy = strategy or ShrinkageFactorStrategy()
    asset_count = len(dataset.asset_names)
    total_months = dataset.asset_returns.shape[0]
    period_count = math.ceil((total_months - CALIBRATION_MONTHS) / INVESTMENT_MONTHS)

    shares: np.ndarray | None = None
    current_value = INITIAL_PORTFOLIO_VALUE
    wealth_rows: list[list[object]] = []
    weight_rows: list[list[object]] = []
    turnover_rows: list[list[object]] = []
    portfolio_values: list[float] = []
    portfolio_risk_free: list[float] = []

    for period_index in range(period_count):
        start_index = CALIBRATION_MONTHS + period_index * INVESTMENT_MONTHS
        end_index = min(start_index + INVESTMENT_MONTHS, total_months)
        if start_index >= total_months:
            break

        current_prices = dataset.prices[start_index - 1, :]
        current_value, pre_trade_weights = _portfolio_drift_weights(
            prices=current_prices,
            shares=shares,
            fallback_asset_count=asset_count,
        )
        if period_index == 0:
            current_value = INITIAL_PORTFOLIO_VALUE

        calibration_returns = dataset.asset_returns[:start_index, :]
        calibration_factors = dataset.factor_returns[:start_index, :]
        target_weights = selected_strategy.allocate(
            asset_returns=calibration_returns,
            factor_returns=calibration_factors,
            previous_weights=pre_trade_weights if period_index > 0 else None,
        )
        turnover = 0.0
        if period_index > 0:
            turnover = float(np.sum(np.abs(target_weights - pre_trade_weights)))

        shares = target_weights * current_value / current_prices

        for asset_name, weight in zip(dataset.asset_names, target_weights):
            weight_rows.append(
                [
                    dataset.dataset_id,
                    period_index + 1,
                    dataset.return_dates[start_index],
                    asset_name,
                    f"{float(weight):.8f}",
                ]
            )

        turnover_rows.append(
            [
                dataset.dataset_id,
                period_index + 1,
                dataset.return_dates[start_index],
                f"{turnover:.8f}",
            ]
        )

        for month_index in range(start_index, end_index):
            value = float(dataset.prices[month_index, :] @ shares)
            portfolio_values.append(value)
            portfolio_risk_free.append(float(dataset.risk_free[month_index]))
            wealth_rows.append(
                [
                    dataset.dataset_id,
                    dataset.return_dates[month_index],
                    f"{value:.2f}",
                ]
            )

    values = np.asarray(portfolio_values, dtype=float)
    if values.size < 2:
        raise ValueError("Backtest produced too few portfolio values.")

    portfolio_returns = values[1:] / values[:-1] - 1.0
    aligned_risk_free = np.asarray(portfolio_risk_free[1:], dtype=float)
    excess_returns = portfolio_returns - aligned_risk_free
    average_excess_return = float(np.mean(excess_returns))
    monthly_volatility = float(np.std(excess_returns, ddof=1))
    sharpe_ratio = 0.0
    if monthly_volatility > 0.0:
        sharpe_ratio = average_excess_return / monthly_volatility

    annualized_excess_return = (1.0 + average_excess_return) ** MONTHS_PER_YEAR - 1.0
    annualized_volatility = monthly_volatility * math.sqrt(MONTHS_PER_YEAR)
    average_turnover = float(np.mean([float(row[3]) for row in turnover_rows[1:]]))

    metrics = {
        "period_count": float(len(turnover_rows)),
        "average_monthly_excess_return": average_excess_return,
        "monthly_volatility": monthly_volatility,
        "annualized_excess_return": annualized_excess_return,
        "annualized_volatility": annualized_volatility,
        "sharpe_ratio": sharpe_ratio,
        "average_turnover": average_turnover,
        "final_value": float(values[-1]),
    }

    return BacktestResult(
        dataset_id=dataset.dataset_id,
        metrics=metrics,
        wealth_rows=wealth_rows,
        weight_rows=weight_rows,
        turnover_rows=turnover_rows,
    )


def run_all_experiments() -> dict[int, BacktestResult]:
    """Run the backtest on all three supplied Project 2 datasets."""

    return {
        dataset_id: run_backtest(load_project_dataset(dataset_id))
        for dataset_id in DATASET_IDS
    }


def ensure_output_dirs() -> None:
    """Create output folders used by the experiment."""

    TABLE_DIR.mkdir(parents=True, exist_ok=True)
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)


def write_csv(path: Path, header: list[str], rows: list[list[object]]) -> None:
    """Write a CSV table."""

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(rows)


def write_experiment_tables(results: dict[int, BacktestResult]) -> None:
    """Write Project 2 result tables under ``outputs/tables``."""

    ensure_output_dirs()
    metric_rows: list[list[object]] = []
    wealth_rows: list[list[object]] = []
    weight_rows: list[list[object]] = []
    turnover_rows: list[list[object]] = []

    for dataset_id, result in results.items():
        metric_rows.append(
            [
                dataset_id,
                int(result.metrics["period_count"]),
                f"{result.metrics['average_monthly_excess_return']:.8f}",
                f"{result.metrics['monthly_volatility']:.8f}",
                f"{result.metrics['annualized_excess_return']:.8f}",
                f"{result.metrics['annualized_volatility']:.8f}",
                f"{result.metrics['sharpe_ratio']:.6f}",
                f"{result.metrics['average_turnover']:.6f}",
                f"{result.metrics['final_value']:.2f}",
            ]
        )
        wealth_rows.extend(result.wealth_rows)
        weight_rows.extend(result.weight_rows)
        turnover_rows.extend(result.turnover_rows)

    write_csv(
        TABLE_DIR / "performance_summary.csv",
        [
            "dataset",
            "period_count",
            "average_monthly_excess_return",
            "monthly_volatility",
            "annualized_excess_return",
            "annualized_volatility",
            "sharpe_ratio",
            "average_turnover",
            "final_value",
        ],
        metric_rows,
    )
    write_csv(
        TABLE_DIR / "portfolio_values.csv",
        ["dataset", "date", "portfolio_value"],
        wealth_rows,
    )
    write_csv(
        TABLE_DIR / "portfolio_weights.csv",
        ["dataset", "period", "rebalance_date", "asset", "weight"],
        weight_rows,
    )
    write_csv(
        TABLE_DIR / "turnover.csv",
        ["dataset", "period", "rebalance_date", "turnover"],
        turnover_rows,
    )


def _scale_points(values: np.ndarray, width: int, height: int, padding: int) -> str:
    """Scale a value series into SVG polyline points."""

    x_values = np.linspace(padding, width - padding, len(values))
    minimum = float(np.min(values))
    maximum = float(np.max(values))
    scale = max(maximum - minimum, 1.0)
    y_values = height - padding - (values - minimum) / scale * (height - 2 * padding)

    return " ".join(f"{x:.1f},{y:.1f}" for x, y in zip(x_values, y_values))


def write_figures(results: dict[int, BacktestResult]) -> None:
    """Write simple SVG figures for the formal report."""

    ensure_output_dirs()
    colors = {1: "#1f77b4", 2: "#2ca02c", 3: "#d62728"}
    width = 900
    height = 420
    padding = 55

    all_values = np.array(
        [float(row[2]) for result in results.values() for row in result.wealth_rows],
        dtype=float,
    )
    minimum = float(np.min(all_values))
    maximum = float(np.max(all_values))

    wealth_lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="white"/>',
        f'<text x="{width / 2}" y="28" text-anchor="middle" font-size="20" font-family="Arial">Project 2 Portfolio Wealth</text>',
        f'<line x1="{padding}" y1="{height - padding}" x2="{width - padding}" y2="{height - padding}" stroke="#333"/>',
        f'<line x1="{padding}" y1="{padding}" x2="{padding}" y2="{height - padding}" stroke="#333"/>',
        f'<text x="12" y="{padding}" font-size="12" font-family="Arial">${maximum:,.0f}</text>',
        f'<text x="12" y="{height - padding}" font-size="12" font-family="Arial">${minimum:,.0f}</text>',
    ]

    for dataset_id, result in results.items():
        values = np.array([float(row[2]) for row in result.wealth_rows], dtype=float)
        points = _scale_points(values, width, height, padding)
        wealth_lines.append(
            f'<polyline points="{points}" fill="none" stroke="{colors[dataset_id]}" stroke-width="2.5"/>'
        )

    for index, dataset_id in enumerate(DATASET_IDS):
        y_position = 58 + 22 * index
        wealth_lines.append(
            f'<rect x="{width - 150}" y="{y_position - 10}" width="12" height="12" fill="{colors[dataset_id]}"/>'
        )
        wealth_lines.append(
            f'<text x="{width - 130}" y="{y_position}" font-size="13" font-family="Arial">Dataset {dataset_id}</text>'
        )

    wealth_lines.append("</svg>")
    (FIGURE_DIR / "wealth_evolution.svg").write_text("\n".join(wealth_lines))

    _write_weight_svg(results[3])


def _write_weight_svg(result: BacktestResult) -> None:
    """Write a stacked bar SVG of Dataset 3 rebalance weights."""

    periods = sorted({int(row[1]) for row in result.weight_rows})
    assets = sorted({str(row[3]) for row in result.weight_rows})
    weights = {
        (int(row[1]), str(row[3])): float(row[4])
        for row in result.weight_rows
        if float(row[4]) > 0.01
    }
    active_assets = [
        asset
        for asset in assets
        if any((period, asset) in weights for period in periods)
    ]
    active_assets = active_assets[:12]

    width = 900
    height = 420
    padding = 55
    bar_width = (width - 2 * padding) / len(periods)
    palette = [
        "#1f77b4",
        "#ff7f0e",
        "#2ca02c",
        "#d62728",
        "#9467bd",
        "#8c564b",
        "#e377c2",
        "#7f7f7f",
        "#bcbd22",
        "#17becf",
        "#393b79",
        "#637939",
    ]

    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="white"/>',
        f'<text x="{width / 2}" y="28" text-anchor="middle" font-size="20" font-family="Arial">Dataset 3 Portfolio Weights</text>',
        f'<line x1="{padding}" y1="{height - padding}" x2="{width - padding}" y2="{height - padding}" stroke="#333"/>',
        f'<line x1="{padding}" y1="{padding}" x2="{padding}" y2="{height - padding}" stroke="#333"/>',
        f'<text x="15" y="{padding}" font-size="12" font-family="Arial">100%</text>',
        f'<text x="20" y="{height - padding}" font-size="12" font-family="Arial">0%</text>',
    ]

    for period_index, period in enumerate(periods):
        x_left = padding + period_index * bar_width + 7
        y_top = height - padding
        for asset_index, asset in enumerate(active_assets):
            weight = weights.get((period, asset), 0.0)
            segment_height = weight * (height - 2 * padding)
            if segment_height <= 0.0:
                continue
            y_top -= segment_height
            color = palette[asset_index % len(palette)]
            lines.append(
                f'<rect x="{x_left:.1f}" y="{y_top:.1f}" width="{bar_width - 14:.1f}" height="{segment_height:.1f}" fill="{color}"/>'
            )
        lines.append(
            f'<text x="{x_left + (bar_width - 14) / 2:.1f}" y="{height - 18}" text-anchor="middle" font-size="11" font-family="Arial">{period}</text>'
        )

    for index, asset in enumerate(active_assets):
        y_position = 58 + 20 * index
        color = palette[index % len(palette)]
        lines.append(
            f'<rect x="{width - 150}" y="{y_position - 10}" width="12" height="12" fill="{color}"/>'
        )
        lines.append(
            f'<text x="{width - 130}" y="{y_position}" font-size="13" font-family="Arial">{asset}</text>'
        )

    lines.append("</svg>")
    (FIGURE_DIR / "portfolio_weights.svg").write_text("\n".join(lines))


def _markdown_table(header: list[str], rows: list[list[object]]) -> str:
    """Render a small Markdown table."""

    table_lines = [
        "| " + " | ".join(header) + " |",
        "| " + " | ".join(["---"] * len(header)) + " |",
    ]
    for row in rows:
        table_lines.append("| " + " | ".join(str(value) for value in row) + " |")

    return "\n".join(table_lines)


def write_report(results: dict[int, BacktestResult], runtime_seconds: float) -> Path:
    """Write the formal Project 2 report in Markdown."""

    performance_rows = []
    for dataset_id, result in results.items():
        performance_rows.append(
            [
                dataset_id,
                f"{result.metrics['sharpe_ratio']:.4f}",
                f"{result.metrics['average_turnover']:.4f}",
                f"{result.metrics['annualized_excess_return']:.2%}",
                f"{result.metrics['annualized_volatility']:.2%}",
                f"\\${result.metrics['final_value']:,.2f}",
            ]
        )

    report = f"""# MMF1921 Project 2: Automated Asset Management Strategy

## Introduction

This report develops a Python-only automated asset management system for the
Project 2 investment competition. The algorithm is designed for monthly equity
and equity-factor data. It uses the first five years of each dataset for
initial calibration and then rebalances every six months.

The assessment criteria are ex-post Sharpe ratio, average turnover, and runtime.
A Sharpe ratio is average excess return divided by volatility, where excess
return means portfolio return minus the risk-free rate. Turnover is the sum of
absolute changes in portfolio weights at a rebalance.

## Methodology

The final strategy is a shrinkage factor-model mean-variance strategy. At each
rebalance date, the algorithm uses the most recent 60 monthly observations. For
asset $i$, the factor model is

$$
r_i - r_f = \\alpha_i + \\sum_k \\beta_{{ik}} f_k + \\epsilon_i
$$

where $r_i$ is the asset return, $r_f$ is the risk-free rate, $\\alpha_i$ is the
intercept, $\\beta_{{ik}}$ is the loading of asset $i$ on factor $k$, $f_k$ is
factor $k$, and $\\epsilon_i$ is the residual return not explained by the
factors.

The fitted model gives an expected excess-return vector $\\mu$ and covariance
matrix $Q$. The covariance estimate is

$$
Q = B^T \\Sigma_f B + D_\\epsilon
$$

where $B$ is the factor-loading matrix, $\\Sigma_f$ is the factor covariance
matrix, and $D_\\epsilon$ is the diagonal matrix of residual variances.

Expected returns are noisy, especially with only monthly data, so the raw
factor-model expected returns are shrunk toward their cross-sectional average.
The optimizer solves a long-only mean-variance problem with a maximum single
asset weight:

$$
\\min_x \\; \\frac12 x^T Q x - \\gamma \\mu^T x
$$

subject to

$$
\\sum_i x_i = 1, \\quad 0 \\le x_i \\le 0.20
$$

where $x$ is the portfolio-weight vector and $\\gamma$ controls the strength of
the expected-return tilt.

## Turnover Control

Project 2 explicitly grades average turnover, so the final portfolio is blended
with the current pre-trade portfolio after the first rebalance. If $x^*$ is the
new optimized portfolio and $x_0$ is the portfolio after market drift, the
traded portfolio is

$$
x = b x^* + (1-b) x_0
$$

where $b = 0.40$. This reduces unnecessary trading while still allowing the
strategy to adapt to changing factor and risk estimates.

## Training Dataset Results

{
        _markdown_table(
            [
                "Dataset",
                "Sharpe ratio",
                "Average turnover",
                "Annualized excess return",
                "Annualized volatility",
                "Final value",
            ],
            performance_rows,
        )
    }

The full output tables are saved in `outputs/tables/`. The wealth and portfolio
composition figures are saved in `outputs/figures/`.

![Portfolio wealth evolution](outputs/figures/wealth_evolution.svg)

![Dataset 3 portfolio weights](outputs/figures/portfolio_weights.svg)

## Discussion

The strategy deliberately avoids aggressive return forecasting. Pure
mean-variance optimization can place extreme weights on assets with slightly
higher estimated returns, but those estimates are unstable in short monthly
samples. Shrinking expected returns and capping single-name weights make the
portfolio less sensitive to estimation error.

The main strength of the algorithm is robustness: it works for different asset
counts, uses only historical information available at each rebalance, and keeps
turnover under control. The main weakness is that conservative shrinkage may
miss strong market regimes where a more aggressive return forecast would have
performed better.

## Conclusion

The selected Project 2 algorithm combines a course-relevant multifactor model
with constrained mean-variance optimization and explicit turnover control. The
implementation is Python-only, uses the provided datasets without modifying
source files, and runs quickly across all three training datasets.

Runtime for the full experiment was {runtime_seconds:.2f} seconds.
"""

    REPORT_PATH.write_text(report)

    return REPORT_PATH


def run_and_write_outputs() -> dict[int, BacktestResult]:
    """Run all Project 2 experiments and write tables, figures, and report."""

    start_time = time.time()
    results = run_all_experiments()
    runtime_seconds = time.time() - start_time
    write_experiment_tables(results)
    write_figures(results)
    write_report(results, runtime_seconds)

    return results


def main() -> None:
    """Command-line entry point for the Project 2 experiment."""

    run_and_write_outputs()
    print(f"Wrote tables to {TABLE_DIR.relative_to(PROJECT_ROOT)}")
    print(f"Wrote figures to {FIGURE_DIR.relative_to(PROJECT_ROOT)}")
    print(f"Wrote report to {REPORT_PATH.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
