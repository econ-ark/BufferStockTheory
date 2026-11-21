# Limiting Consumption Function Inherits MPC Bounds and Is Strictly Positive

*Short form: **cStatStrctPos***

## Defining equation

Anchor: [`remark-cStatStrctPos`](../../BufferStockTheory.md#remark-cStatStrctPos)

$$
\MPCmax\,\mNrm \geq \cFunc(\mNrm) \geq \MPCmin\,\mNrm \quad\text{and}\quad \cFunc(\mNrm)>0 \ \text{for}\ \mNrm>0.
$$

*The pointwise limit $\cFunc$ of the finite-horizon consumption functions stays sandwiched between the same minimal and maximal MPC rays that bound every finite-horizon consumption function, and it is strictly positive on the positive reals.*

## Gloss

This remark records two regularity properties that the limiting (infinite-horizon) consumption function $\cFunc$ inherits once the existence argument has produced it as the pointwise limit of the finite-horizon consumption functions $\cFunc_{T-n}$. It *assumes* the conclusions of the non-degenerate existence theorem [nondegenerate-solution-existence](#nondegenerate-solution-existence): that $\cFunc_{T-n}\to\cFunc$ pointwise on $\Reals_{++}$, that the limit $\cFunc$ satisfies the stationary Bellman equation [](#eq-stationarybellman), and that the associated value function lies in the weighted-norm space $\vFunc\in\mathcal{C}_{\boundFunc}(\Reals_{++},\Reals)$.

The first half is an order-limit argument. Every finite-horizon consumption function is trapped between two linear rays in market resources, $\MPCmax\,\mNrm\geq\cFunc_{T-n}(\mNrm)\geq\MPCmin\,\mNrm$, where $\MPCmin$ and $\MPCmax$ are the limiting minimal and maximal marginal propensities to consume; because pointwise limits preserve weak inequalities, the same sandwich $\MPCmax\,\mNrm\geq\cFunc(\mNrm)\geq\MPCmin\,\mNrm$ survives in the limit. The lower ray is only informative when $\MPCmin>0$ (which holds under full [return impatience](#RIC)); under merely [weak return impatience](#WRIC), $\MPCmin$ can be zero, so the lower bound alone does not deliver strict positivity, which is why the second statement is needed.

The second half establishes strict positivity, $\cFunc(\mNrm)>0$ for every $\mNrm>0$, and it does *not* rely on the lower ray. It follows instead from feasibility and finiteness: $\cFunc$ solves the stationary Bellman equation [](#eq-stationarybellman) and the value $\vFunc$ is $\boundFunc$-bounded, so consuming a strictly positive amount is optimal at every interior resource level (zero consumption would drive CRRA marginal utility to infinity and is never optimal). This rules out the degenerate corner $\cFunc\equiv0$ that the weak-impatience lower bound leaves open.

The remark is a small but load-bearing lemma in the analysis of the converged solution. Strict positivity $\cFunc(\mNrm)>0$ is invoked directly in the proof of [limiting-mpcs-lemma](#limiting-mpcs-lemma) (Lemma [](#lemma-MPCBoundsConvg)) — first to license the monotonicity argument that $\cFunc(\mNrm)/\mNrm$ is non-increasing, and hence to pin down the limiting MPCs $\MPCmaxmax=\MPCmax$ and $\MPCminmin=\MPCmin$. It thereby connects the existence theorem to the subsequent characterization of the limiting consumption function's slope behavior.

## Relations

- **implied-by** [nondegenerate-solution-existence](nondegenerate-solution-existence.md) — Both halves use the existence theorem's outputs: pointwise convergence $\cFunc_{T-n}\to\cFunc$ for the inherited MPC sandwich, and the stationary Bellman equation eq-stationarybellman plus $\vFunc\in\mathcal{C}_{\boundFunc}$ for strict positivity.
- **requires** [`eq-stationarybellman`](../../BufferStockTheory.md#eq-stationarybellman) — Strict positivity $\cFunc(\mNrm)>0$ follows because $\cFunc$ satisfies the stationary Bellman equation and the value function is $\boundFunc$-bounded — feasibility-plus-finiteness, not the lower MPC ray.
- **implies** [limiting-mpcs-lemma](limiting-mpcs-lemma.md) — The proof of Lemma lemma-MPCBoundsConvg cites this remark for $\cFunc(\mNrm)>0$ on $\Reals_{++}$ (BufferStockTheory.md line near "recall Remark remark-cStatStrctPos"), used to get $\cFunc(\mNrm)/\mNrm$ non-increasing and to identify the limiting MPCs.
- **assumed-by** [consumption-ratio-nondecreasing](consumption-ratio-nondecreasing.md) — Reciprocal edge: applying the convex-negative ratio claim to $\fFunc=-\cFunc$ needs $\cFunc>0$ on $\Reals_{++}$, the strict positivity this remark supplies.
- **assumed-by** [mpc-bounds-convergence](mpc-bounds-convergence.md) — Reciprocal edge: the proof of lemma-MPCBoundsConvg uses strict positivity $\cFunc(\mNrm)>0$ from this remark to make the share $\cFunc(\mNrm)/\mNrm$ non-increasing before identifying its one-sided limits.
- **contrasts-with** [return-impatience-condition](return-impatience-condition.md) — Under RIC the minimal MPC $\MPCmin>0$, so the inherited lower ray $\cFunc(\mNrm)\geq\MPCmin\mNrm$ already gives positivity; under only WRIC, $\MPCmin=0$ and the separate Bellman-equation argument is needed for strict positivity.
- **special-case-of** [mpc-bounds-convergence](mpc-bounds-convergence.md) — The MPC-sandwich half is the limiting instance of the finite-horizon MPC bounds; this remark is the statement that those bounds pass to the pointwise limit.

## Sources

- [BufferStockTheory.md#remark-cStatStrctPos](../../BufferStockTheory.md#remark-cStatStrctPos)
- [BufferStockTheory.md#eq-stationarybellman](../../BufferStockTheory.md#eq-stationarybellman)
- [BufferStockTheory.md#lemma-MPCBoundsConvg](../../BufferStockTheory.md#lemma-MPCBoundsConvg)

## bellman-ddsl correspondence

> *Reserved field — the bellman-ddsl perch/stage mapping is **deferred** for every concept in this atlas; the cross-repo bridge has not been authored. This is not a delivered correspondence.*

- perch: `(deferred)`
- stage: `(deferred)`
