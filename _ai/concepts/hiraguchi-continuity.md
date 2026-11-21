# MPC-Bounded Bellman Operator Maps the Weighted-Norm Space Into Itself

## Defining equation

Anchor: [`clm-hiraguchi_cont`](../../BufferStockTheory.md#clm-hiraguchi_cont)

$$
\xFunc\in \mathcal{C}_{\boundFunc}(S,Y) \implies \TMap^{\MPCminInf, \MPCmaxInf}\xFunc \in \mathcal{C}_{\boundFunc}(\Reals_{++}, \Reals_{+})
$$

*If $\xFunc$ is a continuous, $\boundFunc$-bounded function then its image under the MPC-bounded Bellman operator $\TMap^{\MPCminInf,\MPCmaxInf}$ is again continuous and $\boundFunc$-bounded; i.e. the operator is a self-map of the weighted-norm function space $\mathcal{C}_{\boundFunc}(\Reals_{++},\Reals)$.*

## Gloss

This claim is the "well-definedness" lemma that has to be discharged before Boyd's weighted contraction mapping theorem can be applied to the stochastic problem. It asserts that the MPC-bounded Bellman operator $\TMap^{\MPCminInf,\MPCmaxInf}$ — the operator that optimizes consumption only over the share interval $\cNrm_{t}\in[\MPCminInf\mNrm_{t},\MPCmaxInf\mNrm_{t}]$ — sends every element of the space $\mathcal{C}_{\boundFunc}(\Reals_{++},\Reals)$ of continuous, $\boundFunc$-bounded functions back into that same space. Here $\boundFunc(x)=\zeta+x^{1-\CRRA}$ is the bounding (weight) function fixed in Remark [](#rem-shnkrdef), and $\Vert\cdot\Vert_{\boundFunc}$ is the associated weighted supremum norm. The claim *assumes* only that the input $\xFunc$ is itself continuous and $\boundFunc$-bounded; it *implies* the closure property "$\TMap^{\MPCminInf,\MPCmaxInf}:\mathcal{C}_{\boundFunc}\to\mathcal{C}_{\boundFunc}$" that the contraction argument needs, since a contraction must map a Banach space into itself before its fixed point is even meaningful.

The proof proceeds in three steps. First, the conditional-expectation map $\cNrm_{t}\mapsto\Ex[\PermGroFacRnd^{1-\CRRA}\xFunc(\mNrm_{t+1})]$ is shown to be continuous: on any compact consumption interval $[\bar{\cNrm},\underline{\cNrm}]\subset\Reals_{++}$ the integrand is bounded above and below uniformly in $\cNrm$ (because the permanent and transitory shocks live on compact supports $[\permShkIndMin,\permShkIndMax]$ and $[0,\Max{\tranShkEmp}]$ and $\xFunc$ is continuous), so the Dominated Convergence Theorem passes the limit through the expectation. Second, because the feasibility correspondence $\mNrm_{t}\mapsto[\MPCminInf\mNrm_{t},\MPCmaxInf\mNrm_{t}]$ has a closed graph and is compact-valued, Berge's Maximum Theorem (Theorem 17.31 in [(Aliprantis and Border, 2006)](#cite-Aliprantis2005)) makes the value function $\TMap^{\MPCminInf,\MPCmaxInf}\xFunc$ continuous. Third, $\boundFunc$-boundedness follows from the triangle inequality applied to $\Vert\TMap^{\MPCminInf,\MPCmaxInf}\xFunc\Vert_{\boundFunc}$, splitting it into a utility term $\sup_{\mNrm}\{(\mNrm^{1-\CRRA}/(1-\CRRA))/(\zeta+\mNrm^{1-\CRRA})\}<\infty$ and a continuation term controlled by the $\boundFunc$-bound on $\xFunc$.

The claim is load-bearing for the contraction argument: the proof of Theorem [](#thm-cmap) opens by invoking it to assert that $\TMap^{\MPCminInf,\MPCmaxInf}$ maps $\mathcal{C}_{\boundFunc}(\Reals_{++},\Reals)$ to itself, and only then verifies Boyd's three conditions (monotonicity, $\boundFunc$-boundedness of $\TMap^{\MPCminInf,\MPCmaxInf}\mathbf{0}$, and the discounting inequality) to obtain the strict contraction. Its two subsidiary outputs are reused downstream: the Dominated-Convergence step is cited again when passing the limit through the Euler-equation expectation as the horizon recedes, and the continuity of the maximand together with compact-valuedness of the feasible set is what guarantees (via a measurable selector, Section 17.11 of Aliprantis and Border) that an optimal consumption function $\breve{\cFunc}$ exists at every $\mNrm_{t}$. The result *contrasts with* the unbounded operator $\TMap$ itself, which need not map any natural Banach space into itself on the unbounded domain $\Reals_{++}$ — precisely the difficulty that motivates restricting to the consumption-share interval $[\MPCminInf,\MPCmaxInf]$.

## Relations

- **assumed-by** [contraction-mapping-consumption-bounds](contraction-mapping-consumption-bounds.md) — The proof of thm-cmap begins by invoking this claim to state that $\TMap^{\MPCminInf,\MPCmaxInf}$ maps $\mathcal{C}_{\boundFunc}(\Reals_{++},\Reals)$ into itself, a prerequisite for verifying Boyd's three conditions and obtaining the contraction.
- **requires** [`rem-shnkrdef`](../../BufferStockTheory.md#rem-shnkrdef) — The bounding function $\boundFunc(x)=\zeta+x^{1-\CRRA}$ and the constant $\zeta$ that define the weighted-norm space $\mathcal{C}_{\boundFunc}$ are fixed in Remark rem-shnkrdef; the $\boundFunc$-boundedness step is stated relative to this $\boundFunc$.
- **implies** [`thm-Boyd`](../../BufferStockTheory.md#thm-Boyd) — Self-map closure $\TMap^{\MPCminInf,\MPCmaxInf}:\mathcal{C}_{\boundFunc}\to\mathcal{C}_{\boundFunc}$ is the standing hypothesis under which Boyd's weighted contraction mapping theorem (thm-Boyd) is then applied in the proof of thm-cmap.
- **contrasts-with** [boyd-weighted-contraction](boyd-weighted-contraction.md) — The unrestricted operator $\TMap$ need not map a natural Banach space into itself on $\Reals_{++}$; bounding the consumption share to $[\MPCminInf,\MPCmaxInf]$ is exactly what restores the self-map property this claim establishes, enabling the Boyd-style contraction.

## Sources

- [BufferStockTheory.md#clm-hiraguchi_cont](../../BufferStockTheory.md#clm-hiraguchi_cont)
- [BufferStockTheory.md#thm-cmap](../../BufferStockTheory.md#thm-cmap)
- [BufferStockTheory.md#sec-Tcontractionmapping](../../BufferStockTheory.md#sec-Tcontractionmapping)

## bellman-ddsl correspondence

> *Reserved field — the bellman-ddsl perch/stage mapping is **deferred** for every concept in this atlas; the cross-repo bridge has not been authored. This is not a delivered correspondence.*

- perch: `(deferred)`
- stage: `(deferred)`
