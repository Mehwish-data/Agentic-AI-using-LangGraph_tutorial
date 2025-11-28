from __future__ import annotations
from typing import List, Dict
from datetime import datetime

from .state import Paper, Indicator, PolicyRef

REGION_ALIASES = {
    "south punjab": ["Bahawalpur", "Multan", "Dera Ghazi Khan", "Lodhran", "Vehari", "Rahim Yar Khan"],
}

def normalize_region(region: str):
    key = region.strip().lower()
    return {"label": region.strip(), "aliases": REGION_ALIASES.get(key, [])}

def novelty_score(global_hits: int, local_hits: int) -> float:
    if global_hits <= 0:
        return 0.7
    sat = local_hits / max(global_hits, 1)
    return max(0.0, min(1.0, 1.0 - sat))

def policy_demand_score(theme: str, policy_docs: List[PolicyRef]) -> float:
    hits = 0
    t = theme.lower()
    for pd in policy_docs:
        blob = (pd["section"] + " " + pd["excerpt"]).lower()
        if any(k in blob for k in t.split()[:2]):
            hits += 1
    if hits == 0:
        return 0.2
    return min(1.0, 0.3 + 0.2 * hits)

def data_feasibility_score(theme: str, indicators: List[Indicator], papers: List[Paper]) -> float:
    rel_papers = 0
    for p in papers:
        ta = (p.get("title", "") + " " + (p.get("abstract") or "")).lower()
        if theme.lower() in ta:
            rel_papers += 1
    ind_ok = 1 if len(indicators) >= 2 else 0
    score = 0.3 * min(1.0, rel_papers / 3) + 0.7 * ind_ok
    return max(0.0, min(1.0, score))

def method_fit_score(constraints: Dict[str, str]) -> float:
    tl = constraints.get("timeline", "").lower()
    if any(x in tl for x in ["3", "4", "90", "120", "month"]):
        return 0.8
    return 0.6

def timeliness_score(indicators: List[Indicator]) -> float:
    recent = sum(1 for i in indicators if (i.get("year") or 0) >= (datetime.now().year - 3))
    return min(1.0, recent / 5)
