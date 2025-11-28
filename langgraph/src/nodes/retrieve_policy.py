from __future__ import annotations
from typing import List
from ..state import AppState, PolicyRef

MOCK_POLICY_SNIPPETS: List[PolicyRef] = [
    {
        "source": "Pakistan National SME Policy 2021",
        "section": "Women Entrepreneurship & Digital Finance",
        "excerpt": "Expand access to digital financial services for women-led SMEs in rural districts.",
        "url": "https://example.org/sme-policy"
    },
    {
        "source": "Digital Pakistan Policy 2018",
        "section": "Broadband & Inclusion",
        "excerpt": "Broadband expansion and digital upskilling are critical to inclusive growth in underserved regions.",
        "url": "https://example.org/digital-policy"
    },
    {
        "source": "SDG 8: Decent Work & Economic Growth",
        "section": "Productive Employment",
        "excerpt": "Promote sustained, inclusive and sustainable economic growth and decent work for all.",
        "url": "https://sdgs.un.org/goals/goal8"
    },
]

def run(state: AppState) -> AppState:
    state["policy_docs"] = MOCK_POLICY_SNIPPETS
    return state
