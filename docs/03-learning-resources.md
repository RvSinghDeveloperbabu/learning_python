# Learning Resources — LLM Evaluation & Agent Platform

A single consolidated reading list for the whole `python_learning/` workspace, organized by area. Within each area: **official docs first**, then high-signal books, talks, and extras. Every link is annotated with *what to use it for*.

> **How to use these — 30% reading / 70% building.** You already know how to program, model data, test, and ship; this is an idiom-and-tooling transfer, not a "learn to code" course. Budget roughly **30% of your time reading and 70% building** the sub-projects (`foundations/`, `flask-app/`, `django-app/`, `fastapi-app/`, `llm/agent-cli/`, `llm/eval-harness/`). Read the official docs for ground truth, skim every "getting started"/tutorial fast, and pull specifics *as you hit them while building* — do not read any book front-to-back. Treat "**mypy `--strict` clean**" and "**pytest green**" as hard, self-verifiable acceptance bars on every project. When a doc and a random blog disagree, the doc wins — most of the trained-into-you gotchas below come from tutorials lagging behind current versions.

> **Global version note (read once):** Target **Python 3.12 or 3.13** (3.13 is stable as of Oct 2024 and ships an improved async REPL plus the experimental free-threaded build — relevant given the async emphasis). `X | Y` unions and `match` need 3.10+; clean generics/type-alias syntax (`class Foo[T]`, `type Alias = ...`, PEP 695) and `@override` (PEP 698) need 3.12+. Everywhere you meet **Pydantic**, use **v2** (v1 APIs are incompatible: `model_validate`, `model_config`, `@field_validator`). Everywhere you meet **SQLAlchemy**, use **2.0 style**. These recur below.

---

## Core Python, Typing, Testing & Tooling

Treat this as a fast idiom-and-tooling transfer for a strong Rails senior, not a beginner course. Read official docs for ground truth, use the books to internalize idioms, skim Real Python only for the specific senior topics flagged.

### Official language & standard library (ground truth)

- **The Python Tutorial** — https://docs.python.org/3/tutorial/ — Skim, don't study. Read fast through modules/packages, exceptions, classes, and comprehensions; these are where Python's mental model diverges from Ruby. ~Half a day.
- **The Python Language Reference** — https://docs.python.org/3/reference/ — Reference, not a read-through. Go deep on exactly one page: the Data Model (below).
- **Data Model (dunder methods)** — https://docs.python.org/3/reference/datamodel.html — The single most important page for you. Python's answer to Ruby operator overloading, `respond_to?`, `method_missing`, and `inspect`. Understand `__init__`/`__repr__`/`__eq__`/`__hash__`, context managers (`__enter__`/`__exit__`; `with` ≈ Ruby block-with-ensure), iterators/generators, and `__getattr__`. Go deep.
- **The Python Standard Library** — https://docs.python.org/3/library/index.html — Reference. As a senior, bookmark and actually read: `dataclasses`, `enum`, `functools`, `itertools`, `collections`, `contextlib`, `pathlib`, `asyncio`, `logging`. This is your ActiveSupport replacement — mostly already in the stdlib.
- **PEP 8 (style) + PEP 20 (Zen)** — https://peps.python.org/pep-0008/ and https://peps.python.org/pep-0020/ — Read both once. PEP 8 you'll enforce with tooling (ruff/black); PEP 20 explains *why* Python favors explicit over magic — a real adjustment from Rails' convention-over-configuration.

### The Rails → Python mental model

There's no single canonical "Rails dev's guide to Python," so use an idiom guide plus direct concept mappings.

- **The Hitchhiker's Guide to Python** — https://docs.python-guide.org/ — Opinionated idioms, project structure, "how Pythonistas actually do it." Read the "Writing Great Code" section; skim the rest.
- **Talk: "Transforming Code into Beautiful, Idiomatic Python" (Raymond Hettinger, PyCon 2013)** — https://www.youtube.com/watch?v=OSGv2VnC0go — 50 min, still the best "stop writing it like another language" talk. Watch early to unlearn non-Pythonic reflexes.
- **Tooling map to keep in your head:** Gemfile/Bundler → `pyproject.toml`/uv · RSpec → pytest · RuboCop → ruff · Sorbet → mypy · gem → wheel on PyPI · `method_missing`/`define_method` → `__getattr__`/dunder methods/descriptors · blocks & `yield` → context managers, generators, higher-order functions · Rails autoloading → **explicit imports** (no magic — this trips up every Rails dev). Semantic traps: Python has **no `private`** (convention `_name` only), variables are **references**, and default mutable arguments are evaluated **once** — a classic senior gotcha.

### Type hints + static checking

- **`typing` module docs** — https://docs.python.org/3/library/typing.html — Your annotation reference. Learn `Optional`/`| None`, `Union`/`|`, generics, `Protocol` (structural typing — closer to Ruby duck-typing than nominal interfaces), `TypedDict`, `Literal`, `Callable`, `Self`. **Version-sensitive:** prefer `list[int]`/`str | None` (3.10+) over the old `List`/`Optional` forms in older tutorials.
- **Static Typing with Python (typing docs)** — https://typing.readthedocs.io/en/latest/ — The community "how to actually use types well" guide, with a good Protocols section and gradual-typing strategy. Read the guides, skim the spec.
- **mypy documentation** — https://mypy.readthedocs.io/en/stable/ — Go deep enough to run `--strict` and configure it in `pyproject.toml`. "mypy clean under strict" is a hard acceptance bar on every project — your closest thing to the compiler-backed confidence you had via Sorbet.
- **pyright (one-line mention)** — https://microsoft.github.io/pyright/ — The type checker behind VS Code/Pylance; often catches *different* issues than mypy. Not a replacement for the "mypy `--strict` clean" bar, but seniors are expected to know both exist and that they can disagree.

### Testing

- **pytest** — https://docs.pytest.org/en/stable/ — Your RSpec replacement, better in some ways. Study **fixtures** (DI setup, scopes, `yield` fixtures ≈ `let`/`before`), **parametrize** (table-driven tests), `monkeypatch`, and `conftest.py`. Also read `unittest.mock` — https://docs.python.org/3/library/unittest.mock.html — for `Mock`/`patch`/`autospec` (your `double`/`allow`/`expect`).
- **pytest-asyncio** — https://pytest-asyncio.readthedocs.io/ — **Required, not optional.** You cannot test `async def` FastAPI routes, `httpx.AsyncClient` calls, or `asyncio.TaskGroup` eval runners without it. Learn the `asyncio_mode` config and `@pytest.mark.asyncio`.
- **anyio (optional alternative)** — https://anyio.readthedocs.io/ — Starlette/FastAPI run on AnyIO; its pytest plugin is an alternative to pytest-asyncio and lets you test against both asyncio and trio backends. Know it exists.
- **Hypothesis (property-based testing)** — https://hypothesis.readthedocs.io/en/latest/ — Senior differentiator. Use on `eval-harness` parts where invariants matter (parsers, scorers, serializers) — finds edge cases table tests miss. Learn `@given` + strategies; medium depth.
- **testcontainers-python** — https://testcontainers-python.readthedocs.io/ — Spin up a real ephemeral Postgres/Docker for integration tests instead of SQLite. Pairs directly with the docker-py entry below and is thematically perfect given the sandbox/eval-runner work — senior-grade fidelity in your test suite.

### Packaging & tooling (uv, pyproject, ruff, black)

- **uv** — https://docs.astral.sh/uv/ — Modern, fast package/venv/project manager (Astral): your Bundler + rbenv + pip in one. Learn `uv init`, `uv add`, `uv run`, lockfiles, and **workspaces** (useful since each sub-project is its own venv). Go deep — it's the backbone of your workspace setup.
- **Python Packaging User Guide** — https://packaging.python.org/en/latest/ — The official "how packaging actually works" (PyPI, wheels, sdists, `pyproject.toml` metadata, entry points). Read the pyproject.toml/project-metadata and "packaging a project" sections so your `[project]` tables aren't cargo-culted.
- **ruff** — https://docs.astral.sh/ruff/ — Linter *and* formatter in one (replaces flake8/isort, can replace black). Your RuboCop. Configure rule sets in `pyproject.toml`; run in CI. Medium depth.
- **black** — https://black.readthedocs.io/en/stable/ — The uncompromising formatter and de-facto standard for *what* formatted Python looks like. Even if you format with ruff, read black's "code style" page to understand the conventions everyone expects. Skim.

### Senior-grade books & references

- **Fluent Python, 2nd ed. (Luciano Ramalho)** — https://www.fluentpython.com/ — The book for your exact situation: a strong programmer who wants *idiomatic* Python, not translated Ruby. Deep on the data model, sequences, dataclasses, closures/decorators, type hints, concurrency/async. 2nd ed. is current for modern typing. Your primary reference across the 8 weeks.
- **Effective Python, 3rd ed. (Brett Slatkin)** — https://effectivepython.com/ — **Use the 3rd edition (Nov 2024)**, which covers Python through **3.13**, expands 90→**125 items**, and adds two new chapters on **robustness and performance** — directly on-theme for this platform (the older 2nd ed. is a version behind your own "target 3.12+" guidance). Faster day-to-day ROI than Fluent Python; cherry-pick the items relevant to what you're building.
- **Robust Python (Patrick Viafore, O'Reilly)** — https://www.oreilly.com/library/view/robust-python/9781098100650/ — The single best book-length match for your hard acceptance bar ("mypy `--strict` clean on every project"): entirely about using the type system, user-defined types, generics, and testing as a safety net. Explicitly *not* a first Python text — pitched at exactly your level. Read alongside mypy.
- **Architecture Patterns with Python / "Cosmic Python" (Percival & Gregory)** — https://www.cosmicpython.com/ — **Free online.** Repository, Unit of Work, Service Layer, DI, and event-driven design in Python — directly relevant to a production-grade eval/agent platform, and explicitly aimed at developers from other OO/enterprise backgrounds (you). Read when you start structuring the FastAPI/service layers.
- **Real Python (selected senior topics only)** — https://realpython.com/ — High-signal, but ignore beginner tracks. Use targeted articles on **asyncio/concurrency**, **descriptors & metaclasses**, **`__slots__`/dataclasses vs attrs**, **context managers**, and **decorators**. Reach for it when a stdlib page is too terse; don't read it linearly.

---

## Flask

### Core & App Structure

- **Flask official docs** — https://flask.palletsprojects.com/en/stable/ — Your primary reference. Skim the Quickstart fast (you know HTTP/routing), then read Configuration, **Application Context vs Request Context**, and Error Handling closely — the context model is the one genuinely un-Rails-like concept.
- **Application Factories pattern** — https://flask.palletsprojects.com/en/stable/patterns/appfactories/ — Read in full. The production-grade `create_app()` layout (vs a global `app`) that lets you configure per-environment and test cleanly. Treat as mandatory.
- **Blueprints** — https://flask.palletsprojects.com/en/stable/blueprints/ — Read in full. Flask's answer to Rails engines/namespaced controllers; how you split `auth`, `evals`, `runs` into modules. Pair with the factory above.
- **Flaskr tutorial** — https://flask.palletsprojects.com/en/stable/tutorial/ — Optional but efficient: one end-to-end pass showing factory + blueprints + DB + tests wired together. Read the structure, skip the hand-holding.

### Data & Migrations

- **Flask-SQLAlchemy** — https://flask-sqlalchemy.palletsprojects.com/en/stable/ — Your ActiveRecord analog for Flask. **Version-sensitive:** 3.x targets **SQLAlchemy 2.0**; prefer modern `db.session.execute(select(...))` over legacy `Model.query`. Confirm you're on 3.x.
- **SQLAlchemy 2.0 ORM docs** — https://docs.sqlalchemy.org/en/20/orm/quickstart.html — Go one level below the Flask wrapper: ORM Quickstart, `select()`/`Session` usage, relationship loading. **Flag:** most StackOverflow/blog answers show 1.x-era `query` syntax — verify against 2.0 before trusting.
- **Flask-Migrate** — https://flask-migrate.palletsprojects.com/en/latest/ — Thin wrapper over Alembic (= Rails migrations). Read it fully, then skim **Alembic autogenerate** — https://alembic.sqlalchemy.org/en/latest/autogenerate.html — since autogenerate misses some changes (enum/type edits) and a senior reviews generated migrations by hand.

### Auth / HMAC

- **Python `hmac` module** — https://docs.python.org/3/library/hmac.html — Reference for signing/verifying webhook and API requests. Note `hmac.compare_digest` for constant-time comparison — the timing-attack detail interviewers probe. Short read.
- **Werkzeug security helpers** — https://werkzeug.palletsprojects.com/en/stable/utils/#module-werkzeug.security — `generate_password_hash`/`check_password_hash` (bcrypt/scrypt/pbkdf2) for credential storage. ~10 min.
- **Stripe webhook signature verification** — https://docs.stripe.com/webhooks/signatures — Best real-world worked example of HMAC-over-raw-body + timestamp-tolerance (replay protection). Read the algorithm section; mirror this scheme for signed run/eval webhooks.

---

## Django + DRF

### Core, ORM & Admin

- **Django docs + polls tutorial** — https://docs.djangoproject.com/en/stable/ and https://docs.djangoproject.com/en/stable/intro/tutorial01/ — **Version-sensitive:** `stable` currently resolves to **Django 5.2 LTS**; stay on 5.x. Do the tutorial once quickly to absorb batteries-included conventions (settings, apps, URLconf, `manage.py`), then use topic guides as reference.
- **Making queries (ORM)** — https://docs.djangoproject.com/en/stable/topics/db/queries/ — Core reading. QuerySets are lazy (unlike eager ActiveRecord relations) and chainable; internalize when a query actually hits the DB, plus `F()`/`Q()` and `annotate`/`aggregate`.
- **Database access optimization + `select_related`/`prefetch_related`** — https://docs.djangoproject.com/en/stable/topics/db/optimization/ and https://docs.djangoproject.com/en/stable/ref/models/querysets/#select-related — Read both closely; your N+1 toolkit. `select_related` = JOIN (FK/one-to-one), `prefetch_related` = second query + Python join (M2M/reverse FK) — analog to Rails `includes`, but you choose the strategy explicitly.
- **Migrations** — https://docs.djangoproject.com/en/stable/topics/migrations/ — Django's built-in migrations (no Alembic here). Read data migrations, `RunPython`, and squashing; review auto-generated migrations like Rails schema changes.
- **Django admin** — https://docs.djangoproject.com/en/stable/ref/contrib/admin/ — A genuine senior differentiator with no Rails equivalent: a near-free internal CRUD backoffice. Read `ModelAdmin`, `list_display`/`list_filter`, inlines, `readonly_fields` — enough to expose orgs/projects/eval-suites to ops users.

### Django REST Framework

- **DRF docs (tutorial + api-guide)** — https://www.django-rest-framework.org/ — Start with the tutorial for the request/response/router flow, then live in the API Guide. Prioritize **Serializers & ModelSerializer** — https://www.django-rest-framework.org/api-guide/serializers/ — your Grape entities analog — plus ViewSets/Routers, Authentication, Permissions, Pagination. Read serializer validation carefully; it's where most real API logic lives.

### Books

- **Django for APIs (W. S. Vincent)** — https://djangoforapis.com/ — Focused, current, DRF-first; best single book for your API-building target. Skim the Django-101 opening, spend time on auth (token/JWT) and permissions chapters.
- **Two Scoops of Django (Feldroy)** — https://www.feldroy.com/books/two-scoops-of-django-3-x — Read for opinionated production **conventions** (project layout, settings management, fat-models-vs-services, gotchas) — the senior-judgment layer. **Flag:** latest edition covers Django 3.x — patterns hold, but cross-check any version-specific API against the 5.x docs above. Still the best production-conventions book despite the age.

---

## FastAPI + Pydantic v2 + SQLAlchemy (async)

Skim the "getting started" material fast (you know HTTP, ORMs, DI, migrations); slow down on the async/typing/lifecycle sections where the Python model genuinely differs from Rails.

> **Version flags (read once, save hours):**
> - **Pydantic v2 ≠ v1.** APIs renamed (`.dict()`→`.model_dump()`, `@validator`→`@field_validator`, `Config` class→`model_config`); validation is Rust-backed (`pydantic-core`). Ignore any v1 tutorial. FastAPI ≥0.100 assumes v2.
> - **SQLAlchemy 2.0 ≠ 1.x.** Use "2.0 style" only: `Mapped[...]`/`mapped_column`, `select()` + `session.execute()`, `async_sessionmaker`. Any tutorial using `Query`/`session.query()` is legacy.
> - **Python 3.11+** for `asyncio.TaskGroup` and `asyncio.timeout()`. Target **3.12 or 3.13** for your platform.

### FastAPI + ASGI core

- **FastAPI docs** — https://fastapi.tiangolo.com/ — Your primary reference. Read the full Tutorial (dependencies, security/OAuth2, request/response models, background tasks) and all of the Advanced section deeply; the backbone of `fastapi-app/`.
- **FastAPI "Concurrency and async / await"** — https://fastapi.tiangolo.com/async/ — Read carefully. Explains when a path op runs on the event loop vs a threadpool — the #1 thing Rails devs get wrong (blocking sync calls inside `async def`).
- **FastAPI lifespan events** — https://fastapi.tiangolo.com/advanced/events/ — Use the `lifespan` context manager for startup/shutdown (DB pools, HTTP clients). The old `@app.on_event` is deprecated — don't copy it from older blogs.
- **Starlette docs** — https://www.starlette.io/ — FastAPI is built on this. Go one level down for middleware, `StreamingResponse`, `BackgroundTask`, and testing internals FastAPI doesn't re-document.
- **Uvicorn docs** — https://www.uvicorn.org/ — Skim. Deployment settings, workers, `--reload` in dev, how it hosts the ASGI app; pair with a process-manager/Gunicorn-worker note for prod.

### Pydantic v2

- **Pydantic v2 docs** — https://docs.pydantic.dev/latest/ — Read Concepts → Models, Fields, Validators, Serialization deeply. Your validation + DTO layer (think ActiveModel validations + strong params, but type-driven).
- **Pydantic v1→v2 migration guide** — https://docs.pydantic.dev/latest/migration/ — Skim once as a "what changed" map so you can translate any v1 example you hit online into v2.
- **pydantic-settings** — https://docs.pydantic.dev/latest/concepts/pydantic_settings/ — Now a **separate package** (`pip install pydantic-settings`), not built into core v2. Use it for typed, env-var-driven config across every sub-project.

### SQLAlchemy 2.0 + migrations (async)

- **SQLAlchemy 2.0 Unified Tutorial** — https://docs.sqlalchemy.org/en/20/tutorial/index.html — Read fully in 2.0 style. Coming from ActiveRecord, invest here: SQLAlchemy separates Core (SQL expression) from ORM and makes Unit-of-Work/`Session` explicit — no magic auto-flush-on-attribute like AR.
- **SQLAlchemy asyncio extension** — https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html — Read closely. `create_async_engine`, `AsyncSession`, and the gotchas: no implicit lazy-loading in async (use `selectinload`/`joinedload` eagerly — your N+1 instincts transfer directly).
- **Alembic docs** — https://alembic.sqlalchemy.org/en/latest/ — Migrations (the `rails db:migrate` equivalent). Read the tutorial + autogenerate; know its limits (autogenerate misses some changes — review every generated script). **Async gotcha to flag loudly:** initialize async projects with **`alembic init -t async`** — the default template's `env.py` is sync-only and will bite you on `AsyncSession`. One line saves an afternoon.

### asyncio (fundamentals)

- **asyncio official docs** — https://docs.python.org/3/library/asyncio.html — Reference, not a read-through. Focus on the high-level API: `run`, `gather`, `TaskGroup`, `timeout`, and `Task`/`Future` semantics. Node-style concurrency but explicit.
- **David Beazley — "Python Concurrency From the Ground Up: LIVE!" (PyCon 2015)** — https://www.youtube.com/watch?v=MCs5OvhV9S4 — 45 min, high signal. Builds an event loop live so `async`/`await` stops feeling like magic; the best single mental-model primer for someone with no prior async exposure. Companion code: https://github.com/dabeaz/concurrencylive.

### httpx (async HTTP client) + resilience

- **HTTPX docs** — https://www.python-httpx.org/ — Requests-compatible sync + async client. Read the Async and Advanced (connection pools, timeouts, transport-level retries) pages — this is how `agent-cli`/`eval-harness` call model providers concurrently.
- **tenacity** — https://tenacity.readthedocs.io/ — HTTPX's built-in retries are limited to connection errors; for retrying flaky/429'd **provider API calls** with backoff + jitter, tenacity is the idiomatic answer. Wire it into `agent-cli/` and `eval-harness/` around provider calls.

### Streaming / SSE (for token streaming)

- **sse-starlette** — https://github.com/sysid/sse-starlette — The practical way to do Server-Sent Events (streaming LLM tokens) from FastAPI. Read the README + `EventSourceResponse`; understand it's just a long-lived async generator over the response body.
- **MDN — Using server-sent events** — https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events — The protocol itself (event framing, `data:`/`event:` lines, reconnection). Skim so you know what your endpoint must emit — and when to reach for WebSockets instead.

### Docker for Python (deployment)

- **Astral `uv` Docker integration guide** — https://docs.astral.sh/uv/guides/integration/docker/ — Since your workspace is uv-managed, the canonical way to containerize: multi-stage builds, `uv sync --frozen`, cached layers. Directly applicable to shipping each sub-project.
- **Docker official Python language guide** — https://docs.docker.com/language/python/ — General container best practices (slim base images, non-root user, `.dockerignore`, layer caching). Skim for fundamentals if Docker itself is newer to you.

---

## Observability (cross-cutting, senior differentiator)

The project rules demand observability; stdlib `logging` alone isn't enough for a "platform." Wire these into the FastAPI service and the eval-run pipeline.

- **structlog** — https://www.structlog.org/ — Structured/contextual logging, the idiomatic production choice. Use for machine-parseable JSON logs with bound context (request id, org, run id) flowing through the eval pipeline.
- **OpenTelemetry Python** — https://opentelemetry.io/docs/languages/python/ — Tracing and metrics for the FastAPI service and eval-run pipeline (spans across provider calls, sandbox execution, DB). A genuine senior differentiator for a platform — instrument the async request path and the eval runner end-to-end.

---

## LLM Tooling & Evaluation

Your differentiator area. Official provider docs first, then agent-pattern references, SDKs, MCP, and the evaluation/sandbox stack you'll wire into `llm/agent-cli/` and `llm/eval-harness/`. Read concept pages closely; skim SDK references and pull specifics as you build.

> **Version flags throughout:**
> - **Pydantic v2** is the norm; both provider SDKs lean on it for typed tool schemas / structured outputs. Learn v2, not v1.
> - **OpenAI Python SDK** uses a **client-instance pattern** (not module-level `openai.*`) and newer code uses the **Responses API**, not just legacy Chat Completions — know which one a snippet targets. (Don't tie this to a literal "v1.x" version number; the load-bearing distinction is the client pattern + Responses vs Chat Completions, not the version digits.)
> - **Anthropic** pins an `anthropic-version` header and uses the **Messages API** (not the old Completions API). Requires Python 3.9+; target 3.12+.
> - Anthropic docs moved to `platform.claude.com` (old `docs.anthropic.com`/`docs.claude.com` links redirect).

### Function calling & tool use — provider docs (start here)

- **Anthropic — Tool use overview** — https://platform.claude.com/docs/en/build-with-claude/tool-use/overview — The canonical mental model: client vs server tools, `tool_use`/`tool_result` round trip, `tool_choice`, and `strict: true` schema conformance. Read fully; then follow the linked "How tool use works" and the "Build a tool-using agent" tutorial for the agentic loop.
- **OpenAI — Function calling guide** — https://platform.openai.com/docs/guides/function-calling — Same concept, second dialect. Read to see where OpenAI differs (tool schema shape, parallel tool calls, strict mode). Note whether examples use the Responses API vs Chat Completions — your `agent-cli` should abstract over both providers.

### Model Context Protocol (MCP) — your standout differentiator

Directly relevant to target role #1 (Agent Function-call) and your existing MCP server; wire this into `agent-cli/`.

- **MCP docs** — https://modelcontextprotocol.io — The concepts and host/client/server architecture. Read to align your existing MCP work with the current spec's vocabulary.
- **MCP specification (date-versioned)** — https://modelcontextprotocol.io/specification/2025-11-25 — The spec is **date-versioned**; the latest revision is **2025-11-25**. When defending design choices, cite a *dated* revision, not "latest," so your reasoning stays pinned.
- **Official MCP Python SDK** — https://github.com/modelcontextprotocol/python-sdk — Reference for building servers/clients. **Version trap to flag loudly:** the SDK is mid-transition to **v2 (pre-release; stable v2 targeted ~2026-07-27)**, and in v2 the bundled **`FastMCP` server class is renamed `MCPServer`**. Separately, the **standalone FastMCP (Prefect, `gofastmcp.com`)** has diverged from the SDK-bundled FastMCP — a real "which FastMCP is this tutorial using?" gotcha, exactly like the Pydantic v1/v2 problem. Confirm which package and major version any snippet targets before trusting it.
- **Anthropic MCP connector docs** — https://platform.claude.com/docs/en/agents-and-tools/mcp-connector — Call remote MCP servers directly from the Messages API without a separate client — relevant to wiring your MCP work into `agent-cli/`.

### Agent patterns & prompting (design, not framework lock-in)

- **Anthropic — Building Effective Agents** — https://www.anthropic.com/research/building-effective-agents — The single best "how to think about it" piece: when a plain workflow beats an agent, and the core patterns (prompt chaining, routing, orchestrator-workers, evaluator-optimizer). Read closely — this shapes your architecture. (Anthropic also serves it at the now-more-common `/engineering/building-effective-agents` path; either resolves — don't be surprised by the variant.)
- **Anthropic Cookbook (claude-cookbooks) — agent patterns** — https://github.com/anthropics/claude-cookbooks/tree/main/patterns/agents — Reference implementations of those patterns (the repo was renamed from `anthropic-cookbook`; the old URL redirects). Now also includes an **async multi-agent orchestration** example worth studying for `agent-cli/`. Treat as architecture reference — you'll re-implement the loop yourself, not copy-paste.
- **Prompt Engineering Guide — Agents** — https://www.promptingguide.ai/agents — Concise vendor-neutral survey (planning, memory, tool use, common failure modes). Skim for shared vocabulary and to sanity-check your design against known pitfalls.
- **Prompt Engineering Guide — Function calling** — https://www.promptingguide.ai/applications/function_calling — Short applied walkthrough of turning NL into API calls. Quick read; good for framing tool-description quality (the part most engineers underinvest in).

### SDKs — reference while building (version-sensitive)

- **Anthropic Python SDK** — https://github.com/anthropics/anthropic-sdk-python — Client setup, streaming, typed params, retries/timeouts, async client. Skim the README + `/api.md`; lean on typed tool params. Python 3.9+, Messages API.
- **OpenAI Python SDK** — https://github.com/openai/openai-python — Same, for the OpenAI side. Pay attention to the client-instance pattern, async usage, and structured outputs via Pydantic v2. Reference, not front-to-back reading.

### Evaluation — benchmarks & harnesses (the core of `eval-harness/`)

- **SWE-bench — site/leaderboard** — https://www.swebench.com — Orientation: what the task actually is (generate a patch that resolves a real GitHub issue) and the variants (Verified, Lite, Multimodal, Multilingual). Read to understand what "passing" means and which split to target.
- **SWE-bench — GitHub repo** — https://github.com/SWE-bench/SWE-bench — Study the harness architecture: task instances, patch application, Docker-per-instance execution, pass/fail via the repo's own tests. The reference design for your own eval runner. **Needs Docker; x86_64 strongly recommended** (Apple Silicon/arm has known caveats — plan your runner accordingly).
- **SWE-bench — paper** — https://arxiv.org/abs/2310.06770 — "Can Language Models Resolve Real-World GitHub Issues?" Read methodology + limitations for why the dataset is built the way it is and how contamination/flaky-test concerns are handled — senior context for defending eval design.
- **SWE-bench Verified (OpenAI)** — https://openai.com/index/introducing-swe-bench-verified/ — Why a human-filtered subset exists and how noisy benchmarks get cleaned. Short read; the "how we validated task solvability" reasoning is directly reusable in your repository-validation target role.
- **EleutherAI lm-evaluation-harness** — https://github.com/EleutherAI/lm-evaluation-harness — The de-facto reference for eval-harness *architecture*: task registry, pluggable model backends (incl. OpenAI/Anthropic APIs), metrics/aggregation, reproducibility. Skim the docs + a couple of task YAMLs to steal structural ideas (results schema, run isolation, metric plumbing).

### Sandboxed execution (running agent/model-generated code safely)

- **Docker SDK for Python (docker-py)** — https://docker-py.readthedocs.io/en/stable/ — Programmatic containers/images/exec — how you spin up isolated, resource-limited sandboxes per eval run or per agent tool call. Read the containers + exec + low-level API sections. **Requires a running Docker daemon**; mind image cleanup, timeouts, and network isolation for untrusted code. (Pairs with **testcontainers-python** above for integration tests.)

---

**Two suggested reading orders**

- *Agent function-call role:* Anthropic tool use → OpenAI function calling → MCP docs/spec + Python SDK → Building Effective Agents → cookbook patterns (incl. async multi-agent) → build `agent-cli/` alongside, with tenacity around provider calls.
- *Eval / repo-validation role:* SWE-bench (site → repo → paper → Verified) → lm-evaluation-harness → docker-py + testcontainers → build `eval-harness/` alongside, instrumented with structlog + OpenTelemetry.
