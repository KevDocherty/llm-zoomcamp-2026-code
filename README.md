# LLM Zoomcamp 2026

This repository contains my notebooks, supporting code, and experiments for the 2026 [LLM Zoomcamp](https://github.com/DataTalksClub/llm-zoomcamp).

The repository is organized by course module. Each numbered module directory keeps its notebooks, helper code, generated data, and service configuration together, while the root `pyproject.toml` and `uv.lock` provide one reproducible Python environment for the whole course.

## Repository structure

```text
llm-zoomcamp-2026-code/
├── 01-agentic-rag/
│   ├── 01-rag-basics.ipynb
│   ├── 02-rag-cleaned.ipynb
│   ├── 03-rag-ingest.ipynb
│   ├── 04-persistent-ingest.ipynb
│   ├── 05-sqlite-rag.ipynb
│   ├── 06-function-calling.ipynb
│   ├── 07-agentic-loop.ipynb
│   ├── 08-frameworks.ipynb
│   ├── 09-other-frameworks.ipynb
│   ├── ingest.py
│   ├── rag_helper.py
│   └── docker-compose.yml
├── README.md
├── pyproject.toml
└── uv.lock
```

Additional numbered module directories will be added as the course progresses.

## Modules

| Module | Topic | Status |
| --- | --- | --- |
| [`01-agentic-rag`](01-agentic-rag/) | Retrieval-augmented generation, persistence, function calling, agent loops, and agent frameworks | Complete |
| `02-vector-search` | Vector search and embeddings | In progress |

## Prerequisites

- [uv](https://docs.astral.sh/uv/) for Python, dependency, and environment management
- Docker with Docker Compose for examples that use Elasticsearch
- An OpenAI API key for notebooks that call OpenAI models

## Setup

### Install uv

On macOS or Linux, install `uv` with the official standalone installer:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

On macOS, Homebrew is an alternative:

```bash
brew install uv
```

On Windows PowerShell, use:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Restart the terminal if the installer asks you to update your shell, then confirm that `uv` is available:

```bash
uv --version
```

### Install Python and project dependencies

The repository requests Python 3.12 through [`.python-version`](.python-version). If a compatible Python installation is not already available, `uv` can install it explicitly:

```bash
uv python install 3.12
```

From the repository root, create the `.venv` environment and install the exact dependency versions recorded in `uv.lock`:

```bash
uv sync
```

You do not need to install the course packages one by one. `uv sync` reads `pyproject.toml`, resolves the locked environment, and installs both the direct packages and their transitive dependencies.

The direct packages currently used by the course repository are:

| Package | Purpose |
| --- | --- |
| `elasticsearch` | Python client for indexing and searching the Docker-hosted Elasticsearch service |
| `jupyter` | Notebook server and interactive course environment |
| `minsearch` | Lightweight in-memory text search used in the introductory RAG examples |
| `openai` | OpenAI Responses API client used by the LLM and agent examples |
| `python-dotenv` | Loads API keys and other local settings from `.env` |
| `requests` | Downloads the DataTalks.Club FAQ datasets |
| `sqlitesearch` | Persistent SQLite-backed full-text search examples |
| `toyaikit` | Agent framework used in the framework-comparison notebooks |

Docker and the Elasticsearch server are system services and are not installed by `uv`.

### Configure the API key

Create a root `.env` file for API-backed examples:

```text
OPENAI_API_KEY=your-key-here
```

The `.env` file, virtual environment, generated databases, and notebook checkpoints are excluded by `.gitignore`.

### Start Jupyter

Start Jupyter from the repository root:

```bash
uv run jupyter lab
```

Open notebooks through their module directory. The Module 1 notebooks keep their helper modules in the same directory, so imports such as `from ingest import load_faq_data` continue to work naturally.

## Module 1: Agentic RAG

Module 1 builds a retrieval-augmented course assistant over the DataTalks.Club FAQ data. It progresses from direct model calls and in-memory retrieval to persistent search, OpenAI function calling, a handwritten agent loop, and an introduction to agent frameworks.

### What the module demonstrates

- Loading and flattening the DataTalks.Club FAQ datasets
- Retrieving relevant entries with MinSearch, SQLite full-text search, and Elasticsearch
- Building grounded prompts from retrieved context
- Calling the OpenAI Responses API and inspecting response structure and usage
- Reusing RAG orchestration with different search backends
- Persisting indexes with SQLite and Docker-backed Elasticsearch
- Exposing FAQ retrieval as a model-callable tool
- Building an agent loop with conversation memory, iteration limits, and grounding rules
- Comparing handwritten orchestration with ToyAIKit and other agent frameworks

### Notebooks

| Notebook | Purpose |
| --- | --- |
| [`01-rag-basics.ipynb`](01-agentic-rag/01-rag-basics.ipynb) | The full exploratory walkthrough: direct LLM calls, FAQ ingestion, MinSearch retrieval, prompt construction, response inspection, token cost, course filtering, and Elasticsearch. |
| [`02-rag-cleaned.ipynb`](01-agentic-rag/02-rag-cleaned.ipynb) | A concise end-to-end in-memory RAG example using the reusable helper modules. |
| [`03-rag-ingest.ipynb`](01-agentic-rag/03-rag-ingest.ipynb) | A minimal ingestion and retrieval smoke test. |
| [`04-persistent-ingest.ipynb`](01-agentic-rag/04-persistent-ingest.ipynb) | Creates and inspects persistent SQLite indexes, indexes the FAQ collection in Elasticsearch, and verifies persistence. |
| [`05-sqlite-rag.ipynb`](01-agentic-rag/05-sqlite-rag.ipynb) | Reopens an existing SQLite search index and uses it as the retrieval backend for RAG. |
| [`06-function-calling.ipynb`](01-agentic-rag/06-function-calling.ipynb) | Exposes FAQ search through OpenAI function calling and demonstrates two approaches to conversation history. |
| [`07-agentic-loop.ipynb`](01-agentic-rag/07-agentic-loop.ipynb) | Builds the repeated model–tool loop from first principles, including response checks and iteration limits. |
| [`08-frameworks.ipynb`](01-agentic-rag/08-frameworks.ipynb) | Reimplements the loop with ToyAIKit, compares manual and generated schemas, and inspects conversation results. |
| [`09-other-frameworks.ipynb`](01-agentic-rag/09-other-frameworks.ipynb) | Compares production-oriented frameworks and explains when a simpler non-agent workflow is preferable. |

### Supporting files

| File | Purpose |
| --- | --- |
| [`ingest.py`](01-agentic-rag/ingest.py) | Downloads the FAQ data and builds the in-memory MinSearch index. |
| [`rag_helper.py`](01-agentic-rag/rag_helper.py) | Defines reusable retrieval, context, prompt, and answer-generation logic. |
| [`docker-compose.yml`](01-agentic-rag/docker-compose.yml) | Runs a single-node Elasticsearch service with persistent storage. |

### Elasticsearch

Start Elasticsearch from the repository root:

```bash
docker compose -f 01-agentic-rag/docker-compose.yml up -d
docker compose -f 01-agentic-rag/docker-compose.yml ps
```

Confirm that the service is healthy and inspect its indexes:

```bash
curl http://localhost:9200
curl "http://localhost:9200/_cat/indices?v"
```

#### Stopping and restarting

Elasticsearch runs in Docker Desktop independently of VS Code. Closing VS Code or its integrated terminal does not stop the container.

After a study session, stop Elasticsearch to release its memory:

```bash
docker compose -f 01-agentic-rag/docker-compose.yml stop
```

Resume the same container later:

```bash
docker compose -f 01-agentic-rag/docker-compose.yml start
```

For a longer break, you can remove the container and network:

```bash
docker compose -f 01-agentic-rag/docker-compose.yml down
```

Recreate them when needed:

```bash
docker compose -f 01-agentic-rag/docker-compose.yml up -d
```

The Elasticsearch index is stored in the Docker volume `01-agentic-rag_elasticsearch-data`. This volume persists across VS Code restarts, Docker container restarts, `docker compose stop`, and ordinary `docker compose down` operations.

The Compose configuration uses `restart: unless-stopped`, so Elasticsearch may start automatically with Docker Desktop unless it was stopped manually.

Do not include `--volumes` or `-v` with `docker compose down` unless you intentionally want to delete the Elasticsearch index. Likewise, do not manually remove `01-agentic-rag_elasticsearch-data` if you want to retain its data.

### Suggested learning path

1. Work through [`01-rag-basics.ipynb`](01-agentic-rag/01-rag-basics.ipynb) for the complete exploratory path.
2. Review [`ingest.py`](01-agentic-rag/ingest.py) and [`rag_helper.py`](01-agentic-rag/rag_helper.py).
3. Run [`02-rag-cleaned.ipynb`](01-agentic-rag/02-rag-cleaned.ipynb) and [`03-rag-ingest.ipynb`](01-agentic-rag/03-rag-ingest.ipynb) for the compact workflows.
4. Create persistent indexes with [`04-persistent-ingest.ipynb`](01-agentic-rag/04-persistent-ingest.ipynb).
5. Reopen the SQLite index with [`05-sqlite-rag.ipynb`](01-agentic-rag/05-sqlite-rag.ipynb).
6. Introduce model-directed search in [`06-function-calling.ipynb`](01-agentic-rag/06-function-calling.ipynb).
7. Build the full repeated tool-use loop in [`07-agentic-loop.ipynb`](01-agentic-rag/07-agentic-loop.ipynb).
8. Compare the handwritten loop with ToyAIKit in [`08-frameworks.ipynb`](01-agentic-rag/08-frameworks.ipynb).
9. Finish with [`09-other-frameworks.ipynb`](01-agentic-rag/09-other-frameworks.ipynb) to compare framework choices.

## Dependency management

The root [`pyproject.toml`](pyproject.toml) declares the direct dependencies for the complete course repository. [`uv.lock`](uv.lock) records the exact resolved environment, including transitive dependencies, and should remain committed.

### Install a new package from the command line

Add a package from the repository root with `uv add`:

```bash
uv add package-name
```

For example:

```bash
uv add pandas
uv add "numpy>=2.0"
uv add pandas matplotlib
```

Each `uv add` command performs three related updates:

1. It adds the direct dependency and its version constraint to the `[project].dependencies` list in `pyproject.toml`.
2. It updates `uv.lock` with the exact resolved versions of that package and its transitive dependencies.
3. It synchronizes the package into the project's `.venv` environment so it is immediately available to notebooks and `uv run` commands.

For a development-only tool, such as a test runner or formatter, use `--dev`:

```bash
uv add --dev pytest
```

Use `uv add` instead of `uv pip install` for course dependencies. `uv pip install` can modify an environment without recording the package as a project dependency in `pyproject.toml`.

### Remove or synchronize packages

Remove an unused dependency with:

```bash
uv remove package-name
```

After pulling changes that modify `pyproject.toml` or `uv.lock`, run `uv sync` again to update the local environment.

After adding or removing a dependency, review and commit both `pyproject.toml` and `uv.lock` so that other environments reproduce the same package set.

Do not edit `uv.lock` manually; let `uv add`, `uv remove`, `uv sync`, and `uv lock` manage it.
