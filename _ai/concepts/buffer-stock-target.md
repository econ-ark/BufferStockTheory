# Buffer Stock Target

*Short form: **m-target***

## Defining equation

Anchor: [`eq-mTarget`](../../BufferStockTheory.md#eq-mTarget)

$$
\Ex_t [{\mNrm}_{t+1}/\mNrm_t] = 1 \text{ if } \mNrm_t = \mTrgNrm
$$

*A level of normalized market resources at which expected normalized resources are unchanged from one period to the next.*

## Gloss

The buffer stock target $\mTrgNrm$ is the eponymous concept of the paper: a level of (permanent-income-normalized) market resources at which the consumer expects no change in their normalized resources next period. Below the target, expected normalized resources rise; above it, they fall. The target is therefore a stable point of the dynamics of $\mNrm$.

Existence of an individual buffer-stock target (theorem `thm-target`) requires three conditions: weak return impatience (WRIC), finite value of autarky (FVAC), and *strong* growth impatience (GIC-Mod). The last is what makes the buffer-stock target distinct from the weaker "pseudo-target" $\mBalLvl$ (theorem `thm-MSSBalExists`), which exists under the ordinary GIC and concerns the *level* dynamics $\Ex_t[\mLvl_{t+1}/\mLvl_t] = \PermGroFac$ rather than the normalized dynamics. The two coincide when there are no permanent shocks ($\permShk \equiv 1$); when permanent shocks have larger variance, GIC-Mod can fail while GIC still holds, in which case the pseudo-target exists but the individual target does not.

The implicit equation defining the target (`eq-mTargImplicit`) takes the form $(\mTrgNrm - \cFunc(\mTrgNrm))\bar{\RNrmByGRnd} + 1 = \mTrgNrm$ where $\bar{\RNrmByGRnd} = \RNrmByG \Ex[\permShk^{-1}]$ — the "permanent-shock-adjusted" return factor.

## Relations

- **requires** [finite-value-of-autarky](finite-value-of-autarky.md) — thm-target assumes FVAC.
- **requires** [weak-return-impatience-condition](weak-return-impatience-condition.md) — thm-target assumes weak return impatience.
- **requires** [strong-growth-impatience-condition](strong-growth-impatience-condition.md) — thm-target assumes GIC-Mod (the strengthened sibling of GIC).
- **contrasts-with** [pseudo-target](pseudo-target.md) — The pseudo-target $\mBalLvl$ exists under the weaker GIC; the individual target requires GIC-Mod.
- **contrasts-with** [pseudo-target-existence](pseudo-target-existence.md) — Mirror of pseudo-target-existence contrasts-with buffer-stock-target: its existence theorem (thm-MSSBalExists) needs only GIC, so the pseudo-target can exist when this individual target does not.
- **contrasts-with** [nondegenerate-limiting-solution](nondegenerate-limiting-solution.md) — Mirror of nondegenerate-limiting-solution contrasts-with buffer-stock-target: non-degeneracy is the weaker, prior result; the buffer-stock target is the stronger statement about stable dynamics of $\mNrm$.

## Sources

- [BufferStockTheory.md#thm-target](../../BufferStockTheory.md#thm-target)
- [BufferStockTheory.md#eq-mTargImplicit](../../BufferStockTheory.md#eq-mTargImplicit)
- [BufferStockTheory.md#onetarget](../../BufferStockTheory.md#onetarget)

## bellman-ddsl correspondence

> *Reserved field — the bellman-ddsl perch/stage mapping is **deferred** for every concept in this atlas; the cross-repo bridge has not been authored. This is not a delivered correspondence.*

- perch: `(deferred)`
- stage: `(deferred)`
