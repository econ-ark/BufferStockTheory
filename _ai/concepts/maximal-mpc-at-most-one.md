# Maximal-MPC Discount Factor Below One

*Short form: **claim-MPCMAXKleq1***

## Defining equation

Anchor: [`eq-MPCMAXKleq1`](../../BufferStockTheory.md#eq-MPCMAXKleq1)

$$
\pZero \DiscFac {(\Rfree (1-\MPCmaxInf))}^{1-\CRRA}   < 1
$$

*Under weak return impatience there is a threshold horizon $k$ such that, for every consumption-share upper bound $\MPCmaxInf$ no larger than the finite-horizon maximal MPC $\MPCmax_{T-k}$, the risk-adjusted growth factor $\pZero \DiscFac (\Rfree (1-\MPCmaxInf))^{1-\CRRA}$ attached to the unconsumed share $(1-\MPCmaxInf)$ is strictly less than one.*

## Gloss

This claim is the lemma that turns the [weak return impatience condition](#WRIC) (WRIC) into the concrete threshold horizon used to build the contraction underlying the stochastic existence proof. It *assumes* WRIC, namely $\pZero^{1/\CRRA}(\Rfree\DiscFac)^{1/\CRRA}/\Rfree<1$, and concludes that there exists a horizon $k$ such that the quantity $\pZero \DiscFac (\Rfree (1-\MPCmaxInf))^{1-\CRRA}$ is below one for every share bound $\MPCmaxInf\in[0,\MPCmax_{T-k}]$. Here $\MPCmax_{T-k}$ is the maximal marginal propensity to consume $k$ periods before the terminal date and $\MPCmax=1-\pZero^{1/\CRRA}\RPFac$ is its limit (Equation [](#eq-MPCmaxDefn)); $\pZero$ is the probability of the zero-income event and $\Rfree(1-\MPCmaxInf)$ is the gross return applied to the share of resources a maximally-impatient consumer would carry forward.

The proof is a one-line algebraic identity followed by a continuity argument. Substituting the definition of the limiting maximal MPC gives $\pZero \DiscFac (\Rfree (1-\MPCmax))^{1-\CRRA}=\pZero^{1/\CRRA}(\Rfree\DiscFac)^{1/\CRRA}/\Rfree$, and this equals exactly the WRIC quantity, so it is $<1$ precisely when WRIC holds. Since the map $\MPCmaxInf\mapsto \pZero \DiscFac (\Rfree (1-\MPCmaxInf))^{1-\CRRA}$ is continuous and increasing in $\MPCmaxInf$, and the finite-horizon MPCs satisfy $\MPCmax_{T-n}\to\MPCmax$ from above with $0<\MPCmax<1$, the strict inequality at the limit propagates to a whole tail: for $k$ large enough the value at $\MPCmax_{T-k}$ — and hence at every smaller $\MPCmaxInf$ — stays below one.

The claim *implies* the well-definedness and strict contractivity of the MPC-bounded Bellman operator. In the proof of the contraction theorem [contraction-mapping-consumption-bounds](#thm-cmap) one first fixes $k$ so that Equation [](#eq-MPCMAXKleq1) holds; the same inequality makes the first term of the contraction modulus, $\Shrinker=\max\{\pZero \DiscFac (\Rfree (1-\MPCmax_{k}))^{1-\CRRA},\beta\Ex\PermGroFacRnd^{1-\CRRA}\}$ in Remark [](#rem-shnkrdef), strictly below one (the finite-value-of-autarky condition handles the second term). Intuitively, WRIC bounds the maximal MPCs away from one strongly enough that even a consumer spending the largest admissible share has a discounted continuation that shrinks, which is what keeps the restricted operator a genuine contraction on the unbounded resource domain.

## Relations

- **requires** [weak-return-impatience-condition](weak-return-impatience-condition.md) — The strict inequality is exactly the WRIC quantity: $\pZero \DiscFac (\Rfree (1-\MPCmax))^{1-\CRRA}=\pZero^{1/\CRRA}(\Rfree\DiscFac)^{1/\CRRA}/\Rfree<1$ holds iff WRIC (Assumption #WRIC) holds.
- **implied-by** [`WRIC`](../../BufferStockTheory.md#WRIC) — Combined with continuity and monotonicity in $\MPCmaxInf$ plus $\MPCmax_{T-n}\to\MPCmax$, WRIC yields the threshold horizon $k$ for which the inequality holds on the whole interval $[0,\MPCmax_{T-k}]$.
- **assumed-by** [contraction-mapping-consumption-bounds](contraction-mapping-consumption-bounds.md) — The proof of thm-cmap opens by fixing $k$ such that eq-MPCMAXKleq1 holds, which is what makes $\TMap^{\MPCminInf,\MPCmaxInf}$ well-defined and the operator a contraction.
- **assumed-by** [boyd-weighted-contraction](boyd-weighted-contraction.md) — Reciprocal edge: verifying Boyd's discounting condition (3) for $\TMap^{\MPCminInf,\MPCmaxInf}$ uses this WRIC-dependent bound to fix $k$ large enough that $\pZero\DiscFac(\Rfree(1-\MPCmaxInf))^{1-\CRRA}<\Shrinker$.
- **implies** [`rem-shnkrdef`](../../BufferStockTheory.md#rem-shnkrdef) — This claim forces the first argument of the contraction modulus $\Shrinker=\max\{\pZero \DiscFac (\Rfree (1-\MPCmax_{k}))^{1-\CRRA},\beta\Ex\PermGroFacRnd^{1-\CRRA}\}$ to be strictly less than one.
- **requires** [`eq-MPCmaxDefn`](../../BufferStockTheory.md#eq-MPCmaxDefn) — The algebraic identity in the proof substitutes the definition of the limiting maximal MPC $\MPCmax=1-\pZero^{1/\CRRA}\RPFac$ (Equation eq-MPCmaxDefn).

## Sources

- [BufferStockTheory.md#claim-MPCMAXKleq1](../../BufferStockTheory.md#claim-MPCMAXKleq1)
- [BufferStockTheory.md#eq-MPCMAXKleq1](../../BufferStockTheory.md#eq-MPCMAXKleq1)
- [BufferStockTheory.md#thm-cmap](../../BufferStockTheory.md#thm-cmap)

## bellman-ddsl correspondence

> *Reserved field — the bellman-ddsl perch/stage mapping is **deferred** for every concept in this atlas; the cross-repo bridge has not been authored. This is not a delivered correspondence.*

- perch: `(deferred)`
- stage: `(deferred)`
