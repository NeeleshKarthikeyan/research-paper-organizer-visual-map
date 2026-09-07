"""
Research Paper Triage Agent orchestrating multi-step paper analysis workflow.
"""

from typing import List
from src.schemas import PaperInput, TriageOutput
from src import tools


class TriageAgent:
    """Agent that processes input papers through deterministic analysis tools

    to produce structured triage recommendation reports.
    """

    def triage_paper(self, paper: PaperInput) -> TriageOutput:
        """Execute the multi-step triage workflow for a single paper."""
        # 1. Input is already validated by Pydantic PaperInput model
        # 2. Analyze the objective requirements of the paper
        requirements = tools.analyze_paper_requirements(paper.title, paper.abstract)

        # 3. Estimate personalised difficulty
        difficulty = tools.estimate_difficulty(
            paper.title, paper.abstract, paper.user_level, signals=requirements.complexity_signals
        )

        # 4. Decide recommendation and generate public explanation
        decision, reason = tools.recommend_decision(
            requirements.paper_type, difficulty, paper.user_level, paper.user_goal
        )

        # 5. Generate suggested reading path
        reading_path = tools.generate_reading_path(
            requirements.paper_type, difficulty, paper.user_level
        )

        # Create concise summary
        summary = tools.create_short_summary(paper.title, paper.abstract)

        # 7. Return structured triage report
        return TriageOutput(
            title=paper.title,
            decision=decision,
            difficulty=difficulty,
            paper_type=requirements.paper_type,
            topic_tags=requirements.topic_tags,
            prerequisites=requirements.prerequisites,
            summary=summary,
            reading_path=reading_path,
            reason=reason,
            source_url=paper.source_url,
            complexity_signals=requirements.complexity_signals,
            paper_requirements=requirements,
        )

    def triage_batch(self, papers: List[PaperInput]) -> List[TriageOutput]:
        """Triage multiple papers in sequence."""
        return [self.triage_paper(paper) for paper in papers]
