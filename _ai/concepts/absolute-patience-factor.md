# Absolute Patience Factor (APFac, "thorn")

## Defining equation

Anchor: [`eq-APFac`](../../BufferStockTheory.md#eq-APFac)

$$
\APFac := (\Rfree\DiscFac)^{1/\CRRA}
$$

*The geometric blend of the gross interest factor and the time-discount factor, raised to the inverse of relative-risk-aversion.*

## Gloss

The absolute patience factor $\APFac$ — typeset with the archaic letter "thorn" (Þ) — is the consumption-growth factor implied by the Euler equation of a perfect-foresight model: $\cLvl_{t+1}/\cLvl_{t} = (\Rfree\DiscFac)^{1/\CRRA} = \APFac$. Its centrality across the paper's analysis (every patience condition and every existence theorem references it) justifies the special symbol.

Operationally, $\APFac$ aggregates two countervailing forces — the consumer's willingness to substitute consumption across time (governed by $\Rfree\DiscFac$) and curvature of the utility function (governed by $\CRRA$). The various patience conditions are all comparisons of $\APFac$ to one of *four* fundamental rates: $1$ (gives AIC, $\APFac < 1$), $\Rfree$ (RIC, $\APFac/\Rfree < 1$), $\PermGroFac$ (GIC, $\APFac/\PermGroFac < 1$), and $\PermGroFacAdj := \PermGroFac/\Ex[1/\permShk]$ (GIC-Mod, $\APFac/\PermGroFacAdj < 1$). The first three are deterministic; the fourth is the harmonic-mean uncertainty-adjusted growth factor that is strictly smaller than $\PermGroFac$ whenever $\permShk$ has positive variance, making GIC-Mod the strictly-stronger sibling of GIC.

The macro file renders $\APFac$, $\Pat$, and $\Thorn$ as the bold uppercase thorn Þ — all the patience *factor*. Distinct from these is $\APRte$, the absolute patience *rate* (the "Rte" suffix marks it as a rate, in the factor-minus-one / log family), typeset as the lowercase thorn þ — a different quantity, not an alias of the factor. The "Raw" suffixed sibling $\APFacRaw$ writes out the factor's formula verbatim — same quantity as $\APFac$, different typographic intent.

## Relations

- **assumed-by** [absolute-impatience-condition](absolute-impatience-condition.md) — AIC is the inequality $\APFac < 1$.
- **assumed-by** [return-impatience-condition](return-impatience-condition.md) — RIC is the inequality $\APFac/\Rfree < 1$.
- **assumed-by** [growth-impatience-condition](growth-impatience-condition.md) — GIC is the inequality $\APFac/\PermGroFac < 1$.

## Sources

- [BufferStockTheory.md#APFac](../../BufferStockTheory.md#APFac)
- [BufferStockTheory.md#eq-APFac](../../BufferStockTheory.md#eq-APFac)

## bellman-ddsl correspondence

> *Reserved field — the bellman-ddsl perch/stage mapping is **deferred** for every concept in this atlas; the cross-repo bridge has not been authored. This is not a delivered correspondence.*

- perch: `(deferred)`
- stage: `(deferred)`
