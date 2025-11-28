from __future__ import annotations
from typing import List
from ..state import AppState, Indicator

MOCK_INDICATORS: List[Indicator] = [
    {"code": "SL.TLF.ACTI.FE.ZS", "name": "Female labor force participation (%, modeled ILO)", "value": 21.0, "year": 2023},
    {"code": "IT.NET.USER.ZS", "name": "Individuals using the Internet (% of population)", "value": 36.7, "year": 2023},
    {"code": "SE.ADT.1524.LT.ZS", "name": "Youth literacy rate (% ages 15-24)", "value": 74.1, "year": 2022},
]

def run(state: AppState) -> AppState:
    state["indicators"] = MOCK_INDICATORS
    return state
