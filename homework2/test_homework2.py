"""Tests for the numerical claims used in the Homework 2 solution."""

from __future__ import annotations

import unittest

import numpy as np

from exercise28 import get_basic_feasible_solutions as exercise28_solutions
from exercise29 import solve_exercise_23a, solve_exercise_23b
from exercise211 import objective_improvement
from exercise34 import solve_exercise_34
from exercise35 import solve_exercise_35


class BasicFeasibleSolutionTests(unittest.TestCase):
    """Check the basic feasible solution enumerations in Chapter 2."""

    def test_exercise_28_has_degenerate_vertices_with_multiple_bases(self) -> None:
        """The triangle has seven feasible bases but only three vertices."""

        solutions = exercise28_solutions()
        projected_points = {
            tuple(np.round(solution.values[:2], decimals=8)) for solution in solutions
        }

        self.assertEqual(len(solutions), 7)
        self.assertEqual(projected_points, {(0.0, 0.0), (0.0, 6.0), (3.0, 3.0)})

    def test_exercise_29_unique_optima_match_vertex_evaluation(self) -> None:
        """Each supplied linear program has one best basic feasible solution."""

        part_a = solve_exercise_23a()
        part_b = solve_exercise_23b()

        self.assertEqual(len(part_a.solutions), 5)
        np.testing.assert_allclose(part_a.optimal_solution.values[:2], [2.0, 5.0])
        self.assertAlmostEqual(part_a.optimal_solution.objective_value, -12.0)
        self.assertEqual(len(part_b.solutions), 3)
        np.testing.assert_allclose(
            part_b.optimal_solution.values[:2], [10.0 / 3.0, 2.0 / 3.0]
        )
        self.assertAlmostEqual(part_b.optimal_solution.objective_value, -14.0 / 3.0)


class SimplexTests(unittest.TestCase):
    """Check the Python simplex counterparts required for Chapter 3."""

    def test_exercise_34_reports_improving_unbounded_ray(self) -> None:
        """The simplex result contains a feasible direction with falling cost."""

        result = solve_exercise_34()

        self.assertEqual(result.status, "unbounded")
        self.assertIsNotNone(result.unbounded_ray)
        ray = result.unbounded_ray
        assert ray is not None
        self.assertLess(float(result.objective_coefficients @ ray), 0.0)
        np.testing.assert_allclose(
            result.equality_matrix @ ray,
            [0.0, 0.0],
            atol=1.0e-12,
        )
        self.assertTrue(np.all(ray >= 0.0))

    def test_exercise_35_finds_optimum_and_alternative_optimum(self) -> None:
        """The optimum fixes x2 at 3 while x1 may vary from 0 to 6."""

        solution = solve_exercise_35()

        self.assertEqual(solution.simplex_result.status, "optimal")
        self.assertAlmostEqual(solution.simplex_result.objective_value, -3.0)
        np.testing.assert_allclose(solution.simplex_result.solution[:2], [0.0, 3.0])
        np.testing.assert_allclose(solution.second_optimal_point, [6.0, 3.0])
        self.assertEqual(
            [
                iteration.iteration_number
                for iteration in solution.simplex_result.iterations
            ],
            [0, 1],
        )


class StrictFeasibleSetTests(unittest.TestCase):
    """Check the constructive objective improvement used in Exercise 2.11."""

    def test_exercise_211_move_in_direction_c_strictly_improves_objective(self) -> None:
        """A positive move in a nonzero objective direction raises its value."""

        direction = np.array([3.0, -4.0])

        self.assertAlmostEqual(objective_improvement(direction, step_size=0.25), 6.25)


if __name__ == "__main__":
    unittest.main()
