# Concept atlas — index

47 concept(s) authored.

## [Absolute Impatience Condition (AIC)](absolute-impatience-condition.md)

> AIC says the absolute patience factor $\APFac := (\Rfree\DiscFac)^{1/\CRRA}$ is below 1. By the Euler equation of the perfect-foresight model, this is exactly the condition that consumption growth $\cLvl_{t+1}/\cLvl_{t} = \APFac$ is below 1 — the consumer would optimally choose to spend more today than tomorrow.

Relations: contrasts-with, requires (3 edges)

## [Absolute Patience Factor (APFac, "thorn")](absolute-patience-factor.md)

> The absolute patience factor $\APFac$ — typeset with the archaic letter "thorn" (Þ) — is the consumption-growth factor implied by the Euler equation of a perfect-foresight model: $\cLvl_{t+1}/\cLvl_{t} = (\Rfree\DiscFac)^{1/\CRRA} = \APFac$. Its centrality across the paper's analysis (every patience condition and every existence theorem references it) justifies the special symbol.

Relations: assumed-by (3 edges)

## [Asymptotic Consumption Growth Factors](asymptotic-consumption-growth-factors.md)

> This proposition pins down the two extreme-resource limits of the expected one-period consumption growth factor $\Ex_{t}[\cLvl_{t+1}/\cLvl_{t}]$ for the consumer facing labor-income uncertainty. At the rich end ($\mNrm_{t}\to\infty$) the precautionary motive vanishes and the consumer behaves arbitrarily close to the perfect-foresight benchmark, so expected consumption grows at the [absolute patience factor](#absolute-patience-factor) $\APFac=(\Rfree\DiscFac)^{1/\CRRA}$. At the poor end ($\mNrm_{t}\to 0$) the recursive fear of the zero-income event dominates: current consumption is being squeezed toward zero faster than next period's, so the expected growth factor explodes. The result *assumes* the model's bounded shocks ($0<\Min{\tranShkEmp}\leq\tranShkEmp$, $\pZero>0$) and the limiting-MPC machinery; it *implies* that the expected-resource ratio $\Ex_{t}[\mNrm_{t+1}]/\mNrm_{t}$ is likewise unbounded above as $\mNrm_{t}\to 0$ — because the level $\lim_{\mNrm_{t}\to 0}\Ex_{t}[\mNrm_{t+1}]$ stays strictly positive while $\mNrm_{t}\to 0$ — which is the ingredient the target-existence theorems need.

Relations: assumed-by, implies, requires (6 edges)

## [$\boundFunc$-Bounded Functions and the Weighted-Norm Space $\mathcal{C}_{\boundFunc}(\Reals_{++},\Reals)$](boundfunc-weighted-space.md)

> This definition sets up the function space on which the entire existence argument for the stochastic problem is carried out. Fix a *weight* $\boundFunc\in\mathcal{C}(\Reals_{++},\Reals)$ with $\boundFunc>0$. A continuous $\fFunc:\Reals_{++}\to\Reals$ is called $\boundFunc$-*bounded* if its $\boundFunc$-norm $\Vert\fFunc\Vert_{\boundFunc}=\sup_{s\in\Reals_{++}}|\fFunc(s)|/\boundFunc(s)$ is finite, and $\mathcal{C}_{\boundFunc}(\Reals_{++},\Reals)$ denotes the subspace of all such functions. The point of the construction is that it tolerates functions that are unbounded *below*, diverging to $-\infty$ as $s\to 0^{+}$ — exactly the situation for the model's value functions, whose CRRA shape (with $\CRRA>1$) makes both $\uFunc$ and $\vFunc$ unbounded below near zero — provided they diverge no faster than the weight. The definition *assumes* only continuity and strict positivity of $\boundFunc$; it is otherwise generic, and the specific weight that makes it work for this model is supplied separately.

Relations: assumed-by, contrasts-with, implies, requires (5 edges)

## [Boyd’s Contraction Mapping](boyd-weighted-contraction.md)

> Boyd’s weighted contraction mapping theorem is the abstract fixed-point result the paper invokes to establish existence of a non-degenerate limiting value function on an *unbounded* state space, where the standard Banach-space contraction argument fails because utility is not bounded. It applies to an operator $\mathbb{B}$ on the space $\mathcal{C}_{\boundFunc}(S,Y)$ of functions whose ratio to a *bounding function* $\boundFunc$ is bounded (the $\boundFunc$-weighted sup-norm is finite), rather than to bounded functions directly.

Relations: assumed-by, contrasts-with, requires (5 edges)

## [Buffer Stock Target](buffer-stock-target.md)

> The buffer stock target $\mTrgNrm$ is the eponymous concept of the paper: a level of (permanent-income-normalized) market resources at which the consumer expects no change in their normalized resources next period. Below the target, expected normalized resources rise; above it, they fall. The target is therefore a stable point of the dynamics of $\mNrm$.

Relations: contrasts-with, requires (6 edges)

## [Buffer Stock Target](buffer-stock-target-existence.md)

> This theorem is the existence-and-stability result for the individual buffer-stock target $\mTrgNrm$ — the level of (permanent-income-normalized) market resources at which the precautionary saving motive exactly balances impatience, so that $\Ex_t[\mNrm_{t+1}/\mNrm_t]=1$. It asserts not only that such a $\mTrgNrm>0$ exists but that it is globally stabilizing: for $\mNrm_t<\mTrgNrm$ expected next-period resources strictly exceed $\mNrm_t$, and for $\mNrm_t>\mTrgNrm$ they strictly fall short. This is the formal content behind the paper's title.

Relations: contrasts-with, implies, requires (7 edges)

## [Continuity Under Uniform-on-Compacts Convergence](compactness-preserved.md)

> This is a standard real-analysis fact (Appendix [](#sec-realanalysis), Additional Standard Results): let $\{\fFunc_n\}$ be a sequence of continuous functions on a subset of the real line that converges uniformly to $\fFunc$ on every compact set, and let $\{x_n\}$ be a convergent sequence of real numbers with limit $x$; then $\fFunc_n(x_n) \to \fFunc(x)$. The point is that the evaluation argument is allowed to *move* with $n$: ordinary pointwise convergence would only give $\fFunc_n(x) \to \fFunc(x)$ at a fixed argument, whereas here both the function and the point at which it is evaluated change simultaneously. What makes the joint limit go through is the *uniformity* of the convergence on a compact set containing the tail of $\{x_n\}$, which lets a triangle-inequality split $|\fFunc_n(x_n)-\fFunc(x)| \leq |\fFunc_n(x_n)-\fFunc(x_n)| + |\fFunc(x_n)-\fFunc(x)|$ control the first term uniformly (uniform convergence) and the second by continuity of the limit $\fFunc$.

Relations: assumed-by, contrasts-with, requires (3 edges)

## [Consumption Function is C2 (Lemma)](consumption-c2-properties.md)

> This lemma is the smoothness engine for the finite-horizon consumption function $\cFunc_{t}$. It assumes that the value function $\vFunc_{t}$ inherited from the next period is "nice" -- strictly negative, strictly increasing, strictly concave, $\mathbf{C}^{3}$, and satisfying $\lim_{\mNrm\to 0}\vFunc_{t}(\mNrm)=-\infty$ -- and concludes that the optimal consumption rule $\cFunc_{t}$ is $\mathbf{C}^{2}$ (twice continuously differentiable). It is a regularity fact about a single period of the normalized recursive problem (`eq-veqnNrmRecBellman`); no impatience inequality is used, only the curvature and boundary behavior of $\vFunc_{t}$ together with CRRA utility.

Relations: assumed-by, contrasts-with, implies, requires (4 edges)

## [Consumption Function is C2 and Concave](consumption-function-c2-concave.md)

> This proposition records the regularity (shape) properties of the period-$t$ consumption function $\cFunc_t$ in the model with permanent and transitory income shocks (the Friedman-Muth process, Assumption `ass-shocks`): for every $t$, $\cFunc_t$ is twice continuously differentiable ($\mathbf{C}^2$), strictly increasing, and strictly concave. It is a structural result about a single finite-horizon problem and does not by itself invoke any of the impatience inequalities — concavity and monotonicity follow from CRRA utility and the recursive Bellman structure, established by backward induction in the appendix.

Relations: assumed-by, contrasts-with, implies, requires (4 edges)

## [Convex-Negative Function Has Increasing Ratio (Consumption-Ratio Monotonicity)](consumption-ratio-nondecreasing.md)

> This claim is a self-contained real-analysis lemma whose only job is to convert a curvature-plus-sign hypothesis into monotonicity of a ray-slope. It *assumes* that $\fFunc$ is convex and that $\fFunc<0$ throughout an interval $(0,\lambda)$ anchored at the origin, and it *implies* that the ratio $\fFunc(s)/s$ — the slope of the chord from the origin to the point $(s,\fFunc(s))$ — is increasing on that interval. The proof fixes a small $\alpha\in(0,x_{1})$, defines the shifted convex function $F(x)=\fFunc(x)-\fFunc(\alpha)$ with $F(\alpha)=0$, and uses convexity through $x_{1}=t\alpha+(1-t)x_{2}$ to get $F(x_{1})\le(1-t)F(x_{2})$, which is exactly the statement that $F(s)/s$ is increasing; adding back the negative constant term $\fFunc(\alpha)/s$ (which is itself increasing in $s$ because $\fFunc(\alpha)<0$) preserves the inequality, so $\fFunc(s)/s$ is increasing too. The strict negativity matters only in this last step: it is what makes the additive term $\fFunc(\alpha)/s$ help rather than hurt.

Relations: assumed-by, requires (5 edges)

## [Contraction Mapping Under Consumption Bounds](contraction-mapping-consumption-bounds.md)

> This theorem supplies the analytical engine behind existence of the stochastic problem's limiting solution. Because permanent-income-normalized market resources live on the unbounded domain $\Reals_{++}$, the stationary Bellman operator $\TMap$ need not map any natural Banach space into itself, so the usual fixed-point machinery cannot be applied to it directly. The fix is to bound the consumption *share*: for share bounds $0<\MPCminInf<\MPCmaxInf$ the paper defines an "MPC bounded Bellman operator" $\TMap^{\MPCminInf, \MPCmaxInf}$ that optimizes only over $\cNrm\in[\MPCminInf \mNrm, \MPCmaxInf \mNrm]$, and the theorem shows this restricted operator is a genuine contraction on the weighted-norm space $\mathcal{C}_{\boundFunc}(\Reals_{++},\Reals)$ once the interval is narrow enough (specifically $\MPCmaxInf$ no larger than the finite-horizon maximal MPC $\MPCmax_{T-k}$ for some $k$).

Relations: assumed-by, contrasts-with, implied-by, requires (8 edges)

## [Feasibility Correspondence Is Not Compact-Valued (Berge Fails)](feasible-correspondence-not-compact.md)

> This remark isolates the precise technical obstacle that prevents the stationary Bellman operator $\TMap$ from being treated by textbook dynamic-programming machinery. The normalized operator $\TMap\vFunc_{t+1}(\mNrm)=\max_{\cNrm\in(0,\mNrm)}\{\uFunc(\cNrm)+\DiscFac\Ex\PermGroFacRnd^{1-\CRRA}\vFunc_{t+1}(\RNrmByGRnd(\mNrm-\cNrm)+\tranShkAll)\}$ optimizes over the *open* interval $(0,\mNrm)$; the boundary points $0$ and $\mNrm$ are deliberately excluded so that the maximand stays real-valued (at $\cNrm=\mNrm$ end-of-period assets, and hence next-period resources when $\pZero>0$, can hit zero where CRRA value diverges to $-\infty$). The remark *assumes* this open-valued feasibility correspondence $\mNrm\mapsto(0,\mNrm)$ and the consequent failure of compact-valuedness, and it *implies* that the standard Maximum Theorem of Berge cannot be invoked to guarantee continuity of the value of the maximization.

Relations: contrasts-with, implies, requires (6 edges)

## [Finite Human Wealth Condition (FHWC)](finite-human-wealth-condition.md)

> FHWC says the discounted growth factor $\RNrmByG^{-1} = \PermGroFac/\Rfree$ is below 1, equivalently $\Rfree > \PermGroFac$. This is the condition under which the present-discounted value of an infinite stream of permanent-income payments is finite — that is, "human wealth" $\hLvl_{t}$ converges as the horizon extends.

Relations: assumed-by, contrasts-with, requires (4 edges)

## [Finite Value of Autarky (FVAC)](finite-value-of-autarky.md)

> FVAC generalises the standard $\DiscFac < 1$ time-preference assumption to a setting with permanent income growth and uncertainty. It states that the discount factor times the permanent-growth factor (raised to $1-\CRRA$) times the expectation of the permanent shock (raised to $1-\CRRA$) lies strictly between 0 and 1.

Relations: assumed-by, implied-by, implies, special-case-of (8 edges)

## [Friedman-Muth Income Process (Income Shocks Assumption)](friedman-muth-income-process.md)

> This is the maintained income process for the paper's problem with uncertainty — a stochastic implementation of Friedman's permanent-income hypothesis. Noncapital income is the product of a permanent component and a transitory component, both iid across time. The permanent shock $\permShk_{t}$ has mean one ($\Ex[\permShk_{t}]=1$) and lives on a compact positive interval $[\permShkIndMin,\permShkIndMax]$ whose bounds straddle one. The transitory shock $\tranShkAll_{t}$ is a two-point mixture: with probability $\pZero>0$ the consumer suffers a "zero-income event" ($\tranShkAll_{t}=0$), and otherwise draws an employed value $\tranShkEmp_{t}/\pNotZero$, where $\tranShkEmp_{t}$ has mean one on a compact positive interval and the rescaling by $1/\pNotZero$ (with $\pNotZero=1-\pZero$) keeps the unconditional transitory mean at one. Permanent income itself evolves as $\permLvl_{t+1}=\permLvl_{t}\PermGroFac\permShk_{t+1}$, so the growth factor $\PermGroFac$ is modulated period-by-period by $\permShk$ (Equation [](#eq-DBCparts)).

Relations: assumed-by, contrasts-with, generalises (5 edges)

## [Growth Impatience Implies Harmenberg Impatience](gic-implies-harmenberg-impatience.md)

> This claim certifies that the paper's own [growth impatience condition](#growth-impatience-condition) (GIC), $\GPFacRaw=\APFac/\PermGroFac<1$, is sufficient for the (logically distinct) impatience inequality that [(Harmenberg, 2021b)](#cite-harmenbergAggregating) requires for the existence of the permanent-income-weighted ("Harmenberg-invariant") distribution of normalized market resources. Writing $f$ for the density of the permanent-income shock $\permShk$ (normalized so $\Ex[\permShk]=1$), Harmenberg's condition is $\log(\APFac) < \int \log(\PermGroFac\permShk)\,\permShk\, f(\permShk)\,d\permShk$. The claim *assumes* GIC and *implies* this inequality, so any calibration the paper already uses for its growth-impatience results automatically supports the permanent-income-weighted change of measure exploited in the covariance/balanced-growth material of Section 4.

Relations: contrasts-with, implies, requires (4 edges)

## [Growth Impatience Condition (GIC)](growth-impatience-condition.md)

> GIC says the absolute patience factor $\APFac := (\Rfree\DiscFac)^{1/\CRRA}$ is smaller than the expected permanent income growth factor $\PermGroFac$, so that the ratio $\GPFacRaw := \APFac/\PermGroFac$ is below 1.

Relations: assumed-by, contrasts-with, implied-by, implies, requires (8 edges)

## [Growth Patience Factor (GPF)](growth-patience-factor.md)

> The growth patience factor $\GPFacRaw := \APFac/\PermGroFac$ is the patience-factor analogue of the consumption-growth-vs-income-growth comparison: it asks how the consumer's preferred consumption-growth rate (encoded in $\APFac$) compares to the expected permanent-income growth rate $\PermGroFac$. When the ratio is below 1, consumption is growing more slowly than permanent income, so the wealth-to-permanent-income ratio drifts down — exactly the condition the GIC turns into a formal assumption.

Relations: assumed-by, contrasts-with, requires (4 edges)

## [MPC-Bounded Bellman Operator Maps the Weighted-Norm Space Into Itself](hiraguchi-continuity.md)

> This claim is the "well-definedness" lemma that has to be discharged before Boyd's weighted contraction mapping theorem can be applied to the stochastic problem. It asserts that the MPC-bounded Bellman operator $\TMap^{\MPCminInf,\MPCmaxInf}$ — the operator that optimizes consumption only over the share interval $\cNrm_{t}\in[\MPCminInf\mNrm_{t},\MPCmaxInf\mNrm_{t}]$ — sends every element of the space $\mathcal{C}_{\boundFunc}(\Reals_{++},\Reals)$ of continuous, $\boundFunc$-bounded functions back into that same space. Here $\boundFunc(x)=\zeta+x^{1-\CRRA}$ is the bounding (weight) function fixed in Remark [](#rem-shnkrdef), and $\Vert\cdot\Vert_{\boundFunc}$ is the associated weighted supremum norm. The claim *assumes* only that the input $\xFunc$ is itself continuous and $\boundFunc$-bounded; it *implies* the closure property "$\TMap^{\MPCminInf,\MPCmaxInf}:\mathcal{C}_{\boundFunc}\to\mathcal{C}_{\boundFunc}$" that the contraction argument needs, since a contraction must map a Banach space into itself before its fixed point is even meaningful.

Relations: assumed-by, contrasts-with, implies, requires (4 edges)

## [Limiting Consumption Function Inherits MPC Bounds and Is Strictly Positive](limiting-consumption-strictly-positive.md)

> This remark records two regularity properties that the limiting (infinite-horizon) consumption function $\cFunc$ inherits once the existence argument has produced it as the pointwise limit of the finite-horizon consumption functions $\cFunc_{T-n}$. It *assumes* the conclusions of the non-degenerate existence theorem [nondegenerate-solution-existence](#nondegenerate-solution-existence): that $\cFunc_{T-n}\to\cFunc$ pointwise on $\Reals_{++}$, that the limit $\cFunc$ satisfies the stationary Bellman equation [](#eq-stationarybellman), and that the associated value function lies in the weighted-norm space $\vFunc\in\mathcal{C}_{\boundFunc}(\Reals_{++},\Reals)$.

Relations: assumed-by, contrasts-with, implied-by, implies, requires, special-case-of (7 edges)

## [Limiting MPCs](limiting-mpcs-lemma.md)

> This lemma pins down the shape of the finite-horizon consumption function near the two ends of the resource domain. For each period the ratio of optimal consumption to market resources $\cFunc_{t}(\mNrm)/\mNrm$ stays inside the interval $[\MPCmin_{t},\MPCmax_{t}]$ (Equation [](#eq-cBounds)), where the minimal and maximal MPCs $\MPCmin_{t},\MPCmax_{t}$ are the limits of the marginal propensity to consume as $\mNrm\to\infty$ and $\mNrm\to 0$. Item (i) gives the exact backward recursions: the reciprocal minimal MPC accumulates the saving factor $\MPSmax=\RPFac$ each period and the reciprocal maximal MPC accumulates $\MPSmin=\pZero^{1/\CRRA}\RPFac$. Item (ii) takes the limit as the terminal period recedes: the maximal MPC always converges to the strictly positive limit $\MPCmax=1-\pZero^{1/\CRRA}\RPFac>0$, and — only if [return impatience](#RIC) (RIC) holds — the minimal MPC converges to $\MPCmin=1-\RPFac>0$.

Relations: assumed-by, contrasts-with, requires (7 edges)

## [Maximal-MPC Discount Factor Below One](maximal-mpc-at-most-one.md)

> This claim is the lemma that turns the [weak return impatience condition](#WRIC) (WRIC) into the concrete threshold horizon used to build the contraction underlying the stochastic existence proof. It *assumes* WRIC, namely $\pZero^{1/\CRRA}(\Rfree\DiscFac)^{1/\CRRA}/\Rfree<1$, and concludes that there exists a horizon $k$ such that the quantity $\pZero \DiscFac (\Rfree (1-\MPCmaxInf))^{1-\CRRA}$ is below one for every share bound $\MPCmaxInf\in[0,\MPCmax_{T-k}]$. Here $\MPCmax_{T-k}$ is the maximal marginal propensity to consume $k$ periods before the terminal date and $\MPCmax=1-\pZero^{1/\CRRA}\RPFac$ is its limit (Equation [](#eq-MPCmaxDefn)); $\pZero$ is the probability of the zero-income event and $\Rfree(1-\MPCmaxInf)$ is the gross return applied to the share of resources a maximally-impatient consumer would carry forward.

Relations: assumed-by, implied-by, implies, requires (6 edges)

## [Modified Growth Patience Factor (GPF-Mod)](modified-growth-patience-factor.md)

> GPF-Mod is the uncertainty-adjusted sibling of the ordinary growth patience factor. Where $\GPFacRaw = \APFac/\PermGroFac$ uses the unconditional permanent-income growth factor in the denominator, $\GPFacMod$ uses the *uncertainty-adjusted* growth factor $\PermGroFacAdj := \PermGroFac/\Ex[1/\permShk]$ — the harmonic-mean adjustment of $\PermGroFac$ for the spread of the permanent shock $\permShk$. Equivalently (after a Jensen rearrangement), $\GPFacMod = \Ex[\APFac/(\PermGroFac \permShk)]$, the form in which it first appears at `eq-GPFacMod`; the same equation also states the closed form $\GPFacMod \equiv \APFac/\PermGroFacAdj$.

Relations: assumed-by, contrasts-with, requires (3 edges)

## [Limiting MPC Bounds (Convergence)](mpc-bounds-convergence.md)

> This lemma verifies that the limiting non-degenerate consumption function $\cFunc$ satisfies the same marginal-propensity-to-consume bounds that hold for each finite-horizon function $\cFunc_{T-n}$. Under [weak return impatience](#WRIC) (WRIC), the share $\cFunc(\mNrm)/\mNrm$ tends to the minimal MPC $\MPCmin = 1-\APFac/\Rfree$ as $\mNrm\rightarrow\infty$ and to the maximal MPC $\MPCmax = 1-\pZero^{1/\CRRA}\APFac/\Rfree$ as $\mNrm\downarrow 0$. It is the converged-function counterpart of the finite-horizon "Limiting MPCs" lemma (`lemm-MPC`), which establishes the period-by-period bounds $\MPCmin_{T-n}\mNrm\le\cFunc_{T-n}(\mNrm)\le\MPCmax_{T-n}\mNrm$ and the convergence of the bound coefficients $\MPCmin_{T-n}\to\MPCmin$, $\MPCmax_{T-n}\to\MPCmax$; this lemma carries the property through the pointwise limit to $\cFunc$ itself.

Relations: assumed-by, contrasts-with, implied-by, requires (6 edges)

## [Joint Failure of Return and Growth Impatience Implies Failure of Finite Value of Autarky](no-ric-no-gic-implies-no-fvac.md)

> This claim is the formal hinge that lets the [finite value of autarky](#finite-value-of-autarky) (FVAC) condition substitute for the two separate impatience conditions in the existence theory. It *assumes* that both [growth impatience](#growth-impatience-condition) (GIC) fails — the absolute-patience-to-growth ratio satisfies $\GPFacRaw=\APFac/\PermGroFac\geq 1$ — and [return impatience](#return-impatience-condition) (RIC) fails — the [return patience factor](#return-patience-factor) satisfies $\RPFac=(\Rfree\DiscFac)^{1/\CRRA}/\Rfree\geq 1$. It then *implies* that FVAC fails, i.e. $\DiscFac\PermGroFac^{1-\CRRA}\Ex(\permShk^{1-\CRRA})\geq 1$, the negation of the assumption [](#ass-FVAC) that $0<\DiscFac\PermGroFac^{1-\CRRA}\Ex(\permShk^{1-\CRRA})<1$. Contrapositively, FVAC holding *guarantees* that at least one of GIC or RIC holds, so a consumer can never be simultaneously growth-patient and return-patient under FVAC.

Relations: contrasts-with, implies, requires (4 edges)

## [Non-degenerate Limiting Solution](nondegenerate-limiting-solution.md)

> This definition fixes the object whose existence the paper's first set of results is about. The normalized Bellman problem `eq-veqnNrmRecBellman` is said to have a *non-degenerate limiting solution* if, as the terminal period $T$ recedes ($n \to \infty$), the finite-horizon consumption and value functions converge pointwise to limits $\usual{\cFunc}\colon \Reals_{++} \to \Reals_{++}$ and $\usual{\vFunc}\colon \Reals_{++} \to \Reals$. The codomain restrictions carry the whole content of "non-degeneracy": $\usual{\cFunc}$ must be strictly positive (ruling out the degenerate limit $\usual{\cFunc} \equiv 0$, in which the consumer spends nothing) and $\usual{\vFunc}$ must be finite-valued (ruling out the degenerate limit $\usual{\cFunc} \equiv \infty$, in which unbounded human wealth finances unbounded consumption).

Relations: contrasts-with, implied-by, requires (4 edges)

## [Existence of Non-degenerate Solution](nondegenerate-solution-existence.md)

> This is the existence theorem for the stochastic problem: under just two assumptions — weak return impatience (WRIC) and finite value of autarky (FVAC) — the backward-iterated finite-horizon value and consumption functions converge point-wise to a *non-degenerate limiting solution* (`def-nondegeneracy`), i.e. a $\vFunc$ that is a fixed point of the stationary Bellman operator $\TMap$ together with a measurable policy $\cFunc$ satisfying the stationary Bellman equation. "Non-degenerate" means $\cFunc$ maps into $\Reals_{++}$ rather than collapsing to the trivial $\cFunc(\mNrm)=0$ or exploding to $\cFunc(\mNrm)=\infty$.

Relations: assumed-by, contrasts-with, implied-by, requires (6 edges)

## [Weighted-Norm Convergence Implies Uniform Convergence on Compact Sets](norm-implies-compactness.md)

> This fact is a piece of real-analysis plumbing that licenses the move from convergence in a *weighted* supremum norm to ordinary *uniform* convergence on compact sets. Let $X\subseteq\Reals^{n}$ be open and convex, let $\gFunc:X\to\Reals_{+}$ be continuous, and define the weighted norm $\Vert\fFunc\Vert_{\gFunc}=\sup_{x\in X}\vert\fFunc(x)\vert/\gFunc(x)$. The claim is that if $\Vert\fFunc_{n}-\fFunc^{\star}\Vert_{\gFunc}\to0$ then $\fFunc_{n}\to\fFunc^{\star}$ uniformly on every compact $K\subseteq X$. It *assumes* only continuity (and positivity) of the weight $\gFunc$; the paper notes that the convexity and openness of $X$ are not strictly necessary for the argument.

Relations: assumed-by, implies, requires (3 edges)

## [Perfect Foresight Income Process](perfect-foresight-income-process.md)

> This assumption fixes what the paper means, mathematically, by "perfect foresight": it is the degenerate case of the [Friedman-Muth income process](#friedman-muth-income-process) in which the zero-income probability is switched off ($\pZero=0$) and all four shock bounds are pinned to one, forcing the permanent and transitory shocks to be degenerate at their unit means ($\permShk\equiv1$, $\tranShkAll\equiv1$). Income then evolves deterministically: permanent income grows at the fixed factor $\PermGroFac$ each period and noncapital income equals permanent income exactly. The paper maintains this assumption "in force" throughout the Perfect Foresight Benchmarks subsection [](#subsec-PFBbenchmark), using the resulting closed forms as the reference point against which buffer-stock (precautionary) behavior under uncertainty is measured.

Relations: assumed-by, special-case-of (5 edges)

## [Existence of the Perfect Foresight Constrained Solution](pf-constrained-solution-exists.md)

> This proposition characterizes when the *normalized perfect foresight problem with a liquidity constraint* ($\cNrm_t \leq \mNrm_t$) has a non-degenerate limiting solution. It splits into two regimes. If [return impatience](#RIC) (RIC, $\RPFac<1$) holds, a non-degenerate solution always exists. If RIC fails ($\RPFac\geq 1$), a non-degenerate solution exists if and only if [growth impatience](#GICRaw) (GIC, $\GPFacRaw<1$) holds.

Relations: contrasts-with, implied-by (4 edges)

## [Perfect-Foresight Patience-Condition Chain: FHWC + GICRaw ⇒ PF-FVAC ⇒ RIC](pf-consumption-function-properties.md)

> This claim (stated as a `prf:property`, [claim-PFConspC](#claim-PFConspC)) orders three of the paper's patience conditions for the perfect-foresight income process (Assumption [](#ass-pfincome)), under the maintained hypothesis of [finite human wealth](#finite-human-wealth-condition) (FHWC, $\RNrmByG^{-1}=\PermGroFac/\Rfree<1$). It *assumes* FHWC throughout and asserts two one-directional implications: first, that [growth impatience](#growth-impatience-condition) (GICRaw, $\APFac<\PermGroFac$) implies the perfect-foresight [finite value of autarky](#finite-value-of-autarky) — PF-FVAC, the condition [](#PFFVAC) $\DiscFac\PermGroFac^{1-\CRRA}<1$, the perfect-foresight reduction of the general (uncertainty) FVAC; and second, that PF-FVAC in turn implies [return impatience](#return-impatience-condition) (RIC, $\RPFac<1$, equivalently $\APFac<\Rfree$).

Relations: contrasts-with, implies, requires (6 edges)

## [Perfect Foresight Finite Value of Autarky Condition (PF-FVAC)](pf-finite-value-of-autarky.md)

> Under the perfect-foresight income process (Assumption [](#ass-pfincome): $\pZero=0$ and all shocks degenerate at one), the general [finite value of autarky](#finite-value-of-autarky) condition loses its expectation term: the paper says FVAC "reduces to a 'perfect foresight finite value of autarky' condition", $\DiscFac\PermGroFac^{1-\CRRA}<1$. The operational content is that the discounted utility of "autarky" — consuming exactly permanent income every period — stays finite as the horizon extends: each period's utility contribution scales with $(\PermGroFac^{1-\CRRA})$ per period of growth and is discounted by $\DiscFac$, so the value of autarky is a geometric sum with ratio $\DiscFac\PermGroFac^{1-\CRRA}$, finite exactly when that ratio is below one. The paper's Symbols table names this ratio the PF Value of Autarky Factor $\beth\equiv\DiscFac\PermGroFac^{1-\CRRA}$ and reports $\beth=0.932$ at the baseline calibration, so PF-FVAC comfortably holds there. An equivalent patience-factor form, used as the diagonal of the inequalities diagram (Figure [](#fig-RelatePFGICFHWCRICPFFVAC)), is $\APFac < \Rfree^{1/\CRRA}\PermGroFac^{1-1/\CRRA}$.

Relations: contrasts-with, implied-by, implies, requires, special-case-of (6 edges)

## [Perfect Foresight Unconstrained Solution Requires FHWC](pf-unconstrained-requires-fhwc.md)

> This proposition characterizes when the perfect-foresight problem *without* liquidity constraints (Assumption `ass-pfincome` in force) has a well-behaved limiting solution as the horizon recedes. The answer is an "if and only if": a non-degenerate limiting consumption function exists exactly when both the finite human wealth condition (FHWC, $\RNrmByG^{-1} = \PermGroFac/\Rfree < 1$) and the return impatience condition (RIC, $\RPFac < 1$) hold. Neither condition alone suffices; each rules out a distinct mode of degeneracy.

Relations: contrasts-with, requires (4 edges)

## [Pseudo-Target](pseudo-target.md)

> The pseudo-target $\mBalLvl$ is the second of the paper's two stability concepts (alongside the buffer-stock target $\mTrgNrm$). It addresses a different stability question from the individual target: whether the *level* of market resources $\mLvl_t$ grows in expectation at the permanent-income growth factor $\PermGroFac$ — i.e., whether the model has a balanced-growth path.

Relations: contrasts-with, requires (5 edges)

## [‘Pseudo-Target’](pseudo-target-existence.md)

> Theorem `thm-MSSBalExists` is the existence-and-uniqueness result for the pseudo-target $\mBalLvl$ — the paper's second, less restrictive notion of stability, which asks whether the level of market resources $\mLvl$ grows in expectation at the permanent-income growth factor $\PermGroFac$ (a 'balanced growth' path) rather than whether normalised individual resources are stationary. The theorem *assumes* weak return impatience (WRIC), finite value of autarky (FVAC), and the ordinary growth impatience condition (GIC), and *implies* the existence of a unique $\mBalLvl > 0$ solving $\Ex_t[\permShk_{t+1}\mNrm_{t+1}/\mNrm_t] = 1$, together with the level-stability inequalities ($\Ex_t[\mLvl_{t+1}]/\mLvl_t$ exceeds $\PermGroFac$ below $\mBalLvl$ and falls short above it).

Relations: contrasts-with, implies, requires (6 edges)

## [Return Impatience Condition (RIC)](return-impatience-condition.md)

> RIC says the return patience factor $\RPFac := \APFac/\Rfree$ is below 1, i.e. the absolute patience factor $\APFac := (\Rfree\DiscFac)^{1/\CRRA}$ is smaller than the gross interest factor $\Rfree$.

Relations: assumed-by, contrasts-with, generalises, implied-by, requires (11 edges)

## [Return Patience Factor (RPF)](return-patience-factor.md)

> The return patience factor $\RPFac := \APFac/\Rfree$ is the patience-factor analogue of the consumer's preferred-consumption-growth-vs-return comparison. When $\RPFac < 1$ (RIC), the consumer's preferred consumption-growth factor $\APFac$ is below the gross interest factor $\Rfree$ — equivalently, the consumer is willing to forgo enough consumption today to let interest accumulate, so wealth is being drawn down rather than building up indefinitely.

Relations: assumed-by, contrasts-with, requires (5 edges)

## [Return Impatience Yields a Stationary Contraction (and Why WRIC Alone Does Not)](ric-gives-stationary-contraction.md)

> This remark sits immediately after the existence theorem [nondegenerate-solution-existence](#nondegenerate-solution-existence) (`thm-convgtobellman`) and contrasts the construction used there with what would be available under a stronger impatience assumption. The existence proof deliberately uses only [weak return impatience](#WRIC) (WRIC) together with [finite value of autarky](#FVAC), and as a consequence it must work with a *time-varying* family of MPC-bounded operators $\TMap^{\MPCmin_{T-n},\MPCmax_{T-n}}$ whose lower consumption share $\MPCmin_{T-n}$ can drift toward zero as the horizon recedes. The remark observes that if one instead *assumes* the full [return impatience condition](#RIC) (RIC), the minimal MPC is uniformly bounded below, $\MPCmin_{T-n}\geq\MPCmin>0$ for all $n$, and the analysis simplifies dramatically.

Relations: contrasts-with, implied-by, requires (5 edges)

## [Convergence of Arguments from Convergence of Continuous-Function Values](sequence-convergence-fact.md)

> This is a standalone real-analysis lemma collected in the paper's "Additional Standard Results" appendix. It supplies a partial converse to the elementary fact that continuity plus convergent arguments yields convergent values. Concretely: let $\fFunc\colon\Reals_{++}\to\Reals_{+}$ be continuous, take a sequence $x^{n}$ in $\Reals_{++}$ and a sequence of values $\fFunc^{n}(x^{n})$ in $\Reals_{+}$; the claim is that $\fFunc^{n}(x^{n})\to\fFunc(x)$ forces $x^{n}\to x$. The proof is by contradiction: if $x^{n}\not\to x$ then some subsequence stays at least $\delta$ away from $x$, and continuity of $\fFunc$ at the limit point $x$ keeps the corresponding values bounded away from $\fFunc(x)$ by a fixed $\epsilon$, contradicting the assumed convergence of the values.

Relations: assumed-by, contrasts-with, implies, requires (4 edges)

## [Shrink Factor and Bounding Function (Contraction-Modulus Parametrization)](shrink-factor-and-bounding-function.md)

> This remark fixes, in one place, the numerical ingredients on which the weighted-norm contraction machinery runs: the candidate contraction modulus $\Shrinker$ and the bounding (weight) function $\boundFunc$. The first argument of the max, $\pZero\DiscFac(\Rfree(1-\MPCmax_{k}))^{1-\CRRA}$, is the discounting term attached to the zero-income event when the consumption share is capped at the finite-horizon maximal MPC $\MPCmax_{k}$; Claim [maximal-mpc-at-most-one](#maximal-mpc-at-most-one) (where WRIC enters) puts it below one for $k$ large enough. The second argument, $\DiscFac\Ex\PermGroFacRnd^{1-\CRRA}$, is exactly the [finite value of autarky](#finite-value-of-autarky) quantity, below one by Assumption [](#ass-FVAC) — hence the remark's opening "By the finite value of autarky ... and for $k$ large enough, fix $\Shrinker$". From $\Shrinker$ the remark records the strict-positivity condition $\Shrinker(1-\Shrinker^{-1}\DiscFac\Ex\PermGroFacRnd^{1-\CRRA})>0$ (Equation [](#eq-shrnkrCond)), defines the constant $\zeta$ as the ratio of $\DiscFac\Ex\PermGroFacRnd^{1-\CRRA}\pNotZero^{\CRRA}\underline{\tranShkEmp}^{1-\CRRA}$ to that quantity (Equation [](#eq-Mbarddef)), and sets $\boundFunc(x)=\zeta+x^{1-\CRRA}$.

Relations: assumed-by, implied-by, requires (6 edges)

## [Stationary Euler Equation (Converged Consumption Function)](stationary-euler-equation.md)

> This property (stated as a `prf:property` labelled [](#eq-EuelrStatC) and invoked by the paper as a Claim) verifies that the limiting non-degenerate consumption function $\cFunc$ — the policy attached to the fixed point of the Bellman operator delivered by the existence theorem — satisfies the intertemporal first-order condition exactly: $\cFunc(\mNrm)^{-\CRRA}=\Rfree\DiscFac\Ex_{t}[\Rnd{\PermGroFac}_{t+1}^{-\CRRA}\cFunc(\mNrm^{\nxt})^{-\CRRA}]$, where next-period normalized resources $\mNrm^{\nxt}=\RNrmByGRnd(\mNrm-\cFunc(\mNrm))+\tranShkAll$ are generated by following the rule. The $\Rnd{\PermGroFac}_{t+1}^{-\CRRA}$ weight is the footprint of the permanent-income normalization — it is what converts marginal utility of the consumption *ratio* back into level-equivalent terms — making this the stationary, converged-function analogue of the scaled Euler equation ([](#eq-scaledeuler)) that each finite-horizon optimal rule satisfies. The verification is not redundant: the paper's existence machinery works at the level of *value* functions (a weighted-norm contraction), so first-order optimality of the limit object is a conclusion that has to be extracted, not an assumption.

Relations: assumed-by, implied-by, requires (5 edges)

## [Zero-Income-Probability Limit as a Special Case of Ma–Stachurski–Toda](stochastic-discount-factor-mst.md)

> This remark records a structural correspondence between the paper's permanent-income-normalized problem and the income-fluctuation framework of [(Ma, Stachurski, and Toda, 2020)](#cite-mstIncFluct). It *assumes* the degenerate case $\pZero=0$ — that is, the small probability of a zero-income event (the Zeldes (1989) device used elsewhere in the model) is switched off. Under that assumption the normalized Bellman equation [](#eq-veqnNrmRecBellman) becomes a *special case* of the MST (2020) setup: the return-over-growth ratio $\RNrmByGRnd_{t+1}=\Rfree/\Rnd{\PermGroFac}_{t+1}$ takes the part of their stochastic gross return on capital, and the object $\DiscFac\,\Rnd{\PermGroFac}_{t+1}^{1-\CRRA}$ takes the part of their stochastic discount factor. The remark is a mapping of notation and roles, not a new theorem; it tells the reader where this paper's normalized problem sits inside an existing, more general apparatus.

Relations: contrasts-with, generalises, requires, special-case-of (4 edges)

## [Strong Growth Impatience Condition (GIC-Mod)](strong-growth-impatience-condition.md)

> GIC-Mod is the inequality $\GPFacMod < 1$, where the modified growth patience factor has the closed form $\GPFacMod = \APFac/\PermGroFacAdj$ — absolute patience factor divided by the *uncertainty-adjusted* growth factor $\PermGroFacAdj := \PermGroFac/\Ex[1/\permShk]$. Equivalently (and how it first appears in the paper at `eq-GPFacMod`), $\GPFacMod = \Ex[\APFac/(\PermGroFac \permShk)]$. By Jensen's inequality, $\Ex[1/\permShk] \geq 1$, hence $\PermGroFacAdj \leq \PermGroFac$, hence $\GPFacMod \geq \GPFacRaw$ — strictly when $\permShk$ has positive variance. So GIC-Mod is always at least as strong as the ordinary GIC, and strictly stronger whenever there is uncertainty.

Relations: assumed-by, contrasts-with, implies, requires (8 edges)

## [Ordering of Pseudo-Target and Buffer-Stock Target](target-ordering-part-one.md)

> This lemma orders the paper's two distinct notions of a stable point. In the paper's notation the macro $\BalGroFac{\cdot}=\check{\cdot}$ marks the balanced-growth object and $\TargetNrm{\cdot}=\hat{\cdot}$ marks the target, so the lemma's $\BalGroFac{\mNrm}$ is the pseudo-target written elsewhere as $\mBalLvl$, and $\TargetNrm{\mNrm}=\mTrgNrm$ is the individual buffer-stock target. The pseudo-target $\mBalLvl$ is the point at which the *level* of market resources grows in expectation at the permanent-income factor, $\Ex_t[\mLvl_{t+1}/\mLvl_{t}]=\PermGroFac$ (section Collective-Stability), while the individual target $\mTrgNrm$ is the point at which *normalised* resources are stationary, $\Ex_t[\mNrm_{t+1}/\mNrm_{t}]=1$ (thm-target). The lemma states that the former lies weakly below the latter.

Relations: contrasts-with, implies, requires (5 edges)

## [Value Function is C3, Concave, and Diverges at Zero](value-function-c3.md)

> This property records the shape and smoothness of the period-$t$ normalized value function $\vFunc_{t}$ in the problem with permanent and transitory income shocks (the Friedman-Muth process, Assumption `ass-shocks`): for each $t$, $\vFunc_{t}$ is strictly negative, strictly increasing, strictly concave, three-times continuously differentiable ($\mathbf{C}^{3}$), and satisfies $\lim_{\mNrm\to 0}\vFunc_{t}(\mNrm)=-\infty$. The paper abbreviates this bundle of five properties by saying $\vFunc_{t}$ is "nice." It is a structural statement about a single finite-horizon problem and invokes none of the impatience inequalities; the divergence at zero comes from CRRA utility together with the positive probability of a zero-income (transitory-shock) event.

Relations: assumed-by, requires (3 edges)

## [Weak Return Impatience Condition (WRIC)](weak-return-impatience-condition.md)

> WRIC adjusts the return patience factor by the probability $\pZero$ of a zero-income realisation: $(\pZero^{1/\CRRA} \APFac)/\Rfree < 1$. Because $\pZero \leq 1$ implies $\pZero^{1/\CRRA} \leq 1$, RIC ($\APFac/\Rfree < 1$) always implies WRIC. The converse fails — WRIC is *strictly* weaker — whenever $\pZero < 1$: then $\pZero^{1/\CRRA} < 1$ opens a gap in which $\RPFac$ can sit at or above $1$ (RIC violated) while $\pZero^{1/\CRRA}\RPFac < 1$ still holds. Only in the degenerate case $\pZero = 1$ (no noncapital income) does $\pZero^{1/\CRRA} = 1$ and WRIC collapse onto RIC.

Relations: assumed-by, contrasts-with, implied-by, requires (6 edges)
