"""
Unit tests for Pydantic input and output schemas.
"""

import pytest
from pydantic import ValidationError
from src.schemas import PaperInput, TriageOutput, PaperRequirements, ComplexitySignals, UserProfile


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


def test_user_profile_defaults_to_none():
    """An empty UserProfile should have every field set to 'none'."""
    profile = UserProfile()
    assert profile.programming == "none"
    assert profile.mathematics == "none"
    assert profile.machine_learning == "none"
    assert profile.deep_learning == "none"
    assert profile.systems_and_infrastructure == "none"
    assert profile.research_experience == "none"


def test_user_profile_partial_construction():
    """A profile should accept a subset of fields; unset fields default to 'none'."""
    profile = UserProfile(
        programming="working",
        machine_learning="basic",
    )
    assert profile.programming == "working"
    assert profile.machine_learning == "basic"
    assert profile.mathematics == "none"
    assert profile.deep_learning == "none"


def test_user_profile_invalid_competence_level():
    """An invalid competence level string should raise a ValidationError."""
    with pytest.raises(ValidationError):
        UserProfile(programming="expert")  # "expert" is not a valid CompetenceLevel


def test_paper_input_accepts_user_profile():
    """PaperInput should accept an embedded UserProfile without error."""
    profile = UserProfile(mathematics="solid", deep_learning="working")
    paper = PaperInput(
        title="Attention Is All You Need",
        abstract="We propose a new network architecture, the Transformer.",
        user_profile=profile,
    )
    assert paper.user_profile is not None
    assert paper.user_profile.mathematics == "solid"
