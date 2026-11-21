# Existence of Non-degenerate Solution

## Defining equation

Anchor: [`eq-stationarybellman`](../../BufferStockTheory.md#eq-stationarybellman)

$$
\TMap\vFunc(m) =  \uFunc(\cFunc(m)) + \DiscFac\Ex \Rnd{\PermGroFac}^{1-\CRRA}\vFunc(\RNrmByGRnd(m-\cFunc(m)) + \tranShkAll) , \qquad m\in \Reals_{++}.
$$

*The limiting value function is a fixed point of the stationary Bellman operator, attained by a measurable consumption policy.*

## Gloss

This is the existence theorem for the stochastic problem: under just two assumptions — weak return impatience (WRIC) and finite value of autarky (FVAC) — the backward-iterated finite-horizon value and consumption functions converge point-wise to a *non-degenerate limiting solution* (`def-nondegeneracy`), i.e. a $\vFunc$ that is a fixed point of the stationary Bellman operator $\TMap$ together with a measurable policy $\cFunc$ satisfying the stationary Bellman equation. "Non-degenerate" means $\cFunc$ maps into $\Reals_{++}$ rather than collapsing to the trivial $\cFunc(\mNrm)=0$ or exploding to $\cFunc(\mNrm)=\infty$.

The proof cannot use the textbook dynamic-programming route — showing $\TMap$ is itself a contraction on a Banach space (the strategy of standard treatments such as Stachurski (`cite-stachurski2022`)) — because the natural liquidity constraint makes the feasibility correspondence $\mNrm\mapsto(0,\mNrm)$ non-compact, so $\TMap$ is not a self-map on the continuous functions ([feasible-correspondence-not-compact](#feasible-correspondence-not-compact)). Instead the argument applies Boyd's (`cite-jboydWeighted`) weighted contraction theorem to a family of *MPC-bounded* operators $\TMap^{\MPCminInf,\MPCmaxInf}$: by Theorem `thm-cmap` these are contractions of modulus $\Shrinker<1$ on the weighted-norm space $\mathcal{C}_{\boundFunc}(\Reals_{++},\Reals)$, so the value-function sequence is Cauchy and, the space being complete, converges to a fixed point.

The two hypotheses play distinct roles. FVAC guarantees the value is finite (in levels) for a consumer who spends exactly permanent income each period; WRIC is what keeps the upper bound on the consumption share bounded away from zero, preventing consumption from converging to zero as the horizon recedes. Notably, the much stronger return-impatience condition (RIC) is *not* required, and neither is finite human wealth: under RIC one would additionally get a single stationary contraction with a strictly positive lower MPC bound, but the weaker WRIC already secures non-degeneracy (it merely permits the lower MPC bound to vanish). This theorem establishes that a well-behaved consumption rule *exists*; it is the prerequisite step before the target-existence results, which add growth-impatience assumptions to pin down stable points of the converged rule.

## Relations

- **requires** [weak-return-impatience-condition](weak-return-impatience-condition.md) — Hypothesis of the theorem; WRIC keeps the upper bound on the consumption share strictly positive, preventing degeneracy to zero consumption.
- **requires** [finite-value-of-autarky](finite-value-of-autarky.md) — Hypothesis of the theorem; FVAC guarantees finite value for the autarky (spend-permanent-income) policy and hence a finite weighted norm.
- **implied-by** [feasible-correspondence-not-compact](feasible-correspondence-not-compact.md) — Reciprocal edge: the non-compact feasibility correspondence (remark-notCompact) is exactly why a direct fixed point of $\TMap$ cannot be built, motivating the MPC-bounded weighted-norm route this theorem uses.
- **assumed-by** [buffer-stock-target-existence](buffer-stock-target-existence.md) — Existence of the converged non-degenerate rule $\cFunc$ is the prerequisite for the individual buffer-stock target theorem (thm-target), which adds GIC-Mod.
- **assumed-by** [pseudo-target-existence](pseudo-target-existence.md) — The pseudo-target (aggregate balanced-growth) theorem (thm-MSSBalExists) is stated for the same converged solution, adding GIC.
- **contrasts-with** [return-impatience-condition](return-impatience-condition.md) — Under uncertainty the weak WRIC suffices for nondegeneracy; in the perfect-foresight benchmark RIC was necessary. RIC would additionally give a single stationary contraction with $\MPCmin>0$, but is not needed here.

## Sources

- [BufferStockTheory.md#thm-convgtobellman](../../BufferStockTheory.md#thm-convgtobellman)
- [BufferStockTheory.md#eq-stationarybellman](../../BufferStockTheory.md#eq-stationarybellman)
- [BufferStockTheory.md#thm-cmap](../../BufferStockTheory.md#thm-cmap)

## bellman-ddsl correspondence

> *Reserved field — the bellman-ddsl perch/stage mapping is **deferred** for every concept in this atlas; the cross-repo bridge has not been authored. This is not a delivered correspondence.*

- perch: `(deferred)`
- stage: `(deferred)`
