# Project scope and learning roadmap

- Keep changes aligned with the staged backend-learning goals in the root README: market-data discovery and ingestion, PostgreSQL persistence, resilient async fetching, bounded concurrency, background jobs, Redis caching, reporting, testing, and observability.
- Add capabilities incrementally. Prefer the smallest stage-appropriate implementation over introducing future infrastructure prematurely.
- Treat the stock domain as a backend-learning exercise. Do not add trading logic, portfolio management, frontend work, machine-learning predictions, or authentication unless the project requirements change.
- When adding ingestion or concurrency behavior, consider upstream rate limits, timeouts, retries, partial failures, database backpressure, and safe cancellation as relevant to that change.
- Preserve measurable learning outcomes for performance experiments: state what changed and capture relevant timings, throughput, and failure counts where the experiment calls for them.
