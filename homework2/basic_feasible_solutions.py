"""Enumerate basic feasible solutions of small standard-form linear programs.

A standard-form linear program has equality constraints ``A @ x = b`` and
nonnegative decision variables ``x``.  For ``m`` independent constraints, a
basis selects ``m`` columns of ``A``.  The remaining variables are set to zero
and the selected square system is solved.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations

import numpy as np


NUMERICAL_TOLERANCE = 1.0e-9


@dataclass(frozen=True)
class BasicFeasibleSolution:
    """A feasible solution produced from one nonsingular basis.

    Attributes
    ----------
    basis:
        Names of the variables chosen as basic variables.
    values:
        Full variable vector, including slack or surplus variables.
    objective_value:
        Objective value when objective coefficients were supplied; otherwise
        ``None``.
    """

    basis: tuple[str, ...]
    values: np.ndarray
    objective_value: float | None


def enumerate_basic_feasible_solutions(
    equality_matrix: np.ndarray,
    right_hand_side: np.ndarray,
    variable_names: tuple[str, ...],
    objective_coefficients: np.ndarray | None = None,
) -> list[BasicFeasibleSolution]:
    """Generate every feasible solution associated with a nonsingular basis.

    Parameters
    ----------
    equality_matrix:
        Matrix ``A`` in ``A @ x = b`` with one column per variable.
    right_hand_side:
        Vector ``b`` in the equality constraints.
    variable_names:
        Variable names in the same order as columns of ``equality_matrix``.
    objective_coefficients:
        Optional vector ``c`` in the minimization objective ``c @ x``.

    Returns
    -------
    list[BasicFeasibleSolution]
        Feasible basic solutions.  Degenerate solutions are retained once for
        each basis that represents them, which is needed in Exercise 2.8.
    """

    row_count, column_count = equality_matrix.shape
    if len(variable_names) != column_count:
        raise ValueError("Variable names must match the equality-matrix columns.")
    if right_hand_side.shape != (row_count,):
        raise ValueError("The right-hand-side vector must have one value per row.")
    if objective_coefficients is not None:
        if objective_coefficients.shape != (column_count,):
            raise ValueError("Objective coefficients must have one value per variable.")

    feasible_solutions: list[BasicFeasibleSolution] = []
    for basis_indices in combinations(range(column_count), row_count):
        basis_matrix = equality_matrix[:, basis_indices]
        if np.linalg.matrix_rank(basis_matrix) < row_count:
            continue

        basic_values = np.linalg.solve(basis_matrix, right_hand_side)
        if np.any(basic_values < -NUMERICAL_TOLERANCE):
            continue

        values = np.zeros(column_count)
        values[list(basis_indices)] = basic_values
        values[np.abs(values) < NUMERICAL_TOLERANCE] = 0.0

        objective_value = None
        if objective_coefficients is not None:
            objective_value = float(objective_coefficients @ values)

        basis_names = tuple(variable_names[index] for index in basis_indices)
        feasible_solutions.append(
            BasicFeasibleSolution(
                basis=basis_names,
                values=values,
                objective_value=objective_value,
            )
        )

    return feasible_solutions
