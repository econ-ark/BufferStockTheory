"""Side cases: return impatience fails; and G psi_min >= R (no finite natural limit)."""
import numpy as np, positive_income_checks as P

def setpar(R, G, beta, rho=2.0):
    P.R, P.G, P.beta, P.rho = R, G, beta, rho
    P.APF = (R * beta) ** (1 / rho); P.RPF = P.APF / R; P.GPF = P.APF / G; P.Rn = R / G

def facts(M):
    Epsi1mr = float(np.dot(M.w, M.psi ** (1 - P.rho)))
    return (f"APF={P.APF:.4f} RPF={P.RPF:.4f} (RIC {'holds' if P.RPF<1 else 'FAILS'}) GPF={P.GPF:.4f} GPF*E[1/psi]={P.GPF*M.Einv:.4f} "
            f"G/R={P.G/P.R:.4f} (FHWC {'holds' if P.G<P.R else 'FAILS'}) VAF={P.beta*P.G**(1-P.rho)*Epsi1mr:.4f} "
            f"WRPF(P(worst))={M.p_worst**(1/P.rho)*P.RPF:.4f} x=G psi_min/R={M.x:.4f}")

print("=== A. return impatience fails, G psi_min < R ===")
setpar(0.95, 1.03, 0.96)
M = P.Model(0.005, 0.05, 7); print(facts(M), f"h_min={M.h_inf:.4f}")
sol = M.solve(tol=1e-11, maxit=60000); c = P.cf(sol)
print(f"iterations={M.iters}; c at resources-above-limit 0.5, 1, 2, 5, 20: {np.round(c(np.array([0.5,1,2,5,20.])),5)}")
print(f"max MPC at bottom={c(1e-7)/1e-7:.6f} vs {1-M.p_worst**(1/P.rho)*P.RPF:.6f}; c/m at 300={c(300.)/300:.5f} (limit 0)")
co = lambda m: c(m + M.h_inf)
dT = lambda m: (m - co(m)) * P.Rn * M.Einv + 1 - m
dP = lambda m: (m - co(m)) * P.Rn + 1 - m
lo = -M.h_inf + 1e-9
print("target roots, decreasing:", P.roots_decreasing(dT, lo, 200), " pseudo-target:", P.roots_decreasing(dP, lo, 200))
try:
    a = P.hark_agent(0.005, 0.05, 7); hs = a.solution[0]
    mm = np.linspace(0.05, 20, 300)
    print(f"HARK: mNrmMin={hs.mNrmMin:.5f}; max|c-c_HARK|={np.max(np.abs(c(mm)-hs.cFunc(mm-M.h_inf))):.2e}")
except Exception as e:
    print("HARK failed:", repr(e)[:200])

for label, (R, G, beta) in {"B. G psi_min >= R, return impatience holds": (1.00, 1.20, 0.96),
                            "C. G psi_min >= R, return impatience fails, APF >= G psi_min": (0.90, 1.08, 0.99),
                            "D. G psi_min >= R, return impatience fails, APF < G psi_min": (0.90, 1.14, 0.99)}.items():
    print(f"\n=== {label} ===")
    setpar(R, G, beta)
    M = P.Model(0.005, 0.05, 7); print(facts(M), f"APF/(G psi_min)={P.APF/(P.G*M.psi_min):.4f}")
    # finite horizons only: the natural limit h(n) grows without bound
    cur = (np.array([0.0, 1.0]), np.array([0.0, 1.0])); out = []
    hn = lambda j: M.xi_min * sum(M.x ** i for i in range(1, j + 1))
    for j in range(1, 401):
        cur = M.step(cur, hn(j - 1))
        if j in (1, 5, 20, 50, 100, 200, 400):
            h = hn(j); m0 = 1.0
            out.append((j, h, float(np.interp(m0 + h, *cur)) if m0 + h < cur[0][-1] else float('nan')))
    for j, h, cv in out:
        print(f"   n={j:3d}: natural limit -{h:12.4f}   c_n(m=1) = {cv:.5f}")
