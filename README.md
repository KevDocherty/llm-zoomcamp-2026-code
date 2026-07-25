# LLM Zoomcamp 2026 — Module 1

A learning workspace for Module 1 of the 2026 LLM Zoomcamp. The repository builds a retrieval-augmented generation (RAG) assistant over the DataTalks.Club FAQ data, starting with direct model calls and an in-memory text index, then progressing to persistent SQLite and Elasticsearch indexes and an agentic retrieval workflow.

The notebooks are intentionally incremental: [`notebook.ipynb`](notebook.ipynb) records the detailed learning path, while the smaller notebooks and Python modules isolate reusable parts of the pipeline.

## What the project demonstrates

- Loading and flattening the DataTalks.Club FAQ datasets.
- Retrieving relevant FAQ entries with MinSearch, SQLite full-text search, or Elasticsearch.
- Building grounded prompts from retrieved context.
- Calling the OpenAI Responses API and inspecting response structure and usage.
- Reusing the same RAG orchestration with different search backends.
- Persisting indexes locally with SQLite or in Docker-backed Elasticsearch.
- Letting a model invoke FAQ search through OpenAI function calling, then returning the tool result for a grounded answer.

## Prerequisites

- Python 3.12 or newer
- [uv](https://docs.astral.sh/uv/) for Python environment and dependency management
- Docker with Docker Compose for the Elasticsearch examples
- An OpenAI API key for cells that generate answers

## Setup

Install the project dependencies:

~~~bash
uv sync
~~~

Create a local `.env` file for API-backed examples:

~~~text
OPENAI_API_KEY=your-key-here
~~~

The `.env` file and generated database files are excluded by `.gitignore`.

Start Jupyter:

~~~bash
uv run jupyter lab
~~~

## Elasticsearch

Start the single-node Elasticsearch 8.17.6 service:

~~~bash
docker compose up -d
~~~

Check that it is healthy:

~~~bash
docker compose ps
curl http://localhost:9200
~~~

Stop the service when you are finished:

~~~bash
docker compose stop
~~~

Elasticsearch data is stored in the named Docker volume `elasticsearch-data`, so indexes survive container restarts. Use `docker compose down --volumes` only when you also want to delete that persisted data.

## Notebooks

| File | Purpose |
| --- | --- |
| [`notebook.ipynb`](notebook.ipynb) | The full exploratory walkthrough. It starts with direct LLM calls and manually supplied context, downloads all Zoomcamp FAQ data, builds a MinSearch index, implements search/context/prompt/RAG functions, examines OpenAI response objects and token cost, tests course filtering, and finally repeats retrieval with Elasticsearch. |
| [`rag_cleaned.ipynb`](rag_cleaned.ipynb) | A concise end-to-end in-memory RAG example. It uses `ingest.py` and `RAGBase` to build the FAQ index, answer sample questions, and demonstrate custom assistant instructions without the exploratory steps. |
| [`rag_ingest.ipynb`](rag_ingest.ipynb) | A minimal ingestion and retrieval smoke test. It loads the FAQ data, builds the MinSearch index, constructs `RAGBase`, and runs a sample search for Docker-related material. |
| [`persistent_ingest.ipynb`](persistent_ingest.ipynb) | The persistence-focused workflow. It filters LLM Zoomcamp FAQs, creates and inspects SQLitesearch databases, connects a persistent index to `RAGBase`, bulk-indexes the FAQ collection into Elasticsearch, and verifies that the Elasticsearch index survives a Docker restart. |
| [`sqlite_rag.ipynb`](sqlite_rag.ipynb) | Reopens an existing SQLitesearch index in `faq.db`, runs full-text searches, and plugs that persistent index into `RAGBase` for an OpenAI-generated answer. Run an ingestion workflow first if `faq.db` does not yet exist. |
| [`agent.ipynb`](agent.ipynb) | Extends the RAG workflow with OpenAI function calling. It exposes FAQ retrieval as an application-owned tool, executes the model's tool request, demonstrates both `previous_response_id` and manually replayed history, and calculates token usage and estimated cost. |

## Python and configuration files

| File | Purpose |
| --- | --- |
| [`ingest.py`](ingest.py) | Downloads the per-course FAQ JSON files, combines them into one document list, and provides a helper for building a MinSearch index over question, section, and answer fields with course filtering. |
| [`rag_helper.py`](rag_helper.py) | Defines the reusable `RAGBase` class. It owns retrieval, context formatting, prompt construction, the OpenAI Responses API call, and the complete RAG sequence while accepting any index with a compatible `search` method. |
| [`main.py`](main.py) | The generated project entry-point placeholder. It currently prints a greeting and is not part of the RAG workflow. |
| [`docker-compose.yml`](docker-compose.yml) | Runs a single-node, security-disabled Elasticsearch 8.17.6 container on port 9200 with a health check and persistent named volume. |
| [`pyproject.toml`](pyproject.toml) | Declares Python 3.12+ and the project dependencies: Elasticsearch, Jupyter, MinSearch, OpenAI, python-dotenv, Requests, and SQLitesearch. |
| [`.python-version`](.python-version) | Pins the development Python version to 3.12. |
| [`.gitignore`](.gitignore) | Excludes the virtual environment, API-key file, and generated SQLite database, shared-memory, and write-ahead-log files. |

## Generated and local-only files

The following are runtime artifacts rather than source files:

- `faq.db` and `faq_llm.db` are local SQLitesearch indexes created during experiments.
- Files ending in `.db-shm` and `.db-wal` are SQLite working files.
- `.venv/` is the uv-managed Python environment.
- `__pycache__/` contains Python bytecode cache files.
- `.env` stores local API credentials and must not be committed.

## Suggested learning path

1. Work through [`notebook.ipynb`](notebook.ipynb) to see each RAG component built from first principles.
2. Review [`ingest.py`](ingest.py) and [`rag_helper.py`](rag_helper.py) to see the reusable implementation.
3. Run [`rag_cleaned.ipynb`](rag_cleaned.ipynb) for the compact in-memory workflow.
4. Use [`persistent_ingest.ipynb`](persistent_ingest.ipynb) to create and inspect persistent indexes.
5. Reopen the SQLite index with [`sqlite_rag.ipynb`](sqlite_rag.ipynb) and compare its retrieval with Elasticsearch.
6. Finish with [`agent.ipynb`](agent.ipynb) to let the model decide when and how to search through function calling.
