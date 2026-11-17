# Pseudo-Target

*Short form: **m-bal***

## Defining equation

Anchor: [`eq-mBalLvl`](../../BufferStockTheory.md#eq-mBalLvl)

$$
\Ex_t [\permShk_{t+1}{\mNrm}_{t+1}/\mNrm_t] = 1 \text{ if } \mNrm_t = \mBalLvl
$$

*A normalised market-resource level at which the level of market resources grows in expectation at the permanent-income growth rate.*

## Gloss

The pseudo-target $\mBalLvl$ is the second of the paper's two stability concepts (alongside the buffer-stock target $\mTrgNrm$). It addresses a different stability question from the individual target: whether the *level* of market resources $\mLvl_t$ grows in expectation at the permanent-income growth factor $\PermGroFac$ — i.e., whether the model has a balanced-growth path.

Specifically, $\mBalLvl$ is the value of normalised market resources at which $\Ex_t[\mLvl_{t+1}]/\mLvl_t = \PermGroFac$. Equivalently (after normalising), the implicit equation $\Ex_t[\permShk_{t+1} \mNrm_{t+1}/\mNrm_t] = 1$ holds at $\mNrm_t = \mBalLvl$. Below the pseudo-target, level growth exceeds $\PermGroFac$; above it, level growth falls short. Aggregate market resources thus drift toward $\mBalLvl$ even when individual sample paths do not converge to a target.

Existence of the pseudo-target requires WRIC, FVAC, and the ordinary GIC — the same first two conditions as the individual buffer-stock target, but with GIC instead of the stronger GIC-Mod. The two coincide when there are no permanent shocks ($\permShk \equiv 1$) and otherwise differ by a factor of $\Ex[\permShk^{-1}]$ in their implicit equations. When permanent-shock variance is large enough that GIC-Mod fails but GIC still holds, the pseudo-target exists but the individual target does not — the case illustrated by Figure `GICModFailsButGICRawHolds` in the paper.

## Relations

- **contrasts-with** [buffer-stock-target](buffer-stock-target.md) — Pseudo-target is the level/aggregate counterpart; buffer-stock target is the normalised/individual counterpart.
- **contrasts-with** [buffer-stock-target-existence](buffer-stock-target-existence.md) — Mirror of buffer-stock-target-existence contrasts-with pseudo-target: the individual-target theorem (thm-target) requires the stronger GIC-Mod, whereas this pseudo-target needs only GIC.
- **requires** [weak-return-impatience-condition](weak-return-impatience-condition.md) — thm-MSSBalExists assumes WRIC.
- **requires** [finite-value-of-autarky](finite-value-of-autarky.md) — thm-MSSBalExists assumes FVAC.
- **requires** [growth-impatience-condition](growth-impatience-condition.md) — thm-MSSBalExists assumes the ordinary GIC (weaker than the GIC-Mod the individual target needs).

## Sources

- [BufferStockTheory.md#thm-MSSBalExists](../../BufferStockTheory.md#thm-MSSBalExists)
- [BufferStockTheory.md#eq-mBalLvl](../../BufferStockTheory.md#eq-mBalLvl)
- [BufferStockTheory.md#balgrostable](../../BufferStockTheory.md#balgrostable)

## bellman-ddsl correspondence

> *Reserved field — the bellman-ddsl perch/stage mapping is **deferred** for every concept in this atlas; the cross-repo bridge has not been authored. This is not a delivered correspondence.*

- perch: `(deferred)`
- stage: `(deferred)`
