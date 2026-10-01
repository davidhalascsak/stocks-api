# Project instructions

This is a learning-focused FastAPI service for S&P 500 market data, not a trading or portfolio application.

- Use **uv** to manage dependencies and run project tools; `pyproject.toml` is authoritative.
- The supported Python floor is **3.14** (`requires-python` in `pyproject.toml`).
- App entry point: `app.main:app`. Run locally with `uv run uvicorn app.main:app --reload`.
- There is no configured build or type-check command. Use `uv run ruff check .` for linting and `uv run pytest` for tests.
- Read the relevant focused guidance before making changes:
  - [Python and project structure](docs/agent-guides/python.md)
  - [FastAPI and API conventions](docs/agent-guides/fastapi.md)
  - [Testing](docs/agent-guides/testing.md)
  - [Project scope and learning roadmap](docs/agent-guides/project-scope.md)
