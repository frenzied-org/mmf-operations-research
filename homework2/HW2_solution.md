# Homework 2 solution

### Gerard (Lezhi) Wu

All numerical work in this submission uses Python.  Each assigned exercise has
one corresponding Python script.  In Exercise 3.5(c), `exercise35.py`
contains the standard-form simplex implementation used for the computation.

## Exercise 2.8

### Part (a): feasible region

The constraints can be rewritten as

$$
0 \leq x_1 \leq 3, \qquad x_1 \leq x_2 \leq 6-x_1.
$$

The feasible region is the triangle with vertices

$$
(0,0), \qquad (0,6), \qquad (3,3).
$$

The notebook `HW2_explorer.ipynb` plots this triangle and labels the vertices.

### Part (b): standard form and basic feasible solutions

Add nonnegative slack variables $s_1$, $s_2$, and $s_3$.  The standard-form
system is

$$
\begin{aligned}
x_1+x_2+s_1 &= 6, \\
x_1-x_2+s_2 &= 0, \\
x_1+s_3 &= 3, \\
x_1,x_2,s_1,s_2,s_3 &\geq 0.
\end{aligned}
$$

A **basis** is a choice of three linearly independent columns, one for each
equality.  A **basic feasible solution** is the resulting nonnegative
five-variable solution after setting all nonbasic variables equal to zero.
Python enumeration gives:

| Basis | $(x_1,x_2,s_1,s_2,s_3)$ | Extreme point $(x_1,x_2)$ |
|---|---:|---:|
| $(x_1,x_2,s_1)$ | $(3,3,0,0,0)$ | $(3,3)$ |
| $(x_1,x_2,s_2)$ | $(3,3,0,0,0)$ | $(3,3)$ |
| $(x_1,x_2,s_3)$ | $(3,3,0,0,0)$ | $(3,3)$ |
| $(x_1,s_1,s_3)$ | $(0,0,6,0,3)$ | $(0,0)$ |
| $(x_2,s_1,s_3)$ | $(0,0,6,0,3)$ | $(0,0)$ |
| $(s_1,s_2,s_3)$ | $(0,0,6,0,3)$ | $(0,0)$ |
| $(x_2,s_2,s_3)$ | $(0,6,0,6,3)$ | $(0,6)$ |

### Part (c): correspondence with extreme points

There is no one-to-one correspondence.  A solution is **degenerate** when at
least one basic variable is zero; degeneracy allows several bases to describe
one extreme point.

| Extreme point | Number of feasible bases | Reason |
|---|---:|---|
| $(0,0)$ | 3 | $x_1=x_2=s_2=0$ at the point |
| $(0,6)$ | 1 | Only one feasible basis represents it |
| $(3,3)$ | 3 | $s_1=s_2=s_3=0$ at the point |

Thus both $(0,0)$ and $(3,3)$ are represented by multiple feasible bases,
even though each point is a single basic feasible solution vector.

## Exercise 2.9

### Part (a): Exercise 2.3(a)

Introduce slacks $s_1,s_2,s_3\geq0$:

$$
\begin{aligned}
-2x_1+x_2+s_1 &=2,\\
-x_1+x_2+s_2 &=3,\\
x_1+s_3 &=2.
\end{aligned}
$$

The objective is $z=-x_1-2x_2$.  The feasible bases and objective values are:

| Basis | $(x_1,x_2,s_1,s_2,s_3)$ | $z$ |
|---|---:|---:|
| $(x_1,x_2,s_1)$ | $(2,5,1,0,0)$ | $-12$ |
| $(x_1,x_2,s_3)$ | $(1,4,0,0,1)$ | $-9$ |
| $(x_1,s_1,s_2)$ | $(2,0,6,5,0)$ | $-2$ |
| $(x_2,s_2,s_3)$ | $(0,2,0,1,2)$ | $-4$ |
| $(s_1,s_2,s_3)$ | $(0,0,2,3,2)$ | $0$ |

The minimum is

$$
x^*=(2,5), \qquad z^*=-12.
$$

### Part (b): Exercise 2.3(b)

The first inequality is a greater-than constraint, so subtract a nonnegative
surplus variable $s_1$; add slack $s_2$ to the second inequality:

$$
\begin{aligned}
x_1-2x_2-s_1 &=2,\\
x_1+x_2+s_2 &=4,\\
x_1,x_2,s_1,s_2&\geq0.
\end{aligned}
$$

Python enumeration gives:

| Basis | $(x_1,x_2,s_1,s_2)$ | $z=-x_1-2x_2$ |
|---|---:|---:|
| $(x_1,x_2)$ | $(10/3,2/3,0,0)$ | $-14/3$ |
| $(x_1,s_1)$ | $(4,0,2,0)$ | $-4$ |
| $(x_1,s_2)$ | $(2,0,0,2)$ | $-2$ |

Therefore

$$
x^*=\left(\frac{10}{3},\frac{2}{3}\right),
\qquad z^*=-\frac{14}{3}.
$$

More generally, if $u$ and $v$ are two optimal feasible solutions with common
objective value $z^*$ and $0\leq\lambda\leq1$, linear constraints imply that
$w=\lambda u+(1-\lambda)v$ is feasible, while linearity of the objective gives

$$
c^Tw
=\lambda c^Tu+(1-\lambda)c^Tv
=\lambda z^*+(1-\lambda)z^*
=z^*.
$$

Hence $w$ is also optimal and $P^*$ is convex.  For these supplied data, each
part has a unique optimum, so the illustration reduces to
$P^*=\{x^*\}$.  If $u,v\in P^*$, then $u=v=x^*$, and

$$
\lambda u+(1-\lambda)v
=\lambda x^*+(1-\lambda)x^*
=x^*\in P^*.
$$

Thus each computed optimal-solution set is convex, although each is a
singleton rather than an optimal line segment.

## Exercise 2.11

Let $a_i^T$ denote row $i$ of $A$.  If $P$ is empty, the problem has no
feasible point and therefore has no optimal solution.  Suppose instead that
$P$ is nonempty and take any $x\in P$.  Because the inequalities are strict,
each slack is positive:

$$
\delta_i=b_i-a_i^Tx>0.
$$

Move in direction $c$ by defining

$$
y=x+\epsilon c, \qquad \epsilon>0.
$$

For every row with $a_i^Tc>0$, choose $\epsilon$ small enough that

$$
\epsilon < \frac{\delta_i}{a_i^Tc}.
$$

Rows with $a_i^Tc\leq0$ remain strict for every $\epsilon>0$ because the move
does not increase their left-hand side.  Since there are finitely many rows,
a positive $\epsilon$ satisfying all required upper bounds exists.  Hence
$Ay<b$, so $y\in P$.

The objective strictly improves:

$$
\begin{aligned}
c^Ty-c^Tx
&=c^T(x+\epsilon c)-c^Tx \\
&=\epsilon c^Tc \\
&=\epsilon \lVert c\rVert_2^2 \\
&>0,
\end{aligned}
$$

where the final inequality follows from $\epsilon>0$ and $c\ne0$.  Starting
from any feasible $x$, a feasible point with a larger objective value can be
constructed.  No feasible point can be optimal.

## Exercise 3.4

### Part (a): feasible set

Add slack variables $s_1,s_2\geq0$:

$$
\begin{aligned}
-x_1+3x_2+s_1 &=2,\\
-3x_1+2x_2+s_2 &=1,\\
x_1,x_2,s_1,s_2&\geq0.
\end{aligned}
$$

In the original coordinates the constraints give upper bounds on $x_2$:

$$
0\leq x_2\leq
\min\left(\frac{2+x_1}{3},\frac{1+3x_1}{2}\right),
\qquad x_1\geq0.
$$

The region is unbounded to the right.  The notebook plots the feasible portion
over $0\leq x_1\leq8$ and marks that it continues beyond the plotted window.

### Parts (b) and (c): simplex method and unboundedness

Use the initial basis $B=(s_1,s_2)$.  A **reduced cost** is the objective-rate
change associated with increasing a nonbasic variable while preserving the
equalities.  For a minimization problem, a negative reduced cost permits an
improving pivot.

The variable vector below is ordered as $(x_1,x_2,s_1,s_2)$.  If $d$ is a
simplex direction, a move of length $\theta\geq0$ has the form
$x_{\mathrm{new}}=x+\theta d$.

| Iteration | Basis | Basic point $(x_1,x_2,s_1,s_2)$ | Objective | Entering | Leaving | Step |
|---:|---|---:|---:|---|---|---:|
| 0 | $(s_1,s_2)$ | $(0,0,2,1)$ | $0$ | $x_2$ | $s_2$ | $1/2$ |
| 1 | $(s_1,x_2)$ | $(0,1/2,1/2,0)$ | $-5/2$ | $x_1$ | $s_1$ | $1/7$ |
| 2 | $(x_1,x_2)$ | $(1/7,5/7,0,0)$ | $-27/7$ | $s_2$ | none | unbounded |

The corresponding reduced costs and directions are:

| Iteration | Nonbasic reduced costs | Improving direction $d$ | Ratio test |
|---:|---|---:|---|
| 0 | $(r_{x_1},r_{x_2})=(-2,-5)$ | $(0,1,-3,-2)$ | $\min(2/3,1/2)=1/2$, so $s_2$ leaves |
| 1 | $(r_{x_1},r_{s_2})=(-19/2,5/2)$ | $(1,3/2,-7/2,0)$ | $(1/2)/(7/2)=1/7$, so $s_1$ leaves |
| 2 | $(r_{s_1},r_{s_2})=(19/7,-11/7)$ | $(3/7,1/7,0,1)$ | No component restricts an increase in $s_2$ |

At iteration 2, increasing $s_2$ gives the full standard-form direction

$$
d=\left(\frac{3}{7},\frac{1}{7},0,1\right).
$$

It satisfies $Ad=0$ and $d\geq0$, so every point

$$
x(t)=\left(\frac{1}{7},\frac{5}{7},0,0\right)+td,
\qquad t\geq0,
$$

remains feasible.  Its objective decreases by

$$
c^Td=-2\left(\frac{3}{7}\right)-5\left(\frac{1}{7}\right)
=-\frac{11}{7}<0
$$

per unit of $t$.  The minimization problem is unbounded below.  In the
original two variables a simpler feasible ray is $(x_1,x_2)=(t,0)$ for
$t\geq0$, whose objective is $-2t\to-\infty$.

## Exercise 3.5

### Part (a): simplex method

Add slack variables $s_1,s_2,s_3\geq0$:

$$
\begin{aligned}
x_1-2x_2+s_1 &=2,\\
x_1-x_2+s_2 &=3,\\
x_2+s_3 &=3.
\end{aligned}
$$

The objective coefficient vector, equality matrix, right-hand side, and
initial slack basis used by the Python implementation are

$$
c=(0,-1,0,0,0)^T,
$$

$$
A_{eq}=
\begin{bmatrix}
1&-2&1&0&0\\
1&-1&0&1&0\\
0&1&0&0&1
\end{bmatrix},
\qquad
b_{eq}=
\begin{bmatrix}2\\3\\3\end{bmatrix},
\qquad
B_{\mathrm{set}}=(s_1,s_2,s_3).
$$

Here the variable vector is ordered as $(x_1,x_2,s_1,s_2,s_3)$.

| Iteration | Basis | Basic point $(x_1,x_2,s_1,s_2,s_3)$ | Objective | Entering | Leaving | Step |
|---:|---|---:|---:|---|---|---:|
| 0 | $(s_1,s_2,s_3)$ | $(0,0,2,3,3)$ | $0$ | $x_2$ | $s_3$ | $3$ |
| 1 | $(s_1,s_2,x_2)$ | $(0,3,8,6,0)$ | $-3$ | none | none | optimal |

At iteration 0, the nonbasic reduced costs are
$(r_{x_1},r_{x_2})=(0,-1)$.  Thus $x_2$ enters.  Its simplex direction is

$$
d=(0,1,2,1,-1),
$$

and only $s_3$ decreases, giving the ratio $3/1=3$ and the pivot shown in the
table.  At iteration 1, the nonbasic reduced costs are
$(r_{x_1},r_{s_3})=(0,1)$.  There is no negative reduced cost, so the point is
optimal.  The zero reduced cost for $x_1$ also signals alternate optima:
increasing $x_1$ uses direction

$$
d_{\mathrm{alt}}=(1,0,-1,-1,0).
$$

The maximum feasible step is
$\min(8/1,6/1)=6$, which reaches the second optimal endpoint $(6,3)$.

One optimal basic feasible solution is therefore

$$
(x_1,x_2)=(0,3), \qquad z^*=-3.
$$

### Part (b): all optimal solutions

The objective is $-x_2$, so its minimum is obtained by taking $x_2$ as large
as possible.  The third constraint gives $x_2\leq3$; therefore every optimum
has $x_2=3$.  Substitution into the first two constraints gives

$$
x_1\leq8, \qquad x_1\leq6, \qquad x_1\geq0.
$$

The second upper bound binds first.  Hence the complete optimal set is

$$
P^*=\{(x_1,x_2)=(t,3)\mid 0\leq t\leq6\}.
$$

The optimum is not unique.  For example, both $(0,3)$ and $(6,3)$ have
objective value $-3$, and every point on the line segment joining them does
as well.

### Part (c): Python simplex execution

The computation is performed by importing the exercise solver:

```python
from exercise35 import solve_exercise_35

solution = solve_exercise_35()
result = solution.simplex_result
```

The file `exercise35.py` performs this standard-form calculation in Python
using `objective_coefficients`, `equality_matrix`, `right_hand_side`, and
`initial_basis`.  It starts from the same three slack variables, performs one
pivot, and returns the result

$$
(x_1,x_2,s_1,s_2,s_3)=(0,3,8,6,0),
\qquad z^*=-3.
$$
