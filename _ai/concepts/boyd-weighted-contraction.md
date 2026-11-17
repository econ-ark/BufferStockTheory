# Boyd’s Contraction Mapping

## Defining equation

Anchor: [`thm-Boyd`](../../BufferStockTheory.md#thm-Boyd)

$$
\mathbb{B}({\xFunc } +\lambda\boundFunc ) \leq \mathbb{B}{\xFunc } +\lambda\alpha \boundFunc
$$

*A monotone Bellman-type operator that maps a weighted-bounded function space to itself and discounts the bounding function by a factor below one is a contraction with a unique fixed point.*

## Gloss

Boyd’s weighted contraction mapping theorem is the abstract fixed-point result the paper invokes to establish existence of a non-degenerate limiting value function on an *unbounded* state space, where the standard Banach-space contraction argument fails because utility is not bounded. It applies to an operator $\mathbb{B}$ on the space $\mathcal{C}_{\boundFunc}(S,Y)$ of functions whose ratio to a *bounding function* $\boundFunc$ is bounded (the $\boundFunc$-weighted sup-norm is finite), rather than to bounded functions directly.

The theorem ASSUMES three conditions on $\mathbb{B}$: (1) it is non-decreasing ($\xFunc \leq \yFunc \Rightarrow \mathbb{B}\xFunc \leq \mathbb{B}\yFunc$); (2) it maps the null function into the space, $\mathbb{B}\mathbf{0}\in\mathcal{C}_{\boundFunc}(S,Y)$; and (3) there is an $\alpha\in(0,1)$ such that for every $\lambda>0$, $\mathbb{B}(\xFunc+\lambda\boundFunc)\leq\mathbb{B}\xFunc+\lambda\alpha\boundFunc$ — a discounting condition under which adding $\lambda$ units of the bounding function to the input raises the output by at most $\lambda\alpha$ units. It IMPLIES that $\mathbb{B}$ is a contraction (of modulus $\alpha$) and therefore has a unique fixed point.

The paper does not assume these conditions directly; it constructs the bounding function $\boundFunc(x)=\zeta+x^{1-\CRRA}$ and the consumption-bounded Bellman operator $\TMap^{\MPCminInf,\MPCmaxInf}$ and then *verifies* Boyd’s three conditions to prove the contraction result (theorem `thm-cmap`). Monotonicity (1) holds by inspection of the operator; condition (2) — that $\TMap^{\MPCminInf,\MPCmaxInf}\mathbf{0}=\uFunc(\MPCmaxInf\mNrm)$ be $\boundFunc$-bounded — is discharged by the choice of bounding function $\boundFunc(x)=\zeta+x^{1-\CRRA}$ (`rem-shnkrdef`). The discounting condition (3) is the substantive one: the WRIC-dependent bound [maximal-mpc-at-most-one](#maximal-mpc-at-most-one) (used to fix $k$ large enough that $\pZero\DiscFac(\Rfree(1-\MPCmaxInf))^{1-\CRRA}<\Shrinker$) together with finite value of autarky makes the shrink factor $\Shrinker<1$, with the parametrization of $\zeta$ in `rem-shnkrdef` closing the required inequality.

This weighted-norm route is what lets the analysis avoid the artificial liquidity constraint and positive lower bound on income used by the related dynamic-programming approaches of Ma, Stachurski, and Toda to bound utility from below; Boyd’s theorem instead accommodates the unbounded continuation value directly through the choice of $\boundFunc$.

## Relations

- **assumed-by** [contraction-mapping-consumption-bounds](contraction-mapping-consumption-bounds.md) — The paper proves its consumption-bounded contraction result (thm-cmap) by verifying Boyd’s three conditions for the operator $\TMap^{\MPCminInf,\MPCmaxInf}$.
- **requires** [maximal-mpc-at-most-one](maximal-mpc-at-most-one.md) — WRIC-dependent bound (claim-MPCMAXKleq1) used to fix $k$ large enough that $\pZero\DiscFac(\Rfree(1-\MPCmaxInf))^{1-\CRRA}<\Shrinker$; it is deployed in verifying Boyd’s discounting condition (3).
- **requires** [`rem-shnkrdef`](../../BufferStockTheory.md#rem-shnkrdef) — Boyd’s discounting condition (3) uses the FVAC-based shrink factor $\Shrinker<1$ defined here, which also fixes the bounding function $\boundFunc(x)=\zeta+x^{1-\CRRA}$.
- **contrasts-with** [`cite-stachurski2022`](../../BufferStockTheory.md#cite-stachurski2022) — Standard dynamic-programming contraction arguments require a bounded operator on a Banach space; Boyd’s weighted norm instead handles the unbounded-utility case directly.
- **contrasts-with** [hiraguchi-continuity](hiraguchi-continuity.md) — Mirror edge: the unrestricted operator $\TMap$ need not map a natural Banach space into itself on $\Reals_{++}$; bounding the consumption share restores the self-map property (clm-hiraguchi_cont) that this Boyd-style contraction requires.

## Sources

- [BufferStockTheory.md#thm-Boyd](../../BufferStockTheory.md#thm-Boyd)
- [BufferStockTheory.md#thm-cmap](../../BufferStockTheory.md#thm-cmap)
- [BufferStockTheory.md#sec-Tcontractionmapping](../../BufferStockTheory.md#sec-Tcontractionmapping)

## bellman-ddsl correspondence

> *Reserved field — the bellman-ddsl perch/stage mapping is **deferred** for every concept in this atlas; the cross-repo bridge has not been authored. This is not a delivered correspondence.*

- perch: `(deferred)`
- stage: `(deferred)`
