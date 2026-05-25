"""Exercise 2.8: enumerate the basic feasible solutions of a triangle."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from itertools import combinations

import numpy as np


NUMERICAL_TOLERANCE = 1.0e-9
VARIABLE_NAMES = ("x1", "x2", "s1", "s2", "s3")
EQUALITY_MATRIX = np.array(
    [
        [1.0, 1.0, 1.0, 0.0, 0.0],
        [1.0, -1.0, 0.0, 1.0, 0.0],
        [1.0, 0.0, 0.0, 0.0, 1.0],
    ]
)
RIGHT_HAND_SIDE = np.array([6.0, 0.0, 3.0])


@dataclass(frozen=True)
class BasicFeasibleSolution:
    """A feasible standard-form solution associated with one basis.

    Attributes
    ----------
    basis:
        Names of the three selected basic variables.
    values:
        Values ordered as ``(x1, x2, s1, s2, s3)``.
    """

    basis: tuple[str, ...]
    values: np.ndarray


def get_basic_feasible_solutions() -> list[BasicFeasibleSolution]:
    """Return each feasible basis for the standard-form system.

    Returns
    -------
    list[BasicFeasibleSolution]
        Seven bases representing the three vertices of the feasible triangle.
    """

    row_count, column_count = EQUALITY_MATRIX.shape
    feasible_solutions: list[BasicFeasibleSolution] = []

    # A basis chooses one independent column per equality constraint.
    for basis_indices in combinations(range(column_count), row_count):
        basis_matrix = EQUALITY_MATRIX[:, basis_indices]
        if np.linalg.matrix_rank(basis_matrix) < row_count:
            continue

        basic_values = np.linalg.solve(basis_matrix, RIGHT_HAND_SIDE)
        if np.any(basic_values < -NUMERICAL_TOLERANCE):
            continue

        values = np.zeros(column_count)
        values[list(basis_indices)] = basic_values
        values[np.abs(values) < NUMERICAL_TOLERANCE] = 0.0
        basis_names = tuple(VARIABLE_NAMES[index] for index in basis_indices)
        feasible_solutions.append(BasicFeasibleSolution(basis_names, values))

    return feasible_solutions


def get_bases_by_vertex() -> dict[tuple[float, float], list[tuple[str, ...]]]:
    """Group feasible bases by their original ``(x1, x2)`` point.

    Returns
    -------
    dict[tuple[float, float], list[tuple[str, ...]]]
        Vertex coordinates mapped to the bases that generate the vertex.
    """

    bases_by_vertex: defaultdict[tuple[float, float], list[tuple[str, ...]]]
    bases_by_vertex = defaultdict(list)
    for solution in get_basic_feasible_solutions():
        point = tuple(float(value) for value in solution.values[:2])
        bases_by_vertex[point].append(solution.basis)

    return dict(bases_by_vertex)


def main() -> None:
    """Print all Exercise 2.8 feasible bases grouped by geometric vertex."""

    for point, bases in get_bases_by_vertex().items():
        print(f"Vertex {point}: {len(bases)} feasible basis/bases")
        for basis in bases:
            print(f"  {basis}")


if __name__ == "__main__":
    main()
