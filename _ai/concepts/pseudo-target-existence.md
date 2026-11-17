# ‘Pseudo-Target’

*Short form: **m-bal exists***

## Defining equation

Anchor: [`thm-MSSBalExists`](../../BufferStockTheory.md#thm-MSSBalExists)

$$
\Ex_t [\permShk_{t+1}{\mNrm}_{t+1}/\mNrm_t] = 1 ~if~ \mNrm_t = \mBalLvl.
$$

*Under WRIC, FVAC, and the ordinary GIC there exists a unique strictly positive pseudo-target $\mBalLvl$ at which expected $\permShk$-weighted normalised resources are unchanged, equivalently at which the level of market resources grows in expectation at the permanent-income growth factor.*

## Gloss

Theorem `thm-MSSBalExists` is the existence-and-uniqueness result for the pseudo-target $\mBalLvl$ — the paper's second, less restrictive notion of stability, which asks whether the level of market resources $\mLvl$ grows in expectation at the permanent-income growth factor $\PermGroFac$ (a 'balanced growth' path) rather than whether normalised individual resources are stationary. The theorem *assumes* weak return impatience (WRIC), finite value of autarky (FVAC), and the ordinary growth impatience condition (GIC), and *implies* the existence of a unique $\mBalLvl > 0$ solving $\Ex_t[\permShk_{t+1}\mNrm_{t+1}/\mNrm_t] = 1$, together with the level-stability inequalities ($\Ex_t[\mLvl_{t+1}]/\mLvl_t$ exceeds $\PermGroFac$ below $\mBalLvl$ and falls short above it).

Existence (Part i of the proof) is an Intermediate-Value-Theorem argument: the bounded-support assumption on $\permShk$ carries the continuity and the $\mNrm_t \to 0$ divergence over from the individual-target proof, while the limit of $\Ex_t[\permShk_{t+1}\mNrm_{t+1}/\mNrm_t]$ as $\mNrm_t \to \infty$ equals $\GPFacRaw$, which is below 1 precisely because GIC holds; a continuous function crossing 1 from above must equal 1 somewhere. Uniqueness shows the level-gap function $\difFunc(\mNrm_t) := \Ex_t[\permShk_{t+1}\mNrm_{t+1}] - \mNrm_t$ is strictly decreasing on $(0,\infty)$: when return impatience (RIC) holds this follows from the marginal-propensity-to-consume bound, and when RIC fails the same monotonicity holds because the only non-degenerate case with RIC failing is one where finite human wealth also fails, which forces $\Rfree/\PermGroFac < 1$.

The hypothesis here is exactly the ordinary GIC, *weaker* than the strong growth impatience (GIC-Mod) that the individual buffer-stock target requires (theorem `thm-target`). The implicit equations for the two targets differ only by the substitution of $\RNrmByG$ for $\bar{\RNrmByGRnd} = \RNrmByG\,\Ex[\permShk^{-1}]$, so they coincide when there are no permanent shocks ($\permShk \equiv 1$); when permanent-shock variance is large enough that GIC-Mod fails but GIC still holds, this theorem still delivers $\mBalLvl$ while no individual target $\mTrgNrm$ exists — the case in Figure `fig-GICModFailsButGICRawHolds`.

## Relations

- **requires** [weak-return-impatience-condition](weak-return-impatience-condition.md) — The theorem assumes WRIC (Assumption WRIC).
- **requires** [finite-value-of-autarky](finite-value-of-autarky.md) — The theorem assumes FVAC (Assumption FVAC).
- **requires** [growth-impatience-condition](growth-impatience-condition.md) — The theorem assumes the ordinary GIC; the $\mNrm_t\to\infty$ limit of the expected $\permShk$-weighted ratio equals $\GPFacRaw < 1$ exactly by GIC.
- **implies** [pseudo-target](pseudo-target.md) — This is the existence/uniqueness theorem for the pseudo-target $\mBalLvl$; it establishes the object that concept defines.
- **contrasts-with** [buffer-stock-target](buffer-stock-target.md) — Sibling existence theorem thm-target requires the stronger GIC-Mod; the pseudo-target needs only GIC, so it can exist when the individual target does not.
- **contrasts-with** [strong-growth-impatience-condition](strong-growth-impatience-condition.md) — GIC-Mod is the strengthened condition the individual target needs; this theorem deliberately relies only on the weaker GIC.

## Sources

- [BufferStockTheory.md#thm-MSSBalExists](../../BufferStockTheory.md#thm-MSSBalExists)
- [BufferStockTheory.md#eq-mBalLvl](../../BufferStockTheory.md#eq-mBalLvl)
- [BufferStockTheory.md#subsubsec-AppxPseudoSS](../../BufferStockTheory.md#subsubsec-AppxPseudoSS)

## bellman-ddsl correspondence

> *Reserved field — the bellman-ddsl perch/stage mapping is **deferred** for every concept in this atlas; the cross-repo bridge has not been authored. This is not a delivered correspondence.*

- perch: `(deferred)`
- stage: `(deferred)`
