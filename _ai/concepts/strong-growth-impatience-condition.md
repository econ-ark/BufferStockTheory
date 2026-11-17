# Strong Growth Impatience Condition (GIC-Mod)

## Defining equation

Anchor: [`ass-GICMod`](../../BufferStockTheory.md#ass-GICMod)

$$
\Ex\left[\frac{\APFac}{\PermGroFac \permShk}\right] = \GPFacMod < 1
$$

*The expected ratio of absolute patience factor to the stochastic permanent-income growth factor is less than one.*

## Gloss

GIC-Mod is the inequality $\GPFacMod < 1$, where the modified growth patience factor has the closed form $\GPFacMod = \APFac/\PermGroFacAdj$ — absolute patience factor divided by the *uncertainty-adjusted* growth factor $\PermGroFacAdj := \PermGroFac/\Ex[1/\permShk]$. Equivalently (and how it first appears in the paper at `eq-GPFacMod`), $\GPFacMod = \Ex[\APFac/(\PermGroFac \permShk)]$. By Jensen's inequality, $\Ex[1/\permShk] \geq 1$, hence $\PermGroFacAdj \leq \PermGroFac$, hence $\GPFacMod \geq \GPFacRaw$ — strictly when $\permShk$ has positive variance. So GIC-Mod is always at least as strong as the ordinary GIC, and strictly stronger whenever there is uncertainty.

Operationally, GIC-Mod weights the patience comparison by realisations where $\permShk$ is *small* — the cases where post-shock permanent income is unusually low. A consumer who is growth-impatient in expectation but not in the GIC-Mod sense can exhibit individual wealth-to-permanent-income ratios that drift to infinity along sample paths where bad shocks happen to be rare; only GIC-Mod rules this out.

GIC-Mod is the condition required for existence of an *individual* buffer-stock target $\mTrgNrm$ (theorem `thm-target`); the weaker GIC suffices for the *aggregate* "pseudo-target" $\mBalLvl$ (theorem `thm-MSSBalExists`). When permanent shocks have large variance, GIC-Mod can fail while GIC still holds — in which case the pseudo-target exists but no individual target does, and individual sample paths can be unbounded.

## Relations

- **requires** [modified-growth-patience-factor](modified-growth-patience-factor.md) — GIC-Mod is exactly the inequality $\GPFacMod < 1$.
- **requires** [absolute-patience-factor](absolute-patience-factor.md) — Transitively: $\GPFacMod = \Ex[\APFac/(\PermGroFac \permShk)]$ is built from $\APFac$.
- **implies** [growth-impatience-condition](growth-impatience-condition.md) — By Jensen on $\Ex[1/\permShk] \geq 1$: GIC-Mod ⇒ GIC.
- **assumed-by** [buffer-stock-target](buffer-stock-target.md) — Individual buffer-stock target existence requires GIC-Mod.
- **contrasts-with** [pseudo-target](pseudo-target.md) — Pseudo-target existence (thm-MSSBalExists) needs only GIC; the stronger GIC-Mod is what additionally yields the individual target.
- **contrasts-with** [pseudo-target-existence](pseudo-target-existence.md) — Mirror of pseudo-target-existence contrasts-with strong-growth-impatience-condition: that theorem deliberately relies only on the weaker GIC, while GIC-Mod is the strengthened condition the individual target needs.
- **contrasts-with** [target-ordering-part-one](target-ordering-part-one.md) — Mirror of target-ordering-part-one contrasts-with strong-growth-impatience-condition: the pseudo-target/target ordering has content only in the GIC-Mod regime where the individual target exists; under only GIC it is vacuous.
- **contrasts-with** [gic-implies-harmenberg-impatience](gic-implies-harmenberg-impatience.md) — Mirror edge: the GIC⇒Harmenberg-impatience result (claim-gicimpliesharmimp) uses the raw expectations-based GIC for the Harmenberg measure change, not the stronger individual-target condition GIC-Mod.

## Sources

- [BufferStockTheory.md#GICMod](../../BufferStockTheory.md#GICMod)
- [BufferStockTheory.md#ass-GICMod](../../BufferStockTheory.md#ass-GICMod)
- [BufferStockTheory.md#eq-GPFacMod](../../BufferStockTheory.md#eq-GPFacMod)

## bellman-ddsl correspondence

> *Reserved field — the bellman-ddsl perch/stage mapping is **deferred** for every concept in this atlas; the cross-repo bridge has not been authored. This is not a delivered correspondence.*

- perch: `(deferred)`
- stage: `(deferred)`
