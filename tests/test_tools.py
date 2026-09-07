"""
Unit tests for deterministic rule-based analysis tools.
"""

from src import tools


def test_survey_classification():
    paper_type = tools.classify_paper_type(
        title="A Survey on Large Language Models",
        abstract="We review recent literature on LLMs.",
    )
    assert paper_type == "survey"


def test_benchmark_classification():
    paper_type = tools.classify_paper_type(
        title="AgentEval Framework",
        abstract="We present a new evaluation leaderboard and benchmark for AI agents.",
    )
    assert paper_type == "benchmark"


def test_extract_topic_tags():
    tags = tools.extract_topic_tags(
        title="Transformer Agents in RAG Systems",
        abstract="We study retrieval-augmented generation and tool use.",
    )
    assert "transformer" in tags
    assert "agent" in tags
    assert "RAG" in tags
    assert "tool use" in tags


def test_extract_complexity_signals():
    signals = tools.extract_complexity_signals(
        title="Theoretical Bounds for Gradient Descent",
        abstract="We present a mathematical proof for convergence bound in backpropagation."
    )
    assert signals.has_math_complexity is True
    assert signals.has_ml_complexity is True
    assert signals.has_systems_complexity is False
    assert signals.has_experimental_complexity is False


def test_analyze_paper_requirements():
    reqs = tools.analyze_paper_requirements(
        title="Theoretical Bounds for Gradient Descent",
        abstract="We present a mathematical proof for convergence bound in backpropagation."
    )
    assert reqs.paper_type == "theory"
    assert reqs.complexity_signals.has_math_complexity is True
    assert "Multivariate Calculus, Probability Theory & Matrix Calculus" in reqs.prerequisites

