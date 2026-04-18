# Effect Size Formulas

- Rank-biserial (paired): `(n_positive - n_negative) / (n_positive + n_negative)`
- Paired Cohen `d_z`: `mean(diff) / sd(diff)`
- Hedges `g_z`: `J(df) * d_z`, with `J(df) = 1 - 3/(4*df-1)`
- McNemar conditional OR: transform discordant probability `p = b/(b+c)` as `OR = p/(1-p)` and invert exact binomial bounds for CI.
