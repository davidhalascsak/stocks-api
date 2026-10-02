# S&P 500 Market Data API

A small Python + FastAPI project for learning backend engineering through a real-world data pipeline.

The stock domain is just a playground. The goal is to learn the parts of a modern backend by building one step at a time:

- FastAPI and async endpoints
- PostgreSQL and SQLAlchemy
- Redis for caching
- External API integration
- Concurrency and rate limiting
- Timeouts, retries, cancellation, and backpressure
- Background jobs and progress tracking
- Testing, observability, and Docker

This is intentionally not a trading app or portfolio platform. It is a learning project designed to teach backend systems thinking.

---

# Project goals

Build a service that can:

1. Discover the S&P 500 constituents
2. Fetch market data from a third-party source
3. Process requests concurrently without overwhelming upstream services
4. Handle failures and retries gracefully
5. Store data in PostgreSQL
6. Protect downstream systems with backpressure
7. Run ingestion jobs in the background
8. Cancel long-running jobs cleanly
9. Cache reporting data in Redis
10. Expose small but useful reporting endpoints
11. Measure and observe the system

---

# Learning path

The project is intentionally staged. Each phase introduces just enough new material to support the next one.

| Phase | Focus | Outcome |
| --- | --- | --- |
| 1 | Project setup | Clean FastAPI app structure |
| 2 | S&P 500 source | Dynamic company discovery |
| 3 | PostgreSQL | Persistent company and price data |
| 4 | Sequential ingestion | Baseline benchmark |
| 5 | Async HTTP | Understand event loop and non-blocking I/O |
| 6 | `asyncio.gather()` | Concurrent fetches |
| 7 | Semaphore | Limit concurrent requests |
| 8 | Timeouts | Handle slow or hung requests |
| 9 | Retries + backoff | Recover from transient failures |
| 10 | Rate limiting | Control request frequency |
| 11 | Partial failures | Continue on per-ticker errors |
| 12 | DB backpressure | Protect Postgres under load |
| 13 | Background jobs | Async ingestion job flow |
| 14 | Cancellation | Cancel in-flight jobs safely |
| 15 | Redis caching | Cache reads and report endpoints |
| 16 | Cache invalidation | Handle staleness cleanly |
| 17 | Reporting | Sector and market summaries |
| 18 | Testing | Unit, async, and integration tests |
| 19 | Observability | Logs, metrics, traces |
| 20 | Docker | Run the stack locally |

---

# Phase details

## Phase 1: Project setup

Create a clean Python project with a basic FastAPI app, config, logging, and repo structure.

Suggested layout:

```text
app/
├── main.py
├── api/
├── services/
├── models/
├── repositories/
├── db/
├── config.py
└── utils/
```

Learn:

- Application lifecycle
- Dependency injection
- Routers
- ASGI basics
- Configuration patterns

## Phase 2: Basic API

Add:

```text
GET /health
GET /stocks/{ticker}
```

The first `/stocks/{ticker}` response can be mocked. Later, it will read from PostgreSQL.

Learn:

- Path/query parameters
- Pydantic models
- Response models
- HTTP status codes
- Error handling

## Phase 3: PostgreSQL

Add a PostgreSQL database and model the core entities:

```text
companies
---------
id
ticker
name
sector
industry

daily_prices
------------
id
ticker
date
open
high
low
close
volume
```

Add:

- SQLAlchemy
- Async DB engine
- Sessions and transactions
- Alembic migrations
- Repository layer

Learn:

- Async SQLAlchemy
- Connection pooling
- Indexing
- Migrations
- Repository pattern

## Phase 4: S&P 500 ingestion

Add a service to fetch current S&P 500 constituents and expose:

```text
GET /companies
POST /admin/sync-companies
```

Learn:

- HTTP clients
- Data validation
- Upserts
- External data drift

## Phase 5: Sequential ingestion

The first ingestion flow is intentionally simple and slow:

```python
for ticker in tickers:
    data = await fetch_stock(ticker)
    await save_stock(data)
```

Measure runtime and capture a baseline for all future performance experiments.

Learn:

- Baseline performance
- External I/O cost
- Why sequential requests are slow

## Phase 6: Async HTTP

Switch from synchronous HTTP calls to an async client and compare behavior.

Learn:

- Event loop
- Coroutines
- `await`
- Blocking versus non-blocking I/O

## Phase 7: `asyncio.gather()`

Run many external fetches concurrently:

```python
await asyncio.gather(*(fetch(ticker) for ticker in tickers))
```

Benchmark:

- sequential runtime
- concurrent runtime
- requests/second
- failure count

Learn:

- Task scheduling
- Concurrent work
- Why unlimited concurrency is risky

## Phase 8: Semaphore

Introduce request limits:

```python
semaphore = asyncio.Semaphore(10)
```

Test different values like 1, 5, 10, 25, and 50.

Learn:

- Concurrency limits
- Resource protection
- Queuing and waiting

## Phase 9: Timeouts

Add timeouts so a slow request fails predictably instead of hanging forever.

Test:

- normal response
- slow response
- timeout
- no response

Learn:

- cancellation basics
- hung tasks
- failure boundaries

## Phase 10: Retries + exponential backoff

Implement retry logic for temporary failures such as 500, 429, connection resets, and timeouts.

Learn:

- retryable vs non-retryable errors
- exponential backoff
- maximum attempts
- retry storms

## Phase 11: Rate limiting

Now add a limiter for request frequency, not just concurrency.

Example:

```text
max_concurrency = 10
max_request_rate = 5/sec
```

Learn:

- concurrency vs throughput
- throttling
- external API protection

## Phase 12: Partial failures

A failing ticker should not kill the entire ingestion run. Store per-ticker failures and report aggregate results.

Example outcome:

```json
{
  "status": "completed_with_errors",
  "total": 503,
  "successful": 497,
  "failed": 6
}
```

Learn:

- failure isolation
- error aggregation
- resilient batch design

## Phase 13: DB concurrency + backpressure

The database can become the bottleneck just like the external API.

Use separate concurrency controls for external requests and DB writes.

Example:

```text
Yahoo concurrency: 10
DB concurrency: 5
```

Learn:

- backpressure
- connection pool pressure
- resource contention

## Phase 14: Background ingestion jobs

Instead of blocking the client for a long-running refresh, create a job and return a run ID immediately.

```text
POST /admin/refresh
GET /admin/refresh/{run_id}
```

Learn:

- long-running tasks
- job state
- progress tracking
- async API design

## Phase 15: Cancellation

Add a cancel endpoint and test what happens when an ingestion is interrupted mid-flight.

Learn:

- task cancellation
- propagation of cancellation
- cleanup
- partial completion

## Phase 16: Redis caching

Add Redis for read-heavy endpoints and reporting. Compare a PostgreSQL-only flow to a Redis + PostgreSQL flow.

Learn:

- cache-aside pattern
- TTLs
- hit/miss tracking
- read performance

## Phase 17: Cache invalidation

When underlying data changes, cached responses may become stale. Learn when to invalidate or refresh cache entries.

Learn:

- stale data
- explicit invalidation
- TTL tradeoffs
- consistency

## Phase 18: Reporting

Build simple market reports from stored data, such as:

- top gainers
- top losers
- sector leaders
- highest volume
- daily market summaries

Learn:

- SQL aggregations
- reporting queries
- indexes
- response design

## Phase 19: Testing

Add tests for retry logic, timeout handling, cache behavior, semaphore limits, and integrations.

Test types:

- unit tests
- async tests
- integration tests
- failure-path tests

Learn:

- pytest
- async testing
- mocking
- resilience testing

## Phase 20: Observability

Instrument the app with logs, timings, and metrics.

Track:

- request latency
- ingestion duration
- ticker success/failure counts
- Yahoo latency
- retry counts
- cache hit rate
- DB query latency

Learn:

- structured logging
- metrics
- tracing
- debugging async systems

## Phase 21: Docker + final cleanup

Run PostgreSQL and Redis locally through Docker Compose.

Final stack:

```text
FastAPI
PostgreSQL
Redis
```

Finalize:

- environment variables
- Docker Compose
- health checks
- README cleanup
- logging and metrics
- migrations
- remove dead/experimental code

---

# Concurrency laboratory

At the end, keep a short benchmark section with experiments like:

- sequential vs `asyncio.gather()`
- `Semaphore(1)` vs `Semaphore(10)` vs `Semaphore(50)`
- no timeout vs 5 second timeout
- no retry vs 3 retries + backoff
- single DB writer vs DB semaphore
- PostgreSQL only vs Redis + PostgreSQL

For each experiment, record:

- what changed
- why it changed
- what broke
- what you learned
- what configuration worked best

---

# What this project should teach you

## FastAPI

- request handling
- dependency injection
- Pydantic validation
- async endpoints
- background jobs

## AsyncIO

- event loop
- coroutine
- task
- `await`
- cancellation
- timeouts

## Concurrency

- concurrency vs parallelism
- semaphore
- rate limiting
- backpressure
- connection pools

## Reliability

- timeouts
- retries
- exponential backoff
- partial failures
- failure isolation

## Databases

- Async SQLAlchemy
- transactions
- connection pooling
- indexes
- migrations

## Caching

- Redis
- cache-aside pattern
- TTL
- invalidation
- stale data handling

## Backend engineering

- job orchestration
- external API integration
- observability
- testing
- system design

---

# Scope control

Keep this focused on backend learning. Do not turn it into a full trading or portfolio application.

Avoid adding:

- trading logic
- portfolio management
- auth systems unless they become necessary
- front-end work
- ML predictions
- large analytics features

The point is to get better at Python backend engineering, async systems, and real-world reliability patterns.

---

# Final project outcome

By the end, the project should be able to:

1. discover S&P 500 companies
2. fetch market data concurrently
3. control upstream and downstream concurrency
4. handle timeouts and retries
5. store data in PostgreSQL
6. protect the database with backpressure
7. run ingestion jobs in the background
8. cancel jobs safely
9. cache reports in Redis
10. expose useful reporting endpoints
11. measure everything

The important part is not just building the app. It is understanding why each stage exists and what problem it is solving.
