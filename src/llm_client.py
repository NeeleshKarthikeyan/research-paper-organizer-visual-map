"""
Optional LLM interface for semantic paper analysis using Google Gemini.

Note: The core MVP uses deterministic rule-based triage in tools.py and does NOT
depend on or call any external LLM service by default. If it fails, it returns None.
"""

import os
from typing import Optional
from src.schemas import SemanticAnalysis


def is_llm_available() -> bool:
    """Check if an LLM API key (GEMINI_API_KEY) is configured in environment."""
    return bool(os.getenv("GEMINI_API_KEY"))


def analyze_paper_with_llm(title: str, abstract: str) -> Optional[SemanticAnalysis]:
    """Semantic paper analysis using Gemini.
    
    Catches any exceptions to ensure the deterministic pipeline never breaks.
    """
    if not is_llm_available():
        return None

    try:
        from google import genai
        from google.genai import types

        client = genai.Client()  # Automatically picks up GEMINI_API_KEY

        prompt = (
            f"Analyze the following research paper's title and abstract.\n"
            f"Title: {title}\n"
            f"Abstract: {abstract}\n\n"
            f"Provide a structured semantic analysis including topics, prerequisites, "
            f"math/ML/systems concepts, evidence of complexity, and an estimated difficulty "
            f"(beginner, intermediate, or advanced)."
        )

        model_name = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
        
        response = client.models.generate_content(
            model=model_name,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=SemanticAnalysis,
            ),
        )
        
        # Pydantic will validate the JSON string directly
        return SemanticAnalysis.model_validate_json(response.text)
        
    except Exception as e:
        print(f"Warning: LLM analysis failed ({str(e)}). Falling back to deterministic only.")
        return None
