# Homework 1 solution

### Gerard (Lezhi) Wu

## Problem 1

Let $x_i$ be the number of shares sold of stock $i$, for $i = 1,\ldots,10$.
The bounds are

$$
0 \leq x_i \leq 100.
$$

For each sold share, the net cash kept today is

$$
\text{net}_i
= c_i - 0.30(c_i - p_i) - 0.01c_i,
$$

where $p_i$ is the purchase price and $c_i$ is the current price.

The expected one-year value lost from selling $x_i$ shares is $f_i x_i$, where
$f_i$ is the expected price in one year.  The starting portfolio is fixed, so
maximizing the expected value left in the account is the same as minimizing the
expected value sold.

The linear program is

$$
\begin{aligned}
\min \quad & \sum_{i=1}^{10} f_i x_i \\
\text{subject to} \quad
& \sum_{i=1}^{10} \text{net}_i x_i = 30000, \\
& 0 \leq x_i \leq 100,\quad i = 1,\ldots,10.
\end{aligned}
$$

The optimal sales are:

| Stock | Shares sold | Shares remaining |
|---:|---:|---:|
| 1 | 0.000000 | 100.000000 |
| 2 | 0.000000 | 100.000000 |
| 3 | 100.000000 | 0.000000 |
| 4 | 100.000000 | 0.000000 |
| 5 | 0.000000 | 100.000000 |
| 6 | 63.750749 | 36.249251 |
| 7 | 0.000000 | 100.000000 |
| 8 | 100.000000 | 0.000000 |
| 9 | 100.000000 | 0.000000 |
| 10 | 100.000000 | 0.000000 |

These sales raise exactly $\$30{,}000.00$ after taxes and transaction costs.
The expected before-tax one-year value of the remaining portfolio is
$\$20{,}893.71$.

## Problem 2

Yes, the problem can be transformed into a linear program.

Define

$$
y = x_2^2.
$$

Because $x_2 \geq 0$, every $y \geq 0$ corresponds to $x_2 = \sqrt{y}$.  The
constraint $x_2^2 - x_3 = 0$ becomes

$$
y - x_3 = 0.
$$

The transformed problem is

$$
\begin{aligned}
\min \quad & 2x_1 + y + x_3 \\
\text{subject to} \quad
& y - x_3 = 0, \\
& 5x_1 + 3x_3 \leq 5, \\
& x_1, y, x_3 \geq 0.
\end{aligned}
$$

To write it in equality standard form, add a slack variable $s \geq 0$:

$$
\begin{aligned}
\min \quad & 2x_1 + y + x_3 \\
\text{subject to} \quad
& y - x_3 = 0, \\
& 5x_1 + 3x_3 + s = 5, \\
& x_1, y, x_3, s \geq 0.
\end{aligned}
$$

## Problem 3

### Part (a)

Let $x_{ij}$ equal 1 if worker $i$ is assigned to project $j$, and 0 otherwise.
The cost for an assignment is $\$20$ times the number of hours.

The linear program is

$$
\begin{aligned}
\min \quad
& 20 \sum_{i=1}^{4}\sum_{j=1}^{4} h_{ij}x_{ij} \\
\text{subject to} \quad
& \sum_{j=1}^{4} x_{ij} = 1,\quad i = 1,\ldots,4, \\
& \sum_{i=1}^{4} x_{ij} = 1,\quad j = 1,\ldots,4, \\
& 0 \leq x_{ij} \leq 1,\quad i,j = 1,\ldots,4.
\end{aligned}
$$

Here $h_{ij}$ is the number of hours required when worker $i$ does project $j$.

### Part (b)

The Python linear-programming solution already has 0-1 values:

| Worker | Assigned project | Hours | Cost |
|---:|---:|---:|---:|
| 1 | 2 | 3 | $\$60$ |
| 2 | 1 | 5 | $\$100$ |
| 3 | 3 | 7 | $\$140$ |
| 4 | 4 | 8 | $\$160$ |

The minimum total cost is

$$
60 + 100 + 140 + 160 = \$460.
$$

## Problem 4

Let:

- $b_t$ be units bought at the start of month $t$.
- $q_t$ be units sold at the start of month $t$.
- $I_t$ be inventory after the month-$t$ buying or selling decision.
- $I_0 = 2000$ be the initial inventory.

I use the timing convention that the inventory cost $i_t$ is charged on the
inventory carried into month $t$, namely $I_{t-1}$.  With that convention, the
linear program is

$$
\begin{aligned}
\max \quad
& \sum_{t=1}^{12} s_t q_t
- \sum_{t=1}^{12} p_t b_t
- \sum_{t=1}^{12} i_t I_{t-1} \\
\text{subject to} \quad
& I_t = I_{t-1} + b_t - q_t,\quad t = 1,\ldots,12, \\
& I_0 = 2000, \\
& I_{12} = 0, \\
& 0 \leq I_t \leq 10000,\quad t = 0,\ldots,12, \\
& b_t \geq 0,\quad q_t \geq 0,\quad t = 1,\ldots,12.
\end{aligned}
$$

If the course interprets the inventory cost as being charged after the
month-$t$ trade, replace $I_{t-1}$ in the objective with $I_t$.  The balance
constraints remain the same.

## Problem 5

Let:

- $x_i$ be units purchased of bond $i$.
- $y_1$ be excess cash after paying the year-1 liability.
- $y_2$ be excess cash after paying the year-2 liability.

The reinvestment rate is 2%, so one dollar of surplus becomes $1.02$ dollars
one year later.

The linear program is

$$
\begin{aligned}
\min \quad
& 102x_1 + 99x_2 + 98x_3 \\
\text{subject to} \quad
& 105x_1 + 3.5x_2 + 3.5x_3 - y_1 = 12000, \\
& 103.5x_2 + 3.5x_3 + 1.02y_1 - y_2 = 18000, \\
& 103.5x_3 + 1.02y_2 = 20000, \\
& x_1, x_2, x_3, y_1, y_2 \geq 0.
\end{aligned}
$$

The Python solution is:

| Variable | Value |
|---:|---:|
| $x_1$ | 102.265208 |
| $x_2$ | 167.378469 |
| $x_3$ | 193.236715 |
| $y_1$ | 0.000000 |
| $y_2$ | 0.000000 |

The minimum cost is $\$45{,}938.72$.

Allowing excess cash generation and reinvestment can help because surplus cash
in an early period is not wasted.  It earns interest and can pay later
liabilities.  For this data set, the optimal solution uses no surplus cash, so
reinvestment does not lower the minimum cost.

## Problem 6

Use path variables:

- $m$: flights from Calgary to Quebec City through Winnipeg and Montreal.
- $h$: flights from Calgary to Quebec City through Winnipeg and Hamilton.
- $r$: flights from Calgary to Quebec City through Winnipeg and Toronto.

The linear program is

$$
\begin{aligned}
\max \quad & m + h + r \\
\text{subject to} \quad
& m + h + r \leq 5 && \text{Calgary to Winnipeg}, \\
& m \leq 4 && \text{Winnipeg to Montreal}, \\
& h \leq 5 && \text{Winnipeg to Hamilton}, \\
& r \leq 2 && \text{Winnipeg to Toronto}, \\
& m \leq 2 && \text{Montreal to Quebec City}, \\
& h \leq 1 && \text{Hamilton to Quebec City}, \\
& r \leq 3 && \text{Toronto to Quebec City}, \\
& m,h,r \geq 0.
\end{aligned}
$$

The optimal schedule is:

| Path | Daily flights |
|---|---:|
| Calgary-Winnipeg-Montreal-Quebec City | 2 |
| Calgary-Winnipeg-Hamilton-Quebec City | 1 |
| Calgary-Winnipeg-Toronto-Quebec City | 2 |

The maximum number of daily flights from Calgary to Quebec City is 5.
