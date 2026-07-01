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

        # 2. Classify paper type
        paper_type = tools.classify_paper_type(paper.title, paper.abstract)

        # 3. Estimate difficulty
        difficulty = tools.estimate_difficulty(
            paper.title, paper.abstract, paper.user_level
        )

        # 4. Extract topic tags
        topic_tags = tools.extract_topic_tags(paper.title, paper.abstract)

        # 5. Identify prerequisite concepts
        prerequisites = tools.identify_prerequisites(topic_tags, difficulty)

        # 6. Decide recommendation and generate public explanation
        decision, reason = tools.recommend_decision(
            paper_type, difficulty, paper.user_level, paper.user_goal
        )

        # 7. Generate suggested reading path
        reading_path = tools.generate_reading_path(
            paper_type, difficulty, paper.user_level
        )

        # Create concise summary
        summary = tools.create_short_summary(paper.title, paper.abstract)

        # 8. Return structured triage report
        return TriageOutput(
            title=paper.title,
            decision=decision,
            difficulty=difficulty,
            paper_type=paper_type,
            topic_tags=topic_tags,
            prerequisites=prerequisites,
            summary=summary,
            reading_path=reading_path,
            reason=reason,
            source_url=paper.source_url,
        )

    def triage_batch(self, papers: List[PaperInput]) -> List[TriageOutput]:
        """Triage multiple papers in sequence."""
        return [self.triage_paper(paper) for paper in papers]
