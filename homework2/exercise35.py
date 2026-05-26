"""Exercise 3.5: solve the problem using the Python simplex counterpart."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


VARIABLE_NAMES = ("x1", "x2", "s1", "s2", "s3")
OBJECTIVE_COEFFICIENTS = np.array([0.0, -1.0, 0.0, 0.0, 0.0])
EQUALITY_MATRIX = np.array(
    [
        [1.0, -2.0, 1.0, 0.0, 0.0],
        [1.0, -1.0, 0.0, 1.0, 0.0],
        [0.0, 1.0, 0.0, 0.0, 1.0],
    ]
)
RIGHT_HAND_SIDE = np.array([2.0, 3.0, 3.0])
INITIAL_BASIS = (2, 3, 4)
NUMERICAL_TOLERANCE = 1.0e-9


@dataclass(frozen=True)
class SimplexIteration:
    """One basis evaluation and the pivot selected from it, when needed.

    Attributes
    ----------
    iteration_number:
        Zero-based count of basis evaluations.
    basis:
        Zero-based indices of the current basic variables.
    solution:
        Full variable vector at the current basic feasible point.
    objective_value:
        Value of ``-x2`` at the current point.
    entering_variable:
        Entering-variable index, or ``None`` at the optimum.
    leaving_variable:
        Leaving-variable index, or ``None`` at the optimum.
    """

    iteration_number: int
    basis: tuple[int, ...]
    solution: np.ndarray
    objective_value: float
    entering_variable: int | None
    leaving_variable: int | None


@dataclass(frozen=True)
class SimplexResult:
    """Optimal standard-form solution and its simplex iteration record.

    Attributes
    ----------
    status:
        Termination status, ``"optimal"`` for this exercise.
    solution:
        Optimal variable vector ordered as ``(x1, x2, s1, s2, s3)``.
    objective_value:
        Minimum objective value.
    iterations:
        Simplex basis evaluations from the initial slack basis to termination.
    variable_names:
        Names matching vector positions and basis indices.
    """

    status: str
    solution: np.ndarray
    objective_value: float
    iterations: tuple[SimplexIteration, ...]
    variable_names: tuple[str, ...]


def _simplex_method() -> SimplexResult:
    """Solve this standard-form minimization from its slack-variable basis."""

    basis = list(INITIAL_BASIS)
    history: list[SimplexIteration] = []
    column_count = EQUALITY_MATRIX.shape[1]

    iteration_number = 0
    while True:
        basis_matrix = EQUALITY_MATRIX[:, basis]
        basic_values = np.linalg.solve(basis_matrix, RIGHT_HAND_SIDE)

        solution = np.zeros(column_count)
        solution[basis] = basic_values
        solution[np.abs(solution) < NUMERICAL_TOLERANCE] = 0.0

        basis_costs = OBJECTIVE_COEFFICIENTS[basis]
        dual_prices = np.linalg.solve(basis_matrix.T, basis_costs)
        reduced_costs = OBJECTIVE_COEFFICIENTS - EQUALITY_MATRIX.T @ dual_prices
        objective_value = float(OBJECTIVE_COEFFICIENTS @ solution)
        nonbasic_indices = [
            index for index in range(column_count) if index not in basis
        ]
        improving_indices = [
            index
            for index in nonbasic_indices
            if reduced_costs[index] < -NUMERICAL_TOLERANCE
        ]
        if not improving_indices:
            history.append(
                SimplexIteration(
                    iteration_number=iteration_number,
                    basis=tuple(basis),
                    solution=solution,
                    objective_value=objective_value,
                    entering_variable=None,
                    leaving_variable=None,
                )
            )
            return SimplexResult(
                status="optimal",
                solution=solution,
                objective_value=objective_value,
                iterations=tuple(history),
                variable_names=VARIABLE_NAMES,
            )

        entering_variable = min(
            improving_indices, key=lambda index: reduced_costs[index]
        )
        basic_direction = -np.linalg.solve(
            basis_matrix,
            EQUALITY_MATRIX[:, entering_variable],
        )
        eligible_rows = [
            row_index
            for row_index, direction_value in enumerate(basic_direction)
            if direction_value < -NUMERICAL_TOLERANCE
        ]
        _, leaving_row = min(
            (
                basic_values[row_index] / -basic_direction[row_index],
                row_index,
            )
            for row_index in eligible_rows
        )
        leaving_variable = basis[leaving_row]
        history.append(
            SimplexIteration(
                iteration_number=iteration_number,
                basis=tuple(basis),
                solution=solution,
                objective_value=objective_value,
                entering_variable=entering_variable,
                leaving_variable=leaving_variable,
            )
        )
        basis[leaving_row] = entering_variable
        iteration_number += 1


@dataclass(frozen=True)
class Exercise35Solution:
    """Simplex output and a second point proving non-unique optimality.

    Attributes
    ----------
    simplex_result:
        Optimal basic feasible solution and its iteration history.
    second_optimal_point:
        A second optimal point in the original ``(x1, x2)`` coordinates.
    """

    simplex_result: SimplexResult
    second_optimal_point: np.ndarray


def solve_exercise_35() -> Exercise35Solution:
    """Run the standard-form Python simplex calculation for Exercise 3.5.

    Returns
    -------
    Exercise35Solution
        Optimal simplex output and the opposite endpoint of the optimal
        segment ``{(x1, 3) : 0 <= x1 <= 6}``.
    """

    result = _simplex_method()
    return Exercise35Solution(
        simplex_result=result,
        second_optimal_point=np.array([6.0, 3.0]),
    )


def main() -> None:
    """Print the simplex optimum and the complete optimal-set expression."""

    solution = solve_exercise_35()
    result = solution.simplex_result
    print(f"Status: {result.status}")
    print(f"One optimal basic feasible solution: {result.solution}")
    print(f"Optimal objective: {result.objective_value:.6f}")
    print("All original-variable optima: (x1, x2) = (t, 3), 0 <= t <= 6")


if __name__ == "__main__":
    main()
