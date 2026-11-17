# Friedman-Muth Income Process (Income Shocks Assumption)

## Defining equation

Anchor: [`ass-shocks`](../../BufferStockTheory.md#ass-shocks)

$$
\Ex[\permShk_{t}]=\Ex[\tranShkEmp_{t}]=1,\quad \permShk_{t}\in[\permShkIndMin,\permShkIndMax],\quad \tranShkAll_{t}=\begin{cases}0 & \text{with prob. }\pZero>0\\ \tranShkEmp_{t}/\pNotZero & \text{with prob. }\pNotZero\end{cases}
$$

*Income is iid permanent times transitory: the permanent shock $\permShk$ has mean one and compact positive support, and the transitory shock is a zero-income event (value $0$) with probability $\pZero>0$, else a mean-one bounded positive draw $\tranShkEmp$ rescaled by $1/\pNotZero$.*

## Gloss

This is the maintained income process for the paper's problem with uncertainty — a stochastic implementation of Friedman's permanent-income hypothesis. Noncapital income is the product of a permanent component and a transitory component, both iid across time. The permanent shock $\permShk_{t}$ has mean one ($\Ex[\permShk_{t}]=1$) and lives on a compact positive interval $[\permShkIndMin,\permShkIndMax]$ whose bounds straddle one. The transitory shock $\tranShkAll_{t}$ is a two-point mixture: with probability $\pZero>0$ the consumer suffers a "zero-income event" ($\tranShkAll_{t}=0$), and otherwise draws an employed value $\tranShkEmp_{t}/\pNotZero$, where $\tranShkEmp_{t}$ has mean one on a compact positive interval and the rescaling by $1/\pNotZero$ (with $\pNotZero=1-\pZero$) keeps the unconditional transitory mean at one. Permanent income itself evolves as $\permLvl_{t+1}=\permLvl_{t}\PermGroFac\permShk_{t+1}$, so the growth factor $\PermGroFac$ is modulated period-by-period by $\permShk$ (Equation [](#eq-DBCparts)).

Two structural features do most of the analytical work. First, the zero-income event (following [Zeldes, 1989](#cite-zeldesStochastic)) generates a borrowing constraint endogenously: because next period's income can be zero and consuming zero yields utility $-\infty$ under CRRA, the consumer will "never spend everything," which the paper identifies with the "natural borrowing constraint" of [Aiyagari, 1994](#cite-aiyagari-ge); consequently the upper-bound constraint on consumption in Problem [](#eq-levelRecProblem) never binds, and the maximal marginal propensity to consume inherits the probability directly as $\MPCmax=1-\pZero^{1/\CRRA}\RPFac$. Second, the compact ("bounded") support of both shocks — which excludes lognormal and other unbounded specifications but is consistent with any finite-grid discretization such as Gauss-Hermite or equiprobable — guarantees a finite natural borrowing constraint $\underline{\mNrm}$ and is what allows the contraction-rate arguments characterizing the stable target in Section [](#sec-individStability) to be made globally rather than only asymptotically.

Everything the paper proves for the stochastic problem is proved under this assumption, yet the paper stresses that "the model looks more special than it is." A strictly positive minimum transitory income (say, from unemployment insurance) can be folded in by capitalizing its present discounted value into current market assets and transforming back into this specification; persistent-but-mean-reverting transitory shocks would leave the key results unchanged; and the positive point mass on the worst transitory realization is inessential to the results but simplifies the proofs and sharpens intuition. The perfect-foresight benchmark [perfect-foresight-income-process](#perfect-foresight-income-process) is the degenerate boundary of this process (shocks collapse to one and $\pZero$ is switched off), and at $\pZero=0$ the normalized recursion becomes a special case of [Ma, Stachurski, and Toda, 2020](#cite-mstIncFluct) with $\DiscFac\Rnd{\PermGroFac}^{1-\CRRA}$ playing the role of the stochastic discount factor (Remark [](#remark-stochdiscMST)).

## Relations

- **generalises** [perfect-foresight-income-process](perfect-foresight-income-process.md) — The perfect-foresight income process (ass-pfincome) is the degenerate boundary of this one: both shocks collapse to their unit means and the zero-income probability $\pZero$ is switched from positive to $0$.
- **assumed-by** [nondegenerate-solution-existence](nondegenerate-solution-existence.md) — The existence of a non-degenerate limiting solution for the problem with uncertainty (thm-convgtobellman) is established with this income process maintained throughout the setup.
- **assumed-by** [limiting-mpcs-lemma](limiting-mpcs-lemma.md) — The maximal MPC bound $\MPCmax=1-\pZero^{1/\CRRA}\RPFac$ depends directly on the zero-income probability $\pZero$ of this process; setting $\pZero=0$ collapses it toward the perfect-foresight $\MPCmin=1-\RPFac$.
- **assumed-by** [buffer-stock-target](buffer-stock-target.md) — The bounded (compact) support of the shocks is what lets the stable-target contraction argument of Section sec-individStability be made globally, underpinning existence of the individual buffer-stock target.
- **contrasts-with** [stochastic-discount-factor-mst](stochastic-discount-factor-mst.md) — With $\pZero>0$ the natural borrowing constraint arises endogenously, so no artificial liquidity constraint is imposed; only at $\pZero=0$ does the normalized problem reduce to the [Ma, Stachurski, and Toda, 2020] class (remark-stochdiscMST), which does impose one.

## Sources

- [BufferStockTheory.md#ass-shocks](../../BufferStockTheory.md#ass-shocks)
- [BufferStockTheory.md#eq-TranShkDef](../../BufferStockTheory.md#eq-TranShkDef)
- [BufferStockTheory.md#subsec-Setup](../../BufferStockTheory.md#subsec-Setup)

## bellman-ddsl correspondence

> *Reserved field — the bellman-ddsl perch/stage mapping is **deferred** for every concept in this atlas; the cross-repo bridge has not been authored. This is not a delivered correspondence.*

- perch: `(deferred)`
- stage: `(deferred)`
