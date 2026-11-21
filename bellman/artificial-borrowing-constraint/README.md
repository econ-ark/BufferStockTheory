# The problem with uncertainty, under an artificial borrowing constraint

The consumer of *Theoretical Foundations of Buffer Stock Saving* under an artificial borrowing
constraint, a ≥ a_Art. The calibration `restrained_consumer` is the paper's restrained consumer
(the subsubsection and the appendix "The Liquidity Constrained Solution as a Limit"):
- no unemployment event;
- c ≤ m, that is a_Art = 0.

The problem with uncertainty converges to that consumer as the probability of zero income falls to
zero. The consumer ends a period at a_Art below a kink in resources, so the Euler equation carries a
complementarity clause.

Open it in [Bellman Workbench](https://bellman.io/workbench/) with
`bellman-workbench bellman/artificial-borrowing-constraint` (the page
[Install Bellman Workbench](https://bellman.io/overview/00-install/) installs it with Bellman). No
code of this folder writes results.

## Files

- **`declaration/stages/artificial/artificial.bl`:** the stage file. Every line but its comments is
  the stage file of the family `bst-artificial/1` of `llorracc/wg1-buffer-stock` at `3901bc69`.
  - The family is wider than the paper's model: any limit a_Art ≤ 0, and an unemployment event with
    an income ξ_u ≥ 0.
  - It requires a_Art to lie above the natural limit, −h_min, in words only; no line of this folder
    enforces that, and the restrained consumer meets it.
- **`declaration/stages/artificial/methods.bl`:** the paper's default methods, with no toolkit's
  handler:
  - the endogenous grid method, with the complementarity of the constraint;
  - a savings grid that starts at a_Art;
  - linear interpolation of the consumption function;
  - a quadrature rule for the expectation, stated in a comment as the paper's seven equiprobable
    points per law.
- **`declaration/calibration/restrained_consumer.yml`:** the table "Microeconomic Model
  Calibration", with no unemployment event and a_Art = 0, and the shocks' laws as in the problem with
  uncertainty.
- **`declaration/settings/artificial.yml`:** seven nodes per shock, and 960-point grids from 0 (the
  restrained consumer's a_Art) to 20. A grid's bounds are settings and may not name the parameter
  a_Art, so a calibration with another a_Art needs its own settings.

## Not described here

The appendix "Positive Minimum Income" has two more variants:
- a restrained consumer with a positive unemployment income, bounded by minus minimum human wealth;
- a "No borrowing" variant, whose permanent shock has a point mass at its lowest value.

Neither is a calibration of this stage (`bellman/README.md`).
