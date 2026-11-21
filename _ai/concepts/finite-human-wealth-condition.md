# Finite Human Wealth Condition (FHWC)

## Defining equation

Anchor: [`ass-FHWC`](../../BufferStockTheory.md#ass-FHWC)

$$
\RNrmByG^{-1} = \PermGroFac/\Rfree < 1
$$

*The expected permanent income growth factor is smaller than the gross interest factor.*

## Gloss

FHWC says the discounted growth factor $\RNrmByG^{-1} = \PermGroFac/\Rfree$ is below 1, equivalently $\Rfree > \PermGroFac$. This is the condition under which the present-discounted value of an infinite stream of permanent-income payments is finite — that is, "human wealth" $\hLvl_{t}$ converges as the horizon extends.

Without FHWC, the consumer in the perfect-foresight unconstrained problem could borrow against an infinite present-value stream of future income; the limiting consumption function would diverge. FHWC is the natural counterpart to the consumer's no-Ponzi condition, and is the second of the two ingredients (with RIC) that produce a non-degenerate limiting solution in the perfect-foresight unconstrained case (`pf-unconstrained-requires-fhwc`).

In the stochastic case FHWC is no longer a stated assumption of the existence theorems for buffer-stock target / pseudo-target — those rely on FVAC, GIC/GIC-Mod, and (W)RIC. But many of the qualitative conditions relating GIC, RIC, FVAC are conditional on FHWC (e.g., "under FHWC, GIC implies FVAC"; see [pf-consumption-function-properties](#pf-consumption-function-properties)).

## Relations

- **assumed-by** [pf-unconstrained-requires-fhwc](pf-unconstrained-requires-fhwc.md) — Non-degenerate limiting solution exists iff FHWC and RIC both hold (prop-pfUCFHWC).
- **contrasts-with** [return-impatience-condition](return-impatience-condition.md) — FHWC concerns whether human wealth is finite; RIC concerns whether the consumer wants to deplete it.
- **requires** [`ass-pfincome`](../../BufferStockTheory.md#ass-pfincome) — FHWC presupposes the perfect-foresight income process used to define human wealth $\hLvl_t$.
- **assumed-by** [pf-consumption-function-properties](pf-consumption-function-properties.md) — Reciprocal edge: the perfect-foresight patience-condition chain (claim-PFConspC) maintains FHWC as its standing hypothesis, using $(\PermGroFac/\Rfree)^{1-1/\CRRA}<1$ to drive both implications GICRaw⇒FVAC and FVAC⇒RIC.

## Sources

- [BufferStockTheory.md#ass-FHWC](../../BufferStockTheory.md#ass-FHWC)
- [BufferStockTheory.md#eq-FHWC2](../../BufferStockTheory.md#eq-FHWC2)

## bellman-ddsl correspondence

> *Reserved field — the bellman-ddsl perch/stage mapping is **deferred** for every concept in this atlas; the cross-repo bridge has not been authored. This is not a delivered correspondence.*

- perch: `(deferred)`
- stage: `(deferred)`
