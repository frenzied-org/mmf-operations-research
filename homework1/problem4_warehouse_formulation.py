"""Problem 4: formulate the warehouse trading linear program.

This problem gives symbolic monthly prices instead of numerical data, so the
deliverable is the model formulation rather than a numerical solve.
"""

from __future__ import annotations


def get_warehouse_formulation() -> str:
    """Return the warehouse-trading linear program in plain text.

    Returns
    -------
    str
        A compact statement of the objective, balance constraints, capacity
        constraints, and nonnegativity constraints.
    """

    return (
        "Decision variables for months t = 1,...,12:\n"
        "  b_t = units bought at the start of month t\n"
        "  q_t = units sold at the start of month t\n"
        "  I_t = inventory after month-t buy/sell decisions\n"
        "Maximize sum_t s_t q_t - sum_t p_t b_t - sum_t i_t I_{t-1}\n"
        "subject to I_t = I_{t-1} + b_t - q_t for t = 1,...,12\n"
        "           I_0 = 2000, I_12 = 0\n"
        "           0 <= I_t <= 10000 for t = 0,...,12\n"
        "           b_t >= 0 and q_t >= 0 for t = 1,...,12"
    )


def main() -> None:
    """Print the symbolic warehouse-trading formulation."""

    print(get_warehouse_formulation())


if __name__ == "__main__":
    main()
