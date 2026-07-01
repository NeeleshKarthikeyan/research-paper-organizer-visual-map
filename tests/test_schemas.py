"""
Unit tests for Pydantic input and output schemas.
"""

import pytest
from pydantic import ValidationError
from src.schemas import PaperInput, TriageOutput


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
