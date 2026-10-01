# FastAPI and API conventions

- Put endpoint modules under `app/api/`, define route groups with `APIRouter`, and compose routers in `app/main.py`.
- Define request and response shapes with Pydantic models under `app/dto/`. Set an explicit `response_model` on endpoints when returning structured data.
- Use `Depends` for shared request-scoped resources and application services rather than constructing them ad hoc inside route handlers.
- Use HTTP methods and status codes according to their semantics. Validate inputs at the API boundary and return deliberate, stable error responses.
- Raise `HTTPException` or use a focused application exception handler for expected API errors. Do not expose stack traces, secrets, or upstream internals to clients.
- Make route handlers `async` when they await non-blocking I/O. Do not call blocking network, database, or file operations directly from an async handler.
- Keep business workflows in `app/services/`; route handlers should coordinate input validation, dependencies, service calls, and response mapping.
- Use FastAPI lifespan handling for resources that need startup and shutdown management. Ensure created clients, pools, and other resources are closed cleanly.
- For long-running ingestion, follow the project roadmap: return a job identifier, expose progress/results, and define cancellation and partial-failure behavior rather than holding a request open indefinitely.
