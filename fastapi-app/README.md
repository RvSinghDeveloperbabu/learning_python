# fastapi-app/ — async LLM gateway / eval-runner  (Week 9)

**Premise:** the async door to expensive provider APIs. It accepts eval-run requests and orchestrates concurrent calls to LLM providers (Anthropic + OpenAI), validating everything with Pydantic v2. It handles fan-out, cost accounting, and resilience — the concerns that separate a toy async demo from a real gateway.

**Proves:** async correctness (never block the event loop; async httpx; `asyncio.gather` with bounded concurrency), Pydantic v2 mastery (models, validators, `Settings`), dependency injection, streaming responses (SSE), retries/timeouts/circuit-breaking, rate limiting, async SQLAlchemy, and a Dockerized service with auto OpenAPI docs.

**Why it matters:** Pydantic and typed async services are *everywhere* in LLM tooling — this is the most on-theme "senior Python" muscle.

**MVP (must-build):**
- Pydantic v2 request/response models + `Settings`-based config
- async provider calls with bounded concurrency; correct timeout/retry behavior
- DI for provider clients; streaming endpoint (SSE)
- async persistence; Dockerized; OpenAPI docs
- pytest incl. async tests + mocked providers (a **fake adapter**)

**Swing item #2:** the OpenAI adapter is stretch — MVP ships **Anthropic + a fake adapter**.

**I scaffold this myself** (`uv init`, structure, Dockerfile). Mentor guides, doesn't author.

➡️ Full spec: [`../docs/02-real-world-projects.md`](../docs/02-real-world-projects.md) · Curriculum: [`../docs/04-curriculum-core-python-and-web.md`](../docs/04-curriculum-core-python-and-web.md) (Week 9)
