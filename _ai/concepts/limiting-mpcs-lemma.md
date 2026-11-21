# Limiting MPCs

## Defining equation

Anchor: [`eq-MPCminInv`](../../BufferStockTheory.md#eq-MPCminInv)

$$
\MPCmin_{T-n}^{-1}  = 1+\left(\MPSmax\right) \MPCmin_{T-n+1}^{-1}, \qquad \MPCmax_{T-n}^{-1}   = 1+\left(\MPSmin\right) \MPCmax_{T-n+1}^{-1}.
$$

*The reciprocals of the per-period minimal and maximal MPCs obey first-order linear recursions in the horizon, driven respectively by the marginal propensities to save $\MPSmax=\RPFac$ and $\MPSmin=\pZero^{1/\CRRA}\RPFac$.*

## Gloss

This lemma pins down the shape of the finite-horizon consumption function near the two ends of the resource domain. For each period the ratio of optimal consumption to market resources $\cFunc_{t}(\mNrm)/\mNrm$ stays inside the interval $[\MPCmin_{t},\MPCmax_{t}]$ (Equation [](#eq-cBounds)), where the minimal and maximal MPCs $\MPCmin_{t},\MPCmax_{t}$ are the limits of the marginal propensity to consume as $\mNrm\to\infty$ and $\mNrm\to 0$. Item (i) gives the exact backward recursions: the reciprocal minimal MPC accumulates the saving factor $\MPSmax=\RPFac$ each period and the reciprocal maximal MPC accumulates $\MPSmin=\pZero^{1/\CRRA}\RPFac$. Item (ii) takes the limit as the terminal period recedes: the maximal MPC always converges to the strictly positive limit $\MPCmax=1-\pZero^{1/\CRRA}\RPFac>0$, and — only if [return impatience](#RIC) (RIC) holds — the minimal MPC converges to $\MPCmin=1-\RPFac>0$.

The lemma *assumes* [weak return impatience](#WRIC) (WRIC). WRIC is exactly what keeps the maximal-MPC reciprocal sequence convergent and so keeps the maximal-MPC limit $\MPCmax=1-\pZero^{1/\CRRA}\RPFac$ strictly positive; it is too weak to bound the consumption share away from zero below, so it pins down only the upper share bound and prevents that upper bound from collapsing to zero as the horizon grows. The asymmetry between the two items is structural: the maximal-MPC limit needs only WRIC, while the minimal-MPC limit additionally needs full [return impatience](#RIC), because without RIC the reciprocal minimal MPC diverges (the sequence $\{\MPCmin_{T-n}^{-1}\}$ is increasing and grows without bound) and $\MPCmin=0$. The recursions themselves are derived from the normalized Euler equation by taking $\mNrm\to\infty$ (minimal) and $\mNrm\to 0$ (maximal), using twice-continuous differentiability and strict concavity of $\cFunc_{t}$ established in Proposition [](#prop-cfuncprop) ([consumption-function-c2-concave](#consumption-function-c2-concave)); near zero the maximal MPC is governed by the recursive fear of the zero-income event, which is why the zero-income probability $\pZero$ enters $\MPSmin$ and hence $\MPCmax$.

Its conclusion is the load-bearing input to the existence argument for the stochastic problem. The strictly-positive maximal-MPC limit lets the time-varying MPC-bounded Bellman operators $\TMap^{\MPCmin_{t},\MPCmax_{t}}$ be defined on an interval that does not degenerate, and the proof of the existence theorem ([nondegenerate-solution-existence](#nondegenerate-solution-existence)) invokes this lemma directly (under its alias `cFuncBounds`) to assert $\MPCmax_{T-n}\leq\MPCmax_{T-k}$ for the threshold horizon $k$ supplied by the contraction theorem [](#thm-cmap). The economic content — that WRIC stops *everyone* from consuming an arbitrarily small share of resources as the horizon recedes — is precisely the nondegeneracy that the limiting solution inherits. The asymptotic-linearity reading of the consumption function as $\mNrm\to\infty$ connects to results of [Benhabib, Bisin, and Zhu](#cite-benhabibWealth) and [Ma and Toda](#cite-maTodaRich).

## Relations

- **requires** [weak-return-impatience-condition](weak-return-impatience-condition.md) — lemm-MPC assumes WRIC; it is what makes the maximal-MPC reciprocal sequence convergent and hence the limit $\MPCmax=1-\pZero^{1/\CRRA}\RPFac$ strictly positive, keeping the upper consumption share bounded away from zero as the horizon recedes.
- **requires** [return-impatience-condition](return-impatience-condition.md) — Item (ii) needs RIC for the minimal-MPC conclusion: only if RIC holds does $\MPCmin_{T-n}\to\MPCmin=1-\RPFac>0$; without RIC the reciprocal diverges and $\MPCmin=0$.
- **requires** [return-patience-factor](return-patience-factor.md) — The recursion drivers are the saving factors $\MPSmax=\RPFac$ and $\MPSmin=\pZero^{1/\CRRA}\RPFac$, both built from the return patience factor $\RPFac$; the limits $\MPCmin=1-\RPFac$ and $\MPCmax=1-\pZero^{1/\CRRA}\RPFac$ are too.
- **requires** [consumption-function-c2-concave](consumption-function-c2-concave.md) — The bound $\MPCmin_{t}\mNrm\leq\cFunc_{t}(\mNrm)\leq\MPCmax_{t}\mNrm$ (eq-cBounds) and the Euler-equation limit arguments rely on $\cFunc_{t}$ being $C^2$, increasing and strictly concave (Proposition prop-cfuncprop).
- **contrasts-with** [mpc-bounds-convergence](mpc-bounds-convergence.md) — This finite-horizon lemma states the per-period MPC bounds and their coefficient limits $\MPCmin_{T-n}\to\MPCmin$, $\MPCmax_{T-n}\to\MPCmax$; mpc-bounds-convergence is the converged-function counterpart, carrying the same limiting MPCs through to $\cFunc$ itself.
- **assumed-by** [contraction-mapping-consumption-bounds](contraction-mapping-consumption-bounds.md) — thm-cmap presupposes the MPC-bounded operator framework whose threshold horizon $k$ and interval condition $\MPCmax_{T-k}\geq\MPCmaxInf$ are the per-period maximal MPCs characterised here; its proof uses Claim maximal-mpc-at-most-one, which rests on the convergence of $\MPCmax_{T-n}$ to the positive limit $\MPCmax$.
- **assumed-by** [nondegenerate-solution-existence](nondegenerate-solution-existence.md) — The existence proof (thm-convgtobellman) invokes lemm-MPC directly (as cFuncBounds), using $\MPCmax_{T-n}\leq\MPCmax_{T-k}$ and the strictly-positive maximal-MPC limit to keep the bounded Bellman operators nondegenerate.

## Sources

- [BufferStockTheory.md#lemm-MPC](../../BufferStockTheory.md#lemm-MPC)
- [BufferStockTheory.md#eq-cBounds](../../BufferStockTheory.md#eq-cBounds)
- [BufferStockTheory.md#sec-MPCiterproofs](../../BufferStockTheory.md#sec-MPCiterproofs)

## bellman-ddsl correspondence

> *Reserved field — the bellman-ddsl perch/stage mapping is **deferred** for every concept in this atlas; the cross-repo bridge has not been authored. This is not a delivered correspondence.*

- perch: `(deferred)`
- stage: `(deferred)`
