"""
Evaluation framework for comparing deterministic and semantic paper analysis.
"""

from typing import List, Optional, Set
from pydantic import BaseModel
from src.schemas import DecisionType, PaperRequirements, SemanticAnalysis


class EvaluationGroundTruth(BaseModel):
    """Template for human-annotated reference data."""
    paper_title: str
    expected_prerequisites: List[str]
    expected_decision: DecisionType
    # This ground truth is only valid relative to a specific user profile
    # which should be tracked in the dataset this belongs to.


class SystemAgreementMetrics(BaseModel):
    """Metrics comparing deterministic output vs Gemini output."""
    prerequisite_iou: float  # Intersection over Union of prerequisites
    topic_iou: float         # Intersection over Union of topics
    complexity_match: bool   # Did they estimate the same difficulty?


class RetrievalMetrics(BaseModel):
    """Standard precision/recall metrics against a ground truth."""
    precision: float
    recall: float
    f1_score: float


class EvaluationResult(BaseModel):
    """Comprehensive evaluation record for a single paper run."""
    paper_title: str
    system_agreement: SystemAgreementMetrics
    deterministic_retrieval: Optional[RetrievalMetrics] = None
    gemini_retrieval: Optional[RetrievalMetrics] = None
    deterministic_decision_correct: Optional[bool] = None


def _calculate_iou(set_a: Set[str], set_b: Set[str]) -> float:
    """Calculate Intersection over Union for two sets of strings."""
    if not set_a and not set_b:
        return 1.0  # Both agreed there was nothing
    
    intersection = len(set_a.intersection(set_b))
    union = len(set_a.union(set_b))
    return intersection / union


def _calculate_retrieval_metrics(predicted: Set[str], expected: Set[str]) -> RetrievalMetrics:
    """Calculate Precision, Recall, and F1-score."""
    if not expected and not predicted:
        return RetrievalMetrics(precision=1.0, recall=1.0, f1_score=1.0)
    if not expected or not predicted:
        return RetrievalMetrics(precision=0.0, recall=0.0, f1_score=0.0)

    true_positives = len(predicted.intersection(expected))
    
    precision = true_positives / len(predicted)
    recall = true_positives / len(expected)
    
    if precision + recall == 0:
        f1 = 0.0
    else:
        f1 = 2 * (precision * recall) / (precision + recall)
        
    return RetrievalMetrics(precision=precision, recall=recall, f1_score=f1)


def evaluate_paper_analysis(
    deterministic_reqs: PaperRequirements,
    gemini_analysis: Optional[SemanticAnalysis],
    actual_decision: DecisionType,
    ground_truth: Optional[EvaluationGroundTruth] = None,
) -> EvaluationResult:
    """Compare outputs and calculate metrics against optional ground truth."""
    
    # Calculate System Agreement
    if gemini_analysis is None:
        # Cannot compute agreement if Gemini failed or wasn't run
        agreement = SystemAgreementMetrics(
            prerequisite_iou=0.0,
            topic_iou=0.0,
            complexity_match=False
        )
    else:
        det_prereqs = {p.lower().strip() for p in deterministic_reqs.prerequisites}
        gem_prereqs = {p.lower().strip() for p in gemini_analysis.prerequisites}
        
        det_topics = {t.lower().strip() for t in deterministic_reqs.topic_tags}
        gem_topics = {t.lower().strip() for t in gemini_analysis.topics}
        
        from src.tools import estimate_difficulty
        # Determine deterministic complexity equivalent
        det_complexity = estimate_difficulty(deterministic_reqs, "beginner")

        agreement = SystemAgreementMetrics(
            prerequisite_iou=_calculate_iou(det_prereqs, gem_prereqs),
            topic_iou=_calculate_iou(det_topics, gem_topics),
            complexity_match=(det_complexity == gemini_analysis.estimated_complexity)
        )

    # Calculate Ground Truth Metrics
    det_retrieval = None
    gem_retrieval = None
    decision_correct = None
    
    if ground_truth is not None:
        expected_prereqs = {p.lower().strip() for p in ground_truth.expected_prerequisites}
        
        det_prereqs = {p.lower().strip() for p in deterministic_reqs.prerequisites}
        det_retrieval = _calculate_retrieval_metrics(det_prereqs, expected_prereqs)
        
        if gemini_analysis is not None:
            gem_prereqs = {p.lower().strip() for p in gemini_analysis.prerequisites}
            gem_retrieval = _calculate_retrieval_metrics(gem_prereqs, expected_prereqs)
            
        decision_correct = (actual_decision == ground_truth.expected_decision)

    return EvaluationResult(
        paper_title=ground_truth.paper_title if ground_truth else "Unknown",
        system_agreement=agreement,
        deterministic_retrieval=det_retrieval,
        gemini_retrieval=gem_retrieval,
        deterministic_decision_correct=decision_correct,
    )
