# Return Impatience Condition (RIC)

## Defining equation

Anchor: [`ass-RIC`](../../BufferStockTheory.md#ass-RIC)

$$
\RPFac < 1
$$

*The absolute patience factor falls short of the gross interest factor.*

## Gloss

RIC says the return patience factor $\RPFac := \APFac/\Rfree$ is below 1, i.e. the absolute patience factor $\APFac := (\Rfree\DiscFac)^{1/\CRRA}$ is smaller than the gross interest factor $\Rfree$.

Return impatience captures the tension between the income effect of capital income and the substitution effect: the marginal propensity to consume out of total (human plus nonhuman) wealth that would just maintain next-period wealth equals $\MPC = 1 - \APFac/\Rfree$, so RIC is exactly the condition that this MPC is positive. Without RIC, the consumer effectively wants to hold more wealth tomorrow than today, which together with infinite human wealth produces a degenerate limiting solution where consumption goes to zero.

In the perfect-foresight unconstrained problem, RIC together with finite human wealth (FHWC) is necessary and sufficient for a non-degenerate limiting solution (`pf-unconstrained-requires-fhwc`). RIC has a weaker form, WRIC, that adjusts for the probability of zero-income events; WRIC is the condition actually required by the stochastic-problem existence theorems.

## Relations

- **requires** [return-patience-factor](return-patience-factor.md) — RIC is exactly the inequality $\RPFac < 1$.
- **requires** [absolute-patience-factor](absolute-patience-factor.md) — Transitively: $\RPFac = \APFac/\Rfree$ is built from $\APFac$.
- **contrasts-with** [growth-impatience-condition](growth-impatience-condition.md) — RIC is about return (ratio to interest factor); GIC is about growth (ratio to permanent income growth factor).
- **implied-by** [finite-value-of-autarky](finite-value-of-autarky.md) — Under FHWC, FVAC implies RIC (claim-PFConspC, concept pf-consumption-function-properties).
- **implied-by** [pf-consumption-function-properties](pf-consumption-function-properties.md) — Reciprocal edge: under FHWC the perfect-foresight patience chain (claim-PFConspC) gives FVAC⇒RIC, so GICRaw+FHWC also delivers RIC ($\RPFac<1$).
- **assumed-by** [pf-unconstrained-requires-fhwc](pf-unconstrained-requires-fhwc.md) — Non-degenerate limiting solution exists iff FHWC and RIC both hold (prop-pfUCFHWC).
- **generalises** [weak-return-impatience-condition](weak-return-impatience-condition.md) — WRIC is a weaker form that adjusts the patience factor for zero-income probability.
- **contrasts-with** [contraction-mapping-consumption-bounds](contraction-mapping-consumption-bounds.md) — Mirror of contraction-mapping-consumption-bounds contrasts-with RIC: under RIC the minimal MPC is positive and the bounded Bellman operator is a single stationary contraction; under only WRIC it is time-varying.
- **contrasts-with** [nondegenerate-solution-existence](nondegenerate-solution-existence.md) — Mirror of nondegenerate-solution-existence contrasts-with RIC: under uncertainty only WRIC is needed for a non-degenerate solution, whereas RIC was necessary in the perfect-foresight benchmark.
- **contrasts-with** [consumption-function-c2-concave](consumption-function-c2-concave.md) — Mirror: the C2/concavity shape result is unconditional, but the minimal MPC it bounds is strictly positive only under RIC (per limiting-mpcs-lemma).
- **contrasts-with** [limiting-consumption-strictly-positive](limiting-consumption-strictly-positive.md) — Mirror edge: under RIC the inherited lower ray $\cFunc(\mNrm)\geq\MPCmin\mNrm$ with $\MPCmin>0$ already gives positivity; under only WRIC ($\MPCmin=0$) remark-cStatStrctPos needs a separate Bellman-equation argument for strict positivity.

## Sources

- [BufferStockTheory.md#RIC](../../BufferStockTheory.md#RIC)
- [BufferStockTheory.md#ass-RIC](../../BufferStockTheory.md#ass-RIC)

## bellman-ddsl correspondence

> *Reserved field — the bellman-ddsl perch/stage mapping is **deferred** for every concept in this atlas; the cross-repo bridge has not been authored. This is not a delivered correspondence.*

- perch: `(deferred)`
- stage: `(deferred)`
