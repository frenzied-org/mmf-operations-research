"""Problem 3: solve the worker-project assignment linear program.

The assignment variables form a 4 by 4 matrix.  Entry ``x[i, j]`` is 1 when
worker ``i + 1`` is assigned to project ``j + 1`` and is 0 otherwise.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.optimize import linprog


WORKER_HOURLY_COST = 20.0


@dataclass(frozen=True)
class AssignmentSolution:
    """Optimal worker-project assignment.

    Attributes
    ----------
    assignment_matrix:
        Binary matrix showing which worker is assigned to each project.
    total_cost:
        Minimum total cost in dollars.
    """

    assignment_matrix: np.ndarray
    total_cost: float


def solve_assignment() -> AssignmentSolution:
    """Solve the assignment problem as a linear program.

    Returns
    -------
    AssignmentSolution
        Optimal binary assignment matrix and total cost.
    """

    hours = np.array(
        [
            [7, 3, 6, 10],
            [5, 4, 9, 9],
            [6, 4, 7, 10],
            [5, 5, 6, 8],
        ],
        dtype=float,
    )
    costs = WORKER_HOURLY_COST * hours

    equality_rows: list[np.ndarray] = []
    equality_targets: list[float] = []

    # Each worker must be assigned exactly one project.
    for worker_index in range(4):
        row = np.zeros(16)
        row[4 * worker_index : 4 * worker_index + 4] = 1.0
        equality_rows.append(row)
        equality_targets.append(1.0)

    # Each project must be assigned exactly one worker.
    for project_index in range(4):
        row = np.zeros(16)
        row[project_index::4] = 1.0
        equality_rows.append(row)
        equality_targets.append(1.0)

    result = linprog(
        c=costs.reshape(-1),
        A_eq=np.vstack(equality_rows),
        b_eq=np.array(equality_targets),
        bounds=[(0.0, 1.0)] * 16,
        method="highs",
    )
    if not result.success:
        raise RuntimeError(f"Problem 3 linear program failed: {result.message}")

    return AssignmentSolution(
        assignment_matrix=np.rint(result.x.reshape(4, 4)),
        total_cost=float(result.fun),
    )


def main() -> None:
    """Print the optimal assignment."""

    solution = solve_assignment()
    print(solution.assignment_matrix.astype(int))
    print(f"Minimum cost: {solution.total_cost:.2f}")


if __name__ == "__main__":
    main()
