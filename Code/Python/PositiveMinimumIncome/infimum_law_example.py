"""The appendix's example with the point mass of the permanent shock at its law's infimum.

Permanent shock: with probability prb it equals the infimum of a mean-one lognormal truncated at three
standard deviations of its log (log s.d. 0.1 after truncation); otherwise a draw from that law times
(1 - prb*inf)/(1 - prb). This is the construction of the transitory shock around the unemployment event,
and is the default law of HARK-dev's BufferStockConsumerType for positive income while unemployed.
"""
import numpy as np
from scipy.stats import norm
from scipy.optimize import brentq
import positive_income_checks as P

def trunc_lognormal(sd_log, bot=-3.0, top=3.0, N=7):
    """Mean-one lognormal truncated at bot/top s.d. of its log, log s.d. sd_log after truncation: infimum, supremum, N equiprobable atoms."""
    Z = norm.cdf(top) - norm.cdf(bot)
    var_z = 1 + (bot * norm.pdf(bot) - top * norm.pdf(top)) / Z - ((norm.pdf(bot) - norm.pdf(top)) / Z) ** 2
    s = sd_log / np.sqrt(var_z)
    mean_raw = np.exp(s * s / 2) * (norm.cdf(top - s) - norm.cdf(bot - s)) / Z
    mu = -np.log(mean_raw)
    edges = norm.ppf(norm.cdf(bot) + Z * np.arange(N + 1) / N)
    atoms = np.exp(mu + s * s / 2) * (norm.cdf(edges[1:] - s) - norm.cdf(edges[:-1] - s)) / (Z / N)
    return np.exp(mu + s * bot), np.exp(mu + s * top), atoms

class InfModel(P.Model):
    def __init__(self, p, mu, N=7, prb=None, sd=0.1):
        self.p, self.mu, self.n = p, mu, N
        inf, sup, base = trunc_lognormal(sd, N=N)
        _, _, theta = trunc_lognormal(sd, N=N)
        if mu > 0:
            prb = norm.cdf(-3.0) if prb is None else prb
            scale = (1 - prb * inf) / (1 - prb)
            psi1 = np.concatenate(([inf], scale * base)); w1 = np.concatenate(([prb], (1 - prb) * np.ones(N) / N))
        else:
            prb = 0.0; psi1 = base; w1 = np.ones(N) / N
        xi1 = np.concatenate(([mu], theta * (1 - p * mu) / (1 - p))); w2 = np.concatenate(([p], (1 - p) * np.ones(N) / N))
        self.psi = np.repeat(psi1, len(xi1)); self.xi = np.tile(xi1, len(psi1)); self.w = np.outer(w1, w2).ravel()
        self.psi_min, self.xi_min, self.prb = psi1.min(), mu, prb
        self.worst = np.isclose(self.xi, self.xi_min) & (np.isclose(self.psi, self.psi_min) | (self.xi_min == 0))
        self.p_worst = self.w[self.worst].sum()
        self.x = P.G * self.psi_min / P.R
        self.h_inf = self.xi_min * self.x / (1 - self.x)
        self.Einv = float(np.dot(self.w, 1 / self.psi))
        self.agrid = np.concatenate([[0.0], np.geomspace(1e-12, 400.0, 1400)])
        self.inf, self.next_min = inf, np.sort(psi1)[1]

def row(mu, N=7):
    M = InfModel(0.005, mu, N); sol = M.solve(tol=1e-12); c = P.cf(sol)
    co = lambda m: c(m + M.h_inf)
    dT = lambda m: (m - co(m)) * P.Rn * M.Einv + 1 - m
    dP = lambda m: (m - co(m)) * P.Rn + 1 - m
    lo = -M.h_inf + 1e-10
    (mT,), decT = P.roots_decreasing(dT, lo, 60); (mP,), decP = P.roots_decreasing(dP, lo, 60)
    kb = 1 - M.p_worst ** (1 / P.rho) * P.RPF
    return dict(mu=mu, N=N, psi_min=M.psi_min, next=M.next_min, Epsi=float(np.dot(M.w, M.psi)), Exi=float(np.dot(M.w, M.xi)), p_worst=M.p_worst,
                h=M.h_inf, kbar=kb, kbar_num=float(c(1e-10) / 1e-10), c1=float(co(1.0)), mT=mT, mP=mP, aT=mT - float(co(mT)), aP=mP - float(co(mP)),
                unique=decT and decP)

if __name__ == "__main__":
    inf, sup, atoms = trunc_lognormal(0.1)
    print(f"base law: infimum {inf:.5f} supremum {sup:.5f} mean of atoms {atoms.mean():.6f}; point-mass probability Phi(-3) = {norm.cdf(-3):.6f}")
    for mu in (0.0, 0.05, 0.3, 0.5):
        for N in ((7, 15) if mu == 0.3 else (7,)):
            r = row(mu, N)
            print(f"xi_u={r['mu']:.2f} N={r['N']:2d}: psi_min={r['psi_min']:.5f} (next {r['next']:.5f}) E[psi]={r['Epsi']:.6f} E[xi]={r['Exi']:.6f} p_worst={r['p_worst']:.3e} "
                  f"h_min={r['h']:.4f} kappa_max={r['kbar']:.6f} (solver {r['kbar_num']:.6f}) c(1)={r['c1']:.4f} target={r['mT']:.4f} pseudo={r['mP']:.4f} "
                  f"a(target)={r['aT']:.4f} a(pseudo)={r['aP']:.4f} unique&decreasing={r['unique']}")
