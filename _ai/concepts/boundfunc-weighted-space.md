# $\boundFunc$-Bounded Functions and the Weighted-Norm Space $\mathcal{C}_{\boundFunc}(\Reals_{++},\Reals)$

*Short form: **$\boundFunc$-norm space***

## Defining equation

Anchor: [`eq-phinorm`](../../BufferStockTheory.md#eq-phinorm)

$$
\Vert \fFunc\Vert _{\boundFunc }=\sup_{s\in \Reals_{++}}\left[ \frac{|\fFunc(s)|}{\boundFunc (s)}\right]
$$

*The $\boundFunc$-norm rescales $|\fFunc(s)|$ pointwise by a strictly positive continuous weight $\boundFunc(s)$ and takes the supremum over the unbounded domain $\Reals_{++}$; $\fFunc$ is $\boundFunc$-bounded when this norm is finite, and $\mathcal{C}_{\boundFunc}(\Reals_{++},\Reals)$ is the subspace of continuous functions for which it is.*

## Gloss

This definition sets up the function space on which the entire existence argument for the stochastic problem is carried out. Fix a *weight* $\boundFunc\in\mathcal{C}(\Reals_{++},\Reals)$ with $\boundFunc>0$. A continuous $\fFunc:\Reals_{++}\to\Reals$ is called $\boundFunc$-*bounded* if its $\boundFunc$-norm $\Vert\fFunc\Vert_{\boundFunc}=\sup_{s\in\Reals_{++}}|\fFunc(s)|/\boundFunc(s)$ is finite, and $\mathcal{C}_{\boundFunc}(\Reals_{++},\Reals)$ denotes the subspace of all such functions. The point of the construction is that it tolerates functions that are unbounded *below*, diverging to $-\infty$ as $s\to 0^{+}$ — exactly the situation for the model's value functions, whose CRRA shape (with $\CRRA>1$) makes both $\uFunc$ and $\vFunc$ unbounded below near zero — provided they diverge no faster than the weight. The definition *assumes* only continuity and strict positivity of $\boundFunc$; it is otherwise generic, and the specific weight that makes it work for this model is supplied separately.

The paper instantiates the weight as $\boundFunc(x)=\zeta+x^{1-\CRRA}$, where the additive constant $\zeta\in\Reals_{++}$ is built from model primitives and the consumption-share bounds (its parametrization is pinned down in Claim [](#rem-shnkrdef), Appendix [](#sec-Tcontractionmapping)). This choice is dictated by the felicity function: under CRRA utility the term $x^{1-\CRRA}$ matches the order of growth of $\uFunc$ and of the value functions, so candidate value functions are $\boundFunc$-bounded, while the constant $\zeta$ provides the slack needed to verify Boyd's discounting condition $\DiscFac\Ex\PermGroFacRnd^{1-\CRRA}\boundFunc\circ\hat{\mFunc}^{\nxt}\leq\Shrinker\boundFunc$ (Appendix [](#sec-Tcontractionmapping)). The relevant norm is precisely the one used to define the [Boyd-style weighted contraction](#boyd-weighted-contraction) under which the bounded Bellman operators act.

The construction *implies* the two structural properties that the rest of the proof exploits. First, $\mathcal{C}_{\boundFunc}(\Reals_{++},\Reals)$ is a *complete* metric space under the $\boundFunc$-norm, which is what lets a Cauchy sequence of finite-horizon value functions converge *within* the space to a limit $\vFunc\in\mathcal{C}_{\boundFunc}(\Reals_{++},\Reals)$ — the decisive step in the [existence theorem](#nondegenerate-solution-existence) (`thm-convgtobellman`). Second, $\boundFunc$-norm convergence is strong enough to be upgraded: because the weight is continuous and positive, convergence in $\Vert\cdot\Vert_{\boundFunc}$ forces ordinary uniform convergence on every compact subset of $\Reals_{++}$ (the real-analysis fact [norm-implies-compactness](#norm-implies-compactness)), which is what allows the limit to be passed through the expectation operator. The space is the natural setting because the stationary operator $\TMap$ may be *undefined* on a conventional Banach space (Remark [feasible-correspondence-not-compact](#feasible-correspondence-not-compact)); restricting to $\boundFunc$-bounded functions and bounding the consumption share is exactly what tames the unbounded state space $\Reals_{++}$.

## Relations

- **requires** [boyd-weighted-contraction](boyd-weighted-contraction.md) — The $\boundFunc$-norm of eq-phinorm is the weighted supremum norm in Boyd's weighted contraction mapping theorem (thm-Boyd, cite-jboydWeighted); $\mathcal{C}_{\boundFunc}(\Reals_{++},\Reals)$ is the complete space on which that theorem is applied.
- **assumed-by** [contraction-mapping-consumption-bounds](contraction-mapping-consumption-bounds.md) — thm-cmap shows the MPC-bounded operator $\TMap^{\MPCminInf,\MPCmaxInf}:\mathcal{C}_{\boundFunc}(\Reals_{++},\Reals)\to\mathcal{C}_{\boundFunc}(\Reals_{++},\Reals)$ is a contraction in the $\boundFunc$-norm defined here.
- **assumed-by** [nondegenerate-solution-existence](nondegenerate-solution-existence.md) — Completeness of $\mathcal{C}_{\boundFunc}(\Reals_{++},\Reals)$ under the $\boundFunc$-norm is what makes the Cauchy sequence of finite-horizon value functions converge to $\vFunc\in\mathcal{C}_{\boundFunc}(\Reals_{++},\Reals)$ in thm-convgtobellman.
- **implies** [norm-implies-compactness](norm-implies-compactness.md) — Because the weight $\boundFunc$ is continuous and positive, convergence in the $\boundFunc$-norm defined here yields uniform convergence on every compact subset of $\Reals_{++}$ (fact-normimpliescompact), used to pass the limit through the expectation.
- **contrasts-with** [feasible-correspondence-not-compact](feasible-correspondence-not-compact.md) — Two distinct obstacles motivate the construction (remark-notCompact): the non-compact-valued feasibility correspondence $\mNrm\mapsto(0,\mNrm)$ breaks continuity, so Berge's Maximum Theorem fails and $\TMap$ need not map continuous functions to continuous functions; and, separately, the value functions are unbounded (below) on $\Reals_{++}$ — it is this unboundedness that the weighted norm fixes.

## Sources

- [BufferStockTheory.md#def-boundfuncspace](../../BufferStockTheory.md#def-boundfuncspace)
- [BufferStockTheory.md#eq-phinorm](../../BufferStockTheory.md#eq-phinorm)
- [BufferStockTheory.md#subsubsec-eventuallyCauchy](../../BufferStockTheory.md#subsubsec-eventuallyCauchy)

## bellman-ddsl correspondence

> *Reserved field — the bellman-ddsl perch/stage mapping is **deferred** for every concept in this atlas; the cross-repo bridge has not been authored. This is not a delivered correspondence.*

- perch: `(deferred)`
- stage: `(deferred)`
