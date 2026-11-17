# Zero-Income-Probability Limit as a Special Case of Ma–Stachurski–Toda

*Short form: **SDF/MST correspondence***

## Defining equation

Anchor: [`remark-stochdiscMST`](../../BufferStockTheory.md#remark-stochdiscMST)

$$
\pZero=0 \implies \text{[}\href{eq-veqnNrmRecBellman}{\text{normalized Bellman eq.}}\text{]}\ \text{is a special case of MST (2020), with}\ \RNrmByGRnd_{t+1}=\Rfree/\Rnd{\PermGroFac}_{t+1}\ \text{the stochastic return and}\ \DiscFac\,\Rnd{\PermGroFac}_{t+1}^{1-\CRRA}\ \text{the stochastic discount factor.}
$$

*When the probability of a zero-income event is set to zero, the permanent-income-normalized Bellman equation reduces to an instance of the Ma–Stachurski–Toda (2020) income-fluctuation framework, under which the return-over-growth ratio $\RNrmByGRnd_{t+1}=\Rfree/\Rnd{\PermGroFac}_{t+1}$ plays the role of the stochastic gross return on capital and $\DiscFac\,\Rnd{\PermGroFac}_{t+1}^{1-\CRRA}$ plays the role of the stochastic discount factor.*

## Gloss

This remark records a structural correspondence between the paper's permanent-income-normalized problem and the income-fluctuation framework of [(Ma, Stachurski, and Toda, 2020)](#cite-mstIncFluct). It *assumes* the degenerate case $\pZero=0$ — that is, the small probability of a zero-income event (the Zeldes (1989) device used elsewhere in the model) is switched off. Under that assumption the normalized Bellman equation [](#eq-veqnNrmRecBellman) becomes a *special case* of the MST (2020) setup: the return-over-growth ratio $\RNrmByGRnd_{t+1}=\Rfree/\Rnd{\PermGroFac}_{t+1}$ takes the part of their stochastic gross return on capital, and the object $\DiscFac\,\Rnd{\PermGroFac}_{t+1}^{1-\CRRA}$ takes the part of their stochastic discount factor. The remark is a mapping of notation and roles, not a new theorem; it tells the reader where this paper's normalized problem sits inside an existing, more general apparatus.

The economic content of the correspondence is that permanent-income growth, after normalization, is absorbed simultaneously into both the effective return and the effective discount factor. Dividing through by permanent income converts the raw discount factor $\DiscFac$ into the *normalized stochastic discount factor* $\DiscFac\,\Rnd{\PermGroFac}_{t+1}^{1-\CRRA}$ and the raw return $\Rfree$ into $\Rfree/\Rnd{\PermGroFac}_{t+1}$, so growth shocks act as a stochastic wedge on both. This is why the paper's later patience and impatience conditions are expressed in terms of the *growth-adjusted* objects $\DiscFac\,\PermGroFac^{1-\CRRA}$ and $\Rfree/\PermGroFac$ rather than $\DiscFac$ and $\Rfree$ alone; the very next sentence after this remark flags that, despite the formal embedding, "important economic consequences relating consumer patience to buffer stock saving" survive precisely because $\RNrmByGRnd_{t+1}$ is tightly tied to the normalized stochastic discount factor.

The remark also marks the boundary of the embedding rather than asserting equivalence. The reduction to MST (2020) holds *only* at $\pZero=0$; with $\pZero>0$ the zero-income event reinstates the natural liquidity constraint, whose non-compact feasibility correspondence $\mNrm\mapsto(0,\mNrm)$ is exactly the obstruction discussed in [feasible-correspondence-not-compact](#feasible-correspondence-not-compact) and the surrounding dynamic-programming discussion [](#subsubsec-challengesDP). MST (2020) (like [(Ma, Stachurski, and Toda, 2022b)](#cite-Ma2022)) handle that boundary by imposing an *artificial* liquidity constraint, whereas this paper retains the natural constraint and instead builds a weighted-norm contraction argument. Accordingly the remark is invoked elsewhere to position the paper's [finite-value-of-autarky](#finite-value-of-autarky) discount condition as a special case of MST (2020) Assumption 2.1, "albeit in a context with artificial liquidity constraints" — i.e. the MST generalization buys breadth at the cost of an artificial constraint that this paper does not require.

## Relations

- **special-case-of** [`eq-veqnNrmRecBellman`](../../BufferStockTheory.md#eq-veqnNrmRecBellman) — At $\pZero=0$ the normalized Bellman equation eq-veqnNrmRecBellman is a special case of the MST (2020) income-fluctuation framework (cite-mstIncFluct), with $\RNrmByGRnd_{t+1}=\Rfree/\Rnd{\PermGroFac}_{t+1}$ as the stochastic return and $\DiscFac\,\Rnd{\PermGroFac}_{t+1}^{1-\CRRA}$ as the stochastic discount factor.
- **contrasts-with** [feasible-correspondence-not-compact](feasible-correspondence-not-compact.md) — The embedding into MST (2020) holds only at $\pZero=0$; for $\pZero>0$ the natural liquidity constraint makes the feasibility correspondence non-compact-valued (remark-notCompact), which MST handle via an artificial constraint and this paper handles via a weighted-norm contraction.
- **requires** [`subsubsec-challengesDP`](../../BufferStockTheory.md#subsubsec-challengesDP) — Sits within the dynamic-programming-challenges discussion (subsubsec-challengesDP) contrasting the natural-constraint approach here with the artificial-constraint approach of MST (2020) / Ma–Stachurski–Toda (2022b).
- **generalises** [finite-value-of-autarky](finite-value-of-autarky.md) — Reciprocal of finite-value-of-autarky special-case-of: MST (2020) Assumption 2.1 generalises the FVAC discount condition (ass-FVAC) — at the cost of an artificial liquidity constraint, whereas FVAC here uses the natural constraint.

## Sources

- [BufferStockTheory.md#remark-stochdiscMST](../../BufferStockTheory.md#remark-stochdiscMST)
- [BufferStockTheory.md#subsubsec-challengesDP](../../BufferStockTheory.md#subsubsec-challengesDP)
- [BufferStockTheory.md#eq-veqnNrmRecBellman](../../BufferStockTheory.md#eq-veqnNrmRecBellman)

## bellman-ddsl correspondence

> *Reserved field — the bellman-ddsl perch/stage mapping is **deferred** for every concept in this atlas; the cross-repo bridge has not been authored. This is not a delivered correspondence.*

- perch: `(deferred)`
- stage: `(deferred)`
