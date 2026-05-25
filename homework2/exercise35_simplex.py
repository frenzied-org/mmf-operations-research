"""Exercise 3.5: solve the problem using the Python simplex counterpart."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from simplex_method import SimplexResult, simplex_method


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
    """Run the Python analogue of ``SimplexMethod`` for Exercise 3.5.

    Returns
    -------
    Exercise35Solution
        Optimal simplex output and the opposite endpoint of the optimal
        segment ``{(x1, 3) : 0 <= x1 <= 6}``.
    """

    result = simplex_method(
        objective_coefficients=OBJECTIVE_COEFFICIENTS,
        equality_matrix=EQUALITY_MATRIX,
        right_hand_side=RIGHT_HAND_SIDE,
        initial_basis=INITIAL_BASIS,
        variable_names=VARIABLE_NAMES,
    )
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
