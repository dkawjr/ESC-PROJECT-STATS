# McNemar Exact Derivation

For discordant counts `b` and `c`, under the null each discordant pair is equally likely in either direction, so `X ~ Binomial(b+c, 0.5)`. The exact two-sided p-value is `2 * P(X <= min(b,c))`, truncated at 1.
