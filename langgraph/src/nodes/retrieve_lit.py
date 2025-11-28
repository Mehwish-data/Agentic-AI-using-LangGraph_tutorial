from __future__ import annotations
from typing import List
from ..state import AppState, Paper

MOCK_PAPERS: List[Paper] = [
    {"id": "p1", "title": "Digital Microfinance and SME Growth in Pakistan", "year": 2023, "url": "https://example.org/p1", "abstract": "Study on microfinance platforms...", "citations": 12, "fields": ["Economics"], "region_mentioned": True},
    {"id": "p2", "title": "Women Freelancing in South Asia: Constraints and Enablers", "year": 2024, "url": "https://example.org/p2", "abstract": "Regional evidence...", "citations": 8, "fields": ["Labor", "Economics"], "region_mentioned": False},
    {"id": "p3", "title": "Rural Broadband Penetration and Household Welfare: Evidence from Punjab", "year": 2022, "url": "https://example.org/p3", "abstract": "Difference-in-differences analysis...", "citations": 18, "fields": ["Development"], "region_mentioned": True},
    {"id": "p4", "title": "Entrepreneurship Programs and Female Employment: Global Review", "year": 2021, "url": "https://example.org/p4", "abstract": "Systematic review...", "citations": 30, "fields": ["Economics"], "region_mentioned": False},
    {"id": "p5", "title": "Digital Literacy and Online Work Platforms in Pakistan", "year": 2024, "url": "https://example.org/p5", "abstract": "Survey of online work adoption...", "citations": 5, "fields": ["Economics", "ICT4D"], "region_mentioned": True},
]

def run(state: AppState) -> AppState:
    state["papers"] = MOCK_PAPERS
    return state
