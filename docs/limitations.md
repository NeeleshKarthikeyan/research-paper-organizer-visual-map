# Project Limitations

Honesty and transparency regarding current MVP boundaries and scope:

1. **Title & Abstract Dependency**: The current triage heuristics evaluate only paper titles and abstracts. Full body text and mathematical appendices are not analyzed.
2. **Heuristic Classification Accuracy**: Rule-based keyword matching can occasionally misclassify paper types or misjudge difficulty if an author uses non-standard terminology.
3. **Network Dependence for Live Search**: Live paper fetching via `--search` requires an active internet connection and operational availability of the public arXiv API.
4. **No PDF Parsing**: The system does not extract text directly from PDF binary files.
5. **No External Platform Integration**: Direct connections to platforms like Hugging Face Papers or Semantic Scholar are not implemented in this MVP.
6. **No Visual Mapping Yet**: Interactive 3D/2D graphical visual field maps and cluster visualizations are deferred to future releases.
7. **Static Heuristics**: Difficulty and prerequisite scoring rely on rule tables rather than adaptive personalized learning history models.
8. **Optional LLM Integration**: Advanced semantic analysis via Google Gemini is currently structured as an optional interface (`src/llm_client.py`) and requires separate API configuration.
