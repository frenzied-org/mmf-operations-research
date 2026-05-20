# Homework 1 understanding notes

These notes are meant to help you understand the modeling ideas behind the
homework, not just copy the final answers.  The common theme is linear
programming.  A linear program is an optimization problem where the objective
function and every constraint are linear.  Linear means each variable appears
only to the first power, with no products of variables, no square roots, no
absolute values, and no if-statements inside the model.

For almost every problem, the modeling workflow is the same:

1. Decide what the decision variables are.
2. Write the objective: what are we minimizing or maximizing?
3. Write the constraints: what must be true?
4. Check units: dollars, shares, hours, flights, inventory units.
5. Check signs: costs should subtract from profit, limits should point the
   right way, and balances should conserve flow.

## Problem 1: selling stocks while preserving future value

### What the problem is asking

You own 100 shares of each of 10 stocks.  You need to sell some shares today so
that, after taxes and transaction costs, you keep exactly $\$30{,}000$ in cash.
The goal is to keep as much expected one-year portfolio value as possible.

The important phrase is "fractional share."  That tells us the decision
variables can be continuous numbers, not just integers.  For example, selling
63.750749 shares is allowed.

### Decision variables

Let

$$
x_i = \text{shares sold of stock } i.
$$

Since you own 100 shares of each stock,

$$
0 \leq x_i \leq 100.
$$

### Cash from selling one share

If a stock has:

- purchase price $p_i$,
- current price $c_i$,
- expected one-year price $f_i$,

then selling one share gives current sale revenue $c_i$.

But you do not keep all of that.  You pay:

$$
\text{tax per share}
= 0.30(c_i - p_i),
$$

and

$$
\text{transaction cost per share}
= 0.01c_i.
$$

So the net cash kept per share is

$$
\text{net}_i
= c_i - 0.30(c_i - p_i) - 0.01c_i.
$$

That is the coefficient in the cash constraint.

### Objective

If you sell one share of stock $i$, you give up expected future value $f_i$.
If you sell $x_i$ shares, you give up $f_i x_i$.

The original portfolio is fixed, so there are two equivalent ways to write the
objective:

- maximize expected value remaining;
- minimize expected value sold.

The second version is simpler:

$$
\min \sum_{i=1}^{10} f_i x_i.
$$

### Constraint

You must raise exactly $\$30{,}000$ after taxes and transaction costs:

$$
\sum_{i=1}^{10} \text{net}_i x_i = 30000.
$$

### Intuition for the answer

The model sells stocks where the expected future price is low relative to the
cash they generate today.  In other words, it prefers to sell shares that give
you a lot of cash now while sacrificing relatively little expected future value.

The optimal solution sells all shares of stocks 3, 4, 8, 9, and 10, plus part
of stock 6.  It keeps all shares of stocks 1, 2, 5, and 7.

## Problem 2: turning a nonlinear problem into a linear program

### What makes it look nonlinear

The original problem contains $x_2^2$.  A squared variable is not linear, so at
first the problem does not look like a linear program.

The key observation is that the squared term appears in a very special way:

$$
x_2^2 - x_3 = 0.
$$

This means

$$
x_2^2 = x_3.
$$

The objective also uses $x_2^2$, not $x_2$ by itself.  That lets us replace the
squared term with a new variable.

### Change of variables

Define

$$
y = x_2^2.
$$

Because $x_2 \geq 0$, any $y \geq 0$ can be matched with

$$
x_2 = \sqrt{y}.
$$

So we do not lose feasible solutions by replacing $x_2^2$ with $y$.

### New linear model

The objective

$$
2x_1 + x_2^2 + x_3
$$

becomes

$$
2x_1 + y + x_3.
$$

The equality constraint becomes

$$
y - x_3 = 0.
$$

The inequality

$$
5x_1 + 3x_3 \leq 5
$$

is already linear.

To put it in equality standard form, add a slack variable $s \geq 0$:

$$
5x_1 + 3x_3 + s = 5.
$$

### Main lesson

Not every nonlinear-looking problem is hopeless.  If the nonlinear expression
can be replaced by a new variable without changing the feasible set or
objective meaning, the problem may still be equivalent to a linear program.

## Problem 3: assigning workers to projects

### What the problem is asking

There are 4 workers and 4 projects.  Every worker must get one project, and
every project must get one worker.  The cost depends on how many hours the
assigned worker needs.

This is an assignment problem.  Assignment problems are often written with
0-1 variables.

### Decision variables

Let

$$
x_{ij}
= \begin{cases}
1, & \text{if worker } i \text{ is assigned to project } j,\\
0, & \text{otherwise.}
\end{cases}
$$

There are 16 variables because there are 4 workers and 4 projects.

### Objective

Let $h_{ij}$ be the hours worker $i$ needs for project $j$.  The cost per hour
is $\$20$, so assigning worker $i$ to project $j$ costs

$$
20h_{ij}.
$$

The objective is

$$
\min 20\sum_{i=1}^{4}\sum_{j=1}^{4} h_{ij}x_{ij}.
$$

### Constraints

Each worker gets exactly one project:

$$
\sum_{j=1}^{4} x_{ij} = 1,\quad i = 1,\ldots,4.
$$

Each project gets exactly one worker:

$$
\sum_{i=1}^{4} x_{ij} = 1,\quad j = 1,\ldots,4.
$$

The natural model has binary constraints:

$$
x_{ij} \in \{0,1\}.
$$

The homework asks for a linear program, so we relax this to

$$
0 \leq x_{ij} \leq 1.
$$

For this type of assignment model, the linear-programming relaxation often
returns an integer solution anyway.  That happens here.

### Intuition for the answer

The cheapest-looking individual assignments are not enough by themselves,
because two workers cannot take the same project.  The model searches for the
lowest total cost while respecting both sides of the matching.

The optimal assignment is:

- worker 1 to project 2;
- worker 2 to project 1;
- worker 3 to project 3;
- worker 4 to project 4.

The total cost is $\$460$.

## Problem 4: warehouse inventory trading

### What the problem is asking

The trader can buy, sell, and store a commodity over 12 months.  The warehouse
has limited capacity, and the trader must end the year with no inventory.

This is an inventory balance problem.  The central idea is conservation:

$$
\text{ending inventory}
= \text{starting inventory} + \text{bought} - \text{sold}.
$$

### Decision variables

For each month $t = 1,\ldots,12$, define:

- $b_t$: units bought at the start of month $t$;
- $q_t$: units sold at the start of month $t$;
- $I_t$: inventory after the month-$t$ buy or sell decision.

The initial inventory is fixed:

$$
I_0 = 2000.
$$

The final inventory requirement is

$$
I_{12} = 0.
$$

### Inventory balance

For every month,

$$
I_t = I_{t-1} + b_t - q_t.
$$

This single equation is the backbone of the model.

### Capacity

The warehouse can hold at most 10,000 units:

$$
0 \leq I_t \leq 10000.
$$

Buying and selling amounts cannot be negative:

$$
b_t \geq 0,\quad q_t \geq 0.
$$

### Objective

Revenue comes from selling:

$$
\sum_{t=1}^{12} s_t q_t.
$$

Cost comes from buying:

$$
\sum_{t=1}^{12} p_t b_t.
$$

There is also inventory cost.  In the solution, I used the convention that the
holding cost in month $t$ is charged on inventory carried into that month,
$I_{t-1}$.  So the inventory cost is

$$
\sum_{t=1}^{12} i_t I_{t-1}.
$$

The profit objective is

$$
\max
\sum_{t=1}^{12} s_t q_t
- \sum_{t=1}^{12} p_t b_t
- \sum_{t=1}^{12} i_t I_{t-1}.
$$

### Main lesson

When a problem talks about inventory, storage, cash, or network flow over time,
look for a balance equation.  Most of the model follows once the balance
equation is right.

## Problem 5: bond portfolio with reinvested surplus cash

### What the original bond problem does

The bank needs cash to meet liabilities in years 1, 2, and 3.  Bonds generate
cash flows in different years.  The goal is to buy the cheapest portfolio that
produces enough cash to pay the liabilities.

In the original example, each year's bond cash flow must directly cover that
year's liability.  If there is extra cash, the original formulation does not
track it.

### What changes in Problem 5

Problem 5 allows excess cash in one year to be reinvested for one period at 2%.
That means surplus cash is no longer ignored.  It can help pay the next year's
liability.

### Decision variables

Let:

- $x_1, x_2, x_3$ be units purchased of bonds 1, 2, and 3;
- $y_1$ be surplus cash after paying the year-1 liability;
- $y_2$ be surplus cash after paying the year-2 liability.

The surplus variables are important.  Without them, the model has no way to
carry excess cash forward.

### Year-by-year cash equations

Year 1 cash:

$$
105x_1 + 3.5x_2 + 3.5x_3.
$$

After paying the year-1 liability of $\$12{,}000$, leftover cash is $y_1$:

$$
105x_1 + 3.5x_2 + 3.5x_3 - y_1 = 12000.
$$

Year 2 cash comes from bond coupons and principal, plus reinvested year-1
surplus:

$$
103.5x_2 + 3.5x_3 + 1.02y_1.
$$

After paying the year-2 liability of $\$18{,}000$, leftover cash is $y_2$:

$$
103.5x_2 + 3.5x_3 + 1.02y_1 - y_2 = 18000.
$$

Year 3 cash comes from bond 3 and reinvested year-2 surplus:

$$
103.5x_3 + 1.02y_2 = 20000.
$$

### Objective

The bank pays for the bonds today:

$$
\min 102x_1 + 99x_2 + 98x_3.
$$

Surplus variables do not appear in the objective because they are not bought
directly.  They are created by excess bond cash flows.

### Intuition for the answer

Allowing reinvestment can reduce cost when early bond cash flows are cheap and
can be carried forward.  Here, the optimal solution has $y_1 = 0$ and $y_2 = 0$,
so the reinvestment option does not change the best cost.  That is still a
useful result: an option can be valuable in the model even if the optimizer
chooses not to use it for this data set.

## Problem 6: flights as a network flow problem

### What the problem is asking

Yorkville Airlines wants the maximum number of daily flights from Calgary to
Quebec City.  Every route must go:

$$
\text{Calgary} \to \text{Winnipeg} \to
\{\text{Montreal, Hamilton, Toronto}\} \to \text{Quebec City}.
$$

Each flight segment has a capacity.  Capacity means the maximum number of daily
flights allowed on that segment.

### Path variables

Instead of using one variable for every segment, we can use one variable for
each complete path:

- $m$: flights through Montreal;
- $h$: flights through Hamilton;
- $r$: flights through Toronto.

Then the total number of Calgary-to-Quebec-City flights is

$$
m + h + r.
$$

### Objective

The goal is to maximize total flights:

$$
\max m + h + r.
$$

### Constraints

All paths use Calgary to Winnipeg, so

$$
m + h + r \leq 5.
$$

The middle and final segments create path-specific limits:

$$
m \leq 4,\quad m \leq 2,
$$

for the Montreal path,

$$
h \leq 5,\quad h \leq 1,
$$

for the Hamilton path, and

$$
r \leq 2,\quad r \leq 3,
$$

for the Toronto path.

The variables are nonnegative:

$$
m,h,r \geq 0.
$$

### Intuition for the answer

The shared Calgary-to-Winnipeg segment allows at most 5 flights total, so no
solution can exceed 5.  The downstream path capacities allow:

- at most 2 flights through Montreal;
- at most 1 flight through Hamilton;
- at most 2 flights through Toronto.

Those add up to 5, so the upper bound is reachable:

$$
m = 2,\quad h = 1,\quad r = 2.
$$

The maximum number of daily flights is 5.

## How to recognize the pattern next time

| Problem type | What to look for | Usual variables | Usual constraints |
|---|---|---|---|
| Portfolio sale | Sell or keep quantities | Amount sold | Cash target, upper bounds |
| Linearization | Repeated nonlinear expression | New replacement variable | Equality tying variables together |
| Assignment | Match workers to jobs | 0-1 assignment variables | One worker per job, one job per worker |
| Inventory | Stock changes over time | Buy, sell, inventory | Inventory balance, capacity |
| Cash matching | Pay liabilities over time | Asset purchases, surplus cash | Year-by-year cash balance |
| Network flow | Move units through arcs or paths | Flow on arcs or paths | Capacity and conservation |

The most useful habit is to ask: what quantity am I choosing?  Once that is
clear, the objective and constraints usually become much easier to write.
