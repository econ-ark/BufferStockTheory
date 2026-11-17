# Convex-Negative Function Has Increasing Ratio (Consumption-Ratio Monotonicity)

## Defining equation

Anchor: [`claim-rationondec`](../../BufferStockTheory.md#claim-rationondec)

$$
\fFunc\ \text{convex and}\ \fFunc<0\ \text{on}\ (0,\lambda)\ \implies\ \frac{\fFunc(s)}{s}\ \text{is increasing on}\ (0,\lambda)
$$

*If a function is convex and strictly negative on an interval starting at the origin, then its ray-slope $\fFunc(s)/s$ rises with $s$; applied to $-\cFunc$ this makes the consumption ratio $\cFunc(\mNrm)/\mNrm$ non-increasing.*

## Gloss

This claim is a self-contained real-analysis lemma whose only job is to convert a curvature-plus-sign hypothesis into monotonicity of a ray-slope. It *assumes* that $\fFunc$ is convex and that $\fFunc<0$ throughout an interval $(0,\lambda)$ anchored at the origin, and it *implies* that the ratio $\fFunc(s)/s$ — the slope of the chord from the origin to the point $(s,\fFunc(s))$ — is increasing on that interval. The proof fixes a small $\alpha\in(0,x_{1})$, defines the shifted convex function $F(x)=\fFunc(x)-\fFunc(\alpha)$ with $F(\alpha)=0$, and uses convexity through $x_{1}=t\alpha+(1-t)x_{2}$ to get $F(x_{1})\le(1-t)F(x_{2})$, which is exactly the statement that $F(s)/s$ is increasing; adding back the negative constant term $\fFunc(\alpha)/s$ (which is itself increasing in $s$ because $\fFunc(\alpha)<0$) preserves the inequality, so $\fFunc(s)/s$ is increasing too. The strict negativity matters only in this last step: it is what makes the additive term $\fFunc(\alpha)/s$ help rather than hurt.

The lemma is stated abstractly precisely so it can be applied to the *negated* consumption function. The limiting consumption function $\cFunc$ is concave on $\Reals_{++}$ (so $-\cFunc$ is convex) and strictly positive there (so $-\cFunc<0$), with strict positivity supplied by Remark [limiting-consumption-strictly-positive](#limiting-consumption-strictly-positive). Instantiating the claim with $\fFunc=-\cFunc$ therefore makes $-\cFunc(\mNrm)/\mNrm$ increasing, i.e. the consumption ratio $\cFunc(\mNrm)/\mNrm$ is *non-increasing* in market resources; combined with feasibility ($\cFunc(\mNrm)\le\mNrm$, Equation [](#eq-statCbellman)) this pins the ratio inside $[0,1]$. Economically this is the statement that the average propensity to consume falls as a household grows wealthier, the natural counterpart of a concave consumption function passing through the origin.

Two downstream results lean on this monotonicity. First, because $\cFunc(\mNrm)/\mNrm$ is non-increasing and bounded in $[0,1]$, the one-sided limits $\MPCmaxmax=\lim_{\mNrm\downarrow0}\cFunc(\mNrm)/\mNrm$ and $\MPCminmin=\lim_{\mNrm\to\infty}\cFunc(\mNrm)/\mNrm$ exist with $0\le\MPCminmin\le\MPCmaxmax\le1$; these limits are then identified with the limiting marginal propensities $\MPCmax$ and $\MPCmin$ in the proof of the MPC-bounds lemma [mpc-bounds-convergence](#mpc-bounds-convergence). Second, the bound $\Delta_{\epsilon}\cFunc(\mNrm_{t})/\epsilon\le\cFunc(\mNrm_{t})/\mNrm_{t}<1$ — which says a finite forward difference of consumption never exceeds the (decreasing) ratio — is the step that makes the expected-market-resources difference strictly decreasing in the stable-target analysis [consumption-c2-properties](#consumption-c2-properties). The claim is thus small but load-bearing connective tissue between concavity of $\cFunc$ and the existence and ordering of the model's MPC and target objects.

## Relations

- **requires** [limiting-consumption-strictly-positive](limiting-consumption-strictly-positive.md) — When applied to $\fFunc=-\cFunc$, the hypothesis $\fFunc<0$ on $(0,\lambda)$ is exactly strict positivity of $\cFunc$ on $\Reals_{++}$, supplied by Remark remark-cStatStrctPos.
- **requires** [consumption-function-c2-concave](consumption-function-c2-concave.md) — The convexity hypothesis on $\fFunc$ is met by taking $\fFunc=-\cFunc$; this needs $\cFunc$ concave on $\Reals_{++}$, the property established in consumption-function-c2-concave (Proposition prop-cfuncprop), invoked just before this claim.
- **assumed-by** [mpc-bounds-convergence](mpc-bounds-convergence.md) — The proof of Lemma lemma-MPCBoundsConvg invokes this claim to make $\cFunc(\mNrm)/\mNrm$ non-increasing and bounded, then defines $\MPCmaxmax,\MPCminmin$ as its limits at $0$ and $\infty$.
- **assumed-by** [consumption-c2-properties](consumption-c2-properties.md) — The stable-target argument (Lemma lemm-consC2) uses $\Delta_{\epsilon}\cFunc(\mNrm_{t})/\epsilon\le\cFunc(\mNrm_{t})/\mNrm_{t}<1$, which holds because this claim makes the ratio decreasing.
- **requires** [`eq-statCbellman`](../../BufferStockTheory.md#eq-statCbellman) — Feasibility $\cFunc(\mNrm)\le\mNrm$ from Equation eq-statCbellman combines with the claim's monotonicity to confine the ratio to $[0,1]$.

## Sources

- [BufferStockTheory.md#claim-rationondec](../../BufferStockTheory.md#claim-rationondec)
- [BufferStockTheory.md#sec-realanalysis](../../BufferStockTheory.md#sec-realanalysis)
- [BufferStockTheory.md#lemma-MPCBoundsConvg](../../BufferStockTheory.md#lemma-MPCBoundsConvg)

## bellman-ddsl correspondence

> *Reserved field — the bellman-ddsl perch/stage mapping is **deferred** for every concept in this atlas; the cross-repo bridge has not been authored. This is not a delivered correspondence.*

- perch: `(deferred)`
- stage: `(deferred)`
