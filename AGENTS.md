# LLM Zoomcamp 2026 repository guidance

## Purpose and scope

- This is a personal learning repository for the 2026 DataTalks.Club LLM Zoomcamp.
- Keep examples clear and instructional. Prefer small, readable changes over production-style abstractions unless the task explicitly asks for them.
- The repository is organized by numbered course modules. Keep module-specific notebooks, helper code, generated data, and service configuration inside the relevant module directory.
- Use the root Python environment for all modules. The root `pyproject.toml` and `uv.lock` are the dependency source of truth.

## Environment and dependencies

- Use Python 3.12 or newer and `uv` for Python commands and dependency management.
- Run commands from the repository root unless a notebook or command explicitly requires another working directory.
- Install the locked environment with `uv sync`.
- Run Python tools with `uv run`, for example `uv run jupyter lab`.
- Add or remove dependencies with `uv add` and `uv remove`. Never edit `uv.lock` manually, and keep it committed when dependency resolution changes.

## Working conventions

- Preserve the course's incremental progression: exploratory notebooks may intentionally show intermediate or simpler implementations before later abstractions.
- Keep reusable Python helpers beside the notebooks that use them unless functionality is genuinely shared by multiple modules.
- Match the surrounding Python and notebook style. Avoid broad formatting or notebook-output churn unrelated to the requested task.
- Update the root `README.md` when adding a module, changing setup steps, or changing the documented learning path.
- Do not alter generated databases, notebook checkpoints, virtual environments, or Docker data as source files.

## Validation

- There is currently no repository-wide automated test suite. Use the smallest relevant validation for the files changed.
- For ordinary Python helper changes, at minimum check syntax with `uv run python -m compileall <changed-module>` and run a focused smoke test when one does not require paid API calls.
- Do not run every notebook, make live OpenAI API calls, download large datasets, or start external services unless the task requires it or the user asks for it.
- When Elasticsearch is required, use `docker compose -f 01-agentic-rag/docker-compose.yml up -d` and verify it with `docker compose -f 01-agentic-rag/docker-compose.yml ps`.

## Secrets, generated state, and destructive operations

- Never commit `.env`, API keys, credentials, `.venv`, `*.db`, notebook checkpoints, caches, or `.DS_Store` files.
- Treat API-backed notebook execution as potentially billable. Prefer mocks, local checks, or inspection when live execution is unnecessary.
- Preserve the Elasticsearch volume `01-agentic-rag_elasticsearch-data`. Do not use `docker compose down --volumes`, `docker compose down -v`, or remove the volume unless the user explicitly requests deletion of the persisted index.
- Do not overwrite or discard notebook work, generated indexes, or uncommitted changes without explicit confirmation.

## Git scope

- The GitHub-backed repository root is this directory, not its parent `LLM Zooomcamp` folder.
- The primary branch is `main`, and the remote is `https://github.com/KevDocherty/llm-zoomcamp-2026-code.git`.
- Before committing, review the diff and status so local datasets, secrets, notebook noise, and `.DS_Store` are not included.
