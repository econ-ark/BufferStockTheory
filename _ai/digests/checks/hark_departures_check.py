"""Check, by running HARK, the departures the digest lists (worst-income probability, survival in the factors, human wealth convention)."""
import logging, warnings
from copy import deepcopy
import numpy as np
warnings.filterwarnings("ignore"); logging.disable(logging.CRITICAL)
import HARK
from HARK.ConsumptionSaving.ConsIndShockModel import IndShockConsumerType, init_idiosyncratic_shocks
print("HARK", HARK.__version__)
def agent(**kw):
    q = deepcopy(init_idiosyncratic_shocks)
    q.update(dict(CRRA=2.0, DiscFac=0.96, PermGroFac=[1.03], PermShkStd=[0.1], TranShkStd=[0.1], UnempPrb=0.005, IncUnemp=0.0,
                  LivPrb=[1.0], BoroCnstArt=None, cycles=0, T_retire=0))
    q["Rfree"] = [1.04] if isinstance(q.get("Rfree"), list) else 1.04
    q.update(kw); a = IndShockConsumerType(**q); a.check_conditions(verbose=False); return a
keys = ["APFac", "RPFac", "GPFacRaw", "GPFacMod", "GPFacLiv", "PFVAFac", "VAFac", "WRPFac", "WorstPrb", "MPCmin", "MPCmax", "hNrm"]
for label, kw in [("paper baseline", {}), ("IncUnemp=0.3", dict(IncUnemp=0.3)), ("IncUnemp=0.95 (above worst employed draw)", dict(IncUnemp=0.95)),
                  ("LivPrb=0.98", dict(LivPrb=[0.98])), ("default HARK", None)]:
    if kw is None:
        a = IndShockConsumerType(cycles=0); a.check_conditions(verbose=False)
    else:
        a = agent(**kw)
    d = a.IncShkDstn[0]; xi = d.atoms[1]
    print(f"\n{label}: xi atoms min={xi.min():.4f} next={np.sort(np.unique(xi))[1]:.4f} E[xi]={np.dot(d.pmv, xi):.6f}")
    print("  " + " ".join(f"{k}={a.bilt[k]:.5f}" for k in keys if k in a.bilt))
    print("  conditions:", {k: bool(v) for k, v in a.conditions.items()})
