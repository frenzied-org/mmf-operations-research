# Homework Assignment 1 Questions

## Problem 1

Currently we own 100 shares each of stocks 1 through 10. The original price we paid for these stocks, today’s price, and the expected price in one year for each stock is shown in Table 76.

| Stock | Shares Owned | Purchase | Current | In One Year |
|-------|--------------|----------|---------|-------------|
| 1 | 100 | 20 | 30 | 36 |
| 2 | 100 | 25 | 34 | 39 |
| 3 | 100 | 30 | 43 | 42 |
| 4 | 100 | 35 | 47 | 45 |
| 5 | 100 | 40 | 49 | 51 |
| 6 | 100 | 45 | 53 | 55 |
| 7 | 100 | 50 | 60 | 63 |
| 8 | 100 | 55 | 62 | 64 |
| 9 | 100 | 60 | 64 | 66 |
| 10 | 100 | 65 | 66 | 70 |

| Parameter | Value |
|-----------|-------|
| Tax rate (%) | 0.3 |
| Transaction cost (%) | 0.01 |

We need money today and are going to sell some of our stocks. The tax rate on capital gains is 30%. If we sell 50 shares of stock 1, then we must pay tax of

$$
0.3 \cdot 50(30 - 20) = \$150.
$$

We must also pay transaction costs of 1% on each transaction. Thus, our sale of 50 shares of stock 1 would incur transaction costs of

$$
0.01 \cdot 50 \cdot 30 = \$15.
$$

After taxes and transaction costs, we must be left with \$30,000 from our stock sales. Our goal is to maximize the expected before-tax value in one year of our remaining stock.

**What stocks should we sell?** Assume it is all right to sell a fractional share of stock.

---

## Problem 2 — Exercise 1.3

Can the following optimization problem be transformed to a linear program? If so, write the linear program in standard form.

$$
\begin{aligned}
\operatorname{minimize} \quad & 2x_1 + x_2^2 + x_3 \\
\operatorname{subject\ to} \quad & x_2^2 - x_3 = 0 \\
& 5x_1 + 3x_3 \leq 5 \\
& x_1 \geq 0,\; x_2 \geq 0,\; x_3 \geq 0
\end{aligned}
$$

---

## Problem 3 — Exercise 1.8

Suppose that there are 4 different projects and 4 workers, and each worker must be assigned a project and each project must be assigned a worker. It costs \$20 an hour for a worker. The following table gives the time required, in hours, for each worker $i$ to complete a particular project $j$:

|          | Project 1 | Project 2 | Project 3 | Project 4 |
|----------|-----------|-----------|-----------|-----------|
| Worker 1 | 7 | 3 | 6 | 10 |
| Worker 2 | 5 | 4 | 9 | 9 |
| Worker 3 | 6 | 4 | 7 | 10 |
| Worker 4 | 5 | 5 | 6 | 8 |

### (a)

Formulate this problem of assigning workers and jobs at minimum cost as a linear program.

### (b)

Solve the model in part (a) using the MATLAB `linprog` function. If you get a fractional optimal solution, find a feasible integer solution, meaning all variables are 0 or 1, with the same optimal objective function value.


## Problem 4 — Exercise 1.13

A warehouse can store 10,000 units of a certain commodity. A commodities trader has access to the warehouse and currently has 2,000 units of the commodity in storage.

At the start of each month $t$, for the next 12 months $(t = 1, \ldots, 12)$, the trader can buy an amount of the commodity at price $p_t$, subject to the capacity of the warehouse at the start of month $t$, or can sell an amount of the commodity at price $s_t$, subject to how much of the commodity is currently in the warehouse.

In addition, there is a unit inventory cost $i_t$ for holding the commodity in the warehouse, which is incurred at the start of month $t$.

The trader wishes to have no inventory of the commodity at the end of the year.

Formulate a linear program that maximizes profit from the buying or selling of the commodity over the 12-month time horizon.

---

## Example 1.9 — Bond Portfolio

A bank has the following liability schedule:

| Year | Liability |
|------|-----------:|
| 1 | 12,000 |
| 2 | 18,000 |
| 3 | 20,000 |

The bank wishes to use the three bonds below to form a portfolio today to hold until all bonds have matured and that will generate the required cash to meet the liabilities. All bonds have a face value of \$100 and the coupons are annual, with one coupon per year. For example, one unit of Bond 2 costs \$99 now and the holder will receive \$3.50 after 1 year and then \$3.50 plus the face value of \$100 at the end of the second year, which is the maturity of Bond 2.

| Bond | Price | Coupon | Maturity year |
|------|------:|-------:|--------------:|
| 1 | 102 | 5 | 1 |
| 2 | 99 | 3.5 | 2 |
| 3 | 98 | 3.5 | 3 |

Let $x_i$ be the amount of bond $i$ purchased. The minimum-cost portfolio can be formulated as

$$
\begin{aligned}
\min \quad & 102x_1 + 99x_2 + 98x_3 \\
\mathrm{subject\ to} \quad & 105x_1 + 3.5x_2 + 3.5x_3 \geq 12000 \\
& 103.5x_2 + 3.5x_3 \geq 18000 \\
& 103.5x_3 \geq 20000 \\
& x_1, x_2, x_3 \geq 0.
\end{aligned}
$$

The cash-flow interpretation is the same as in the source text: in year 1, Bond 1 contributes \$105 per unit, Bond 2 contributes \$3.50 per unit, and Bond 3 contributes \$3.50 per unit. In year 2, Bond 1 no longer contributes because it has matured, while Bond 2 contributes \$103.50 per unit and Bond 3 contributes \$3.50 per unit. In year 3, only Bond 3 contributes, with \$103.50 per unit.


## Problem 5 — Exercise 1.14

In Example 1.9, Bond Portfolio, suppose that one is allowed to invest in a portfolio of bonds such that the cash generated for a time period may exceed the amount of the liability for that time period.

Any excess cash generated is reinvested at an interest rate of 2% for one time period and can be used toward future liabilities. Assume that fractional investments in bonds are allowed.

Formulate this modified version of the Bond Portfolio problem as a linear program and solve in MATLAB.

Why would it be advantageous to allow excess cash generation and reinvestment?


## Problem 6 — Exercise 1.18

Yorkville Airlines has service from Calgary to each of the following cities: Winnipeg, Hamilton, Toronto, Montreal, and Quebec City.

As an operations research analyst for Yorkville Airlines, you have been asked to determine how many daily flights there should be from Calgary to Quebec City, with the condition that flights must connect via Winnipeg and then to either Hamilton, Montreal, or Toronto, and then finally to Quebec City.

It has already been determined by the government transportation bureau that Yorkville Airlines must have no more than the following flights for each connecting segment:

| City Pair | Maximum Number of Daily Flights |
|-----------|---------------------------------|
| Calgary to Winnipeg | 5 |
| Winnipeg to Montreal | 4 |
| Winnipeg to Hamilton | 5 |
| Winnipeg to Toronto | 2 |
| Montreal to Quebec City | 2 |
| Hamilton to Quebec City | 1 |
| Toronto to Quebec City | 3 |

Formulate this problem as a linear program and solve in MATLAB.