# Architecture

The Research Paper Triage Agent uses a "pipe-and-filter" architecture orchestrating deterministic heuristics and optional LLM semantic analysis.

## Core Flow
1. **Input Generation**: A `PaperInput` object is created via the CLI (`src/main.py`) using arXiv metadata (`src/arxiv_client.py`), a local JSON file, or local PDF extraction (`src/pdf_parser.py`).
2. **Validation**: Pydantic strictly validates the `PaperInput` schema.
3. **Objective Analysis (Deterministic)**: `src/tools.py` evaluates the paper's text to determine its objective demands, creating a `PaperRequirements` object.
4. **Semantic Analysis (Optional LLM)**: `src/llm_client.py` optionally queries Google Gemini to produce a `SemanticAnalysis` object. If the API key is missing or the call fails, the pipeline safely ignores it.
5. **Personalised Scoring**: The objective `PaperRequirements` are compared against the reader's `UserProfile` (if provided) to calculate a "gap score", yielding a `PersonalisedDifficulty`.
6. **Recommendation Generation**: Using the gap score, `src/tools.py` generates a tailored decision (Read/Skim/Save/Skip), a dynamic reason string highlighting missing prerequisites, and a customized reading path.
7. **Output**: The aggregated data is wrapped in a `TriageOutput` object and formatted for the terminal or exported as Markdown (`src/output_formatter.py`).

## Component Responsibilities

- **`main.py`**: CLI entrypoint; handles argument parsing and orchestration initialization.
- **`schemas.py`**: The single source of truth for data structures (Pydantic models). Defines the boundaries between system components.
- **`tools.py`**: The deterministic "brain". Contains all heuristic keyword matching, complexity scoring, and dynamic text generation for recommendations.
- **`triage_agent.py`**: The orchestrator. Moves data through the pipeline steps from Input -> Analysis -> Scoring -> Output.
- **`pdf_parser.py`**: Extracts raw text from local PDF files using `pypdf`.
- **`arxiv_client.py`**: Fetches and parses XML metadata from the public arXiv API.
- **`llm_client.py`**: Securely interfaces with Google Gemini, enforcing structured JSON output via Pydantic.
- **`evaluation.py`**: Calculates Intersection over Union (IoU) and Retrieval metrics (Precision/Recall/F1) to benchmark deterministic vs. Gemini performance.
- **`output_formatter.py`**: Formats `TriageOutput` objects for terminal display and Markdown export.
