# Research Paper Organizer & Visual Map

> **Kaggle 5-Day AI Agents Intensive Capstone Project**
>
> A modular AI-powered Research Paper Triage Agent that helps students and researchers discover, prioritise, and organise research papers while laying the foundations for an intelligent research knowledge management system.

---

## Overview

Keeping up with Artificial Intelligence research has become increasingly difficult. Thousands of papers are published every month across repositories such as arXiv, making it challenging to determine:

- Which papers are worth reading
- Which papers are too advanced
- What prerequisite knowledge is required
- Where to begin learning a new topic
- How individual papers fit into the wider AI landscape

This project addresses the first stage of that problem by building a **Research Paper Triage Agent**.

Instead of simply searching for papers, the agent analyses each paper and recommends whether the user should:

- 📖 Read
- 👀 Skim
- ⏳ Save for Later
- ❌ Skip for Now

The long-term goal is to evolve this project into a complete AI-powered research assistant capable of organising papers into an interactive visual knowledge graph.

---

# Project Goals

The long-term vision is to build a platform that can:

- Search multiple research repositories
- Automatically organise papers into collections
- Classify papers by topic and type
- Estimate reading difficulty
- Recommend prerequisite material
- Build personalised reading pathways
- Generate AI-assisted summaries
- Create an interactive visual map of AI research

This submission focuses on the **Minimum Viable Product (MVP): the Research Paper Triage Agent**.

---

# Features

Current MVP features include:

- Search arXiv using the official API
- Analyse papers from local JSON files
- Validate paper metadata using Pydantic schemas
- Classify paper type
- Estimate reading difficulty
- Extract topic tags
- Identify prerequisite concepts
- Recommend whether to Read, Skim, Save for Later or Skip
- Generate structured reading pathways
- Export results as Markdown
- Unit tested with PyTest

---

# Example Workflow

```text
                Search Query
                      │
                      ▼
            Official arXiv API
                      │
                      ▼
              Paper Metadata
                      │
                      ▼
             Schema Validation
                      │
                      ▼
         Research Paper Triage Agent
                      │
      ┌───────────────┼───────────────┐
      ▼               ▼               ▼
 Classification   Difficulty     Topic Tags
      │               │               │
      └───────────────┼───────────────┘
                      ▼
        Recommendation Generation
                      │
                      ▼
             Structured Report
```

---

# Repository Structure

```
research-paper-organizer-visual-map/

├── src/
│   ├── main.py
│   ├── schemas.py
│   ├── triage_agent.py
│   ├── tools.py
│   ├── arxiv_client.py
│   ├── output_formatter.py
│   └── llm_client.py
│
├── examples/
│   ├── sample_papers.json
│   └── sample_outputs.md
│
├── tests/
│
├── docs/
│
├── screenshots/
│
├── README.md
├── requirements.txt
├── .gitignore
└── .env.example
```

---

# Usage

## Analyse local example papers

```bash
python -m src.main --input examples/sample_papers.json
```

---

## Search arXiv

Example:

```bash
python -m src.main --search "LLM agents"
```

Specify the number of papers

```bash
python -m src.main --search "world models" --max-results 10
```

---

## Export results

```bash
python -m src.main --input examples/sample_papers.json --output examples/sample_outputs.md
```

---

# Example Output

```text
Title:
Survey of Large Language Model Agents

Decision:
READ

Difficulty:
Intermediate

Paper Type:
Survey

Topic Tags:
LLMs
Agents
Planning

Prerequisites:
Python
Transformers
Prompt Engineering

Reason:
Excellent overview paper suitable for users entering the field.
```

---

# Testing

Run the test suite

```bash
pytest
```

---

# Technologies Used

- Python
- Pydantic
- Requests
- PyTest
- Official arXiv API

---

# Design Philosophy

The project follows a modular architecture.

Rather than placing all logic into a single script, responsibilities are separated into independent modules:

- Data retrieval
- Schema validation
- Paper classification
- Recommendation generation
- Output formatting

This makes the project easier to maintain and allows future AI models or additional paper repositories to be integrated without major architectural changes.

---

# Current Limitations

The MVP currently:

- Uses paper metadata (primarily title and abstract)
- Uses deterministic rule-based classification
- Does not yet analyse full PDFs
- Does not yet build the planned visual knowledge graph
- Does not yet generate AI-powered semantic summaries

These limitations are intentional in order to create a reliable and easily testable MVP.

---

# Future Work

Planned features include:

- Full PDF parsing
- Semantic paper embeddings
- Vector search
- Personal paper libraries
- Reading history
- Automatic note generation
- Citation graph visualisation
- Interactive knowledge maps
- Multi-agent paper analysis
- Optional Gemini integration
- Hugging Face paper support
- Semantic clustering of research topics

---

# Why I Built This

As an Applied AI student, I quickly discovered that keeping up with research is one of the biggest challenges when learning modern AI.

This project began as an attempt to solve a personal problem:

> *How can students discover the right papers to read without becoming overwhelmed by the sheer volume of research being published?*

The Research Paper Triage Agent is the first step towards answering that question.

---

# Kaggle Capstone

This repository was developed as my submission for the **Kaggle 5-Day AI Agents Intensive Capstone Project**.

The submitted MVP demonstrates:

- Agent-oriented software architecture
- Real-time retrieval of research papers using the official arXiv API
- Automated paper triage
- Structured recommendations
- Modular, extensible design suitable for future AI-powered enhancements

---

# License

This project is released under the MIT License.

