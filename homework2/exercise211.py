"""Exercise 2.11: express the strict-feasible-set non-attainment proof.

For a feasible point ``x`` in ``P = {x | A @ x < b}``, move a small positive
distance in the objective direction ``c``.  Strict inequalities provide room
for a sufficiently small move, while the objective increases by
``step_size * (c @ c)`` whenever ``c`` is nonzero.
"""

from __future__ import annotations

import numpy as np


def objective_improvement(direction: np.ndarray, step_size: float) -> float:
    """Return the objective gain from moving in objective direction ``c``.

    Parameters
    ----------
    direction:
        Nonzero objective coefficient vector ``c``.
    step_size:
        Positive scalar ``epsilon`` in the feasible move
        ``y = x + epsilon*c``.

    Returns
    -------
    float
        The strictly positive gain ``epsilon * (c @ c)``.

    Raises
    ------
    ValueError
        If ``direction`` is zero or ``step_size`` is not positive.
    """

    if step_size <= 0.0:
        raise ValueError("The step size must be positive.")
    if np.allclose(direction, 0.0):
        raise ValueError("The objective direction must be nonzero.")

    return float(step_size * (direction @ direction))


def get_proof_summary() -> str:
    """Return the constructive proof argument in plain text.

    Returns
    -------
    str
        Short explanation of why no optimal solution can be attained.
    """

    return (
        "For any x with A @ x < b, choose epsilon > 0 small enough that "
        "y = x + epsilon*c still satisfies A @ y < b. Since c is nonzero, "
        "c @ y - c @ x = epsilon*(c @ c) > 0. Every feasible point can be "
        "strictly improved, so no optimum is attained."
    )


def main() -> None:
    """Print the proof summary and one numerical illustration."""

    example_direction = np.array([3.0, -4.0])
    example_step_size = 0.25
    gain = objective_improvement(example_direction, example_step_size)
    print(get_proof_summary())
    print(f"Example objective gain with c=(3, -4) and epsilon=0.25: {gain:.2f}")


if __name__ == "__main__":
    main()
