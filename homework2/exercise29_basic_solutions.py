"""Exercise 2.9: solve two linear programs by enumerating their bases."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from basic_feasible_solutions import (
    BasicFeasibleSolution,
    enumerate_basic_feasible_solutions,
)


@dataclass(frozen=True)
class EnumerationResult:
    """Feasible bases and the best basic feasible solution for one problem.

    Attributes
    ----------
    variable_names:
        Names matching the value vector in every solution.
    solutions:
        All feasible bases, including distinct bases at a degenerate point.
    optimal_solution:
        Basic feasible solution with the smallest objective value.
    """

    variable_names: tuple[str, ...]
    solutions: list[BasicFeasibleSolution]
    optimal_solution: BasicFeasibleSolution


def _solve_by_enumeration(
    equality_matrix: np.ndarray,
    right_hand_side: np.ndarray,
    variable_names: tuple[str, ...],
    objective_coefficients: np.ndarray,
) -> EnumerationResult:
    """Enumerate feasible bases and select the minimum objective value."""

    solutions = enumerate_basic_feasible_solutions(
        equality_matrix=equality_matrix,
        right_hand_side=right_hand_side,
        variable_names=variable_names,
        objective_coefficients=objective_coefficients,
    )
    optimal_solution = min(
        solutions,
        key=lambda solution: float(solution.objective_value),
    )
    return EnumerationResult(
        variable_names=variable_names,
        solutions=solutions,
        optimal_solution=optimal_solution,
    )


def solve_exercise_23a() -> EnumerationResult:
    """Solve Exercise 2.3(a), used as Exercise 2.9(a).

    Returns
    -------
    EnumerationResult
        Five feasible bases and the unique minimizer ``(2, 5)``.
    """

    variable_names = ("x1", "x2", "s1", "s2", "s3")
    equality_matrix = np.array(
        [
            [-2.0, 1.0, 1.0, 0.0, 0.0],
            [-1.0, 1.0, 0.0, 1.0, 0.0],
            [1.0, 0.0, 0.0, 0.0, 1.0],
        ]
    )
    right_hand_side = np.array([2.0, 3.0, 2.0])
    objective_coefficients = np.array([-1.0, -2.0, 0.0, 0.0, 0.0])
    return _solve_by_enumeration(
        equality_matrix,
        right_hand_side,
        variable_names,
        objective_coefficients,
    )


def solve_exercise_23b() -> EnumerationResult:
    """Solve Exercise 2.3(b), used as Exercise 2.9(b).

    Returns
    -------
    EnumerationResult
        Three feasible bases and the unique minimizer ``(10/3, 2/3)``.
    """

    variable_names = ("x1", "x2", "s1", "s2")
    equality_matrix = np.array(
        [
            [1.0, -2.0, -1.0, 0.0],
            [1.0, 1.0, 0.0, 1.0],
        ]
    )
    right_hand_side = np.array([2.0, 4.0])
    objective_coefficients = np.array([-1.0, -2.0, 0.0, 0.0])
    return _solve_by_enumeration(
        equality_matrix,
        right_hand_side,
        variable_names,
        objective_coefficients,
    )


def main() -> None:
    """Print every feasible basis and its objective for both programs."""

    for label, result in (
        ("2.9(a)", solve_exercise_23a()),
        ("2.9(b)", solve_exercise_23b()),
    ):
        print(label)
        for solution in result.solutions:
            values = np.array2string(solution.values, precision=6)
            print(
                f"  basis={solution.basis}, x={values}, objective={solution.objective_value:.6f}"
            )
        print(f"  optimum={result.optimal_solution.values[:2]}\n")


if __name__ == "__main__":
    main()
