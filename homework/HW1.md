# Homework Assignment 1 Questions

## Problem 1

Currently we own 100 shares each of stocks 1 through 10. The original price we paid for these stocks, today’s price, and the expected price in one year for each stock is shown in Table 76.

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