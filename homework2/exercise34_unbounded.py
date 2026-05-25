"""Exercise 3.4: expose unboundedness through simplex iterations."""

from __future__ import annotations

import numpy as np

from simplex_method import SimplexResult, simplex_method


VARIABLE_NAMES = ("x1", "x2", "s1", "s2")
OBJECTIVE_COEFFICIENTS = np.array([-2.0, -5.0, 0.0, 0.0])
EQUALITY_MATRIX = np.array(
    [
        [-1.0, 3.0, 1.0, 0.0],
        [-3.0, 2.0, 0.0, 1.0],
    ]
)
RIGHT_HAND_SIDE = np.array([2.0, 1.0])
INITIAL_BASIS = (2, 3)


def solve_exercise_34() -> SimplexResult:
    """Apply the minimum-form simplex method to Exercise 3.4.

    Returns
    -------
    SimplexResult
        An unbounded result whose ray is a certificate of decreasing cost.
    """

    return simplex_method(
        objective_coefficients=OBJECTIVE_COEFFICIENTS,
        equality_matrix=EQUALITY_MATRIX,
        right_hand_side=RIGHT_HAND_SIDE,
        initial_basis=INITIAL_BASIS,
        variable_names=VARIABLE_NAMES,
    )


def main() -> None:
    """Print the simplex termination and its unbounded ray."""

    result = solve_exercise_34()
    print(f"Status: {result.status}")
    print(f"Last basic feasible solution: {result.solution}")
    print(f"Last objective value: {result.objective_value:.6f}")
    print(f"Unbounded ray: {result.unbounded_ray}")


if __name__ == "__main__":
    main()
