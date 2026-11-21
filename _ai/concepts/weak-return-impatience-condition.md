# Weak Return Impatience Condition (WRIC)

## Defining equation

Anchor: [`ass-WRIC`](../../BufferStockTheory.md#ass-WRIC)

$$
\frac{\pZero^{1/\CRRA} \APFac}{\Rfree} < 1
$$

*The zero-income-probability-adjusted return patience factor is less than one.*

## Gloss

WRIC adjusts the return patience factor by the probability $\pZero$ of a zero-income realisation: $(\pZero^{1/\CRRA} \APFac)/\Rfree < 1$. Because $\pZero \leq 1$ implies $\pZero^{1/\CRRA} \leq 1$, RIC ($\APFac/\Rfree < 1$) always implies WRIC. The converse fails — WRIC is *strictly* weaker — whenever $\pZero < 1$: then $\pZero^{1/\CRRA} < 1$ opens a gap in which $\RPFac$ can sit at or above $1$ (RIC violated) while $\pZero^{1/\CRRA}\RPFac < 1$ still holds. Only in the degenerate case $\pZero = 1$ (no noncapital income) does $\pZero^{1/\CRRA} = 1$ and WRIC collapse onto RIC.

The role of $\pZero$ is technical: a consumer with zero end-of-period assets has probability $\pZero$ of receiving zero income next period, in which case $\mNrm_{t+1} = 0$ would yield $u(0) = -\infty$ under CRRA utility. WRIC is the precise weakening of RIC that handles this corner correctly. Crucially, WRIC does NOT approach irrelevance as $\pZero \to 0$: the limit of the natural-borrowing-constraint problem coincides with the artificial-constraint problem, not with the unconstrained one.

WRIC is the patience condition actually required by the stochastic existence theorems — both pseudo-target existence (`thm-MSSBalExists`) and individual-target existence (`thm-target`) take WRIC rather than the stronger RIC. It cannot be relaxed further without imposing an artificial liquidity constraint.

## Relations

- **requires** [return-patience-factor](return-patience-factor.md) — WRIC is the probability-adjusted inequality $\pZero^{1/\CRRA} \RPFac < 1$.
- **requires** [absolute-patience-factor](absolute-patience-factor.md) — Transitively: $\RPFac = \APFac/\Rfree$ is built from $\APFac$.
- **implied-by** [return-impatience-condition](return-impatience-condition.md) — RIC implies WRIC whenever $\pZero \in [0, 1]$. WRIC is the weaker form.
- **assumed-by** [pseudo-target](pseudo-target.md) — Pseudo-target existence theorem requires WRIC (with FVAC and GIC).
- **assumed-by** [buffer-stock-target](buffer-stock-target.md) — Buffer-stock target existence theorem requires WRIC (with FVAC and GIC-Mod).
- **contrasts-with** [ric-gives-stationary-contraction](ric-gives-stationary-contraction.md) — Mirror edge: under only WRIC the lower share $\MPCmin_{T-n}$ can drift to zero, forcing time-varying bounded operators; remark-ricstationary notes RIC instead buys a single fixed-share stationary contraction.

## Sources

- [BufferStockTheory.md#WRIC](../../BufferStockTheory.md#WRIC)
- [BufferStockTheory.md#ass-WRIC](../../BufferStockTheory.md#ass-WRIC)

## bellman-ddsl correspondence

> *Reserved field — the bellman-ddsl perch/stage mapping is **deferred** for every concept in this atlas; the cross-repo bridge has not been authored. This is not a delivered correspondence.*

- perch: `(deferred)`
- stage: `(deferred)`
