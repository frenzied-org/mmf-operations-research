"""Problem 1: choose stock sales to raise cash while preserving future value.

The model is a bounded linear program.  The decision variable ``sold_shares[i]``
is the number of shares sold of stock ``i + 1``.  Because fractional shares are
allowed, each variable can take any value between 0 and 100.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.optimize import linprog


CAPITAL_GAINS_TAX_RATE = 0.30
TRANSACTION_COST_RATE = 0.01
REQUIRED_NET_CASH = 30_000.0


@dataclass(frozen=True)
class StockSaleSolution:
    """Optimal stock-sale result.

    Attributes
    ----------
    sold_shares:
        Number of shares sold for stocks 1 through 10.
    remaining_shares:
        Number of shares still held for stocks 1 through 10.
    net_cash_per_share:
        Net cash kept per sold share after taxes and transaction costs.
    net_cash:
        Total net cash raised today.
    expected_remaining_value:
        Expected before-tax value of the remaining shares in one year.
    """

    sold_shares: np.ndarray
    remaining_shares: np.ndarray
    net_cash_per_share: np.ndarray
    net_cash: float
    expected_remaining_value: float


def solve_stock_sales() -> StockSaleSolution:
    """Solve the stock-sale linear program.

    Returns
    -------
    StockSaleSolution
        Optimal share sales, remaining positions, and expected remaining value.
    """

    owned_shares = np.full(10, 100.0)
    purchase_price = np.array([20, 25, 30, 35, 40, 45, 50, 55, 60, 65], dtype=float)
    current_price = np.array([30, 34, 43, 47, 49, 53, 60, 62, 64, 66], dtype=float)
    expected_price = np.array([36, 39, 42, 45, 51, 55, 63, 64, 66, 70], dtype=float)

    # Net sale proceeds equal current price minus tax on the capital gain
    # minus the transaction cost paid on current sale value.
    capital_gain_per_share = current_price - purchase_price
    tax_per_share = CAPITAL_GAINS_TAX_RATE * capital_gain_per_share
    transaction_cost_per_share = TRANSACTION_COST_RATE * current_price
    net_cash_per_share = current_price - tax_per_share - transaction_cost_per_share

    # Minimizing future value sold is equivalent to maximizing future value
    # retained, because the original portfolio is fixed before selling.
    result = linprog(
        c=expected_price,
        A_eq=np.array([net_cash_per_share]),
        b_eq=np.array([REQUIRED_NET_CASH]),
        bounds=[(0.0, shares) for shares in owned_shares],
        method="highs",
    )
    if not result.success:
        raise RuntimeError(f"Problem 1 linear program failed: {result.message}")

    sold_shares = np.where(np.abs(result.x) < 1e-9, 0.0, result.x)
    remaining_shares = owned_shares - sold_shares

    return StockSaleSolution(
        sold_shares=sold_shares,
        remaining_shares=remaining_shares,
        net_cash_per_share=net_cash_per_share,
        net_cash=float(net_cash_per_share @ sold_shares),
        expected_remaining_value=float(expected_price @ remaining_shares),
    )


def main() -> None:
    """Print the optimal stock-sale policy."""

    solution = solve_stock_sales()
    for stock_number, sold in enumerate(solution.sold_shares, start=1):
        print(f"Stock {stock_number}: sell {sold:.6f} shares")
    print(f"Net cash raised: {solution.net_cash:.2f}")
    print(f"Expected one-year remaining value: {solution.expected_remaining_value:.2f}")


if __name__ == "__main__":
    main()
