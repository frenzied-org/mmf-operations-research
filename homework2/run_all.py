"""Run all Python computations used in the Homework 2 written solution."""

from __future__ import annotations

import numpy as np

from exercise28_feasible_region import get_bases_by_vertex
from exercise29_basic_solutions import solve_exercise_23a, solve_exercise_23b
from exercise34_unbounded import solve_exercise_34
from exercise35_simplex import solve_exercise_35
from simplex_method import SimplexResult


def _print_simplex_history(label: str, result: SimplexResult) -> None:
    """Print basis, objective, and pivot decisions for a simplex result.

    Parameters
    ----------
    label:
        Exercise label printed before the iterations.
    result:
        Result returned by the Python simplex counterpart.
    """

    print(label)
    for iteration in result.iterations:
        basis_names = tuple(result.variable_names[index] for index in iteration.basis)
        entering_name = None
        if iteration.entering_variable is not None:
            entering_name = result.variable_names[iteration.entering_variable]
        leaving_name = None
        if iteration.leaving_variable is not None:
            leaving_name = result.variable_names[iteration.leaving_variable]
        point = np.array2string(iteration.solution, precision=6)
        print(
            f"  iteration={iteration.iteration_number}, basis={basis_names}, "
            f"x={point}, objective={iteration.objective_value:.6f}, "
            f"enter={entering_name}, leave={leaving_name}"
        )
    print(f"  status={result.status}")
    if result.unbounded_ray is not None:
        print(f"  improving ray={result.unbounded_ray}")


def main() -> None:
    """Print a compact numerical record for all computational exercises."""

    print("Exercise 2.8")
    for vertex, bases in get_bases_by_vertex().items():
        print(f"  vertex={vertex}: bases={bases}")

    for label, result in (
        ("Exercise 2.9(a)", solve_exercise_23a()),
        ("Exercise 2.9(b)", solve_exercise_23b()),
    ):
        print(f"\n{label}")
        for solution in result.solutions:
            point = np.array2string(solution.values[:2], precision=6)
            print(
                f"  basis={solution.basis}, original variables={point}, "
                f"objective={solution.objective_value:.6f}"
            )

    exercise34_result = solve_exercise_34()
    print()
    _print_simplex_history("Exercise 3.4", exercise34_result)

    exercise35_solution = solve_exercise_35()
    print()
    _print_simplex_history("Exercise 3.5", exercise35_solution.simplex_result)
    print("  optimal set=(x1, x2) = (t, 3), 0 <= t <= 6")


if __name__ == "__main__":
    main()
