# Natural Language to SQL (NL2SQL)

A production-style application that converts plain English questions into SQL queries and executes them against real databases : no SQL knowledge required.

**Live Demo:** [Link here]

---

## Problem Statement

Non-technical users often need insights from databases but lack SQL knowledge. This app bridges that gap by allowing users to type questions in plain English and get answers instantly, with the generated SQL query visible for transparency.

---

## Architecture

```
User Question
     ↓
Embed Question (FastEmbed - BAAI/bge-small-en-v1.5)
     ↓
FAISS Vector Search → Retrieve Most Similar Database Schema
     ↓
Inject Schema + Question into Prompt
     ↓
LLM Generates SQL (Groq - LLaMA 3.3 70B)
     ↓
Execute SQL against SQLite Database
     ↓
Return Results to User
```

---

## Key Decisions

**Prompt Engineering over Fine-tuning**
Modern LLMs already have strong SQL knowledge. The real challenge is schema understanding - injecting the right context into the prompt solves this without the compute overhead of fine-tuning.

**FAISS for Schema Retrieval**
Spider benchmark has 200+ databases. Rather than using labels to pick the right schema, FAISS vector search is used to find the most semantically similar database - making the system generalisable to unseen questions.

**Schema Text Formatting**
Column and table names in Spider contain spaces which cause SQLite errors. These are normalised to underscores during index building. Schema is structured as `table: X, columns: Y` for unambiguous LLM parsing.

**Groq API (LLaMA 3.3 70B)**
Chosen for free tier availability, low latency, and strong SQL generation capability - consistent with existing portfolio stack.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| Backend | FastAPI |
| LLM | Groq API (LLaMA 3.3 70B) |
| Embeddings | FastEmbed (BAAI/bge-small-en-v1.5) |
| Vector Search | FAISS |
| Database | SQLite (Spider Benchmark) |

---

## Implementation Details

- `src/schema_retriever.py` — builds FAISS index from Spider schemas at startup, retrieves most similar schema for each query
- `src/prompt_builder.py` — constructs structured prompt and calls Groq API
- `src/sql_executor.py` — executes generated SQL against the correct SQLite database
- `main.py` — FastAPI backend with lifespan startup hook
- `app.py` — Streamlit frontend

---

## How to Run Locally

1. Clone the repository
2. Download the Spider dataset from https://yale-lily.github.io/spider and place `tables.json`, `train_spider.json`, and `database/` folder in the project root
3. Create a virtual environment and install dependencies:
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```
4. Create a `.env` file with your Groq API key:
```
GROQ_API_KEY=your_key_here
```

5. Start the FastAPI backend:
```bash
uvicorn main:app --reload
```
6. In a new terminal, start the Streamlit frontend:
```bash
streamlit run app.py
```

---

## Limitations & Future Enhancements

- **Out-of-domain detection** — the system attempts SQL generation even for unrelated questions. A classifier to detect invalid queries would improve robustness.
- **Multi-turn conversations** — currently stateless, each question is independent. Conversation history could enable follow-up questions.
- **Schema retrieval accuracy** — FAISS retrieval may fail for ambiguous questions. Re-ranking or hybrid search could improve this.
- **Deployment** — Currently runs locally; cloud deployment pending due to large dataset size (838MB SQLite files). Full source code available on GitHub.

---

## Author

Prasanna D | B.Tech, IIT Gandhinagar (2022) |\
Incoming MS Applied Machine Learning, University of Maryland College Park (Fall 2026)
