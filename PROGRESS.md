# PROGRESS — Ravi's Python + LLM-Eval Journey

> **Mentor:** read this at the **start** of every session (CLAUDE.md §5.1) and update it at the **end** (§5.6, §10). This is the memory that makes the 10 weeks a coherent arc. Log honestly — including reveals and recurring gaps — even when unflattering.

**Status:** 🟡 Not started — Week 0 (setup)
**Started:** _(fill on day 1)_
**Current focus:** toolchain setup + `foundations/` kickoff
**Target:** 10 weeks · 3–4 hrs/day · ~30% reading / 70% writing

Legend: `[ ]` todo · `[~]` in progress · `[x]` done · `[-]` cut/skipped (swing item)

---

## Week 0 — Setup + apply now (2–3 days)
- [ ] Confirm Python 3.12+ working
- [ ] Install `uv`; create a throwaway venv, install a package, run a script (prove the toolchain)
- [ ] VS Code + Python + Pylance working
- [ ] **Apply to "LLM Trainer – Agent Function Call" role** (don't wait for the plan to finish)
- **Deliverable:** working env + one application submitted

## Weeks 1–2 — Python for programmers → `foundations/` (`evalctl`)
- [ ] Ruby→Python syntax & idioms; data structures + comprehensions
- [ ] Type hints + `mypy --strict`; stdlib tour (collections, itertools, pathlib, dataclasses, json)
- [ ] Context managers, decorators, generators (streaming large logs)
- [ ] `pytest` (fixtures, parametrize); rewrite 2 Ruby scripts idiomatically
- [ ] Publish the shared `contracts/` JSON schemas (test-case / run / result, versioned)
- **Deliverable:** `evalctl` CLI — type-hinted, `mypy` clean, passing pytest suite → GitHub

## Week 3 — `flask-app/` (ingestion & webhooks) · **SWING ITEM #1**
- [ ] Flask app-factory + blueprints; SQLAlchemy + Flask-Migrate
- [ ] HMAC signature verification over raw bytes + API keys + idempotency keys
- [ ] Background processing (queue or thread pool); query API + minimal dashboard
- **Deliverable:** Flask ingestion service → GitHub  · _(cut if behind → fold HMAC+idempotency into FastAPI stretch)_

## Weeks 4–5 — `django-app/` (platform system of record)
- [ ] Domain model: orgs, users/roles, projects, eval suites, test cases, provider configs, runs, results
- [ ] Migrations; Django admin configured for ops
- [ ] DRF: viewsets, serializers (nested), pagination, filtering, permissions, throttling
- [ ] ORM depth: create then FIX N+1 (`select_related`/`prefetch_related`), aggregations, transactions, custom managers
- [ ] Stretch: Celery task to trigger a run; API versioning
- **Deliverable:** Django + DRF platform core (2–3+ models, REST API, admin) → GitHub

## Week 6 — `fastapi-app/` (async LLM gateway / eval-runner)
- [ ] Pydantic v2 request/response models, validators, Settings
- [ ] Async correctness: httpx async, `asyncio.gather` with bounded concurrency, no event-loop blocking
- [ ] Dependency injection; streaming (SSE); retries/timeouts/circuit-breaking; rate limiting
- [ ] Async SQLAlchemy persistence; Dockerized; OpenAPI docs
- [ ] OpenAI adapter = **SWING ITEM #2** (MVP ships Anthropic + a fake adapter)
- **Deliverable:** Dockerized FastAPI gateway → GitHub

## Weeks 7–8 — `llm/agent-cli/` (function-calling agent)
- [ ] Tool schemas (JSON); the full tool-use loop (request → execute → feed back → loop)
- [ ] Agent loop: stop conditions, max steps; provider-agnostic (Anthropic + OpenAI)
- [ ] 2–3 real tools (read_file, search_code, run_tests/run_shell sandboxed); `apply_patch` = internal cut line
- [ ] Structured decision trace/logging; guardrails (input validation, timeouts, no destructive ops); secret redaction
- **Deliverable:** CLI function-calling agent → GitHub

## Weeks 9–10 — `llm/eval-harness/` (FLAGSHIP)
- [ ] Task spec format (repo, base commit, patch, test command)
- [ ] Docker sandbox: checkout → apply patch → run tests in isolation (timeouts + resource limits)
- [ ] Result parsing → pass/fail report (`report.json` conforming to `contracts/`) + captured logs/artifacts
- [ ] Small task dataset (a few real OSS Python repos); reproducibility; clean CLI
- [ ] Stretch: thin API + parallel runs
- **Deliverable:** flagship eval-harness repo w/ excellent README → GitHub

## Closeout (alongside weeks 9–10)
- [ ] 2–4 small PRs to Python OSS projects
- [ ] Resume: add Python + LLM-eval section; re-lead with MCP / function-calling / OAuth
- [ ] Apply to Senior Python Developer + LLM Evaluation / Repo-Validation roles
- [ ] Interview prep: practice explaining reasoning aloud (half the grade)

---

## 📓 Session log
_(newest first — the mentor appends one entry per session)_

| Date | Week/Day | Worked on | Shipped | Interview Qs (verdict) | Notes |
|---|---|---|---|---|---|
| — | 0 | _not started_ | — | — | tracker created |

## 🔁 Recurring gaps to watch
_(the mentor names patterns here and resurfaces them in reviews + interviews — §10)_
- _(none logged yet)_

## 🔓 Override-phrase / reveal log
_(every Rung-5 reveal logged honestly — §3; 2 overrides on one task ⇒ under-practicing signal)_
- _(none yet)_

## 🎤 Interview performance by topic
_(strong / passable / weak, with the specific gap — §6)_
- _(none yet)_
