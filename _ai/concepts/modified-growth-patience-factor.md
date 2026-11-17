# Modified Growth Patience Factor (GPF-Mod)

## Defining equation

Anchor: [`eq-GPFacMod`](../../BufferStockTheory.md#eq-GPFacMod)

$$
\GPFacMod := \frac{\APFac}{\PermGroFacAdj} = \Ex\left[\frac{\APFac}{\PermGroFac \permShk}\right]
$$

*Ratio of absolute patience factor to the *uncertainty-adjusted* permanent-income growth factor; equivalently, expected ratio of absolute patience factor to the stochastic permanent-income growth factor.*

## Gloss

GPF-Mod is the uncertainty-adjusted sibling of the ordinary growth patience factor. Where $\GPFacRaw = \APFac/\PermGroFac$ uses the unconditional permanent-income growth factor in the denominator, $\GPFacMod$ uses the *uncertainty-adjusted* growth factor $\PermGroFacAdj := \PermGroFac/\Ex[1/\permShk]$ — the harmonic-mean adjustment of $\PermGroFac$ for the spread of the permanent shock $\permShk$. Equivalently (after a Jensen rearrangement), $\GPFacMod = \Ex[\APFac/(\PermGroFac \permShk)]$, the form in which it first appears at `eq-GPFacMod`; the same equation also states the closed form $\GPFacMod \equiv \APFac/\PermGroFacAdj$.

By Jensen's inequality applied to $1/x$, $\Ex[1/\permShk] \geq 1/\Ex[\permShk] = 1$ with strict inequality whenever $\permShk$ has positive variance. Therefore $\PermGroFacAdj \leq \PermGroFac$, hence $\GPFacMod \geq \GPFacRaw$, with the inequality strict in any non-degenerate stochastic setting. This is exactly the structural fact that makes GIC-Mod a *strictly stronger* condition than GIC: requiring $\GPFacMod < 1$ implies $\GPFacRaw < 1$, but not the reverse.

Operationally, the harmonic-mean adjustment over-weights bad-permanent-shock realisations (small $\permShk$) relative to good ones, because $1/\permShk$ blows up as $\permShk$ shrinks. A consumer who is impatient in expectation but not in this harmonic sense can have wealth-to-permanent-income ratios drift to infinity along sample paths where bad shocks happen to be rare. Only $\GPFacMod < 1$ (i.e. GIC-Mod) rules this out and yields the individual buffer-stock target.

## Relations

- **requires** [absolute-patience-factor](absolute-patience-factor.md) — $\GPFacMod = \Ex[\APFac/(\PermGroFac \permShk)]$ is built from $\APFac$.
- **assumed-by** [strong-growth-impatience-condition](strong-growth-impatience-condition.md) — GIC-Mod is exactly the inequality $\GPFacMod < 1$.
- **contrasts-with** [growth-patience-factor](growth-patience-factor.md) — GPF-Mod uses denominator $\PermGroFacAdj := \PermGroFac/\Ex[1/\permShk] \leq \PermGroFac$; GPF uses $\PermGroFac$. So GPF-Mod $\geq$ GPF, strictly when $\permShk$ has positive variance.

## Sources

- [BufferStockTheory.md#GICMod](../../BufferStockTheory.md#GICMod)
- [BufferStockTheory.md#eq-GPFacMod](../../BufferStockTheory.md#eq-GPFacMod)

## bellman-ddsl correspondence

> *Reserved field — the bellman-ddsl perch/stage mapping is **deferred** for every concept in this atlas; the cross-repo bridge has not been authored. This is not a delivered correspondence.*

- perch: `(deferred)`
- stage: `(deferred)`
