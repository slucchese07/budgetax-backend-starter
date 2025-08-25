from datetime import date
from typing import List, Dict

def prime_cost(cost: float, effective_life_years: int) -> float:
    """Annual depreciation using Prime Cost (straight line)."""
    if effective_life_years <= 0:
        return 0.0
    return cost / effective_life_years

def diminishing_value(opening_value: float, effective_life_years: int) -> float:
    """Simple DV approximation using 200%/effective life (non-pro-rata)."""
    if effective_life_years <= 0:
        return 0.0
    rate = 2.0 / effective_life_years
    return opening_value * rate

def build_schedule(cost: float, method: str, effective_life_years: int, salvage: float, fy_start: int, years: int = None) -> List[Dict]:
    """Return a schedule list of dicts (year, opening, depreciation, closing)."""
    entries = []
    remaining = cost
    years = years or effective_life_years
    for i in range(years):
        if remaining <= salvage:
            dep = 0.0
        else:
            if method == "PC":
                dep = prime_cost(cost - salvage, effective_life_years)
                if remaining - dep < salvage:
                    dep = max(0.0, remaining - salvage)
            else:
                dep = diminishing_value(remaining - salvage, effective_life_years)
                if remaining - dep < salvage:
                    dep = max(0.0, remaining - salvage)
        closing = remaining - dep
        entries.append({
            "fy_label": f"{fy_start+i}-{str((fy_start+i+1)%100).zfill(2)}",
            "opening_value": round(remaining, 2),
            "depreciation": round(dep, 2),
            "closing_value": round(closing, 2),
        })
        remaining = closing
    return entries
