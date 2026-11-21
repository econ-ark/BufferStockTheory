# Absolute Impatience Condition (AIC)

## Defining equation

Anchor: [`ass-AIC`](../../BufferStockTheory.md#ass-AIC)

$$
\APFac < 1
$$

*The absolute patience factor is less than one — perfect-foresight consumption falls over time.*

## Gloss

AIC says the absolute patience factor $\APFac := (\Rfree\DiscFac)^{1/\CRRA}$ is below 1. By the Euler equation of the perfect-foresight model, this is exactly the condition that consumption growth $\cLvl_{t+1}/\cLvl_{t} = \APFac$ is below 1 — the consumer would optimally choose to spend more today than tomorrow.

AIC is the simplest of the four named patience conditions: while RIC compares $\APFac$ to the gross interest factor $\Rfree$ and GIC compares it to the permanent income growth factor $\PermGroFac$, AIC compares it to 1. In standard income-fluctuation-literature notation, AIC corresponds to $\DiscFac\Rfree < 1$, which guarantees the existence of a stable asset distribution when there is no permanent income growth (Szeidl 2013; Ma-Stachurski-Toda 2022). With permanent income growth in the model, however, AIC is neither necessary nor sufficient for the paper's existence theorems — those use the more nuanced RIC, WRIC, and the FVAC/GIC family.

AIC is therefore a useful reference point and a sanity-check (does the consumer want to spend more today than tomorrow at all?) rather than a load-bearing condition for the main results.

## Relations

- **requires** [absolute-patience-factor](absolute-patience-factor.md) — AIC is defined in terms of $\APFac$.
- **contrasts-with** [return-impatience-condition](return-impatience-condition.md) — AIC compares $\APFac$ to 1; RIC compares it to $\Rfree$. RIC is the binding condition in the paper.
- **contrasts-with** [growth-impatience-condition](growth-impatience-condition.md) — AIC compares $\APFac$ to 1; GIC compares it to $\PermGroFac$.

## Sources

- [BufferStockTheory.md#AIC](../../BufferStockTheory.md#AIC)
- [BufferStockTheory.md#ass-AIC](../../BufferStockTheory.md#ass-AIC)
- [BufferStockTheory.md#eq-APFac](../../BufferStockTheory.md#eq-APFac)

## bellman-ddsl correspondence

> *Reserved field — the bellman-ddsl perch/stage mapping is **deferred** for every concept in this atlas; the cross-repo bridge has not been authored. This is not a delivered correspondence.*

- perch: `(deferred)`
- stage: `(deferred)`
