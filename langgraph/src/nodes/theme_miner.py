from __future__ import annotations
from typing import List
import re
from collections import Counter
from ..state import AppState

STOP = {"with","from","that","this","have","been","into","about","which","where","there"}

def _keywords(texts: List[str], top_k: int = 12) -> List[str]:
    toks = []
    for t in texts:
        for w in re.findall(r"[A-Za-z][A-Za-z\-]+", t.lower()):
            if len(w) >= 4 and w not in STOP:
                toks.append(w)
    most = [w for w,_ in Counter(toks).most_common(top_k)]
    uniq, seen = [], set()
    for w in most:
        stem = w[:6]
        if stem not in seen:
            uniq.append(w); seen.add(stem)
    return uniq

def run(state: AppState) -> AppState:
    texts = [p["title"] for p in state["papers"]] + [(p.get("abstract") or "") for p in state["papers"]]
    texts += [pd["section"] + ": " + pd["excerpt"] for pd in state["policy_docs"]]
    state["themes"] = _keywords(texts, 12)[:10]
    return state
