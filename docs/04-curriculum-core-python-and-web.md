# Curriculum: Core Python & Web Frameworks (Weeks 4–9)

**Prerequisite:** [`07-python-fundamentals.md`](07-python-fundamentals.md) — Weeks 1–3. Do not start here until Day 18's tooling gate is green. This file assumes you can already write functions, classes, exceptions, file I/O, and a pytest suite.

**How to read this:** Each day is ~3–4 hrs, split roughly **30% READ / 70% BUILD**. You type every line of Python; acceptance criteria are things *you* can verify (mypy/pytest/output) so you know you're done before I review. "Watch-outs" are the Ruby-brain traps for that exact topic. The "senior signal" is the one sentence that tells an interviewer you actually own the concept.

**Standing rule from Week 4 on:** run it with `uv run`, keep it under version control, and before you call it done run `ruff check`, `mypy --strict`, and `pytest`. *(This gate begins at the Week-3 Day-18 graduation, not before — see the fundamentals file.)*

> **Week numbers come from [`../Ravi_Python_LLM_Learning_Plan.md`](../Ravi_Python_LLM_Learning_Plan.md)**, the single source of truth. Project specs live in [`02-real-world-projects.md`](02-real-world-projects.md).

---

## WEEK 0 — Environment + Apply ✅ COMPLETE

Kept for reference. Python 3.12+ via `uv`, the venv model, VS Code + Pylance, and the first job application. Superseded operationally — see `PROGRESS.md` for status.

---

## WEEKS 4–5 — Idiomatic Python + ship `evalctl` (10 days)

**GitHub deliverable (end of Day 10):** `evalctl` — a typed, streaming, pytest-covered CLI, plus the shared `contracts/` schemas.

> **Note on what moved.** Basic syntax, data structures, functions, classes, exceptions, files, JSON/dataclasses, logging, and first-pass pytest are now taught in [`07-python-fundamentals.md`](07-python-fundamentals.md). This phase covers what makes Python code *idiomatic* rather than merely correct.

### Day 1 — Comprehensions + generator expressions
- **Focus:** list/dict/set comprehensions and the lazy generator-expression variant.
- **READ:** Real Python "When to Use a List Comprehension"; the comprehension section of "Introduction to Python Generators".
- **BUILD:** revisit your fundamentals contact book — rewrite the loops that genuinely read better as comprehensions. Add a dict comprehension and one generator-expression path over a large file.
- **Acceptance:** identical output to the loop version; at least one list, one dict comprehension, and one generator expression used appropriately; you can state which one is lazy and why the big-file path stays memory-flat.
- **Ruby→Python watch-outs:** `arr.map{...}` → comprehension; `arr.select{...}` → comprehension with an `if`; map+select chains collapse into one comprehension. **Don't over-nest** — a triple-nested comprehension is worse than a loop. Generator expressions are **single-use and lazy** — iterating twice yields nothing the second time, a real gotcha coming from eager Ruby enumerables.
- **Senior signal:** You reach for a generator expression instead of a list comprehension when the result is consumed once, and can explain the memory difference.

### Day 2 — Type hints + `mypy --strict`, properly
- **Focus:** `list[int]`, `dict[str, X]`, `X | None`, unions, generics on your own functions.
- **READ:** mypy "Type hints cheat sheet"; Python docs `typing` intro; Real Python "Python Type Checking".
- **BUILD:** fully annotate your fundamentals package and get it through `mypy --strict` with no escape hatches.
- **Acceptance:** `mypy --strict` passes with zero errors and **zero `# type: ignore`**; no `Any` in your own signatures; "maybe absent" is expressed with `X | None`.
- **Ruby→Python watch-outs:** `Optional[X]` is exactly `X | None`. A function that returns nothing is annotated `-> None`.
- **⚠️ Get this right:** annotations are **not enforced at runtime** — mypy is a *static* checker, like a compiler pass, not a `raise` on bad types. But they **are** evaluated, stored, and readable at runtime (via `__annotations__` / `typing.get_type_hints`), which is exactly the mechanism dataclasses, Pydantic, and FastAPI rely on. Never say "erased at runtime" in an interview — that's a different language's model, and it contradicts your Weeks 9–12 work.
- **Senior signal:** You treat `mypy --strict` green as the baseline and can explain precisely what static checking does and does not guarantee.

### Day 3 — Functions II: `*args`/`**kwargs`, keyword-only, unpacking
- **Focus:** flexible signatures; re-meeting the mutable-default trap now that you've been bitten by it once.
- **READ:** Python tutorial §4.7–4.9; Real Python "Python args and kwargs".
- **BUILD:** a small configurable aggregator — takes an iterable of records plus optional flags via keyword-only args, returns a summary. Include one `*args` function, one `**kwargs` function, and `*`/`**` unpacking at a call site.
- **Acceptance:** at least one keyword-only parameter (after a bare `*`); your code does not accumulate state across calls; `mypy --strict` clean.
- **Ruby→Python watch-outs:** `**kwargs` ≈ Ruby's trailing options hash; `*args` ≈ Ruby splat. Python `lambda` is single-expression only — pass named functions for anything real.
- **Senior signal:** Asked "why does this function 'remember' its last call's list?", you name the mutable-default-arg trap and give the `None`-default fix instantly.

### Day 4 — `collections` + `pathlib` in depth
- **Focus:** `Counter`, `defaultdict`, `namedtuple`; real filesystem work.
- **READ:** Python docs `collections`; Real Python "Python's pathlib Module".
- **BUILD:** refactor your counting code onto `Counter` (and `most_common`); rewrite any traversal with `pathlib` globbing.
- **Acceptance:** `Counter`'s top-N replaces your hand-rolled version; a `defaultdict` removes a "does this key exist?" check; **all** path handling via `pathlib` — no string concatenation, no `os.path`.
- **Ruby→Python watch-outs:** `defaultdict` ≈ `Hash.new(0)` / `Hash.new{|h,k| h[k]=[]}`. `Path.glob`/`rglob` ≈ `Dir.glob`. `Counter` has no Ruby stdlib twin — it's a dict subclass.
- **Senior signal:** You reach for `Counter`/`defaultdict` reflexively instead of hand-initializing dict entries.

### Day 5 — Generators (`yield`) + `itertools`/`functools`
- **Focus:** lazy streaming with `yield`; composing iterators; caching and partial application.
- **READ:** Real Python "How to Use Generators and yield"; Python docs `itertools` (islice, groupby, chain) and `functools` (lru_cache, reduce).
- **BUILD:** a generator function that streams records from a large file one at a time; use `groupby`/`islice` to batch them; cache an expensive pure function.
- **Acceptance:** the reader is a generator; memory stays flat regardless of file size; `groupby` used correctly (**it needs sorted input**); the cache measurably avoids recomputation.
- **Ruby→Python watch-outs:** **Python `yield` is NOTHING like Ruby's `yield`** (which calls a block). Python's produces a lazy iterator — closer to Ruby `Enumerator`/`.lazy`. A generator is exhausted after one pass. `itertools.groupby` groups only *consecutive* equal keys — unlike Ruby's `group_by`, which buckets globally. `functools.reduce` ≈ Ruby `inject`.
- **Senior signal:** You explain generators as lazy, single-pass iterators and know `groupby` requires pre-sorted input.

### Day 6 — Context managers you write + decorators
- **Focus:** the `with` protocol (`__enter__`/`__exit__` and `@contextmanager`) and writing decorators. You *used* `with` in fundamentals; now you author both.
- **READ:** Real Python "Context Managers and Python's with Statement" + "Primer on Python Decorators"; Python docs `contextlib`.
- **BUILD:** (a) a context manager that times a block or guarantees cleanup of a resource; (b) a timing or retry decorator applied to one of your functions, using `functools.wraps`.
- **Acceptance:** the context manager releases the resource **even when an exception is raised inside the `with`**; the decorator preserves the wrapped function's name and docstring; both are annotated and mypy-clean.
- **Ruby→Python watch-outs:** `with` ≈ `File.open(...) do |f| ... end`, generalized. Decorators ≈ Ruby method wrapping / `prepend`, but as first-class `@` syntax. Forgetting `functools.wraps` silently mangles introspection — a subtle senior tell. A decorator that takes arguments needs an extra layer of nesting; understand why.
- **Senior signal:** You can explain the `__enter__`/`__exit__` protocol and guarantee cleanup-on-exception without a `begin/ensure` mindset leaking through.

### Day 7 — `Protocol`, `TypedDict`, `Literal` — typed duck typing
- **Focus:** structural typing: describing "anything with these methods" without inheritance.
- **READ:** Python docs `typing.Protocol`, `TypedDict`, `Literal`; mypy docs on protocols.
- **BUILD:** define a `Protocol` for a pluggable component in `evalctl` (e.g. a report formatter) and write two implementations that satisfy it without a shared base class.
- **Acceptance:** both implementations type-check against the protocol with no inheritance; deliberately break one method's signature and watch mypy catch it; a `TypedDict` describes one JSON shape you parse.
- **Ruby→Python watch-outs:** this is duck typing — which Ruby does implicitly — but **checked statically**. Ruby has no daily equivalent; the closest is an RBS interface.
- **Senior signal:** You reach for a `Protocol` instead of an abstract base class when you only need a shape, and can say why that's the more Pythonic seam.
- **📌 Forward link:** this is the exact seam you'll need for the provider abstraction in `agent-cli` (P5 M1) and the `Sandbox` protocol in `eval-harness` (P6 M2). Learn it here, not there.

### Days 8–10 — Assemble `evalctl` + publish `contracts/` (DELIVERABLE)
- **Focus:** wiring a real CLI; streaming validation; metrics; the shared schema artifact.
- **READ:** Python docs `argparse` tutorial (or Typer docs); [`02-real-world-projects.md`](02-real-world-projects.md) → Project 1 for the full spec, milestones, and acceptance criteria.
- **BUILD:** the `evalctl` MVP — validate JSONL against the schema with per-line errors, filter/aggregate, compute pass rate and latency p50/p95 and cost, dual table/JSON export, and a threshold gate. Publish `contracts/` (test-case / run / result, each with `schema_version`).
- **Acceptance:** streams a ~1M-line file at roughly constant memory (measure it); `--format json` is byte-stable across two runs; malformed lines produce a precise `line N: field X expected Y` error and a non-zero exit; empty input yields 0.0 with no `ZeroDivisionError`; `mypy --strict` + `ruff` clean; pytest green; **pushed to GitHub**.
- **⚠️ Deliberate omission:** **Pydantic is NOT used here.** You meet it in Week 9. Hand-rolling validation over dataclasses is the learning goal — it teaches you what a schema layer *does* before a library hides it.
- **Senior signal:** You can defend every acceptance number, and explain why exact percentiles are not O(1) memory while counts and sums are.

**Weeks 4–5 interview check:** (1) "List comprehension vs generator expression — when does it matter?" (2) "What does `mypy --strict` buy you, and what does it *not* enforce at runtime?"

---

## WEEK 6 — Flask: your first web framework (6 days)

**GitHub deliverable (Day 6):** the eval-results ingestion & webhook service.
**Framing:** **Flask ≈ Sinatra**, not Rails. You assemble every component yourself — which is exactly why it's the right first framework: nothing is hidden by convention. Full spec: [`02-real-world-projects.md`](02-real-world-projects.md) → Project 2.

### Day 1 — App factory, blueprints, routing, config
- **READ:** Flask docs "Quickstart" + "Application Factories" + "Blueprints".
- **BUILD:** a Flask app created by a factory function, with `ingest` and `api` blueprints registered, config loaded from environment variables, and `/healthz` responding.
- **Acceptance:** the dev server runs; `/healthz` returns 200 JSON; config comes from the environment, not literals; blueprints are registered in the factory, not at import time.
- **Ruby→Python watch-outs:** the factory ≈ how you'd build a Sinatra app class rather than Rails' implicit boot. Blueprints ≈ mountable Sinatra apps / Rails engines. **There is no autoloading** — every import is explicit.
- **Senior signal:** You can explain why an app factory matters for testing (a fresh app per test, no global state).

### Day 2 — SQLAlchemy 2.0 models + migrations
- **READ:** SQLAlchemy 2.0 ORM quickstart; Flask-Migrate docs.
- **BUILD:** models for `Client`, `Run`, `TestCaseResult`, `WebhookDelivery`, `IdempotencyRecord`, and an `Outbox` table. Generate and apply the first migration.
- **Acceptance:** migration applies and rolls back cleanly; a duplicate `(run_id, case_key)` raises `IntegrityError` — **prove the constraint at the database level, don't rely on application logic**.
- **Ruby→Python watch-outs:** SQLAlchemy 2.0 is **not** ActiveRecord — sessions are explicit, there's no implicit save, and objects aren't magically persisted. Alembic/Flask-Migrate ≈ `rails db:migrate`, but migrations are generated from *your* diff, then edited by you.
- **Senior signal:** You put uniqueness in a database constraint, not a `find_by`-then-`create` race.

### Day 3 — HMAC signature verification + API keys
- **READ:** Python docs `hmac` and `hashlib`; any provider's webhook-signature guide (Stripe's or GitHub's is the canonical shape).
- **BUILD:** verify inbound webhooks — API key lookup, then HMAC-SHA256 over `timestamp + "." + raw body`, then a ±5-minute freshness window.
- **Acceptance:** flip **one byte** of the body → 401; a 10-minute-old timestamp → 400; signatures compared with a constant-time comparison, **never `==`**; the signature covers the timestamp (so it can't be replayed with a new one).
- **Ruby→Python watch-outs:** you must hash the **raw bytes**, not the parsed-and-re-serialized JSON — re-serialization changes whitespace and key order and silently breaks verification. This is the single most common webhook bug.
- **Senior signal:** You know why constant-time comparison matters and can describe the replay window and key rotation.

### Day 4 — Idempotency
- **READ:** Stripe's idempotency documentation (the canonical treatment).
- **BUILD:** honour an `Idempotency-Key` header, writing the delivery record and the outbox row in **one transaction**.
- **Acceptance:** same key + same body → replays the identical stored response with **no new rows**; same key + *different* body → **409**; two concurrent duplicates → exactly one write (enforced by a unique constraint, not a check-then-insert).
- **Ruby→Python watch-outs:** at-least-once delivery is the norm for every webhook sender — the receiver is responsible for exactly-once *effects*. Same discipline as making a Sidekiq job idempotent.
- **Senior signal:** You can state the full same-key/different-body decision matrix without waffling.

### Day 5 — Durable background work (the outbox)
- **READ:** the "transactional outbox" pattern; Postgres `SELECT ... FOR UPDATE SKIP LOCKED`.
- **BUILD:** a CLI command that drains the outbox table, claiming rows with `FOR UPDATE SKIP LOCKED`.
- **Acceptance:** **kill the drain worker mid-batch, restart it, and pending rows still process.** Two workers running concurrently never process the same row.
- **Ruby→Python watch-outs:** the tempting answer is a thread pool — **don't**. A thread pool inside a web worker loses jobs on restart and re-creates the enqueue-before-commit bug. A DB-backed outbox ≈ Sidekiq's durability guarantee without Redis.
- **Senior signal:** You can explain why enqueuing *inside* the transaction (to a table) is safe while enqueuing to an external queue before commit is not.

### Day 6 — Query API, tests, README (DELIVERABLE)
- **BUILD:** `GET /v1/runs`, `/runs/<id>`, `/runs/<id>/results`; structured logging with a correlation id; a pytest suite; and a README section titled **"Why Flask here and Django for the platform app."**
- **Acceptance:** pytest green with coverage on the auth, idempotency, and drain paths; `mypy --strict` and `ruff` clean; a test greps log output for the HMAC secret and asserts **zero matches**; **pushed to GitHub**.
- **Senior signal:** You defend the framework choice explicitly — choosing assemble-your-own and articulating the tradeoff is itself the signal.

**Week 6 interview check:** (1) "How do you verify a webhook is authentic, and what's the classic bug?" (2) "Design idempotency for an endpoint that may be called twice concurrently."

---

## WEEKS 7–8 — Django + DRF (the Rails analog, 12 days)

**GitHub deliverable:** Django + DRF platform core with the N+1 before/after story.
**Framing:** Django Model = ActiveRecord, `manage.py migrate` = `rails db:migrate`, the free admin ≈ a better ActiveAdmin, QuerySets are lazy like AR relations. **Biggest Rails-brain shift: you don't write migrations by hand — `makemigrations` generates them from model changes.** Full spec: [`02-real-world-projects.md`](02-real-world-projects.md) → Project 3.

### Days 1–2 — Project vs app, models, migrations
- **READ:** Django tutorial parts 1–2.
- **BUILD:** a project plus one app; the core entities (Organization, User, Membership with a role, Project, EvalSuite, TestCase, ModelConfig, Run, Result, Metric); `makemigrations` + `migrate`; models registered in the admin; a superuser.
- **Acceptance:** dev server runs; models are editable in `/admin`; **`migrate` and `migrate <app> zero` both succeed** (your migrations are reversible); migrations committed.
- **Ruby→Python watch-outs:** a Django "project" holds many "apps" (a Rails app ≈ a Django app; the project ≈ the Rails app shell). `null=True` (database) and `blank=True` (validation) are separate concepts. There is no `save!` bang convention — validation is decoupled from saving by default.

### Days 3–4 — ORM: querysets, relationships, transactions
- **READ:** Django "Making queries"; the QuerySet API reference (skim); `transaction.atomic` docs.
- **BUILD:** in the shell, exercise filter/exclude/get, forward and reverse relations, and one aggregate. Add `__str__` and a couple of model methods. Wrap a multi-write operation in a transaction.
- **Acceptance:** reverse relations work; at least one `annotate`/aggregate returns correct numbers; **force an exception mid-transaction and assert nothing was written**.
- **Ruby→Python watch-outs:** QuerySets are **lazy** — no database hit until iterated or sliced (like AR relations). `.get()` raises `DoesNotExist`/`MultipleObjectsReturned`. Reverse FK accessors default to `<model>_set` unless you set `related_name`. `filter` ≈ `where`; `exclude` ≈ `where.not`.

### Days 5–6 — Views, URLs, admin for operators
- **READ:** Django tutorial parts 3, 4, and 7.
- **BUILD:** list and detail views wired through `urls.py`; customize the admin (`list_display`, filters, search).
- **Acceptance:** pages render real data including a path parameter; **a non-engineer could use your admin to find "all failed runs for project X this week."**

### Days 7–9 — DRF: serializers, viewsets, routers, permissions
- **READ:** the DRF tutorial — Serializers, Requests/Responses, ViewSets & Routers, Permissions.
- **BUILD:** serializers for the core models, `ModelViewSet`s registered with a router, pagination, filtering, and object-level permissions scoped to the caller's organization.
- **Acceptance:** the browsable API returns valid JSON for all models; create and update work; invalid payloads return 400 with field errors; **a user in Org A gets 404/403 (not 200) for Org B's objects — write that test.**
- **Ruby→Python watch-outs:** DRF serializers ≈ Grape Entities *fused with* StrongParameters — they both serialize **and** validate/deserialize. `ModelViewSet` + router ≈ `resources :things`.

### Days 10–12 — N+1, query counts, and ship (DELIVERABLE)
- **READ:** Django "Database access optimization"; `select_related`/`prefetch_related` reference.
- **BUILD:** instrument query counts with `assertNumQueries`. **Prove your nested serializer triggers N+1, then fix it.** Move aggregations into SQL with `annotate`/`aggregate`. Finalize README + push.
- **Acceptance:** a test shows the query count dropping from O(N) to a **bounded constant** after the fix, with the pre-fix count recorded; percentiles computed by SQL aggregation, not Python loops (verify with `.query` or query capture); API returns identical data before and after; **pushed to GitHub**.
- **Ruby→Python watch-outs:** `select_related` ≈ `includes`/`joins` for single-valued FK relations (a SQL JOIN); `prefetch_related` ≈ `includes` for collections (separate query, joined in Python). **Picking the wrong one doesn't error — it just doesn't help.**
- **Senior signal:** You look at a serializer and predict the query count, then name the right prefetch strategy. **Lead with this story in interviews** — it maps directly onto your Rails N+1 experience.

**Weeks 7–8 interview check:** (1) "Explain N+1 in Django and how `select_related` differs from `prefetch_related`." (2) "When does a QuerySet actually hit the database?"

---

## WEEK 9 — FastAPI + Pydantic v2 (6 days)

**GitHub deliverable (Day 6):** a Dockerized FastAPI service with Pydantic models and async endpoints.
**Why this week matters most for LLM/eval roles:** Pydantic is everywhere in tool-calling and eval schemas — learn it *well*, not just enough. Full spec: [`02-real-world-projects.md`](02-real-world-projects.md) → Project 4.

### Day 1 — FastAPI basics, path/query params, first Pydantic model
- **READ:** FastAPI tutorial "First Steps", "Path Parameters", "Query Parameters".
- **BUILD:** a few GET endpoints with typed path and query params returning a Pydantic model.
- **Acceptance:** the server runs; `/docs` auto-renders your endpoints; wrong-typed params return **422 automatically**; responses match the model.
- **Ruby→Python watch-outs:** routing is decorator-based, and **the type hints in the signature *are* the contract** — they drive parsing, validation, and docs. No Grape `params do ... end` block needed.

### Day 2 — Pydantic v2 in depth
- **READ:** Pydantic docs — Models, Validators (field + model), Settings management.
- **BUILD:** rich models: field constraints, a `field_validator`, a cross-field `model_validator`, a nested model, and `BaseSettings` loaded from environment variables.
- **Acceptance:** bad input is rejected with clear 422 field errors; the cross-field rule fires correctly; settings load from real env vars.
- **Ruby→Python watch-outs:** Pydantic ≈ ActiveModel validations + StrongParameters + coercion, but at the *type* boundary and much stricter. It **coerces** by default (a numeric string may become an int) — know when you want strict mode. Validators run **on construction**, unlike AR validations you trigger with `valid?`. This is **v2** — `field_validator`, not the v1 `@validator` you'll find in old tutorials.
- **Senior signal:** You can explain why Pydantic is ubiquitous in LLM tooling: every boundary is loosely-typed JSON you don't control — inbound requests, provider responses, tool-argument schemas, config.

### Day 3 — Request bodies, `response_model`, dependency injection
- **READ:** FastAPI tutorial "Request Body", "Response Model", "Dependencies".
- **BUILD:** POST/PUT endpoints with Pydantic bodies; shape output with `response_model` to hide internal fields; factor shared logic into a `Depends()` reused across two endpoints.
- **Acceptance:** excluded fields are genuinely absent from responses; **overriding the dependency in a test changes behavior with no code edits**; 422 on invalid bodies.
- **Ruby→Python watch-outs:** `Depends()` ≈ `before_action`/service-object injection, but resolved per-request and declared in the signature. Input and output should often be **different** model classes.

### Days 4–5 — async/await + async SQLAlchemy
- **READ:** FastAPI "Concurrency and async/await"; Real Python "Async IO in Python"; SQLAlchemy 2.0 async ORM docs.
- **BUILD:** add async persistence and CRUD-backed endpoints. Fan out concurrent calls with **bounded** concurrency (a semaphore), not an unbounded gather.
- **Acceptance:** data persists across requests; **no `time.sleep` or synchronous HTTP anywhere on the request path** (verify by grep and a loop-blocking test); with a fake slow provider that records in-flight count, **observed max concurrency never exceeds your configured ceiling**.
- **Ruby→Python watch-outs:** MRI Ruby is thread/GVL-based and mostly synchronous in your daily work. Python `async`/`await` is **cooperative single-threaded concurrency** — `await` yields to the event loop for I/O, it does **not** parallelize CPU work. Calling a blocking function inside an `async def` **stalls the entire event loop** — the top FastAPI mistake. (Note: a plain `def` endpoint is run in a threadpool by FastAPI, which is why mixing the two carelessly is subtle.)
- **⚠️ Highest-risk day of the week:** async SQLAlchemy + async migrations produce confusing greenlet errors. Front-load it — discover the problem here, not on Day 6.
- **Senior signal:** You explain what `await` actually does and why blocking calls in async routes are a bug — not just "async is faster."

### Day 6 — Docker + finalize (DELIVERABLE)
- **READ:** FastAPI "Deployment - Docker"; Docker's Python image docs.
- **BUILD:** a `Dockerfile` (uv-based, slim, pinned base) and `.dockerignore`; build and run the container.
- **Acceptance:** `docker build` succeeds; `docker run` serves the API and `/docs` from the container; `.dockerignore` excludes `.venv` and caches; base image and Python version **pinned** (no `:latest`); not running as root; README documents build + run; **pushed to GitHub**.
- **Ruby→Python watch-outs:** pin the base image and commit `uv.lock` for reproducibility — same discipline as `Gemfile.lock`. Don't ship `--reload` in the image.

**Week 9 interview check:** (1) "What does `await` actually do, and what breaks if you call a blocking function in an async route?" (2) "How does Pydantic v2 validation and coercion work, and why is it central to tool-calling and eval schemas?"

---

### Threading it together

Weeks 1–3 → your first repo (fundamentals). Weeks 4–5 → `evalctl` + `contracts/`. Week 6 → Flask. Weeks 7–8 → Django. Week 9 → FastAPI. That's **five GitHub deliverables** before the LLM half of the plan begins in [`05-curriculum-llm-and-flagship.md`](05-curriculum-llm-and-flagship.md).

Every day ends the same way: `ruff` clean, `mypy --strict` clean, `pytest` green, committed. If those three are green and the acceptance criteria are met, ping me for review.
