# Feasibility Correspondence Is Not Compact-Valued (Berge Fails)

*Short form: **remark-notCompact***

## Defining equation

Anchor: [`remark-notCompact`](../../BufferStockTheory.md#remark-notCompact)

$$
\mNrm \mapsto (0,\mNrm)\ \text{open} \implies \text{Berge's Maximum Theorem fails} \implies \TMap\fFunc\ \text{need not be continuous for continuous}\ \fFunc
$$

*Because the consumption feasibility correspondence $\mNrm\mapsto(0,\mNrm)$ has open (hence non-compact) values, the hypotheses of Berge's Maximum Theorem are not met, so the stationary Bellman operator $\TMap$ can fail to send a continuous function to a continuous function.*

## Gloss

This remark isolates the precise technical obstacle that prevents the stationary Bellman operator $\TMap$ from being treated by textbook dynamic-programming machinery. The normalized operator $\TMap\vFunc_{t+1}(\mNrm)=\max_{\cNrm\in(0,\mNrm)}\{\uFunc(\cNrm)+\DiscFac\Ex\PermGroFacRnd^{1-\CRRA}\vFunc_{t+1}(\RNrmByGRnd(\mNrm-\cNrm)+\tranShkAll)\}$ optimizes over the *open* interval $(0,\mNrm)$; the boundary points $0$ and $\mNrm$ are deliberately excluded so that the maximand stays real-valued (at $\cNrm=\mNrm$ end-of-period assets, and hence next-period resources when $\pZero>0$, can hit zero where CRRA value diverges to $-\infty$). The remark *assumes* this open-valued feasibility correspondence $\mNrm\mapsto(0,\mNrm)$ and the consequent failure of compact-valuedness, and it *implies* that the standard Maximum Theorem of Berge cannot be invoked to guarantee continuity of the value of the maximization.

Concretely, Berge's Maximum Theorem requires the constraint correspondence to be continuous and compact-valued for the optimized value to inherit continuity from a continuous objective. The paper cites the form in Lemma 1 of [Jaśkiewicz and Nowak (2011)](#cite-Jaskiewicz2011); because $(0,\mNrm)$ is not compact, that hypothesis fails, so one cannot assert that $\TMap\fFunc$ is continuous whenever $\fFunc$ is. The remark is a *negative* result: it does not claim $\TMap$ destroys continuity, only that the usual sufficient condition for preserving it is unavailable, so $\TMap$ need not be a self-map on a vector space of continuous functions.

The implication propagates structurally. Standard dynamic programming [(Stachurski, 2022)](#cite-stachurski2022) would build a fixed point of $\TMap$ by showing it is a contraction on a Banach space of continuous functions; this remark blocks that route, since $\TMap$ may not even land in such a space. Reintroducing the endpoints $0$ and $\mNrm$ recovers a compact-valued correspondence $[0,\mNrm]$ and a map on upper-semicontinuous functions, but then values must lie in $\Reals_{+}\cup\{-\infty\}$, which is not a vector space; the artificial-liquidity-constraint device of [(Ma, Stachurski, and Toda, 2022b)](#cite-Ma2022) restores a real-valued continuation and a compact interval, but the present paper declines that route. This is exactly why the authors abandon a direct fixed-point attack on $\TMap$ and instead bound the consumption *share*, working with the per-period MPC-bounded operators $\TMap^{\MPCminInf,\MPCmaxInf}$ that *are* weighted-norm contractions — the strategy whose engine is [contraction-mapping-consumption-bounds](#contraction-mapping-consumption-bounds) and whose payoff is [nondegenerate-solution-existence](#nondegenerate-solution-existence).

## Relations

- **requires** [`eq-maintmap`](../../BufferStockTheory.md#eq-maintmap) — The remark is a statement about the stationary operator $\TMap$ defined at eq-maintmap, specifically its maximization over the open interval $(0,\mNrm)$.
- **implies** [contraction-mapping-consumption-bounds](contraction-mapping-consumption-bounds.md) — Because $\TMap$ need not be a continuous self-map (Berge fails), the paper cannot apply a fixed-point theorem to $\TMap$ directly and instead bounds the consumption share, using the MPC-bounded operators $\TMap^{\MPCminInf,\MPCmaxInf}$ of thm-cmap; this remark is the motivation cited for that detour.
- **implies** [nondegenerate-solution-existence](nondegenerate-solution-existence.md) — The non-compact feasibility correspondence is precisely why existing dynamic-programming arguments cannot establish a fixed point of $\TMap$ directly (BufferStockTheory.md near eq-maintmap), forcing the alternative existence route of thm-convgtobellman.
- **contrasts-with** [`Stationary-Bellman-Operator`](../../BufferStockTheory.md#Stationary-Bellman-Operator) — The stationary operator $\TMap$ excludes the boundary $\{0,\mNrm\}$ to stay real-valued; reintroducing it gives a compact interval $[0,\mNrm]$ on which only upper-semicontinuity (not a vector-space structure) survives.
- **contrasts-with** [boundfunc-weighted-space](boundfunc-weighted-space.md) — Mirror edge: the $\boundFunc$-weighted-norm space is introduced precisely because this non-compact feasibility correspondence leaves $\TMap$ possibly undefined on a conventional Banach space over $\Reals_{++}$.
- **contrasts-with** [stochastic-discount-factor-mst](stochastic-discount-factor-mst.md) — Mirror edge: the MST (2020) embedding holds only at $\pZero=0$; for $\pZero>0$ the zero-income event reinstates the natural constraint and this non-compact correspondence, which MST sidestep with an artificial constraint.

## Sources

- [BufferStockTheory.md#remark-notCompact](../../BufferStockTheory.md#remark-notCompact)
- [BufferStockTheory.md#subsubsec-challengesDP](../../BufferStockTheory.md#subsubsec-challengesDP)
- [BufferStockTheory.md#eq-maintmap](../../BufferStockTheory.md#eq-maintmap)

## bellman-ddsl correspondence

> *Reserved field — the bellman-ddsl perch/stage mapping is **deferred** for every concept in this atlas; the cross-repo bridge has not been authored. This is not a delivered correspondence.*

- perch: `(deferred)`
- stage: `(deferred)`
