"""Problem 2: state the linear-program transformation.

There is no numerical solve required for this problem.  The key observation is
that the nonlinear term ``x2 ** 2`` can be replaced by a new nonnegative
variable because the same expression appears in the objective and in one
equality constraint.
"""

from __future__ import annotations


def get_standard_form() -> str:
    """Return the standard-form linear program for Problem 2.

    Returns
    -------
    str
        A plain-text statement of the transformed linear program.
    """

    return (
        "Let y = x2^2. Since x2 >= 0, y >= 0 and x2 can be recovered as "
        "sqrt(y). The standard-form LP is:\n"
        "minimize 2 x1 + y + x3\n"
        "subject to y - x3 = 0\n"
        "           5 x1 + 3 x3 + s = 5\n"
        "           x1, y, x3, s >= 0"
    )


def main() -> None:
    """Print the transformed linear program."""

    print(get_standard_form())


if __name__ == "__main__":
    main()
