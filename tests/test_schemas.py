"""
Unit tests for Pydantic input and output schemas.
"""

import pytest
from pydantic import ValidationError
from src.schemas import PaperInput, TriageOutput, PaperRequirements, ComplexitySignals


def test_valid_paper_input():
    paper = PaperInput(
        title="Test Paper",
        abstract="This is a test abstract.",
        user_level="beginner",
    )
    assert paper.title == "Test Paper"
    assert paper.abstract == "This is a test abstract."
    assert paper.user_level == "beginner"


def test_empty_title_or_abstract_fails():
    with pytest.raises(ValidationError):
        PaperInput(title="", abstract="Valid abstract")

    with pytest.raises(ValidationError):
        PaperInput(title="Valid title", abstract="   ")


def test_valid_paper_requirements():
    req = PaperRequirements(
        paper_type="methods",
        topic_tags=["LLM", "agent"],
        complexity_signals=ComplexitySignals(has_ml_complexity=True),
        prerequisites=["Basic Python"]
    )
    assert req.paper_type == "methods"
    assert "LLM" in req.topic_tags
    assert req.complexity_signals.has_ml_complexity is True


def test_invalid_paper_requirements():
    with pytest.raises(ValidationError):
        PaperRequirements(
            paper_type="invalid_type",  # Should fail Enum/Literal validation
            topic_tags=["LLM"],
            complexity_signals=ComplexitySignals(),
            prerequisites=[]
        )
