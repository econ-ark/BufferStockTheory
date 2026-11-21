"""Simulation check of the invariant-distribution proposition with positive minimum income (mu = 0.3, baseline, 7 points)."""
import numpy as np, positive_income_checks as P
rng = np.random.default_rng(20261111)
M = P.Model(0.005, 0.3, 7); sol = M.solve(); c = P.cf(sol)
xt = M.xi_tilde(M.h_inf)
print(f"log GPF={np.log(P.GPF):.5f}  E[log psi]={np.dot(M.w, np.log(M.psi)):.5f}  E[psi log psi]={np.dot(M.w, M.psi*np.log(M.psi)):.5f}  GPF={P.GPF:.5f}")
def run(pmf, m0, N=200_000, T=1500, label=""):
    m = np.full(N, m0); cdf = np.cumsum(pmf); out = []
    for t in range(1, T + 1):
        k = np.searchsorted(cdf, rng.random(N)); k = np.minimum(k, len(pmf) - 1)
        m = (m - c(m)) * P.Rn / M.psi[k] + xt[k]
        if t in (10, 100, 500, 1000, 1500):
            q = np.quantile(m, [0.01, 0.1, 0.5, 0.9, 0.99])
            out.append((t, m.mean(), c(m).mean(), q))
    for t, mean, cm, q in out:
        print(f"  {label} t={t:5d}: mean m~={mean:8.4f} mean c={cm:7.4f} quantiles(1,10,50,90,99%)={np.round(q,3)}")
    return m
print("objective measure (distribution of resources above the limit):")
a = run(M.w, 0.01, label="start 0.01")
b = run(M.w, 50.0, label="start 50  ")
print("permanent-income-neutral measure (shock probabilities weighted by psi):")
wt = M.w * M.psi; wt = wt / wt.sum()
a = run(wt, 0.01, label="start 0.01")
b = run(wt, 50.0, label="start 50  ")
print(f"bound on the weighted mean from the proof: xi~max/(1-GPF) = {xt.max()/(1-P.GPF):.3f}")
print(f"h_min={M.h_inf:.4f}: weighted mean of m itself = weighted mean of m~ minus h_min")
