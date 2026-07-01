"""
Pydantic schemas for input paper metadata and output triage reports.
"""

from typing import List, Optional, Literal
from pydantic import BaseModel, Field, field_validator


UserLevel = Literal["beginner", "intermediate", "advanced"]
DecisionType = Literal["read", "skim", "save_for_later", "skip_for_now"]
DifficultyType = Literal["beginner", "intermediate", "advanced"]
PaperType = Literal[
    "survey",
    "methods",
    "benchmark",
    "application",
    "dataset",
    "systems",
    "theory",
    "position",
    "unknown",
]


class PaperInput(BaseModel):
    title: str = Field(..., description="The title of the paper.")
    abstract: str = Field(..., description="The abstract or summary of the paper.")
    user_level: UserLevel = Field(
        default="beginner", description="Experience level of the user."
    )
    user_goal: Optional[str] = Field(
        default=None, description="Optional stated learning goal of the user."
    )
    source_url: Optional[str] = Field(
        default=None, description="URL to the paper or arXiv page."
    )
    authors: Optional[List[str]] = Field(
        default=None, description="List of paper authors."
    )
    published_date: Optional[str] = Field(
        default=None, description="Publication or upload date string."
    )
    source: Optional[str] = Field(
        default="manual", description="Source of the input (e.g. manual, arxiv)."
    )
    category: Optional[str] = Field(
        default=None, description="Primary field or category (e.g. cs.CL)."
    )

    @field_validator("title", "abstract")
    @classmethod
    def check_non_empty(cls, value: str) -> str:
        if not value or not value.strip():
            raise ValueError("Field cannot be empty or whitespace only.")
        return value.strip()


class TriageOutput(BaseModel):
    title: str
    decision: DecisionType
    difficulty: DifficultyType
    paper_type: PaperType
    topic_tags: List[str]
    prerequisites: List[str]
    summary: str
    reading_path: List[str]
    reason: str
    source_url: Optional[str] = None
