# Value Function is C3, Concave, and Diverges at Zero

## Defining equation

Anchor: [`prop-vfc3`](../../BufferStockTheory.md#prop-vfc3)

$$
\text{For each } t,~ \vFunc_{t} \text{ is strictly negative, strictly increasing, strictly concave, } \mathbf{C}^{3} \text{ and satisfies } \lim\limits_{\mNrm\rightarrow 0}~\vFunc_{t}(\mNrm) =-\infty.
$$

*Every finite-horizon normalized value function is strictly negative, strictly increasing, strictly concave, three-times continuously differentiable, and tends to minus infinity as market resources approach zero.*

## Gloss

This property records the shape and smoothness of the period-$t$ normalized value function $\vFunc_{t}$ in the problem with permanent and transitory income shocks (the Friedman-Muth process, Assumption `ass-shocks`): for each $t$, $\vFunc_{t}$ is strictly negative, strictly increasing, strictly concave, three-times continuously differentiable ($\mathbf{C}^{3}$), and satisfies $\lim_{\mNrm\to 0}\vFunc_{t}(\mNrm)=-\infty$. The paper abbreviates this bundle of five properties by saying $\vFunc_{t}$ is "nice." It is a structural statement about a single finite-horizon problem and invokes none of the impatience inequalities; the divergence at zero comes from CRRA utility together with the positive probability of a zero-income (transitory-shock) event.

The proof is a backward induction on the "nice" property. The terminal value function $\vFunc_{T}(\mNrm)=\uFunc(\mNrm)=\mNrm^{1-\CRRA}/(1-\CRRA)$ is nice by inspection (base case). For the inductive step, assume $\vFunc_{t+1}$ is nice; then Lemma `lemm-consC2` yields $\cFunc_{t}\in\mathbf{C}^{2}$, and because both $\uFunc$ and the end-of-period value function $\mathfrak{v}_{t}$ are strictly concave, $\cFunc_{t}$ and $\aFunc_{t}(\mNrm)=\mNrm-\cFunc_{t}(\mNrm)$ are strictly increasing (via the derivative formula `eq-derivativeConsFunc`). Then $\vFunc_{t}(\mNrm)=\uFunc(\cFunc_{t}(\mNrm))+\mathfrak{v}_{t}(\aFunc_{t}(\mNrm))$ is a composition of nice ingredients, so $\vFunc_{t}$ is nice. Property and lemma interlock: the proof consumes `lemm-consC2` at each step, while "nice" is exactly that lemma's hypothesis at the next stage.

Its downstream role is to certify smoothness, not existence. The proof of Proposition `prop-cfuncprop` (consumption function is $\mathbf{C}^{2}$, increasing, strictly concave) opens by invoking this property (cited as "Claim `prop-vfc3`") and applies Lemma `lemm-consC2` to conclude $\cFunc_{t}\in\mathbf{C}^{2}$, so it is one of the two inputs (with the lemma) to that wave-1 shape result. By underwriting that $\mathbf{C}^{2}$ smoothness it ultimately supports the differentiation-based arguments of the Limiting-MPCs lemma (`lemm-MPC`), where the impatience conditions (WRIC, RIC) finally enter.

## Relations

- **requires** [`ass-shocks`](../../BufferStockTheory.md#ass-shocks) — Governing assumption of the section (Friedman-Muth income process); the zero-income event drives the divergence to minus infinity at zero.
- **requires** [`lemm-consC2`](../../BufferStockTheory.md#lemm-consC2) — The inductive step invokes Lemma lemm-consC2 to get a twice-differentiable consumption function; the property's own conclusion is in turn the lemma's hypothesis at the next stage.
- **assumed-by** [consumption-function-c2-concave](consumption-function-c2-concave.md) — The proof of Proposition prop-cfuncprop opens "By Claim prop-vfc3 ..." and applies lemm-consC2; this property is a direct input to that wave-1 shape result.

## Sources

- [BufferStockTheory.md#prop-vfc3](../../BufferStockTheory.md#prop-vfc3)
- [BufferStockTheory.md#lemm-consC2](../../BufferStockTheory.md#lemm-consC2)
- [BufferStockTheory.md#sec-MPCiterproofs](../../BufferStockTheory.md#sec-MPCiterproofs)

## bellman-ddsl correspondence

> *Reserved field — the bellman-ddsl perch/stage mapping is **deferred** for every concept in this atlas; the cross-repo bridge has not been authored. This is not a delivered correspondence.*

- perch: `(deferred)`
- stage: `(deferred)`
