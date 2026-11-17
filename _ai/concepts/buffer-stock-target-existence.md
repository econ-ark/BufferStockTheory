# Buffer Stock Target

## Defining equation

Anchor: [`thm-target`](../../BufferStockTheory.md#thm-target)

$$
\Ex_t [{\mNrm}_{t+1}/\mNrm_t] = 1 ~if~ \mNrm_t = \mTrgNrm,
\quad\text{and}\quad
\begin{aligned}
  \forall {\mNrm}_t\in(0,\mTrgNrm),      \,\,& \Ex_t [{\mNrm}_{t+1}] > {\mNrm}_t  \\
  \forall {\mNrm}_t\in(\mTrgNrm,\infty), \,\,& \Ex_t [{\mNrm}_{t+1}] < {\mNrm}_t.
\end{aligned}
$$

*Under weak return impatience, finite value of autarky, and strong growth impatience, a strictly positive buffer-stock target exists and is stable: normalized resources rise in expectation below it and fall above it.*

## Gloss

This theorem is the existence-and-stability result for the individual buffer-stock target $\mTrgNrm$ — the level of (permanent-income-normalized) market resources at which the precautionary saving motive exactly balances impatience, so that $\Ex_t[\mNrm_{t+1}/\mNrm_t]=1$. It asserts not only that such a $\mTrgNrm>0$ exists but that it is globally stabilizing: for $\mNrm_t<\mTrgNrm$ expected next-period resources strictly exceed $\mNrm_t$, and for $\mNrm_t>\mTrgNrm$ they strictly fall short. This is the formal content behind the paper's title.

The theorem ASSUMES three conditions: weak return impatience (WRIC), finite value of autarky (FVAC), and *strong* growth impatience (GIC-Mod). GIC-Mod — the expectation of the ratio $\APFac/(\PermGroFac\permShk)$ being below one — is the load-bearing hypothesis: in the proof it delivers $\lim_{\mNrm_t\to\infty}\Ex_t[\mNrm_{t+1}/\mNrm_t]=\Ex_t[\APFac/\PermGroFacRnd_{t+1}]<1$, which (with continuity from the Dominated Convergence Theorem and the unboundedness of the ratio as $\mNrm_t\to 0$) gives a crossing point of one by the Intermediate Value Theorem, while uniqueness/stability follows from showing $\Ex_t[\mNrm_{t+1}]-\mNrm_t$ is strictly decreasing.

The result IMPLIES the existence of the target object $\mTrgNrm$ and the sign pattern of the drift in `eq-stability`; the implicit equation $(\mTrgNrm-\cFunc(\mTrgNrm))\bar{\RNrmByGRnd}+1=\mTrgNrm$ at `eq-mTargImplicit` then characterizes it, where $\bar{\RNrmByGRnd}=\RNrmByG\,\Ex[\permShk^{-1}]$ is the permanent-shock-adjusted return factor. It is the strictly stronger sibling of the pseudo-target existence theorem (`thm-MSSBalExists`), which shares WRIC and FVAC but needs only the ordinary GIC; when permanent-shock variance is large enough that GIC-Mod fails while GIC still holds, the pseudo-target exists but no individual target does.

## Relations

- **requires** [weak-return-impatience-condition](weak-return-impatience-condition.md) — thm-target assumes WRIC (Assumption WRIC).
- **requires** [finite-value-of-autarky](finite-value-of-autarky.md) — thm-target assumes FVAC (Assumption FVAC).
- **requires** [strong-growth-impatience-condition](strong-growth-impatience-condition.md) — thm-target assumes GIC-Mod; the proof uses $\GPFacMod<1$ at the limit $\mNrm_t\to\infty$ and in the strict-monotonicity step.
- **implies** [buffer-stock-target](buffer-stock-target.md) — Conclusion: a strictly positive target $\mTrgNrm$ exists, with $\Ex_t[\mNrm_{t+1}/\mNrm_t]=1$ there.
- **implies** [`eq-stability`](../../BufferStockTheory.md#eq-stability) — Conclusion: the target is stabilizing — expected normalized resources rise below $\mTrgNrm$ and fall above it.
- **contrasts-with** [pseudo-target](pseudo-target.md) — The pseudo-target existence theorem (thm-MSSBalExists) shares WRIC and FVAC but needs only GIC, not the stronger GIC-Mod.
- **contrasts-with** [pseudo-target-existence](pseudo-target-existence.md) — Sibling existence theorem: pseudo-target-existence (thm-MSSBalExists) needs only the ordinary GIC, so the pseudo-target can exist when this individual target does not.

## Sources

- [BufferStockTheory.md#thm-target](../../BufferStockTheory.md#thm-target)
- [BufferStockTheory.md#eq-mTargImplicit](../../BufferStockTheory.md#eq-mTargImplicit)
- [BufferStockTheory.md#subsubsec-AppxIndividTarget](../../BufferStockTheory.md#subsubsec-AppxIndividTarget)

## bellman-ddsl correspondence

> *Reserved field — the bellman-ddsl perch/stage mapping is **deferred** for every concept in this atlas; the cross-repo bridge has not been authored. This is not a delivered correspondence.*

- perch: `(deferred)`
- stage: `(deferred)`
