"""Exercise 3.4: apply simplex and certify that the problem is unbounded.

This script contains its standard-form problem data and the minimum-form
simplex calculation needed to record reduced costs, pivots, and the improving
unbounded ray.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


NUMERICAL_TOLERANCE = 1.0e-9
DEFAULT_MAXIMUM_ITERATIONS = 100


@dataclass(frozen=True)
class SimplexIteration:
    """One basis evaluation and any pivot chosen from it.

    Attributes
    ----------
    iteration_number:
        Zero-based count of basis evaluations.
    basis:
        Zero-based column indices of the current basic variables.
    solution:
        Full current basic feasible solution.
    objective_value:
        Value of the minimization objective at ``solution``.
    reduced_costs:
        Reduced cost for every variable.  A negative nonbasic reduced cost
        indicates an improving entering variable in a minimization problem.
    entering_variable:
        Column index selected to enter, or ``None`` at an optimal basis.
    direction:
        Full solution-space direction for increasing the entering variable.
    step_length:
        Maximum nonnegative feasible move, or ``None`` if no pivot is needed
        or the improving direction is unbounded.
    leaving_variable:
        Column index leaving the basis, or ``None`` without a finite pivot.
    """

    iteration_number: int
    basis: tuple[int, ...]
    solution: np.ndarray
    objective_value: float
    reduced_costs: np.ndarray
    entering_variable: int | None
    direction: np.ndarray | None
    step_length: float | None
    leaving_variable: int | None


@dataclass(frozen=True)
class SimplexResult:
    """Output of the standard-form minimum simplex solver.

    Attributes
    ----------
    status:
        Either ``"optimal"`` or ``"unbounded"``.
    solution:
        Final basic feasible point reached before termination.
    objective_value:
        Objective value at ``solution``.  For an unbounded problem this is
        not a finite optimum; it is the last evaluated feasible value.
    basis:
        Final basic variable column indices.
    iterations:
        Complete iteration history.
    unbounded_ray:
        Nonnegative direction preserving the equalities and improving the
        objective, or ``None`` for an optimal result.
    equality_matrix:
        Original equality-constraint matrix, retained for verification.
    right_hand_side:
        Original equality right-hand-side vector.
    objective_coefficients:
        Original objective vector.
    variable_names:
        Variable names in vector order.
    """

    status: str
    solution: np.ndarray
    objective_value: float
    basis: tuple[int, ...]
    iterations: tuple[SimplexIteration, ...]
    unbounded_ray: np.ndarray | None
    equality_matrix: np.ndarray
    right_hand_side: np.ndarray
    objective_coefficients: np.ndarray
    variable_names: tuple[str, ...]


def simplex_method(
    objective_coefficients: np.ndarray,
    equality_matrix: np.ndarray,
    right_hand_side: np.ndarray,
    initial_basis: tuple[int, ...],
    variable_names: tuple[str, ...],
    maximum_iterations: int = DEFAULT_MAXIMUM_ITERATIONS,
) -> SimplexResult:
    """Solve a minimization linear program from a feasible initial basis.

    Parameters
    ----------
    objective_coefficients:
        Vector ``c`` in the objective ``c @ x``.
    equality_matrix:
        Matrix ``A`` in the equality constraints ``A @ x = b``.
    right_hand_side:
        Vector ``b`` in the equality constraints.
    initial_basis:
        Zero-based column indices of a feasible starting basis.
    variable_names:
        Names of the variables in column order.
    maximum_iterations:
        Maximum number of basis evaluations before reporting a likely cycling
        or modelling error.

    Returns
    -------
    SimplexResult
        Optimal solution or an unboundedness certificate with iteration log.

    Raises
    ------
    ValueError
        If dimensions do not agree or the initial basis is not feasible.
    RuntimeError
        If the iteration cap is reached.
    """

    row_count, column_count = equality_matrix.shape
    if objective_coefficients.shape != (column_count,):
        raise ValueError("Objective coefficients must match the number of variables.")
    if right_hand_side.shape != (row_count,):
        raise ValueError("The right-hand side must match the number of constraints.")
    if len(variable_names) != column_count:
        raise ValueError("Variable names must match the number of variables.")
    if len(initial_basis) != row_count:
        raise ValueError("A basis must contain one variable per equality constraint.")

    basis = list(initial_basis)
    history: list[SimplexIteration] = []

    for iteration_number in range(maximum_iterations):
        basis_matrix = equality_matrix[:, basis]
        basic_values = np.linalg.solve(basis_matrix, right_hand_side)
        if iteration_number == 0 and np.any(basic_values < -NUMERICAL_TOLERANCE):
            raise ValueError("The supplied initial basis is not feasible.")

        solution = np.zeros(column_count)
        solution[basis] = basic_values
        solution[np.abs(solution) < NUMERICAL_TOLERANCE] = 0.0

        # For a minimization problem, r_j = c_j - c_B^T B^(-1) A_j.
        basis_costs = objective_coefficients[basis]
        dual_prices = np.linalg.solve(basis_matrix.T, basis_costs)
        reduced_costs = objective_coefficients - equality_matrix.T @ dual_prices
        reduced_costs[np.abs(reduced_costs) < NUMERICAL_TOLERANCE] = 0.0
        objective_value = float(objective_coefficients @ solution)

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
                    reduced_costs=reduced_costs,
                    entering_variable=None,
                    direction=None,
                    step_length=None,
                    leaving_variable=None,
                )
            )
            return SimplexResult(
                status="optimal",
                solution=solution,
                objective_value=objective_value,
                basis=tuple(basis),
                iterations=tuple(history),
                unbounded_ray=None,
                equality_matrix=equality_matrix,
                right_hand_side=right_hand_side,
                objective_coefficients=objective_coefficients,
                variable_names=variable_names,
            )

        entering_variable = min(
            improving_indices,
            key=lambda index: reduced_costs[index],
        )
        basic_direction = -np.linalg.solve(
            basis_matrix,
            equality_matrix[:, entering_variable],
        )
        direction = np.zeros(column_count)
        direction[basis] = basic_direction
        direction[entering_variable] = 1.0
        direction[np.abs(direction) < NUMERICAL_TOLERANCE] = 0.0

        eligible_rows = [
            row_index
            for row_index, change in enumerate(basic_direction)
            if change < -NUMERICAL_TOLERANCE
        ]
        if not eligible_rows:
            history.append(
                SimplexIteration(
                    iteration_number=iteration_number,
                    basis=tuple(basis),
                    solution=solution,
                    objective_value=objective_value,
                    reduced_costs=reduced_costs,
                    entering_variable=entering_variable,
                    direction=direction,
                    step_length=None,
                    leaving_variable=None,
                )
            )
            return SimplexResult(
                status="unbounded",
                solution=solution,
                objective_value=objective_value,
                basis=tuple(basis),
                iterations=tuple(history),
                unbounded_ray=direction,
                equality_matrix=equality_matrix,
                right_hand_side=right_hand_side,
                objective_coefficients=objective_coefficients,
                variable_names=variable_names,
            )

        step_length, leaving_row = min(
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
                reduced_costs=reduced_costs,
                entering_variable=entering_variable,
                direction=direction,
                step_length=float(step_length),
                leaving_variable=leaving_variable,
            )
        )
        basis[leaving_row] = entering_variable

    raise RuntimeError("Simplex iteration limit reached before termination.")


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
