# Growth Impatience Implies Harmenberg Impatience

## Defining equation

Anchor: [`claim-gicimpliesharmimp`](../../BufferStockTheory.md#claim-gicimpliesharmimp)

$$
\GPFacRaw < 1 \implies \log \left( \APFac \right) < \int \log(\PermGroFac\permShk) \permShk f(\permShk)\,d\permShk
$$

*If the consumer is growth impatient (absolute patience factor below the expected permanent-income growth factor), then the absolute patience factor satisfies the impatience inequality Harmenberg (2021b) imposes to guarantee a well-defined permanent-income-weighted distribution of normalized market resources.*

## Gloss

This claim certifies that the paper's own [growth impatience condition](#growth-impatience-condition) (GIC), $\GPFacRaw=\APFac/\PermGroFac<1$, is sufficient for the (logically distinct) impatience inequality that [(Harmenberg, 2021b)](#cite-harmenbergAggregating) requires for the existence of the permanent-income-weighted ("Harmenberg-invariant") distribution of normalized market resources. Writing $f$ for the density of the permanent-income shock $\permShk$ (normalized so $\Ex[\permShk]=1$), Harmenberg's condition is $\log(\APFac) < \int \log(\PermGroFac\permShk)\,\permShk\, f(\permShk)\,d\permShk$. The claim *assumes* GIC and *implies* this inequality, so any calibration the paper already uses for its growth-impatience results automatically supports the permanent-income-weighted change of measure exploited in the covariance/balanced-growth material of Section 4.

The proof is a one-line Jensen argument. The map $\permShk\mapsto \log(\PermGroFac\permShk)\,\permShk$ is convex, so Jensen's inequality bounds the right-hand integral below by its value at the mean: $\int \log(\PermGroFac\permShk)\,\permShk\, f(\permShk)\,d\permShk \geq \log(\PermGroFac\,\Ex[\permShk])\,\Ex[\permShk] = \log(\PermGroFac)$, where the final equality uses the unit-mean normalization $\Ex[\permShk]=1$. GIC says $\GPFacRaw<1$, i.e. $\PermGroFac>\APFac$, and because $\log$ is strictly increasing this gives $\log(\PermGroFac)>\log(\APFac)$. Chaining the two inequalities yields $\int \log(\PermGroFac\permShk)\,\permShk\, f(\permShk)\,d\permShk \geq \log(\PermGroFac) > \log(\APFac)$, which is exactly Harmenberg's condition.

Two scope remarks. First, GIC is *sufficient but not claimed necessary*: the Jensen step only lower-bounds the Harmenberg integral, so the converse implication is not asserted and Harmenberg impatience could in principle hold even where GIC fails. Second, this result sits squarely in the aggregation/distributional strand of the paper (it underwrites use of Harmenberg's permanent-income-weighted measure) rather than in the individual-problem existence/convergence theorems; it relates GIC to a *measure-change* condition on $\permShk$, not to the value-function contraction conditions (RIC/WRIC/FVAC) that govern existence of the individual nondegenerate solution.

## Relations

- **requires** [growth-impatience-condition](growth-impatience-condition.md) — The claim takes GIC ($\GPFacRaw=\APFac/\PermGroFac<1$, anchor ass-GICRaw) as its hypothesis; GIC supplies $\PermGroFac>\APFac$, the strict gap that the strictly increasing $\log$ converts into $\log(\PermGroFac)>\log(\APFac)$.
- **implies** [`eq-HarmImp`](../../BufferStockTheory.md#eq-HarmImp) — Delivers Harmenberg (2021b) impatience $\log(\APFac) < \int \log(\PermGroFac\permShk)\permShk f(\permShk)\,d\permShk$ (eq-HarmImp), the condition guaranteeing existence of the permanent-income-weighted distribution of normalized market resources.
- **requires** [`eq-Jensen`](../../BufferStockTheory.md#eq-Jensen) — The proof rests on Jensen's inequality applied to the convex map $\permShk\mapsto\log(\PermGroFac\permShk)\permShk$ (eq-Jensen), which lower-bounds the Harmenberg integral by $\log(\PermGroFac\Ex[\permShk])\Ex[\permShk]=\log(\PermGroFac)$ using $\Ex[\permShk]=1$.
- **contrasts-with** [strong-growth-impatience-condition](strong-growth-impatience-condition.md) — The hypothesis here is the (raw, expectations-based) GIC governing the cross-sectional mean ratio, not the stronger individual-target condition GIC-Mod $\Ex[\APFac/\PermGroFacRnd]<1$; this claim concerns the Harmenberg measure change rather than existence of an individual buffer-stock target.

## Sources

- [BufferStockTheory.md#claim-gicimpliesharmimp](../../BufferStockTheory.md#claim-gicimpliesharmimp)
- [BufferStockTheory.md#sec-AppxHarmImpGIC](../../BufferStockTheory.md#sec-AppxHarmImpGIC)
- [BufferStockTheory.md#eq-HarmImp](../../BufferStockTheory.md#eq-HarmImp)

## bellman-ddsl correspondence

> *Reserved field — the bellman-ddsl perch/stage mapping is **deferred** for every concept in this atlas; the cross-repo bridge has not been authored. This is not a delivered correspondence.*

- perch: `(deferred)`
- stage: `(deferred)`
