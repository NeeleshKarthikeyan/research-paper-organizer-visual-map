# Project Evaluation & Testing Strategy

## Overview

The **Research Paper Triage Agent** is evaluated through automated unit tests with `pytest` and manual verification using representative sample datasets.

## Automated Test Suite Overview

| Test Module | Coverage Area | Key Verification Assertions |
|---|---|---|
| `test_schemas.py` | Data validation contracts | Validates `PaperInput` instantiation and confirms empty titles/abstracts trigger `ValidationError`. |
| `test_tools.py` | Heuristic analysis functions | Verifies paper type classification (e.g. `survey`, `benchmark`) and topic tag extraction accuracy. |
| `test_agent.py` | End-to-end agent workflow | Confirms `TriageAgent` returns valid decision types, populates prerequisites, and generates custom reading paths. |
| `test_arxiv_client.py` | XML parsing & data mapping | Tests conversion of Atom XML payloads into `PaperInput` models using offline mocked XML samples. |

## Running Evaluation Suite

To run the automated test suite locally:

```bash
pytest
```

Output highlights:
```text
tests/test_agent.py ..                                                   [ 25%]
tests/test_arxiv_client.py .                                             [ 37%]
tests/test_schemas.py ..                                                 [ 62%]
tests/test_tools.py ...                                                  [100%]
============================== 8 passed in 0.20s ==============================
```
