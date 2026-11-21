"""Baseline (paper Table 'Microeconomic Model Calibration') values: closed forms, and HARK's solved target and pseudo-target."""
import logging, warnings, math
from copy import deepcopy
import numpy as np
warnings.filterwarnings("ignore"); logging.disable(logging.CRITICAL)
import HARK
from HARK.ConsumptionSaving.ConsIndShockModel import IndShockConsumerType, init_idiosyncratic_shocks
from HARK.distributions import expected

R, G, beta, rho, p, sP, sT = 1.04, 1.03, 0.96, 2.0, 0.005, 0.1, 0.1
APF = (R * beta) ** (1 / rho)
print("HARK", HARK.__version__)
print(f"APF={APF:.6f} RPF={APF/R:.6f} GPF={APF/G:.6f} FHWF={G/R:.6f} PFVAF={beta*G**(1-rho):.6f}")
print(f"lognormal exact: E[psi^-1]={math.exp(sP**2):.6f} GPFMod={APF/G*math.exp(sP**2):.6f} "
      f"VAF={beta*G**(1-rho)*math.exp(rho*(rho-1)/2*sP**2):.6f} E[log psi]={-sP**2/2:.6f} E[psi log psi]={sP**2/2:.6f}")
print(f"MPCmin={1-APF/R:.6f} MPCmax={1-p**(1/rho)*APF/R:.6f} WRPF={p**(1/rho)*APF/R:.6f} h(incl. current)={1/(1-G/R):.4f} h(excl.)={(G/R)/(1-G/R):.4f}")

def agent(n):
    q = deepcopy(init_idiosyncratic_shocks)
    q.update(dict(CRRA=rho, DiscFac=beta, PermGroFac=[G], PermShkStd=[sP], TranShkStd=[sT], UnempPrb=p, IncUnemp=0.0,
                  LivPrb=[1.0], BoroCnstArt=None, cycles=0, CubicBool=True, vFuncBool=False, PermShkCount=n, TranShkCount=n,
                  aXtraMin=0.001, aXtraMax=100.0, aXtraCount=400, aXtraNestFac=3, T_retire=0))
    q["Rfree"] = [R] if isinstance(q.get("Rfree"), list) else R
    a = IndShockConsumerType(**q); a.tolerance = 1e-10; a.solve(); return a

for n in (7, 15, 31):
    a = agent(n)
    d = a.IncShkDstn[0]; psi, xi = d.atoms[0], d.atoms[1]; w = d.pmv
    Einv = float(np.dot(w, 1 / psi)); E1mr = float(np.dot(w, psi ** (1 - rho)))
    a.check_conditions(verbose=False); a.calc_stable_points()
    s = a.solution[0]
    print(f"n={n:2d}: psi in [{psi.min():.4f},{psi.max():.4f}] xi in [{xi.min():.4f},{xi.max():.4f}] min employed xi={np.min(xi[xi>0]):.4f} "
          f"E[psi]={np.dot(w,psi):.6f} E[xi]={np.dot(w,xi):.6f} E[psi^-1]={Einv:.6f} GPFMod={APF/G*Einv:.6f} VAF={beta*G**(1-rho)*E1mr:.6f}")
    print(f"      mNrmMin={s.mNrmMin:.4f} hNrm(solution)={s.hNrm:.4f} MPCmin={s.MPCmin:.6f} MPCmax={s.MPCmax:.6f} "
          f"pseudo-target mNrmStE={a.bilt['mNrmStE']:.5f} target mNrmTrg={a.bilt['mNrmTrg']:.5f} c(target)={float(s.cFunc(a.bilt['mNrmTrg'])):.5f}")
