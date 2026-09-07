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


def test_full_text_influences_analysis():
    # Only title and abstract, which don't trigger systems complexity
    title = "A New Training Approach"
    abstract = "We train models faster."
    
    reqs_no_full_text = tools.analyze_paper_requirements(title=title, abstract=abstract)
    assert reqs_no_full_text.complexity_signals.has_systems_complexity is False
    
    # Now provide full text that contains systems complexity triggers
    full_text = "We achieved this by improving throughput and latency in distributed training."
    reqs_with_full_text = tools.analyze_paper_requirements(title=title, abstract=abstract, full_text=full_text)
    assert reqs_with_full_text.complexity_signals.has_systems_complexity is True


def test_references_do_not_influence_analysis():
    title = "A Simple Guide to AI"
    abstract = "A beginner friendly guide."
    
    # Math complexity triggers in the references should be ignored
    full_text = "This is a simple guide.\n\nReferences\n1. A theorem and proof for convergence bound."
    
    reqs = tools.analyze_paper_requirements(title=title, abstract=abstract, full_text=full_text)
    
    # The math complexity should remain false because the triggers are in the references
    assert reqs.complexity_signals.has_math_complexity is False

