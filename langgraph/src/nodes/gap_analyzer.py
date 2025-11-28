from __future__ import annotations
from typing import List, Dict
from ..state import AppState
from ..scoring import normalize_region

def _saturation(themes: List[str], papers, region_aliases: List[str]) -> Dict[str, Dict[str,int]]:
    stats = {}
    al = [a.lower() for a in region_aliases]
    for th in themes:
        gl, loc = 0, 0
        thl = th.lower()
        for p in papers:
            ta = (p.get("title","") + " " + (p.get("abstract") or "")).lower()
            if thl in ta:
                gl += 1
                local_flag = p.get("region_mentioned") or any(a in ta for a in al)
                if local_flag:
                    loc += 1
        stats[th] = {"global": gl, "local": loc}
    return stats

def run(state: AppState) -> AppState:
    reg = normalize_region(state["region"]) 
    stats = _saturation(state["themes"], state["papers"], reg["aliases"] + [state["region"]])
    gaps: List[str] = []
    for th, st in stats.items():
        gl, loc = st["global"], st["local"]
        if gl == 0 and loc == 0:
            continue
        if loc / max(gl, 1) <= 0.3:
            gaps.append(f"Local gap on '{th}': only {loc} local vs {gl} global studies.")
    if not gaps:
        ranked = sorted(stats.items(), key=lambda kv: kv[1]["local"] / max(1, kv[1]["global"]))
        for th, st in ranked[:5]:
            gl, loc = st["global"], st["local"]
            gaps.append(f"Potential gap on '{th}': {loc} local vs {gl} global studies.")
    state["gaps"] = gaps[:8]
    return state
