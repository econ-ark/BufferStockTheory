# Convergence of Arguments from Convergence of Continuous-Function Values

*Short form: **xnconvgf***

## Defining equation

Anchor: [`fact-xnconvgf`](../../BufferStockTheory.md#fact-xnconvgf)

$$
\fFunc^{n}(x^{n}) \to \fFunc(x) \ \Longrightarrow\  x^{n} \to x \quad\text{as } n\to\infty
$$

*For a continuous limit function $\fFunc$, if the values $\fFunc^{n}(x^{n})$ converge to $\fFunc(x)$ then the arguments $x^{n}$ must themselves converge to $x$.*

## Gloss

This is a standalone real-analysis lemma collected in the paper's "Additional Standard Results" appendix. It supplies a partial converse to the elementary fact that continuity plus convergent arguments yields convergent values. Concretely: let $\fFunc\colon\Reals_{++}\to\Reals_{+}$ be continuous, take a sequence $x^{n}$ in $\Reals_{++}$ and a sequence of values $\fFunc^{n}(x^{n})$ in $\Reals_{+}$; the claim is that $\fFunc^{n}(x^{n})\to\fFunc(x)$ forces $x^{n}\to x$. The proof is by contradiction: if $x^{n}\not\to x$ then some subsequence stays at least $\delta$ away from $x$, and continuity of $\fFunc$ at the limit point $x$ keeps the corresponding values bounded away from $\fFunc(x)$ by a fixed $\epsilon$, contradicting the assumed convergence of the values.

The result *assumes* only that the limit function $\fFunc$ is continuous at the relevant point $x$, that $x$ lies in the open positive domain $\Reals_{++}$ (so the $\epsilon$–$\delta$ neighbourhood is genuinely interior), and that the value sequence $\fFunc^{n}(x^{n})$ actually converges to $\fFunc(x)$; no monotonicity, differentiability, or uniform convergence of the $\fFunc^{n}$ is needed. It *implies* that argument-level convergence can be recovered from value-level convergence whenever the limiting map is continuous — i.e. the map is, in this asymptotic sense, "left-invertible" along the sequence even when no global inverse exists.

Its purpose in the paper is to close the existence argument for the stochastic problem. In the proof that the finite-horizon solutions converge to a non-degenerate limiting solution (Theorem [](#thm-convgtobellman), concept [nondegenerate-solution-existence](#nondegenerate-solution-existence)), the value-function recursion has already been shown to converge — Equation [](#eq-convgcvftni) gives $\vFunc(\mNrm)=\uFunc(\cFunc_{t_{n}}(\mNrm))+\DiscFac\Ex[\PermGroFacRnd^{1-\CRRA}\vFunc(\mNrm^{\nxt})]$ in the limit. Reading the right-hand side as a continuous function $\fFunc$ of the consumption value $\cFunc_{t_{n}}(\mNrm)$, this Fact converts that value-level convergence into the needed *pointwise* convergence $\cFunc_{t_{n}}(\mNrm)\to\cFunc(\mNrm)$ of the consumption functions, which is what certifies that the limit $\cFunc$ is non-degenerate ($\cFunc(\mNrm)>0$ for every $\mNrm>0$, hence neither $\cFunc\equiv 0$ nor $\cFunc\equiv\infty$). It sits alongside two companion lemmas in the same section — [norm-implies-compactness](#norm-implies-compactness) ($\boundFunc$-norm convergence implies uniform convergence on compacts) and [compactness-preserved](#compactness-preserved) (continuity carries convergent arguments to convergent values) — which together supply the standard-analysis plumbing of that proof.

## Relations

- **assumed-by** [nondegenerate-solution-existence](nondegenerate-solution-existence.md) — The existence proof (Theorem thm-convgtobellman, part iii) applies this Fact to the converged value recursion eq-convgcvftni to deduce pointwise convergence $\cFunc_{t_{n}}(\mNrm)\to\cFunc(\mNrm)$ of the consumption functions, which establishes non-degeneracy $\cFunc(\mNrm)>0$.
- **implies** [nondegenerate-limiting-solution](nondegenerate-limiting-solution.md) — Recovering argument-level (consumption) convergence from value-level convergence is exactly what yields the strictly-positive limiting consumption function $\cFunc\colon\Reals_{++}\to\Reals_{++}$ that defines a non-degenerate limiting solution.
- **contrasts-with** [compactness-preserved](compactness-preserved.md) — compactness-preserved (Fact fact-compactnt) is the forward direction (convergent arguments $x_{n}\to x$ plus continuity give convergent values $\fFunc_{n}(x_{n})\to\fFunc(x)$); this Fact is the partial converse, recovering the arguments from the values.
- **requires** [`prop-cfuncprop`](../../BufferStockTheory.md#prop-cfuncprop) — The map whose continuity is exploited here — the right-hand side of the Bellman recursion as a function of consumption — inherits continuity from the regularity of $\cFunc_{t}$ and $\uFunc$ established for the finite-horizon problem in Proposition prop-cfuncprop.

## Sources

- [BufferStockTheory.md#fact-xnconvgf](../../BufferStockTheory.md#fact-xnconvgf)
- [BufferStockTheory.md#sec-realanalysis](../../BufferStockTheory.md#sec-realanalysis)
- [BufferStockTheory.md#eq-convgcvftni](../../BufferStockTheory.md#eq-convgcvftni)

## bellman-ddsl correspondence

> *Reserved field — the bellman-ddsl perch/stage mapping is **deferred** for every concept in this atlas; the cross-repo bridge has not been authored. This is not a delivered correspondence.*

- perch: `(deferred)`
- stage: `(deferred)`
