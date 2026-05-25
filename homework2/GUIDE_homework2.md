# Homework 2 Folder Guide

## Part 1: Conceptual explanation

This folder contains the Homework 2 questions and a Python-only solution to
five linear-optimization exercises.  The solution separates the written
submission from reproducible calculation:

- `HW2_solution.md` gives the mathematical derivations, tables, proof, and
  interpretations suitable for submission.
- `HW2_explorer.ipynb` reproduces tables and draws the feasible regions.
- Small Python modules compute the basic feasible solutions and run the
  simplex method used in the written answer.

A **basic feasible solution** is obtained from an equality-form system
$Ax=b$, $x\geq0$ by selecting as many independent columns of $A$ as there are
rows, solving for those basic variables, setting other variables to zero, and
retaining nonnegative results.  Exercises 2.8 and 2.9 enumerate these bases
directly.

The **simplex method** iterates between basic feasible solutions.  For a
minimization problem, a negative reduced cost identifies a variable whose
increase can lower the objective.  The minimum-ratio test determines whether a
pivot limits that increase; if no basic variable restricts an improving
direction, the problem is unbounded.  Exercises 3.4 and 3.5 use this logic.

## Part 2: Code reference

| File | Purpose |
|---|---|
| `questions.md` | Assignment statements and supplied reference context. |
| `HW2_solution.md` | Complete written Python-based answer. |
| `HW2_explorer.ipynb` | Interactive reproduction of calculations and plots. |
| `basic_feasible_solutions.py` | Enumerates feasible nonsingular bases for a standard-form system. |
| `exercise28_feasible_region.py` | States Exercise 2.8 in standard form and groups bases by vertex. |
| `exercise29_basic_solutions.py` | Enumerates and selects the optimum for Exercises 2.3(a) and 2.3(b). |
| `simplex_method.py` | Python counterpart of the textbook MATLAB simplex routine, with an iteration record. |
| `exercise34_unbounded.py` | Applies simplex to Exercise 3.4 and returns its improving unbounded ray. |
| `exercise35_simplex.py` | Applies simplex to Exercise 3.5 and records the alternate-optimum segment. |
| `test_homework2.py` | Verifies the vertices, optima, ray certificate, and optimal line segment. |
| `run_all.py` | Prints a compact calculation record for all computed answers. |

Start with `HW2_solution.md`, then open `HW2_explorer.ipynb` for plots or run
`uv run python homework2/run_all.py` from the project root for numerical
output.  The plotting notebook additionally needs Matplotlib.  It can be
executed without changing project dependencies by running this command from
the `homework2` folder:

```bash
uv run --with matplotlib --with nbconvert jupyter nbconvert \
    --to notebook --execute --inplace HW2_explorer.ipynb
```

## Part 3: Short journal

- 2026-05-25: MATLAB-specific instructions were fulfilled with a Python
  standard-form simplex counterpart, as required for this submission.
- 2026-05-25: Enumeration shows that both $(0,0)$ and $(3,3)$ in Exercise 2.8
  are degenerate vertices with multiple feasible bases.
