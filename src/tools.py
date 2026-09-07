"""
Deterministic rule-based helper tool functions for paper analysis and triage.
"""

import re
from typing import List, Optional, Dict
from src.schemas import (
    DecisionType, DifficultyType, PaperType, UserLevel,
    ComplexitySignals, PaperRequirements, UserProfile, PersonalisedDifficulty
)


def _strip_references(text: str) -> str:
    """Truncate paper text at the references or bibliography section to avoid false positives."""
    if not text:
        return ""
    # Use regex to find "references" or "bibliography" on their own line
    # \n\s* ensures it's at the start of a line, \s*\n ensures it's the only thing on the line
    match = re.search(r'\n\s*(references|bibliography)\s*\n', text.lower())
    if match:
        return text[:match.start()]
    return text


def classify_paper_type(title: str, abstract: str, full_text: Optional[str] = None) -> PaperType:
    """Classify paper type based on keywords in title, abstract, and optionally full text."""
    body = _strip_references(full_text) if full_text else ""
    text = f"{title} {abstract} {body}".lower()

    if any(k in text for k in ["survey", "review", "taxonomy"]):
        return "survey"
    if any(k in text for k in ["benchmark", "evaluation", "leaderboard"]):
        return "benchmark"
    if any(k in text for k in ["dataset", "corpus", "data collection"]):
        return "dataset"
    if any(k in text for k in ["theorem", "proof", "bound", "convergence"]):
        return "theory"
    if any(
        k in text
        for k in [
            "system",
            "serving",
            "latency",
            "scaling",
            "distributed",
            "throughput",
            "deployment",
        ]
    ):
        return "systems"
    if any(k in text for k in ["position", "perspective", "opinion"]):
        return "position"
    if any(
        k in text
        for k in ["we propose", "we introduce", "architecture", "framework", "method"]
    ):
        return "methods"
    if any(k in text for k in ["application", "applied", "case study"]):
        return "application"

    return "unknown"


def extract_topic_tags(title: str, abstract: str, full_text: Optional[str] = None) -> List[str]:
    """Extract relevant topic tags from title, abstract, and optional full text."""
    body = _strip_references(full_text) if full_text else ""
    text = f"{title} {abstract} {body}".lower()

    topic_map = {
        "transformer": ["transformer", "transformers"],
        "attention": ["attention", "self-attention"],
        "large language model": ["large language model", "large language models"],
        "LLM": ["llm", "llms"],
        "agent": ["agent", "agents", "autonomous agent"],
        "tool use": ["tool use", "tool-use", "calling tools", "function calling"],
        "retrieval": ["retrieval", "retriever"],
        "RAG": ["rag", "retrieval-augmented"],
        "reinforcement learning": ["reinforcement learning", "rlhf", "rl"],
        "diffusion": ["diffusion", "score-based"],
        "computer vision": ["computer vision", "vision", "image processing"],
        "multimodal": ["multimodal", "multi-modal", "vision-language"],
        "safety": ["safety", "alignment", "guardrails"],
        "alignment": ["alignment", "preference optimization", "dpo"],
        "evaluation": ["evaluation", "evaluating", "benchmark"],
        "benchmark": ["benchmark", "benchmarking"],
        "robotics": ["robotics", "robot", "embodied"],
        "graph neural network": ["graph neural network", "gnn", "gnns"],
        "optimisation": ["optimisation", "optimization", "optimizer"],
        "inference": ["inference", "decoding"],
        "serving": ["serving", "vllm", "tgi"],
        "distributed systems": ["distributed", "parallelism", "deepspeed"],
        "healthcare": ["healthcare", "medical", "clinical"],
        "finance": ["finance", "financial", "trading"],
        "education": ["education", "tutoring", "learning"],
    }

    tags = []
    for tag, keywords in topic_map.items():
        for kw in keywords:
            # Match exact word or phrase boundary
            pattern = r"\b" + re.escape(kw) + r"\b"
            if re.search(pattern, text):
                if tag not in tags:
                    tags.append(tag)
                break

    return tags if tags else ["general AI"]


def extract_complexity_signals(title: str, abstract: str, full_text: Optional[str] = None) -> ComplexitySignals:
    """Extract explicit complexity signals from title, abstract, and optional full text."""
    body = _strip_references(full_text) if full_text else ""
    text = f"{title} {abstract} {body}".lower()
    
    # Justified minimal keyword lists for complexity dimensions
    math_terms = ["theorem", "proof", "asymptotic", "convergence bound"]
    ml_terms = ["gradient descent", "backpropagation", "loss landscape", "hyperparameter"]
    systems_terms = ["throughput", "latency", "quantization", "distributed training"]
    experimental_terms = ["ablation study", "baseline comparison", "empirical validation", "statistical significance"]

    return ComplexitySignals(
        has_math_complexity=any(t in text for t in math_terms),
        has_ml_complexity=any(t in text for t in ml_terms),
        has_systems_complexity=any(t in text for t in systems_terms),
        has_experimental_complexity=any(t in text for t in experimental_terms)
    )


def estimate_difficulty(
    requirements: PaperRequirements, user_level: UserLevel
) -> DifficultyType:
    """Estimate paper difficulty based on objective requirements and user level context."""
    
    # Count how many different complexity dimensions are present
    advanced_score = sum([
        requirements.complexity_signals.has_math_complexity,
        requirements.complexity_signals.has_ml_complexity,
        requirements.complexity_signals.has_systems_complexity,
        requirements.complexity_signals.has_experimental_complexity
    ])

    if requirements.paper_type in ["theory", "systems"] or advanced_score >= 2 or requirements.complexity_signals.has_math_complexity:
        return "advanced"
    elif requirements.paper_type == "survey":
        return "beginner"
    elif requirements.paper_type in ["methods", "benchmark"] or advanced_score == 1:
        return "intermediate"
    else:
        return "intermediate" if user_level == "intermediate" else "beginner"


def identify_prerequisites(topic_tags: List[str], signals: ComplexitySignals) -> List[str]:
    """Identify recommended prerequisite concepts based on topics and complexity signals."""
    prereqs = ["Basic Python & Machine Learning concepts"]

    if "transformer" in topic_tags or "LLM" in topic_tags or "attention" in topic_tags:
        prereqs.append("Transformer Architecture & Self-Attention mechanisms")
    if "agent" in topic_tags or "tool use" in topic_tags:
        prereqs.append("Prompt Engineering & Agentic loops (ReAct pattern)")
    if "RAG" in topic_tags or "retrieval" in topic_tags:
        prereqs.append("Vector Embeddings & Similarity Search")
    if "reinforcement learning" in topic_tags or "alignment" in topic_tags:
        prereqs.append("Reinforcement Learning fundamentals & RLHF")
    if "systems" in topic_tags or signals.has_systems_complexity:
        prereqs.append("Distributed Systems & GPU Memory Optimization fundamentals")
    if "theory" in topic_tags or signals.has_math_complexity:
        prereqs.append("Multivariate Calculus, Probability Theory & Matrix Calculus")

    return list(dict.fromkeys(prereqs))  # Remove duplicates preserving order


def analyze_paper_requirements(
    title: str, abstract: str, full_text: Optional[str] = None
) -> PaperRequirements:
    """Analyze a paper and return its objective requirements."""
    paper_type = classify_paper_type(title, abstract, full_text)
    topic_tags = extract_topic_tags(title, abstract, full_text)
    signals = extract_complexity_signals(title, abstract, full_text)
    prerequisites = identify_prerequisites(topic_tags, signals)

    return PaperRequirements(
        paper_type=paper_type,
        topic_tags=topic_tags,
        complexity_signals=signals,
        prerequisites=prerequisites
    )


# Maps CompetenceLevel strings to numeric scores for gap calculation.
_COMPETENCE_SCORE: Dict[str, int] = {"none": 0, "basic": 1, "working": 2, "solid": 3}

# Human-readable labels for each complexity signal dimension.
_DIMENSION_LABELS: Dict[str, str] = {
    "math":         "Mathematics & Theory",
    "ml":           "Machine Learning & Deep Learning",
    "systems":      "Systems & Infrastructure",
    "experimental": "Research Methods & Experimentation",
}


def assess_personalised_difficulty(
    requirements: PaperRequirements, profile: UserProfile
) -> PersonalisedDifficulty:
    """Compare PaperRequirements against a UserProfile to produce a personalised difficulty.

    For each complexity dimension where the paper fires a signal, we compute
    the gap between what the paper demands (score=3) and what the user offers.
    Gaps sum to a total score used to classify difficulty.

    Gap score ranges:
      0-3  → beginner  (paper demands match or barely exceed user strengths)
      4-7  → intermediate
      8-12 → advanced  (significant missing prerequisites)
    """
    sigs = requirements.complexity_signals

    # Average the two ML sub-fields for a single ML score.
    def _ml_score() -> int:
        return (_COMPETENCE_SCORE[profile.machine_learning]
                + _COMPETENCE_SCORE[profile.deep_learning]) // 2

    # Average the two math-adjacent sub-fields.
    def _math_score() -> int:
        return (_COMPETENCE_SCORE[profile.mathematics]
                + _COMPETENCE_SCORE[profile.statistics]) // 2

    # Build a mapping from active dimensions → user score.
    active_dimensions: Dict[str, tuple[bool, int]] = {
        "math":         (sigs.has_math_complexity,         _math_score()),
        "ml":           (sigs.has_ml_complexity,           _ml_score()),
        "systems":      (sigs.has_systems_complexity,      _COMPETENCE_SCORE[profile.systems_and_infrastructure]),
        "experimental": (sigs.has_experimental_complexity, _COMPETENCE_SCORE[profile.research_experience]),
    }

    gap_score = 0
    matched_strengths: List[str] = []
    missing_prerequisites: List[str] = []

    for dim_key, (is_active, user_score) in active_dimensions.items():
        if not is_active:
            continue  # paper does not demand this dimension — skip

        label = _DIMENSION_LABELS[dim_key]
        gap = 3 - user_score          # max gap is 3 (solid fully covers demand)
        gap_score += max(gap, 0)      # never go negative

        if user_score == 0:
            missing_prerequisites.append(label)
        elif user_score >= 2:         # working or solid
            matched_strengths.append(label)
        # user_score == 1 (basic): neither a strength nor fully missing — neutral

    # Classify by total gap
    if gap_score <= 3:
        difficulty: DifficultyType = "beginner"
    elif gap_score <= 7:
        difficulty = "intermediate"
    else:
        difficulty = "advanced"

    return PersonalisedDifficulty(
        difficulty=difficulty,
        gap_score=gap_score,
        matched_strengths=matched_strengths,
        missing_prerequisites=missing_prerequisites,
    )


def recommend_decision(
    paper_type: PaperType,
    difficulty: DifficultyType,
    user_level: UserLevel,
    user_goal: Optional[str] = None,
) -> tuple[DecisionType, str]:
    """Recommend a decision (read/skim/save_for_later/skip_for_now) and provide a short public reason."""

    # Survey papers are usually great starting points
    if paper_type == "survey":
        if difficulty == "advanced" and user_level == "beginner":
            return (
                "skim",
                "This is a survey paper, but covers advanced mathematical or architectural topics. Skimming the overview is recommended for beginners.",
            )
        return (
            "read",
            "Survey papers provide an excellent high-level overview of the field and are ideal for building background context.",
        )

    # User level vs paper difficulty checks
    if user_level == "beginner":
        if difficulty == "advanced":
            return (
                "save_for_later",
                "This paper covers advanced mathematical or systems topics that require deeper prerequisites before a full read.",
            )
        elif difficulty == "intermediate":
            return (
                "skim",
                "As a beginner, skimming the introduction, figures, and conclusions will give you core insights without getting stuck on technical details.",
            )
        else:
            return (
                "read",
                "This paper is accessible and introductory, making it a great candidate for a complete read.",
            )

    elif user_level == "intermediate":
        if difficulty == "advanced":
            return (
                "skim",
                "This paper has dense advanced concepts. Skim first to evaluate specific sections relevant to your work.",
            )
        else:
            return (
                "read",
                "The methodology and complexity match an intermediate background well.",
            )

    else:  # advanced user
        return (
            "read",
            "Suitable for your advanced background; recommended for a thorough reading.",
        )


def generate_reading_path(
    paper_type: PaperType, difficulty: DifficultyType, user_level: UserLevel
) -> List[str]:
    """Generate a recommended step-by-step reading path."""
    if user_level == "beginner" or paper_type == "survey":
        return [
            "1. Abstract (Understand core problem and claims)",
            "2. Conclusion (Review key takeaways and summary of results)",
            "3. Figures & Tables (Visual intuition of architecture and results)",
            "4. Introduction (Contextual background and motivation)",
            "5. Methods & Experiments (Dive deeper only if details are needed)",
        ]
    elif difficulty == "advanced":
        return [
            "1. Abstract & Introduction (Grasp high-level problem formulation)",
            "2. Review Prerequisite Concepts (Ensure familiarity with mathematical/systems foundations)",
            "3. System Architecture / Main Theorems (Examine core theoretical contribution)",
            "4. Experiments & Ablations (Verify empirical validation)",
            "5. Related Work & Appendix (Contextual comparison and detailed proofs)",
        ]
    else:
        return [
            "1. Abstract & Introduction",
            "2. System Architecture / Methodology",
            "3. Key Experiments & Results Tables",
            "4. Conclusion & Future Work",
        ]


def create_short_summary(title: str, abstract: str) -> str:
    """Create a concise, clean summary sentence from abstract."""
    cleaned = re.sub(r"\s+", " ", abstract).strip()
    sentences = re.split(r"(?<=[.!?]) +", cleaned)
    if sentences:
        first_two = " ".join(sentences[:2])
        if len(first_two) > 250:
            return first_two[:247] + "..."
        return first_two
    return title
