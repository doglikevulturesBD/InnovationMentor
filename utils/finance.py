
from typing import List

def npv(rate: float, cashflows: List[float]) -> float:
    return sum(cf / ((1 + rate) ** t) for t, cf in enumerate(cashflows))

def irr(cashflows: List[float], guess: float = 0.1, tol: float = 1e-6, max_iter: int = 100) -> float:
    rate = guess
    for _ in range(max_iter):
        npv_val = 0.0
        d_npv = 0.0
        for t, cf in enumerate(cashflows):
            denom = (1 + rate) ** t
            npv_val += cf / denom
            if t > 0:
                d_npv += -t * cf / ((1 + rate) ** (t + 1))
        if abs(npv_val) < tol:
            return rate
        if d_npv == 0:
            break
        rate -= npv_val / d_npv
        if rate <= -0.9999:
            rate = -0.99
    return rate

def payback_period(cashflows: List[float]) -> float:
    cum = 0.0
    for i, cf in enumerate(cashflows):
        cum += cf
        if cum >= 0:
            prev_cum = cum - cf
            if cf != 0:
                return i - prev_cum / cf
            return float(i)
    return float('inf')

def build_projection(years:int, revenue:list, opex:list, capex:list, tax_rate:float=0.28, depreciation_years:int=5):
    depreciation = [0.0]*years
    if years>0 and sum(capex)>0:
        total_capex = sum(capex)
        per_year = total_capex / max(1,depreciation_years)
        for y in range(min(years,depreciation_years)):
            depreciation[y] = per_year
    ebit = []
    tax = []
    net_cf = []
    for y in range(years):
        e = revenue[y] - opex[y] - depreciation[y]
        ebit.append(e)
        t = max(0.0, e)*tax_rate
        tax.append(t)
        net = (revenue[y] - opex[y]) - t - capex[y]
        net_cf.append(net)
    return {"depreciation": depreciation, "ebit": ebit, "tax": tax, "net_cf": net_cf}
