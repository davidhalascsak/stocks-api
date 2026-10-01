# Python and project structure

- Follow the existing package layout: `app/main.py` is the application entry point, configuration lives in `app/config/`, and API, service, and model code belongs in `app/api/`, `app/services/`, and `app/models/` respectively.
- Keep modules focused. Add repository or database packages when their functionality is introduced; avoid creating layers that have no current use.
- Use Python 3.14+ syntax and type annotations for new or changed functions and public data structures.
- Use Pydantic v2 APIs, consistent with the existing `model_validate` usage.
- Keep I/O and application configuration explicit. Do not commit credentials or rely on implicit working-directory assumptions when locating files.
- Prefer asynchronous libraries for I/O in async flows. Bound concurrency when fanning out requests or writes, and use timeouts for network operations.
- Retry only transient failures, with a finite attempt limit and backoff. Preserve cancellation and report partial failures explicitly instead of hiding them behind broad exception handling.
- Use Ruff for linting and follow the formatting and style already present in the repository.
