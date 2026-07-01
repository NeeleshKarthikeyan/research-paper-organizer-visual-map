"""
Optional LLM interface placeholder for future integration (e.g. Google Gemini API).

Note: The core MVP uses deterministic rule-based triage in tools.py and does NOT
depend on or call any external LLM service by default.
"""

import os
from typing import Optional, Dict, Any


def is_llm_available() -> bool:
    """Check if an LLM API key (GOOGLE_API_KEY) is configured in environment."""
    return bool(os.getenv("GOOGLE_API_KEY"))


def analyze_paper_with_llm(title: str, abstract: str) -> Optional[Dict[str, Any]]:
    """Placeholder function for future Gemini-assisted deep semantic paper analysis.

    Returns None in the current MVP as rule-based evaluation is used.
    """
    if not is_llm_available():
        return None

    # Future integration point:
    # 1. Initialize google.generativeai with GOOGLE_API_KEY
    # 2. Pass prompt and schema to model.generate_content
    # 3. Parse JSON response into structured triage insights
    return None
