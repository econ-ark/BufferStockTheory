# The buffer-stock model as the paper states it: a digest for building a HARK model class

**Private working document. Nothing here goes public without Chris's word.**

Written 2026-11-11 by the BufferStockTheory-Latest session, at the request of the HARK-dev
session, which is drafting a new HARK class, `ConsBufferStockModel`, aligned exactly with the
paper. Chris's instruction, typed in the HARK-dev session at 2026-11-11 15:15:21 EST:

> "I think we need to draft a new ConsBufferStockModel in HARK that is directly aligned with
> representing the problem in the BST-Latest paper. So, for example, it would take a separate
> parameter for the probability of the "disaster" event, would reject a model where income shock
> in the "disaster" (unemployment) event is greater than income in the worst of the draws for
> employment; the transitory and permanent shocks have lower bounds in R++ and upper bounds
> < \infty; and so on. To facilitate this you should first ask the BST-Latest AI to make a digest
> of the paper (if it has not already done so) that will contain all the info needed to build
> this new model."

The sections follow the order of what HARK-dev asked for: the problem, the income process, the
parameters, the conditions, the limits and bounds, the liquidity-constrained case, what the
paper leaves open, and where HARK's `IndShockConsumerType` departs from the paper. Test values
and sources are at the end. A section on the appendix "Positive Minimum Income", added on
2026-11-12, follows the liquidity-constrained case.

## How to read this digest

### Which paper

The LaTeX source in this repository as it stood on branch `20260713-powerlaw-decay-theory-port`
at `93a4df46`: `sections/*.tex`, `Appendices/Apndx*.tex`, `Tables/*.tex`, `Equations/*.tex`,
`@local/local.sty`. The digest was first committed on that branch (`c94cb44e`, 2026-11-11) and
moved the same day to this one, the AI-indexing branch, because it is not power-law work.

- The files that define the model are byte-identical on
  `20261105-paper-revisions-without-powerlaw` at `6a55ccad`, the branch of draft pull request
  163, which is the candidate for `master`. Checked with `git diff` on 2026-11-11:
  `sections/TheoreticalFoundations.tex`, `sections/IndividualBufferStockStability.tex`, every
  appendix the paper includes, and `Tables/*.tex` do not differ.
- The port branch adds three passages that cite the power-law pages: the converse to Szeidl's
  theorem with the table "Which Condition Governs Which High-Wealth Phenomenon", the paragraph
  on the killed root, and the remark on the rate of approach. Anything taken from them is marked
  **port branch only**; those passages are not on the main line or on this branch.
- The section "The appendix "Positive Minimum Income"" (added 2026-11-12) reads branch
  `20261111-positive-minimum-income` at `2e875060`. That branch is cut from pull request 163's
  tip and adds the appendix, the repair from pull request 161, and a corrected sentence in
  `subsec:Setup`. Nothing else in this digest depends on that branch.
- `origin/master` (2026-05-05) predates the 27 fixes from the AI-aided review. Do not read the
  model from it.
- Pull request 161 (repairs to the existence proof, open, merged nowhere) changes
  `Appendices/ApndxConcaveCFunc.tex` and `sections/TheoreticalFoundations.tex`. It does not
  change the model or the statements of the theorems, except that it adds finite value of
  autarky to the hypotheses of `lemma:MPCBoundsConvg`.

### Tags

- **[stated: `label`]**: the paper says it at that LaTeX label, or in the named section.
- **[derived]**: the paper does not say it, but it follows from what the paper says. The step is
  given, or checked numerically in the scripts named under "Sources".
- **[not in the paper]**: a choice the class has to make.

Labels are the paper's own (`ass:shocks`, `eq:TranShkDef`, `thm:target`). Section and equation
numbers are never used: they move.

### Symbols

The printed glyphs differ between builds of the paper (the growth factor prints as 𝒢, Γ or G;
the paper's source currently prints relative risk aversion as γ, with a move to ρ deferred). The
macro names are stable, so this digest uses plain symbols tied to the macros.

| Here | Paper macro | Meaning | HARK name |
|---|---|---|---|
| R | `\Rfree` | interest factor | `Rfree` |
| G | `\PermGroFac` | permanent income growth factor | `PermGroFac` |
| β | `\DiscFac` | time preference factor | `DiscFac` |
| ρ | `\CRRA` (prints γ) | relative risk aversion | `CRRA` |
| ℘ | `\pZero` | probability of the zero-income event | `UnempPrb`; reported as `WorstPrb` |
| ψ | `\permShk` | permanent shock | `PermShk` |
| θ | `\tranShkEmp` | transitory shock when income is not zero | none: HARK's `TranShk` is ξ |
| ξ | `\tranShkAll` | transitory shock, including the zero-income event | `TranShk` |
| G̃ = Gψ | `\PermGroFacRnd` | realized growth factor of permanent income | |
| 𝓡 = R/G | `\RNrmByG` | growth-normalized return factor | |
| 𝓡̃ = R/(Gψ) | `\RNrmByGRnd` | its realized value | |
| **m**, **c**, **a**, **k**, **b**, **p**, **y** | `\mLvl` … | levels (bold) | `mLvl`, `cLvl`, `aLvl`, …, `pLvl` |
| m, c, a, b | `\mNrm` … | the same divided by **p** | `mNrm`, `cNrm`, `aNrm`, `bNrm` |
| Þ, Þ_R, Þ_G | `\APFac`, `\RPFac`, `\GPFacRaw` | absolute, return and growth patience factors | `APFac`, `RPFac`, `GPFacRaw` |
| κ̲, κ̄ | `\MPCmin`, `\MPCmax` | limiting MPCs as m → ∞ and as m → 0 | `MPCmin`, `MPCmax` |
| h | `\hNrm` | human wealth divided by **p** | `hNrm` (two conventions: see the HARK section) |
| m̂ | `\mTrgNrm` | buffer stock target | `mNrmTrg` |
| m̌ | `\mBalLvl` | pseudo-target | `mNrmStE` |
| ℒ | `\Alive` | probability of remaining alive (only in the paper's section on mortality) | `LivPrb` |

A factor is a number compared with one; a condition is the inequality, which holds or fails.

## The problem

### Timing within a period

[stated: `eq:DBCparts`, section "Setup" (`subsec:Setup`)]

In this order:

- the consumer ends period t with assets **a**_t = **m**_t − **c**_t;
- assets become next period's capital one for one: **k**_{t+1} = **a**_t;
- capital earns the interest factor: **b**_{t+1} = R **k**_{t+1} ("bank balances");
- permanent income moves: **p**_{t+1} = **p**_t G ψ_{t+1};
- income arrives: **y**_{t+1} = **p**_{t+1} ξ_{t+1};
- market resources are **m**_{t+1} = **b**_{t+1} + **y**_{t+1};
- the consumer chooses **c**_{t+1}.

So the shocks dated t+1 are realized before consumption in t+1, and the expectation E_t is over
(ψ_{t+1}, ξ_{t+1}). The time index runs over {T, T−1, T−2, …}; the horizon is n in T−n.

### The problem in levels

[stated: `eq:levelRecProblem`]

    v_t(m_t, p_t) = max over 0 < c_t ≤ m_t of  u(c_t) + β E_t[ v_{t+1}(m_{t+1}, p_{t+1}) ]      (levels, bold in the paper)

- States: (**m**_t, **p**_t), both strictly positive. Control: **c**_t.
- Utility: u(c) = c^(1−ρ)/(1−ρ) with **ρ > 1** [stated: `subsec:Setup`].
- β is "the (strictly positive) discount factor" [stated: `subsec:Setup`].
- R is "a fixed interest factor" [stated: `subsec:Setup`]. A footnote says a stochastic return
  is outside the paper.
- G is constant. A footnote says a time-varying G "has straightforward consequences" and is "an
  option allowed for in the HARK toolkit"; the paper's results are for constant G.
- No survival probability appears in the problem [derived: none is in `eq:levelRecProblem` or
  `eq:veqnNrmRecBellman`]. Mortality appears only in the section "Mortality Yields Invariance"
  (`sec:Mortality`), as two alternative additions discussed in prose.

### The terminal period

[stated: `eq:NoDebtAtDeath`, `subsec:Setup`, `subsubsec:cFuncBounds`]

- "The consumer cannot die in debt": **c**_T ≤ **m**_T.
- With v_{T+1} = 0, the terminal value function is u(m_T) and the terminal consumption function
  is c_T(m) = m.
- κ̲_T = κ̄_T = 1.

### Normalization

[stated: section "Normalized Problem" (`subsubsec:ratio`), `eq:veqnNrmRecBellman`, `sec:recoverLevels`]

Nonbold variables are the bold ones divided by **p**_t, with one exception: normalized value is
**v**_t / **p**_t^(1−ρ). The state is the single variable m = **m**/**p**.

    v_t(m_t) = max over 0 < c_t < m_t of  u(c_t) + β E_t[ G̃_{t+1}^(1−ρ) v_{t+1}(m_{t+1}) ]
    a_t     = m_t − c_t
    b_{t+1} = a_t R/G̃_{t+1} = 𝓡̃_{t+1} a_t
    m_{t+1} = b_{t+1} + ξ_{t+1}

- Recovering levels: **v**_t(**m**, **p**) = **p**^(1−ρ) v_t(**m**/**p**) and
  **c**_t(**m**, **p**) = **p** c_t(**m**/**p**).
- The feasible set is the open interval (0, m) in the normalized problem, and 0 < **c** ≤ **m**
  in the level problem. The paper says the upper bound never binds, because of the zero-income
  event (next section).
- First-order condition [stated: `eq:scaledeuler`]:
  c_t^(−ρ) = R β E_t[ G̃_{t+1}^(−ρ) c_{t+1}^(−ρ) ].
- End-of-period value [stated: `eq:vfFrackdefn`]:
  𝔳_t(a) = β E_t[ G̃_{t+1}^(1−ρ) v_{t+1}(𝓡̃_{t+1} a + ξ_{t+1}) ], defined for a > 0. The
  first-order condition is u′(c_t(m)) = 𝔳_t′(m − c_t(m)), and the envelope condition is
  v_t′(m) = u′(c_t(m)) [stated: proofs of `lemm:consC2` and `prop:vfc3`].

### The limiting solution

[stated: `def:nondegeneracy`, `eq:maintmap`]

- The problem "has a non-degenerate limiting solution" if c(m) = lim c_{T−n}(m) and
  v(m) = lim v_{T−n}(m) exist as n → ∞ for every m > 0, with c strictly positive and v
  real-valued. Informally: neither c = 0 everywhere nor c = ∞ everywhere.
- The stationary Bellman operator is
  (T f)(m) = max over c in (0, m) of { u(c) + β E[ G̃^(1−ρ) f(𝓡̃(m − c) + ξ) ] }.
  A finite-valued fixed point of T is a limiting non-degenerate solution.
- The limit is in the horizon (n → ∞), not in calendar time.

### What holds in every period before the last

[stated: `prop:cfuncprop`, `prop:vfc3`]

- c_t is twice continuously differentiable, increasing and strictly concave.
- v_t is strictly negative, strictly increasing, strictly concave, three times continuously
  differentiable, and tends to −∞ as m → 0.
- These need no patience condition, only the income process below and ρ > 1.

## The income process

### What the paper assumes

[stated: `ass:shocks` ("Friedman-Muth Income Process"), `eq:TranShkDef`, and the footnote to the
first paragraph of `subsec:Setup`]

- {ψ_t, ξ_t} is a sequence of independent and identically distributed random variables on a
  common probability space.
- **Permanent shock.** E[ψ] = 1 and ψ ∈ [ψ̲, ψ̄] with 0 < ψ̲ ≤ 1 ≤ ψ̄ < ∞.
- **Transitory shock.**
  - ξ = 0 with probability ℘ > 0 (the "zero-income event");
  - ξ = θ/(1−℘) with probability 1−℘,
  - where θ is independent and identically distributed over time, E[θ] = 1, and θ ∈ [θ̲, θ̄]
    with θ̲ > 0 and θ̲ ≤ 1 ≤ θ̄ < ∞.
- **Bounded support** [stated: paragraph "Bounded support."]: both ψ and θ live on compact
  intervals inside the strictly positive reals. This "excludes lognormal and other
  unbounded-support specifications" but "is consistent with all standard discretizations of
  unbounded distributions onto a finite grid (Gauss–Hermite, equiprobable, etc.)".

### What follows

- E[ξ] = ℘·0 + (1−℘)·E[θ]/(1−℘) = 1 [derived]. The division by 1−℘ is the scaling that keeps
  mean transitory income at one.
- The support of ξ is {0} together with [θ̲/(1−℘), θ̄/(1−℘)] [derived].
- The worst income when the zero-income event does not happen is θ̲/(1−℘) > 0, so the
  zero-income event is strictly the worst outcome [derived].
- ℘ < 1 is needed for the scaling [derived]. The paper mentions ℘ = 1 only as a limiting case in
  which there is no noncapital income [stated: `subsec:TheModelUncertainty`].
- E[ψξ] = 1 is used in the pseudo-target equation [stated: `eq:balgrostable`], which needs ψ and
  ξ to be independent of each other within a period. `ass:shocks` does not say so; the section
  on aggregates refers to "the independence assumptions we have made about the shocks ξ and ψ"
  [stated: `subsec:cGroEqPermGroFacQ`].

### Income in the zero-income event

- It is zero [stated: `eq:TranShkDef`], "without loss of generality" [stated: footnote in
  `subsec:Setup`, citing Aiyagari].
- A positive minimum "could be handled by capitalizing the present discounted value (PDV) of
  minimum income into current market assets, and transforming that model back into this one",
  "so long as unemployment benefits are proportional to **p**_t" [stated: `subsec:Setup`, at the
  anchor `PDV`]. The paper does not carry the transformation out. Its footnote points to the
  section "Normalized Problem", which says nothing about it.
- **On branch `20261111-positive-minimum-income`** (2026-11-12) the claim is corrected, and the
  appendix "Positive Minimum Income" carries the transformation out. The sentence now reads:
  "Without permanent shocks, that transforms the model back into this one. With permanent shocks
  it does not, but Appendix [Positive Minimum Income] shows that our results still hold, with
  market resources measured from the resulting natural borrowing limit and with ℘ replaced by the
  probability that minimum income and the lowest permanent shock occur together (which may be
  zero, in which case the maximal MPC is one and the borrowing limit can be reached), provided
  that Gψ̲ < R." See "The appendix "Positive Minimum Income"" below.
- "The assumption of a positive point mass for the worst realization of the transitory shock is
  inessential, but simplifies the proofs", and "no key results would change if the transitory
  shocks were persistent but mean-reverting" [stated: `subsec:Setup`]. Every formal result uses
  the point mass and independence over time.

### The restriction Chris asked for

"Reject a model where income in the disaster event is greater than income in the worst of the
draws for employment."

- In the paper it holds automatically: 0 < θ̲/(1−℘).
- If the class allows income μ ≥ 0 in the event and keeps mean transitory income at one the way
  HARK does (employed draws multiplied by (1 − ℘μ)/(1−℘)), the restriction is
  **μ < θ̲/(1 − ℘(1−θ̲))** [derived; not in the paper]. The bound is at most one. The appendix
  "Positive Minimum Income" adopts exactly this bound (`eq:MinIncomeBelowEmployed`, with
  μ = ξ_u).
- Why the restriction matters [derived]: the paper's κ̄ and its weak return impatience condition
  use ℘ as the probability of the worst outcome of ξ. The proof of `lemm:MPC` splits the Euler
  equation on ξ = 0 against ξ > 0. If the event were not the worst outcome, ℘ would not be that
  probability.
- A second consequence of μ > 0, which the paper does not discuss, is under "The natural
  borrowing constraint" below: with permanent shocks, the paper's formula for κ̄ no longer holds
  as written.

### The perfect foresight income process

[stated: `ass:pfincome`] ℘ = 0 and θ̲ = θ̄ = ψ̲ = ψ̄ = 1.

## Parameters and their admissible sets

| Parameter | Admissible set | Source |
|---|---|---|
| ρ | ρ > 1 | [stated: `subsec:Setup`]. Used for u(0⁺) = −∞, for the direction of Jensen's inequality, and for value normalized by **p**^(1−ρ). ρ = 1 is not covered. |
| β | β > 0 | [stated: `subsec:Setup`]. β < 1 is not assumed, and neither is Rβ < 1: "βR < 1 is not necessary for an infinite-horizon solution" [stated: under `ass:AIC`]. One illustration does say "since β < 1 by assumption"; see "What the paper leaves open". |
| R | R > 0 | fixed [stated]. R < 1 is allowed: "neither theory nor evidence demand that R ≥ 1" [stated: `subsec:TheModelUncertainty`]. Positivity is [derived]. |
| G | G > 0 | [derived]: **p** must stay strictly positive and G^(1−ρ) must be finite. G = 0 appears once, as a "cake-eating" aside. |
| ℘ | 0 < ℘ < 1 | ℘ > 0 [stated: `eq:TranShkDef`]; ℘ < 1 [derived]. ℘ = 0 belongs to perfect foresight or to the liquidity-constrained problem, which needs an explicit constraint. |
| distribution of ψ | mean one; support [ψ̲, ψ̄], 0 < ψ̲ ≤ 1 ≤ ψ̄ < ∞ | [stated: `ass:shocks`] |
| distribution of θ | mean one; support [θ̲, θ̄], 0 < θ̲ ≤ 1 ≤ θ̄ < ∞ | [stated: `ass:shocks`] |
| independence | (ψ_t, ξ_t) independent over time; ψ_t independent of ξ_t | over time [stated]; within a period used but not in `ass:shocks` |

**Joint restrictions.** The paper imposes none for the problem to be stated. Each finite-horizon
problem is well defined for every admissible parameter set [derived: `prop:cfuncprop` has no
patience hypothesis]. The joint restrictions are the conditions in the next section, and each is
a hypothesis of particular results:

- for a limiting solution: weak return impatience and finite value of autarky;
- for a target: those two and strong growth impatience;
- for a pseudo-target: those two and growth impatience.

**The paper's calibration** [stated: `table:Parameters`]: G = 1.03, R = 1.04, β = 0.96, ρ = 2,
℘ = 0.005, standard deviation of log ψ = 0.1, standard deviation of log θ = 0.1. The lognormal
is "our default (though not required) assumption": log ψ is normal with mean −σ²/2 and variance
σ² [stated: footnote after `eq:GICSdl`]. The paper's numbers therefore come from discretized
lognormals, which are bounded.

## The conditions

### Factors and inequalities

| Condition | Factor | Formula | Holds when | Label |
|---|---|---|---|---|
| Absolute impatience (AIC) | absolute patience factor Þ | (Rβ)^(1/ρ) | Þ < 1 | `eq:APFac`, `ass:AIC` |
| Return impatience (RIC) | return patience factor Þ_R | Þ/R | Þ_R < 1 | `ass:RIC` |
| Weak return impatience (WRIC) | none in the text (but see the note on `table:Calibration` under "What the paper leaves open") | ℘^(1/ρ) Þ/R = (℘Rβ)^(1/ρ)/R | < 1 | `ass:WRIC` |
| Growth impatience (GIC) | growth patience factor Þ_G | Þ/G | Þ_G < 1 | `eq:GPFacRaw`, `ass:GICRaw` |
| Strong growth impatience (GIC-Mod) | modified growth patience factor | E[Þ/(Gψ)] = Þ_G E[ψ⁻¹] | < 1 | `eq:GPFacMod`, `ass:GICMod` |
| Log growth impatience (Szeidl) | none | log Þ_G < E[log ψ] | as written | `eq:GICSdl` |
| Harmenberg's condition | none | log Þ < E[ψ log(Gψ)], that is log Þ_G < E[ψ log ψ] | as written | `eq:HarmImp` |
| Mortality-adjusted growth impatience | none | ℒ Þ_G | < 1 | `eq:GICLivMod` |
| Finite human wealth (FHWC) | finite human wealth factor | G/R | < 1 | `ass:FHWC`, `eq:FHWC2` |
| Perfect foresight finite value of autarky (PF-FVAC) | perfect foresight value of autarky factor | β G^(1−ρ) | < 1, equivalently Þ < R^(1/ρ) G^(1−1/ρ) | `eq:PFFVAC` |
| Finite value of autarky (FVAC) | value of autarky factor | β G^(1−ρ) E[ψ^(1−ρ)] | strictly between 0 and 1 | `ass:FVAC` |

Related objects the paper names [stated: `table:Calibration`, `eq:PermGroFacAdj`]:

- "uncertainty-adjusted growth" G̲ = G/E[ψ⁻¹], so the modified growth patience factor is Þ/G̲;
- "growth compensated permanent shock" 1/E[ψ⁻¹];
- "utility compensated permanent shock" (E[ψ^(1−ρ)])^(1/(1−ρ)), so the value of autarky factor
  is β times (G times that)^(1−ρ).

There is no separate perfect foresight growth condition: with ψ = 1 the two growth conditions
coincide. Autarky means consuming permanent income every period [stated: under `ass:FVAC`].

**Port branch only:** the table "Which Condition Governs Which High-Wealth Phenomenon" adds a
"rate condition", 𝓡 Þ_G compared with E[ψ²]. It governs how fast c(m) approaches its perfect
foresight bound, is cited from the power-law pages, and is "not an impatience condition at all".

### How the conditions relate

- Return impatience implies weak return impatience, because ℘ < 1 [stated: under `ass:WRIC`].
  They coincide only at ℘ = 1.
- Strong growth impatience implies Szeidl's condition, which implies growth impatience, which
  implies Harmenberg's condition [stated: text after `eq:GICSdl`; `claim:gicimpliesharmimp`].
  With a lognormal ψ the four are Þ_G below e^(−σ²), e^(−σ²/2), 1 and e^(σ²/2) [the first is
  stated in the footnote after `eq:GICSdl`, the second follows from the distribution stated
  there, and the fourth is derived].
- Finite value of autarky implies its perfect foresight version, because E[ψ^(1−ρ)] ≥ 1
  [stated: `table:Comparison`].
- With finite human wealth: growth impatience implies perfect foresight finite value of
  autarky, which implies return impatience [stated: `claim:PFConspC`].
- Without finite human wealth the chain reverses: return impatience implies perfect foresight
  finite value of autarky, which implies growth impatience [derived; the paper's figure
  `fig:RelatePFGICFHWCRICPFFVAC` read in the other direction].
- If growth impatience and return impatience both fail, finite value of autarky fails
  [stated: `claim:noRICGIC`]. So, given finite value of autarky:
  - if return impatience fails, finite human wealth fails and growth impatience holds
    [stated: `eq:RICimplies`];
  - if finite human wealth fails, growth impatience holds [stated: the display in "Case 3" of
    `subsubsec:casesUC`; the sentence that follows it is mis-worded, see "What the paper leaves
    open"];
  - if finite human wealth holds, return impatience holds [derived: the first of these three,
    read the other way].
- If R ≥ 1 and β < 1, return impatience holds, so weak return impatience is "redundant"
  [stated: `subsec:TheModelUncertainty`].
- Finite value of autarky and weak return impatience do not imply each other [derived]. The
  paper assumes both and derives neither from the other.
- Absolute impatience implies none of the others and is a hypothesis of no result [derived].
- The complete eight-by-eight table of implications, with a numerical witness for every
  non-implication and a probe script, is in `_ai/audit/conditions-lattice.md`.

### What each combination delivers

Every result for the model with uncertainty is a sufficiency statement. The paper claims
necessity only under perfect foresight.

| Result | Hypotheses | Label |
|---|---|---|
| Each finite-horizon c_t: smooth, increasing, strictly concave | `ass:shocks`, ρ > 1 | `prop:cfuncprop` |
| κ̲_t m ≤ c_t(m) ≤ κ̄_t m, with the recursions for κ̲_t and κ̄_t | the lemma is stated under weak return impatience | `eq:cBounds`, `lemm:MPC` |
| The bounded Bellman operators are contractions | weak return impatience, finite value of autarky | `thm:cmap` |
| A non-degenerate limiting solution exists; v_{T−n} → v and c_{T−n} → c pointwise; v is a fixed point of T | weak return impatience, finite value of autarky | `thm:convgtobellman` |
| The limit obeys the Euler equation | weak return impatience | the claim labeled `eq:EuelrStatC` |
| The limit is concave, with c(m)/m → κ̲ as m → ∞ and → κ̄ as m → 0 | weak return impatience (the proof also uses the existence theorem, so finite value of autarky too) | `lemma:MPCBoundsConvg` |
| A unique buffer stock target m̂ | weak return impatience, finite value of autarky, strong growth impatience | `thm:target` |
| A unique pseudo-target m̌ | weak return impatience, finite value of autarky, growth impatience | `thm:MSSBalExists` |
| m̌ ≤ m̂ | both exist | `lemma:orderingPartOne` |
| Expected consumption growth (levels) → ∞ as m → 0, and → Þ as m → ∞ | the limit exists; return impatience for the second | `prop:convgGrowth` |
| Invariant distributions of m, c and a across a population | Szeidl's condition | text at `eq:GICSdl`, citing Szeidl |
| An invariant permanent-income-weighted distribution; aggregate consumption, assets and market resources grow by G | growth impatience | text after `eq:HarmCDF`, citing Harmenberg; `claim:gicimpliesharmimp` |
| Perfect foresight, no constraint: a non-degenerate limit exists if and only if finite human wealth and return impatience hold | | `prop:pfUCFHWC` |
| Perfect foresight with the constraint: a non-degenerate limit exists if return impatience holds; if it fails, if and only if growth impatience holds | | `prop:PFCExist` |

### The contraction and its norm

[stated: `def:boundfuncspace`, `eq:phinorm`, `thm:Boyd`, `claim:MPCMAXKleq1`, `rem:shnkrdef`,
`thm:cmap`]

- **Space.** Continuous functions f on the strictly positive reals with finite weighted norm
  ‖f‖ = sup over s > 0 of |f(s)|/ϝ(s), with weight ϝ(x) = ζ + x^(1−ρ) and ζ > 0.
- **Operator.** For bounds 0 < ν̲ < ν̄ on the share of market resources consumed,
  (T^{ν̲,ν̄} f)(m) = max over c in [ν̲ m, ν̄ m] of { u(c) + β E[ G̃^(1−ρ) f(𝓡̃(m − c) + ξ) ] }.
  The finite-horizon value functions satisfy v_t = T^{κ̲_t, κ̄_t} v_{t+1}.
- **Theorem.** Under weak return impatience and finite value of autarky there are a k and an
  α in (0, 1) such that T^{ν̲,ν̄} is a contraction with modulus α for all
  0 < ν̲ < ν̄ ≤ κ̄_{T−k}.
- **Modulus.** Any α strictly between
  max{ ℘β(R(1 − κ̄_{T−k}))^(1−ρ), β E[G̃^(1−ρ)] } and one.
- **Constant.** ζ = β E[G̃^(1−ρ)] (1−℘)^ρ θ̲^(1−ρ) / ( α (1 − β E[G̃^(1−ρ)]/α) ) [stated:
  `eq:Mbarddef`].
- At the limiting κ̄ the first term of the maximum equals ℘^(1/ρ) Þ_R [stated: proof of
  `claim:MPCMAXKleq1`]. The second term is the value of autarky factor. So for a long horizon
  the modulus can be taken as close as wished to the larger of those two factors [derived]:
  about 0.941 at the paper's calibration.
- The paper does not show that the stationary operator T is itself a contraction: its feasible
  set (0, m) is not compact [stated: `remark:notCompact`]. With return impatience,
  T^{κ̲, κ̄_{T−k}} is one stationary contraction that generates the value functions beyond
  horizon k [stated: `remark:ricstationary`].
- Uniqueness of the fixed point of T is not asserted. The limiting solution is unique because it
  is defined as the limit of the finite-horizon sequence [derived].

### What happens when a condition fails

- **Weak return impatience fails.** With ℘^(1/ρ) Þ_R ≥ 1 the recursion for 1/κ̄_{T−n} diverges,
  so κ̄_{T−n} → 0 and, since c_{T−n}(m) ≤ κ̄_{T−n} m, consumption tends to zero at every m: the
  limit is degenerate [derived from `eq:MPCminInv` and `eq:cBounds`]. The paper says the
  condition "prevents a situation where everyone consumes an arbitrarily small share of current
  market resources as the terminal period recedes", and that it "cannot be relaxed further
  without an artificial liquidity constraint" [stated].
- **Finite value of autarky fails, weak return impatience holds.** The paper proves nothing. Its
  theorem is sufficiency only. See "What the paper leaves open".
- **Return impatience fails, the two existence conditions hold.** A non-degenerate solution
  exists. Human wealth is unbounded and growth impatience holds. κ̲ = 0, so the MPC tends to
  zero as m → ∞ and c approaches no linear limit [stated: "Case 1" in `subsubsec:casesUC`,
  `eq:RICimplies`].
- **Finite human wealth fails.** h is infinite and the perfect foresight solution is no longer a
  finite upper bound. The existence theorem does not need the condition; the natural borrowing
  constraint does its work [stated: "Case 1" and "Case 3" in `subsubsec:casesUC`].
- **Growth impatience fails.** No pseudo-target is guaranteed. Given finite value of autarky,
  return impatience and finite human wealth must then hold [derived from `claim:noRICGIC` and
  the relations above].
- **Strong growth impatience fails, growth impatience holds.** No target is guaranteed, and the
  pseudo-target exists. The paper's example quadruples the variance of the permanent shocks and
  says "now there is no target" [stated: section "Example With Balanced-Growth m̌ But No Target
  m̂", `fig:GICModFailsButGICRawHolds`].
  - What can be said in general [derived]: E_t[m_{t+1}] − m_t = 𝓡 E[ψ⁻¹](m − c(m)) + 1 − m is
    convex in m, because c is concave. It tends to 1 as m → 0. With return impatience its slope
    tends to Þ_G E[ψ⁻¹] − 1 as m → ∞. If strong growth impatience fails strictly it is positive
    at both ends, so it has either no zero, or (generically) two: a lower one that is stable and
    an upper one that is not. The theorem's uniqueness does not extend.
  - The same holds for the pseudo-target when growth impatience fails, with 𝓡 in place of
    𝓡 E[ψ⁻¹] and Þ_G in place of Þ_G E[ψ⁻¹].
- **Absolute impatience fails.** Nothing is lost. Under return impatience, expected consumption
  growth at high m tends to Þ ≥ 1.
- **Szeidl's condition fails.** On the branch of pull request 163 the paper states only
  sufficiency. **Port branch only:** if it fails strictly, "escape from high wealth is almost
  sure" and, under a reachability proviso, no invariant distribution of m exists; the boundary
  case is left open; with mortality the cross-section is nonetheless well behaved.
- **Mortality-adjusted growth impatience fails.** The paper says the aggregate ratio of wealth to
  income "will head to infinity only if" the cohort is patient enough to fail it [stated:
  `sec:Mortality`]. **Port branch only:** the table says that on strict failure the ratio
  diverges.

## Limits and bounds the class should be able to report

### The natural borrowing constraint

- With the zero-income event the consumer "will never spend everything": a_t > 0 in every
  period before the last [stated: `subsec:Setup`]. End-of-period value 𝔳_t(a) is real-valued
  only for a > 0 and tends to −∞ as a → 0 [stated: proof of `lemm:consC2`, anchor
  `BoroCnstNat`].
- So the natural borrowing constraint is a ≥ 0, never attained, in every period and at every
  horizon, and the lower bound of m is zero [derived]. In the paper's model it does not depend
  on R, G or the supports of the shocks, because the worst income is zero.
- The paragraph "Bounded support." says boundedness "guarantees a finite natural borrowing
  constraint m̲" and points to the section "Main Results for Problem with Uncertainty", which
  defines no m̲.
- **How it would depend on the worst incomes** [derived; not in the paper]. With a floor ξ̲ ≥ 0
  on ξ and the lower bound ψ̲ on ψ, repayment must be certain on the worst path:
  a̲_t = (m̲_{t+1} − ξ̲) G ψ̲ / R with m̲_T = 0. In the limit
  a̲ = −ξ̲ x/(1 − x), where x = G ψ̲ / R, finite only if x < 1. HARK's `calc_boro_const_nat`
  is this recursion. With ξ̲ = 0 it gives zero.
- **With ξ̲ > 0 and permanent shocks, the paper's κ̄ does not hold as written** [derived]. At
  the constraint, next period's m reaches its own lower bound only when ψ = ψ̲ and ξ = ξ̲
  together. The probability in κ̄ and in weak return impatience is then the probability of that
  joint event, not ℘. For a continuous ψ it is zero and κ̄ = 1. With ξ̲ = 0 every ψ leads to
  m = 0 in the event, and the probability is ℘, as in the paper.
- The two derived items above are now stated, in the appendix "Positive Minimum Income":
  - `lemma:NaturalBorrowingLimit` and `eq:FiniteMinHumanWealth` give the limit;
  - `eq:pWorst` and `lemma:MPCPositiveMinimum` give κ̄;
  - `thm:existenceNoWorst` covers the continuous ψ.

### The limiting MPCs

[stated: `eq:MPCminInv`, `eq:MPCminDefn`, `eq:MPCmaxDefn`, `lemm:MPC`, `lemma:MPCBoundsConvg`]

- Recursions, from κ̲_T = κ̄_T = 1:
  - 1/κ̲_{T−n} = 1 + Þ_R / κ̲_{T−n+1};
  - 1/κ̄_{T−n} = 1 + ℘^(1/ρ) Þ_R / κ̄_{T−n+1}.
- Limits: κ̲ = max{0, 1 − Þ_R}, the limit of c(m)/m and of the MPC as m → ∞;
  κ̄ = 1 − ℘^(1/ρ) Þ_R, the limit as m → 0.
- Closed forms n periods before the last: κ̲_{T−n} = (1 − Þ_R)/(1 − Þ_R^(n+1)) [stated: `eq:WDef`
  in the proof of `prop:pfUCFHWC`]; the same with ℘^(1/ρ) Þ_R in place of Þ_R gives κ̄_{T−n}
  [derived].
- Bounds on the limit: κ̲ m ≤ c(m) ≤ κ̄ m and c(m) > 0 [stated: `remark:cStatStrctPos`].
- κ̄ → 1 as ℘ → 0 [stated: end of `sec:LiqConstrAsLimit`].

### Human wealth

[stated: `eq:HDef`; `table:Comparison`]

- h_t = (1 − 𝓡^(−(T−t+1)))/(1 − 𝓡^(−1)). It counts the current period's income: the series
  starts at one.
- Limit: h = 1/(1 − G/R) when finite human wealth holds, infinite otherwise [derived from
  `eq:HDef`].
- It is the same with uncertainty: "the model's risks are mean-preserving spreads, so the PDV
  of future income is unchanged by their introduction".

### The perfect foresight solution and the bounds on c and v

- Finite horizon: c̄_{T−n}(m) = (m − 1 + h_{T−n}) κ̲_{T−n} [stated: the display before
  `eq:PFMPCminInv`].
- Limit, under finite human wealth and return impatience: c̄(m) = (m − 1 + h) κ̲ with
  κ̲ = 1 − Þ_R [stated: `eq:cFuncPFUnc`, `eq:MPCminDef`].
- Its value: v̄(m) = u(c̄(m))/(1 − Þ_R) [stated: proof of `prop:pfUCFHWC`].
- With no human wealth: c̲(m) = κ̲ m [stated: `table:Required`].
- Under uncertainty: c̲(m) < c(m) < c̄(m) and v̲(m) < v(m) < v̄(m) [stated: `table:Required`].
  Combined with the MPC bounds: κ̲ m ≤ c(m) ≤ min{κ̄ m, c̄(m)}, the second term available when
  finite human wealth and return impatience hold [derived].
- c(m) and v(m) approach their perfect foresight counterparts as m → ∞ when both conditions
  hold [stated: "Case 2" in `subsubsec:casesUC`].
- Value of autarky [stated: opening of `sec:ApndxLiqConstr`; `eq:ValuePFAnalyticalAutarky`]:
  u(**p**_t) (1 − F^(T−t+1))/(1 − F), where F is the value of autarky factor.

### The target and the pseudo-target

- **Buffer stock target m̂** [stated: `thm:target`, `eq:mTarget`, `eq:stability`,
  `eq:mTargImplicit`]: E_t[m_{t+1}/m_t] = 1 at m_t = m̂; below it E_t[m_{t+1}] > m_t, above it
  E_t[m_{t+1}] < m_t. Equation: (m̂ − c(m̂)) 𝓡 E[ψ⁻¹] + 1 = m̂.
- **Pseudo-target m̌** [stated: `thm:MSSBalExists`, `eq:mBalLvl`, `eq:stabilityStE`,
  `eq:balgrostable`]: E_t[ψ_{t+1} m_{t+1}/m_t] = 1 at m_t = m̌, that is, the level of market
  resources is expected to grow by G; below it E_t[**m**_{t+1}]/**m**_t > G, above it < G.
  Equation: (m̌ − c(m̌)) 𝓡 + 1 = m̌.
- The two equations differ only by 𝓡 E[ψ⁻¹] in place of 𝓡. With no permanent shocks they
  coincide [stated].
- As lines in (m, c) [derived by rearranging]: the target is where c(m) crosses
  c = (1 − 1/R̄) m + 1/R̄ with R̄ = 𝓡 E[ψ⁻¹]; the pseudo-target is where it crosses
  c = (1 − 1/𝓡) m + 1/𝓡. These are HARK's `Delta_mNrm_ZeroFunc` and `BalGroFunc`. Both use
  E[ξ] = 1 and E[ψξ] = 1.
- A third point [stated: footnote in `subsec:onetarget`]: the m at which
  E_t[log **m**_{t+1}] = log(G **m**_t). It lies between m̌ and m̂ when they exist and is
  "guaranteed to exist" under Szeidl's condition. The paper says HARK computes it as `mBalLog`.
- No single m makes **p**, **m** and **c** all grow at one expected rate; at m̂ expected
  consumption growth is below G [stated: `sec:individStability`].
- The aggregate ratio of market resources to permanent income in balanced growth is "not
  numerically the same" as m̌ [stated: same section].

### Limits of expected growth factors

- As m → ∞, with return impatience: E_t[m_{t+1}/m_t] → Þ_G E[ψ⁻¹] [stated: `eq:emgro`];
  E_t[ψ_{t+1} m_{t+1}/m_t] → Þ_G [stated: `eq:emgro2`]; E_t[**c**_{t+1}/**c**_t] → Þ [stated:
  `prop:convgGrowth`].
- As m → ∞, without return impatience: E_t[m_{t+1}/m_t] → 𝓡 E[ψ⁻¹] [stated: proof of
  `thm:target`]; E_t[ψ_{t+1} m_{t+1}/m_t] → 𝓡 [derived, same step].
- As m → 0: all three are unbounded [stated: `prop:convgGrowth` and the proofs of the two
  theorems].

## The liquidity-constrained case

### Perfect foresight with the constraint a ≥ 0

[stated: section "Perfect Foresight with Liquidity Constraints"; "Perfect Foresight Constrained
Solution" (`subsec:PFCon`); appendix `sec:ApndxLiqConstr`; `table:LiqConstrScenarios`]

- The constraint is relevant if and only if growth impatience holds: at m = 1 it binds when
  1 > Rβ G^(−ρ) [stated: `eq:LiqConstrBinds`].
- A non-degenerate limit exists if return impatience holds; if it fails, if and only if growth
  impatience holds [stated: `prop:PFCExist`]. Finite human wealth is not needed.
- **Growth impatience fails, return impatience holds.** Finite human wealth follows. The
  constraint never binds for m ≥ 1. The rule is c(m) = m below m_# and the unconstrained c̄(m)
  above it, with m_# = (h − 1) κ̲/(1 − κ̲) strictly between 0 and 1.
- **Both hold.** The constraint binds in finite time from any m. The rule is piecewise linear:
  c(m) = m up to m = 1, then kinks at m_#^n = b_#^n + 1, where n is the number of periods until
  the constraint binds:
  - c_#^n = Þ_G^(−n);
  - b_#^n = Þ_G^(−n)(1 − Þ_R^(n+1))/(1 − Þ_R) − (1 − 𝓡^(−(n+1)))/(1 − 𝓡^(−1))
    [stated: the equations labeled `eq:cPreHist`, `PDVc` and `eq:bPound`].
  The rule approaches c̄(m) and the MPC approaches κ̲ as m → ∞, whether or not human wealth is
  finite.
- **Growth impatience holds, return impatience fails.** Finite human wealth fails. The limit is
  non-degenerate, strictly positive and increasing, with the MPC tending to zero. The paper's
  example: ρ = 2, R = 0.98, β = 1.00, G = 0.99.
- **Both fail.** Degenerate. On the boundary Þ = G the rule tends to min{m, 1}, and the
  degeneracy shows only in the value function, which tends to −∞ [stated: text after
  `prop:PFCExist`].

### Uncertainty with the constraint

[stated: "The Liquidity Constrained Solution as a Limit" (`subsubsec:deatonIsLimit` and
`sec:LiqConstrAsLimit`), `eq:RestrEqUnrestr`, `remark:stochdiscMST`]

- The "liquidity constrained problem" is the setup with ℘ = 0 and the constraint c_t ≤ m_t. The
  paper calls this consumer "restrained", and "constrained" only when the constraint binds.
- Result: as ℘ falls to zero, c_t(m; ℘) tends to the restrained consumer's c_t(m). The argument
  is written for the next-to-last period with β = R = G = 1 and no permanent shocks, and said
  to generalize.
- Imposing the constraint while keeping ℘ > 0 "would not affect behavior", because the
  consumer already never ends a period with zero assets.
- The restrained consumer's first kink in the next-to-last period is at
  (𝔳′_{T−1}(0))^(−1/ρ), with 𝔳′ computed with ℘ = 0.
- On branch `20261111-positive-minimum-income`, `thm:LiqConstrLimitPositiveMinimum` proves the
  result for any R, β, G and permanent shocks. It holds at every horizon, and also in the limit
  under finite value of autarky. It covers a positive minimum income as well. See "The liquidity-constrained solution as a limit" under the
  appendix.

### How the conditions change

- The paper proves no existence theorem for uncertainty with an artificial constraint. With
  ℘ = 0 the problem is "a special case of" Ma, Stachurski and Toda's, with stochastic return
  𝓡̃ and stochastic discount factor β G̃^(1−ρ) [stated: `remark:stochdiscMST`]. Their
  discounting assumption "is a generalization of" finite value of autarky, and their stability
  condition β G̃^(1−ρ) 𝓡̃ < 1 is stronger than strong growth impatience [stated: footnote in
  `subsec:GICTheorySetup` and the text after `ass:GICMod`].
- At ℘ = 0 the weak return impatience factor is zero, so that condition holds trivially. The
  paper says it "does not approach irrelevance": the set of parameters for which it matters
  shrinks as ℘ → 0, and the constraint takes over its role [stated: under `ass:WRIC` and in
  `subsec:TheModelUncertainty`].
- "In the presence of a constraint neither return impatience nor growth impatience is
  individually necessary for nondegeneracy"; if both fail the consumption function is
  degenerate [stated: opening of `sec:GICdiscussion`].
- κ̄ = 1 for a constrained consumer [stated: end of `sec:LiqConstrAsLimit`].
- Not in the paper: a borrowing limit other than zero; a formal treatment of an artificial
  constraint together with ℘ > 0; the target theorems under an artificial constraint.
- The appendix "Positive Minimum Income" covers each of these:
  - a borrowing limit −h̲_t below zero (`item:Restrained`);
  - c ≤ m in every period with ℘ > 0 and ξ_u > 0 (`item:Artificial`);
  - existence and the targets for both (`thm:existenceNoWorst`, `prop:NoWorstTargets`).

  With ξ_u = 0 an artificial c ≤ m never binds, as the paper says.

## The appendix "Positive Minimum Income"

[stated: `sec:ApndxPositiveMinimumIncome`, in `Appendices/ApndxPositiveMinimumIncome.tex`]

Added to this digest on 2026-11-12 at Chris's request, typed in the BufferStockTheory-Latest
session at about 15:20 EST: "You have already constructed a digest for the paper.  Add to that
digest a digest of the newly constructed Appendix E".

**Where it is.** Only on branch `20261111-positive-minimum-income`, which is local and not pushed.
The branch was cut from the tip of pull request 163 (`6a55ccad`). Chris accepted the appendix on
2026-11-11 (`5978e774`) and its revision on 2026-11-12 (`ed059e54`). This section reads the
branch at `2e875060`. The appendix prints as Appendix E in that build. Letters move, so cite
its label. The same branch also holds the repair from pull request 161 (`e9f363eb`) and the
corrected sentence in `subsec:Setup` (see "Income in the zero-income event").

**What it does.** It carries out the capitalization that the paper's one sentence claims, and
finds that with permanent shocks it does not give back the paper's model. The [derived] items
under "The restriction Chris asked for" and "The natural borrowing constraint" are stated in the
appendix. Every item in this section is [stated] at the label given unless marked otherwise.

### Symbols it adds

| Here | Paper macro | Meaning | HARK name |
|---|---|---|---|
| ξ_u | `\IncUnemp` | income in the unemployment event, a fraction of **p** | `IncUnemp` |
| ℘_ψ | `\pZeroPerm` | probability that ψ takes its lowest value ψ̲ | none |
| p_worst | `\pWorst` | probability of the worst event | `WorstPrb` (computed differently: see below) |
| h̲ | `\hNrmPes` | minimum human wealth; excludes current income | none (`BoroCnstNat` is −h̲) |
| m̲ | `\mNrmMin` | lowest m from which positive consumption is feasible, = −h̲ | `mNrmMin` |
| m̈, ä, c̈, v̈ | `\nbl{}` | measured from the borrowing limit: m̈ = m + h̲_t | none |
| ξ̈ | `\tranShkNbl` | income in those units | none |
| θ_min | `\IncEmpMin` | lowest income outside the unemployment event | none |

The paper's ℘ is called the probability of the "unemployment event" here, because income in it
is no longer zero.

### The income process

[stated: `ass:shocksPositiveMinimum`, `eq:TranShkDefPositiveMinimum`, `eq:MinIncomeBelowEmployed`,
`eq:pWorst`]

- ψ is as in `ass:shocks`, and in addition takes its lowest value ψ̲ with probability ℘_ψ > 0.
  Its other values are no smaller than some ψ̲_next > ψ̲.
- ξ = ξ_u with probability ℘ > 0; otherwise ξ = θ (1 − ℘ ξ_u)/(1 − ℘). The scaling keeps
  E[ξ] = 1, as HARK's does.
- **0 ≤ ξ_u < θ_min := θ̲ (1 − ℘ ξ_u)/(1 − ℘)**, equivalently ξ_u < θ̲/(1 − ℘(1 − θ̲)). This is
  the restriction Chris asked for, with the bound this digest derived.
- {ψ_t, ξ_t} is iid over time, and ψ_t and ξ_t are independent of each other. The appendix states
  this independence; `ass:shocks` does not.
- **How to build ψ** [stated: the paragraph after the assumption]. With probability ℘_ψ, ψ is the
  infimum ψ̲ of a continuous mean-one law. Otherwise it is a draw from that law times
  (1 − ℘_ψ ψ̲)/(1 − ℘_ψ). Then E[ψ] = 1 whatever discretization is used for the rest, and
  ψ̲_next = ψ̲ (1 − ℘_ψ ψ̲)/(1 − ℘_ψ).
  - This follows Chris's rule, typed in the HARK-dev session on 2026-11-11 at 21:55:00 EST: a
    discretized shock's lowest value is the law's infimum.
  - HARK's equiprobable laws put the lowest value at the lowest grid point, with probability one
    over the number of points, so both move with the grid.
- **The worst event** is {ψ = ψ̲, ξ = ξ_u}.
  - p_worst = ℘ ℘_ψ if ξ_u > 0.
  - p_worst = ℘ if ξ_u = 0, because zero income is zero whatever ψ is.
  - The jump at ξ_u = 0 is real: for every ξ_u > 0, however small, the maximal MPC uses ℘ ℘_ψ.
- **The problem** [stated: `eq:veqnPositiveMinimum`]:
  - The constraint c ≤ m holds only at T (no debt at death); before T the consumer may borrow.
  - With ξ_u = 0 this is the paper's problem.
  - With ξ_u > 0, keeping c ≤ m in every period is an artificial constraint that binds. That is
    problem (c) of "When the borrowing limit can be reached" below, and it is what HARK's
    `BoroCnstArt=0` with `IncUnemp>0` solves.

### Minimum human wealth and the natural borrowing limit

[stated: `eq:hNrmMinRecursion`, `lemma:NaturalBorrowingLimit`, `eq:FiniteMinHumanWealth`]

- **Minimum human wealth:**
  - h̲_T = 0 and h̲_t = (Gψ̲/R)(ξ_u + h̲_{t+1}), so h̲_{T−n} = ξ_u Σ_{j=1..n} (Gψ̲/R)^j.
  - It is the present value of minimum income along the path on which every permanent shock is
    ψ̲: what a lender who must be repaid with certainty will lend.
  - Unlike the paper's h, it leaves out current income.
- **The feasible set:** a feasible plan exists if and only if m_t > −h̲_t, and the feasible
  choices are a_t > −h̲_t, that is 0 < c_t < m_t + h̲_t. The limit is never reached.
- **The limit as the horizon grows:**
  - h̲ is finite if and only if ξ_u = 0 or **Gψ̲ < R**, and then h̲ = ξ_u Gψ̲/(R − Gψ̲).
  - Finite human wealth implies this condition, but not conversely, and the paper's existence
    results do not need finite human wealth.
  - When G ≥ R, this condition restricts ψ̲.
  - The appendix keeps this condition from that point on, and calls it finite minimum human
    wealth.
- **Lower bound of m:** m̲_t = −h̲_t, with limit −h̲. With ξ_u = 0 this is the paper's 0. HARK's
  `calc_boro_const_nat` is the same recursion, applied to the lowest point of its grid for ψ.

### Resources measured from the limit

[stated: `eq:nblDefs`, `eq:tranShkNbl`, `lemma:ExcessResources`, `remark:TransformingBack`]

- **The change of variables:**
  - m̈ = m + h̲_t and ä = a + h̲_t;
  - ξ̈_{t+1} = (ξ_{t+1} − ξ_u) + (ξ_u + h̲_{t+1})(1 − ψ̲/ψ_{t+1});
  - m̈_{t+1} = ä_t 𝓡̃_{t+1} + ξ̈_{t+1}.
- **The problem in m̈** is the paper's normalized problem with ξ̈ in place of ξ, and the choice c
  in (0, m̈).
- **Properties of ξ̈:**
  - (a) ξ̈ ≥ 0, with equality exactly in the worst event.
  - (b) Outside the worst event ξ̈ ≥ min{θ_min − ξ_u, ξ_u (1 − ψ̲/ψ̲_next)} > 0.
  - (c) ξ̈ is bounded.
  - (d) Shock by shock, ξ̈ is non-decreasing in the horizon and converges geometrically, at the
    rate Gψ̲/R.
  - (e) E[ξ̈] = 1 − ξ_u + (ξ_u + h̲_{t+1})(1 − ψ̲ E[ψ⁻¹]), which need not be one. ξ̈ depends on ψ
    unless ξ_u = 0 or there are no permanent shocks.
- **Transforming back.** Without permanent shocks, dividing by 1 − ξ_u turns the problem in m̈
  into exactly the paper's, with a mean-one θ. In the original variables c_t(m) is (1 − ξ_u)
  times the paper's rule evaluated at (m + h̲_t)/(1 − ξ_u). With permanent shocks it is not an
  instance of the paper's problem. This is the corrected form of the paper's one-sentence claim.

### Results when ψ has a point mass at ψ̲

The hypotheses are `ass:shocksPositiveMinimum`, finite minimum human wealth,
**p_worst^(1/ρ) Þ_R < 1** (`eq:WRICWorst`, the paper's weak return impatience with p_worst in
place of ℘) and finite value of autarky.

- **When ξ_u > 0 the third hypothesis is not separate** [stated: `remark:WRICWorstImplied`].
  Finite value of autarky and Gψ̲ < R imply p_worst^(1/ρ) Þ_R < 1, so the hypotheses come down
  to finite value of autarky and Gψ̲ < R. When ξ_u = 0, `eq:WRICWorst` is the paper's weak
  return impatience.
- **Shape at each horizon** [stated: `prop:cfuncpropPositiveMinimum`]: c̈_t is C², strictly
  increasing and strictly concave, with 0 < c̈_t(m̈) < m̈. v̈_t is as in the paper.
- **MPCs** [stated: `lemma:MPCPositiveMinimum`, `eq:MPCInvPositiveMinimum`,
  `eq:cBoundsPositiveMinimum`]:
  - The recursions start from κ̲_T = κ̄_T = 1:
    - 1/κ̲_{T−n} = 1 + Þ_R/κ̲_{T−n+1};
    - 1/κ̄_{T−n} = 1 + p_worst^(1/ρ) Þ_R/κ̄_{T−n+1}.
  - The limits:
    - κ̄ = 1 − p_worst^(1/ρ) Þ_R, the MPC as m → −h̲;
    - κ̲ = max{0, 1 − Þ_R}, unchanged.
  - The bounds: κ̲_t (m + h̲_t) ≤ c_t(m) ≤ κ̄_t (m + h̲_t).
- **Existence** [stated: `thm:cmapPositiveMinimum`, `thm:existencePositiveMinimum`]:
  - There is a non-degenerate limiting solution on (−h̲, ∞), with c(m) = c̈(m + h̲) > 0. Value
    converges in a weighted norm.
  - The proof's new element: the operators differ across horizons, through ξ̈, and the
    perturbation is summable.
- **The limiting rule** [stated: `lemma:MPCBoundsConvgPositiveMinimum`]:
  - c is concave and non-decreasing, and strictly increasing under return impatience.
  - It satisfies the Euler equation, κ̲ (m + h̲) ≤ c(m) ≤ κ̄ (m + h̲), and slopes in [κ̲, κ̄].
- **Two bounds carry over** [stated: the paragraph after that lemma]:
  - Under finite human wealth and return impatience, c(m) ≤ (m − 1 + h) κ̲.
  - So c lies between the perfect foresight consumption of a consumer who counts only minimum
    human wealth and that of one who counts all of human wealth.
  - As income risk vanishes (ξ_u → 1, ψ̲ → 1), h̲ → h − 1 and the two bounds coincide.
- **The target and the pseudo-target** [stated: `eq:difFuncsPositiveMinimum`,
  `thm:targetPositiveMinimum`, `thm:pseudoTargetPositiveMinimum`]:
  - The target needs strong growth impatience in addition; the pseudo-target needs growth
    impatience. Each exists and is unique in (−h̲, ∞).
  - The equations are the paper's, written as differences because m can be zero or negative:
    - E_t[m_{t+1}] − m_t = 𝓡 E[ψ⁻¹] a(m_t) + 1 − m_t;
    - E_t[ψ_{t+1} m_{t+1}] − m_t = 𝓡 a(m_t) + 1 − m_t.
- **Their sign and order** [stated: `lemma:orderingPositiveMinimum`, needs ψ not degenerate]. These
  six quantities have the same sign:
  - 1 − c(1);
  - m̌ − 1 and m̂ − 1;
  - a(m̌) and a(m̂);
  - m̂ − m̌.

  So if a consumer with no assets and mean income borrows (c(1) > 1):
  - both targets are below one;
  - the consumer is a borrower at both;
  - the target is **below** the pseudo-target.

  Either target may be negative. A class must allow negative targets and must not assume
  m̌ < m̂.
- **Consumption growth** [stated: after that lemma]: `prop:convgGrowth` carries over.
  E_t[**c**_{t+1}/**c**_t] → ∞ as m → −h̲, and → Þ as m → ∞ under return impatience.
- **Invariant distributions** [stated: `prop:invariantPositiveMinimum`, `eq:mNblProcess`,
  `eq:HarmTransition`]. The hypotheses are those of existence plus return impatience.
  - (i) If log Þ_G < E[log ψ] (Szeidl's condition), m has a unique invariant distribution, and
    its distribution converges to it from any start.
  - (ii) If log Þ_G < E[ψ log ψ], the same holds for the distribution weighted by permanent
    income.
  - (iii) Under growth impatience, aggregate c, m and a are constant multiples of aggregate **p**,
    and aggregate consumption grows by G. The multiples for m and a can be zero or negative.
  - Why the proof is new: Szeidl's buffer-stock proposition assumes no borrowing and independent
    shocks. In m̈, ξ̈ depends on ψ, so the appendix verifies the hypotheses of Szeidl's general
    theorem for increasing Markov processes (his Theorem 1) instead. Harmenberg's result is
    derived directly and does not need independence.

### When the borrowing limit can be reached

[stated: `subsec:PositiveMinimumNoWorstEvent`]

In three problems ξ̈ > 0 with probability one, so a consumer who ends a period at the limit is
sure to be above it in the next:

- **(a) `item:NoPointMass`.** ξ_u > 0, and ψ has no mass at ψ̲, the lowest point of its support:
  a continuous ψ. The limit a = −h̲_t can be chosen.
- **(b) `item:Restrained`.** There is no unemployment event, and a_t ≥ −h̲_t, where h̲_t comes from
  some ξ_u in [0, θ̲). This limit is tighter than the natural one. With ξ_u = 0 this is the
  paper's restrained consumer.
- **(c) `item:Artificial`, titled "No borrowing".** `ass:shocksPositiveMinimum` with ξ_u > 0, and
  c ≤ m in every period, so h̲ ≡ 0. The worst event still has positive probability, but
  ξ̈ = ξ ≥ ξ_u > 0.

The problem is `eq:veqnNoWorst`: the same, with the choice 0 < c ≤ m̈, so the limit is included.

- **Each horizon** [stated: `lemma:NoWorstFinite`, `coro:ConcaveNoWorst`]:
  - The rule is unique, continuous, strictly increasing and concave, with slopes in [κ̲_t, 1].
  - The Euler equation holds with equality where c̈ < m̈.
  - c̈/m̈ → 1 as m̈ → 0.
  - The limit binds (c̈ = m̈) exactly for m̈ ≤ m̈_#,t = (R β E[G̃^(−ρ) c̈_{t+1}(ξ̈)^(−ρ)])^(−1/ρ).
    This is positive if and only if E[ξ̈^(−ρ)] < ∞:
    - always in (b) and (c);
    - in (a) if and only if E[(ψ − ψ̲)^(−ρ)] < ∞.
  - Otherwise the rule approaches the limit with a slope that tends to one.
- **MPCs:** κ̄_t = 1 at every horizon before the last; κ̲_t is as before.
- **Existence** [stated: `thm:existenceNoWorst`]:
  - It needs finite value of autarky, plus finite minimum human wealth in (a) and (b).
  - It does not need `eq:WRICWorst` or return impatience.
  - The limiting rule is concave and non-decreasing with slopes in [κ̲, 1], with c̈/m̈ → 1 at the
    limit and → κ̲ as m → ∞. It satisfies the Euler equation wherever c < m + h̲.
  - The proof is different from the main case's: it bounds consumption by the rule for the
    next-to-last period and uses Hölder's inequality.
- **Targets and aggregates** [stated: `prop:NoWorstTargets`]:
  - The target, pseudo-target, ordering and invariant-distribution results hold under the same
    additional conditions.
  - In (b), the invariant distributions also need θ not degenerate.
  - In (c) the consumer never borrows, so both targets are at least one, and both equal one if
    the constraint binds at m = 1.

### The liquidity-constrained solution as a limit

[stated: `thm:LiqConstrLimitPositiveMinimum`]

- Fix ξ_u in [0, θ̲) and every parameter other than ℘. As ℘ ↓ 0, the solution converges to that
  of problem (b) with the same ξ_u and ψ:
  - (i) c_t(m; ℘) and v_t(m; ℘) converge at every horizon t and every m > −h̲_t;
  - (ii) if finite value of autarky holds and ξ_u = 0 or Gψ̲ < R, the limiting solutions exist
    for small ℘ and converge too.
- With ξ_u = 0 this proves the paper's `eq:RestrEqUnrestr` at every horizon and in the limit.
  The paper's own argument covers only the next-to-last period (see "Uncertainty with the
  constraint").
- Size of the gap: the largest distance between the two rules over m + h̲ in [0.001, 30]:
  - with ξ_u = 0.3, from 0.12 at ℘ = 0.05 to 0.0005 at ℘ = 5 × 10⁻⁶;
  - with ξ_u = 0, from 0.30 to 0.011.
- κ̄ → 1 as ℘ → 0.
- Read the other way: a constraint a_t ≥ −h̲_t is the limit, as ℘ → 0, of natural limits
  generated by unemployment insurance. In the limit h̲ can be any fraction of permanent income
  below θ̲ Gψ̲/(R − Gψ̲).

### When the hypotheses fail

[stated: `subsec:PositiveMinimumFailures`, `prop:InfiniteMinHumanWealth`]

- **`eq:WRICWorst` fails while h̲ is finite.** Then κ̄_{T−n} → 0 and c_{T−n}(m) → 0 at every m, so
  the solution is degenerate. With ξ_u > 0 this happens only if finite value of autarky fails.
- **Minimum human wealth is infinite** (ξ_u > 0 and Gψ̲ ≥ R). Then h̲_{T−n} → ∞.
  - If lim c_{T−n}(m) is finite and positive at any one m, it is the same constant at every m,
    and R β E[G̃^(−ρ)] = 1, which contradicts finite value of autarky. So under finite value of
    autarky there is no non-degenerate limiting solution.
  - c_{T−n}(m) → ∞ if Þ < Gψ̲, in particular under return impatience.
  - c_{T−n}(m) → 0 if p_worst^(1/ρ) Þ > Gψ̲ or Þ > G.
  - c_{T−n}(m + Δ)/c_{T−n}(m) → 1: consumption becomes flat in m.
  - **Open:** when Gψ̲ ≤ Þ ≤ G and p_worst^(1/ρ) Þ ≤ Gψ̲, the bounds do not say whether c goes to
    zero, goes to infinity, or fails to converge. In the examples computed it goes to infinity.
  - The first statement and the parts on infinity and flatness also hold for problem (a).
- **Perfect foresight:** unaffected, since that model has no unemployment event.

### What a class built on the appendix would need [derived; not in the appendix]

- **Parameters:**
  - ξ_u ≥ 0, checked against the bound above;
  - ℘_ψ, with the point mass at the infimum of the continuous law, or zero for problem (a).
- **Report p_worst from the parameters,** not from the grid: ℘ ℘_ψ when ξ_u > 0, ℘ when ξ_u = 0.
  HARK's `WorstPrb` is the mass of the lowest grid atom, so it changes with the number of points
  (see "The probability of the worst event").
- **When ξ_u > 0, check Gψ̲ < R.**
  - If it fails and finite value of autarky holds, there is no non-degenerate limiting solution.
    Refuse, or report that.
  - If it holds, `eq:WRICWorst` follows from finite value of autarky. Computing it as well does no
    harm.
- **When P(ξ̈ = 0) = 0** (problems (a), (b), (c)):
  - report κ̄ = 1;
  - expect a region near the limit where it binds: everywhere below a point in (b) and (c), and
    in (a) only when E[(ψ − ψ̲)^(−ρ)] < ∞.
- **Targets:** allow negative values, and do not assume their order.

### Test values

[stated: `table:PositiveMinimumExample` and the paragraph after it.] These use the baseline
calibration. ψ has a point mass Φ(−3) = 0.00135 at ψ̲ = 0.734, the infimum of a mean-one
lognormal truncated at three standard deviations of its log, whose standard deviation after
truncation is 0.1. θ has the same truncated law without the point mass. The continuous part of
each law uses seven equiprobable points. In the ξ_u = 0 column ψ has no point mass, so that
column is the paper's model.

| | ξ_u = 0 | ξ_u = 0.05 | ξ_u = 0.3 | ξ_u = 0.5 |
|---|---|---|---|---|
| p_worst | 0.005 | 6.7 × 10⁻⁶ | 6.7 × 10⁻⁶ | 6.7 × 10⁻⁶ |
| h̲ | 0 | 0.133 | 0.799 | 1.332 |
| κ̄ | 0.9321 | 0.9975 | 0.9975 | 0.9975 |
| κ̲ | 0.039 | 0.039 | 0.039 | 0.039 |
| c(1) | 0.853 | 0.942 | 1.105 | 1.152 |
| target m̂ | 1.392 | 1.190 | 0.381 | −0.126 |
| pseudo-target m̌ | 1.378 | 1.183 | 0.405 | −0.080 |
| a(m̂) | 0.385 | 0.186 | −0.607 | −1.105 |

Variations at ξ_u = 0.3:
- **(a) No point mass**, with 200 equiprobable points:
  - m̂ = 0.393 and m̌ = 0.417, against 0.399 and 0.424 with the point mass, also at 200 points.
  - At 800 points: 0.3931 and 0.4179.
  - The limit is computed from the law's infimum, which no grid point reaches.
- **(c) No borrowing**, with seven points:
  - The constraint binds below m = 0.946.
  - m̂ = 1.100 and m̌ = 1.097.
- **Against HARK 0.17.2**, with `BoroCnstArt=0`, `IncUnemp=0.3` and HARK's own equiprobable laws:
  - the largest difference in c is 3.6 × 10⁻⁵;
  - the constraint binds below m = 0.9466 (HARK's grid for ψ, so not the table's law).

Scripts on the appendix's branch, in `Code/Python/PositiveMinimumIncome/`, each with its output
beside it:
- `infimum_law_example.py`: the table;
- `no_worst_event_checks.py`: the revision's results and these variations;
- `positive_income_checks.py`: the solver against HARK;
- `simulate_invariant.py`, `sweep_ordering.py` and `explore_cases.py`: further checks.

## What the paper leaves open

Each item is something a model class has to decide. "My view" lines are this session's, not
rulings.

- **Mortality.** The model has none. The section "Mortality Yields Invariance" describes two
  schemes in prose.
  - *Blanchard* (estates annuitized to survivors): effective discount factor βℒ and effective
    interest factor R/ℒ, so Þ is unchanged, and "the RIC … becomes Þ/R̄" with R̄ = R/ℒ. The
    paper says these are "the only adjustments", but the value of autarky factor uses β alone
    and the finite human wealth factor uses R alone; it does not say what they become. Its
    display for this scheme omits the exponent 1/ρ on the left-hand side.
  - *Modigliani* (estates destroyed): the condition for balanced growth "changes from the plain
    growth impatience to a looser mortality-adjusted version", ℒ Þ_G < 1 (`eq:GICLivMod`). The
    paper does not say whether Þ there is built from β or from βℒ. **Port branch only:** "the
    Modigliani scheme lowers [Þ_G] to ℒ^(1/ρ) Þ_G".
  - The two readings of `eq:GICLivMod` are ℒ (Rβ)^(1/ρ)/G and ℒ^(1+1/ρ) (Rβ)^(1/ρ)/G. HARK
    computes the second.
  - My view: the second reading is the coherent one for destroyed estates (survivors discount by
    βℒ and the cohort shrinks by ℒ), but the paper does not say it. The simplest class that
    matches the paper has no mortality.
- **Income in the zero-income event.** The paper has zero, and a one-sentence claim that a
  positive minimum can be transformed away. With permanent shocks the transformation changes
  which probability enters κ̄ and weak return impatience (see "The natural borrowing
  constraint"). The choice: require zero, which matches the paper exactly; or allow a positive
  amount below the bound in "The restriction Chris asked for" and document that κ̄ then uses the
  probability of the joint worst event. The appendix "Positive Minimum Income" now supplies the
  theory for the second choice, with the point mass of ψ at its infimum. Its list under "What a
  class built on the appendix would need" is what that choice entails.
- **Independence of ψ and ξ within a period.** Used, not stated in `ass:shocks`.
- **Whether β < 1.** The setup requires only β > 0. One passage says "(with ρ > 1 and β < 1)"
  and "since β < 1 by assumption". The appendix's own example uses β = 1.00. My view: admit any
  β > 0.
- **Bounded supports against a lognormal calibration.** A class that takes discretized
  distributions satisfies `ass:shocks`. But ψ̲, ψ̄, θ̲, θ̄ and every factor with an expectation
  then depend on the discretization: the modified growth patience factor is 0.97920 with seven
  equiprobable points and 0.97985 for the lognormal itself. The paper does not say which its
  conditions refer to.
- **Finite value of autarky fails while weak return impatience holds.** No result. A footnote
  says "it should be possible to extend the circumstances under which the problem can be shown
  to define a contraction mapping to the union of the parameter values under which {RIC, FHWC}
  hold and {FVAC, WRIC} hold", "left for future work" [stated: first footnote of
  `sec:individStability`]. A class has to choose between refusing, warning, and reporting
  "not established".
- **What to report when a target condition fails.** The theorems are sufficiency only. See the
  convexity argument under "What happens when a condition fails".
- **The lower bound of m.** The paper points to an m̲ it never defines.
- **Names.** The paper's terms are "buffer stock target" for m̂ and "pseudo-target" for m̌ (a
  comment in the source of `sec:individStability` records that choice), but one sentence there
  calls m̌ "a buffer stock target", an appendix heading says "Pseudo-Steady-State", and HARK
  says `mNrmStE`. The first of these is recorded as an open defect in this repository's memory.
- **Simulation.** The paper specifies no initial distribution, newborns or population dynamics
  beyond "a continuum of ex ante identical buffer-stock households, with constant total mass
  normalized to one".
- **Time-varying parameters and life cycles.** Outside the paper, apart from one footnote on G.
- **Defects in the text that a reader should not build on.**
  - "Case 3" in `subsubsec:casesUC` ends "under return impatience and finite human wealth, we
    must have growth impatience". As worded it is false (R = 1, G = 0.8, β = 0.9025, ρ = 2).
    The display above it shows what is meant: given finite value of autarky, when finite human
    wealth fails, growth impatience holds.
  - `subsec:TheModelUncertainty` says that with ℘ = 1 weak return impatience "is identical to
    weak return impatience". It means return impatience.
  - `table:Calibration` gives the "Weak Return Impatience Factor" as ℘^(1/ρ) Þ = 0.071. The
    condition compares ℘^(1/ρ) Þ/R = 0.068 with one. The same table writes the finite human
    wealth factor with the symbol for the realized 𝓡̃.
  - In the appendix on liquidity constraints, a footnote gives the point where the constraint
    would bind when growth impatience fails as G/Þ. The text's m_# = (h − 1) κ̲/(1 − κ̲) is the
    point where c̄(m) = m; the two differ unless Þ = G (with R = 1.03, G = 1, β = 1, ρ = 2:
    0.4963 against 0.9853).
  - `rem:shnkrdef` defines the modulus as any number in an open interval; a later sentence in
    the proof of `thm:cmap` still says it equals the maximum.
  - `subsubsec:deatonIsLimit` cites the existence theorem's label where it means `ass:shocks`.

## Where HARK's `IndShockConsumerType` departs from the paper

Read from `HARK/ConsumptionSaving/ConsIndShockModel.py`,
`HARK/Calibration/Income/IncomeProcesses.py` and `HARK/distributions/utils.py` at upstream
`main`, `f86e2551` (2026-11-08). Items marked "run" were also run on HARK 0.17.2; the outputs
are under "Test values".

### Scope

- The class is a life-cycle class: parameters can vary over time, there is a survival
  probability, an artificial borrowing constraint, retirement, and a finite horizon by default.
  The paper's model is the case `cycles=0`, `T_cycle=1`, `LivPrb=[1.0]`, `BoroCnstArt=None`,
  `IncUnemp=0.0`, `T_retire=0`.
- The defaults are far from the paper: `cycles=1`, `LivPrb=[0.98]`, `BoroCnstArt=0.0`,
  `UnempPrb=0.05`, `IncUnemp=0.3`, `Rfree=[1.03]`, `PermGroFac=[1.01]`.
- The conditions are evaluated only when `cycles=0` and `T_cycle=1`, and only reported: `solve`
  goes ahead whatever they say.

### What is not validated

- The only parameter check is that `DiscFac` is not negative (`check_restrictions`).
- ρ > 1 is not required.
- Nothing checks that a supplied `IncShkDstn` has E[ψ] = 1 and E[ξ] = 1, or that the shocks are
  strictly positive. The lines used to find the target and pseudo-target assume both means.
- Nothing checks 0 < ℘ < 1, or that `IncUnemp` is below the smallest employed draw.

### The probability of the worst event

- There is no parameter for it. `calc_worst_inc_prob` infers it from the discretized joint
  distribution as the mass at the smallest value of ψξ.
- With `IncUnemp=0` this is `UnempPrb`, as in the paper (run: 0.00500).
- With `IncUnemp>0` it is the mass of the single atom with the smallest ψ and the smallest ξ:
  `UnempPrb` divided by the number of permanent shock points. Run at the paper's calibration
  with `IncUnemp=0.3`: `WorstPrb` 0.00071, `MPCmax` 0.97432 in place of 0.93206. That is right
  for the discretized model (see "The natural borrowing constraint"), but it is a property of
  the discretization, not of ℘.
- With `IncUnemp` above the smallest employed draw, HARK silently treats that employed draw as
  the worst event (run with `IncUnemp=0.95`: `WorstPrb` 0.02031, `MPCmax` 0.86309).
- In the appendix "Positive Minimum Income", p_worst = ℘ ℘_ψ, with ℘_ψ a parameter: the point
  mass of ψ at the infimum of its continuous law. At the appendix's example this is
  6.7 × 10⁻⁶ and κ̄ = 0.9975.

### Survival inside the factors

- `APFac` is (R β ℒ)^(1/ρ). So `RPFac`, `GPFacRaw`, `GPFacMod`, `WRPFac`, `MPCmin` and `MPCmax`
  all carry ℒ^(1/ρ). This is discounting by βℒ with R unchanged, the destroyed-estates scheme.
  The paper's Þ has no ℒ. With `LivPrb=[1.0]` they agree.
- `PFVAFac` is βℒ G^(1−ρ), but `VAFac` is β G^(1−ρ) E[ψ^(1−ρ)] with no ℒ. With ℒ < 1 the two
  are inconsistent with each other (run with ℒ = 0.98: 0.91340 and 0.94078).
- `GPFacLiv` is ℒ times `GPFacRaw`, that is ℒ^(1+1/ρ) (Rβ)^(1/ρ)/G: one of the two readings of
  the paper's `eq:GICLivMod`.
- `GPFacLivMod` is ℒ times `GPFacLiv`, described as "Modigliani Mortality-Adjusted". It is
  computed but not checked, and the paper has no counterpart.

### Messages

- Weak return impatience: the message prints "℘ Þ/R < 1". The code computes ℘^(1/ρ) Þ/R, which
  is right.
- Return impatience fails: the message says the consumer is "pathologically impatient". The
  paper's word for this case is patient.
- "Because the RIC is satisfied but the FHWC is violated, the GIC is satisfied" is true only
  given finite value of autarky.
- Szeidl's condition fails: the message says invariant distributions "do not exist". The paper
  states sufficiency (and, port branch only, a converse under strict failure and a proviso).
- Harmenberg's condition: the message speaks of "a target ratio of the individual market
  resources to permanent income, under the permanent-income-neutral measure". The paper's
  statement is that an invariant permanent-income-weighted distribution exists.
- Finite value of autarky fails: "might not be a contraction mapping … Proceed with caution"
  matches the paper's silence. Weak return impatience fails: "degenerate at c(m) = 0" matches
  the derivation above.

### Names and conventions

- HARK's `TranShk` and its θ are the paper's ξ, the transitory shock including the zero-income
  event. The paper's θ, the shock when income is not zero, has no HARK name.
- `mNrmStE` is the pseudo-target m̌; `mNrmTrg` is the target m̂. The paper says HARK computes a
  third point as `mBalLog`; HARK does not have it.
- `solution.hNrm` leaves out the current period's income, and its limit is (G/R)/(1 − G/R).
  `bilt["hNrm"]` includes it and is the paper's h = 1/(1 − G/R). HARK's limiting rule
  κ̲(m + `solution.hNrm`) equals the paper's (m − 1 + h) κ̲.
- The conditions use moments of the discretized distributions.
- The docstring of `BufferStockIncShkDstn` says the distribution is "as modeled in the Buffer
  Stock Theory paper", while admitting `IncUnemp > 0`.

### Stable points

- `calc_stable_points` looks for the target only when growth impatience holds, by Newton's
  method from m = 1 with no bracket. Under strong growth impatience the root is unique, as the
  theorem says. When it fails there can be no root or two (see "What happens when a condition
  fails"), and the method does not distinguish them.

### What already matches

- The normalized Bellman equation and transitions, with ℒ = 1.
- The scaling of employed draws at `IncUnemp=0`: θ/(1−℘).
- The recursions for κ̲_t and κ̄_t, and the natural borrowing constraint (zero when the worst
  income is zero).
- The formulas for the growth, modified growth, Szeidl and Harmenberg conditions, the finite
  human wealth factor, and the two value of autarky factors with ℒ = 1.
- The equations for the target and pseudo-target.

## Test values

### From the paper

[stated: `table:Calibration`, "approximate calculated value"]

| Object | Value |
|---|---|
| finite human wealth factor G/R | 0.990 |
| perfect foresight value of autarky factor | 0.932 |
| growth compensated permanent shock | 0.990 |
| uncertainty-adjusted growth | 1.020 |
| utility compensated permanent shock | 0.990 |
| absolute patience factor | 0.999 |
| return patience factor | 0.961 |
| growth patience factor | 0.970 |
| modified growth patience factor | 0.980 |
| value of autarky factor | 0.941 |
| ℘^(1/ρ) Þ | 0.071 |

### Computed for this digest

Not from the paper. Closed forms at the paper's calibration:

| Object | Value |
|---|---|
| Þ | 0.999200 |
| Þ_R | 0.960769 |
| Þ_G | 0.970097 |
| G/R | 0.990385 |
| β G^(1−ρ) | 0.932039 |
| ℘^(1/ρ) Þ_R | 0.067937 |
| κ̲ | 0.039231 |
| κ̄ | 0.932063 |
| h, counting current income | 104 |
| h, not counting it | 103 |
| lognormal ψ: E[ψ⁻¹] | 1.010050 |
| lognormal ψ: modified growth patience factor | 0.979846 |
| lognormal ψ: value of autarky factor | 0.941406 |
| lognormal ψ: E[log ψ] | −0.005 |
| lognormal ψ: E[ψ log ψ] | 0.005 |

Solved with HARK 0.17.2 (`IndShockConsumerType`, `cycles=0`, `LivPrb=[1.0]`,
`BoroCnstArt=None`, `IncUnemp=0`, equiprobable discretization with the same number of points for
both shocks, 400 asset points up to 100, cubic interpolation, tolerance 1e-10):

| Points | Support of ψ | Smallest employed ξ | Modified growth patience factor | Value of autarky factor | Pseudo-target m̌ | Target m̂ | c(m̂) |
|---|---|---|---|---|---|---|---|
| 7 | [0.8504, 1.1664] | 0.8547 | 0.979199 | 0.940784 | 1.37732 | 1.39103 | 1.00736 |
| 15 | [0.8202, 1.2089] | 0.8243 | 0.979607 | 0.941176 | 1.38312 | 1.39794 | 1.00765 |
| 31 | [0.7958, 1.2456] | 0.7998 | 0.979751 | 0.941314 | 1.38524 | 1.40048 | 1.00776 |

In all three: E[ψ] = E[ξ] = 1 to six decimals, lower bound of m = 0, κ̲ = 0.039231,
κ̄ = 0.932063.

HARK's condition factors at variations on the paper's calibration (seven points, HARK 0.17.2):

| Case | `APFac` | `PFVAFac` | `VAFac` | `GPFacLiv` | `WorstPrb` | `MPCmax` |
|---|---|---|---|---|---|---|
| the paper's calibration | 0.99920 | 0.93204 | 0.94078 | 0.97010 | 0.00500 | 0.93206 |
| `IncUnemp=0.3` | 0.99920 | 0.93204 | 0.94078 | 0.97010 | 0.00071 | 0.97432 |
| `IncUnemp=0.95` | 0.99920 | 0.93204 | 0.94078 | 0.97010 | 0.02031 | 0.86309 |
| `LivPrb=[0.98]` | 0.98916 | 0.91340 | 0.94078 | 0.94114 | 0.00500 | 0.93275 |

## Sources

- Paper source read in full for this digest: `sections/TheoreticalFoundations.tex`,
  `sections/IndividualBufferStockStability.tex`,
  `sections/AggregateInvariantRelationships.tex`,
  `sections/ConsumerPatienceAndLimitingConsumption.tex`, `Appendices/ApndxConcaveCFunc.tex`,
  `Appendices/ApndxMTargetIsStable.tex`, `Appendices/ApndxLiqConstr.tex`,
  `Appendices/ApndxSupportingAnalysis.tex`, `Appendices/ApndxBalancedGrowthcNrmAndCov.tex`
  (its first part), `Tables/Parameters.tex`, `Tables/Calibration.tex`, `Tables/Comparison.tex`,
  `Tables/Required.tex`, `Tables/LiqConstrScenarios.tex`, and the macro definitions in
  `@local/local.sty` and `@resources/`.
- Read in part: `Introduction.tex`.
- For the section on the appendix (2026-11-12): `Appendices/ApndxPositiveMinimumIncome.tex`,
  read in full, on branch `20261111-positive-minimum-income` at `2e875060`, and the sentence at
  the anchor `PDV` in `sections/TheoreticalFoundations.tex` on that branch.
- Not read, because they do not state the model: `Appendices/ApndxConditionDiagrams.tex`, the
  figure files, and the appendices the paper does not include.
- In this repository, for cross-checking: `_ai/audit/conditions-lattice.md` and
  `_ai/audit/notation-and-assumptions.md`. They cite anchors in the web edition
  (`ass-shocks`); this digest cites LaTeX labels (`ass:shocks`). The two differ only in the
  separator.
- Scripts behind the computed values and the derived statements are in `_ai/digests/checks/`.
  The first two need HARK (run here on 0.17.2); the third needs only Python.
  - `baseline_values.py`: the closed forms and the solved target and pseudo-target.
  - `hark_departures_check.py`: HARK's factors at variations on the paper's calibration.
  - `derived_statement_checks.py`: the bound on income in the zero-income event, the closed
    form for κ̄ at a finite horizon, the natural borrowing limit with an income floor, the
    point m_# against the appendix footnote, and the lognormal thresholds.
