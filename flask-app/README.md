# flask-app/ — results-ingestion & webhook service  (Week 3 · SWING ITEM #1)

**Premise:** the always-on front door where distributed eval runners POST results. It authenticates callers (API key + **HMAC signature over raw bytes**), enforces **idempotency keys**, validates payloads against the shared contract, persists them, processes work in the background, and exposes a small query API + minimal dashboard.

**Proves:** a real micro-framework service (Flask is Python's Sinatra) — app-factory pattern, blueprints, SQLAlchemy + Flask-Migrate, request auth, idempotency, background jobs (a queue or thread pool). A deliberate contrast with Django's "batteries included."

**MVP (must-build):**
- app-factory + blueprints; SQLAlchemy models + migrations
- HMAC verification over the raw request body + API-key auth
- idempotency-key handling (same delivery twice ⇒ one effect)
- validate against [`../contracts/`](../contracts/); persist; query endpoint(s)
- pytest suite incl. bad-signature, replay, and malformed-payload cases

> **Swing item:** tight 3–4 day core. If I'm behind, this is the first thing to cut — its crown-jewel signals (HMAC-over-raw-bytes + the idempotency decision matrix) fold into the FastAPI gateway as a stretch webhook endpoint.

**I scaffold this myself** (`uv init`, structure, config). Mentor guides, doesn't author.

➡️ Full spec: [`../docs/02-real-world-projects.md`](../docs/02-real-world-projects.md) · Curriculum: [`../docs/04-curriculum-weeks-0-4.md`](../docs/04-curriculum-weeks-0-4.md)
