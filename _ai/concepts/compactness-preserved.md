# Continuity Under Uniform-on-Compacts Convergence

*Short form: **Fact (moving evaluation point)***

## Defining equation

Anchor: [`fact-compactnt`](../../BufferStockTheory.md#fact-compactnt)

$$
\fFunc_n \to \fFunc \text{ uniformly on compact sets},\ \ x_n \to x \ \Longrightarrow\ \fFunc_n(x_n) \to \fFunc(x).
$$

*If continuous functions converge uniformly on compact sets and the evaluation points converge, then the function values evaluated along the moving points converge to the limit function evaluated at the limit point.*

## Gloss

This is a standard real-analysis fact (Appendix [](#sec-realanalysis), Additional Standard Results): let $\{\fFunc_n\}$ be a sequence of continuous functions on a subset of the real line that converges uniformly to $\fFunc$ on every compact set, and let $\{x_n\}$ be a convergent sequence of real numbers with limit $x$; then $\fFunc_n(x_n) \to \fFunc(x)$. The point is that the evaluation argument is allowed to *move* with $n$: ordinary pointwise convergence would only give $\fFunc_n(x) \to \fFunc(x)$ at a fixed argument, whereas here both the function and the point at which it is evaluated change simultaneously. What makes the joint limit go through is the *uniformity* of the convergence on a compact set containing the tail of $\{x_n\}$, which lets a triangle-inequality split $|\fFunc_n(x_n)-\fFunc(x)| \leq |\fFunc_n(x_n)-\fFunc(x_n)| + |\fFunc(x_n)-\fFunc(x)|$ control the first term uniformly (uniform convergence) and the second by continuity of the limit $\fFunc$.

The fact *assumes* continuity of the $\fFunc_n$ and convergence that is uniform on compact sets — not merely pointwise — together with convergence of the argument sequence. In this paper that hypothesis is supplied by its companion result [weighted-norm convergence implies uniform convergence on compacts](#norm-implies-compactness): convergence in the weighted $\boundFunc$-norm $\Vert\cdot\Vert_{\boundFunc}$ implies uniform convergence on compact subsets of $\Reals_{++}$. So the two facts are used as a pair — [norm-implies-compactness](#norm-implies-compactness) upgrades $\boundFunc$-norm convergence to uniform-on-compacts convergence, and this fact then transports that convergence through a moving evaluation point. It is a partial converse in spirit to [the argument-recovery proposition](#sequence-convergence-fact), which runs the implication the other way (convergence of the values forces convergence of the arguments).

Its role is purely instrumental inside the existence argument for the stochastic problem. In the proof of the limiting-solution theorem ([nondegenerate-solution-existence](#nondegenerate-solution-existence)), once the value-function subsequence $\vFunc_{t_{n(i)}+1}$ is known to converge in the $\boundFunc$-norm (hence uniformly on compacts) and the random next-period resources $\mNrm_{t_{n(i)}+1}$ converge, this fact yields $\vFunc_{t_{n(i)}+1}(\mNrm_{t_{n(i)}+1}) \to \vFunc(\mNrm^{\nxt})$ almost surely (Equation [](#eq-convgcvftni) and surrounding text). That almost-sure convergence is exactly what is needed to apply the Dominated Convergence Theorem and pass the limit inside the expectation $\Ex\PermGroFacRnd^{1-\CRRA}\vFunc_{t_{n(i)}+1}(\mNrm_{t_{n(i)}+1})$, completing the verification that the limiting $\vFunc$ satisfies the stationary Bellman equation. It carries no economic content of its own; it is a piece of the analytic plumbing that makes the convergence-of-iterates argument rigorous.

## Relations

- **requires** [norm-implies-compactness](norm-implies-compactness.md) — The uniform-on-compacts hypothesis is delivered in this paper by norm-implies-compactness (Fact fact-normimpliescompact), which converts weighted $\boundFunc$-norm convergence into uniform convergence on compact subsets of $\Reals_{++}$; the two facts are applied together.
- **contrasts-with** [sequence-convergence-fact](sequence-convergence-fact.md) — sequence-convergence-fact (Proposition fact-xnconvgf) is the converse-direction companion: it infers convergence of the argument sequence $x_n\to x$ from convergence of the values $\fFunc^n(x^n)\to\fFunc(x)$, whereas this fact infers convergence of the values from convergence of the arguments.
- **assumed-by** [nondegenerate-solution-existence](nondegenerate-solution-existence.md) — Used in the existence proof (thm-convgtobellman): combined with $\boundFunc$-norm convergence of $\vFunc_{t_{n(i)}+1}$ and convergence of $\mNrm_{t_{n(i)}+1}$, it gives almost-sure convergence $\vFunc_{t_{n(i)}+1}(\mNrm_{t_{n(i)}+1})\to\vFunc(\mNrm^{\nxt})$, enabling the Dominated Convergence step (eq-convgcvftni).

## Sources

- [BufferStockTheory.md#fact-compactnt](../../BufferStockTheory.md#fact-compactnt)
- [BufferStockTheory.md#sec-realanalysis](../../BufferStockTheory.md#sec-realanalysis)
- [BufferStockTheory.md#eq-convgcvftni](../../BufferStockTheory.md#eq-convgcvftni)

## bellman-ddsl correspondence

> *Reserved field — the bellman-ddsl perch/stage mapping is **deferred** for every concept in this atlas; the cross-repo bridge has not been authored. This is not a delivered correspondence.*

- perch: `(deferred)`
- stage: `(deferred)`
