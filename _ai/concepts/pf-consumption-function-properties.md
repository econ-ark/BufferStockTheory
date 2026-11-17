# Perfect-Foresight Patience-Condition Chain: FHWC + GICRaw ⇒ PF-FVAC ⇒ RIC

*Short form: **PFConspC***

## Defining equation

Anchor: [`claim-PFConspC`](../../BufferStockTheory.md#claim-PFConspC)

$$
\RNrmByG^{-1}<1 \;\Longrightarrow\; \big(\text{GICRaw}\Rightarrow\text{PFFVAC}\big)\ \wedge\ \big(\text{PFFVAC}\Rightarrow\text{RIC}\big)
$$

*Maintaining finite human wealth ($\RNrmByG^{-1}<1$): growth impatience implies the perfect-foresight finite value of autarky (PF-FVAC), and PF-FVAC implies return impatience.*

## Gloss

This claim (stated as a `prf:property`, [claim-PFConspC](#claim-PFConspC)) orders three of the paper's patience conditions for the perfect-foresight income process (Assumption [](#ass-pfincome)), under the maintained hypothesis of [finite human wealth](#finite-human-wealth-condition) (FHWC, $\RNrmByG^{-1}=\PermGroFac/\Rfree<1$). It *assumes* FHWC throughout and asserts two one-directional implications: first, that [growth impatience](#growth-impatience-condition) (GICRaw, $\APFac<\PermGroFac$) implies the perfect-foresight [finite value of autarky](#finite-value-of-autarky) — PF-FVAC, the condition [](#PFFVAC) $\DiscFac\PermGroFac^{1-\CRRA}<1$, the perfect-foresight reduction of the general (uncertainty) FVAC; and second, that PF-FVAC in turn implies [return impatience](#return-impatience-condition) (RIC, $\RPFac<1$, equivalently $\APFac<\Rfree$).

The proof (Appendix [](#subsec-PFBProofs)) is a short chain of inequalities resting entirely on FHWC plus $\CRRA>1$. For the first implication, GICRaw and FHWC give $\APFac<\PermGroFac<\Rfree$, so dividing by $\Rfree$ yields $\RPFac<\PermGroFac/\Rfree<(\PermGroFac/\Rfree)^{1-1/\CRRA}<1$ (Equation [](#eq-GICandFHWCimplyPFFVAC)); the middle step uses that $0\le\PermGroFac/\Rfree<1$ is raised to a power $1-1/\CRRA\in(0,1)$; the inequality $\RPFac<(\PermGroFac/\Rfree)^{1-1/\CRRA}$ — equivalently $\APFac<\Rfree^{1/\CRRA}\PermGroFac^{1-1/\CRRA}$ — is exactly PFFVAC, while the concluding $<1$ is FHWC. For the second, dividing the perfect-foresight autarky inequality by $\Rfree$ gives $\APFac/\Rfree<(\PermGroFac/\Rfree)^{1-1/\CRRA}$ (Equation [](#eq-FHWCandPFFVACimplyRIC)), whose right side is strictly below $1$ under FHWC, delivering $\RPFac<1$, i.e. RIC.

The economic payoff, noted immediately after the claim, is that imposing FHWC makes GICRaw a *sufficient* condition for a non-degenerate limiting solution: FVAC and RIC both follow, and by Proposition [](#prop-pfUCFHWC) the perfect-foresight unconstrained problem has a non-degenerate limit exactly when FHWC and RIC hold. The implications are strict and one-way. RIC together with FHWC need *not* yield FVAC — the canonical counterexample is $\PermGroFac=0$ (a 'cake-eating' problem), which has a non-degenerate solution under RIC while FVAC fails. The chain is the perfect-foresight backbone for the uncertainty-model results: Claims [](#VAFacDefn)–[](#claim-PFConspC) together pin down how finite value of autarky, return impatience and growth impatience interrelate once uncertainty is present.

## Relations

- **requires** [finite-human-wealth-condition](finite-human-wealth-condition.md) — FHWC ($\PermGroFac/\Rfree<1$) is the maintained hypothesis for both implications; it is what makes $(\PermGroFac/\Rfree)^{1-1/\CRRA}<1$ and supplies the strict inequalities in eq-GICandFHWCimplyPFFVAC and eq-FHWCandPFFVACimplyRIC.
- **implies** [finite-value-of-autarky](finite-value-of-autarky.md) — First implication: under FHWC, GICRaw ($\APFac<\PermGroFac$) yields PFFVAC ($\DiscFac\PermGroFac^{1-\CRRA}<1$, Equation eq-PFFVAC), the perfect-foresight reduction of FVAC, via eq-GICandFHWCimplyPFFVAC.
- **implies** [return-impatience-condition](return-impatience-condition.md) — Second implication: under FHWC, PFFVAC implies RIC ($\RPFac<1$) via eq-FHWCandPFFVACimplyRIC; hence GICRaw+FHWC also delivers RIC.
- **requires** [growth-impatience-condition](growth-impatience-condition.md) — GICRaw ($\APFac<\PermGroFac$) is the antecedent of the first implication; combined with FHWC it makes growth impatience sufficient for non-degeneracy.
- **requires** [pf-unconstrained-requires-fhwc](pf-unconstrained-requires-fhwc.md) — The claim's nondegeneracy corollary invokes Proposition prop-pfUCFHWC, which gives non-degeneracy of the PF-unconstrained limit iff FHWC and RIC; combined with this claim's two implications it makes GICRaw+FHWC sufficient, because FVAC and RIC then follow.
- **contrasts-with** [`prop-PFCExist`](../../BufferStockTheory.md#prop-PFCExist) — The implications are one-way: RIC+FHWC need not give FVAC (counterexample $\PermGroFac=0$, cake-eating). The constrained case prop-PFCExist instead makes GICRaw the relevant condition when RIC fails.

## Sources

- [BufferStockTheory.md#claim-PFConspC](../../BufferStockTheory.md#claim-PFConspC)
- [BufferStockTheory.md#subsec-PFBProofs](../../BufferStockTheory.md#subsec-PFBProofs)
- [BufferStockTheory.md#PFFVAC](../../BufferStockTheory.md#PFFVAC)

## bellman-ddsl correspondence

> *Reserved field — the bellman-ddsl perch/stage mapping is **deferred** for every concept in this atlas; the cross-repo bridge has not been authored. This is not a delivered correspondence.*

- perch: `(deferred)`
- stage: `(deferred)`
