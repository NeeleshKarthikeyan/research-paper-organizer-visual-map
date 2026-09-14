# Design Decisions

## 1. Deterministic Baseline First
Before integrating any LLMs, the core triage engine was built using deterministic rules. 
**Why**: This ensures the tool is fast, free to run, reproducible, and robust. It guarantees that the core application functions perfectly offline and without requiring users to manage API keys. It also creates a baseline to evaluate LLM performance against.

## 2. PaperRequirements Intermediate Representation
The analysis pipeline extracts objective demands into a `PaperRequirements` schema before making any decisions.
**Why**: It strictly separates "what the paper is" from "who is reading it." By isolating the objective demands, we can compare one paper against multiple different users without re-running the text analysis.

## 3. Separation of Paper Analysis and User Profiling
The `UserProfile` tracks human competence across 7 explicit domains (e.g., Mathematics, Systems & Infrastructure) using a 4-point scale (`none`, `basic`, `working`, `solid`).
**Why**: Early iterations used a simple "beginner/intermediate/advanced" label. However, an expert in Systems might be a beginner in Deep Learning math. By breaking the profile into domains, the system can accurately assess jagged skill profiles.

## 4. Personalised Difficulty via "Gap Scoring"
Difficulty is calculated by subtracting a user's domain competence score from the paper's domain complexity signal to find a "gap".
**Why**: Difficulty is subjective. A paper requiring advanced Math is only difficult if the reader lacks Math skills. By summing these gaps, the system generates a tailored difficulty score that explicitly identifies *why* a paper is hard (e.g., "missing prerequisites in Linear Algebra").

## 5. PDF Extraction Separation
PDF parsing (`src/pdf_parser.py`) is entirely decoupled from the analysis logic. It only extracts text and passes it to the `full_text` field in `PaperInput`.
**Why**: The analysis tools (`src/tools.py`) shouldn't care where the text came from. This allows the deterministic engine to seamlessly process arXiv abstracts, JSON dumps, or full PDFs without changing its core logic. The only specific PDF-handling logic is `_strip_references()`, which prevents lengthy bibliographies from triggering false complexity flags.

## 6. Optional LLM Integration
Google Gemini (`gemini-2.5-flash`) is integrated as an optional semantic layer, producing a `SemanticAnalysis` object.
**Why**: Relying solely on deterministic keyword matching is brittle (e.g., missing synonyms). However, making Gemini mandatory would break the offline-first design. By running Gemini side-by-side and attaching its output to `TriageOutput`, users get semantic insights when available, but the pipeline never crashes if the API fails.

## 7. Evaluation Rather Than Assuming LLM Superiority
We explicitly built an `evaluation.py` module to calculate IoU and Precision/Recall/F1 metrics between the deterministic and Gemini systems, requiring a human-curated ground truth to judge accuracy.
**Why**: It is a common anti-pattern to assume that an LLM automatically performs better than a well-tuned heuristic system. By building an evaluation framework, we require empirical proof before claiming that the semantic analysis is superior or replacing the deterministic engine entirely.
