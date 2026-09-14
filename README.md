# Research Paper Organizer & Visual Map

*A Kaggle 5-Day AI Agents Intensive Capstone Project*

## 1. What the Research Paper Triage Agent Does
The **Research Paper Triage Agent** is a CLI-based personal research assistant. It analyzes research papers (from arXiv, local JSON, or local PDFs) and evaluates them against your specific technical background (`UserProfile`). It then generates a personalized "read, skim, save, or skip" recommendation, complete with an explanation of *why* the paper is suitable (or demanding), alongside a tailored reading path that identifies any missing prerequisites you need to study first.

## 2. The Problem it Solves
With the explosive growth of AI/ML research, it's difficult for students and engineers to know which papers are worth their time. Reading a highly technical paper without the right prerequisites is frustrating and inefficient. This agent filters the noise by explicitly matching a paper's deterministic complexity signals against a user's self-assessed competence, ensuring you only spend time on papers you are prepared to understand.

## 3. Supported Input Methods
The agent accepts papers through three primary avenues:
- **Local JSON**: Triage a bundled set of offline papers (`--input`).
- **Live arXiv Search**: Query the arXiv API directly (`--search "LLM agents"`).
- **Local PDF**: Extract and analyze the full text of a downloaded PDF (`--pdf`).

## 4. How Deterministic Analysis Works
The core of the system is a fast, deterministic, rule-based inference engine (`src/tools.py`). It scans the paper's title, abstract, and (optionally) full text for specific keywords and phrases. It strips out the "References" section to prevent false positives, then triggers boolean complexity signals (e.g., `has_math_complexity`, `has_systems_complexity`) and extracts domain tags based on exact matches.

## 5. How PaperRequirements Works
`PaperRequirements` is an objective, intermediate representation of what the paper *demands* from any reader. It encapsulates the paper type (survey, methods, etc.), extracted topic tags, complexity signals, and a baseline list of prerequisites. Crucially, it describes the paper in isolation, entirely unaware of who will be reading it.

## 6. How UserProfile Works
`UserProfile` is the opposing side of the equation: an objective representation of what the reader *offers*. It tracks the user's self-assessed competence across 7 distinct domains (e.g., `mathematics`, `deep_learning`, `systems_and_infrastructure`). Each domain is scored as `none`, `basic`, `working`, or `solid`.

## 7. How Personalised Difficulty is Calculated
Difficulty is not an absolute trait of a paper; it is the gap between a paper's demands and a user's abilities. 
For every complexity signal fired by the `PaperRequirements`, the agent looks up the user's corresponding `UserProfile` competence score. It subtracts the user's score from the maximum demand (3) to calculate a "gap score".
- A low total gap (≤ 3) yields a **Beginner** difficulty (the paper is accessible).
- A moderate gap (4–7) yields an **Intermediate** difficulty.
- A high gap (≥ 8) yields an **Advanced** difficulty (significant missing prerequisites).

## 8. How Recommendations are Generated
Recommendations are dynamically constructed from the gap score and evidence:
- **No gap**: `Read` ("This paper is well within your abilities.")
- **Moderate gap**: `Skim`
- **High gap + at least 1 matched strength**: `Save for later` (Provides a partial foothold, but foundations are missing).
- **High gap + 0 strengths**: `Skip for now`.
The agent explicitly names the specific domains the user is missing or strong in. If prerequisites are missing, the generated reading path prepends targeted study suggestions (e.g., "Review linear algebra") before the actual paper sections.

## 9. How Optional Gemini Analysis Works
For deep semantic understanding, the agent integrates optionally with Google Gemini (`gemini-2.5-flash`). If a `GEMINI_API_KEY` is detected, the agent passes the paper metadata to Gemini, instructing it to return a structured JSON response matching the Pydantic `SemanticAnalysis` schema. This runs safely alongside the deterministic system—if the API fails or is offline, the exception is caught, and the agent falls back seamlessly to the rule-based output without crashing.

## 10. Evaluation Framework
Rather than assuming the LLM is superior, the project includes an evaluation module (`src/evaluation.py`). It calculates Intersection over Union (IoU) for topics and prerequisites between the deterministic and Gemini systems. It also provides a framework to measure Precision/Recall/F1 scores against a human-annotated `EvaluationGroundTruth` dataset, ensuring that any claims of "better performance" can be backed by hard metrics.

## 11. Repository Structure
```
research-paper-organizer-visual-map/
├── .env.example             # Template for Gemini API key setup
├── .gitignore
├── README.md
├── requirements.txt         # Python dependencies
├── src/
│   ├── main.py              # CLI entrypoint
│   ├── schemas.py           # Pydantic data models (PaperInput, PaperRequirements, UserProfile, etc.)
│   ├── triage_agent.py      # Orchestrator (pipe-and-filter workflow)
│   ├── tools.py             # Deterministic analysis engine
│   ├── arxiv_client.py      # Live arXiv API integration
│   ├── pdf_parser.py        # Local PDF text extraction (pypdf)
│   ├── llm_client.py        # Optional Gemini semantic analysis
│   ├── evaluation.py        # Deterministic vs Gemini comparison metrics
│   └── output_formatter.py  # Terminal and Markdown report formatting
├── tests/                   # Pytest unit tests (49 tests)
├── examples/                # Sample inputs and outputs
└── docs/                    # Architecture and design decision documentation
```

## 12. Installation
1. Clone the repository.
2. Create and activate a virtual environment.
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. (Optional) Copy `.env.example` to `.env` and add your Google Gemini API key to enable semantic analysis.

## 13. Usage Examples
**Triage a local JSON file (using legacy coarse user level):**
```bash
python -m src.main --input examples/sample_papers.json
```

**Triage a live arXiv search:**
```bash
python -m src.main --search "transformer agents" --max-results 3
```

**Triage a local PDF:**
```bash
python -m src.main --pdf path/to/downloaded_paper.pdf
```

**Interactive mode (no arguments):**
```bash
python -m src.main
```

**Save output to Markdown:**
```bash
python -m src.main --input examples/sample_papers.json --output report.md
```

## 14. Testing
The project includes a 49-test `pytest` suite covering schema validation, deterministic heuristics, personalised scoring, recommendation logic, API failure mocking, and evaluation metrics.
```bash
pytest -v
```

## 15. Limitations
- **Regex Brittleness**: The deterministic engine uses simple regex (e.g., to strip references). A poorly formatted PDF might leak bibliography text into the analysis.
- **Competence Averaging**: The personalised scoring averages math/stats and ML/DL competence scores, which can obscure jagged profiles (e.g., an expert in ML but a total novice in DL).
- **Evaluation Data Needed**: The evaluation framework exists, but a curated dataset of 50+ human-annotated papers is required before making objective claims about LLM superiority.
- **Gemini is Informational Only**: The `SemanticAnalysis` from Gemini is currently attached to `TriageOutput` for inspection but does not influence the triage decision or reading path. The recommendation logic relies exclusively on the deterministic system.
- **No UserProfile via CLI**: The CLI currently has no flag for providing a `UserProfile`. The personalised path is only available programmatically. Interactive profile input is a natural next step.

## 16. Future Work
- Add CLI flags or an interactive wizard for creating a `UserProfile`.
- Build a curated ground-truth dataset to properly benchmark the deterministic vs. Gemini systems.
- Optionally merge `SemanticAnalysis` insights into the deterministic `PaperRequirements` when both are available (with clear evaluation-backed justification).
- 3D Visual Mapping: Cluster papers based on extracted semantic topics and generate interactive web-based visual field maps.
- Connect to Hugging Face Papers or Semantic Scholar APIs.
