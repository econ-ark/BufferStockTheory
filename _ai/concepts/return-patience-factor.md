# Return Patience Factor (RPF)

## Defining equation

Anchor: [`ass-RIC`](../../BufferStockTheory.md#ass-RIC)

$$
\RPFac := \APFac/\Rfree
$$

*Ratio of the absolute patience factor to the gross interest factor.*

## Gloss

The return patience factor $\RPFac := \APFac/\Rfree$ is the patience-factor analogue of the consumer's preferred-consumption-growth-vs-return comparison. When $\RPFac < 1$ (RIC), the consumer's preferred consumption-growth factor $\APFac$ is below the gross interest factor $\Rfree$ — equivalently, the consumer is willing to forgo enough consumption today to let interest accumulate, so wealth is being drawn down rather than building up indefinitely.

RPF appears throughout the perfect-foresight benchmark results: the limiting marginal propensity to consume out of total wealth is $\MPCmin = 1 - \RPFac$, which is positive iff RIC holds; the natural-borrowing-constraint limiting consumption function is built from $\RPFac$-based recursions; and WRIC weakens RIC by adjusting the patience side (multiplying by $\pZero^{1/\CRRA}$) rather than the return side, which means WRIC is the inequality $\pZero^{1/\CRRA} \RPFac < 1$.

RPF is one of four patience factors sharing the same numerator $\APFac$ but differing in denominator. The other three: $\APFac$ itself (denominator $1$, gives AIC), $\GPFacRaw = \APFac/\PermGroFac$ (denominator $\PermGroFac$, gives GIC), and $\GPFacMod = \APFac/\PermGroFacAdj$ (denominator $\PermGroFacAdj$, the uncertainty-adjusted growth factor, gives GIC-Mod). RPF stands apart from the growth siblings by using $\Rfree$ — the *return* comparison rather than the growth comparison.

## Relations

- **requires** [absolute-patience-factor](absolute-patience-factor.md) — $\RPFac = \APFac/\Rfree$ is built from $\APFac$.
- **assumed-by** [return-impatience-condition](return-impatience-condition.md) — RIC is exactly the inequality $\RPFac < 1$.
- **assumed-by** [weak-return-impatience-condition](weak-return-impatience-condition.md) — WRIC is the probability-adjusted inequality $\pZero^{1/\CRRA} \RPFac < 1$.
- **contrasts-with** [growth-patience-factor](growth-patience-factor.md) — RPF and GPF share numerator $\APFac$ and differ in denominator: RPF uses $\Rfree$, GPF uses $\PermGroFac$.
- **contrasts-with** [no-ric-no-gic-implies-no-fvac](no-ric-no-gic-implies-no-fvac.md) — Mirror edge: the doubly-patient case $\RPFac\geq 1$ together with $\GPFacRaw\geq 1$ is precisely the configuration FVAC excludes (claim-noRICGIC); under FVAC at least one patience factor must be below one.

## Sources

- [BufferStockTheory.md#ass-RIC](../../BufferStockTheory.md#ass-RIC)
- [BufferStockTheory.md#RIC](../../BufferStockTheory.md#RIC)

## bellman-ddsl correspondence

> *Reserved field — the bellman-ddsl perch/stage mapping is **deferred** for every concept in this atlas; the cross-repo bridge has not been authored. This is not a delivered correspondence.*

- perch: `(deferred)`
- stage: `(deferred)`
