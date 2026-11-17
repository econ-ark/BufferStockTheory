"""Arithmetic checks for statements the digest marks 'derived'."""
import math
# (a) PF constrained, GIC fails, RIC holds: where the unconstrained rule crosses c=m, against the appendix footnote's c_# = G/thorn
R, G, beta, rho = 1.03, 1.00, 1.00, 2.0
th = (R * beta) ** (1 / rho); thR = th / R; k = 1 - thR; h = 1 / (1 - G / R)
m_hash = (h - 1) * k / (1 - k); c_foot = G / th; cbar = lambda m: (m - 1 + h) * k
print(f"(a) thorn={th:.6f} thorn_R={thR:.6f} kappa={k:.6f} h={h:.4f}  m_#={m_hash:.5f} cbar(m_#)={cbar(m_hash):.5f}  footnote c_#={c_foot:.5f} cbar(c_#)={cbar(c_foot):.5f}")
# (b) disaster income mu below the worst employed draw after the mean-preserving rescale
p, th_min = 0.05, 0.85
bound = th_min / (1 - p * (1 - th_min))
for mu in (bound - 1e-6, bound + 1e-6):
    worst_emp = th_min * (1 - p * mu) / (1 - p)
    print(f"(b) mu={mu:.6f} worst employed={worst_emp:.6f} mu<worst? {mu < worst_emp}   bound={bound:.6f}")
# (c) closed form for the finite-horizon maximal MPC against the recursion
R, beta, rho, p = 1.04, 0.96, 2.0, 0.005
s = p ** (1 / rho) * (R * beta) ** (1 / rho) / R; kap = 1.0
for n in range(1, 6):
    kap = 1 / (1 + s / kap); print(f"(c) n={n} recursion={kap:.8f} closed={(1 - s) / (1 - s ** (n + 1)):.8f}")
# (d) natural borrowing limit with an income floor: recursion against the closed form
G, R, psi_min, xi_min = 1.03, 1.04, 0.85, 0.3
x = G * psi_min / R; a = 0.0
for _ in range(2000): a = (a - xi_min) * x
print(f"(d) recursion limit={a:.6f} closed={-xi_min * x / (1 - x):.6f}; check a*(1/x-1)={a * (1 / x - 1):.6f} (= -xi_min)")
# (e) lognormal thresholds on thorn_G: GICMod, Szeidl, GIC, Harmenberg
sig = 0.1
print(f"(e) exp(-s^2)={math.exp(-sig**2):.6f} exp(-s^2/2)={math.exp(-sig**2/2):.6f} 1 exp(+s^2/2)={math.exp(sig**2/2):.6f}")
