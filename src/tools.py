"""
Deterministic rule-based helper tool functions for paper analysis and triage.
"""

import re
from typing import List, Optional, Dict
from src.schemas import DecisionType, DifficultyType, PaperType, UserLevel, ComplexitySignals


def classify_paper_type(title: str, abstract: str) -> PaperType:
    """Classify paper type based on keywords in title and abstract."""
    text = f"{title} {abstract}".lower()

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


def extract_topic_tags(title: str, abstract: str) -> List[str]:
    """Extract relevant topic tags from title and abstract text."""
    text = f"{title} {abstract}".lower()

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


def extract_complexity_signals(title: str, abstract: str) -> ComplexitySignals:
    """Extract explicit complexity signals from title and abstract text."""
    text = f"{title} {abstract}".lower()
    
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
    title: str, abstract: str, user_level: UserLevel, signals: Optional[ComplexitySignals] = None
) -> DifficultyType:
    """Estimate paper difficulty based on complexity signals and user level context."""
    text = f"{title} {abstract}".lower()
    paper_type = classify_paper_type(title, abstract)

    if signals is None:
        signals = extract_complexity_signals(title, abstract)

    # Count how many different complexity dimensions are present
    advanced_score = sum([
        signals.has_math_complexity,
        signals.has_ml_complexity,
        signals.has_systems_complexity,
        signals.has_experimental_complexity
    ])

    if paper_type in ["theory", "systems"] or advanced_score >= 2 or signals.has_math_complexity:
        return "advanced"
    elif paper_type == "survey" or "introduction" in text:
        return "beginner"
    elif paper_type in ["methods", "benchmark"] or advanced_score == 1:
        return "intermediate"
    else:
        return "intermediate" if user_level == "intermediate" else "beginner"


def identify_prerequisites(topic_tags: List[str], difficulty: DifficultyType) -> List[str]:
    """Identify recommended prerequisite concepts based on topics and difficulty."""
    prereqs = ["Basic Python & Machine Learning concepts"]

    if "transformer" in topic_tags or "LLM" in topic_tags or "attention" in topic_tags:
        prereqs.append("Transformer Architecture & Self-Attention mechanisms")
    if "agent" in topic_tags or "tool use" in topic_tags:
        prereqs.append("Prompt Engineering & Agentic loops (ReAct pattern)")
    if "RAG" in topic_tags or "retrieval" in topic_tags:
        prereqs.append("Vector Embeddings & Similarity Search")
    if "reinforcement learning" in topic_tags or "alignment" in topic_tags:
        prereqs.append("Reinforcement Learning fundamentals & RLHF")
    if "systems" in topic_tags or difficulty == "advanced":
        prereqs.append("Distributed Systems & GPU Memory Optimization fundamentals")
    if "theory" in topic_tags or difficulty == "advanced":
        prereqs.append("Multivariate Calculus, Probability Theory & Matrix Calculus")

    return list(dict.fromkeys(prereqs))  # Remove duplicates preserving order


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
