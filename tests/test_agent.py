"""
Unit tests for the TriageAgent workflow.
"""

from src.schemas import PaperInput
from src.triage_agent import TriageAgent


def test_agent_returns_valid_decision():
    agent = TriageAgent()
    paper = PaperInput(
        title="Introductory Guide to Neural Networks",
        abstract="A clear survey and introduction to foundational deep learning concepts.",
        user_level="beginner",
    )
    report = agent.triage_paper(paper)

    assert report.title == paper.title
    assert report.decision in ["read", "skim", "save_for_later", "skip_for_now"]
    assert report.paper_type == "survey"


def test_beginner_receives_prerequisites_and_reading_path():
    agent = TriageAgent()
    paper = PaperInput(
        title="Advanced Distributed Transformer Serving",
        abstract="We optimize throughput latency and inference scaling across large clusters.",
        user_level="beginner",
    )
    report = agent.triage_paper(paper)

    assert len(report.prerequisites) > 0
    assert len(report.reading_path) > 0
    assert report.decision == "save_for_later"
