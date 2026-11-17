# Consumption Function is C2 and Concave

## Defining equation

Anchor: [`prop-cfuncprop`](../../BufferStockTheory.md#prop-cfuncprop)

$$
\text{For each } t,~ \cFunc_{t} \text{ is twice continuously differentiable, increasing and strictly concave.}
$$

*Every finite-horizon consumption function is twice continuously differentiable, strictly increasing, and strictly concave.*

## Gloss

This proposition records the regularity (shape) properties of the period-$t$ consumption function $\cFunc_t$ in the model with permanent and transitory income shocks (the Friedman-Muth process, Assumption `ass-shocks`): for every $t$, $\cFunc_t$ is twice continuously differentiable ($\mathbf{C}^2$), strictly increasing, and strictly concave. It is a structural result about a single finite-horizon problem and does not by itself invoke any of the impatience inequalities — concavity and monotonicity follow from CRRA utility and the recursive Bellman structure, established by backward induction in the appendix.

The proof (`sec-MPCiterproofs`) proceeds via the companion value-function claim `value-function-c3` (each $\vFunc_t$ is strictly negative, increasing, concave, $\mathbf{C}^3$, with $\lim_{\mNrm\to 0}\vFunc_t(\mNrm)=-\infty$) and Lemma `consumption-c2-properties`, which together give $\cFunc_t \in \mathbf{C}^2$; strict monotonicity comes from the first-order condition (`eq-derivativeConsFunc`), and strict concavity is Theorem 1 of `cite-ckConcavity` (Carroll and Kimball, 1996), who proved concavity but not continuous differentiability — the $\mathbf{C}^2$ refinement is this paper's contribution.

The proposition's main downstream use is shape, not existence: because $\cFunc_t$ is concave with a positive, decreasing, sub-unit marginal propensity to consume, the consumption share $\cFunc_t(\mNrm_t)/\mNrm_t$ is sandwiched between the period's minimal and maximal MPCs (`eq-cBounds`), and these bounds feed the Limiting-MPCs lemma (`limiting-mpcs-lemma`). That lemma is where the impatience conditions finally enter: weak return impatience (WRIC) for the recursions and return impatience (RIC) for the minimal MPC limit to be strictly positive.

## Relations

- **requires** [`ass-shocks`](../../BufferStockTheory.md#ass-shocks) — The proposition is stated for the normalized problem under the Friedman-Muth income process (Assumption ass-shocks); see the section preamble.
- **implies** [`eq-cBounds`](../../BufferStockTheory.md#eq-cBounds) — Concavity/monotonicity of $\cFunc_t$ imply the consumption share is bounded by the period MPCs $\MPCmin_t \mNrm_t \le \cFunc_t(\mNrm_t) \le \MPCmax_t \mNrm_t$ ("Proposition will imply").
- **assumed-by** [limiting-mpcs-lemma](limiting-mpcs-lemma.md) — The Limiting-MPCs lemma uses the proposition's concavity and differentiability when characterizing the MPC limits; RIC enters there (not here) to make the minimal MPC strictly positive.
- **contrasts-with** [return-impatience-condition](return-impatience-condition.md) — This proposition is an unconditional shape result; the value of the limiting minimal MPC it bounds becomes strictly positive only under RIC (per limiting-mpcs-lemma).

## Sources

- [BufferStockTheory.md#prop-cfuncprop](../../BufferStockTheory.md#prop-cfuncprop)
- [BufferStockTheory.md#sec-MPCiterproofs](../../BufferStockTheory.md#sec-MPCiterproofs)
- [BufferStockTheory.md#subsec-limSolExists](../../BufferStockTheory.md#subsec-limSolExists)

## bellman-ddsl correspondence

> *Reserved field — the bellman-ddsl perch/stage mapping is **deferred** for every concept in this atlas; the cross-repo bridge has not been authored. This is not a delivered correspondence.*

- perch: `(deferred)`
- stage: `(deferred)`
