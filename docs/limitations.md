# Project Limitations

Honesty and transparency regarding current MVP boundaries and scope:

## Known Limitations

1. **Regex Brittleness**: The deterministic engine uses simple regex (e.g., to strip references). A poorly formatted PDF might leak bibliography text into the analysis, triggering false complexity signals.
2. **Competence Averaging**: The personalised scoring averages math/stats and ML/DL competence scores, which can obscure jagged profiles (e.g., an expert in ML but a total novice in DL).
3. **Evaluation Data Needed**: The evaluation framework exists and calculates theoretical metrics (IoU, P/R/F1), but a curated dataset of 50+ human-annotated papers is required before making objective claims about LLM superiority.
4. **Gemini is Informational Only**: The `SemanticAnalysis` from Gemini is currently attached to `TriageOutput` for inspection but does not influence the triage decision or reading path. The recommendation logic relies exclusively on the deterministic system.
5. **No Interactive UserProfile via CLI**: The CLI allows loading a `UserProfile` from a JSON file (`--profile`), but does not currently feature an interactive wizard for constructing one dynamically.

## Future Work

1. Build a curated ground-truth dataset to properly benchmark the deterministic vs. Gemini systems.
2. Optionally merge `SemanticAnalysis` insights into the deterministic `PaperRequirements` when both are available (with clear evaluation-backed justification).
3. 3D Visual Mapping: Interactive 3D/2D graphical visual field maps and cluster visualizations are deferred to future releases.
4. External Platform Integration: Direct connections to platforms like Hugging Face Papers or Semantic Scholar.
