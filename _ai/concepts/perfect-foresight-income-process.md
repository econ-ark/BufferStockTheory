# Perfect Foresight Income Process

## Defining equation

Anchor: [`ass-pfincome`](../../BufferStockTheory.md#ass-pfincome)

$$
\pZero=0 \quad\text{and}\quad \tranShkEmpMin=\tranShkEmpMax=\bar{\tranShkEmp}=\permShkIndMin=\permShkIndMax=1
$$

*The zero-income probability is switched off ($\pZero=0$) and every shock bound is pinned to one, so $\permShk\equiv1$ and $\tranShkAll\equiv1$ and income is known with certainty — the perfect-foresight benchmark.*

## Gloss

This assumption fixes what the paper means, mathematically, by "perfect foresight": it is the degenerate case of the [Friedman-Muth income process](#friedman-muth-income-process) in which the zero-income probability is switched off ($\pZero=0$) and all four shock bounds are pinned to one, forcing the permanent and transitory shocks to be degenerate at their unit means ($\permShk\equiv1$, $\tranShkAll\equiv1$). Income then evolves deterministically: permanent income grows at the fixed factor $\PermGroFac$ each period and noncapital income equals permanent income exactly. The paper maintains this assumption "in force" throughout the Perfect Foresight Benchmarks subsection [](#subsec-PFBbenchmark), using the resulting closed forms as the reference point against which buffer-stock (precautionary) behavior under uncertainty is measured.

Degeneracy strips the expectation operators out of the model's conditions and yields analytic solutions. The finite-value-of-autarky condition loses its shock term and reduces to the [perfect-foresight finite value of autarky](#pf-finite-value-of-autarky) condition $\DiscFac\PermGroFac^{1-\CRRA}<1$ (Equation [](#eq-PFFVAC)). The consumption Euler equation holds with equality every period, giving the deterministic growth factor $\cLvl_{t+1}/\cLvl_{t}=(\Rfree\DiscFac)^{1/\CRRA}=\APFac$ (Equation [](#eq-cGroFac)). Human wealth becomes the geometric present discounted value of certain future income (Equation [](#eq-HDef)), finite exactly when [finite human wealth](#finite-human-wealth-condition) holds ($\RNrmByG^{-1}=\PermGroFac/\Rfree<1$). The unconstrained perfect-foresight consumption function is then linear in total wealth, $\bar{\cFunc}(\mNrm)=(\mNrm+\hNrm-1)\MPCmin$ with $\MPCmin=1-\RPFac$ (Equations [](#eq-cFuncPFUnc), [](#eq-MPCminDef)) — positive precisely when [return impatience](#return-impatience-condition) holds.

Several benchmark results are stated under this assumption. Proposition [](#prop-pfUCFHWC) shows the unconstrained perfect-foresight limit is non-degenerate if and only if finite human wealth and return impatience both hold — return impatience keeps $\MPCmin>0$ so the consumer does not save everything, while finite human wealth keeps the wealth intercept finite so the consumer does not borrow without bound against it. Proposition [](#prop-PFCExist) delivers the perfect-foresight constrained limiting consumption function, and the perfect-foresight patience chain (Claim [](#claim-PFConspC)) — under finite human wealth, growth impatience implies PF-FVAC implies return impatience — is derived entirely within this benchmark. Removing the zero-income event is precisely what removes the natural borrowing constraint that the [Friedman-Muth process](#friedman-muth-income-process) supplies, which is why studying a *constrained* perfect-foresight problem requires imposing a liquidity constraint by hand.

## Relations

- **special-case-of** [friedman-muth-income-process](friedman-muth-income-process.md) — Perfect foresight is the degenerate boundary of the Friedman-Muth process — $\pZero$ set to $0$ and all shock bounds pinned to one ($\permShk\equiv1$, $\tranShkAll\equiv1$); it sits just outside the $\pZero>0$ interior the stochastic process maintains.
- **assumed-by** [pf-unconstrained-requires-fhwc](pf-unconstrained-requires-fhwc.md) — Proposition prop-pfUCFHWC (unconstrained perfect-foresight non-degeneracy iff finite human wealth and return impatience) is stated with this income process in force.
- **assumed-by** [pf-constrained-solution-exists](pf-constrained-solution-exists.md) — The perfect-foresight constrained limiting consumption function (prop-PFCExist) is derived under this assumption, with an imposed liquidity constraint replacing the natural one that the zero-income event would otherwise supply.
- **assumed-by** [pf-finite-value-of-autarky](pf-finite-value-of-autarky.md) — Under this process the finite-value-of-autarky condition loses its expectation term and reduces to PF-FVAC, $\DiscFac\PermGroFac^{1-\CRRA}<1$ (eq-PFFVAC).
- **assumed-by** [pf-consumption-function-properties](pf-consumption-function-properties.md) — The perfect-foresight patience chain GICRaw implies PF-FVAC implies RIC (claim-PFConspC, under finite human wealth) is a perfect-foresight benchmark result derived within this assumption.

## Sources

- [BufferStockTheory.md#ass-pfincome](../../BufferStockTheory.md#ass-pfincome)
- [BufferStockTheory.md#subsec-PFBbenchmark](../../BufferStockTheory.md#subsec-PFBbenchmark)
- [BufferStockTheory.md#eq-cFuncPFUnc](../../BufferStockTheory.md#eq-cFuncPFUnc)

## bellman-ddsl correspondence

> *Reserved field — the bellman-ddsl perch/stage mapping is **deferred** for every concept in this atlas; the cross-repo bridge has not been authored. This is not a delivered correspondence.*

- perch: `(deferred)`
- stage: `(deferred)`
