# Research Paper Organizer & Visual Map

*A Kaggle 5-Day AI Agents Intensive Capstone Project*

## Kaggle Capstone MVP Summary

This repository contains the **Research Paper Triage Agent**, a lightweight CLI-based MVP developed for the Kaggle 5-Day AI Agents Intensive capstone project. 

The MVP agent acts as a personal research assistant. It can process local JSON files or fetch real paper metadata from the arXiv API. Using deterministic rule-based heuristics, it analyzes titles and abstracts, extracting topics, estimating difficulty, identifying prerequisite concepts, and generating personalized "read/skim/skip" recommendations with suggested reading paths.

## Long-Term Vision

The long-term goal of this project is to become a comprehensive research paper organizer and 3D visual mapping tool. We aim to help students and early AI researchers organize papers, discover connections between subfields, and eventually visualize entire areas of the AI field in interactive cluster maps. 

**Note on MVP Scope**: The submitted MVP focuses strictly on the text-based Research Paper Triage Agent. The full 3D visual map is *not* complete yet and is planned for future work. This MVP is not currently production-ready and serves as a foundational prototype.

## Problem

With the explosive growth of AI and ML research, beginner and intermediate students often struggle to decide which papers are worth their time. Reading a highly technical paper without the right prerequisites can be demoralizing. Students need a way to filter the noise and receive contextual reading recommendations based on their experience level.

## Solution

The **Research Paper Triage Agent** solves this by evaluating a paper’s metadata (title, abstract) against a rule-based inference engine. It outputs structured, actionable triage reports that clearly state whether a student should read, skim, or save a paper for later, alongside the prerequisites needed to understand it.

## Track Recommendation

This project aligns well with the **Freestyle** or **Agents for Good** tracks (by democratizing access to complex AI research for students).

## Features

- **Local JSON Support**: Triage custom sets of offline papers.
- **Live arXiv Search**: Query the arXiv API directly from the CLI (e.g., `python -m src.main --search "LLM agents"`).
- **Interactive Mode**: Manually enter paper details via terminal prompts.
- **Rule-Based Triage Engine**: Deterministically assigns difficulty, topics, and decisions.
- **Markdown Export**: Generate beautifully formatted triage reports for sharing or documentation.
- **Zero API Cost**: The MVP is fully open-source and deterministic, requiring no paid LLM API keys.

## Agent Workflow

The triage agent follows a strict multi-step orchestration:
1. `validate input` via Pydantic schemas.
2. `classify paper type` (e.g., Survey, Benchmark, Methods).
3. `estimate difficulty` (Beginner, Intermediate, Advanced).
4. `extract topic tags` via heuristic keyword matching.
5. `identify prerequisite concepts`.
6. `decide` (Read, Skim, Save for Later, Skip for Now).
7. `generate a suggested reading path` tailored to the paper type and user level.
8. `return a structured triage report`.

## Repository Structure

```
research-paper-organizer-visual-map/
├── README.md               # Project documentation
├── requirements.txt        # Python dependencies
├── src/
│   ├── main.py             # CLI entrypoint
│   ├── schemas.py          # Pydantic data models
│   ├── triage_agent.py     # Multi-step agent workflow
│   ├── tools.py            # Rule-based heuristic functions
│   ├── arxiv_client.py     # Live arXiv API integration
│   ├── llm_client.py       # Placeholder for future LLM support
│   └── output_formatter.py # Terminal and Markdown formatting
├── examples/               # Sample inputs and outputs
├── tests/                  # Pytest unit tests
└── docs/                   # Architectural decisions and limitations
```

## How to Run

1. Clone the repository and navigate into the folder.
2. Create and activate a virtual environment.
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Run with Local Examples
Triage a bundled set of 5 diverse sample papers:
```bash
python -m src.main --input examples/sample_papers.json
```

### Run with arXiv Search
Query the arXiv API live (requires internet):
```bash
python -m src.main --search "transformer agents" --max-results 5
```

### Save Output to Markdown
Save the triage report to a Markdown file:
```bash
python -m src.main --input examples/sample_papers.json --output examples/sample_outputs.md
```

## Example Input

A typical `PaperInput` schema expects:
- Title
- Abstract
- User Level (beginner/intermediate/advanced)

*(See `examples/sample_papers.json` for full JSON examples).*

## Example Output

```text
[1] A Comprehensive Survey of Autonomous LLM Agents
--------------------------------------------------------------------------------
  * Recommendation : READ
  * Paper Type     : Survey
  * Difficulty     : Beginner
  * Topic Tags     : large language model, LLM, agent, tool use
  * Summary        : We present a detailed survey and taxonomy of autonomous...
  * Reason         : Survey papers provide an excellent high-level overview...
  * Prerequisites  :
      - Basic Python & Machine Learning concepts
      - Transformer Architecture & Self-Attention mechanisms
  * Reading Path   :
      1. Abstract
      2. Conclusion
      3. Figures & Tables
```

## Evaluation/Testing

The project includes a robust `pytest` suite testing schema validation, heuristic tool logic, end-to-end agent workflows, and mocked XML parsing for the arXiv client.
Run tests using:
```bash
pytest
```

## Limitations

- **Rule-Based Heuristics**: The agent relies on deterministic keyword rules, which can occasionally misclassify papers if unconventional terminology is used.
- **Abstract-Only**: The agent does not parse full PDF texts.
- **Live Search**: arXiv searches depend on public API availability.
- **Visual Map**: The 3D visual cluster mapping feature is not yet built.

*(See `docs/limitations.md` for a complete list).*

## Future Work

Future enhancements beyond the Kaggle intensive capstone include:
- **PDF Parsing**: Extracting insights from full-text PDFs.
- **LLM-Assisted Analysis**: Integrating Google Gemini (`src/llm_client.py`) for deep semantic understanding.
- **Platform Integrations**: Connecting to Hugging Face Papers or Semantic Scholar.
- **3D Visual Mapping**: Clustering papers and generating interactive web-based visual field maps.

---
*Note: This repository was built as a capstone project for the Kaggle 5-Day AI Agents Intensive course. The core submission is the Research Paper Triage Agent MVP.*
