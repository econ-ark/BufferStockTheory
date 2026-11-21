# Contraction Mapping Under Consumption Bounds

## Defining equation

Anchor: [`thm-cmap`](../../BufferStockTheory.md#thm-cmap)

$$
\text{WRIC} \wedge \text{FVAC} \implies \exists\, k,\ \alpha\in(0,1)\ \text{s.t.}\ \forall\,[\MPCminInf,\MPCmaxInf]\ \text{with}\ \MPCmax_{T-k}\geq \MPCmaxInf> \MPCminInf>0,\ \TMap^{\MPCminInf, \MPCmaxInf}\ \text{is a contraction with modulus}\ \alpha
$$

*Under weak return impatience and finite value of autarky, there exist a threshold horizon $k$ and modulus $\alpha\in(0,1)$ such that the MPC-bounded Bellman operator $\TMap^{\MPCminInf,\MPCmaxInf}$ is a contraction whenever the consumption-share interval $[\MPCminInf,\MPCmaxInf]$ is narrow enough (upper share bounded by the finite-horizon maximal MPC $\MPCmax_{T-k}$).*

## Gloss

This theorem supplies the analytical engine behind existence of the stochastic problem's limiting solution. Because permanent-income-normalized market resources live on the unbounded domain $\Reals_{++}$, the stationary Bellman operator $\TMap$ need not map any natural Banach space into itself, so the usual fixed-point machinery cannot be applied to it directly. The fix is to bound the consumption *share*: for share bounds $0<\MPCminInf<\MPCmaxInf$ the paper defines an "MPC bounded Bellman operator" $\TMap^{\MPCminInf, \MPCmaxInf}$ that optimizes only over $\cNrm\in[\MPCminInf \mNrm, \MPCmaxInf \mNrm]$, and the theorem shows this restricted operator is a genuine contraction on the weighted-norm space $\mathcal{C}_{\boundFunc}(\Reals_{++},\Reals)$ once the interval is narrow enough (specifically $\MPCmaxInf$ no larger than the finite-horizon maximal MPC $\MPCmax_{T-k}$ for some $k$).

The result *assumes* [weak return impatience](#WRIC) (WRIC) and [finite value of autarky](#FVAC) (FVAC). WRIC is what keeps the maximal MPCs $\MPCmax_{T-n}$ small enough that the operator stays well-defined and stops the upper consumption bound from approaching zero as the terminal period recedes; it is exactly the inequality used in Claim [maximal-mpc-at-most-one](#maximal-mpc-at-most-one) to produce the threshold horizon $k$. FVAC is what makes the contraction modulus strict: the modulus is $\Shrinker=\max\{\pZero \DiscFac (\Rfree (1-\MPCmax_{k}))^{1-\CRRA},\ \beta\Ex\PermGroFacRnd^{1-\CRRA}\}$ (Remark [](#rem-shnkrdef)), and FVAC is precisely what forces the second term $\beta\Ex\PermGroFacRnd^{1-\CRRA}<1$, so that $\Shrinker<1$. The proof proceeds by verifying the three hypotheses of Boyd's weighted contraction mapping theorem (`thm-Boyd`): monotonicity of $\TMap^{\MPCminInf,\MPCmaxInf}$, that $\TMap^{\MPCminInf,\MPCmaxInf}\mathbf{0}$ is $\boundFunc$-bounded, and a discounting condition that reduces to $\DiscFac\Ex\PermGroFacRnd^{1-\CRRA}\boundFunc\circ\hat{\mFunc}^{\nxt}\leq \Shrinker\boundFunc$.

Its conclusion feeds directly into the existence argument: the per-period operators $\TMap^{\MPCmin_{T-n}, \MPCmax_{T-n}}$ are eventually contractions with a common modulus, which makes the sequence of finite-horizon value functions Cauchy and hence convergent to a limiting non-degenerate solution (`thm-convgtobellman`, whose proof invokes this theorem for Item (i)(a)). It contrasts with the stronger situation under full [return impatience](#RIC): a remark notes that with RIC the minimal MPC obeys $\MPCmin>0$ for all $n$, so $\TMap^{\MPCmin, \MPCmax_{T-k}}$ becomes a single *stationary* contraction; without RIC, $\MPCmin=0$ and $\TMap^{0,\MPCmax_{T-k}}$ is not even a well-defined operator on $\mathcal{C}_{\boundFunc}(\Reals_{++},\Reals)$, which is exactly why the weaker WRIC plus a time-varying lower share bound is used here.

## Relations

- **requires** [weak-return-impatience-condition](weak-return-impatience-condition.md) — thm-cmap assumes WRIC; via Claim maximal-mpc-at-most-one it keeps the maximal MPCs shrinking so the bounded operator stays well-defined and the upper consumption bound stays strictly positive.
- **requires** [finite-value-of-autarky](finite-value-of-autarky.md) — thm-cmap assumes FVAC; it forces the second term $\beta\Ex\PermGroFacRnd^{1-\CRRA}<1$ of the max defining the modulus $\Shrinker$, giving the strict contraction modulus $\alpha<1$.
- **requires** [boyd-weighted-contraction](boyd-weighted-contraction.md) — The proof verifies the three conditions of Boyd's weighted contraction mapping theorem (thm-Boyd, cite-jboydWeighted).
- **requires** [maximal-mpc-at-most-one](maximal-mpc-at-most-one.md) — The proof opens by fixing $k$ so that Claim maximal-mpc-at-most-one (eq-MPCMAXKleq1) holds; this is what makes $\TMap^{\MPCminInf,\MPCmaxInf}$ well-defined and forces the first term of the modulus $\Shrinker$ strictly below one.
- **implied-by** [feasible-correspondence-not-compact](feasible-correspondence-not-compact.md) — Reciprocal edge: because Berge fails for the non-compact correspondence $\mNrm\mapsto(0,\mNrm)$ (remark-notCompact), the paper cannot fix a point of $\TMap$ directly and instead bounds the consumption share, which is the construction this theorem analyses.
- **assumed-by** [nondegenerate-solution-existence](nondegenerate-solution-existence.md) — The existence theorem's proof (thm-convgtobellman) invokes thm-cmap (Item (i)(a)); the eventual-contraction conclusion makes the finite-horizon value-function sequence Cauchy, yielding the limiting non-degenerate solution.
- **contrasts-with** [return-impatience-condition](return-impatience-condition.md) — Under RIC, $\MPCmin>0$ gives a single stationary contraction $\TMap^{\MPCmin,\MPCmax_{T-k}}$; under only WRIC, $\MPCmin=0$ forces the time-varying bounded operators used here.
- **contrasts-with** [ric-gives-stationary-contraction](ric-gives-stationary-contraction.md) — Mirror edge: thm-cmap proves the WRIC operators are eventually contractions with a common modulus (Cauchy argument); remark-ricstationary notes RIC upgrades that to a genuinely stationary contraction $\TMap^{\MPCmin,\MPCmax_{T-k}}$ on the whole tail.

## Sources

- [BufferStockTheory.md#thm-cmap](../../BufferStockTheory.md#thm-cmap)
- [BufferStockTheory.md#thm-Boyd](../../BufferStockTheory.md#thm-Boyd)
- [BufferStockTheory.md#sec-Tcontractionmapping](../../BufferStockTheory.md#sec-Tcontractionmapping)

## bellman-ddsl correspondence

> *Reserved field — the bellman-ddsl perch/stage mapping is **deferred** for every concept in this atlas; the cross-repo bridge has not been authored. This is not a delivered correspondence.*

- perch: `(deferred)`
- stage: `(deferred)`
