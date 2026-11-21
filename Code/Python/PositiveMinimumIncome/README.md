# Checks for the appendix "Positive Minimum Income"

These scripts check, numerically, the statements of `Appendices/ApndxPositiveMinimumIncome.tex`
and produce the numbers in its example table. Each `*_out.txt` is the output of the script of the
same name, run on 2026-11-11 with econ-ark (HARK) 0.17.2, numpy and scipy.

**Before you start:** install HARK using Econ-ARK's
[installation guide](https://docs.econ-ark.org/docs/guides/installation.html).

Run each script from this folder: `python positive_income_checks.py`, and so on.

| script | what it does |
|---|---|
| `positive_income_checks.py` | Solves the model two ways and compares them: an endogenous-gridpoints solver written here, in resources measured from the natural borrowing limit with the appendix's transformed income; and HARK's `IndShockConsumerType` in the original variables. Then checks the natural limit, the limiting MPCs at each horizon, the bounds on consumption, uniqueness of the target and pseudo-target and their order, and the limit as the unemployment probability goes to zero. The other scripts import its solver. |
| `infimum_law_example.py` | The example table: the permanent shock has a point mass at the infimum of a mean-one truncated lognormal and is otherwise a scaled draw from it, as the appendix describes after its assumption. |
| `sweep_ordering.py` | Sweeps income while unemployed and checks that the six quantities of the ordering lemma share a sign; checks the contraction's key inequality and the uniform lower bound on consumption from the existence proof. |
| `simulate_invariant.py` | Simulates a population from two starting points, under the objective measure and under the permanent-income-neutral one, to check the invariant distributions. |
| `no_worst_event_checks.py` | Checks for the revision (2026-11-12, not yet in the appendix): a permanent shock with no point mass at its lowest value, the restrained consumer and the limit as the unemployment probability goes to zero (also with zero income while unemployed, the text's claim), and the constraint c ≤ m kept with positive income while unemployed (against HARK with `BoroCnstArt=0`); the key inequality and bounds of the existence proof that needs only finite value of autarky; that finite value of autarky and Gψ̲ < R imply weak return impatience at the worst event's probability; and consumption with infinite minimum human wealth. |
| `explore_cases.py` | Return impatience failing with finite minimum human wealth (a limiting solution exists), and three cases with G times the lowest permanent shock at least R (consumption grows without bound as the horizon recedes). |

What the checks do not establish is listed in the appendix's section "When the Hypotheses Fail" and
in its paragraph on the liquidity constrained solution as a limit.

Two things to know when reading the outputs:

- `positive_income_checks.py`, `sweep_ordering.py`, `simulate_invariant.py` and `explore_cases.py`
  use HARK's equiprobable discrete laws, whose lowest permanent shock is the lowest point of the
  discretization (probability one over the number of points). They test the theory, which holds for
  any law that satisfies the appendix's assumption. The example table does not use those laws: it
  uses the law in `infimum_law_example.py`, whose lowest value does not depend on the number of
  points.
- Differences of order 1e-4 between the two solvers are interpolation error.
