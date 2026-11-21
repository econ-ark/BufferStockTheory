# Perfect Foresight Finite Value of Autarky Condition (PF-FVAC)

## Defining equation

Anchor: [`eq-PFFVAC`](../../BufferStockTheory.md#eq-PFFVAC)

$$
\DiscFac \PermGroFac^{1-\CRRA} < 1
$$

*The discount factor times the permanent-income growth factor raised to $1-\CRRA$ is below one — the perfect-foresight specialization of the finite-value-of-autarky requirement.*

## Gloss

Under the perfect-foresight income process (Assumption [](#ass-pfincome): $\pZero=0$ and all shocks degenerate at one), the general [finite value of autarky](#finite-value-of-autarky) condition loses its expectation term: the paper says FVAC "reduces to a 'perfect foresight finite value of autarky' condition", $\DiscFac\PermGroFac^{1-\CRRA}<1$. The operational content is that the discounted utility of "autarky" — consuming exactly permanent income every period — stays finite as the horizon extends: each period's utility contribution scales with $(\PermGroFac^{1-\CRRA})$ per period of growth and is discounted by $\DiscFac$, so the value of autarky is a geometric sum with ratio $\DiscFac\PermGroFac^{1-\CRRA}$, finite exactly when that ratio is below one. The paper's Symbols table names this ratio the PF Value of Autarky Factor $\beth\equiv\DiscFac\PermGroFac^{1-\CRRA}$ and reports $\beth=0.932$ at the baseline calibration, so PF-FVAC comfortably holds there. An equivalent patience-factor form, used as the diagonal of the inequalities diagram (Figure [](#fig-RelatePFGICFHWCRICPFFVAC)), is $\APFac < \Rfree^{1/\CRRA}\PermGroFac^{1-1/\CRRA}$.

Logically, PF-FVAC is the middle node of the perfect-foresight patience chain [pf-consumption-function-properties](#pf-consumption-function-properties) (Claim [](#claim-PFConspC)): maintaining [finite human wealth](#finite-human-wealth-condition), [growth impatience](#growth-impatience-condition) implies PF-FVAC (Equation [](#eq-GICandFHWCimplyPFFVAC): $\APFac<\PermGroFac<\Rfree$ delivers $\RPFac<\PermGroFac/\Rfree<(\PermGroFac/\Rfree)^{1-1/\CRRA}<1$), and PF-FVAC in turn implies [return impatience](#return-impatience-condition) (Equation [](#eq-FHWCandPFFVACimplyRIC): dividing the autarky inequality by $\Rfree$ gives $\APFac/\Rfree<(\PermGroFac/\Rfree)^{1-1/\CRRA}$, whose right side is below one under FHWC). Both implications are one-way, and PF-FVAC is *not* necessary for a well-behaved perfect-foresight problem: the paper notes that RIC and FHWC "can hold while the finite value of autarky under perfect foresight fails", giving the example $\PermGroFac=0$ — a standard cake-eating problem with a non-degenerate solution under return impatience — and Proposition [](#prop-pfUCFHWC) shows nondegeneracy of the unconstrained perfect-foresight limit needs only FHWC and RIC.

Against the uncertainty version of the condition, PF-FVAC is the weaker requirement: since $\CRRA>1$ makes $\permShk\mapsto\permShk^{1-\CRRA}$ convex and the permanent shock has mean one, Jensen's inequality gives $\Ex[\permShk^{1-\CRRA}]\geq 1$, so the FVAC quantity $\DiscFac\PermGroFac^{1-\CRRA}\Ex[\permShk^{1-\CRRA}]$ (the Value of Autarky Factor $\DiscAltuAdj$, $0.941$ at baseline versus $\beth=0.932$) weakly exceeds the PF-FVAC quantity — matching the paper's summary that "FVAC is stronger than PF-FVAC". The condition earns its keep in the taxonomy of parameter regions: in the analysis of the case where FHWC fails but RIC holds, the paper traverses the extended inequalities diagram (Figure [](#fig-Inequalities)) to show that infinite human wealth together with FVAC implies that PF-FVAC holds and that $\APFac<\PermGroFac$ — i.e. growth impatience — so PF-FVAC is the hinge through which the autarky-value conditions discipline the exotic parameter configurations.

## Relations

- **special-case-of** [finite-value-of-autarky](finite-value-of-autarky.md) — PF-FVAC is FVAC evaluated under the perfect-foresight income process (ass-pfincome); conversely FVAC implies PF-FVAC unconditionally, since Jensen gives $\Ex[\permShk^{1-\CRRA}]\geq1$ for the mean-one shock with $\CRRA>1$ ("FVAC is stronger than PF-FVAC").
- **implied-by** [growth-impatience-condition](growth-impatience-condition.md) — Jointly with FHWC: eq-GICandFHWCimplyPFFVAC shows GICRaw ($\APFac<\PermGroFac$) plus $\PermGroFac<\Rfree$ delivers $\RPFac<(\PermGroFac/\Rfree)^{1-1/\CRRA}$, which is PF-FVAC in patience-factor form.
- **implies** [return-impatience-condition](return-impatience-condition.md) — Under FHWC: dividing the PF-FVAC inequality by $\Rfree$ gives $\APFac/\Rfree<(\PermGroFac/\Rfree)^{1-1/\CRRA}<1$ (eq-FHWCandPFFVACimplyRIC), i.e. RIC.
- **implied-by** [pf-consumption-function-properties](pf-consumption-function-properties.md) — Reciprocal edge: claim-PFConspC is the two-part chain (FHWC maintained) GICRaw ⇒ PF-FVAC ⇒ RIC, in which PF-FVAC is the middle node; its first half derives PF-FVAC.
- **requires** [`ass-pfincome`](../../BufferStockTheory.md#ass-pfincome) — The condition is stated for the perfect-foresight income process ($\pZero=0$, degenerate unit shocks); with uncertainty the relevant condition is the full FVAC.
- **contrasts-with** [pf-unconstrained-requires-fhwc](pf-unconstrained-requires-fhwc.md) — PF-FVAC is not necessary for nondegeneracy: prop-pfUCFHWC characterizes the PF-unconstrained limit by FHWC and RIC alone, and the $\PermGroFac=0$ cake-eating example satisfies both while PF-FVAC fails.

## Sources

- [BufferStockTheory.md#PFFVAC](../../BufferStockTheory.md#PFFVAC)
- [BufferStockTheory.md#eq-PFFVAC](../../BufferStockTheory.md#eq-PFFVAC)
- [BufferStockTheory.md#subsec-PFBdiscussion](../../BufferStockTheory.md#subsec-PFBdiscussion)

## bellman-ddsl correspondence

> *Reserved field — the bellman-ddsl perch/stage mapping is **deferred** for every concept in this atlas; the cross-repo bridge has not been authored. This is not a delivered correspondence.*

- perch: `(deferred)`
- stage: `(deferred)`
