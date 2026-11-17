"""Checks for the appendix's section on problems in which the worst event has probability zero.

Three problems, each written in resources x measured from its borrowing limit, with income Y > 0:
  (a) no point mass: the permanent shock has a continuous law down to its infimum; natural limit -h;
  (b) restrained:    no unemployment event; may not borrow more than the h that xi_u would support;
  (c) artificial:    unemployment pays xi_u > 0; the constraint c <= m is kept in every period.
Checks: the maximal MPC is one; where the limit binds; a limiting solution exists under finite value of
autarky alone; the bound c <= cbar and the key inequality of the existence proof; unique target and
pseudo-target and the ordering lemma; the limit as the unemployment probability goes to zero, at finite
horizons and in the limit, including xi_u = 0 (the claim of the text); and that weak return impatience at
the probability of the worst event follows from finite value of autarky and finite minimum human wealth.
"""
import numpy as np
from scipy.stats import norm, beta as beta_dist
from scipy.integrate import quad
import positive_income_checks as P
from infimum_law_example import trunc_lognormal

AGRID = np.concatenate([[0.0], np.geomspace(1e-12, 400.0, 1400)])


class Problem(P.Model):
    """kind: 'natural' (unemployment event, natural limit), 'restrained', or 'artificial'.
    prb: probability of the point mass at the infimum of the permanent shock (0 = no point mass)."""

    def __init__(self, kind, p, mu, N=7, prb=0.0, sd=0.1, NT=7):
        self.kind, self.p, self.mu, self.N, self.prb = kind, p, mu, N, prb
        inf, sup, base = trunc_lognormal(sd, N=N)
        _, _, theta = trunc_lognormal(sd, N=NT)
        if prb > 0:
            scale = (1 - prb * inf) / (1 - prb)
            psi1 = np.concatenate(([inf], scale * base)); w1 = np.concatenate(([prb], (1 - prb) * np.ones(N) / N))
        else:
            psi1 = base; w1 = np.ones(N) / N
        if kind == "restrained":
            xi1 = theta.copy(); w2 = np.ones(NT) / NT
        else:
            xi1 = np.concatenate(([mu], theta * (1 - p * mu) / (1 - p))); w2 = np.concatenate(([p], (1 - p) * np.ones(NT) / NT))
        self.psi = np.repeat(psi1, len(xi1)); self.xi = np.tile(xi1, len(psi1)); self.w = np.outer(w1, w2).ravel()
        self.inf, self.psi_min, self.xi_min = inf, inf, mu
        self.x = P.G * inf / P.R
        if kind == "artificial" or mu == 0:
            self.h_inf = 0.0
        else:
            self.h_inf = mu * self.x / (1 - self.x) if self.x < 1 else np.inf
        if kind == "natural":
            self.worst = np.isclose(self.xi, mu) & (np.isclose(self.psi, inf) | (mu == 0))
        else:
            self.worst = np.zeros(self.psi.shape, bool)
        self.p_worst = self.w[self.worst].sum()
        self.Einv = float(np.dot(self.w, 1 / self.psi))
        self.agrid = AGRID

    def h(self, j):
        if self.kind == "artificial" or self.mu == 0:
            return 0.0
        return self.mu * sum(self.x ** i for i in range(1, j + 1))

    def xi_tilde(self, hnext):
        if self.kind == "artificial":
            return self.xi.copy()
        t = (self.xi - self.mu) + (self.mu + hnext) * (1 - self.inf / self.psi)
        t[self.worst] = 0.0
        return t

    def solve(self, horizon=None, tol=1e-12, maxit=20000):
        return P.Model.solve(self, horizon=horizon, tol=tol, maxit=maxit, constrained=True)


def targets(M, sol):
    c = P.cf(sol)
    co = lambda m: c(m + M.h_inf)
    dT = lambda m: (m - co(m)) * P.Rn * M.Einv + 1 - m
    dP = lambda m: (m - co(m)) * P.Rn + 1 - m
    lo = -M.h_inf + 1e-10
    rT, decT = P.roots_decreasing(dT, lo, 60); rP, decP = P.roots_decreasing(dP, lo, 60)
    mT, mP = rT[0], rP[0]
    return dict(c1=float(co(1.0)), mT=mT, mP=mP, aT=mT - float(co(mT)), aP=mP - float(co(mP)),
                one=(len(rT) == 1 and len(rP) == 1), dec=bool(decT and decP), kink=float(sol[0][1]) if sol[1][1] == sol[0][1] else 0.0)


def line(tag, M, sol):
    r = targets(M, sol); c = P.cf(sol)
    signs = np.sign(np.round([1 - r["c1"], r["mP"] - 1, r["mT"] - 1, r["aP"], r["aT"], r["mT"] - r["mP"]], 9))
    print(f"{tag}: limit h={M.h_inf:.4f}  binds below x={r['kink']:.3e}  c(x)/x at x=1e-9: {c(1e-9)/1e-9:.6f}  c(1)={r['c1']:.4f}  "
          f"target={r['mT']:.4f}  pseudo-target={r['mP']:.4f}  a(target)={r['aT']:.4f}  one root each, decreasing: {r['one'] and r['dec']}  "
          f"six signs equal: {bool(np.all(signs == signs[0]))}")
    return r


def section_a():
    print("=== (a) No point mass: xi_u = 0.3, unemployment probability 0.005; permanent shock = N equiprobable points of the truncated lognormal ===")
    print("    (with N points the lowest point is above the infimum, so the limit binds below some x; that x goes to 0 as N grows)")
    out = {}
    for N in (7, 15, 50, 200, 800):
        M = Problem("natural", 0.005, 0.3, N=N); sol = M.solve(); out[N] = line(f"  no point mass, N={N:3d}", M, sol)
    for N in (7, 15, 50, 200):
        M = Problem("natural", 0.005, 0.3, N=N, prb=norm.cdf(-3.0)); sol = P.Model.solve(M)  # interior: worst event has positive probability
        r = targets(M, sol)
        print(f"  point mass Phi(-3), N={N:3d}: target={r['mT']:.4f} pseudo-target={r['mP']:.4f} c(1)={r['c1']:.4f}   "
              f"difference from no point mass: target {r['mT']-out[N]['mT']:+.2e}, pseudo-target {r['mP']-out[N]['mP']:+.2e}")
    print("  where the limit binds in the next-to-last period: R beta E[(G psi Y)^-rho] is finite iff E[(psi - inf)^-rho] is finite")
    lo, hi = 0.7, 1.3
    for a in (1.0, 2.0, 2.5, 3.0, 4.0):
        vals = []
        for eps in (1e-3, 1e-5, 1e-7, 1e-9):
            f = lambda u: beta_dist.pdf(u, a, a) * ((hi - lo) * u) ** (-P.rho)
            vals.append(quad(f, eps, 1, limit=400, points=[eps * 10, 1e-2, 0.1])[0])
        print(f"    permanent shock = {lo} + {hi-lo:.1f} Beta({a},{a}): E[(psi - inf)^-rho ; psi - inf > eps] for eps = 1e-3,1e-5,1e-7,1e-9: "
              + ", ".join(f"{v:.4g}" for v in vals) + f"   (finite iff {a} > rho = {P.rho}: {a > P.rho})")


def section_bounds():
    print("\n=== The bound c <= cbar and the key inequality of the existence proof (no point mass, N=200) ===")
    M = Problem("natural", 0.005, 0.3, N=200)
    Gt = P.G * M.psi
    EG = float(np.dot(M.w, Gt ** (1 - P.rho))); vaf = P.beta * EG
    theta = 1 - M.x
    alpha = 0.5 * (1 + vaf)
    Y1 = M.xi_tilde(0.0); Yinf = M.xi_tilde(M.h_inf)
    # largest delta on a grid with theta-term at most alpha
    deltas = np.geomspace(1e-6, 1.0, 400)
    q = np.array([M.w[Y1 <= d].sum() for d in deltas])
    ok = P.RPF * theta ** (1 - P.rho) * (1 + P.RPF) ** (P.rho - 1) * q ** (1 / P.rho) <= alpha
    delta = deltas[ok][-1]
    zeta = vaf * delta ** (1 - P.rho) / (alpha - vaf)
    F = lambda x: zeta + x ** (1 - P.rho)
    print(f"  beta E[Gtilde^(1-rho)] = {vaf:.4f} (finite value of autarky); theta = 1 - G psi_min/R = {theta:.4f}; alpha = {alpha:.4f}; delta = {delta:.4g}; zeta = {zeta:.4g}")
    # cbar: next-to-last-period consumption function with the largest income
    g = lambda a: np.sum(M.w[None, :] * (P.R * a[:, None] + (Gt * Yinf)[None, :]) ** (-P.rho), axis=1)
    cb = (P.R * P.beta * g(AGRID)) ** (-1 / P.rho); mb = AGRID + cb
    cbar = lambda x: np.where(x <= mb[0], x, np.interp(x, mb, cb))
    xs = np.geomspace(1e-6, 200, 600)
    abar = xs - cbar(xs)
    worst_ratio = 0.0
    for n, Y in (("1", Y1), ("inf", Yinf)):
        lhs = P.beta * np.sum(M.w[None, :] * Gt[None, :] ** (1 - P.rho) * F(abar[:, None] * P.R / Gt[None, :] + Y[None, :]), axis=1)
        worst_ratio = max(worst_ratio, float(np.max(lhs / (alpha * F(xs)))))
    print(f"  key inequality: max over x and both extreme horizons of beta E[Gtilde^(1-rho) F(x')] / (alpha F(x)) at a = abar(x): {worst_ratio:.4f} (must be <= 1)")
    hist = M.solve(horizon=40); sol = M.solve()
    B = (1 + P.RPF) ** (P.rho - 1) / ((P.rho - 1) * (1 - alpha))
    clow = lambda x: ((P.rho - 1) * B * F(x)) ** (-1 / (P.rho - 1))
    viol_up = max(float(np.max(P.cf(s)(xs) - cbar(xs))) for s in hist[1:] + [sol])
    viol_lo = min(float(np.min(P.cf(s)(xs) - clow(xs))) for s in hist[1:] + [sol])
    print(f"  c_t <= cbar at horizons 1..40 and in the limit: max(c_t - cbar) = {viol_up:.2e} (<= 0 up to interpolation); min(c_t - c_lower) = {viol_lo:.3e} (>= 0)")


def section_existence_without_ric():
    print("\n=== Existence needs only finite value of autarky: return impatience fails (R=0.95), no point mass, xi_u = 0.05 ===")
    keep = (P.R, P.G, P.beta)
    P.R, P.G, P.beta = 0.95, 1.03, 0.96
    P.APF = (P.R * P.beta) ** (1 / P.rho); P.RPF = P.APF / P.R; P.GPF = P.APF / P.G; P.Rn = P.R / P.G
    M = Problem("natural", 0.005, 0.05, N=200)
    vaf = P.beta * float(np.dot(M.w, (P.G * M.psi) ** (1 - P.rho)))
    sol = M.solve(tol=1e-11, maxit=60000); c = P.cf(sol)
    print(f"  return patience factor {P.RPF:.4f} (return impatience fails); beta E[Gtilde^(1-rho)] = {vaf:.4f}; G psi_min/R = {M.x:.4f}; iterations {M.iters}")
    print(f"  c at x = 0.5, 1, 2, 5, 20: {np.round(c(np.array([0.5, 1, 2, 5, 20.])), 5)};  c(x)/x at 1e-9: {c(1e-9)/1e-9:.6f};  c(300)/300 = {c(300.)/300:.4f}")
    line("  targets", M, sol)
    P.R, P.G, P.beta = keep
    P.APF = (P.R * P.beta) ** (1 / P.rho); P.RPF = P.APF / P.R; P.GPF = P.APF / P.G; P.Rn = P.R / P.G


def section_limit():
    print("\n=== The restrained consumer as the limit when the unemployment probability goes to zero ===")
    xs = np.geomspace(1e-3, 30, 500)
    for mu, prb, label in ((0.3, norm.cdf(-3.0), "xi_u=0.3, point mass at the infimum"), (0.3, 0.0, "xi_u=0.3, no point mass (N=50)"),
                           (0.0, 0.0, "xi_u=0 (the claim of the text)")):
        N = 50 if (mu > 0 and prb == 0) else 7
        L = Problem("restrained", 0.0, mu, N=N, prb=prb)
        histL = L.solve(horizon=6); solL = L.solve(); cL = P.cf(solL)
        print(f"  {label}: restrained consumer's limit binds below x = {solL[0][1]:.4f}; c(x)/x at 1e-9 = {cL(1e-9)/1e-9:.4f}")
        for p in (5e-2, 5e-3, 5e-4, 5e-5, 5e-6):
            M = Problem("natural", p, mu, N=N, prb=prb)
            hist = M.solve(horizon=6); sol = M.solve()
            fin = [float(np.max(np.abs(P.cf(hist[j])(xs) - P.cf(histL[j])(xs)))) for j in (1, 2, 6)]
            print(f"     p={p:7.0e}: max |c_t(.;p) - restrained| at horizons 1, 2, 6: {fin[0]:.2e} {fin[1]:.2e} {fin[2]:.2e};  in the limit: {np.max(np.abs(P.cf(sol)(xs) - cL(xs))):.2e}")


def section_c():
    print("\n=== (c) The constraint c <= m kept in every period, with xi_u > 0 ===")
    for mu in (0.05, 0.3, 0.5):
        M = Problem("artificial", 0.005, mu, N=7, prb=norm.cdf(-3.0)); sol = M.solve(); line(f"  artificial, xi_u={mu:.2f}, point-mass law", M, sol)
    # against HARK, with HARK's own equiprobable laws
    a = P.hark_agent(0.005, 0.3, 7, boro=0.0); hs = a.solution[0]
    M = P.Model(0.005, 0.3, 7)
    A = Problem("artificial", 0.005, 0.3); A.psi, A.xi, A.w = M.psi, M.xi, M.w; A.Einv = M.Einv
    sol = A.solve(); c = P.cf(sol)
    mm = np.linspace(0.02, 30, 600)
    print(f"  against HARK (BoroCnstArt=0, IncUnemp=0.3, HARK's equiprobable laws): max |c - c_HARK| = {np.max(np.abs(c(mm) - hs.cFunc(mm))):.2e}; "
          f"constraint binds below m = {sol[0][1]:.4f}")
    try:
        a.check_conditions(verbose=False); a.calc_stable_points()
        r = targets(A, sol)
        print(f"  targets: here {r['mT']:.4f}, {r['mP']:.4f}; HARK mNrmTrg={a.bilt['mNrmTrg']:.4f} mNrmStE={a.bilt['mNrmStE']:.4f}")
    except Exception as e:
        print("  HARK stable points failed:", repr(e)[:120])


def section_wric():
    print("\n=== Finite value of autarky and G psi_min < R imply weak return impatience at the probability of the worst event (xi_u > 0) ===")
    rng = np.random.default_rng(0); bad = 0; n = 0; closest = 0.0
    for _ in range(200000):
        R, G, rho = rng.uniform(0.8, 1.3), rng.uniform(0.8, 1.6), rng.uniform(1.05, 6)
        k = rng.integers(2, 6); psi = np.sort(rng.uniform(0.2, 2.5, k)); w = rng.dirichlet(np.ones(k)); psi = psi / np.dot(w, psi)
        b = rng.uniform(0.5, 1.5); p = rng.uniform(0.001, 1.0)
        if b * G ** (1 - rho) * np.dot(w, psi ** (1 - rho)) < 1 and G * psi[0] < R:
            n += 1
            val = (p * w[0]) ** (1 / rho) * (R * b) ** (1 / rho) / R
            closest = max(closest, val); bad += val >= 1
    print(f"  random draws satisfying both hypotheses: {n}; violations of (p_worst)^(1/rho) * return patience factor < 1: {bad}; largest value {closest:.4f}")


def section_infinite_h():
    print("\n=== Minimum human wealth not finite (G psi_min >= R): consumption is flat in resources, relative to its level ===")
    keep = (P.R, P.G, P.beta)
    for label, (R, G, b) in {"return impatience holds": (1.00, 1.20, 0.96), "return impatience fails, APF >= G psi_min": (0.90, 1.08, 0.99)}.items():
        P.R, P.G, P.beta = R, G, b
        P.APF = (R * b) ** (1 / P.rho); P.RPF = P.APF / R; P.GPF = P.APF / G; P.Rn = R / G
        M = P.Model(0.005, 0.05, 7)
        EGr = float(np.dot(M.w, (G * M.psi) ** (-P.rho)))
        print(f"  {label}: G psi_min/R = {M.x:.4f}; R beta E[Gtilde^-rho] = {R*b*EGr:.4f} (a constant limit would need exactly 1)")
        cur = (np.array([0.0, 1.0]), np.array([0.0, 1.0]))
        hn = lambda j: M.xi_min * sum(M.x ** i for i in range(1, j + 1))
        for j in range(1, 201):
            cur = M.step(cur, hn(j - 1))
            if j in (5, 20, 50, 100, 200):
                h = hn(j); c1, c5 = (float(np.interp(m0 + h, *cur)) for m0 in (1.0, 5.0))
                print(f"     n={j:3d}: limit -{h:10.3f}  c_n(1)={c1:9.4f}  c_n(5)/c_n(1)={c5/c1:.5f}  bound 1 + 4/(1+h) = {1 + 4/(1+h):.5f}")
    P.R, P.G, P.beta = keep
    P.APF = (P.R * P.beta) ** (1 / P.rho); P.RPF = P.APF / P.R; P.GPF = P.APF / P.G; P.Rn = P.R / P.G


if __name__ == "__main__":
    section_a(); section_bounds(); section_existence_without_ric(); section_limit(); section_c(); section_wric(); section_infinite_h()
