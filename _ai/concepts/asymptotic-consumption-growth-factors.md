# Asymptotic Consumption Growth Factors

## Defining equation

Anchor: [`prop-convgGrowth`](../../BufferStockTheory.md#prop-convgGrowth)

$$
\lim\limits_{\mNrm_{t} \rightarrow \infty} \Ex_{t}[\cLvl_{t+1}/\cLvl_{t}] =  {\APFac} \quad\text{and}\quad \lim\limits_{\mNrm_{t} \rightarrow  0} \Ex_{t}[\cLvl_{t+1}/\cLvl_{t}] =  \infty.
$$

*As market resources grow without bound the expected gross growth factor of consumption converges to the perfect-foresight absolute patience factor; as resources fall toward zero it diverges to infinity.*

## Gloss

This proposition pins down the two extreme-resource limits of the expected one-period consumption growth factor $\Ex_{t}[\cLvl_{t+1}/\cLvl_{t}]$ for the consumer facing labor-income uncertainty. At the rich end ($\mNrm_{t}\to\infty$) the precautionary motive vanishes and the consumer behaves arbitrarily close to the perfect-foresight benchmark, so expected consumption grows at the [absolute patience factor](#absolute-patience-factor) $\APFac=(\Rfree\DiscFac)^{1/\CRRA}$. At the poor end ($\mNrm_{t}\to 0$) the recursive fear of the zero-income event dominates: current consumption is being squeezed toward zero faster than next period's, so the expected growth factor explodes. The result *assumes* the model's bounded shocks ($0<\Min{\tranShkEmp}\leq\tranShkEmp$, $\pZero>0$) and the limiting-MPC machinery; it *implies* that the expected-resource ratio $\Ex_{t}[\mNrm_{t+1}]/\mNrm_{t}$ is likewise unbounded above as $\mNrm_{t}\to 0$ — because the level $\lim_{\mNrm_{t}\to 0}\Ex_{t}[\mNrm_{t+1}]$ stays strictly positive while $\mNrm_{t}\to 0$ — which is the ingredient the target-existence theorems need.

The $\mNrm_{t}\to\infty$ limit is proved by sandwiching the growth factor between expressions built from the minimal and maximal consumption functions and showing both bounds collapse to $\lim_{\mNrm_{t}\to\infty}\PermGroFacRnd_{t+1}\mNrm_{t+1}/\mNrm_{t}$. That common limit evaluates (Equation [](#eq-xtp1toinfty)) to $(\Rfree\DiscFac)^{1/\CRRA}=\APFac$ because the end-of-period-assets function satisfies $\lim_{\mNrm_{t}\to\infty}\aFunc^{\prime}(\mNrm)=\RPFac$ — equivalently $\lim_{\mNrm_{t}\to\infty}\cFunc^{\prime}(\mNrm)=\MPCmin=1-\RPFac$ — and the rescaled transitory shock $\PermGroFacRnd_{t+1}\tranShkAll_{t+1}/\mNrm_{t}$ vanishes; this step relies on the [return patience factor](#return-patience-factor) $\RPFac=\APFac/\Rfree$ being the limiting marginal propensity to save, a fact carried by the converged consumption function ([mpc-bounds-convergence](#mpc-bounds-convergence)) and valid when [return impatience](#RIC) holds. The $\mNrm_{t}\to 0$ limit (Equation [](#eq-consGrowth)) lower-bounds next-period consumption by $\Min{\cFunc}(\tranShkEmp_{t+1}/\pNotZero)$, whose minimum realization is strictly positive since $\Min{\tranShkEmp}>0$, while the denominator $\MPCmax\mNrm_{t}\to 0$; the ratio therefore diverges.

The proposition is the formal engine behind the informal statement in Section [](#sec-individStability) that consumption growth approaches its perfect-foresight value as wealth rises. Its first limit reappears, with the permanent-growth factor stripped out, as the resource-ratio limit $\Ex_{t}[\APFac/\PermGroFacRnd_{t+1}]$ that anchors Part (i) of the individual-target proof ([buffer-stock-target-existence](#buffer-stock-target-existence)); the unboundedness of the ratio $\Ex_{t}[\mNrm_{t+1}]/\mNrm_{t}$ at $\mNrm_{t}\to 0$ (resting on the strictly-positive level limit $\lim_{\mNrm_{t}\to 0}\Ex_{t}[\mNrm_{t+1}]>0$) that it furnishes anchors Part (ii) of both that proof and the pseudo-target proof ([pseudo-target-existence](#pseudo-target-existence)). It is a statement purely about *limits* of growth — it does not by itself establish that a target exists or is unique; the existence theorems add the relevant impatience condition and an intermediate-value argument.

## Relations

- **implies** [absolute-patience-factor](absolute-patience-factor.md) — The high-wealth limit identifies the asymptotic expected consumption growth factor as exactly $\APFac=(\Rfree\DiscFac)^{1/\CRRA}$, the perfect-foresight value.
- **requires** [return-patience-factor](return-patience-factor.md) — The $\mNrm\to\infty$ argument uses $\lim_{\mNrm\to\infty}\aFunc^{\prime}(\mNrm)=\RPFac$ (equivalently $\lim\cFunc^{\prime}=\MPCmin=1-\RPFac$) so that $\lim\PermGroFacRnd_{t+1}\mNrm_{t+1}/\mNrm_{t}=\Rfree\RPFac\DiscFac^{0}=\APFac$.
- **requires** [mpc-bounds-convergence](mpc-bounds-convergence.md) — Supplies the limiting marginal propensities $\lim_{\mNrm\to\infty}\cFunc^{\prime}=\MPCmin$ and $\lim_{\mNrm\to\infty}\cFunc/\mNrm$ that make the end-of-period-assets slope $\aFunc^{\prime}\to\RPFac$ in eq-xtp1toinfty.
- **requires** [return-impatience-condition](return-impatience-condition.md) — The clean $\aFunc^{\prime}\to\RPFac$ form of the high-wealth limit holds when RIC holds; the target proofs separately handle the RIC-failure branch where $\lim\cFunc/\mNrm=0$ instead.
- **assumed-by** [buffer-stock-target-existence](buffer-stock-target-existence.md) — Part (i) of the thm-target proof reuses eq-xtp1toinfty (dropping $\PermGroFac_{t+1}$) to get $\lim_{\mNrm\to\infty}\Ex_{t}[\mNrm_{t+1}/\mNrm_{t}]=\Ex_{t}[\APFac/\PermGroFacRnd_{t+1}]$, and Part (ii) reuses eq-consGrowth for the $\mNrm\to0$ unboundedness of the ratio $\Ex_{t}[\mNrm_{t+1}]/\mNrm_{t}$ (driven by the positive level limit $\lim_{\mNrm\to0}\Ex_{t}[\mNrm_{t+1}]>0$).
- **assumed-by** [pseudo-target-existence](pseudo-target-existence.md) — The thm-MSSBalExists proof inherits the $\mNrm\to0$ unboundedness of $\Ex[\mNrm_{t+1}]/\mNrm_{t}$ established here to supply the below-one/above-one bracketing for its intermediate-value argument.

## Sources

- [BufferStockTheory.md#prop-convgGrowth](../../BufferStockTheory.md#prop-convgGrowth)
- [BufferStockTheory.md#subsec-AppxCgrowthFac](../../BufferStockTheory.md#subsec-AppxCgrowthFac)
- [BufferStockTheory.md#eq-xtp1toinfty](../../BufferStockTheory.md#eq-xtp1toinfty)

## bellman-ddsl correspondence

> *Reserved field — the bellman-ddsl perch/stage mapping is **deferred** for every concept in this atlas; the cross-repo bridge has not been authored. This is not a delivered correspondence.*

- perch: `(deferred)`
- stage: `(deferred)`
