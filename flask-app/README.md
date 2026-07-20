# flask-app/ — results-ingestion & webhook service  (Week 6)

**Premise:** the always-on front door where distributed eval runners POST results. It authenticates callers (API key + **HMAC signature over raw bytes**), enforces **idempotency keys**, validates payloads against the shared contract, persists them, processes work in the background, and exposes a small query API + minimal dashboard.

**Proves:** a real micro-framework service (Flask is Python's Sinatra) — app-factory pattern, blueprints, SQLAlchemy + Flask-Migrate, request auth, idempotency, background jobs (a queue or thread pool). A deliberate contrast with Django's "batteries included."

**MVP (must-build):**
- app-factory + blueprints; SQLAlchemy models + migrations
- HMAC verification over the raw request body + API-key auth
- idempotency-key handling (same delivery twice ⇒ one effect)
- validate against [`../contracts/`](../contracts/); persist; query endpoint(s)
- pytest suite incl. bad-signature, replay, and malformed-payload cases

> **No longer a swing item.** Flask is now the **first web framework I learn** (Week 6) — small and explicit, so nothing is hidden by convention. It is therefore no longer "the first thing to cut." If I fall badly behind, this shrinks to a **3-day tour** (routing, blueprints, one HMAC-verified endpoint) rather than disappearing; its crown-jewel signals are HMAC-over-raw-bytes and the idempotency decision matrix.

**I scaffold this myself** (`uv init`, structure, config). Mentor guides, doesn't author.

➡️ Full spec: [`../docs/02-real-world-projects.md`](../docs/02-real-world-projects.md) · Curriculum: [`../docs/04-curriculum-core-python-and-web.md`](../docs/04-curriculum-core-python-and-web.md) (Week 6 — six Flask days)
