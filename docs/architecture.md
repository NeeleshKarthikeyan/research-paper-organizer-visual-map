# Architecture Documentation

## Overview

The **Research Paper Triage Agent** is designed as a modular, pipe-and-filter CLI architecture. It processes raw research paper metadata (either from local JSON storage or live via the arXiv API) through validated data schemas, deterministic tool functions, and a central orchestration agent to produce structured triage reports.

## Component Workflow

```
   [ Local JSON File ]  OR  [ arXiv API Query ]
             │                       │
             └───────────┬───────────┘
                         ▼
           [ PaperInput Schema Validation ]
                         │
                         ▼
                 [ TriageAgent ]
                         │
        ┌────────────────┼────────────────┐
        ▼                ▼                ▼
[ classify_paper_type ] [ extract_topics ] [ estimate_difficulty ]
        │                │                │
        └────────────────┼────────────────┘
                         ▼
         [ identify_prerequisites ]
                         │
                         ▼
           [ recommend_decision & path ]
                         │
                         ▼
           [ TriageOutput Structured Model ]
                         │
             ┌───────────┴───────────┐
             ▼                       ▼
    [ Terminal Formatter ]   [ Markdown Exporter ]
```

## Detailed Module Roles

1. **`src/schemas.py`**: Utilizes Pydantic to enforce data contracts for both input metadata (`PaperInput`) and generated triage reports (`TriageOutput`).
2. **`src/arxiv_client.py`**: Encapsulates external API interaction with `export.arxiv.org`. Fetches XML feeds and converts entry metadata into standardized `PaperInput` objects.
3. **`src/tools.py`**: Pure, deterministic functional tools implementing rules for classification, difficulty estimation, topic tag extraction, prerequisite matching, and reading path generation.
4. **`src/triage_agent.py`**: Orchestrates the multi-step analysis sequence across tools for individual papers or batches.
5. **`src/output_formatter.py`**: Transforms structured `TriageOutput` models into readable ANSI terminal blocks or clean Markdown files.
6. **`src/llm_client.py`**: Provides a stub interface for optional future Gemini LLM expansion without adding runtime dependencies for the core MVP.
