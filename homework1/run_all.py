"""Run all Python computations for Homework Assignment 1."""

from __future__ import annotations

from problem1_stock_sales import solve_stock_sales
from problem2_linearization import get_standard_form
from problem3_assignment import solve_assignment
from problem4_warehouse_formulation import get_warehouse_formulation
from problem5_bond_reinvestment import solve_bond_reinvestment
from problem6_flight_network import solve_flight_network


def main() -> None:
    """Print a compact summary of all homework answers."""

    stock_solution = solve_stock_sales()
    print("Problem 1")
    for stock_number, sold in enumerate(stock_solution.sold_shares, start=1):
        print(f"  Stock {stock_number}: sell {sold:.6f} shares")
    print(f"  Net cash raised: {stock_solution.net_cash:.2f}")
    print(f"  Expected one-year remaining value: {stock_solution.expected_remaining_value:.2f}")

    print("\nProblem 2")
    print(get_standard_form())

    assignment_solution = solve_assignment()
    print("\nProblem 3")
    print(assignment_solution.assignment_matrix.astype(int))
    print(f"  Minimum cost: {assignment_solution.total_cost:.2f}")

    print("\nProblem 4")
    print(get_warehouse_formulation())

    bond_solution = solve_bond_reinvestment()
    print("\nProblem 5")
    for bond_number, units in enumerate(bond_solution.bond_units, start=1):
        print(f"  Bond {bond_number}: buy {units:.6f} units")
    print(f"  Surplus cash after years 1 and 2: {bond_solution.surplus_cash}")
    print(f"  Minimum cost: {bond_solution.total_cost:.2f}")

    flight_solution = solve_flight_network()
    print("\nProblem 6")
    path_names = ["via Montreal", "via Hamilton", "via Toronto"]
    for path_name, flights in zip(path_names, flight_solution.path_flights, strict=True):
        print(f"  {path_name}: {flights:.6f}")
    print(f"  Maximum daily flights: {flight_solution.total_flights:.2f}")


if __name__ == "__main__":
    main()
