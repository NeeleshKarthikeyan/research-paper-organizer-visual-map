"""
Tests for the personalised recommendation and reading path logic.
"""

from src import tools
from src.schemas import PaperRequirements, ComplexitySignals, UserProfile, PersonalisedDifficulty


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_pd(gap_score: int, matched: list, missing: list) -> PersonalisedDifficulty:
    """Build a PersonalisedDifficulty directly for unit testing the recommend logic."""
    if gap_score <= 3:
        difficulty = "beginner"
    elif gap_score <= 7:
        difficulty = "intermediate"
    else:
        difficulty = "advanced"
    return PersonalisedDifficulty(
        difficulty=difficulty,
        gap_score=gap_score,
        matched_strengths=matched,
        missing_prerequisites=missing,
    )


def _make_requirements(paper_type="methods", math=False, ml=False, systems=False, experimental=False):
    return PaperRequirements(
        paper_type=paper_type,
        topic_tags=[],
        complexity_signals=ComplexitySignals(
            has_math_complexity=math,
            has_ml_complexity=ml,
            has_systems_complexity=systems,
            has_experimental_complexity=experimental,
        ),
        prerequisites=[],
    )


# ---------------------------------------------------------------------------
# Decision tests
# ---------------------------------------------------------------------------

def test_strong_user_gets_read():
    """Gap score ≤ 1 → 'read'."""
    pd = _make_pd(gap_score=0, matched=["Machine Learning & Deep Learning"], missing=[])
    decision, reason = tools.recommend_with_profile("methods", pd)
    assert decision == "read"
    assert "well within" in reason


def test_moderate_gap_gets_skim():
    """Intermediate difficulty (gap 4-7) → 'skim'."""
    pd = _make_pd(gap_score=5, matched=["Machine Learning & Deep Learning"],
                  missing=["Mathematics & Theory"])
    decision, reason = tools.recommend_with_profile("methods", pd)
    assert decision == "skim"


def test_high_gap_with_strengths_gets_save_for_later():
    """Advanced difficulty with at least one matched strength → 'save_for_later'."""
    pd = _make_pd(gap_score=9, matched=["Machine Learning & Deep Learning"],
                  missing=["Mathematics & Theory", "Systems & Infrastructure"])
    decision, reason = tools.recommend_with_profile("methods", pd)
    assert decision == "save_for_later"


def test_high_gap_no_strengths_gets_skip_for_now():
    """Advanced difficulty with no matched strengths → 'skip_for_now'."""
    pd = _make_pd(gap_score=12, matched=[], missing=[
        "Mathematics & Theory", "Machine Learning & Deep Learning", "Systems & Infrastructure"
    ])
    decision, reason = tools.recommend_with_profile("methods", pd)
    assert decision == "skip_for_now"


def test_survey_always_gets_read():
    """Survey papers always get 'read' regardless of gap score."""
    pd = _make_pd(gap_score=9, matched=[], missing=["Mathematics & Theory"])
    decision, reason = tools.recommend_with_profile("survey", pd)
    assert decision == "read"


# ---------------------------------------------------------------------------
# Reason content tests
# ---------------------------------------------------------------------------

def test_reason_mentions_missing_domain():
    """If Mathematics & Theory is missing, the reason should name it."""
    pd = _make_pd(gap_score=5, matched=[], missing=["Mathematics & Theory"])
    _, reason = tools.recommend_with_profile("methods", pd)
    assert "Mathematics & Theory" in reason


def test_reason_mentions_matched_strength():
    """If a strength exists, the reason should reference it."""
    pd = _make_pd(gap_score=2, matched=["Machine Learning & Deep Learning"], missing=[])
    _, reason = tools.recommend_with_profile("methods", pd)
    assert "Machine Learning & Deep Learning" in reason


def test_reason_no_fabricated_content_when_no_signals():
    """When there are no missing or matched areas, the reason should be plain."""
    pd = _make_pd(gap_score=0, matched=[], missing=[])
    _, reason = tools.recommend_with_profile("methods", pd)
    # Should not mention any domain names
    assert "Mathematics" not in reason
    assert "Machine Learning" not in reason


# ---------------------------------------------------------------------------
# Determinism test
# ---------------------------------------------------------------------------

def test_recommendation_is_deterministic():
    """Calling recommend_with_profile twice with the same inputs must produce identical results."""
    pd = _make_pd(gap_score=6, matched=["Systems & Infrastructure"], missing=["Mathematics & Theory"])
    result_1 = tools.recommend_with_profile("methods", pd)
    result_2 = tools.recommend_with_profile("methods", pd)
    assert result_1 == result_2


# ---------------------------------------------------------------------------
# Reading path tests
# ---------------------------------------------------------------------------

def test_reading_path_prepends_prereq_steps_for_missing_domains():
    """Missing prerequisites must appear as numbered [Prerequisite] steps first."""
    pd = _make_pd(gap_score=9, matched=[], missing=["Mathematics & Theory"])
    path = tools.generate_reading_path_with_profile("methods", pd)
    assert path[0].startswith("1. [Prerequisite]")
    assert "linear algebra" in path[0] or "calculus" in path[0]


def test_reading_path_no_prereq_steps_when_no_gaps():
    """No prerequisites missing → path starts directly with paper reading steps."""
    pd = _make_pd(gap_score=0, matched=["Machine Learning & Deep Learning"], missing=[])
    path = tools.generate_reading_path_with_profile("methods", pd)
    assert not any("[Prerequisite]" in step for step in path)


def test_reading_path_is_non_empty():
    """Reading path must always contain at least one step."""
    pd = _make_pd(gap_score=0, matched=[], missing=[])
    path = tools.generate_reading_path_with_profile("survey", pd)
    assert len(path) > 0


def test_reading_path_multiple_missing_prereqs_numbered_correctly():
    """Two missing prereqs → steps 1 and 2 are prerequisites, step 3 starts paper."""
    pd = _make_pd(gap_score=12, matched=[], missing=[
        "Mathematics & Theory", "Systems & Infrastructure"
    ])
    path = tools.generate_reading_path_with_profile("methods", pd)
    assert path[0].startswith("1. [Prerequisite]")
    assert path[1].startswith("2. [Prerequisite]")
    assert path[2].startswith("3.")  # first paper step
    assert "[Prerequisite]" not in path[2]


# ---------------------------------------------------------------------------
# Agent integration test
# ---------------------------------------------------------------------------

def test_agent_uses_personalised_reason_with_profile():
    """When a UserProfile is provided, the reason should reference actual gaps."""
    from src.schemas import PaperInput
    from src.triage_agent import TriageAgent

    agent = TriageAgent()
    # Paper with math complexity, user with zero math background
    profile = UserProfile(
        mathematics="none",
        statistics="none",
        machine_learning="working",
        deep_learning="working",
    )
    paper = PaperInput(
        title="Theoretical Convergence Proof for Gradient Descent",
        abstract="We present a mathematical proof using convergence bounds and backpropagation analysis.",
        user_level="intermediate",
        user_profile=profile,
    )
    report = agent.triage_paper(paper)

    # The reason must mention the math gap specifically
    assert "Mathematics" in report.reason or "mathematics" in report.reason.lower()
    # The reading path must contain a prerequisite review step
    assert any("[Prerequisite]" in step for step in report.reading_path)
