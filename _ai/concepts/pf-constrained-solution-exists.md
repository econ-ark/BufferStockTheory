# Existence of the Perfect Foresight Constrained Solution

## Defining equation

Anchor: [`prop-PFCExist`](../../BufferStockTheory.md#prop-PFCExist)

$$
\RPFac < 1 \implies \text{nondegenerate}; \quad \text{if } \RPFac \geq 1, \text{ then nondegenerate} \iff \GPFacRaw < 1
$$

*For the liquidity-constrained perfect foresight problem, return impatience suffices for a non-degenerate limiting solution; if return impatience fails, a non-degenerate solution exists if and only if growth impatience holds.*

## Gloss

This proposition characterizes when the *normalized perfect foresight problem with a liquidity constraint* ($\cNrm_t \leq \mNrm_t$) has a non-degenerate limiting solution. It splits into two regimes. If [return impatience](#RIC) (RIC, $\RPFac<1$) holds, a non-degenerate solution always exists. If RIC fails ($\RPFac\geq 1$), a non-degenerate solution exists if and only if [growth impatience](#GICRaw) (GIC, $\GPFacRaw<1$) holds.

The role of GIC here is that the liquidity constraint is *relevant* exactly when GIC holds: at the lowest possible resource level $\mNrm_t=1$ the constraint binds iff the marginal-utility comparison $1^{-\CRRA} > \Rfree\DiscFac\PermGroFac^{-\CRRA}1^{-\CRRA}$ (Equation `eq-LiqConstrBinds`) holds, which is just a restatement of GIC. So when RIC fails, it is precisely the binding constraint, made relevant by GIC, that rules out the unbounded borrowing that would otherwise destroy the solution.

The result is notable because in the *unconstrained* perfect foresight problem (`prop-pfUCFHWC`) a non-degenerate solution exists if and only if both return impatience and finite human wealth (FHWC) hold, so each is necessary. Here, by contrast, FHWC may fail: when RIC fails ($\Rfree\leq\APFac$) and GIC holds ($\APFac<\PermGroFac$), FHWC also fails ($\Rfree\leq\PermGroFac$), yet the constraint prevents borrowing against unbounded human wealth, so for any finite $\mNrm$ the consumption function remains finite, strictly positive, and strictly increasing (with the MPC limiting to zero as $\mNrm\to\infty$). The proof is the case analysis of Section `subsec-PFCon`.

## Relations

- **implied-by** [return-impatience-condition](return-impatience-condition.md) — RIC alone is sufficient for a non-degenerate constrained solution (first clause); existence does not, however, require RIC, since GIC can substitute when RIC fails.
- **implied-by** [growth-impatience-condition](growth-impatience-condition.md) — When RIC fails, GIC is necessary and sufficient for a non-degenerate constrained solution (second clause).
- **contrasts-with** [pf-unconstrained-requires-fhwc](pf-unconstrained-requires-fhwc.md) — In the unconstrained PF problem (prop-pfUCFHWC) a non-degenerate solution requires both RIC and FHWC (iff); here RIC suffices and, failing RIC, GIC restores existence even though FHWC fails.
- **contrasts-with** [finite-human-wealth-condition](finite-human-wealth-condition.md) — Existence holds here even when FHWC fails ($\Rfree\leq\PermGroFac$), because the liquidity constraint blocks borrowing against unbounded human wealth.

## Sources

- [BufferStockTheory.md#prop-PFCExist](../../BufferStockTheory.md#prop-PFCExist)
- [BufferStockTheory.md#subsec-PFCon](../../BufferStockTheory.md#subsec-PFCon)
- [BufferStockTheory.md#eq-LiqConstrBinds](../../BufferStockTheory.md#eq-LiqConstrBinds)

## bellman-ddsl correspondence

> *Reserved field — the bellman-ddsl perch/stage mapping is **deferred** for every concept in this atlas; the cross-repo bridge has not been authored. This is not a delivered correspondence.*

- perch: `(deferred)`
- stage: `(deferred)`
