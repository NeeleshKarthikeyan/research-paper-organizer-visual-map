# Technical Design Decisions

## 1. Deterministic Rule-Based Logic First
**Decision**: Rely primarily on deterministic rule-based algorithms (keyword extraction, pattern matching heuristics) for paper classification and triage recommendations.
**Rationale**: 
- Ensures zero API cost and removes dependency on external LLM availability or API keys.
- Guaranteed reproducible, instant execution suitable for offline local runs.
- Provides predictable behavior for testing and evaluation during the Kaggle intensive capstone.

## 2. Pydantic Schemas for Strict Data Contracts
**Decision**: Enforce input and output structures using Pydantic models.
**Rationale**:
- Eliminates silent failures from missing metadata or malformed input JSON.
- Provides automatic data type coercion and verification.
- Makes the code easily extensible for future API or database persistence layers.

## 3. Real-World API Integration via arXiv
**Decision**: Implement live arXiv search capability (`src/arxiv_client.py`) alongside local JSON loading.
**Rationale**:
- Demonstrates real-world utility beyond static sandbox datasets.
- Allows students to immediately query active AI subfields (e.g., `"LLM agents"`, `"RAG"`) and get instant recommendations on newly published papers.

## 4. Deferring Full PDF Parsing & 3D Mapping to Future Work
**Decision**: Scope the Capstone MVP strictly to paper triage using titles and abstracts, deferring PDF parsing and 3D visual field maps.
**Rationale**:
- Adheres to standard MVP practices by focusing on solving the core user pain point: *deciding what to read next*.
- PDF parsing introduces significant noise and library overhead, while 3D visualization requires front-end rendering frameworks better suited for post-capstone expansion.

## 5. Extensibility for LLM Enhancements (`src/llm_client.py`)
**Decision**: Include an optional, non-blocking placeholder module for Google Gemini integration.
**Rationale**:
- Demonstrates clean software engineering practices by separating core logic from AI model integration.
- Enables seamless upgrading to LLM-driven synthesis when a `GOOGLE_API_KEY` is present, without breaking offline functionality.
