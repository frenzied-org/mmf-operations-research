"""Problem 6: maximize daily flights from Calgary to Quebec City.

The compact model uses one variable for each complete route from Calgary to
Quebec City through Winnipeg and then through Montreal, Hamilton, or Toronto.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.optimize import linprog


@dataclass(frozen=True)
class FlightSolution:
    """Maximum-flow flight schedule.

    Attributes
    ----------
    path_flights:
        Daily flights on paths through Montreal, Hamilton, and Toronto.
    total_flights:
        Maximum daily Calgary-to-Quebec-City flights.
    """

    path_flights: np.ndarray
    total_flights: float


def solve_flight_network() -> FlightSolution:
    """Solve the maximum-flow linear program.

    Returns
    -------
    FlightSolution
        Optimal path flights and total daily flights.
    """

    # Variable order is flights via Montreal, via Hamilton, and via Toronto.
    objective_coefficients = np.array([-1.0, -1.0, -1.0])
    capacity_matrix = np.array(
        [
            [1.0, 1.0, 1.0],
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [0.0, 0.0, 1.0],
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [0.0, 0.0, 1.0],
        ]
    )
    capacity_limits = np.array([5.0, 4.0, 5.0, 2.0, 2.0, 1.0, 3.0])

    result = linprog(
        c=objective_coefficients,
        A_ub=capacity_matrix,
        b_ub=capacity_limits,
        bounds=[(0.0, None)] * 3,
        method="highs",
    )
    if not result.success:
        raise RuntimeError(f"Problem 6 linear program failed: {result.message}")

    return FlightSolution(
        path_flights=result.x,
        total_flights=float(-result.fun),
    )


def main() -> None:
    """Print the maximum-flow flight schedule."""

    solution = solve_flight_network()
    path_names = ["via Montreal", "via Hamilton", "via Toronto"]
    for path_name, flights in zip(path_names, solution.path_flights, strict=True):
        print(f"{path_name}: {flights:.6f}")
    print(f"Maximum daily flights: {solution.total_flights:.2f}")


if __name__ == "__main__":
    main()
