# Growth Impatience Condition (GIC)

## Defining equation

Anchor: [`ass-GICRaw`](../../BufferStockTheory.md#ass-GICRaw)

$$
\GPFacRaw < 1
$$

*The absolute patience factor falls short of the permanent income growth factor.*

## Gloss

GIC says the absolute patience factor $\APFac := (\Rfree\DiscFac)^{1/\CRRA}$ is smaller than the expected permanent income growth factor $\PermGroFac$, so that the ratio $\GPFacRaw := \APFac/\PermGroFac$ is below 1.

In a perfect-foresight setting GIC implies that consumption growth is slower than permanent income growth, so the consumer's consumption-to-permanent-income ratio falls over time. (The analogous statement for the *market-resources*-to-permanent-income ratio is a consequence of the stronger GIC-Mod, not of plain GIC under uncertainty.) Together with finite human wealth (FHWC), GIC is sufficient for the perfect-foresight finite value of autarky (PF-FVAC), which in turn implies return impatience (RIC); see the implication chain established in the proof of the perfect-foresight benchmarks.

GIC is the weaker of the two patience conditions used in the existence theorems for the stochastic problem. The stronger sibling, "strong growth impatience" (GIC-Mod), additionally takes the expectation over the permanent shock and is required for existence of an *individual* buffer-stock target. GIC alone is sufficient for the *aggregate* "pseudo-target" (`pseudo-target-existence`, theorem `thm-MSSBalExists`).

## Relations

- **requires** [growth-patience-factor](growth-patience-factor.md) — GIC is exactly the inequality $\GPFacRaw < 1$.
- **requires** [absolute-patience-factor](absolute-patience-factor.md) — Transitively: $\GPFacRaw = \APFac/\PermGroFac$ is built from $\APFac$.
- **contrasts-with** [return-impatience-condition](return-impatience-condition.md) — GIC is about growth (ratio of patience factor to growth factor); RIC is about return (ratio of patience factor to interest factor).
- **implies** [finite-value-of-autarky](finite-value-of-autarky.md) — Under FHWC, GIC implies the perfect-foresight finite value of autarky PF-FVAC (claim-PFConspC, concept pf-consumption-function-properties).
- **assumed-by** [pf-consumption-function-properties](pf-consumption-function-properties.md) — Reciprocal edge: GICRaw ($\APFac<\PermGroFac$) is the antecedent of the first implication in the perfect-foresight patience chain (claim-PFConspC); combined with FHWC it makes growth impatience sufficient for non-degeneracy.
- **assumed-by** [pseudo-target](pseudo-target.md) — The pseudo-target existence theorem requires GIC (together with WRIC and FVAC).
- **assumed-by** [pseudo-target-existence](pseudo-target-existence.md) — Reciprocal edge: the pseudo-target existence theorem (thm-MSSBalExists) requires GIC; it relies on the ordinary GIC rather than the stronger GIC-Mod.
- **implied-by** [strong-growth-impatience-condition](strong-growth-impatience-condition.md) — GIC-Mod is a strengthened sibling adding an expectation over the permanent shock; by Jensen, GIC-Mod implies GIC.

## Sources

- [BufferStockTheory.md#GICRaw](../../BufferStockTheory.md#GICRaw)
- [BufferStockTheory.md#ass-GICRaw](../../BufferStockTheory.md#ass-GICRaw)

## bellman-ddsl correspondence

> *Reserved field — the bellman-ddsl perch/stage mapping is **deferred** for every concept in this atlas; the cross-repo bridge has not been authored. This is not a delivered correspondence.*

- perch: `(deferred)`
- stage: `(deferred)`
