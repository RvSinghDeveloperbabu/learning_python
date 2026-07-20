# Ravi's 14-Week Plan: Ruby on Rails → Python + LLM Eval Roles

> **This file is the single source of truth for the schedule.**
> If any other document in this repo implies different week numbers, **this file wins** and the other document is stale. Report it and it gets fixed.

**Goal:** learn Python properly from the ground up, then build a portfolio that proves you can do LLM-evaluation and function-calling work.

**Your budget:** 3–4 hours/day, **6 days a week** (see the honest schedule below — this matters).

**Target jobs:**
1. **LLM Trainer – Agent Function Call** (least Python needed — apply first)
2. **Senior Python Developer**
3. **LLM Evaluation & Repository Validation**

---

## How to use this file

- This is the **map**, not the daily detail. Tick a box `[x]` when a week is done.
- **Your daily lessons for Weeks 1–3 live in [`docs/07-python-fundamentals.md`](docs/07-python-fundamentals.md).** Start there.
- **Rule of thumb: ~30% reading, ~70% writing code.** You learn Python by writing Python.
- **You are senior at programming and a beginner at Python. Both are true.** You already know loops, objects, testing, APIs, and N+1 tuning. What you do not yet know is Python's syntax and its ecosystem. Weeks 1–3 fix exactly that — and nothing else. Do not skip them, and do not feel bad about them.
- Every phase ends with something on your GitHub. By Week 14 your repo tells the story for you.
- **Your unfair advantage:** you already built an MCP server + OAuth + function-calling system. Most applicants never have. Lead with that everywhere.

---

## The 14-week map

| Week | What you learn | Where you build | What you finish with |
|---|---|---|---|
| **0** | Setup ✅ **done** | — | working Python env |
| **1** | Running Python, values, control flow, lists, dicts | `fundamentals/` | contact book v1 |
| **2** | Functions, **classes/OOP**, **errors**, files | `fundamentals/` | it saves and reloads |
| **3** | Modules, JSON, logging, **pytest**, tooling | `fundamentals/` | **first Python repo on GitHub** |
| **4–5** | Comprehensions, generators, type hints, stdlib | `foundations/` + `contracts/` | `evalctl` — a typed CLI |
| **6** | **Flask** — your first web framework | `flask-app/` | ingestion + webhook service |
| **7–8** | Django + DRF | `django-app/` | the platform system of record |
| **9** | FastAPI + Pydantic, async | `fastapi-app/` | async LLM gateway, Dockerized |
| **10** | SWE-bench, Docker, reading real repos | — | written spec + 2 OSS PRs |
| **11–12** | Function calling, the agent loop | `llm/agent-cli/` | a CLI agent with real tools |
| **13–14** | **FLAGSHIP** — repo → Docker → patch → tests | `llm/eval-harness/` | SWE-bench in miniature |
| *alongside 13–14* | Resume, applications, interview practice | — | applied to all 3 tracks |

---

## Week 0 — Setup ✅ DONE

- [x] Python 3.12+ working — you have 3.13.14
- [x] `uv` installed and proven (you saw package isolation with your own eyes)
- [x] VS Code + Python + Pylance working

---

## Weeks 1–3 — Python fundamentals (start here)

**This is the phase that was missing.** Three weeks, 18 days, building **one program** — a contact book — from a single print statement into a tested, typed, packaged command-line tool.

- [ ] **Week 1** — running Python, numbers and strings, `if`/`for`/`while`, lists, dicts and sets
- [ ] **Week 2** — functions, **classes and objects**, **exceptions and error handling**, reading and writing files
- [ ] **Week 3** — modules and entry points, JSON + dataclasses, logging, **pytest**, then the tooling gate

**Important:** you do **not** touch `mypy --strict`, comprehensions, generators, or decorators in these three weeks. Tooling comes on **Day 18**, after you have written sixteen working programs — not before.

📖 **Daily steps:** [`docs/07-python-fundamentals.md`](docs/07-python-fundamentals.md)
**Deliverable:** your first Python repo on GitHub — tested, type-checked, and pushed.

---

## Weeks 4–5 — `evalctl` (your first real tool)

Now that basics are automatic, you learn the Python that makes code *idiomatic*.

- [ ] Comprehensions and generator expressions; generators (`yield`) for streaming big files
- [ ] Type hints and `mypy --strict`; `Protocol` for duck-typed seams
- [ ] Stdlib tour: `collections`, `itertools`, `pathlib`, `dataclasses`, `json`
- [ ] Context managers and decorators you write yourself
- [ ] Publish the shared `contracts/` JSON schemas (test-case / run / result, versioned)

**Deliverable:** `evalctl` — a typed CLI that validates eval logs, computes pass rate and latency percentiles, and streams huge files without loading them into memory. → GitHub

---

## Week 6 — Flask (your first web framework)

Flask is small and explicit — you assemble the pieces yourself, so you actually see how a web app works. **Flask ≈ Sinatra**, not Rails.

- [ ] App factory + blueprints; SQLAlchemy + migrations
- [ ] Verify webhook signatures (HMAC over the raw bytes) + API keys
- [ ] Idempotency keys — the same request twice must not double-write
- [ ] Background work via a durable outbox table; a small query API

**Deliverable:** an eval-results ingestion service → GitHub

---

## Weeks 7–8 — Django + DRF (your Rails analog)

Django is the closest thing to Rails: models, migrations, a free admin panel.

- [ ] Domain model: orgs, users/roles, projects, eval suites, test cases, runs, results
- [ ] Migrations; the Django admin configured for real ops use
- [ ] DRF: viewsets, serializers, pagination, filtering, permissions
- [ ] **ORM depth: create an N+1, prove it with query counts, then fix it** with `select_related`/`prefetch_related`
- [ ] Multi-tenant isolation — a test proving Org A cannot read Org B's data

**Deliverable:** the platform system of record → GitHub
**Lead with the N+1 story in interviews.** It maps straight onto your Rails experience.

---

## Week 9 — FastAPI + Pydantic

- [ ] Pydantic v2 models, validators, settings from environment variables
- [ ] Async done correctly: bounded concurrency, never blocking the event loop
- [ ] Dependency injection; streaming; retries, timeouts, circuit breaking
- [ ] Async SQLAlchemy; Dockerized; automatic OpenAPI docs

**Deliverable:** a Dockerized async LLM gateway → GitHub
**Learn Pydantic well** — it is everywhere in LLM and eval work.

---

## Week 10 — SWE-bench, Docker, and real repositories

This is the week that turns "Python developer" into "LLM-eval Python developer."

- [ ] Study **SWE-bench**: how tasks are built from real GitHub issues and graded by *running the repo's own test suite*
- [ ] Write, in your own words, a one-page spec of how a patch gets graded (FAIL_TO_PASS / PASS_TO_PASS)
- [ ] Clone a real open-source Python library, Dockerize it, get its test suite green
- [ ] Trace one closed issue → the PR that fixed it → the test that proves it
- [ ] Open **2 small OSS pull requests**

**Deliverable:** written SWE-bench spec + 2 PRs

---

## Weeks 11–12 — `llm/agent-cli` (your differentiator)

You already built this in Ruby with MCP. Now do it in Python.

- [ ] Tool schemas (JSON) and the full tool-use loop: request → execute → feed the result back → loop
- [ ] Agent loop as architecture: a tool registry, dispatch, stop conditions, a hard step cap
- [ ] Two providers behind one interface (Anthropic + OpenAI)
- [ ] 2–3 real tools (read a file, search code, run tests) with guardrails and timeouts
- [ ] A structured trace of every decision, with secrets redacted

**Deliverable:** a command-line function-calling agent → GitHub

---

## Weeks 13–14 — `llm/eval-harness` (FLAGSHIP)

The centerpiece. This is the job, literally.

- [ ] Task spec format: repo, base commit, patch, test command
- [ ] Docker sandbox: check out → apply patch → run tests in isolation, with timeouts and resource limits
- [ ] Parse results into a clear verdict: **resolved / unresolved / error** — and never confuse "tests failed" with "the harness failed"
- [ ] A `report.json` conforming to `contracts/`, plus captured logs
- [ ] A small dataset of real repos so anyone can reproduce your results
- [ ] An excellent README

**Deliverable:** the flagship eval-harness repo → GitHub

### Alongside Weeks 13–14 (non-code — I can help write these)

- [ ] Update your resume: lead with **MCP / function-calling / OAuth**, then the agent, then the harness
- [ ] Apply to all three tracks
- [ ] Practice explaining your reasoning **out loud in English** — that is roughly half the grade in these interviews

---

## The honest schedule (read this before you trust the map)

Adding up the day estimates in [`docs/02-real-world-projects.md`](docs/02-real-world-projects.md), at **MVP only, with every optional extra dropped**:

| Phase | Days |
|---|---|
| Python fundamentals | 18 |
| `evalctl` + `contracts/` | 10 |
| Flask | 6 |
| Django | 12 |
| FastAPI | 9 |
| SWE-bench + Docker + OSS PRs | 8 |
| `agent-cli` | 10 |
| `eval-harness` | 13 |
| **Total** | **86** |

Fourteen weeks at **6 days/week = 84 days.**

**So: 14 weeks fits every project's MVP, with about two days of slack, and only if you work six days a week.** At five days a week this is a ~17-week plan. That is not a warning — it is arithmetic. Plan accordingly, and if you lose a week, use the cut lines below instead of quietly compressing the flagship.

### Cut lines, in the order you use them

1. FastAPI's OpenAI adapter — ship Anthropic + a fake adapter
2. `agent-cli`'s `apply_patch` tool
3. Flask's dashboard — ship API-only
4. Django admin polish
5. The second OSS library Dockerize pass
6. OSS PRs: 4 → 2
7. Eval-harness dataset: 3 tasks → 2
8. **Last resort:** Flask shrinks to a 3-day tour (routing, blueprints, one signed endpoint)

**Never cut:** Weeks 1–3 fundamentals · `evalctl` MVP · `agent-cli` MVP · `eval-harness` MVP.

**Week-8 checkpoint.** If you are more than 5 days behind the map, execute cut lines 1–4 *immediately*. Do not let the flagship absorb the slippage — it is the thing that gets you hired.

**One honest tension.** Flask is now the first web framework you learn, so it can no longer also be "the first thing to cut." If the schedule genuinely fails, the real choices are: Flask shrinks to 3 days, **or** Django loses a week. Pick deliberately; don't drift.

---

## Honest notes

- **One or two weeks on a framework makes you productive, not expert.** That is normal and it is enough to apply. Depth keeps building through the projects.
- **These are mostly contractor roles:** fixed hours/week, ~4-hour PST overlap, sometimes one-month contracts with extensions based on performance, no benefits. Great for breaking into AI-eval work — just go in knowing the shape of the deal.
- **Weeks 10–14 are what win the eval jobs.** The web frameworks make you a stronger general Python developer (and matter for the "Senior Python Developer" label), but the SWE-bench, agent, and harness work is the differentiator.
- **Tooling is not progress.** Config work feels productive because it resembles Rails work you already know. Writing unfamiliar Python is the actual job. If you notice yourself polishing configuration instead of writing code, that is the signal — go write the program.

---

## Start today

1. Open [`docs/07-python-fundamentals.md`](docs/07-python-fundamentals.md).
2. Create a `fundamentals/` folder and set it up yourself with `uv`.
3. Do **Day 1**. It is one small program, and it takes well under an hour.
4. Ask me when you want to write the LLM Trainer application — that one is not code, so I can write it with you.
