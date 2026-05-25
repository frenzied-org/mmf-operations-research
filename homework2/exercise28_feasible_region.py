"""Exercise 2.8: enumerate the basic feasible solutions of a triangle."""

from __future__ import annotations

from collections import defaultdict

import numpy as np

from basic_feasible_solutions import (
    BasicFeasibleSolution,
    enumerate_basic_feasible_solutions,
)


VARIABLE_NAMES = ("x1", "x2", "s1", "s2", "s3")
EQUALITY_MATRIX = np.array(
    [
        [1.0, 1.0, 1.0, 0.0, 0.0],
        [1.0, -1.0, 0.0, 1.0, 0.0],
        [1.0, 0.0, 0.0, 0.0, 1.0],
    ]
)
RIGHT_HAND_SIDE = np.array([6.0, 0.0, 3.0])


def get_basic_feasible_solutions() -> list[BasicFeasibleSolution]:
    """Return each feasible basis for the standard-form system.

    Returns
    -------
    list[BasicFeasibleSolution]
        Seven bases representing the three vertices of the feasible triangle.
    """

    return enumerate_basic_feasible_solutions(
        equality_matrix=EQUALITY_MATRIX,
        right_hand_side=RIGHT_HAND_SIDE,
        variable_names=VARIABLE_NAMES,
    )


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
