# Growth Patience Factor (GPF)

## Defining equation

Anchor: [`eq-GPFacRaw`](../../BufferStockTheory.md#eq-GPFacRaw)

$$
\GPFacRaw := \APFac/\PermGroFac
$$

*Ratio of the absolute patience factor to the (unconditional) permanent-income growth factor.*

## Gloss

The growth patience factor $\GPFacRaw := \APFac/\PermGroFac$ is the patience-factor analogue of the consumption-growth-vs-income-growth comparison: it asks how the consumer's preferred consumption-growth rate (encoded in $\APFac$) compares to the expected permanent-income growth rate $\PermGroFac$. When the ratio is below 1, consumption is growing more slowly than permanent income, so the wealth-to-permanent-income ratio drifts down — exactly the condition the GIC turns into a formal assumption.

$\GPFac$ and $\GPFacRaw$ are macro aliases for the same quantity (both bodies are `\APFac/\PermGroFac`); the "Raw" suffix emphasises that this is the *unmodified* factor — the non-stochastic version. Its modified sibling $\GPFacMod := \Ex[\APFac/(\PermGroFac \permShk)]$ takes the expectation over the permanent shock and is what GIC-Mod tests against 1.

Operationally, GPF is one of *four* patience factors the paper tests against 1: $\APFac$ itself (AIC), $\GPFacRaw = \APFac/\PermGroFac$ (GIC), $\GPFacMod = \APFac/\PermGroFacAdj$ (GIC-Mod), and $\RPFac = \APFac/\Rfree$ (RIC). All four share the common numerator $\APFac$ and differ only in their denominators — the four rates against which "is the consumer patient enough?" gets asked: $1$, $\PermGroFac$, $\PermGroFacAdj$, $\Rfree$.

## Relations

- **requires** [absolute-patience-factor](absolute-patience-factor.md) — $\GPFac = \APFac/\PermGroFac$ is built from $\APFac$.
- **assumed-by** [growth-impatience-condition](growth-impatience-condition.md) — GIC is exactly the inequality $\GPFacRaw < 1$.
- **contrasts-with** [modified-growth-patience-factor](modified-growth-patience-factor.md) — GPF uses denominator $\PermGroFac$; GPF-Mod uses the harmonic-mean uncertainty-adjusted version $\PermGroFacAdj := \PermGroFac/\Ex[1/\permShk]$. Since $\PermGroFacAdj \leq \PermGroFac$, GPF-Mod $\geq$ GPF.
- **contrasts-with** [return-patience-factor](return-patience-factor.md) — GPF and RPF share the numerator $\APFac$ and differ in denominator: GPF uses $\PermGroFac$, RPF uses $\Rfree$.

## Sources

- [BufferStockTheory.md#GPFacRawDefn](../../BufferStockTheory.md#GPFacRawDefn)
- [BufferStockTheory.md#eq-GPFacRaw](../../BufferStockTheory.md#eq-GPFacRaw)

## bellman-ddsl correspondence

> *Reserved field — the bellman-ddsl perch/stage mapping is **deferred** for every concept in this atlas; the cross-repo bridge has not been authored. This is not a delivered correspondence.*

- perch: `(deferred)`
- stage: `(deferred)`
