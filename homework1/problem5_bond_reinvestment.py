"""Problem 5: solve the bond portfolio with reinvested surplus cash.

The variables are bond purchases and surplus cash balances.  Surplus cash from
one year earns 2% and can be used to pay the next year's liability.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.optimize import linprog


REINVESTMENT_RATE = 0.02


@dataclass(frozen=True)
class BondReinvestmentSolution:
    """Optimal bond portfolio with reinvestment.

    Attributes
    ----------
    bond_units:
        Units purchased of bonds 1, 2, and 3.
    surplus_cash:
        Excess cash after years 1 and 2, reinvested for one year.
    total_cost:
        Minimum portfolio purchase cost today.
    """

    bond_units: np.ndarray
    surplus_cash: np.ndarray
    total_cost: float


def solve_bond_reinvestment() -> BondReinvestmentSolution:
    """Solve the modified bond portfolio linear program.

    Returns
    -------
    BondReinvestmentSolution
        Optimal bond units, surplus balances, and total cost.
    """

    # Variable order is x1, x2, x3, y1, y2.  The x variables are bond units.
    # The y variables are reinvested surplus balances after years 1 and 2.
    objective_coefficients = np.array([102.0, 99.0, 98.0, 0.0, 0.0])
    equality_matrix = np.array(
        [
            [105.0, 3.5, 3.5, -1.0, 0.0],
            [0.0, 103.5, 3.5, 1.0 + REINVESTMENT_RATE, -1.0],
            [0.0, 0.0, 103.5, 0.0, 1.0 + REINVESTMENT_RATE],
        ]
    )
    liabilities = np.array([12_000.0, 18_000.0, 20_000.0])

    result = linprog(
        c=objective_coefficients,
        A_eq=equality_matrix,
        b_eq=liabilities,
        bounds=[(0.0, None)] * 5,
        method="highs",
    )
    if not result.success:
        raise RuntimeError(f"Problem 5 linear program failed: {result.message}")

    return BondReinvestmentSolution(
        bond_units=result.x[:3],
        surplus_cash=result.x[3:],
        total_cost=float(result.fun),
    )


def main() -> None:
    """Print the optimal bond portfolio."""

    solution = solve_bond_reinvestment()
    for bond_number, units in enumerate(solution.bond_units, start=1):
        print(f"Bond {bond_number}: buy {units:.6f} units")
    print(f"Surplus cash after years 1 and 2: {solution.surplus_cash}")
    print(f"Minimum cost: {solution.total_cost:.2f}")


if __name__ == "__main__":
    main()
