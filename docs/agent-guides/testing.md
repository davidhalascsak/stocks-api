# Testing

- Add tests for new behavior and for regressions when fixing bugs. Use pytest; use pytest-asyncio for async tests as appropriate.
- Keep unit tests deterministic and independent of live market-data providers, databases, or Redis. Stub or inject external dependencies at the boundary.
- Cover success and failure paths, especially timeouts, retries, cancellation, concurrency limits, cache behavior, and per-ticker partial failures when those features exist.
- Add integration tests for interactions that cannot be adequately covered by isolated tests; make required services and setup explicit.
- Run the narrowest relevant test selection while iterating, then run the full suite with `uv run pytest` before completing a change.
- Run `uv run ruff check .` to check linting. The repository does not currently configure a separate build or type-check command.
