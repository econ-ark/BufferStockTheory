"""Checks for the appendix on positive income in the zero-income event.

Solves the model two ways and compares:
  (a) an endogenous-gridpoints solver written here, in resources measured from the natural
      borrowing limit, with the transformed (horizon-dependent) income of the appendix;
  (b) HARK's IndShockConsumerType in the original variables (IncUnemp > 0, no artificial constraint).
Then checks the appendix's statements: the natural limit, the limiting MPCs, the bounds on c,
the target and pseudo-target and their order, and the limit as the event's probability goes to zero.
"""
import logging, warnings, sys
from copy import deepcopy
import numpy as np
warnings.filterwarnings("ignore"); logging.disable(logging.CRITICAL)
import HARK
from HARK.ConsumptionSaving.ConsIndShockModel import IndShockConsumerType, init_idiosyncratic_shocks

R, G, beta, rho, sP, sT = 1.04, 1.03, 0.96, 2.0, 0.1, 0.1
APF = (R * beta) ** (1 / rho); RPF = APF / R; GPF = APF / G; Rn = R / G


def hark_agent(p, mu, n, cycles=0, boro=None, grid=400):
    q = deepcopy(init_idiosyncratic_shocks)
    q.update(dict(CRRA=rho, DiscFac=beta, PermGroFac=[G], PermShkStd=[sP], TranShkStd=[sT], UnempPrb=p, IncUnemp=mu,
                  LivPrb=[1.0], BoroCnstArt=boro, cycles=cycles, CubicBool=False, vFuncBool=False, PermShkCount=n,
                  TranShkCount=n, aXtraMin=0.0001, aXtraMax=300.0, aXtraCount=grid, aXtraNestFac=3, T_retire=0))
    q["Rfree"] = [R] if isinstance(q.get("Rfree"), list) else R
    a = IndShockConsumerType(**q); a.tolerance = 1e-11; a.solve(); return a


def shocks(p, mu, n):
    """Marginal laws exactly as HARK builds them: psi (n equiprobable atoms), xi (event atom mu, employed atoms rescaled)."""
    a = hark_agent(p, mu, n, cycles=1)
    d = a.IncShkDstn[0]
    return d.atoms[0].copy(), d.atoms[1].copy(), d.pmv.copy()


class Model:
    def __init__(self, p, mu, n):
        self.p, self.mu, self.n = p, mu, n
        self.psi, self.xi, self.w = shocks(p, mu, n)
        self.psi_min, self.xi_min = self.psi.min(), self.xi.min()
        self.worst = np.isclose(self.xi, self.xi_min) & (np.isclose(self.psi, self.psi_min) | (self.xi_min == 0))
        self.p_worst = self.w[self.worst].sum()
        self.x = G * self.psi_min / R
        self.h_inf = self.xi_min * self.x / (1 - self.x) if self.x < 1 else np.inf
        self.Einv = float(np.dot(self.w, 1 / self.psi))
        self.agrid = np.concatenate([[0.0], np.geomspace(1e-9, 400.0, 900)])

    def h(self, j):
        """Minimum human wealth with j periods to go (current income excluded)."""
        return self.xi_min * self.x * (1 - self.x ** j) / (1 - self.x)

    def xi_tilde(self, hnext):
        t = (self.xi - self.xi_min) + (self.xi_min + hnext) * (1 - self.psi_min / self.psi)
        t[self.worst] = 0.0
        return t

    def step(self, cprev, hnext, constrained=False):
        """One backward step in resources measured from the natural limit. cprev: (m grid, c grid) of next period."""
        mp, cp = cprev
        xt = self.xi_tilde(hnext)
        a = self.agrid[:, None]
        mnext = a * Rn / self.psi[None, :] + xt[None, :]
        cnext = np.interp(mnext, mp, cp)
        top = mnext > mp[-1]
        if top.any():
            slope = (cp[-1] - cp[-2]) / (mp[-1] - mp[-2])
            cnext = np.where(top, cp[-1] + slope * (mnext - mp[-1]), cnext)
        with np.errstate(divide="ignore"):
            mv = beta * R * np.sum(self.w[None, :] * (G * self.psi[None, :]) ** (-rho) * cnext ** (-rho), axis=1)
        c = np.where(np.isfinite(mv), mv ** (-1 / rho), 0.0)
        m = self.agrid + c
        if constrained and c[0] > 0:  # artificial constraint a~ >= 0 binds below m[0]
            m = np.concatenate([[0.0], m]); c = np.concatenate([[0.0], c])
        return m, c

    def solve(self, horizon=None, tol=1e-12, maxit=20000, constrained=False):
        cur = (np.array([0.0, 1.0]), np.array([0.0, 1.0]))  # c_T(m) = m
        hist = [cur]
        j = 0
        while True:
            hnext = self.h(j) if horizon is not None else self.h_inf  # next period has j periods to go
            new = self.step(cur, hnext, constrained)
            j += 1
            if horizon is not None:
                hist.append(new)
                if j == horizon:
                    return hist
            else:
                mm = np.geomspace(1e-6, 300, 400)
                if np.max(np.abs(np.interp(mm, *new) - np.interp(mm, *cur))) < tol or j >= maxit:
                    self.iters = j
                    return new
            cur = new


def cf(sol):
    return lambda m: np.interp(m, sol[0], sol[1])


def roots_decreasing(f, lo, hi, k=20001):
    g = np.linspace(lo, hi, k); v = f(g)
    s = np.where(np.sign(v[:-1]) != np.sign(v[1:]))[0]
    out = []
    for i in s:
        a, b = g[i], g[i + 1]
        for _ in range(80):
            mid = 0.5 * (a + b)
            if np.sign(f(np.array([mid]))[0]) == np.sign(f(np.array([a]))[0]): a = mid
            else: b = mid
        out.append(0.5 * (a + b))
    return out, bool(np.all(np.diff(v) < 0))


def report(p, mu, n):
    print(f"\n================ p={p}  income in the event mu={mu}  points={n} ================")
    M = Model(p, mu, n)
    print(f"psi_min={M.psi_min:.5f}  xi_min={M.xi_min:.5f} (lowest employed xi={np.min(M.xi[M.xi > M.xi_min + 1e-12]):.5f})  "
          f"P(worst)={M.p_worst:.6f} (p/n={p/n:.6f})  x=G psi_min/R={M.x:.5f}  h_min={M.h_inf:.5f}")
    print(f"E[xi]={np.dot(M.w, M.xi):.6f} E[psi]={np.dot(M.w, M.psi):.6f}")
    # ---- the transformed income
    xt = M.xi_tilde(M.h_inf)
    print(f"transformed income: min={xt.min():.3g} (only at the worst event: {bool(np.all((xt == 0) == M.worst))}); "
          f"smallest positive value={xt[xt > 0].min():.5f}; mean={np.dot(M.w, xt):.5f} "
          f"(formula 1 - xi_min + (xi_min+h)(1-psi_min E[1/psi]) = {1 - M.xi_min + (M.xi_min + M.h_inf) * (1 - M.psi_min * M.Einv):.5f}); "
          f"corr with psi={(lambda C: C[0, 1] / np.sqrt(C[0, 0] * C[1, 1]))(np.cov(M.psi, xt, aweights=M.w)):.3f}")
    # ---- finite horizon: MPC recursions and agreement with HARK
    N = 6
    hist = M.solve(horizon=N)
    kmax, kmin = 1.0, 1.0
    s = M.p_worst ** (1 / rho) * RPF
    print("finite horizon  n : h_min(n) vs -HARK mNrmMin | max MPC: solver, recursion, HARK | min MPC: solver, recursion | max |c - c_HARK|")
    for j in range(1, N + 1):
        kmax = 1 / (1 + s / kmax); kmin = 1 / (1 + RPF / kmin)
        m, c = hist[j]
        k_hi = c[1] / m[1]
        k_lo = (c[-1] - c[-2]) / (m[-1] - m[-2])
        a = hark_agent(p, mu, n, cycles=j); sol = a.solution[0]
        mm = np.linspace(0.02, 20, 400)
        err = np.max(np.abs(cf(hist[j])(mm) - sol.cFunc(mm - M.h(j))))
        print(f"              {j:2d} : {M.h(j):.6f} {-sol.mNrmMin:.6f} | {k_hi:.6f} {kmax:.6f} {sol.MPCmax:.6f} | {k_lo:.6f} {kmin:.6f} | {err:.2e}")
    # ---- infinite horizon
    sol = M.solve(); c = cf(sol)
    a = hark_agent(p, mu, n); hs = a.solution[0]
    mm = np.linspace(0.02, 30, 600)
    print(f"limit: solver iterations={M.iters}; -HARK mNrmMin={-hs.mNrmMin:.6f} vs h_min={M.h_inf:.6f}; "
          f"max |c - c_HARK| on resources-above-limit in [0.02,30] = {np.max(np.abs(c(mm) - hs.cFunc(mm - M.h_inf))):.2e}")
    kbar, klow = 1 - s, max(0.0, 1 - RPF)
    print(f"max MPC: c(m)/m at m=1e-7 above the limit = {c(1e-7)/1e-7:.6f}; 1 - P(worst)^(1/rho) RPF = {kbar:.6f}; HARK MPCmax={hs.MPCmax:.6f}; "
          f"with p instead of P(worst): {1 - p ** (1 / rho) * RPF:.6f}")
    print(f"min MPC: slope at the top = {(sol[1][-1]-sol[1][-2])/(sol[0][-1]-sol[0][-2]):.6f}; 1 - RPF = {klow:.6f}")
    g = np.geomspace(1e-6, 300, 4000)
    ratio = c(g) / g
    print(f"bounds: min c/m~ = {ratio.min():.6f} >= {klow:.6f}: {bool(ratio.min() >= klow - 1e-9)};  max c/m~ = {ratio.max():.6f} <= {kbar:.6f}: {bool(ratio.max() <= kbar + 1e-9)}; "
          f"c/m~ nonincreasing: {bool(np.all(np.diff(ratio) <= 1e-10))}")
    h_pf = 1 / (1 - G / R)
    print(f"perfect-foresight upper bound c <= (m - 1 + h) k_min holds on grid: {bool(np.all(c(g) <= (g - M.h_inf - 1 + h_pf) * klow + 1e-9))}")
    # ---- target and pseudo-target in the original variables
    co = lambda m: c(m + M.h_inf)                      # consumption as a function of m
    dT = lambda m: (m - co(m)) * Rn * M.Einv + 1 - m    # E[m'] - m
    dP = lambda m: (m - co(m)) * Rn + 1 - m             # E[psi m'] - m
    lo = -M.h_inf + 1e-9
    rT, decT = roots_decreasing(dT, lo, 60); rP, decP = roots_decreasing(dP, lo, 60)
    print(f"E[m']-m: value just above the limit={dT(np.array([lo]))[0]:.5f} (= E[transformed income] {np.dot(M.w, xt):.5f}); strictly decreasing={decT}; roots={np.round(rT, 5)}")
    print(f"E[psi m']-m: value just above the limit={dP(np.array([lo]))[0]:.5f} (= E[psi * transformed income] {np.dot(M.w, M.psi * xt):.5f}); strictly decreasing={decP}; roots={np.round(rP, 5)}")
    if rT and rP:
        mT, mP = rT[0], rP[0]
        print(f"target m={mT:.5f} (assets {mT - co(mT):.5f}); pseudo-target m={mP:.5f} (assets {mP - co(mP):.5f}); c(1)={float(co(1.0)):.5f}")
        print(f"order: target > pseudo-target is {mT > mP}; c(1) < 1 is {bool(co(1.0) < 1)}; pseudo-target > 1 is {mP > 1}; target > 1 is {mT > 1}")
        try:
            a.check_conditions(verbose=False); a.calc_stable_points()
            print(f"HARK: mNrmTrg={a.bilt['mNrmTrg']:.5f} mNrmStE={a.bilt['mNrmStE']:.5f}")
        except Exception as e:
            print("HARK stable points failed:", repr(e)[:120])
    return M, sol


def limit_check(mu, n):
    print(f"\n================ limit as the event's probability goes to zero (mu={mu}, points={n}) ================")
    base = Model(1e-12, mu, n)   # shock atoms as p -> 0; the event atom keeps (numerically) zero weight
    # the limit consumer: no event, may not borrow more than h_min(mu)
    L = Model(1e-12, mu, n)
    keep = ~np.isclose(L.xi, mu)
    L.psi, L.xi, L.w = L.psi[keep], L.xi[keep], L.w[keep] / L.w[keep].sum()
    L.worst = np.zeros(L.psi.shape, bool)
    L.xi_tilde = lambda hnext: (L.xi - mu) + (mu + hnext) * (1 - base.psi_min / L.psi)
    L.h_inf = mu * base.x / (1 - base.x)
    solL = L.solve(constrained=True); cL = cf(solL)
    mm = np.geomspace(1e-3, 30, 500)
    print(f"limit consumer: borrowing limit h={L.h_inf:.5f}; constraint binds below resources-above-limit {solL[0][1]:.5f}")
    for p in (5e-2, 5e-3, 5e-4, 5e-5, 5e-6):
        M = Model(p, mu, n); sol = M.solve(); c = cf(sol)
        print(f"  p={p:8.0e}: P(worst)={M.p_worst:.2e}  h_min={M.h_inf:.5f}  max |c(.;p) - c_limit| = {np.max(np.abs(c(mm) - cL(mm))):.3e}  max MPC={1 - M.p_worst ** (1 / rho) * RPF:.5f}")


if __name__ == "__main__":
    print("HARK", HARK.__version__, f"| APF={APF:.6f} RPF={RPF:.6f} GPF={GPF:.6f} R/G={Rn:.6f}")
    for mu in (0.0, 0.05, 0.3):
        report(0.005, mu, 7)
    limit_check(0.3, 7)
