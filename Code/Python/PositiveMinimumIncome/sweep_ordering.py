"""Sweep minimum income: the order of target and pseudo-target, and the bounds used in the existence proof."""
import numpy as np, positive_income_checks as P
rho = P.rho
print(" mu     h_min    c(1)     target   pseudo   a(target) a(pseudo)  signs agree")
for mu in (0.0, 0.02, 0.05, 0.06, 0.065, 0.07, 0.08, 0.1, 0.2, 0.3, 0.5):
    M = P.Model(0.005, mu, 7); sol = M.solve(); c = P.cf(sol)
    co = lambda m: c(m + M.h_inf)
    dT = lambda m: (m - co(m)) * P.Rn * M.Einv + 1 - m
    dP = lambda m: (m - co(m)) * P.Rn + 1 - m
    lo = -M.h_inf + 1e-9
    (mT,), _ = P.roots_decreasing(dT, lo, 60); (mP,), _ = P.roots_decreasing(dP, lo, 60)
    s = [np.sign(round(v, 7)) for v in (1 - co(1.0), mP - 1, mT - 1, mP - co(mP), mT - co(mT), mT - mP)]
    print(f"{mu:5.3f} {M.h_inf:8.4f} {float(co(1.0)):8.5f} {mT:8.5f} {mP:8.5f} {mT-co(mT):9.5f} {mP-co(mP):9.5f}  {len(set(s))==1} {s[0]:+.0f}")

print("\nexistence-proof constants at mu=0.3 (baseline, 7 points)")
M = P.Model(0.005, 0.3, 7)
xt = M.xi_tilde(M.h_inf); xt_min = xt[xt > 0].min()
EG = P.beta * np.dot(M.w, (P.G * M.psi) ** (1 - rho))            # beta E[Gtilde^(1-rho)]
s = M.p_worst ** (1 / rho) * P.RPF
kb = [1.0]
for _ in range(60): kb.append(1 / (1 + s / kb[-1]))
k = next(j for j, v in enumerate(kb) if j > 0 and M.p_worst * P.beta * (P.R * (1 - v)) ** (1 - rho) < 1)
edge = M.p_worst * P.beta * (P.R * (1 - kb[k])) ** (1 - rho)
alpha = 0.5 * (max(edge, EG) + 1)
zeta = EG * xt_min ** (1 - rho) / (alpha - EG)
print(f"k={k}  kbar_(T-k)={kb[k]:.6f}  edge term={edge:.6f}  beta E[G~^(1-rho)]={EG:.6f}  alpha={alpha:.6f}  zeta={zeta:.4f}  xi~min={xt_min:.5f}")
F = lambda x: zeta + x ** (1 - rho)
# the key inequality, on a grid of m and for a = (1-kbar)m, for several horizons' incomes
worst = 0.0
for hn in (0.0, M.h(1), M.h(5), M.h_inf):
    x = M.xi_tilde(hn)
    for m in np.geomspace(1e-8, 1e4, 400):
        a = (1 - kb[k]) * m
        lhs = P.beta * np.sum(M.w * (P.G * M.psi) ** (1 - rho) * F(a * P.Rn / M.psi + x))
        worst = max(worst, lhs / (alpha * F(m)))
print(f"max over m and horizons of  beta E[G~^(1-rho) F(m')] / (alpha F(m)) = {worst:.6f}  (must be <= 1)")
# uniform bounds along the finite-horizon sequence
B = kb[k] ** (1 - rho) / ((rho - 1) * (1 - alpha))
clow = lambda m: kb[k] * ((1 - alpha) / F(m)) ** (1 / (rho - 1))
hist = M.solve(horizon=300)
g = np.geomspace(1e-6, 300, 500)
ok = all(np.all(np.interp(g, *hist[n]) >= clow(g) - 1e-12) for n in range(0, 301))
print(f"B={B:.3f}; consumption >= the uniform lower bound at every horizon 0..300 on the grid: {ok}; "
      f"min over horizons of c_n(xi~min)={min(float(np.interp(xt_min, *hist[n])) for n in range(301)):.5f} vs bound {float(clow(xt_min)):.5f}")
