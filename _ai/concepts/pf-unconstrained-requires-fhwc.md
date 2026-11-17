# Perfect Foresight Unconstrained Solution Requires FHWC

## Defining equation

Anchor: [`prop-pfUCFHWC`](../../BufferStockTheory.md#prop-pfUCFHWC)

$$
\text{Non-degenerate limiting solution exists} \iff \RNrmByG^{-1}<1 \text{ (FHWC) and } \RPFac<1 \text{ (RIC)}
$$

*In the unconstrained perfect-foresight problem, a non-degenerate limiting consumption function exists if and only if both finite human wealth and return impatience hold.*

## Gloss

This proposition characterizes when the perfect-foresight problem *without* liquidity constraints (Assumption `ass-pfincome` in force) has a well-behaved limiting solution as the horizon recedes. The answer is an "if and only if": a non-degenerate limiting consumption function exists exactly when both the finite human wealth condition (FHWC, $\RNrmByG^{-1} = \PermGroFac/\Rfree < 1$) and the return impatience condition (RIC, $\RPFac < 1$) hold. Neither condition alone suffices; each rules out a distinct mode of degeneracy.

The two conditions guard against opposite pathologies. The proof (Appendix `subsec-ApndxUCPF`) writes the limiting consumption function as $\bar{\cFunc}(\mNrm) = (\mNrm + \hNrm - 1)\MPCmin$ with $\MPCmin = 1 - \RPFac$. RIC keeps the limiting marginal propensity to consume strictly positive, ruling out the degenerate solution $\bar{\cFunc}(\mNrm) = 0$ in which a pathologically patient consumer saves everything; FHWC keeps limiting normalized human wealth $\hNrm$ finite, ruling out the degenerate solution $\bar{\cFunc}(\mNrm) = \infty$ in which the consumer borrows against an unbounded present value of future income.

FHWC is *necessary* here precisely because there are no constraints: in the unconstrained problem only finite human wealth can prevent infinite borrowing in the limit. This is the sharp point of contrast with the liquidity-constrained sibling result (proposition `prop-PFCExist`), where a binding constraint prevents the infinite-borrowing pathology, so RIC alone (or, failing RIC, growth impatience) suffices and FHWC can be dispensed with.

## Relations

- **requires** [return-impatience-condition](return-impatience-condition.md) — RIC is one of the two jointly necessary-and-sufficient hypotheses; it keeps $\MPCmin = 1-\RPFac > 0$, ruling out the degenerate $\bar{\cFunc}=0$.
- **requires** [finite-human-wealth-condition](finite-human-wealth-condition.md) — FHWC is the other jointly necessary-and-sufficient hypothesis; it keeps $\hNrm$ finite, ruling out the degenerate $\bar{\cFunc}=\infty$.
- **contrasts-with** [pf-constrained-solution-exists](pf-constrained-solution-exists.md) — With a liquidity constraint (prop-PFCExist), the binding constraint prevents infinite borrowing, so RIC alone (or GIC if RIC fails) suffices and FHWC is not required.
- **requires** [`ass-pfincome`](../../BufferStockTheory.md#ass-pfincome) — The result is stated for the normalized perfect-foresight income process used to define human wealth.

## Sources

- [BufferStockTheory.md#prop-pfUCFHWC](../../BufferStockTheory.md#prop-pfUCFHWC)
- [BufferStockTheory.md#subsec-ApndxUCPF](../../BufferStockTheory.md#subsec-ApndxUCPF)
- [BufferStockTheory.md#eq-cFuncPFUncAppx](../../BufferStockTheory.md#eq-cFuncPFUncAppx)

## bellman-ddsl correspondence

> *Reserved field — the bellman-ddsl perch/stage mapping is **deferred** for every concept in this atlas; the cross-repo bridge has not been authored. This is not a delivered correspondence.*

- perch: `(deferred)`
- stage: `(deferred)`
