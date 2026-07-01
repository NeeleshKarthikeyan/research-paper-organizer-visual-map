"""
CLI entrypoint for the Research Paper Triage Agent.
"""

import argparse
import json
import os
import sys
from typing import List

from src.schemas import PaperInput
from src.triage_agent import TriageAgent
from src.arxiv_client import fetch_arxiv_papers
from src.output_formatter import format_terminal_output, format_markdown_output


def load_papers_from_json(filepath: str) -> List[PaperInput]:
    """Load and validate papers from a local JSON file."""
    if not os.path.exists(filepath):
        print(f"Error: Input file '{filepath}' does not exist.", file=sys.stderr)
        sys.exit(1)

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        if isinstance(data, dict):
            data = [data]

        papers = [PaperInput(**item) for item in data]
        return papers
    except Exception as e:
        print(f"Error reading or parsing JSON file '{filepath}': {e}", file=sys.stderr)
        sys.exit(1)


def run_interactive_mode() -> List[PaperInput]:
    """Prompt user interactively for paper details."""
    print("\n--- Interactive Paper Triage Mode ---")
    title = input("Enter paper title: ").strip()
    abstract = input("Enter paper abstract/summary: ").strip()
    user_level = (
        input("Enter your experience level (beginner/intermediate/advanced) [beginner]: ")
        .strip()
        .lower()
    )
    if user_level not in ["beginner", "intermediate", "advanced"]:
        user_level = "beginner"

    user_goal = input("Enter your learning goal (optional): ").strip() or None

    return [
        PaperInput(
            title=title or "Untitled Paper",
            abstract=abstract or "No abstract provided.",
            user_level=user_level,  # type: ignore
            user_goal=user_goal,
            source="interactive",
        )
    ]


def main():
    parser = argparse.ArgumentParser(
        description="Research Paper Triage Agent - Kaggle AI Agents Capstone MVP"
    )
    parser.add_argument(
        "--input",
        "-i",
        type=str,
        help="Path to local JSON file containing paper metadata.",
    )
    parser.add_argument(
        "--search",
        "-s",
        type=str,
        help="Search query to fetch live papers from arXiv.",
    )
    parser.add_argument(
        "--max-results",
        "-m",
        type=int,
        default=5,
        help="Maximum results to fetch when searching arXiv (default: 5).",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        help="Optional path to save triage report as Markdown file.",
    )

    args = parser.parse_args()

    papers: List[PaperInput] = []

    if args.input:
        print(f"\n[Info] Loading papers from local file: {args.input}")
        papers = load_papers_from_json(args.input)
    elif args.search:
        print(f"\n[Info] Querying arXiv API for: '{args.search}' (max {args.max_results} results)...")
        papers = fetch_arxiv_papers(args.search, max_results=args.max_results)
        if not papers:
            print("No papers found or error fetching from arXiv.")
            sys.exit(0)
    else:
        papers = run_interactive_mode()

    agent = TriageAgent()
    results = agent.triage_batch(papers)

    # Print clean terminal output
    terminal_report = format_terminal_output(results)
    print("\n" + terminal_report)

    # Save Markdown output if requested
    if args.output:
        md_report = format_markdown_output(results)
        os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(md_report)
        print(f"\n[Success] Markdown report saved to: {args.output}")


if __name__ == "__main__":
    main()