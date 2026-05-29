# MMF 1921 — Expanded Markdown Answer Key with Questions

This Markdown file is written as a study guide, not just a list of final answers. For each problem, I include:

1. a cleaned version of the question,
2. the main definitions and setup,
3. the reasoning steps, and
4. the final answer.

## Notation used throughout

- $x$ is usually a vector of decision variables.
- $e$ or $\mathbf{1}$ is the vector of all ones.
- $Q$ or $V$ is a covariance matrix.
- $\mu$ is a vector of expected returns.
- KKT means **Karush-Kuhn-Tucker** conditions, which are first-order optimality conditions for constrained optimization.
- VaR means **Value-at-Risk**.
- CVaR means **Conditional Value-at-Risk**, also called expected shortfall.
- In the robust-optimization questions, the exam writes the second ellipsoidal constraint as $y^2 \ge x^T \Theta x$. Since the expected returns were estimated using 20 monthly observations, I use

$$
\Theta = \frac{Q}{20}.
$$

---

# 2023 Final Exam

## Problem 1 — Linear programming formulation for staged investments

### Question

You have three investments available:

- Investment A: for each dollar invested at time 0, receive $0.10 at time 1 and $1.30 at time 2.
- Investment B: for each dollar invested at time 1, receive $1.60 at time 2.
- Investment C: for each dollar invested at time 2, receive $1.20 at time 3.
- Leftover cash can be invested in one-year Treasury bills paying 10% per year.
- You have $100 at time 0.
- At most $50 can be invested in each of A, B, and C.

Formulate, but do not solve, a linear program that maximizes cash at time 3.

### Answer and explanation

The key idea is to write a **cash-flow balance equation at each time**. Money that is available at a time must either be invested in the available risky investment or put into Treasury bills.

Define the decision variables:

- $A$ = dollars invested in investment A at time 0.
- $B$ = dollars invested in investment B at time 1.
- $C$ = dollars invested in investment C at time 2.
- $T_0$ = dollars invested in Treasury bills at time 0.
- $T_1$ = dollars invested in Treasury bills at time 1.
- $T_2$ = dollars invested in Treasury bills at time 2.

All variables are nonnegative. The Treasury bill variable $T_t$ means cash placed into the risk-free investment from time $t$ to time $t+1$.

At time 0, you have $100. You can split it between investment A and Treasury bills:

$$
A + T_0 = 100.
$$

At time 1, you receive $0.10A$ from investment A and $1.10T_0$ from Treasury bills. That cash is split between investment B and Treasury bills:

$$
B + T_1 = 0.10A + 1.10T_0.
$$

At time 2, you receive $1.30A$ from investment A, $1.60B$ from investment B, and $1.10T_1$ from Treasury bills. That cash is split between investment C and Treasury bills:

$$
C + T_2 = 1.30A + 1.60B + 1.10T_1.
$$

At time 3, the cash comes from investment C and the last Treasury bill:

$$
\text{cash at time 3} = 1.20C + 1.10T_2.
$$

The full linear program is therefore

$$
\begin{aligned}
\max \quad & 1.20C + 1.10T_2 \\
\text{s.t.}\quad
& A + T_0 = 100, \\
& B + T_1 = 0.10A + 1.10T_0, \\
& C + T_2 = 1.30A + 1.60B + 1.10T_1, \\
& 0 \le A \le 50, \\
& 0 \le B \le 50, \\
& 0 \le C \le 50, \\
& T_0,T_1,T_2 \ge 0.
\end{aligned}
$$

The important modeling point is that this is linear because every cash-flow term is a constant times a decision variable. There are no products of decision variables.

---

## Problem 2 — LP dual and simplex method

### Question

Consider the linear program

$$
\begin{aligned}
\min \quad & -4x_1 - 3x_2 - 2x_3 \\
\text{s.t.}\quad
& 2x_1 + 3x_2 + 2x_3 \le 6, \\
& -x_1 + x_2 + x_3 \le 5, \\
& x_1,x_2,x_3 \ge 0.
\end{aligned}
$$

(a) Write the dual.  
(b) Solve the primal using the simplex method and show that the dual is solved to optimality at the same time.

### Part (a) — Dual

The primal is a minimization problem with constraints of the form $Ax \le b$ and $x \ge 0$.

For this sign pattern:

- primal is a minimization,
- constraints are $\le$,
- variables are nonnegative,

so the dual variables satisfy $y \le 0$, and the dual constraints are $A^T y \le c$.

Here

$$
A =
\begin{bmatrix}
2 & 3 & 2 \\
-1 & 1 & 1
\end{bmatrix},
\quad
b =
\begin{bmatrix}
6 \\
5
\end{bmatrix},
\quad
c =
\begin{bmatrix}
-4 \\
-3 \\
-2
\end{bmatrix}.
$$

The dual is

$$
\begin{aligned}
\max \quad & 6y_1 + 5y_2 \\
\text{s.t.}\quad
& 2y_1 - y_2 \le -4, \\
& 3y_1 + y_2 \le -3, \\
& 2y_1 + y_2 \le -2, \\
& y_1,y_2 \le 0.
\end{aligned}
$$

### Part (b) — Simplex solution

Add slack variables $s_1,s_2 \ge 0$:

$$
\begin{aligned}
2x_1 + 3x_2 + 2x_3 + s_1 &= 6, \\
-x_1 + x_2 + x_3 + s_2 &= 5.
\end{aligned}
$$

The initial basic variables are $s_1$ and $s_2$:

$$
(x_1,x_2,x_3,s_1,s_2) = (0,0,0,6,5).
$$

The objective value is $0$. Because this is a minimization problem, a negative reduced cost tells us that increasing that variable can reduce the objective. The original objective coefficients are

$$
(-4,-3,-2).
$$

The most negative coefficient is for $x_1$, so let $x_1$ enter the basis.

When $x_1$ increases by $\theta$:

- the first constraint gives $s_1 = 6 - 2\theta$,
- the second constraint gives $s_2 = 5 + \theta$.

Only $s_1$ restricts the increase, because $s_2$ increases. The ratio test gives

$$
\theta \le \frac{6}{2} = 3.
$$

So $s_1$ leaves and $x_1=3$. The new basic feasible solution is

$$
(x_1,x_2,x_3,s_1,s_2) = (3,0,0,0,8).
$$

The objective value is

$$
-4(3)-3(0)-2(0) = -12.
$$

Now compute the reduced costs using the basis $\{x_1,s_2\}$. The basis matrix is

$$
B =
\begin{bmatrix}
2 & 0 \\
-1 & 1
\end{bmatrix},
\quad
c_B =
\begin{bmatrix}
-4 \\
0
\end{bmatrix}.
$$

The simplex multiplier is

$$
y^T = c_B^T B^{-1} = (-2,0).
$$

The reduced costs for the nonbasic variables are all nonnegative:

$$
r_{x_2}=3,
\quad
r_{x_3}=2,
\quad
r_{s_1}=2.
$$

Since this is a minimization problem, nonnegative reduced costs mean no nonbasic variable can enter and reduce the objective. Therefore the primal optimum is

$$
\boxed{x^*=(3,0,0)^T}
$$

with optimal value

$$
\boxed{-12}.
$$

### Showing the dual is also optimal

At termination, the simplex multiplier is

$$
y^* = (-2,0)^T.
$$

Check the dual constraints:

$$
2y_1-y_2 = 2(-2)-0 = -4 \le -4,
$$

$$
3y_1+y_2 = 3(-2)+0 = -6 \le -3,
$$

$$
2y_1+y_2 = 2(-2)+0 = -4 \le -2.
$$

Also $y_1,y_2 \le 0$, so $y^*$ is dual feasible.

Its objective value is

$$
6(-2)+5(0) = -12.
$$

This equals the primal value. By weak duality, a feasible primal solution and a feasible dual solution with the same value must both be optimal. Therefore the dual is solved to optimality as well.

---

## Problem 3 — Nonlinear optimization

## Part 1

### Question

For

$$
f(x_1,x_2)=2x_2^3-6x_2^2+3x_1^2x_2,
$$

find all stationary points and classify them.

### Answer and explanation

A stationary point is a point where the gradient is zero. The gradient is the vector of first partial derivatives:

$$
\nabla f(x_1,x_2)=
\begin{bmatrix}
\frac{\partial f}{\partial x_1} \\
\frac{\partial f}{\partial x_2}
\end{bmatrix}
=
\begin{bmatrix}
6x_1x_2 \\
6x_2^2-12x_2+3x_1^2
\end{bmatrix}.
$$

Set both components equal to zero:

$$
6x_1x_2=0,
$$

and

$$
6x_2^2-12x_2+3x_1^2=0.
$$

Divide the second equation by $3$:

$$
2x_2^2-4x_2+x_1^2=0.
$$

The first equation says either $x_1=0$ or $x_2=0$.

If $x_1=0$, then

$$
2x_2^2-4x_2=0
\quad\Longrightarrow\quad
2x_2(x_2-2)=0.
$$

So $x_2=0$ or $x_2=2$. This gives $(0,0)$ and $(0,2)$.

If $x_2=0$, then the second equation becomes

$$
x_1^2=0,
$$

so $x_1=0$. This again gives $(0,0)$.

Therefore the stationary points are

$$
\boxed{(0,0) \text{ and } (0,2)}.
$$

To classify them, compute the Hessian matrix, which is the matrix of second partial derivatives:

$$
H(x_1,x_2)=
\begin{bmatrix}
6x_2 & 6x_1 \\
6x_1 & 12x_2-12
\end{bmatrix}.
$$

At $(0,2)$:

$$
H(0,2)=
\begin{bmatrix}
12 & 0 \\
0 & 12
\end{bmatrix}.
$$

This matrix is positive definite because both eigenvalues are positive. Therefore $(0,2)$ is a strict local minimum.

It is not a global minimum because the function is unbounded below. For example, if $x_1=0$ and $x_2\to -\infty$, then

$$
f(0,x_2)=2x_2^3-6x_2^2\to -\infty.
$$

At $(0,0)$:

$$
H(0,0)=
\begin{bmatrix}
0 & 0 \\
0 & -12
\end{bmatrix}.
$$

The Hessian test is inconclusive because the Hessian is negative semidefinite but singular. To classify the point, check different paths approaching $(0,0)$.

Along the path $x_1=0$, $x_2=t$:

$$
f(0,t)=2t^3-6t^2.
$$

For small nonzero $t$, this is negative because the $-6t^2$ term dominates.

Along the path $x_1=2t$, $x_2=t^2$:

$$
f(2t,t^2)=2t^6-6t^4+3(4t^2)(t^2)=2t^6+6t^4.
$$

For small nonzero $t$, this is positive.

Because the function is positive in some directions and negative in others near $(0,0)$, the point $(0,0)$ is a saddle point.

Final classification:

$$
\boxed{(0,0) \text{ is a saddle point.}}
$$

$$
\boxed{(0,2) \text{ is a strict local minimum, but not a global minimum.}}
$$

There are no local maxima and no global extrema.

---

## Problem 3, Part 2 — Rosenbrock function

### Question

Consider

$$
f(x_1,x_2)=100(x_2-x_1^2)^2+(1-x_1)^2.
$$

(a) Prove that $(1,1)^T$ is the unique global minimizer.  
(b) Starting from $x^{(0)}=(0,0)^T$, apply two iterations of pure Newton's method.  
(c) Starting from $x^{(0)}=(0,0)^T$, apply two iterations of gradient descent with step length $0.05$.

### Part (a) — Unique global minimizer

The function is a sum of two squared terms:

$$
f(x_1,x_2)=100(x_2-x_1^2)^2+(1-x_1)^2.
$$

A square is always nonnegative, so

$$
f(x_1,x_2)\ge 0
$$

for all $(x_1,x_2)\in\mathbb{R}^2$.

The smallest possible value is therefore $0$. To get value $0$, both squares must be zero:

$$
x_2-x_1^2=0,
$$

and

$$
1-x_1=0.
$$

The second equation gives $x_1=1$. Substituting into the first gives $x_2=1$. Therefore the only point where $f=0$ is $(1,1)^T$.

Thus

$$
\boxed{(1,1)^T \text{ is the unique global minimizer.}}
$$

### Part (b) — Two Newton iterations

Newton's method for minimization uses

$$
x^{(k+1)} = x^{(k)} + d^{(k)},
$$

where the Newton direction $d^{(k)}$ solves

$$
\nabla^2 f(x^{(k)})d^{(k)} = -\nabla f(x^{(k)}).
$$

The gradient is

$$
\nabla f(x_1,x_2)=
\begin{bmatrix}
400x_1^3-400x_1x_2+2x_1-2 \\
200(x_2-x_1^2)
\end{bmatrix}.
$$

The Hessian is

$$
\nabla^2 f(x_1,x_2)=
\begin{bmatrix}
1200x_1^2-400x_2+2 & -400x_1 \\
-400x_1 & 200
\end{bmatrix}.
$$

At $x^{(0)}=(0,0)^T$:

$$
\nabla f(0,0)=
\begin{bmatrix}
-2 \\
0
\end{bmatrix},
\quad
\nabla^2 f(0,0)=
\begin{bmatrix}
2 & 0 \\
0 & 200
\end{bmatrix}.
$$

Solve

$$
\begin{bmatrix}
2 & 0 \\
0 & 200
\end{bmatrix}
\begin{bmatrix}
d_1 \\
d_2
\end{bmatrix}
=
\begin{bmatrix}
2 \\
0
\end{bmatrix}.
$$

This gives $d^{(0)}=(1,0)^T$, so

$$
x^{(1)}=(0,0)^T+(1,0)^T=(1,0)^T.
$$

At $x^{(1)}=(1,0)^T$:

$$
\nabla f(1,0)=
\begin{bmatrix}
400 \\
-200
\end{bmatrix},
$$

and

$$
\nabla^2 f(1,0)=
\begin{bmatrix}
1202 & -400 \\
-400 & 200
\end{bmatrix}.
$$

The Newton direction solves

$$
\begin{bmatrix}
1202 & -400 \\
-400 & 200
\end{bmatrix}
\begin{bmatrix}
d_1 \\
d_2
\end{bmatrix}
=
\begin{bmatrix}
-400 \\
200
\end{bmatrix}.
$$

Solving gives

$$
d^{(1)}=(0,1)^T.
$$

Therefore

$$
x^{(2)}=(1,0)^T+(0,1)^T=(1,1)^T.
$$

Final Newton iterates:

$$
\boxed{x^{(1)}=(1,0)^T, \qquad x^{(2)}=(1,1)^T.}
$$

### Part (c) — Two gradient descent iterations

Gradient descent with constant step length $\alpha=0.05$ is

$$
x^{(k+1)} = x^{(k)} - 0.05\nabla f(x^{(k)}).
$$

At $x^{(0)}=(0,0)^T$:

$$
\nabla f(0,0)=(-2,0)^T.
$$

So

$$
x^{(1)}=(0,0)^T-0.05(-2,0)^T=(0.1,0)^T.
$$

At $x^{(1)}=(0.1,0)^T$:

$$
\nabla f(0.1,0)=
\begin{bmatrix}
400(0.1)^3-400(0.1)(0)+2(0.1)-2 \\
200(0-(0.1)^2)
\end{bmatrix}
=
\begin{bmatrix}
-1.4 \\
-2
\end{bmatrix}.
$$

Thus

$$
x^{(2)}=(0.1,0)^T-0.05(-1.4,-2)^T.
$$

So

$$
\boxed{x^{(2)}=(0.17,0.10)^T.}
$$

---

## Problem 4 — Minimum variance portfolio

### Question

Consider

$$
\min_x x^T Vx
\quad\text{s.t.}\quad
 e^T x=1,
$$

where $V$ is the covariance matrix and $e$ is the vector of all ones.

(a) Find the closed-form solution when short selling is allowed.  
(b) Find the KKT conditions when short selling is not allowed. Is a closed-form solution possible?

### Part (a) — Short selling allowed

The constraint says all portfolio weights must add to one. Because short selling is allowed, weights can be negative.

Write the Lagrangian:

$$
L(x,\lambda)=x^TVx-\lambda(e^Tx-1).
$$

Different sign conventions for $\lambda$ are possible. The final portfolio weights will be the same.

The first-order condition with respect to $x$ is

$$
2Vx-\lambda e=0.
$$

Therefore

$$
Vx=\frac{\lambda}{2}e.
$$

Assuming $V$ is invertible,

$$
x=\frac{\lambda}{2}V^{-1}e.
$$

Now use the budget constraint $e^Tx=1$:

$$
e^Tx=\frac{\lambda}{2}e^TV^{-1}e=1.
$$

So

$$
\frac{\lambda}{2}=\frac{1}{e^TV^{-1}e}.
$$

Substitute this back into $x$:

$$
\boxed{x^*=\frac{V^{-1}e}{e^TV^{-1}e}.}
$$

This is the global minimum-variance portfolio.

The closed form is well-defined and unique if $V$ is symmetric positive definite. Positive definiteness matters because:

1. $V^{-1}$ exists.
2. $e^TV^{-1}e>0$, so the denominator is not zero.
3. $x^TVx$ is strictly convex, so the feasible minimizer is unique.

### Part (b) — No short selling

Now add

$$
x\ge 0.
$$

The problem is

$$
\begin{aligned}
\min_x\quad & x^TVx \\
\text{s.t.}\quad & e^Tx=1, \\
& x\ge 0.
\end{aligned}
$$

Introduce:

- $\lambda$ for the equality constraint $e^Tx=1$,
- $\nu_i\ge 0$ for the inequality $x_i\ge 0$.

Using the Lagrangian

$$
L(x,\lambda,\nu)=x^TVx+\lambda(e^Tx-1)-\nu^Tx,
$$

the KKT conditions are

$$
\boxed{2Vx+\lambda e-\nu=0}
$$

$$
\boxed{e^Tx=1}
$$

$$
\boxed{x\ge 0,\quad \nu\ge 0}
$$

$$
\boxed{\nu_i x_i=0 \quad \text{for every } i.}
$$

The last condition is complementary slackness. It says that for each asset, either:

- the asset has positive weight, so its nonnegativity constraint is not binding and $\nu_i=0$, or
- the asset has zero weight, so the nonnegativity constraint may have positive multiplier.

There is usually no single closed-form formula for the no-short-selling case because we do not know in advance which assets will have zero weights. If we knew the active set of zero-weight assets, we could solve the minimum-variance formula on the remaining assets. But identifying that active set is part of the optimization problem.

---

## Problem 5 — True/False questions

### Question

Give True/False answers with brief justification.

(a) Risk parity portfolios do not always have better risk-return characteristics than minimum variance portfolios.  
(b) For a nonlinear optimization problem with equality and inequality constraints, at optimality the problem can essentially be transformed into one with only equality constraints.  
(c) In the Black-Litterman framework, subjective views are allowed to be correlated.  
(d) KKT conditions are both sufficient and necessary for all convex optimization problems.

### Answers and explanation

#### (a) True

Risk parity portfolios equalize risk contributions. Minimum-variance portfolios minimize total portfolio variance. These are different objectives. Equalizing risk contributions can produce a more diversified-looking portfolio, but that does not guarantee a better risk-return tradeoff in every market environment.

So the statement is true.

#### (b) True, with a regularity caveat

At a KKT point, each inequality constraint is either:

- active, meaning it binds as an equality, or
- inactive, meaning it has zero multiplier.

So once the active set is known, the problem behaves like an equality-constrained problem around the solution. The caveat is that this active-set interpretation relies on regularity conditions, also called constraint qualifications.

So the intended answer is true.

#### (c) True

In Black-Litterman, subjective views are represented with a view-error covariance matrix, usually denoted $\Omega$. If $\Omega$ has off-diagonal entries, the view errors are correlated. Therefore subjective views are allowed to be correlated.

So the statement is true.

#### (d) False

For convex optimization problems, KKT conditions are sufficient under the standard convexity assumptions. However, they are not automatically necessary for all convex problems unless a constraint qualification holds. For example, Slater's condition is one common condition that ensures KKT necessity in convex problems.

Therefore the statement says too much and is false.

---

## Problem 6 — Robust optimization KKT check

### Question

You have two stocks with

$$
\mu_A=0.025,
\quad
\mu_B=0.015,
\quad
\sigma_A^2=0.0049,
\quad
\sigma_B^2=0.0025,
\quad
\sigma_{AB}=0.001.
$$

The expected returns were estimated using the last 20 monthly observations. Consider

$$
\begin{aligned}
\min_{x,y}\quad & x^TQx \\
\text{s.t.}\quad
& \mu^Tx-y\ge 1\%, \\
& y^2\ge x^T\Theta x, \\
& \mathbf{1}^Tx=1, \\
& y\ge 0.
\end{aligned}
$$

Check whether

$$
x=\begin{bmatrix}0.425\\0.575\end{bmatrix}
$$

satisfies the KKT conditions. Assume the target-return constraint is active.

### Answer and explanation

First build the covariance matrix:

$$
Q=
\begin{bmatrix}
0.0049 & 0.001 \\
0.001 & 0.0025
\end{bmatrix}.
$$

Since the means were estimated from 20 observations, the covariance matrix of the estimated mean is

$$
\Theta=\frac{Q}{20}.
$$

The return vector is

$$
\mu=
\begin{bmatrix}
0.025 \\
0.015
\end{bmatrix}.
$$

The question says to assume the target-return constraint is active. That means

$$
\mu^Tx-y=0.01.
$$

So

$$
y=\mu^Tx-0.01.
$$

Compute $\mu^Tx$:

$$
\mu^Tx=0.025(0.425)+0.015(0.575).
$$

This gives

$$
\mu^Tx=0.01925.
$$

Therefore

$$
y=0.01925-0.01=0.00925.
$$

Now check the ellipsoidal constraint:

$$
y^2\ge x^T\Theta x.
$$

First,

$$
y^2=(0.00925)^2=0.0000855625.
$$

Next,

$$
x^TQx=0.002200375.
$$

Therefore

$$
x^T\Theta x=\frac{0.002200375}{20}=0.00011001875.
$$

Compare:

$$
y^2=0.0000855625
$$

but

$$
x^T\Theta x=0.00011001875.
$$

The required inequality is

$$
y^2\ge x^T\Theta x,
$$

but here

$$
0.0000855625 < 0.00011001875.
$$

So the proposed point is not even feasible. A point that is not feasible cannot satisfy the KKT conditions.

Thus

$$
\boxed{\text{The proposed } x=(0.425,0.575)^T \text{ does not satisfy the KKT conditions.}}
$$

The most important point is that we do not even need to check stationarity once feasibility fails. KKT conditions require primal feasibility first.

---

## Problem 7 — CVaR formulation and robust counterpart

### Question

The scenario-based CVaR minimization formulation is

$$
\begin{aligned}
\min \quad & \gamma + \frac{1}{(1-\beta)S}\sum_{s=1}^S z_s \\
\text{s.t.}\quad
& z_s\ge 0, && s=1,\ldots,S, \\
& z_s\ge f(x,y_s)-\gamma, && s=1,\ldots,S, \\
& \mathbf{1}^Tx=1, \\
& \mu^Tx\ge R, \\
& x\ge 0.
\end{aligned}
$$

(a) Define $\gamma$, $\beta$, $z_s$, $y_s$, and $f(x,y_s)$.  
(b) Formulate the most tractable robust counterpart when the model is robust with respect to $\mu$ using an ellipsoidal uncertainty set.

### Part (a) — Definitions

The model is a finite-scenario version of CVaR minimization.

- $\gamma$ is the threshold variable. At the optimum, it becomes a Value-at-Risk level for the loss distribution.
- $\beta$ is the confidence level, such as $0.95$ or $0.99$.
- $S$ is the number of scenarios.
- $z_s$ is the excess loss above the threshold $\gamma$ in scenario $s$.
- $y_s$ is the random scenario data in scenario $s$.
- $f(x,y_s)$ is the loss produced by portfolio decision $x$ under scenario $y_s$.

The constraints

$$
z_s\ge f(x,y_s)-\gamma
$$

and

$$
z_s\ge 0
$$

together force

$$
z_s=\max\{f(x,y_s)-\gamma,0\}
$$

at the optimum. That is why the objective measures the average tail loss above $\gamma$.

### Part (b) — Robust counterpart for uncertain $\mu$

The only uncertain part is the expected-return constraint

$$
\mu^Tx\ge R.
$$

To make this robust, require it to hold for every $\mu$ in an ellipsoid. Let

$$
\mathcal{U}=\left\{\mu:\mu=\widehat{\mu}+\Sigma_\mu^{1/2}u,\ \|u\|_2\le \rho\right\}.
$$

Here:

- $\widehat{\mu}$ is the estimated expected-return vector.
- $\Sigma_\mu$ is the uncertainty covariance or shape matrix.
- $\rho$ is the radius of the uncertainty set.
- $u$ is an auxiliary vector with Euclidean norm at most $\rho$.

The robust return constraint is

$$
\mu^Tx\ge R \quad \text{for all } \mu\in\mathcal{U}.
$$

The worst-case expected return is

$$
\min_{\mu\in\mathcal{U}} \mu^Tx
=\widehat{\mu}^Tx-\rho\|\Sigma_\mu^{1/2}x\|_2.
$$

So the robust counterpart is

$$
\widehat{\mu}^Tx-\rho\|\Sigma_\mu^{1/2}x\|_2\ge R.
$$

To write this as a second-order cone constraint, introduce an auxiliary scalar $t$:

$$
\|\Sigma_\mu^{1/2}x\|_2\le t.
$$

Then impose

$$
\widehat{\mu}^Tx-\rho t\ge R.
$$

The robust CVaR formulation is

$$
\begin{aligned}
\min \quad & \gamma + \frac{1}{(1-\beta)S}\sum_{s=1}^S z_s \\
\text{s.t.}\quad
& z_s\ge 0, && s=1,
\ldots,S, \\
& z_s\ge f(x,y_s)-\gamma, && s=1,
\ldots,S, \\
& \mathbf{1}^Tx=1, \\
& \widehat{\mu}^Tx-\rho t\ge R, \\
& \|\Sigma_\mu^{1/2}x\|_2\le t, \\
& x\ge 0.
\end{aligned}
$$

This is the most tractable form because the uncertainty has been converted into a second-order cone constraint.

---

# 2024 Final Exam

## Problem 1 — Warehouse commodity LP

### Question

A warehouse can store 10,000 units of a commodity. The trader starts with 2,000 units in storage. At the start of each month $t=1,\ldots,12$, the trader may buy at price $p_t$ or sell at price $s_t$. The trader pays inventory cost $i_t$ for holding the commodity. The trader wants zero inventory at the end of the year. Formulate an LP that maximizes profit.

### Answer and explanation

This is an inventory balance problem. The key state variable is how much inventory remains after each month.

Define:

- $B_t$ = units bought at the start of month $t$.
- $S_t$ = units sold at the start of month $t$.
- $I_t$ = inventory at the end of month $t$.
- $I_0=2000$ = initial inventory.
- Warehouse capacity is $10{,}000$.

The inventory balance is

$$
I_t=I_{t-1}+B_t-S_t,
\quad t=1,\ldots,12.
$$

This says ending inventory equals beginning inventory plus purchases minus sales.

The trader cannot store more than capacity:

$$
0\le I_t\le 10000.
$$

The trader also cannot sell more than what is available at the beginning of the month:

$$
S_t\le I_{t-1}.
$$

The trader cannot buy more than the empty space available in the warehouse at the beginning of the month:

$$
B_t\le 10000-I_{t-1}.
$$

The final inventory must be zero:

$$
I_{12}=0.
$$

Profit equals selling revenue minus purchase cost minus inventory holding cost:

$$
\sum_{t=1}^{12}(s_tS_t-p_tB_t-i_tI_t).
$$

The LP is

$$
\begin{aligned}
\max \quad & \sum_{t=1}^{12}(s_tS_t-p_tB_t-i_tI_t) \\
\text{s.t.}\quad
& I_t=I_{t-1}+B_t-S_t, && t=1,\ldots,12, \\
& 0\le I_t\le 10000, && t=1,\ldots,12, \\
& S_t\le I_{t-1}, && t=1,\ldots,12, \\
& B_t\le 10000-I_{t-1}, && t=1,\ldots,12, \\
& I_0=2000, \\
& I_{12}=0, \\
& B_t,S_t\ge 0, && t=1,\ldots,12.
\end{aligned}
$$

A minor convention issue: if inventory cost is charged on beginning inventory rather than ending inventory, replace $i_tI_t$ with $i_tI_{t-1}$ in the objective. The structure of the LP is the same.

---

## Problem 2 — LP dual, simplex, and reduced-cost necessity

### Question

Same primal LP as 2023 Problem 2:

$$
\begin{aligned}
\min \quad & -4x_1-3x_2-2x_3 \\
\text{s.t.}\quad
& 2x_1+3x_2+2x_3\le 6, \\
& -x_1+x_2+x_3\le 5, \\
& x_1,x_2,x_3\ge 0.
\end{aligned}
$$

(a) Write the dual.  
(b) Solve the primal using simplex.  
(c) Use the simplex work to show the dual is optimal at termination.  
(d) Explain why $r_N\ge 0$ is necessary for optimality.

### Parts (a), (b), and (c)

The dual and simplex solution are the same as in 2023 Problem 2.

The dual is

$$
\begin{aligned}
\max \quad & 6y_1+5y_2 \\
\text{s.t.}\quad
& 2y_1-y_2\le -4, \\
& 3y_1+y_2\le -3, \\
& 2y_1+y_2\le -2, \\
& y_1,y_2\le 0.
\end{aligned}
$$

The primal optimum is

$$
\boxed{x^*=(3,0,0)^T}
$$

with optimal value

$$
\boxed{-12}.
$$

At termination, the basis is $\{x_1,s_2\}$. The simplex multiplier is

$$
y^T=c_B^TB^{-1}=(-2,0).
$$

This vector is dual feasible and has dual objective value $-12$. Since primal and dual feasible solutions have the same value, both are optimal.

### Part (d) — Why $r_N\ge 0$ is necessary

At a basic feasible solution, the nonbasic variables $x_N$ are zero. Any feasible solution can be written in terms of the nonbasic variables. The objective change from the current basic feasible solution is

$$
c^Tx-c^Tx^* = r_N^Tx_N.
$$

For a minimization problem, an optimal solution must not allow any feasible movement that lowers the objective.

Suppose one reduced cost is negative, say $r_j<0$. Then increasing the corresponding nonbasic variable $x_j$ from zero, while following the simplex direction that keeps $Ax=b$, would initially change the objective by

$$
r_j x_j<0.
$$

That would reduce the objective, contradicting optimality. Therefore every nonbasic reduced cost must be nonnegative:

$$
\boxed{r_N\ge 0.}
$$

The expression $r_N^Tx_N\ge 0$ might look possible even if some $r_j<0$, because other terms could offset it. But the simplex method can test variables one at a time. If any one reduced cost is negative, we can choose that variable as the only entering nonbasic variable and get a descent direction. That is why nonnegativity of every reduced cost is necessary.

---

## Problem 3 — Rosenbrock and gradient descent sequence

## Part 1 — Rosenbrock function

### Question

For

$$
f(x_1,x_2)=100(x_2-x_1^2)^2+(1-x_1)^2,
$$

prove $(1,1)^T$ is the unique global minimizer and apply two pure Newton iterations from $(0,0)^T$.

### Answer

The proof of uniqueness and the Newton iterations are exactly as in the 2023 solution:

$$
\boxed{(1,1)^T \text{ is the unique global minimizer.}}
$$

Starting from $x^{(0)}=(0,0)^T$:

$$
\boxed{x^{(1)}=(1,0)^T,\qquad x^{(2)}=(1,1)^T.}
$$

The reason Newton reaches the minimizer in two steps here is not because Newton always does this. It is because the starting point and the structure of the Rosenbrock function produce exactly the two directions $(1,0)^T$ and $(0,1)^T$.

## Part 2 — Gradient descent for $f(x)=x^2-x^3/3$

### Question

Let

$$
f(x)=x^2-\frac{x^3}{3}.
$$

Apply gradient descent with step length $0.5$ and initial point $x^{(0)}=1$.

(a) Write the formula for the $(k+1)$st iterate.  
(b) Derive a closed form for $x^{(k)}$.  
(c) Show convergence to a strict local minimum.  
(d) Find the convergence rate.

### Part (a) — Iteration formula

First compute the derivative:

$$
f'(x)=2x-x^2.
$$

Gradient descent in one dimension is

$$
x^{(k+1)}=x^{(k)}-\alpha f'(x^{(k)}),
$$

where $\alpha=0.5$. Therefore

$$
x^{(k+1)}=x^{(k)}-0.5\left(2x^{(k)}-(x^{(k)})^2\right).
$$

Simplify:

$$
x^{(k+1)}=x^{(k)}-x^{(k)}+0.5(x^{(k)})^2.
$$

So

$$
\boxed{x^{(k+1)}=\frac{1}{2}(x^{(k)})^2.}
$$

### Part (b) — Closed form

Starting from $x^{(0)}=1$:

$$
x^{(1)}=\frac12,
$$

$$
x^{(2)}=\frac12\left(\frac12\right)^2=\frac18,
$$

$$
x^{(3)}=\frac12\left(\frac18\right)^2=\frac{1}{128}.
$$

The pattern is

$$
\boxed{x^{(k)}=2^{-(2^k-1)}.}
$$

Check by induction. For $k=0$:

$$
2^{-(2^0-1)}=2^0=1=x^{(0)}.
$$

Assume it is true for $k$. Then

$$
x^{(k+1)}=\frac12(x^{(k)})^2
=\frac12\left(2^{-(2^k-1)}\right)^2.
$$

This becomes

$$
x^{(k+1)}=2^{-1}2^{-2(2^k-1)}=2^{-(2^{k+1}-1)}.
$$

So the formula holds for all $k$.

### Part (c) — Convergence to a strict local minimum

Because $2^k-1\to\infty$,

$$
x^{(k)}=2^{-(2^k-1)}\to 0.
$$

So the iterates converge to $0$.

To classify $0$, compute the second derivative:

$$
f''(x)=2-2x.
$$

At $x=0$:

$$
f''(0)=2>0.
$$

Therefore $x=0$ is a strict local minimum.

### Part (d) — Rate of convergence

Let the error be

$$
e_k=x^{(k)}-0=x^{(k)}.
$$

The recurrence is

$$
e_{k+1}=\frac12 e_k^2.
$$

This is quadratic convergence because the next error is proportional to the square of the current error. More precisely,

$$
\lim_{k\to\infty}\frac{|e_{k+1}|}{|e_k|^2}=\frac12.
$$

So the convergence is

$$
\boxed{\text{quadratic, with asymptotic constant } 1/2.}
$$

---

## Problem 4 — Mean-variance portfolio with budget only

### Question

Consider the mean-variance problem with short selling allowed and only a budget constraint. The exam text says one maximizes risk-adjusted return, although the displayed problem has a minimization label. The meaningful interpretation is

$$
\max_x \ \mu^Tx-\frac{\gamma}{2}x^TQx
\quad\text{s.t.}\quad
\mathbf{1}^Tx=1,
$$

where $\gamma>0$ is risk aversion.

(a) Find the closed-form solution and conditions for uniqueness.  
(b) Interpret the solution.  
(c) Write the KKT conditions when no short selling is allowed.

### Part (a) — Closed-form solution

The objective is concave when $Q$ is positive definite and $\gamma>0$. The Lagrangian is

$$
L(x,\eta)=\mu^Tx-\frac{\gamma}{2}x^TQx-\eta(\mathbf{1}^Tx-1).
$$

The first-order condition is

$$
\mu-\gamma Qx-\eta\mathbf{1}=0.
$$

Rearrange:

$$
\gamma Qx=\mu-\eta\mathbf{1}.
$$

Assuming $Q$ is invertible,

$$
x=\frac{1}{\gamma}Q^{-1}(\mu-\eta\mathbf{1}).
$$

Now use the budget constraint:

$$
\mathbf{1}^Tx=1.
$$

Substitute the formula for $x$:

$$
\frac{1}{\gamma}\mathbf{1}^TQ^{-1}(\mu-\eta\mathbf{1})=1.
$$

Define

$$
A=\mathbf{1}^TQ^{-1}\mu,
\quad
C=\mathbf{1}^TQ^{-1}\mathbf{1}.
$$

Then

$$
\frac{1}{\gamma}(A-\eta C)=1.
$$

So

$$
\eta=\frac{A-\gamma}{C}.
$$

Therefore

$$
\boxed{x^*=\frac{1}{\gamma}Q^{-1}\left(\mu-\frac{A-\gamma}{C}\mathbf{1}\right).}
$$

An equivalent and more interpretable form is

$$
\boxed{x^*=\frac{Q^{-1}\mathbf{1}}{\mathbf{1}^TQ^{-1}\mathbf{1}}+rac{1}{\gamma}\left[Q^{-1}\mu-\frac{\mathbf{1}^TQ^{-1}\mu}{\mathbf{1}^TQ^{-1}\mathbf{1}}Q^{-1}\mathbf{1}\right].}
$$

This solution is well-defined and unique if $Q$ is symmetric positive definite and $\gamma>0$.

### Part (b) — Interpretation

The first term

$$
\frac{Q^{-1}\mathbf{1}}{\mathbf{1}^TQ^{-1}\mathbf{1}}
$$

is the global minimum-variance portfolio.

The second term is a zero-budget tilt toward assets with better expected returns after adjusting for covariance. The risk-aversion coefficient $\gamma$ controls the size of this tilt:

- large $\gamma$ means high risk aversion, so the tilt is small;
- small $\gamma$ means low risk aversion, so the tilt is large.

### Part (c) — No short selling KKT conditions

With no short selling, add

$$
x\ge 0.
$$

It is easier to write KKT conditions by converting the maximization to minimization:

$$
\min_x \ \frac{\gamma}{2}x^TQx-\mu^Tx
\quad\text{s.t.}\quad
\mathbf{1}^Tx=1,
\quad x\ge 0.
$$

Use $\eta$ for the equality constraint and $\nu\ge 0$ for $x\ge 0$. The Lagrangian is

$$
L(x,\eta,\nu)=\frac{\gamma}{2}x^TQx-\mu^Tx+\eta(\mathbf{1}^Tx-1)-\nu^Tx.
$$

The KKT conditions are

$$
\boxed{\gamma Qx-\mu+\eta\mathbf{1}-\nu=0}
$$

$$
\boxed{\mathbf{1}^Tx=1}
$$

$$
\boxed{x\ge 0,\quad \nu\ge 0}
$$

$$
\boxed{\nu_i x_i=0\quad \text{for every } i.}
$$

---

## Problem 5 — Robust optimization KKT check

### Question

Same robust optimization question as in 2023 Problem 6.

### Answer and explanation

The calculation is the same. With

$$
Q=
\begin{bmatrix}
0.0049 & 0.001 \\
0.001 & 0.0025
\end{bmatrix},
\quad
\Theta=\frac{Q}{20},
\quad
x=
\begin{bmatrix}
0.425 \\
0.575
\end{bmatrix},
$$

and assuming the target-return constraint is active, we get

$$
y=0.00925.
$$

Then

$$
y^2=0.0000855625,
$$

whereas

$$
x^T\Theta x=0.00011001875.
$$

Since

$$
y^2<x^T\Theta x,
$$

the ellipsoidal constraint is violated. The point is not feasible, so it cannot satisfy the KKT conditions.

Final answer:

$$
\boxed{\text{No, the proposed portfolio does not satisfy KKT.}}
$$

---

## Problem 6 — Risk contribution and log-barrier risk parity

### Question

Consider

$$
f(x)=\sqrt{x^TQx}-\lambda\mu^Tx.
$$

Also consider

$$
\begin{aligned}
\min_y\quad & \frac12 y^TQy-\lambda\mu^Ty-c\sum_{i=1}^n b_i\ln(y_i) \\
\text{s.t.}\quad & y\ge 0,
\end{aligned}
$$

where $\lambda>0$, $c>0$, and $b_i>0$.

(a) Derive each asset's individual risk contribution to $f(x)$.  
(b) Use the optimization model to relate the risk contribution of asset $i$ to asset $j$ at optimality.

### Part (a) — Individual risk contribution

A common definition of contribution is

$$
\text{contribution of asset } i = x_i\frac{\partial f}{\partial x_i}.
$$

First compute the derivative of the volatility term:

$$
\sqrt{x^TQx}=(x^TQx)^{1/2}.
$$

Using the chain rule:

$$
\frac{\partial}{\partial x_i}\sqrt{x^TQx}
=\frac{(Qx)_i}{\sqrt{x^TQx}}.
$$

The derivative of $-\lambda\mu^Tx$ with respect to $x_i$ is

$$
-\lambda\mu_i.
$$

Therefore

$$
\frac{\partial f}{\partial x_i}=\frac{(Qx)_i}{\sqrt{x^TQx}}-\lambda\mu_i.
$$

Thus the individual contribution is

$$
\boxed{RC_i(x)=x_i\left(\frac{(Qx)_i}{\sqrt{x^TQx}}-\lambda\mu_i\right).}
$$

If the course uses risk contribution only for the volatility term, then the volatility-only risk contribution is

$$
\boxed{RC_i^{\text{vol}}(x)=\frac{x_i(Qx)_i}{\sqrt{x^TQx}}.}
$$

### Part (b) — Relation at optimality

The log term forces $y_i>0$ at the optimum, because $\ln(y_i)$ is undefined at zero and goes to $-\infty$ as $y_i\downarrow 0$. So we can use first-order conditions directly.

The objective is

$$
\frac12 y^TQy-\lambda\mu^Ty-c\sum_{i=1}^n b_i\ln(y_i).
$$

Differentiate with respect to $y_i$:

$$
(Qy)_i-\lambda\mu_i-\frac{cb_i}{y_i}=0.
$$

Rearrange:

$$
(Qy)_i-\lambda\mu_i=\frac{cb_i}{y_i}.
$$

Multiply by $y_i$:

$$
y_i\left((Qy)_i-\lambda\mu_i\right)=cb_i.
$$

Therefore

$$
\frac{y_i\left((Qy)_i-\lambda\mu_i\right)}{b_i}=c.
$$

For any two assets $i$ and $j$:

$$
\boxed{
\frac{y_i\left((Qy)_i-\lambda\mu_i\right)}{b_i}
=
\frac{y_j\left((Qy)_j-\lambda\mu_j\right)}{b_j}.
}
$$

This says the budget-adjusted contributions are equal at the optimum.

---

## Problem 7 — Why optimize VaR or CVaR, and role of $F_\alpha(x,\gamma)$

### Question

(a) Why optimize VaR or CVaR?  
(b) Define and explain the role of $F_\alpha(x,\gamma)$.

### Part (a) — Why optimize VaR or CVaR?

Variance treats upside and downside deviations symmetrically. In risk management, investors often care more about large losses than large gains. VaR and CVaR focus on the loss tail.

VaR answers a quantile question. For example, 95% VaR is the loss level that is exceeded only 5% of the time.

CVaR answers a more conservative tail-average question. It asks: conditional on being in the worst tail, what is the average loss?

CVaR is usually more useful for optimization because it has a tractable convex formulation in scenario models, while VaR can be nonconvex and harder to optimize.

### Part (b) — Role of $F_\alpha(x,\gamma)$

Let $L(x,Y)$ denote the loss for decision $x$ under random scenario $Y$. The function

$$
F_\alpha(x,\gamma)
=
\gamma+rac{1}{1-\alpha}\mathbb{E}\left[(L(x,Y)-\gamma)^+\right]
$$

is an auxiliary function used to compute CVaR.

Here

$$
(a)^+=\max(a,0).
$$

The variable $\gamma$ plays the role of a candidate VaR threshold. If a scenario loss is below $\gamma$, it contributes nothing to the excess-loss term. If it is above $\gamma$, only the excess above $\gamma$ contributes.

In a finite scenario model with $S$ equally weighted scenarios, this becomes

$$
F_\alpha(x,\gamma)
=
\gamma+rac{1}{(1-\alpha)S}\sum_{s=1}^S z_s,
$$

where

$$
z_s\ge L(x,y_s)-\gamma,
\quad
z_s\ge 0.
$$

Minimizing $F_\alpha(x,\gamma)$ over $\gamma$ gives CVaR:

$$
\operatorname{CVaR}_\alpha(x)=\min_\gamma F_\alpha(x,\gamma).
$$

Any minimizing $\gamma$ is a VaR value. This is why $F_\alpha$ is important: it converts tail-risk minimization into a form that can be optimized with linear or convex programming methods.

---

## Problem 8 — Primal-dual interior-point method

### Question

Consider

$$
\begin{aligned}
\min_x\quad & f(x) \\
\text{s.t.}\quad & Ax=b, \\
& x\ge 0,
\end{aligned}
$$

where $f$ is differentiable.

(a) Formulate the barrier problem and derive KKT conditions.  
(b) Write the Newton system for a primal-dual interior-point search direction.  
(c) State requirements on $f$ for the Newton system to be well-defined and give a descent direction.

### Part (a) — Barrier problem

The inequality $x\ge 0$ is handled by adding a logarithmic barrier. For barrier parameter $\tau>0$, solve

$$
\begin{aligned}
\min_x\quad & f(x)-\tau\sum_{i=1}^n\ln(x_i) \\
\text{s.t.}\quad & Ax=b, \\
& x>0.
\end{aligned}
$$

The logarithm forces the iterate to stay inside the feasible region because $\ln(x_i)$ is undefined for $x_i\le 0$ and goes to $-\infty$ as $x_i\downarrow 0$.

The Lagrangian is

$$
L(x,\lambda)=f(x)-\tau\sum_{i=1}^n\ln(x_i)+\lambda^T(Ax-b).
$$

The KKT conditions are

$$
\nabla f(x)+A^T\lambda-\tau X^{-1}e=0,
$$

$$
Ax=b,
$$

$$
x>0.
$$

Here $X=\operatorname{diag}(x)$.

### Part (b) — Primal-dual Newton system

Introduce a positive dual/slack vector $s>0$ so that

$$
s=\tau X^{-1}e.
$$

Equivalently,

$$
Xs=\tau e.
$$

The primal-dual system is

$$
\nabla f(x)+A^T\lambda-s=0,
$$

$$
Ax=b,
$$

$$
Xs=\tau e.
$$

Linearizing this system gives the Newton equations:

$$
\begin{bmatrix}
H & A^T & -I \\
A & 0 & 0 \\
S & 0 & X
\end{bmatrix}
\begin{bmatrix}
\Delta x \\
\Delta \lambda \\
\Delta s
\end{bmatrix}
= -
\begin{bmatrix}
\nabla f(x)+A^T\lambda-s \\
Ax-b \\
Xs-\tau e
\end{bmatrix},
$$

where

$$
H=\nabla^2 f(x),
\quad
X=\operatorname{diag}(x),
\quad
S=\operatorname{diag}(s).
$$

Solving this system gives the search direction $(\Delta x,\Delta\lambda,\Delta s)$.

### Part (c) — Requirements on $f$

For this Newton system to be well-defined, $f$ should be twice continuously differentiable so that $\nabla^2 f(x)$ exists and changes smoothly.

For the direction to be a descent direction in a convex optimization setting, $f$ should be convex, meaning

$$
\nabla^2 f(x)\succeq 0.
$$

For uniqueness and nonsingularity, one typically wants positive curvature on the feasible directions, meaning $\nabla^2 f(x)$ is positive definite on the nullspace of $A$, together with $x>0$ and $s>0$.

---

# 2025 Final Exam

## Problem 1 — Rebalancing with only three stocks changed

### Question

You have an eight-stock portfolio with current weights

$$
(0.12,0.15,0.13,0.10,0.20,0.10,0.12,0.08),
$$

and Markowitz target weights

$$
(0.02,0.05,0.25,0.06,0.18,0.10,0.22,0.12).
$$

You want to rebalance on only three stocks and minimize

$$
|x_1-0.02|+|x_2-0.05|+|x_3-0.25|+\cdots+|x_8-0.12|.
$$

Formulate the most tractable optimization model in complete detail without summation notation.

### Answer and explanation

This is a mixed-integer linear program. It is mixed-integer because we must choose which three stocks can change. It is linear because the absolute values can be linearized using auxiliary variables.

Define:

- $x_i$ = new weight in stock $i$.
- $d_i$ = absolute deviation from the Markowitz target for stock $i$.
- $z_i\in\{0,1\}$ = 1 if stock $i$ is allowed to be rebalanced, 0 otherwise.

Current weights are

$$
a=(0.12,0.15,0.13,0.10,0.20,0.10,0.12,0.08).
$$

Markowitz target weights are

$$
m=(0.02,0.05,0.25,0.06,0.18,0.10,0.22,0.12).
$$

The objective is

$$
\min \ d_1+d_2+d_3+d_4+d_5+d_6+d_7+d_8.
$$

Budget and long-only constraints:

$$
x_1+x_2+x_3+x_4+x_5+x_6+x_7+x_8=1,
$$

$$
0\le x_1\le 1,
\quad
0\le x_2\le 1,
\quad
0\le x_3\le 1,
\quad
0\le x_4\le 1,
$$

$$
0\le x_5\le 1,
\quad
0\le x_6\le 1,
\quad
0\le x_7\le 1,
\quad
0\le x_8\le 1.
$$

Absolute-value linearization:

$$
d_1\ge x_1-0.02,
\quad
d_1\ge 0.02-x_1,
$$

$$
d_2\ge x_2-0.05,
\quad
d_2\ge 0.05-x_2,
$$

$$
d_3\ge x_3-0.25,
\quad
d_3\ge 0.25-x_3,
$$

$$
d_4\ge x_4-0.06,
\quad
d_4\ge 0.06-x_4,
$$

$$
d_5\ge x_5-0.18,
\quad
d_5\ge 0.18-x_5,
$$

$$
d_6\ge x_6-0.10,
\quad
d_6\ge 0.10-x_6,
$$

$$
d_7\ge x_7-0.22,
\quad
d_7\ge 0.22-x_7,
$$

$$
d_8\ge x_8-0.12,
\quad
d_8\ge 0.12-x_8,
$$

$$
d_1,d_2,d_3,d_4,d_5,d_6,d_7,d_8\ge 0.
$$

Now force $x_i$ to equal the current weight $a_i$ unless $z_i=1$. Since all weights lie between 0 and 1, we can use big-$M=1$:

$$
x_1-0.12\le z_1,
\quad
0.12-x_1\le z_1,
$$

$$
x_2-0.15\le z_2,
\quad
0.15-x_2\le z_2,
$$

$$
x_3-0.13\le z_3,
\quad
0.13-x_3\le z_3,
$$

$$
x_4-0.10\le z_4,
\quad
0.10-x_4\le z_4,
$$

$$
x_5-0.20\le z_5,
\quad
0.20-x_5\le z_5,
$$

$$
x_6-0.10\le z_6,
\quad
0.10-x_6\le z_6,
$$

$$
x_7-0.12\le z_7,
\quad
0.12-x_7\le z_7,
$$

$$
x_8-0.08\le z_8,
\quad
0.08-x_8\le z_8.
$$

If $z_i=0$, these two inequalities force $x_i=a_i$. If $z_i=1$, the inequalities do not restrict $x_i$ beyond the usual $0\le x_i\le 1$ bounds.

Allow at most three changes:

$$
z_1+z_2+z_3+z_4+z_5+z_6+z_7+z_8\le 3.
$$

Finally,

$$
z_1,z_2,z_3,z_4,z_5,z_6,z_7,z_8\in\{0,1\}.
$$

If the professor interprets “only three stocks” as exactly three, replace $\le 3$ with $=3$. The more standard interpretation is “at most three.”

---

## Problem 2 — LP dual and simplex

### Question

Consider

$$
\begin{aligned}
\max\quad & 3x_1+5x_2+2x_3 \\
\text{s.t.}\quad
& 2x_1+x_2+x_3\le 10, \\
& x_1+3x_2+2x_3\le 15, \\
& x_1,x_2,x_3\ge 0.
\end{aligned}
$$

(a) Write the dual.  
(b) Solve the primal using simplex.  
(c) Show the dual is optimal at termination.  
(d) Show that the search direction after the first iteration satisfies $Ad=0$, and explain why this matters.  
(e) Show that the dual solution after the first iteration is infeasible, but complementary slackness holds.

### Part (a) — Dual

This primal is a maximization problem with $\le$ constraints and nonnegative variables. The dual is a minimization problem with $\ge$ constraints and nonnegative dual variables.

Let $y_1,y_2\ge 0$ be the dual variables. The dual is

$$
\begin{aligned}
\min\quad & 10y_1+15y_2 \\
\text{s.t.}\quad
& 2y_1+y_2\ge 3, \\
& y_1+3y_2\ge 5, \\
& y_1+2y_2\ge 2, \\
& y_1,y_2\ge 0.
\end{aligned}
$$

### Part (b) — Simplex solution

Add slack variables:

$$
2x_1+x_2+x_3+s_1=10,
$$

$$
x_1+3x_2+2x_3+s_2=15.
$$

Initial solution:

$$
(x_1,x_2,x_3,s_1,s_2)=(0,0,0,10,15).
$$

For a maximization problem, the variable with the largest positive objective coefficient is a natural entering variable. Here $x_2$ has coefficient $5$, so let $x_2$ enter.

If $x_2$ increases by $\theta$:

$$
s_1=10-\theta,
$$

$$
s_2=15-3\theta.
$$

The ratio test gives

$$
\theta\le \min\left\{10,\frac{15}{3}\right\}=5.
$$

So $s_2$ leaves and $x_2=5$. The new basic feasible solution is

$$
(x_1,x_2,x_3,s_1,s_2)=(0,5,0,5,0).
$$

The objective value is

$$
5(5)=25.
$$

Now the basis is $\{s_1,x_2\}$. The reduced costs show that $x_1$ should enter next. Solving the resulting pivot gives the next basic feasible solution

$$
(x_1,x_2,x_3,s_1,s_2)=(3,4,0,0,0).
$$

The objective value is

$$
3(3)+5(4)+2(0)=29.
$$

At this point the reduced costs satisfy the simplex optimality test, so

$$
\boxed{x^*=(3,4,0)^T}
$$

and

$$
\boxed{\text{optimal value}=29.}
$$

### Part (c) — Dual optimality at termination

At the final basis $\{x_1,x_2\}$,

$$
B=
\begin{bmatrix}
2 & 1 \\
1 & 3
\end{bmatrix},
\quad
c_B=
\begin{bmatrix}
3 \\
5
\end{bmatrix}.
$$

The dual vector is

$$
y^T=c_B^TB^{-1}.
$$

Compute it:

$$
y^T=\left(\frac45,\frac75\right).
$$

Check dual constraints:

$$
2y_1+y_2=2\left(\frac45\right)+\frac75=3,
$$

$$
y_1+3y_2=\frac45+3\left(\frac75\right)=5,
$$

$$
y_1+2y_2=\frac45+2\left(\frac75\right)=\frac{18}{5}\ge 2.
$$

So $y$ is dual feasible. Its objective value is

$$
10\left(\frac45\right)+15\left(\frac75\right)=8+21=29.
$$

This equals the primal value. Therefore the final primal and dual solutions are both optimal.

### Part (d) — Search direction after the first iteration

After the first pivot, the basis is $\{s_1,x_2\}$. In the variable order $(x_1,x_2,x_3,s_1,s_2)$, let $x_1$ enter.

The basis matrix is

$$
B=
\begin{bmatrix}
1 & 1 \\
0 & 3
\end{bmatrix}.
$$

The entering column for $x_1$ is

$$
a_1=\begin{bmatrix}2\\1\end{bmatrix}.
$$

Compute

$$
B^{-1}a_1=
\begin{bmatrix}
5/3 \\
1/3
\end{bmatrix}.
$$

When $x_1$ increases by one unit, the basic variables change by minus this vector. Therefore the full direction is

$$
\boxed{d=\left(1,-\frac13,0,-\frac53,0\right)^T.}
$$

Check that it keeps the equality constraints satisfied. Let $\bar A$ be the full constraint matrix including slack columns:

$$
\bar A=
\begin{bmatrix}
2 & 1 & 1 & 1 & 0 \\
1 & 3 & 2 & 0 & 1
\end{bmatrix}.
$$

Then

$$
\bar A d=
\begin{bmatrix}
2(1)+1(-1/3)+1(0)+1(-5/3)+0(0) \\
1(1)+3(-1/3)+2(0)+0(-5/3)+1(0)
\end{bmatrix}
=
\begin{bmatrix}
0 \\
0
\end{bmatrix}.
$$

This matters because if $\bar A d=0$, then for any step length $\theta$,

$$
\bar A(x+\theta d)=\bar Ax+\theta \bar Ad=b.
$$

So moving along $d$ preserves the equality constraints. The only remaining issue is choosing $\theta$ small enough to keep all variables nonnegative.

### Part (e) — Dual after first iteration

After the first iteration, the basis is $\{s_1,x_2\}$. Then

$$
B=
\begin{bmatrix}
1 & 1 \\
0 & 3
\end{bmatrix},
\quad
c_B=\begin{bmatrix}0\\5\end{bmatrix}.
$$

Thus

$$
y^T=c_B^TB^{-1}=\left(0,\frac53\right).
$$

Check the dual constraint for $x_1$:

$$
2y_1+y_2=0+\frac53=\frac53.
$$

But the dual requires

$$
2y_1+y_2\ge 3.
$$

Since $5/3<3$, the dual solution is infeasible.

Complementary slackness still holds at this first-iteration primal-dual pair because:

- $x_2=5>0$, and the corresponding dual constraint is binding:

$$
y_1+3y_2=0+3\left(\frac53\right)=5.
$$

- $s_1=5>0$, and the corresponding dual variable is $y_1=0$.
- The other primal variables $x_1,x_3,s_2$ are zero, so their complementary-slackness products are automatically zero.

This illustrates an important point: complementary slackness alone is not enough for optimality. Dual feasibility is also required.

---

## Problem 3 — Rosenbrock and Newton convergence for a flat quartic

## Part 1 — Rosenbrock

### Question

For

$$
f(x_1,x_2)=100(x_2-x_1^2)^2+(1-x_1)^2,
$$

prove the unique global minimizer and apply two pure Newton iterations from $(0,0)^T$.

### Answer

As in the earlier Rosenbrock problems:

$$
\boxed{(1,1)^T \text{ is the unique global minimizer.}}
$$

The two Newton iterates from $x^{(0)}=(0,0)^T$ are

$$
\boxed{x^{(1)}=(1,0)^T,\qquad x^{(2)}=(1,1)^T.}
$$

## Part 2 — Newton method for $f(x)=(x-x_0)^4$

### Question

Let

$$
f(x)=(x-x_0)^4,
$$

where $x_0$ is constant. Apply Newton's method.

(a) Write the recurrence.  
(b) Show $y^{(k+1)}=\frac23 y^{(k)}$, where $y^{(k)}=|x^{(k)}-x_0|$.  
(c) Show convergence to $x_0$.  
(d) Show linear convergence.  
(e) Explain why convergence is not quadratic.

### Part (a) — Newton recurrence

Newton's method in one dimension is

$$
x^{(k+1)}=x^{(k)}-\frac{f'(x^{(k)})}{f''(x^{(k)})}.
$$

Compute derivatives:

$$
f'(x)=4(x-x_0)^3,
$$

$$
f''(x)=12(x-x_0)^2.
$$

For $x^{(k)}\ne x_0$,

$$
\frac{f'(x^{(k)})}{f''(x^{(k)})}
=
\frac{4(x^{(k)}-x_0)^3}{12(x^{(k)}-x_0)^2}
=
\frac13(x^{(k)}-x_0).
$$

Therefore

$$
x^{(k+1)}=x^{(k)}-\frac13(x^{(k)}-x_0).
$$

So

$$
\boxed{x^{(k+1)}=\frac23x^{(k)}+\frac13x_0.}
$$

### Part (b) — Error recurrence

Subtract $x_0$ from both sides:

$$
x^{(k+1)}-x_0=\frac23x^{(k)}+\frac13x_0-x_0.
$$

Simplify:

$$
x^{(k+1)}-x_0=\frac23(x^{(k)}-x_0).
$$

Taking absolute values gives

$$
y^{(k+1)}=|x^{(k+1)}-x_0|=\frac23|x^{(k)}-x_0|.
$$

Therefore

$$
\boxed{y^{(k+1)}=\frac23y^{(k)}.}
$$

### Part (c) — Convergence

Repeatedly applying the recurrence gives

$$
y^{(k)}=\left(\frac23\right)^ky^{(0)}.
$$

Because

$$
\left(\frac23\right)^k\to 0,
$$

we get

$$
y^{(k)}\to 0.
$$

Thus

$$
x^{(k)}\to x_0.
$$

So Newton's method converges to the minimizer from any initial guess other than the minimizer itself. If $x^{(0)}=x_0$, the method is already at the solution.

### Part (d) — Linear convergence

A sequence converges linearly if the error contracts by a constant factor $q$ with $0<q<1$:

$$
\frac{y^{(k+1)}}{y^{(k)}}\to q.
$$

Here

$$
\frac{y^{(k+1)}}{y^{(k)}}=\frac23.
$$

Therefore the convergence is linear with rate factor $2/3$:

$$
\boxed{\text{linear convergence with factor }2/3.}
$$

### Part (e) — Why not quadratic?

Quadratic convergence would require

$$
y^{(k+1)}\le C(y^{(k)})^2
$$

near the solution for some constant $C$.

But here

$$
y^{(k+1)}=\frac23y^{(k)}.
$$

Then

$$
\frac{y^{(k+1)}}{(y^{(k)})^2}
=
\frac{2/3}{y^{(k)}}.
$$

As $k\to\infty$, $y^{(k)}\to 0$, so this ratio goes to infinity. It does not stay bounded.

The deeper reason is that the minimizer is flat:

$$
f''(x_0)=0.
$$

Standard quadratic convergence of Newton's method requires a nonsingular second derivative at the solution. That condition fails here.

---

## Problem 4 — Mean-variance with a risk-free asset

### Question

There are $n$ risky assets and one risk-free asset with return $r_f$. The risky weights are $x$, and the risk-free weight is $x_{n+1}$. The model maximizes risk-adjusted return subject to a budget constraint:

$$
\max \ \mu^Tx+r_fx_{n+1}-\frac{\gamma}{2}x^TQx
$$

subject to

$$
\mathbf{1}^Tx+x_{n+1}=1.
$$

Find the closed-form solution and interpret it.

### Part (a) — Closed-form solution

Use the budget constraint to eliminate the risk-free weight:

$$
x_{n+1}=1-\mathbf{1}^Tx.
$$

Substitute into the objective:

$$
\mu^Tx+r_f(1-\mathbf{1}^Tx)-\frac{\gamma}{2}x^TQx.
$$

Simplify:

$$
r_f+(\mu-r_f\mathbf{1})^Tx-\frac{\gamma}{2}x^TQx.
$$

The constant $r_f$ does not affect the optimizer. Therefore maximize

$$
(\mu-r_f\mathbf{1})^Tx-\frac{\gamma}{2}x^TQx.
$$

The first-order condition is

$$
\mu-r_f\mathbf{1}-\gamma Qx=0.
$$

So

$$
\gamma Qx=\mu-r_f\mathbf{1}.
$$

Assuming $Q$ is invertible,

$$
\boxed{x^*=\frac{1}{\gamma}Q^{-1}(\mu-r_f\mathbf{1}).}
$$

The risk-free asset weight is then

$$
\boxed{x_{n+1}^*=1-\mathbf{1}^Tx^*.}
$$

The solution is well-defined and unique if $Q$ is symmetric positive definite and $\gamma>0$.

### Part (b) — Interpretation

The risky portfolio is proportional to the covariance-adjusted excess-return vector $Q^{-1}(\mu-r_f\mathbf{1})$.

The term $\mu-r_f\mathbf{1}$ is the vector of expected returns above the risk-free rate. The inverse covariance matrix adjusts these excess returns for risk and correlation.

The scalar $1/\gamma$ controls risk exposure:

- higher $\gamma$ means more risk aversion and smaller risky positions;
- lower $\gamma$ means less risk aversion and larger risky positions.

The risk-free asset absorbs whatever budget remains. If $\mathbf{1}^Tx^*>1$, then $x_{n+1}^*<0$, meaning the investor borrows at the risk-free rate to lever the risky portfolio.

---

## Problem 5 — Robust optimization True/False

### Question

Check whether the same proposed portfolio

$$
x=(0.425,0.575)^T
$$

satisfies the KKT conditions of the robust optimization problem.

### Answer and explanation

This is the same numerical check as in 2023 and 2024. The covariance matrix is

$$
Q=
\begin{bmatrix}
0.0049 & 0.001 \\
0.001 & 0.0025
\end{bmatrix}.
$$

With 20 observations,

$$
\Theta=\frac{Q}{20}.
$$

Assuming the target-return constraint is active gives

$$
y=0.00925.
$$

Then

$$
y^2=0.0000855625,
$$

but

$$
x^T\Theta x=0.00011001875.
$$

Since

$$
y^2<x^T\Theta x,
$$

the robust ellipsoid constraint is violated. Therefore the proposed point is not feasible.

So the True/False answer is

$$
\boxed{\text{False.}}
$$

It does not satisfy the KKT conditions.

---

## Problem 6 — Risk parity

### Question

Given the covariance matrix

$$
Q=
\begin{bmatrix}
0.0144 & 0.0144 & 0.0012 \\
0.0144 & 0.0400 & 0.0050 \\
0.0012 & 0.0050 & 0.0025
\end{bmatrix}
$$

and portfolio

$$
x=\begin{bmatrix}0.35\\0.10\\0.55\end{bmatrix},
$$

(a) determine whether $x$ is a risk parity portfolio.  
(b) formulate the simplest least-squares risk parity model using the actual numbers.  
(c) prove that the model is nonconvex.

### Part (a) — Check risk parity

For a volatility risk-parity portfolio, the unnormalized risk contribution of asset $i$ is

$$
x_i(Qx)_i.
$$

First compute $Qx$:

$$
Qx=
\begin{bmatrix}
0.007140 \\
0.011790 \\
0.002295
\end{bmatrix}.
$$

Now compute each contribution:

$$
RC_1=0.35(0.007140)=0.002499,
$$

$$
RC_2=0.10(0.011790)=0.001179,
$$

$$
RC_3=0.55(0.002295)=0.00126225.
$$

For risk parity, these contributions must be equal. They are not equal:

$$
0.002499\ne 0.001179\ne 0.00126225.
$$

Therefore

$$
\boxed{x \text{ is not a risk parity portfolio.}}
$$

### Part (b) — Least-squares risk parity model

Let $x_1,x_2,x_3$ be portfolio weights. The budget and long-only constraints are

$$
x_1+x_2+x_3=1,
$$

$$
x_1,x_2,x_3\ge 0.
$$

Define the unnormalized risk contributions:

$$
R_1=x_1(0.0144x_1+0.0144x_2+0.0012x_3),
$$

$$
R_2=x_2(0.0144x_1+0.0400x_2+0.0050x_3),
$$

$$
R_3=x_3(0.0012x_1+0.0050x_2+0.0025x_3).
$$

The least-squares risk-parity model minimizes pairwise differences in risk contributions:

$$
\begin{aligned}
\min \quad & (R_1-R_2)^2+(R_1-R_3)^2+(R_2-R_3)^2 \\
\text{s.t.}\quad
& x_1+x_2+x_3=1, \\
& x_1,x_2,x_3\ge 0.
\end{aligned}
$$

This model is “least complex” because it avoids extra logarithmic or nonlinear barrier terms and simply penalizes unequal risk contributions.

### Part (c) — Prove nonconvexity

To prove nonconvexity, it is enough to show that the Hessian of the objective is indefinite at some feasible point.

Use the budget constraint to eliminate $x_3$:

$$
x_3=1-x_1-x_2.
$$

Substitute into the objective and call the resulting two-variable function $\phi(x_1,x_2)$.

At the feasible point

$$
(x_1,x_2,x_3)=(1,0,0),
$$

the Hessian of $\phi$ with respect to $(x_1,x_2)$ is approximately

$$
\nabla^2\phi(1,0)=
\begin{bmatrix}
0.00463104 & 0.00132480 \\
0.00132480 & -0.00096768
\end{bmatrix}.
$$

Its determinant is

$$
(0.00463104)(-0.00096768)-(0.00132480)^2\approx -0.00000623646.
$$

A $2\times 2$ symmetric matrix with negative determinant has one positive and one negative eigenvalue. Therefore the Hessian is indefinite.

A twice differentiable convex function must have a positive semidefinite Hessian everywhere on the feasible region. Since this Hessian is indefinite at a feasible point, the least-squares risk-parity objective is not convex.

Thus

$$
\boxed{\text{the model is nonconvex.}}
$$

---

## Problem 7 — True/False

### Question

(a) Under the One Fund Theorem, all investors invest in the same risky asset in the same amount.  
(b) The role of $\gamma$ in $F_\alpha(x,\gamma)$ is to be a placeholder variable that ultimately becomes $\operatorname{VaR}_\alpha$.  
(c) In Black-Litterman, subjective views are assumed to be statistically dependent.  
(d) In Black-Litterman, the expected return vector is generated only through reverse optimization.

### Answers and explanation

#### (a) False

The One Fund Theorem says investors hold the same risky fund or risky portfolio, but they do not necessarily invest the same amount in it. The amount invested in the risky fund depends on risk aversion. One investor may hold more of the risky fund and less of the risk-free asset; another may hold less.

Therefore the statement is false because it says “same amount.”

#### (b) True

In the CVaR auxiliary function

$$
F_\alpha(x,\gamma)=\gamma+\frac{1}{1-\alpha}\mathbb{E}[(L(x,Y)-\gamma)^+],
$$

$\gamma$ is the threshold variable. When the function is minimized over $\gamma$, the optimal $\gamma$ is a VaR threshold.

Therefore the statement is true.

#### (c) False

Black-Litterman views can be modeled as dependent if the view covariance matrix has off-diagonal terms. But they are not necessarily assumed to be statistically dependent. A diagonal view-error covariance matrix corresponds to independent view errors.

The statement says they are assumed dependent, which is too strong. Therefore it is false.

#### (d) False

Black-Litterman starts from reverse-optimized equilibrium returns, but then combines those equilibrium returns with subjective views. The final expected-return vector is not obtained only through reverse optimization.

Therefore the statement is false.

---

## Problem 8 — Primal-dual interior-point method for $f(x)+g(x)$

### Question

Consider

$$
\begin{aligned}
\min_x\quad & f(x)+g(x) \\
\text{s.t.}\quad & Ax=b, \\
& x\ge 0,
\end{aligned}
$$

where $f$ and $g$ are differentiable.

(a) Formulate the barrier problem and KKT conditions.  
(b) Write the Newton system for the primal-dual interior-point search direction.  
(c) State requirements on $f$ and $g$.

### Part (a) — Barrier problem

The barrier problem is

$$
\begin{aligned}
\min_x\quad & f(x)+g(x)-\tau\sum_{i=1}^n\ln(x_i) \\
\text{s.t.}\quad & Ax=b, \\
& x>0.
\end{aligned}
$$

The KKT condition for stationarity is

$$
\nabla f(x)+\nabla g(x)+A^T\lambda-\tau X^{-1}e=0.
$$

Together with primal feasibility:

$$
Ax=b,
\quad
x>0.
$$

For the primal-dual form, introduce $s>0$:

$$
\nabla f(x)+\nabla g(x)+A^T\lambda-s=0,
$$

$$
Ax=b,
$$

$$
Xs=\tau e.
$$

### Part (b) — Newton system

Let

$$
H=\nabla^2 f(x)+\nabla^2 g(x).
$$

The Newton system is

$$
\begin{bmatrix}
H & A^T & -I \\
A & 0 & 0 \\
S & 0 & X
\end{bmatrix}
\begin{bmatrix}
\Delta x \\
\Delta \lambda \\
\Delta s
\end{bmatrix}
= -
\begin{bmatrix}
\nabla f(x)+\nabla g(x)+A^T\lambda-s \\
Ax-b \\
Xs-\tau e
\end{bmatrix}.
$$

This is the system solved at each interior-point iteration to obtain a direction for $x$, the equality multiplier $\lambda$, and the nonnegativity multiplier $s$.

### Part (c) — Requirements

The functions $f$ and $g$ should be twice continuously differentiable so the Hessian matrix exists.

For a convex optimization problem, the sum $f+g$ should be convex:

$$
\nabla^2 f(x)+\nabla^2 g(x)\succeq 0.
$$

For the Newton direction to be well-defined and descent-like, the Hessian should have enough positive curvature on the feasible directions, meaning on directions $d$ satisfying $Ad=0$. A common sufficient condition is that

$$
d^T\left(\nabla^2 f(x)+\nabla^2 g(x)\right)d>0
$$

for all nonzero feasible directions $d$ in the nullspace of $A$.

Also, the interior-point method requires

$$
x>0,
\quad
s>0,
$$

so that the logarithmic barrier and complementarity equations are well-defined.
