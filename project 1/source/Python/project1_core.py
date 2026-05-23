"""Core experiment code for MMF1921 Project 1.

This module keeps the scripts thin. It loads the supplied CSV files, fits
the four factor models, runs annual long-only mean-variance optimization,
and writes result tables and simple SVG figures.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import csv
import sys

import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[2]
PYTHON_SOURCE_DIR = PROJECT_ROOT / "source" / "Python"
FUNCTIONS_DIR = PYTHON_SOURCE_DIR / "functions"
OUTPUT_DIR = PROJECT_ROOT / "outputs"
TABLE_DIR = OUTPUT_DIR / "tables"
FIGURE_DIR = OUTPUT_DIR / "figures"

if str(FUNCTIONS_DIR) not in sys.path:
    sys.path.insert(0, str(FUNCTIONS_DIR))

from BSS import BSS  # noqa: E402
from FF import FF  # noqa: E402
from LASSO import LASSO  # noqa: E402
from MVO import MVO  # noqa: E402
from OLS import OLS  # noqa: E402


LASSO_LAMBDA = 0.04
BSS_K = 4
INITIAL_PORTFOLIO_VALUE = 100_000.0
TRADING_MONTHS_PER_YEAR = 12
MODEL_FUNCTIONS = [OLS, FF, LASSO, BSS]
MODEL_NAMES = ["OLS", "FF", "LASSO", "BSS"]


@dataclass
class MarketData:
    """Market data loaded from the supplied project CSV files.

    Parameters
    ----------
    price_dates:
        Month-end dates for adjusted close prices, stored as ISO strings.
    tickers:
        Stock ticker labels.
    prices:
        Adjusted close price matrix. Rows are months and columns are stocks.
    factor_dates:
        Month-end dates for factor returns, stored as ISO strings.
    factor_names:
        Factor labels excluding the risk-free rate.
    factors:
        Monthly factor return matrix. Rows are months and columns are factors.
    risk_free:
        Monthly risk-free rate vector.
    return_dates:
        Month-end dates for computed asset excess returns.
    excess_returns:
        Monthly stock returns minus the monthly risk-free rate.
    """

    price_dates: list[str]
    tickers: list[str]
    prices: np.ndarray
    factor_dates: list[str]
    factor_names: list[str]
    factors: np.ndarray
    risk_free: np.ndarray
    return_dates: list[str]
    excess_returns: np.ndarray


def read_csv_table(path: Path) -> tuple[list[str], list[list[str]]]:
    """Read a CSV file as header and rows."""

    with path.open(newline="") as file:
        reader = csv.reader(file)
        header = next(reader)
        rows = list(reader)

    return header, rows


def load_market_data() -> MarketData:
    """Load supplied asset-price and factor-return CSV files.

    Returns
    -------
    MarketData
        Clean matrices with aligned monthly excess returns.
    """

    price_header, price_rows = read_csv_table(
        PYTHON_SOURCE_DIR / "MMF1921_AssetPrices.csv"
    )
    factor_header, factor_rows = read_csv_table(
        PYTHON_SOURCE_DIR / "MMF1921_FactorReturns.csv"
    )

    price_dates = [row[0] for row in price_rows]
    tickers = price_header[1:]
    prices = np.array([[float(value) for value in row[1:]] for row in price_rows])

    factor_dates = [row[0] for row in factor_rows]
    stripped_factor_header = [name.strip() for name in factor_header]
    risk_free_index = stripped_factor_header.index("RF")
    factor_indices = [
        index for index in range(1, len(factor_header)) if index != risk_free_index
    ]
    factor_names = [stripped_factor_header[index] for index in factor_indices]
    factors = np.array(
        [[float(row[index]) for index in factor_indices] for row in factor_rows]
    )
    risk_free = np.array([float(row[risk_free_index]) for row in factor_rows])

    simple_returns = prices[1:, :] / prices[:-1, :] - 1.0
    excess_returns = simple_returns - risk_free.reshape(-1, 1)
    return_dates = price_dates[1:]

    if return_dates != factor_dates:
        raise ValueError("Asset return dates do not align with factor return dates.")

    return MarketData(
        price_dates=price_dates,
        tickers=tickers,
        prices=prices,
        factor_dates=factor_dates,
        factor_names=factor_names,
        factors=factors,
        risk_free=risk_free,
        return_dates=return_dates,
        excess_returns=excess_returns,
    )


def date_window_indices(dates: list[str], start_date: str, end_date: str) -> np.ndarray:
    """Return row indices whose ISO date string lies inside a closed window."""

    return np.array(
        [index for index, date in enumerate(dates) if start_date <= date <= end_date],
        dtype=int,
    )


def geometric_mean_return(returns: np.ndarray) -> float:
    """Calculate the geometric mean of monthly returns."""

    gross_returns = 1.0 + np.asarray(returns, dtype=float)
    log_gross_returns = np.log(gross_returns)
    mean_log_return = float(np.mean(log_gross_returns))

    return float(np.exp(mean_log_return) - 1.0)


def ensure_output_dirs() -> None:
    """Create output folders used by the scripts."""

    TABLE_DIR.mkdir(parents=True, exist_ok=True)
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)


def write_csv(path: Path, header: list[str], rows: list[list[object]]) -> None:
    """Write rows to a CSV file."""

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(rows)


def run_experiment() -> dict[str, object]:
    """Run the full rolling factor-model and portfolio experiment.

    Returns
    -------
    dict[str, object]
        Dictionary containing fit diagnostics, portfolio values, weights,
        and performance summaries used by the report generator.
    """

    data = load_market_data()
    fit_rows: list[list[object]] = []
    selected_rows: list[list[object]] = []
    weight_rows: list[list[object]] = []
    wealth_rows: list[list[object]] = []
    wealth_by_model: dict[str, list[tuple[str, float]]] = {
        model_name: [] for model_name in MODEL_NAMES
    }

    current_values = {model_name: INITIAL_PORTFOLIO_VALUE for model_name in MODEL_NAMES}
    current_shares = {
        model_name: np.zeros(len(data.tickers), dtype=float)
        for model_name in MODEL_NAMES
    }

    for period_index in range(5):
        calibration_start_year = 2008 + period_index
        test_year = 2012 + period_index
        calibration_start = f"{calibration_start_year}-01-01"
        calibration_end = f"{calibration_start_year + 3}-12-31"
        test_start = f"{test_year}-01-01"
        test_end = f"{test_year}-12-31"
        rebalance_date = f"{test_year - 1}-12-31"

        calibration_indices = date_window_indices(
            data.return_dates,
            calibration_start,
            calibration_end,
        )
        test_price_indices = date_window_indices(data.price_dates, test_start, test_end)
        rebalance_price_index = data.price_dates.index(rebalance_date)

        calibration_returns = data.excess_returns[calibration_indices, :]
        calibration_factors = data.factors[calibration_indices, :]
        rebalance_prices = data.prices[rebalance_price_index, :]
        period_prices = data.prices[test_price_indices, :]
        period_price_dates = [data.price_dates[index] for index in test_price_indices]

        if period_index > 0:
            for model_name in MODEL_NAMES:
                current_values[model_name] = float(
                    rebalance_prices @ current_shares[model_name]
                )

        target_return = geometric_mean_return(calibration_factors[:, 0])
        model_results = [
            model_function(
                calibration_returns, calibration_factors, LASSO_LAMBDA, BSS_K
            )
            for model_function in MODEL_FUNCTIONS
        ]

        for model_name, result in zip(MODEL_NAMES, model_results):
            mean_adjusted_r2 = float(np.mean(result.adjusted_r2))
            mean_selected_count = float(np.mean(result.selected_counts))
            fit_rows.append(
                [
                    period_index + 1,
                    calibration_start,
                    calibration_end,
                    model_name,
                    f"{mean_adjusted_r2:.6f}",
                    f"{mean_selected_count:.2f}",
                    f"{target_return:.6f}",
                ]
            )

            for ticker, adjusted_r2, selected_count in zip(
                data.tickers,
                result.adjusted_r2,
                result.selected_counts,
            ):
                selected_rows.append(
                    [
                        period_index + 1,
                        model_name,
                        ticker,
                        f"{float(adjusted_r2):.6f}",
                        int(selected_count),
                    ]
                )

            weights = MVO(result.mu, result.Q, target_return)
            current_shares[model_name] = (
                weights * current_values[model_name] / rebalance_prices
            )

            for ticker, weight in zip(data.tickers, weights):
                weight_rows.append(
                    [
                        period_index + 1,
                        test_year,
                        model_name,
                        ticker,
                        f"{float(weight):.8f}",
                    ]
                )

            if not wealth_by_model[model_name]:
                wealth_by_model[model_name].append(
                    (rebalance_date, current_values[model_name])
                )
                wealth_rows.append(
                    [
                        rebalance_date,
                        model_name,
                        f"{current_values[model_name]:.2f}",
                    ]
                )

            for price_date, prices_at_date in zip(period_price_dates, period_prices):
                portfolio_value = float(prices_at_date @ current_shares[model_name])
                wealth_by_model[model_name].append((price_date, portfolio_value))
                wealth_rows.append([price_date, model_name, f"{portfolio_value:.2f}"])

    performance_rows: list[list[object]] = []
    for model_name in MODEL_NAMES:
        values = np.array(
            [value for _, value in wealth_by_model[model_name]], dtype=float
        )
        monthly_returns = values[1:] / values[:-1] - 1.0
        average_monthly_return = float(np.mean(monthly_returns))
        monthly_volatility = float(np.std(monthly_returns, ddof=1))
        annualized_return = (
            1.0 + average_monthly_return
        ) ** TRADING_MONTHS_PER_YEAR - 1.0
        annualized_volatility = monthly_volatility * np.sqrt(TRADING_MONTHS_PER_YEAR)
        sharpe_ratio = annualized_return / annualized_volatility
        final_value = float(values[-1])

        performance_rows.append(
            [
                model_name,
                f"{average_monthly_return:.6f}",
                f"{monthly_volatility:.6f}",
                f"{annualized_return:.6f}",
                f"{annualized_volatility:.6f}",
                f"{sharpe_ratio:.4f}",
                f"{final_value:.2f}",
            ]
        )

    return {
        "data": data,
        "fit_rows": fit_rows,
        "selected_rows": selected_rows,
        "weight_rows": weight_rows,
        "wealth_rows": wealth_rows,
        "wealth_by_model": wealth_by_model,
        "performance_rows": performance_rows,
    }


def write_experiment_tables(results: dict[str, object]) -> None:
    """Write experiment result tables to ``outputs/tables``."""

    ensure_output_dirs()
    write_csv(
        TABLE_DIR / "in_sample_fit_summary.csv",
        [
            "period",
            "calibration_start",
            "calibration_end",
            "model",
            "mean_adjusted_r2",
            "mean_selected_coefficients",
            "target_return",
        ],
        results["fit_rows"],
    )
    write_csv(
        TABLE_DIR / "asset_fit_details.csv",
        ["period", "model", "ticker", "adjusted_r2", "selected_coefficients"],
        results["selected_rows"],
    )
    write_csv(
        TABLE_DIR / "portfolio_weights.csv",
        ["period", "test_year", "model", "ticker", "weight"],
        results["weight_rows"],
    )
    write_csv(
        TABLE_DIR / "portfolio_values.csv",
        ["date", "model", "portfolio_value"],
        results["wealth_rows"],
    )
    write_csv(
        TABLE_DIR / "performance_summary.csv",
        [
            "model",
            "average_monthly_return",
            "monthly_volatility",
            "annualized_return",
            "annualized_volatility",
            "sharpe_ratio",
            "final_value",
        ],
        results["performance_rows"],
    )


def _polyline_points(values: np.ndarray, width: int, height: int, padding: int) -> str:
    """Scale a numeric series to SVG polyline coordinates."""

    x_values = np.linspace(padding, width - padding, len(values))
    minimum = float(np.min(values))
    maximum = float(np.max(values))
    scale = max(maximum - minimum, 1.0)
    y_values = height - padding - (values - minimum) / scale * (height - 2 * padding)

    return " ".join(f"{x:.1f},{y:.1f}" for x, y in zip(x_values, y_values))


def write_wealth_svg(wealth_by_model: dict[str, list[tuple[str, float]]]) -> None:
    """Write a simple SVG line chart of portfolio wealth."""

    colors = {"OLS": "#1f77b4", "FF": "#2ca02c", "LASSO": "#d62728", "BSS": "#9467bd"}
    width = 900
    height = 420
    padding = 55
    all_values = np.array(
        [value for series in wealth_by_model.values() for _, value in series],
        dtype=float,
    )
    minimum = float(np.min(all_values))
    maximum = float(np.max(all_values))

    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="white"/>',
        f'<text x="{width / 2}" y="28" text-anchor="middle" font-size="20" font-family="Arial">Portfolio Wealth Evolution</text>',
        f'<line x1="{padding}" y1="{height - padding}" x2="{width - padding}" y2="{height - padding}" stroke="#333"/>',
        f'<line x1="{padding}" y1="{padding}" x2="{padding}" y2="{height - padding}" stroke="#333"/>',
        f'<text x="{padding}" y="{height - 18}" font-size="12" font-family="Arial">2012</text>',
        f'<text x="{width - padding}" y="{height - 18}" text-anchor="end" font-size="12" font-family="Arial">2016</text>',
        f'<text x="12" y="{padding}" font-size="12" font-family="Arial">${maximum:,.0f}</text>',
        f'<text x="12" y="{height - padding}" font-size="12" font-family="Arial">${minimum:,.0f}</text>',
    ]

    for model_name, series in wealth_by_model.items():
        values = np.array([value for _, value in series], dtype=float)
        points = _polyline_points(values, width, height, padding)
        color = colors[model_name]
        lines.append(
            f'<polyline points="{points}" fill="none" stroke="{color}" stroke-width="2.5"/>'
        )

    for index, model_name in enumerate(MODEL_NAMES):
        y_position = 58 + 22 * index
        color = colors[model_name]
        lines.append(
            f'<rect x="{width - 150}" y="{y_position - 10}" width="12" height="12" fill="{color}"/>'
        )
        lines.append(
            f'<text x="{width - 130}" y="{y_position}" font-size="13" font-family="Arial">{model_name}</text>'
        )

    lines.append("</svg>")
    (FIGURE_DIR / "wealth_evolution.svg").write_text("\n".join(lines))


def write_weights_svg(weight_rows: list[list[object]]) -> None:
    """Write an SVG area-style chart for model weights by rebalance period."""

    model_name = "BSS"
    filtered_rows = [row for row in weight_rows if row[2] == model_name]
    tickers = sorted({str(row[3]) for row in filtered_rows})
    periods = sorted({int(row[0]) for row in filtered_rows})
    weights = {
        (int(row[0]), str(row[3])): float(row[4])
        for row in filtered_rows
        if float(row[4]) > 0.0001
    }
    active_tickers = [
        ticker
        for ticker in tickers
        if any((period, ticker) in weights for period in periods)
    ]

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
    ]

    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="white"/>',
        f'<text x="{width / 2}" y="28" text-anchor="middle" font-size="20" font-family="Arial">BSS Portfolio Weights by Rebalance Period</text>',
        f'<line x1="{padding}" y1="{height - padding}" x2="{width - padding}" y2="{height - padding}" stroke="#333"/>',
        f'<line x1="{padding}" y1="{padding}" x2="{padding}" y2="{height - padding}" stroke="#333"/>',
        f'<text x="15" y="{padding}" font-size="12" font-family="Arial">100%</text>',
        f'<text x="20" y="{height - padding}" font-size="12" font-family="Arial">0%</text>',
    ]

    for period_index, period in enumerate(periods):
        x_left = padding + period_index * bar_width + 10
        y_top = height - padding
        for ticker_index, ticker in enumerate(active_tickers):
            weight = weights.get((period, ticker), 0.0)
            segment_height = weight * (height - 2 * padding)
            if segment_height <= 0:
                continue
            y_top -= segment_height
            color = palette[ticker_index % len(palette)]
            lines.append(
                f'<rect x="{x_left:.1f}" y="{y_top:.1f}" width="{bar_width - 20:.1f}" height="{segment_height:.1f}" fill="{color}"/>'
            )
        lines.append(
            f'<text x="{x_left + (bar_width - 20) / 2:.1f}" y="{height - 18}" text-anchor="middle" font-size="12" font-family="Arial">{period}</text>'
        )

    for index, ticker in enumerate(active_tickers[:10]):
        y_position = 58 + 20 * index
        color = palette[index % len(palette)]
        lines.append(
            f'<rect x="{width - 150}" y="{y_position - 10}" width="12" height="12" fill="{color}"/>'
        )
        lines.append(
            f'<text x="{width - 130}" y="{y_position}" font-size="13" font-family="Arial">{ticker}</text>'
        )

    lines.append("</svg>")
    (FIGURE_DIR / "bss_weights.svg").write_text("\n".join(lines))


def write_figures(results: dict[str, object]) -> None:
    """Write all SVG figures used by the report."""

    ensure_output_dirs()
    write_wealth_svg(results["wealth_by_model"])
    write_weights_svg(results["weight_rows"])
