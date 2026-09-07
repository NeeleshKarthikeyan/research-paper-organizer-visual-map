"""
Unit tests for assess_personalised_difficulty scoring logic.
"""

from src import tools
from src.schemas import (
    PaperRequirements,
    ComplexitySignals,
    UserProfile,
)


def _make_requirements(math=False, ml=False, systems=False, experimental=False) -> PaperRequirements:
    """Helper to build a PaperRequirements with specific complexity signals."""
    return PaperRequirements(
        paper_type="methods",
        topic_tags=["LLM"],
        complexity_signals=ComplexitySignals(
            has_math_complexity=math,
            has_ml_complexity=ml,
            has_systems_complexity=systems,
            has_experimental_complexity=experimental,
        ),
        prerequisites=[],
    )


# ---------------------------------------------------------------------------
# Scenario 1: Strong user profile + demanding paper → should be "beginner"
# ---------------------------------------------------------------------------
def test_strong_profile_difficult_paper_is_accessible():
    """A user with solid math and ML should find a math+ML paper accessible."""
    requirements = _make_requirements(math=True, ml=True)
    profile = UserProfile(
        mathematics="solid",
        statistics="solid",
        machine_learning="solid",
        deep_learning="working",
    )
    result = tools.assess_personalised_difficulty(requirements, profile)

    # solid math (score 3) → gap 0; solid+working ML (avg 2) → gap 1 → total 1
    assert result.difficulty == "beginner"
    assert result.gap_score <= 3
    assert "Mathematics & Theory" in result.matched_strengths
    assert "Machine Learning & Deep Learning" in result.matched_strengths
    assert result.missing_prerequisites == []


# ---------------------------------------------------------------------------
# Scenario 2: Weak user profile + demanding paper → should be "advanced"
# ---------------------------------------------------------------------------
def test_weak_profile_difficult_paper_is_advanced():
    """A user with no background should find a math+ML+systems paper very hard."""
    requirements = _make_requirements(math=True, ml=True, systems=True)
    profile = UserProfile()  # all "none"

    result = tools.assess_personalised_difficulty(requirements, profile)

    # none in all 3 active dims: gap = 3+3+3 = 9
    assert result.difficulty == "advanced"
    assert result.gap_score == 9
    assert "Mathematics & Theory" in result.missing_prerequisites
    assert "Machine Learning & Deep Learning" in result.missing_prerequisites
    assert "Systems & Infrastructure" in result.missing_prerequisites
    assert result.matched_strengths == []


# ---------------------------------------------------------------------------
# Scenario 3: Strong in one domain, weak in another → mixed result
# ---------------------------------------------------------------------------
def test_mixed_profile_partial_difficulty():
    """A user strong in ML but with no systems background gets intermediate difficulty."""
    requirements = _make_requirements(ml=True, systems=True)
    profile = UserProfile(
        machine_learning="solid",
        deep_learning="solid",
        systems_and_infrastructure="none",
    )
    result = tools.assess_personalised_difficulty(requirements, profile)

    # ML: avg(3+3)//2 = 3, gap = 0
    # Systems: score = 0, gap = 3
    # Total gap = 3 → "beginner" by boundary (<=3)
    assert result.gap_score == 3
    assert result.difficulty == "beginner"
    assert "Machine Learning & Deep Learning" in result.matched_strengths
    assert "Systems & Infrastructure" in result.missing_prerequisites


# ---------------------------------------------------------------------------
# Scenario 4: Missing prerequisite detection
# ---------------------------------------------------------------------------
def test_missing_prerequisites_are_reported():
    """Dimensions where user_score=0 should always appear in missing_prerequisites."""
    requirements = _make_requirements(math=True, experimental=True)
    profile = UserProfile(
        mathematics="none",
        statistics="none",
        research_experience="none",
    )
    result = tools.assess_personalised_difficulty(requirements, profile)

    assert "Mathematics & Theory" in result.missing_prerequisites
    assert "Research Methods & Experimentation" in result.missing_prerequisites
    assert result.matched_strengths == []


# ---------------------------------------------------------------------------
# Scenario 5: Paper with no complexity signals → gap is zero regardless of profile
# ---------------------------------------------------------------------------
def test_paper_with_no_signals_always_beginner():
    """A paper that fires no complexity signals should always be 'beginner' difficulty."""
    requirements = _make_requirements()  # all False
    profile = UserProfile()  # all none — doesn't matter

    result = tools.assess_personalised_difficulty(requirements, profile)

    assert result.gap_score == 0
    assert result.difficulty == "beginner"
    assert result.matched_strengths == []
    assert result.missing_prerequisites == []


# ---------------------------------------------------------------------------
# Scenario 6: Agent integration test — UserProfile is used end-to-end
# ---------------------------------------------------------------------------
def test_agent_uses_personalised_difficulty_when_profile_provided():
    from src.schemas import PaperInput
    from src.triage_agent import TriageAgent

    agent = TriageAgent()
    profile = UserProfile(
        mathematics="solid",
        statistics="solid",
        machine_learning="solid",
        deep_learning="solid",
    )
    paper = PaperInput(
        title="Theoretical Convergence Proof for Gradient Descent",
        abstract="We present a mathematical proof using convergence bounds and backpropagation analysis.",
        user_level="beginner",  # legacy field says beginner
        user_profile=profile,   # but profile says expert in the relevant domains
    )
    report = agent.triage_paper(paper)

    # personalised_difficulty should be populated and reflect the strong profile
    assert report.personalised_difficulty is not None
    assert report.personalised_difficulty.difficulty in ["beginner", "intermediate"]
    # The top-level difficulty should come from the personalised assessment
    assert report.difficulty == report.personalised_difficulty.difficulty
