# PROGRESS — Ravi's Python + LLM-Eval Journey

> **Mentor:** read this at the **start** of every session (CLAUDE.md §5.1) and update it at the **end** (§5.6, §10). This is the memory that makes the 14 weeks a coherent arc. Log honestly — including reveals and recurring gaps — even when unflattering.

**Status:** 🟢 In progress — Week 1 Day 1 (`fundamentals/`) · Week 0 was 3/4, application #1 deferred
**Started:** 2026-07-13
**Current focus:** `docs/07-python-fundamentals.md` **Day 1** — create `fundamentals/`, write the argv-greeting program under a `__main__` guard.
**Target:** 14 weeks · 3–4 hrs/day · **6 days/week** · ~30% reading / 70% writing

Legend: `[ ]` todo · `[~]` in progress · `[x]` done · `[-]` cut/skipped (swing item)

> **Schedule source of truth:** [`Ravi_Python_LLM_Learning_Plan.md`](Ravi_Python_LLM_Learning_Plan.md). Daily lessons for Weeks 1–3: [`docs/07-python-fundamentals.md`](docs/07-python-fundamentals.md).

---

## Week 0 — Setup ✅ (3/4)
- [x] Confirm Python 3.12+ working — 3.13.14 (2026-07-13)
- [x] Install `uv`; create a throwaway venv, install a package, run a script (prove the toolchain) — `uv-scratch` project + httpx, isolation shown by import failing outside the project (2026-07-13)
- [x] VS Code + Python + Pylance working — interpreter on `.venv`, `httpx.` autocompletes from package docstrings (2026-07-13)
- [~] **Apply to "LLM Trainer – Agent Function Call" role** — DEFERRED (not yet submitted) as of 2026-07-14. Non-code; mentor helps draft on request. Flip to [x] only when actually sent.

## Weeks 1–3 — Python fundamentals → `fundamentals/`
_One contact-book program, grown daily. No `mypy --strict`, comprehensions, generators, or decorators until Day 18._

**Week 1 — absolute basics**
- [ ] D1 — interpreter, `uv run`, `__main__` guard → argv greeting
- [ ] D2 — numbers, strings, f-strings, `None`, truthiness → tip calculator
- [ ] D3 — `if`/`elif`, `for`, `while`, `range` → FizzBuzz + guessing loop
- [ ] D4 — lists and tuples (no comprehensions) → to-do list
- [ ] D5 — dicts and sets → **contact book v1**
- [ ] D6 — flex: rebuild an earlier program from a blank file

**Week 2 — functions, objects, failure, files**
- [ ] D7 — functions, defaults, kwargs → refactor into functions
- [ ] D8 — classes I: `__init__`, `self`, `__repr__` → `Contact` class
- [ ] D9 — classes II: equality/hashing, `@property`, `super()`
- [ ] D10 — exceptions + EAFP → clean CLI errors, custom exception type
- [ ] D11 — files, `with`, `pathlib` → save and reload
- [ ] D12 — flex / review

**Week 3 — structure, data, tests, tooling**
- [ ] D13 — modules, imports, packages, console entry point
- [ ] D14 — JSON + dataclasses → JSON storage
- [ ] D15 — `logging` + first type hints (annotations only)
- [ ] D16 — pytest, first real suite (5+ tests, one asserting a raise)
- [ ] D17 — fixtures, parametrize, monkeypatch, capsys
- [ ] D18 — **tooling gate:** ruff + `mypy --strict` + pytest green
- **Deliverable:** first Python repo → GitHub

## Weeks 4–5 — `foundations/` (`evalctl`) + `contracts/`
- [ ] Comprehensions + generator expressions; generators (`yield`) for streaming
- [ ] Type hints + `mypy --strict` properly; `*args`/`**kwargs`, keyword-only
- [ ] `collections` (`Counter`, `defaultdict`) + `pathlib` depth; `itertools`/`functools`
- [ ] Context managers you author + decorators (`functools.wraps`)
- [ ] `Protocol` / `TypedDict` / `Literal` — typed duck typing (feeds agent-cli + eval-harness)
- [ ] Publish the shared `contracts/` JSON schemas (test-case / run / result, versioned)
- **Deliverable:** `evalctl` CLI — type-hinted, `mypy --strict` clean, passing pytest suite → GitHub

## Week 6 — `flask-app/` (ingestion & webhooks) · first web framework
- [ ] App factory + blueprints; SQLAlchemy 2.0 + migrations
- [ ] HMAC verification over **raw bytes** + API keys + freshness window
- [ ] Idempotency keys (same key/same body vs same key/different body vs concurrent)
- [ ] Durable outbox drained with `FOR UPDATE SKIP LOCKED`; query API
- **Deliverable:** Flask ingestion service → GitHub · _(if badly behind: depth-cut to a 3-day tour, never dropped)_

## Weeks 7–8 — `django-app/` (platform system of record)
- [ ] Domain model: orgs, users/roles, projects, eval suites, test cases, model configs, runs, results
- [ ] Migrations (reversible); Django admin configured for ops
- [ ] DRF: viewsets, serializers (nested), pagination, filtering, permissions
- [ ] Multi-tenant isolation — a test proving Org A cannot read Org B's data
- [ ] ORM depth: create then FIX N+1 (`assertNumQueries` before/after), SQL aggregations, transactions
- **Deliverable:** Django + DRF platform core → GitHub

## Week 9 — `fastapi-app/` (async LLM gateway / eval-runner)
- [ ] Pydantic v2 models, validators, `BaseSettings`
- [ ] Async correctness: bounded concurrency, **no event-loop blocking** (proven by test)
- [ ] Dependency injection (+ override in tests); `response_model` shaping
- [ ] Async SQLAlchemy persistence; Dockerized; OpenAPI docs
- [ ] OpenAI adapter = **SWING ITEM** (MVP ships Anthropic + a fake adapter)
- **Deliverable:** Dockerized FastAPI gateway → GitHub

## Week 10 — SWE-bench, Docker, reading real repos, first OSS PRs
- [ ] SWE-bench methodology: FAIL_TO_PASS / PASS_TO_PASS, execution-based grading (written spec)
- [ ] Docker fundamentals; Dockerize a pure-Python OSS library, suite green
- [ ] Trace a closed issue → the fix PR → the test that verifies it
- [ ] A repeatable method for reading an unfamiliar codebase (1-page map in ~90 min)
- [ ] **2 small OSS PRs**, each naming its verifying test
- **Deliverable:** written SWE-bench spec + 2 PRs

## Weeks 11–12 — `llm/agent-cli/` (function-calling agent)
- [ ] Anthropic + OpenAI SDKs behind one interface; streaming
- [ ] Tool schemas (JSON); the full tool-use loop (request → execute → feed back → loop)
- [ ] Agent loop: registry + dispatch, stop conditions, hard step cap
- [ ] Pydantic validation of tool args → corrective tool result, not an exception
- [ ] 2–3 real tools sandboxed; `apply_patch` = internal cut line
- [ ] Structured trace; guardrails; **secret redaction proven by a grep test**
- **Deliverable:** CLI function-calling agent → GitHub

## Weeks 13–14 — `llm/eval-harness/` (FLAGSHIP)
- [ ] Task spec format (repo, base commit, patch, test command, fail_to_pass/pass_to_pass, lockfile)
- [ ] Docker sandbox: checkout → apply patch → run tests (timeouts + resource limits, zero leaked containers)
- [ ] JUnit-XML parsing → verdict taxonomy: **RESOLVED / UNRESOLVED / ERROR** (never conflated)
- [ ] `report.json` conforming to `contracts/` + captured logs
- [ ] Small task dataset with vendored lockfiles; reproducibility; clean CLI
- **Deliverable:** flagship eval-harness repo w/ excellent README → GitHub

## Closeout (alongside weeks 13–14, non-code)
- [ ] Resume: add Python + LLM-eval section; re-lead with MCP / function-calling / OAuth
- [ ] Apply to Senior Python Developer + LLM Evaluation / Repo-Validation roles
- [ ] Interview prep: practice explaining reasoning aloud (half the grade)

---

## 📓 Session log
_(newest first — the mentor appends one entry per session)_

| Date | Week/Day | Worked on | Shipped | Interview Qs (verdict) | Notes |
|---|---|---|---|---|---|
| 2026-07-20 | — | **Plan restructure** — re-scoped to 14 weeks for a genuine Python beginner; Flask promoted to first web framework | New `docs/07-python-fundamentals.md` (18 beginner days); plan file rewritten as canonical map; all 13 schedule-bearing docs reconciled; 2 broken curriculum links + the stale tracker path in `CLAUDE.md` fixed | — | Root cause named: curriculum assumed "skip beginner material" (true of programming, false of Python). Tooling gate moved from Week 1 → Week 3 Day 18. |
| 2026-07-20 | 1 / d1 | Status check on `foundations/` scaffold | Dev-dependency classification fixed correctly (all 3 tools moved to `[dependency-groups] dev`, `[project].dependencies` emptied) | — | ⚠️ Under-practice: 5 days since 07-15, only one config fix. `main.py` still the `uv init` stub, test file empty (pytest collects 0), mypy strict still off, nothing committed since `7ea3f86`. |
| 2026-07-13 | 0 | Toolchain setup — Python 3.13.14, `uv` project + httpx isolation proof, VS Code + Pylance verified | Working env (3/4 Week-0 criteria); throwaway `uv-scratch` proof | — (setup day; none run yet) | Recurring gap logged: declares "done" before verifying (×2). Picked up `main()` + `if __name__` guard fast. |
| — | 0 | _not started_ | — | — | tracker created |

## 🔁 Recurring gaps to watch
_(the mentor names patterns here and resurfaces them in reviews + interviews — §10)_
- **Declares "done" before verifying** — Week 0 (2026-07-13), seen ×2: ran the `uv init` stub and called it a package test before adding `import httpx`; called Pylance "done" at extension-install before checking interpreter/autocomplete. "Installed/ran" ≠ "verified passing" — and that exact distinction *is* the LLM-eval/repo-validation job. Resurface in every review: make him state *how* he'll verify before he claims done.
- **Stalls in setup; little code actually written** — 2026-07-15 → 2026-07-20: five days elapsed, one config fix shipped, zero lines of his own Python. Scaffolding/tooling is comfortable territory (it resembles Rails config work); writing unfamiliar Python is not. Plan is ~70% writing code. Countermeasure: shrink the task and get real Python on the page *before* any further tooling polish.
- **Mentor-side gap (2026-07-20):** the tasks were mis-pitched — beginner-Python explanation was skipped on the assumption that "senior developer" meant "senior in Python." Corrected in `CLAUDE.md` §1/§9 and by the Weeks 1–3 fundamentals phase. Watch for this recurring: if he goes quiet for days, suspect the task is above his current Python level, not that he lacks discipline.

## 🔓 Override-phrase / reveal log
_(every Rung-5 reveal logged honestly — §3; 2 overrides on one task ⇒ under-practicing signal)_
- _(none yet)_

## 🎤 Interview performance by topic
_(strong / passable / weak, with the specific gap — §6)_
- **Import resolution / venvs** — 2026-07-13 — *passable (leaning weak)*: had the isolation intuition but couldn't name the mechanism (`sys.path` search → `site-packages`; a venv swaps which `site-packages` is on the path). Re-ask. _(Scheduled re-ask: fundamentals Day 13.)_
- **`__name__` / `__main__` guard** — 2026-07-13 — *weak (no answer)*: brand-new idiom; gave model answer + Ruby `__FILE__ == $0` anchor. Re-ask in a later mock. _(Scheduled re-ask: fundamentals Day 1.)_
