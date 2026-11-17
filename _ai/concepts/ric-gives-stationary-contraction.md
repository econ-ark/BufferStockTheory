# Return Impatience Yields a Stationary Contraction (and Why WRIC Alone Does Not)

*Short form: **RIC-stationary remark***

## Defining equation

Anchor: [`remark-ricstationary`](../../BufferStockTheory.md#remark-ricstationary)

$$
\text{RIC} \implies \big(\MPCmin_{T-n}\geq \MPCmin>0\ \forall n\big)\ \text{so}\ \exists\,k:\ \TMap^{\MPCmin, \MPCmax_{T-k}}\ \text{is a \emph{stationary} contraction with}\ \vFunc_{T-n}=\TMap^{\MPCmin, \MPCmax_{T-k}}\vFunc_{T-n+1}\ \forall n>k;\quad \neg\text{RIC}\implies \MPCmin=0\ \text{and}\ \TMap^{0, \MPCmax_{T-k}}\ \text{is not a self-map of}\ \mathcal{C}_{\boundFunc}(\Reals_{++},\Reals)
$$

*If the return impatience condition holds, the minimal MPC is bounded away from zero for all horizons, so for large enough $k$ a single fixed (stationary) MPC-bounded Bellman operator $\TMap^{\MPCmin,\MPCmax_{T-k}}$ generates the entire tail of the finite-horizon value-function sequence; if return impatience fails, the minimal MPC is zero and the would-be stationary operator $\TMap^{0,\MPCmax_{T-k}}$ is not even a well-defined self-map of the weighted-norm function space.*

## Gloss

This remark sits immediately after the existence theorem [nondegenerate-solution-existence](#nondegenerate-solution-existence) (`thm-convgtobellman`) and contrasts the construction used there with what would be available under a stronger impatience assumption. The existence proof deliberately uses only [weak return impatience](#WRIC) (WRIC) together with [finite value of autarky](#FVAC), and as a consequence it must work with a *time-varying* family of MPC-bounded operators $\TMap^{\MPCmin_{T-n},\MPCmax_{T-n}}$ whose lower consumption share $\MPCmin_{T-n}$ can drift toward zero as the horizon recedes. The remark observes that if one instead *assumes* the full [return impatience condition](#RIC) (RIC), the minimal MPC is uniformly bounded below, $\MPCmin_{T-n}\geq\MPCmin>0$ for all $n$, and the analysis simplifies dramatically.

Concretely, RIC *implies* that for $k\in\mathbb{N}$ large enough a single *stationary* operator $\TMap^{\MPCmin,\MPCmax_{T-k}}$ — with fixed lower share $\MPCmin$ and fixed upper share $\MPCmax_{T-k}$ — is a contraction satisfying $\vFunc_{T-n}=\TMap^{\MPCmin,\MPCmax_{T-k}}\vFunc_{T-n+1}$ for every $n>k$. In that case the limiting value function is literally the fixed point of one contraction map and the standard Banach fixed-point picture applies to the tail of the sequence, rather than the Cauchy-sequence-of-eventually-common-modulus argument that the WRIC-only theorem (`thm-cmap`, [contraction-mapping-consumption-bounds](#contraction-mapping-consumption-bounds)) is forced to run.

The second half of the remark is the cautionary converse: *without* RIC the minimal MPC collapses to $\MPCmin=0$, and then the candidate stationary operator $\TMap^{0,\MPCmax_{T-k}}$ fails to be a well-defined map from $\mathcal{C}_{\boundFunc}(\Reals_{++},\Reals)$ into itself, no matter how large $k$ is taken. The reason is the continuity/compactness obstruction catalogued in Section [](#subsubsec-challengesDP): when the lower share is zero the feasibility correspondence reopens to $\mNrm\mapsto(0,\mNrm)$, which is not compact-valued, so $\TMap$ need not send continuous functions to continuous functions. This is exactly why the existence theorem cannot simply invoke a stationary contraction and must instead bound the consumption share strictly inside $(0,\MPCmax_{T-n})$ at each step — the WRIC machinery is the price of *not* assuming RIC. The remark thus delimits the boundary between the paper's general (WRIC) existence result and the cleaner stationary-operator route that the stronger RIC would buy.

## Relations

- **requires** [return-impatience-condition](return-impatience-condition.md) — RIC is precisely the hypothesis that forces $\MPCmin_{T-n}\geq\MPCmin>0$ for all $n$, which is what makes the single stationary operator $\TMap^{\MPCmin,\MPCmax_{T-k}}$ a well-defined contraction; the remark is a statement about what RIC adds.
- **contrasts-with** [weak-return-impatience-condition](weak-return-impatience-condition.md) — Under only WRIC the lower share $\MPCmin_{T-n}$ can drift to zero, forcing the time-varying operators of thm-convgtobellman; RIC replaces this with one fixed-share stationary contraction.
- **contrasts-with** [contraction-mapping-consumption-bounds](contraction-mapping-consumption-bounds.md) — thm-cmap proves the WRIC operators are eventually contractions with a common modulus (a Cauchy-sequence argument); this remark notes that RIC upgrades that to a genuinely stationary contraction $\TMap^{\MPCmin,\MPCmax_{T-k}}$ acting on the whole tail.
- **implied-by** [nondegenerate-solution-existence](nondegenerate-solution-existence.md) — The remark is appended to thm-convgtobellman and qualifies its proof strategy: it explains why the theorem uses WRIC-style time-varying bounded operators rather than the stationary contraction that RIC would permit.
- **requires** [`subsubsec-challengesDP`](../../BufferStockTheory.md#subsubsec-challengesDP) — The claim that $\TMap^{0,\MPCmax_{T-k}}$ is not a self-map of $\mathcal{C}_{\boundFunc}(\Reals_{++},\Reals)$ rests on the non-compact-valued feasibility correspondence $\mNrm\mapsto(0,\mNrm)$ documented there, which breaks continuity of $\TMap$.

## Sources

- [BufferStockTheory.md#remark-ricstationary](../../BufferStockTheory.md#remark-ricstationary)
- [BufferStockTheory.md#thm-convgtobellman](../../BufferStockTheory.md#thm-convgtobellman)
- [BufferStockTheory.md#subsubsec-challengesDP](../../BufferStockTheory.md#subsubsec-challengesDP)

## bellman-ddsl correspondence

> *Reserved field — the bellman-ddsl perch/stage mapping is **deferred** for every concept in this atlas; the cross-repo bridge has not been authored. This is not a delivered correspondence.*

- perch: `(deferred)`
- stage: `(deferred)`
