# Joint Failure of Return and Growth Impatience Implies Failure of Finite Value of Autarky

*Short form: **noRICGIC***

## Defining equation

Anchor: [`claim-noRICGIC`](../../BufferStockTheory.md#claim-noRICGIC)

$$
\GPFacRaw \geq 1 \ \wedge\ \RPFac \geq 1 \ \implies\ \DiscFac \PermGroFac^{1-\CRRA}\Ex(\permShk^{1-\CRRA}) \geq 1
$$

*If both growth impatience ($\GPFacRaw<1$) and return impatience ($\RPFac<1$) fail, then the finite value of autarky condition also fails — autarky value is not finite.*

## Gloss

This claim is the formal hinge that lets the [finite value of autarky](#finite-value-of-autarky) (FVAC) condition substitute for the two separate impatience conditions in the existence theory. It *assumes* that both [growth impatience](#growth-impatience-condition) (GIC) fails — the absolute-patience-to-growth ratio satisfies $\GPFacRaw=\APFac/\PermGroFac\geq 1$ — and [return impatience](#return-impatience-condition) (RIC) fails — the [return patience factor](#return-patience-factor) satisfies $\RPFac=(\Rfree\DiscFac)^{1/\CRRA}/\Rfree\geq 1$. It then *implies* that FVAC fails, i.e. $\DiscFac\PermGroFac^{1-\CRRA}\Ex(\permShk^{1-\CRRA})\geq 1$, the negation of the assumption [](#ass-FVAC) that $0<\DiscFac\PermGroFac^{1-\CRRA}\Ex(\permShk^{1-\CRRA})<1$. Contrapositively, FVAC holding *guarantees* that at least one of GIC or RIC holds, so a consumer can never be simultaneously growth-patient and return-patient under FVAC.

The proof is a short algebraic chain. Failure of RIC, $\RPFac\geq 1$, written as $(\Rfree\DiscFac)^{1/\CRRA}/\Rfree\geq 1$ and multiplied through by $\Rfree\PermGroFac^{1-\CRRA}$, rearranges to $\DiscFac\PermGroFac^{1-\CRRA}\geq(\APFac/\PermGroFac)^{\CRRA-1}=\GPFacRaw^{\CRRA-1}$. Because $\CRRA>1$ throughout the paper, failure of GIC ($\GPFacRaw\geq 1$) makes the right-hand side at least one, forcing $\DiscFac\PermGroFac^{1-\CRRA}\geq 1$. The stated conclusion carries the extra factor $\Ex(\permShk^{1-\CRRA})$, which by Jensen's inequality is itself $\geq 1$ when $\CRRA>1$, so the autarky-value product is bounded below by one and FVAC cannot hold.

The economic reading is stark. When *both* impatience conditions fail — the consumer is both return-patient ($\RPFac\geq 1$) and growth-patient ($\GPFacRaw\geq 1$) — FVAC fails, and the paper shows the limiting consumption function then *degenerates*, collapsing to $\cFunc(\mNrm)=0$ or exploding toward $\cFunc(\mNrm)=\infty$ as the horizon recedes (the joint-failure case discussed near `sec-GICdiscussion`). This is exactly why the paper's existence theorems require only WRIC and FVAC — rather than GIC and RIC separately — for a non-degenerate solution: FVAC is the patience condition that rules out this doubly-patient case. (Note: in the *joint-failure* configuration both $\Rfree$ and $\PermGroFac$ sit weakly below $\APFac$, so they do **not** order against each other — joint failure does not by itself imply $\Rfree<\PermGroFac$. The $\Rfree<\APFac<\PermGroFac\Rightarrow\Rfree<\PermGroFac$ chain — finite human wealth failing, limiting human wealth infinite — belongs to a *different*, adjacent case in the paper: growth impatience *holding* while return patience holds, i.e. RIC fails but GIC holds, not the joint failure documented here.) The point that FVAC stops a consumer from becoming *both* growth and return patient is made where the claim is introduced, in the same passage that notes the strong-growth-impatience strengthening is weaker (since $\CRRA>1$) than the stability condition used by [(Ma, Stachurski, and Toda, 2020)](#cite-mstIncFluct).

## Relations

- **requires** [return-impatience-condition](return-impatience-condition.md) — The hypothesis is failure of RIC, $\RPFac\geq 1$; this is the inequality multiplied through by $\Rfree\PermGroFac^{1-\CRRA}$ to start the proof.
- **requires** [growth-impatience-condition](growth-impatience-condition.md) — The hypothesis is failure of GIC, $\GPFacRaw=\APFac/\PermGroFac\geq 1$; with $\CRRA>1$ this makes $\GPFacRaw^{\CRRA-1}\geq 1$, completing the bound.
- **implies** [finite-value-of-autarky](finite-value-of-autarky.md) — Concludes that FVAC (ass-FVAC) fails: $\DiscFac\PermGroFac^{1-\CRRA}\Ex(\permShk^{1-\CRRA})\geq 1$. Contrapositively, FVAC implies at least one of GIC/RIC holds.
- **contrasts-with** [return-patience-factor](return-patience-factor.md) — The doubly-patient case ($\RPFac\geq 1$ with $\GPFacRaw\geq 1$) is precisely the configuration FVAC excludes; under FVAC at least one patience factor must be below one.

## Sources

- [BufferStockTheory.md#claim-noRICGIC](../../BufferStockTheory.md#claim-noRICGIC)
- [BufferStockTheory.md#ass-FVAC](../../BufferStockTheory.md#ass-FVAC)
- [BufferStockTheory.md#sec-GICdiscussion](../../BufferStockTheory.md#sec-GICdiscussion)

## bellman-ddsl correspondence

> *Reserved field — the bellman-ddsl perch/stage mapping is **deferred** for every concept in this atlas; the cross-repo bridge has not been authored. This is not a delivered correspondence.*

- perch: `(deferred)`
- stage: `(deferred)`
