# The problem with uncertainty, under the natural borrowing constraint

The consumer of *Theoretical Foundations of Buffer Stock Saving* (the subsection "Model with
Uncertainty"):
- has CRRA utility, infinitely lived (survival probability ℒ = 1);
- faces bounded permanent and transitory shocks, plus a zero-income event with probability ℘;
- saves in a riskless asset at the return R.

The natural borrowing constraint is a > −h_min, minus minimum human wealth (the appendix "Positive
Minimum Income"). The stage takes h_min in from the next period as a field, h_min[>], and sends its
own back. Because of the zero-income event, minimum human wealth is zero in every period, so the
natural borrowing constraint is a > 0, and the consumer never reaches it.

Open it in [Bellman Workbench](https://bellman.io/workbench/) with
`bellman-workbench bellman/natural-borrowing-constraint` (the page
[Install Bellman Workbench](https://bellman.io/overview/00-install/) installs it with Bellman). No
code of this folder writes results.

## Files

- **`declaration/stages/natural/natural.bl`:** the stage file. Every line but its comments is the
  stage file of the family `bst-natural/1` of `llorracc/wg1-buffer-stock` at `8976a31`.
- **`declaration/stages/natural/methods.bl`:** the paper's default methods, with no toolkit's
  handler:
  - the endogenous grid method;
  - linear interpolation of the consumption function;
  - a quadrature rule for the expectation, stated in a comment as the paper's seven equiprobable
    points per law.
- **`declaration/calibration/baseline.yml`:** the table "Microeconomic Model Calibration", with the
  shocks' laws truncated at three standard deviations of their logs and a standard deviation of 0.1
  kept after truncation.
- **`declaration/settings/natural.yml`:** seven nodes per shock, and 960-point grids from 0.001 to 20.

## A check against the paper

The appendix "Positive Minimum Income" solves this model in its subsection "An Example", with these
laws and seven equiprobable points per law. Its table "Positive Minimum Income at the Baseline
Calibration", in the column for an unemployment income of zero, gives consumption at resources of 1
as 0.853.

## Bellman's own buffer-stock example

Bellman's documentation has a buffer-stock model of its own:
[the example](https://bellman.io/examples/buffer-stock/buffer_stock/), from
[`applications/buffer-stock`](https://github.com/econ-ark/bellman/tree/main/applications/buffer-stock).
It is Bellman's example, not the paper's statement of this model: its stage file draws the shocks
from lognormals that are not truncated. Its settings file gives the node counts and grids that
`declaration/settings/natural.yml` uses.
