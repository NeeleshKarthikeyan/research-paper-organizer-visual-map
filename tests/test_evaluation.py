"""
Tests for the evaluation metrics logic.
"""

from src.evaluation import (
    _calculate_iou,
    _calculate_retrieval_metrics,
    evaluate_paper_analysis,
    EvaluationGroundTruth,
)
from src.schemas import PaperRequirements, ComplexitySignals, SemanticAnalysis


def test_calculate_iou():
    set_a = {"apple", "banana"}
    set_b = {"banana", "cherry"}
    
    iou = _calculate_iou(set_a, set_b)
    # intersection: banana (1)
    # union: apple, banana, cherry (3)
    assert iou == 1.0 / 3.0
    
    # identical sets
    assert _calculate_iou({"a"}, {"a"}) == 1.0
    
    # empty sets
    assert _calculate_iou(set(), set()) == 1.0
    
    # disjoint sets
    assert _calculate_iou({"a"}, {"b"}) == 0.0


def test_calculate_retrieval_metrics():
    predicted = {"python", "math"}
    expected = {"python", "systems"}
    
    # TP = python (1)
    # predicted = 2
    # expected = 2
    # Precision = 1/2 = 0.5
    # Recall = 1/2 = 0.5
    # F1 = 2 * (0.25) / 1.0 = 0.5
    
    metrics = _calculate_retrieval_metrics(predicted, expected)
    assert metrics.precision == 0.5
    assert metrics.recall == 0.5
    assert metrics.f1_score == 0.5
    
    # Perfect match
    metrics = _calculate_retrieval_metrics({"a"}, {"a"})
    assert metrics.precision == 1.0
    assert metrics.recall == 1.0
    assert metrics.f1_score == 1.0
    
    # Zero match
    metrics = _calculate_retrieval_metrics({"a"}, {"b"})
    assert metrics.precision == 0.0
    assert metrics.recall == 0.0
    assert metrics.f1_score == 0.0


def test_evaluate_paper_analysis_agreement_only():
    """Test when no ground truth is provided, only agreement is calculated."""
    det_reqs = PaperRequirements(
        paper_type="methods",
        topic_tags=["LLMs", "Agents"],
        complexity_signals=ComplexitySignals(has_ml_complexity=True),
        prerequisites=["Python", "Machine Learning"]
    )
    
    gemini_analysis = SemanticAnalysis(
        topics=["Agents", "LLMs"],
        prerequisites=["Machine Learning", "Python"],
        mathematical_concepts=[],
        ml_concepts=[],
        systems_concepts=[],
        evidence="Some evidence",
        estimated_complexity="intermediate"
    )
    
    result = evaluate_paper_analysis(det_reqs, gemini_analysis, actual_decision="read")
    
    # Case insensitive, order independent IOU should be 1.0
    assert result.system_agreement.topic_iou == 1.0
    assert result.system_agreement.prerequisite_iou == 1.0
    # Deterministic fallback logic in evaluation predicts intermediate for methods + 1 advanced signal
    assert result.system_agreement.complexity_match is True
    
    # Ground truth metrics should be None
    assert result.deterministic_retrieval is None
    assert result.gemini_retrieval is None
    assert result.deterministic_decision_correct is None


def test_evaluate_paper_analysis_with_ground_truth():
    """Test when ground truth is provided, retrieval metrics are calculated."""
    det_reqs = PaperRequirements(
        paper_type="methods",
        topic_tags=[],
        complexity_signals=ComplexitySignals(),
        prerequisites=["Python"]
    )
    
    ground_truth = EvaluationGroundTruth(
        paper_title="Test Paper",
        expected_prerequisites=["Python", "Math"],
        expected_decision="skim"
    )
    
    result = evaluate_paper_analysis(
        det_reqs, 
        gemini_analysis=None,  # testing missing gemini
        actual_decision="skim",
        ground_truth=ground_truth
    )
    
    assert result.paper_title == "Test Paper"
    
    # Agreement should be 0 since Gemini is missing
    assert result.system_agreement.topic_iou == 0.0
    
    # Retrieval for deterministic
    assert result.deterministic_retrieval is not None
    # TP: Python (1). Pred: 1. Expected: 2.
    assert result.deterministic_retrieval.precision == 1.0
    assert result.deterministic_retrieval.recall == 0.5
    
    assert result.gemini_retrieval is None
    assert result.deterministic_decision_correct is True
