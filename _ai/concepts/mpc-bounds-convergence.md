# Limiting MPC Bounds (Convergence)

## Defining equation

Anchor: [`lemma-MPCBoundsConvg`](../../BufferStockTheory.md#lemma-MPCBoundsConvg)

$$
\lim\limits_{m\rightarrow \infty} \cFunc (m)/m =\MPCmin m \quad\text{and}\quad \lim\limits_{m\rightarrow 0} \cFunc (m)/m =\MPCmax m
$$

*For the limiting (converged) consumption function, the consumption share approaches the minimal MPC as market resources grow without bound and the maximal MPC as they shrink to zero.*

## Gloss

This lemma verifies that the limiting non-degenerate consumption function $\cFunc$ satisfies the same marginal-propensity-to-consume bounds that hold for each finite-horizon function $\cFunc_{T-n}$. Under [weak return impatience](#WRIC) (WRIC), the share $\cFunc(\mNrm)/\mNrm$ tends to the minimal MPC $\MPCmin = 1-\APFac/\Rfree$ as $\mNrm\rightarrow\infty$ and to the maximal MPC $\MPCmax = 1-\pZero^{1/\CRRA}\APFac/\Rfree$ as $\mNrm\downarrow 0$. It is the converged-function counterpart of the finite-horizon "Limiting MPCs" lemma (`lemm-MPC`), which establishes the period-by-period bounds $\MPCmin_{T-n}\mNrm\le\cFunc_{T-n}(\mNrm)\le\MPCmax_{T-n}\mNrm$ and the convergence of the bound coefficients $\MPCmin_{T-n}\to\MPCmin$, $\MPCmax_{T-n}\to\MPCmax$; this lemma carries the property through the pointwise limit to $\cFunc$ itself.

The proof has two parts. First it establishes that $\cFunc$ is concave on $\Reals_{++}$: because WRIC delivers pointwise convergence $\cFunc_{T-n}\rightarrow\cFunc$ (Theorem [](#Sufficient-Conditions-For-non-degenerate-Solution)) and $\Reals_{++}$ is open, the pointwise limit of concave functions is concave by Theorem 10.8 of [(Rockafellar, 1972)](#cite-Rockafellar1972). Concavity together with $\cFunc(\mNrm)>0$ (Remark [limiting-consumption-strictly-positive](#limiting-consumption-strictly-positive)) makes the share $\cFunc(\mNrm)/\mNrm$ non-increasing and bounded in $[0,1]$, so the two one-sided limits $\MPCmaxmax:=\lim_{\mNrm\downarrow 0}\cFunc(\mNrm)/\mNrm$ and $\MPCminmin:=\lim_{\mNrm\rightarrow\infty}\cFunc(\mNrm)/\mNrm$ exist. Second, feeding these limits through the stationary Euler equation (Claim [](#eq-EuelrStatC)) and letting $\mNrm\rightarrow\infty$ pins $\MPCminmin=1-\APFac/\Rfree=\MPCmin$; the symmetric $\mNrm\downarrow 0$ argument gives $\MPCmaxmax=1-\pZero^{1/\CRRA}\APFac/\Rfree=\MPCmax$.

The lemma's two outputs are used separately downstream. The concavity (hence continuity) of $\cFunc$ is what licenses the stability analysis of the converged rule, and the limiting consumption share supplies the asymptotic consumption-growth bounds used in establishing existence of the buffer-stock target and pseudo-target: when [return impatience](#RIC) holds the high-wealth ratio is driven by $\cFunc(\mNrm)/\mNrm\rightarrow\MPCmin$, and when RIC fails the same proof branch instead uses $\cFunc(\mNrm)/\mNrm\rightarrow 0$. The lemma itself only assumes WRIC, so a priori $\MPCmin$ could be zero; it is exactly when RIC additionally holds that $\MPCmin>0$, giving the strict sandwich $0<\MPCmin\leq\cFunc(\mNrm)/\mNrm<1$ on which the target results rely.

## Relations

- **requires** [weak-return-impatience-condition](weak-return-impatience-condition.md) — The lemma's stated hypothesis is WRIC (Assumption WRIC); it is what delivers the pointwise convergence $\cFunc_{T-n}\to\cFunc$ used to inherit concavity and the MPC bounds.
- **implied-by** [nondegenerate-solution-existence](nondegenerate-solution-existence.md) — The proof builds on the existence theorem (thm-convgtobellman / Sufficient-Conditions-For-non-degenerate-Solution), which under WRIC gives the pointwise limit $\cFunc_{T-n}\to\cFunc$ that this lemma characterizes.
- **contrasts-with** [`lemm-MPC`](../../BufferStockTheory.md#lemm-MPC) — lemm-MPC ("Limiting MPCs") states the finite-horizon per-period bounds $\MPCmin_{T-n}\mNrm\le\cFunc_{T-n}(\mNrm)\le\MPCmax_{T-n}\mNrm$ and the convergence $\MPCmin_{T-n}\to\MPCmin$; this lemma is its converged-function counterpart, verifying the limiting $\cFunc$ shares the same limiting MPCs.
- **contrasts-with** [return-impatience-condition](return-impatience-condition.md) — WRIC alone leaves open $\MPCmin=0$; adding RIC makes $\MPCmin>0$, yielding the strict sandwich $0<\MPCmin\leq\cFunc(\mNrm)/\mNrm<1$ (eq-MPCminDef together with this lemma, BufferStockTheory.md line ~2581/2680).
- **assumed-by** [buffer-stock-target-existence](buffer-stock-target-existence.md) — The proof of thm-target uses this lemma for concavity/continuity of $\cFunc$ and for $\lim_{\mNrm\to\infty}\cFunc(\mNrm)/\mNrm=\MPCmin$ (RIC holds) or $\to 0$ (RIC fails) when establishing the buffer-stock target.
- **assumed-by** [pseudo-target-existence](pseudo-target-existence.md) — The pseudo-target proof (subsubsec-AppxPseudoSS) uses the same converged-function properties: concavity and the limiting consumption share underpin the asymptotic growth-factor argument.

## Sources

- [BufferStockTheory.md#lemma-MPCBoundsConvg](../../BufferStockTheory.md#lemma-MPCBoundsConvg)
- [BufferStockTheory.md#sec-ApndxConcaveCFunc](../../BufferStockTheory.md#sec-ApndxConcaveCFunc)
- [BufferStockTheory.md#remark-cStatStrctPos](../../BufferStockTheory.md#remark-cStatStrctPos)

## bellman-ddsl correspondence

> *Reserved field — the bellman-ddsl perch/stage mapping is **deferred** for every concept in this atlas; the cross-repo bridge has not been authored. This is not a delivered correspondence.*

- perch: `(deferred)`
- stage: `(deferred)`
