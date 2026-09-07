"""
Pydantic schemas for input paper metadata and output triage reports.
"""

from typing import List, Optional, Literal, Dict
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
CompetenceLevel = Literal["none", "basic", "working", "solid"]



class ComplexitySignals(BaseModel):
    has_math_complexity: bool = Field(default=False, description="Contains mathematical or theoretical terms (e.g. proof, theorem).")
    has_ml_complexity: bool = Field(default=False, description="Contains machine learning methodology terms (e.g. gradient, backpropagation).")
    has_systems_complexity: bool = Field(default=False, description="Contains systems or infrastructure terms (e.g. latency, throughput).")
    has_experimental_complexity: bool = Field(default=False, description="Contains research methodology terms (e.g. ablation, baseline).")


class PaperRequirements(BaseModel):
    paper_type: PaperType = Field(description="The structural type of the paper.")
    topic_tags: List[str] = Field(description="Domain-specific topics covered in the paper.")
    complexity_signals: ComplexitySignals = Field(description="Deterministic evidence of complexity.")
    prerequisites: List[str] = Field(description="Knowledge required by the paper.")


class UserProfile(BaseModel):
    """Describes the reader's self-assessed competence across relevant domains.

    Each field uses CompetenceLevel: 'none' | 'basic' | 'working' | 'solid'.
    Defaults to 'none' so that a partially filled profile is still valid.
    """
    programming: CompetenceLevel = Field(
        default="none",
        description="General programming ability (Python, scripting, debugging)."
    )
    mathematics: CompetenceLevel = Field(
        default="none",
        description="Mathematical maturity (calculus, proofs, notation)."
    )
    statistics: CompetenceLevel = Field(
        default="none",
        description="Probability and statistical reasoning."
    )
    machine_learning: CompetenceLevel = Field(
        default="none",
        description="Familiarity with ML concepts (training, loss, evaluation)."
    )
    deep_learning: CompetenceLevel = Field(
        default="none",
        description="Experience with neural networks, backpropagation, optimizers."
    )
    systems_and_infrastructure: CompetenceLevel = Field(
        default="none",
        description="Knowledge of distributed systems, GPUs, quantization, latency."
    )
    research_experience: CompetenceLevel = Field(
        default="none",
        description="Familiarity with experimental design, baselines, ablation studies."
    )


class PersonalisedDifficulty(BaseModel):
    """The result of comparing PaperRequirements against a UserProfile."""
    difficulty: DifficultyType = Field(
        description="Personalised difficulty for this reader."
    )
    gap_score: int = Field(
        description="Raw gap score (0-12). Higher means more prerequisites are missing."
    )
    matched_strengths: List[str] = Field(
        default_factory=list,
        description="Domains where the user has working or solid competence matching a paper demand."
    )
    missing_prerequisites: List[str] = Field(
        default_factory=list,
        description="Domains where the paper demands knowledge the user does not yet have."
    )


class PaperInput(BaseModel):
    title: str = Field(..., description="The title of the paper.")
    abstract: str = Field(..., description="The abstract or summary of the paper.")
    full_text: Optional[str] = Field(
        default=None, description="The complete text of the paper if extracted from a source like a PDF."
    )
    user_level: UserLevel = Field(
        default="beginner", description="Experience level of the user (legacy coarse field)."
    )
    user_goal: Optional[str] = Field(
        default=None, description="Optional stated learning goal of the user."
    )
    user_profile: Optional[UserProfile] = Field(
        default=None, description="Structured competence profile of the user across domains."
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
    complexity_signals: Optional[ComplexitySignals] = None
    paper_requirements: Optional[PaperRequirements] = None
    user_profile: Optional[UserProfile] = None
    personalised_difficulty: Optional[PersonalisedDifficulty] = None

