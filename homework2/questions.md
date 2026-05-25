# Homework: Linear Optimization Exercises

## Source

Textbook: *Introduction to Linear Optimization and Extensions with MATLAB* by Roy H. Kwon.

## Assigned Exercises

Complete the following exercises:

- Exercise 2.8
- Exercise 2.9
- Exercise 2.11
- Exercise 3.4
- Exercise 3.5

---

# Background Context

This homework uses the following concepts.

A **linear program** is an optimization problem with a linear objective function and linear constraints.

A **feasible region** is the set of all points satisfying the constraints.

A **standard-form linear program** has the form

\[
\text{minimize } c^T x
\]

subject to

\[
Ax = b
\]

\[
x \ge 0.
\]

A **basic feasible solution** is a feasible solution obtained by selecting a basis, setting the nonbasic variables equal to zero, and solving for the basic variables.

An **extreme point** is a corner point of the feasible region.

The **simplex method** solves a linear program by moving from one basic feasible solution to an adjacent basic feasible solution while improving the objective value.

---

# Reference Context for Exercise 2.9

Exercise 2.9 refers to Exercise 2.2(b) and Exercise 2.3(a)–(b). Those statements are included here so the assignment is standalone.

---

## Exercise 2.2(b)

Consider a linear program in standard form:

\[
\text{minimize } c^T x
\]

subject to

\[
Ax = b
\]

\[
x \ge 0.
\]

Prove that the set of optimal solutions for the linear program in standard form,

\[
P^* = \{x \in \mathbb{R}^n \mid x \text{ is an optimal solution for the linear program}\},
\]

is a convex set.

---

## Exercise 2.3(a)

Consider the following linear program:

\[
\text{minimize } -x_1 - 2x_2
\]

subject to

\[
-2x_1 + x_2 \le 2
\]

\[
-x_1 + x_2 \le 3
\]

\[
x_1 \le 2
\]

\[
x_1 \ge 0, \qquad x_2 \ge 0.
\]

---

## Exercise 2.3(b)

Consider the following linear program:

\[
\text{minimize } -x_1 - 2x_2
\]

subject to

\[
x_1 - 2x_2 \ge 2
\]

\[
x_1 + x_2 \le 4
\]

\[
x_1 \ge 0, \qquad x_2 \ge 0.
\]

---

# Exercise 2.8

Consider the following system of constraints:

\[
x_1 + x_2 \le 6
\]

\[
x_1 - x_2 \le 0
\]

\[
x_1 \le 3
\]

\[
x_1 \ge 0, \qquad x_2 \ge 0.
\]

## Questions

### (a)

Sketch the feasible region.

### (b)

Convert the system to standard form and find all basic feasible solutions.

### (c)

Is there a one-to-one correspondence between basic feasible solutions and extreme points?

If not, identify which extreme points can be represented by multiple basic feasible solutions.

---

# Exercise 2.9

## Questions

### (a)

Solve the linear program in Exercise 2.3(a) by generating all basic feasible solutions.

### (b)

Solve the linear program in Exercise 2.3(b) by generating all basic feasible solutions.

Also illustrate Exercise 2.2(b), that is, show that the set of optimal solutions is convex.

---

# Exercise 2.11

Consider the set

\[
P = \{x \in \mathbb{R}^n \mid Ax < b\}.
\]

Prove that the problem

\[
\text{maximize } c^T x
\]

subject to

\[
x \in P
\]

does not have an optimal solution.

Assume that

\[
c \ne 0.
\]

---

# Reference Context for Exercises 3.4 and 3.5

Exercises 3.4 and 3.5 should be solved using the simplex method.

Use the same simplex-method structure as the textbook examples:

1. Convert the problem to standard form.
2. Add slack variables where appropriate.
3. Choose an initial basic feasible solution.
4. Identify the basis \(B\) and nonbasis \(N\).
5. Compute reduced costs.
6. Select an entering variable if the current solution is not optimal.
7. Compute the simplex direction.
8. Perform the minimum-ratio test to find the step length.
9. Identify the leaving variable.
10. Update the basis.
11. Repeat until optimality or unboundedness is determined.

For Exercise 3.5(c), use the textbook MATLAB function from Section 3.7:

\[
\texttt{[xsol, objval, exitflag] = SimplexMethod(c, Aeq, beq, B\_set)}
\]

where:

- \(c\) is the objective coefficient vector.
- \(Aeq\) is the equality-constraint matrix after converting to standard form.
- \(beq\) is the right-hand-side vector.
- \(B\_set\) is the set of indices for the initial basic variables.

---

# Exercise 3.4

Consider the following linear program:

\[
\text{minimize } -2x_1 - 5x_2
\]

subject to

\[
-x_1 + 3x_2 \le 2
\]

\[
-3x_1 + 2x_2 \le 1
\]

\[
x_1 \ge 0, \qquad x_2 \ge 0.
\]

## Questions

### (a)

Graph the feasible set.

### (b)

Solve the linear program using the simplex method.

### (c)

Is the linear program bounded?

If not, find the ray along which the linear program is unbounded.

---

# Exercise 3.5

Consider the following linear program:

\[
\text{minimize } -x_2
\]

subject to

\[
x_1 - 2x_2 \le 2
\]

\[
x_1 - x_2 \le 3
\]

\[
x_2 \le 3
\]

\[
x_1 \ge 0, \qquad x_2 \ge 0.
\]

## Questions

### (a)

Solve the linear program using the simplex method.

### (b)

Does the linear program have a unique optimal solution?

If not, derive an expression for the set of optimal solutions.

### (c)

Solve the linear program using the `SimplexMethod` MATLAB function from Section 3.7.

---

# Submission Checklist

## Exercise 2.8

- Sketch the feasible region.
- Convert the system to standard form.
- Find all basic feasible solutions.
- Compare basic feasible solutions with extreme points.
- Identify any extreme points represented by multiple basic feasible solutions.

## Exercise 2.9

- Use Exercise 2.3(a) for part (a).
- Use Exercise 2.3(b) for part (b).
- Generate all basic feasible solutions.
- Show that the set of optimal solutions is convex.

## Exercise 2.11

- Prove that the stated maximization problem has no optimal solution.
- Use the assumptions \(P = \{x \in \mathbb{R}^n \mid Ax < b\}\) and \(c \ne 0\).

## Exercise 3.4

- Graph the feasible set.
- Solve using the simplex method.
- Determine whether the linear program is bounded.
- If unbounded, give the ray of unboundedness.

## Exercise 3.5

- Solve using the simplex method.
- Determine whether the optimal solution is unique.
- If not unique, describe the full set of optimal solutions.
- Solve using the `SimplexMethod` MATLAB function from Section 3.7.