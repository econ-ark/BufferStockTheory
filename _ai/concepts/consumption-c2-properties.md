# Consumption Function is C2 (Lemma)

## Defining equation

Anchor: [`lemm-consC2`](../../BufferStockTheory.md#lemm-consC2)

$$
\text{Let } t<T.\ \text{If } \vFunc_{t}\ \text{is strictly negative, strictly increasing, strictly concave, } \mathbf{C}^{3}\ \text{and satisfies } \lim_{\mNrm\rightarrow 0}\vFunc_{t}(\mNrm)=-\infty,\ \text{then } \cFunc_{t}\ \text{is } \mathbf{C}^{2}.
$$

*If the period-$t$ value function is "nice" (strictly negative, increasing, strictly concave, three-times continuously differentiable, with value diverging to $-\infty$ as resources go to zero), then the period-$t$ consumption function is twice continuously differentiable.*

## Gloss

This lemma is the smoothness engine for the finite-horizon consumption function $\cFunc_{t}$. It assumes that the value function $\vFunc_{t}$ inherited from the next period is "nice" -- strictly negative, strictly increasing, strictly concave, $\mathbf{C}^{3}$, and satisfying $\lim_{\mNrm\to 0}\vFunc_{t}(\mNrm)=-\infty$ -- and concludes that the optimal consumption rule $\cFunc_{t}$ is $\mathbf{C}^{2}$ (twice continuously differentiable). It is a regularity fact about a single period of the normalized recursive problem (`eq-veqnNrmRecBellman`); no impatience inequality is used, only the curvature and boundary behavior of $\vFunc_{t}$ together with CRRA utility.

The proof constructs the end-of-period value function $\mathfrak{v}_{t}(\aNrm):=\DiscFac\Ex_{t}[\PermGroFacRnd_{t+1}^{1-\CRRA}\vFunc_{t+1}(\RNrmByGRnd_{t+1}\aNrm+\tranShkAll_{t+1})]$ (`eq-vfFrackdefn`), which is $\mathbf{C}^{3}$ and diverges to $-\infty$ as saving $\aNrm\to 0$ because the transitory shock can attain zero. Writing $\vFunc_{t}(\mNrm)=\max_{0<\cNrm<\mNrm}[\uFunc(\cNrm)+\mathfrak{v}_{t}(\mNrm-\cNrm)]$, the boundary limits and strict concavity in $\cNrm$ guarantee a unique interior maximizer, so $\cFunc_{t}$ obeys the first-order condition $\uFunc'(\cFunc_{t}(\mNrm))=\mathfrak{v}_{t}'(\mNrm-\cFunc_{t}(\mNrm))$ (`eq-uprimcFOC`). The Implicit Function Theorem then delivers the derivative $\cFunc_{t}'$ as a continuous ratio of $\mathbf{C}^{2}$ pieces (`eq-derivativeConsFunc`), giving $\cFunc_{t}\in\mathbf{C}^{1}$; differentiating once more uses that $\mathfrak{v}_{t}''$ is $\mathbf{C}^{1}$ to show $\cFunc_{t}''$ is continuous, hence $\cFunc_{t}\in\mathbf{C}^{2}$.

The lemma is the inductive step behind the value-function regularity claim (`prop-vfc3`): assuming $\vFunc_{t+1}$ is nice, the lemma makes $\cFunc_{t}$ be $\mathbf{C}^{2}$, and since $\uFunc$ and $\mathfrak{v}_{t}$ are strictly concave both $\cFunc_{t}$ and $\aFunc_{t}$ are strictly increasing, which in turn makes $\vFunc_{t}=\uFunc(\cFunc_{t})+\mathfrak{v}_{t}(\aFunc_{t})$ nice and propagates the hypotheses backward from $\vFunc_{T}=\uFunc$. Combined with `prop-vfc3`, it yields the shape proposition `prop-cfuncprop` (each $\cFunc_{t}$ is $\mathbf{C}^{2}$, increasing, strictly concave); the $\mathbf{C}^{2}$ conclusion is the paper's continuous-differentiability refinement over Theorem 1 of [Carroll and Kimball (1996)](#cite-ckConcavity), who proved concavity but not continuous differentiability.

## Relations

- **requires** [`eq-veqnNrmRecBellman`](../../BufferStockTheory.md#eq-veqnNrmRecBellman) — The lemma concerns the consumption rule of the normalized recursive (Bellman) problem; the proof rewrites that problem as $\vFunc_{t}=\max_{0<\cNrm<\mNrm}[\uFunc(\cNrm)+\mathfrak{v}_{t}(\mNrm-\cNrm)]$.
- **implies** [value-function-c3](value-function-c3.md) — In the induction for prop-vfc3, assuming $\vFunc_{t+1}$ is nice, this lemma gives $\cFunc_{t}\in\mathbf{C}^{2}$, a step in showing $\vFunc_{t}$ is nice; it is the reciprocal of value-function-c3 requiring this lemma at each stage.
- **assumed-by** [consumption-function-c2-concave](consumption-function-c2-concave.md) — The proof of Proposition prop-cfuncprop applies this lemma (via prop-vfc3) to conclude each $\cFunc_{t}$ is $\mathbf{C}^{2}$.
- **contrasts-with** [`cite-ckConcavity`](../../BufferStockTheory.md#cite-ckConcavity) — Carroll and Kimball (1996) proved strict concavity of $\cFunc_{t}$ but not continuous differentiability; this lemma supplies the $\mathbf{C}^{2}$ refinement.

## Sources

- [BufferStockTheory.md#lemm-consC2](../../BufferStockTheory.md#lemm-consC2)
- [BufferStockTheory.md#sec-MPCiterproofs](../../BufferStockTheory.md#sec-MPCiterproofs)
- [BufferStockTheory.md#prop-vfc3](../../BufferStockTheory.md#prop-vfc3)

## bellman-ddsl correspondence

> *Reserved field — the bellman-ddsl perch/stage mapping is **deferred** for every concept in this atlas; the cross-repo bridge has not been authored. This is not a delivered correspondence.*

- perch: `(deferred)`
- stage: `(deferred)`
