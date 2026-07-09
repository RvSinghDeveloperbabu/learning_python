# Ravi's 8-Week Plan: Ruby on Rails → Python + LLM Eval Roles

**Goal:** Get fluent enough in Python to work in it daily, learn Django + FastAPI, and build 1–2 portfolio pieces that prove you can do the LLM-evaluation / function-calling work these jobs ask for.

**Your budget:** 3–4 hours/day.

**Target jobs:**
1. LLM Trainer – Agent Function call (least Python needed — apply first)
2. Senior Python Developer
3. LLM Evaluation & Repository Validation

---

## How to use this file

- Tick a box `[x]` when done. Move at your own pace — if a week takes 9 days, that's fine.
- **Rule of thumb: ~30% reading/watching, ~70% writing code.** You already know how to program. You learn Python by writing Python, not by watching tutorials. Don't waste your hours on beginner courses.
- Every week has a small **deliverable** that goes on your GitHub. By week 8 your GitHub tells the story for you.
- Your unfair advantage: you already built an MCP server + OAuth + function-calling system. Most applicants never have. Lead with that everywhere.

---

## Week 0 — Setup + apply now (2–3 days)

Don't wait for the whole plan to finish before acting.

- [ ] Install Python 3.12+ and set up `uv` for environments/packages (fast, modern default). Resource: Astral `uv` docs.
- [ ] Pick your editor (VS Code is the safe choice) and get Python + Pylance extensions working.
- [ ] Run "hello world", create a venv with `uv`, install a package, run a script. Prove the toolchain works.
- [ ] **Apply to the "LLM Trainer – Agent Function call" role today.** It rewards what you already have (function-calling knowledge + clear English). Going through their process teaches you what "good tool-use data" looks like, which helps everything else.

**Deliverable:** A working Python environment + one job application submitted.

---

## Weeks 1–2 — Python for someone who already programs

Skip beginner material. Map Ruby → Python directly. The ideas transfer; you're learning syntax and idioms.

- [ ] Core syntax differences from Ruby: indentation blocks, `None`/`True`/`False`, f-strings, no `end`.
- [ ] Data structures: `list`, `dict`, `set`, `tuple` — and comprehensions (`[x for x in ...]`).
- [ ] **Type hints** + `mypy`. Python's typing culture is stronger than Ruby's, and these jobs care. Learn `list[int]`, `dict[str, X]`, `Optional`, `|` unions.
- [ ] Standard library tour: `collections`, `itertools`, `pathlib`, `dataclasses`, `datetime`, `json`.
- [ ] Context managers (`with`), decorators, generators (`yield`).
- [ ] **`pytest`** — this will feel like RSpec's cousin. Learn fixtures, parametrize, assertions.
- [ ] Drill: take 2 small Ruby scripts you've written and rewrite them in idiomatic Python.

**Resources:** official Python tutorial (docs.python.org), Real Python articles, pytest docs.

**Deliverable:** A small Python CLI tool (e.g. a file/JSON processor) with type hints and a passing pytest suite. Push to GitHub.

**Goal by end of week 2:** you *think* in Python, not translate from Ruby.

---

## Week 3 — Django (your Rails analog)

Django is the closest thing to Rails: MVC, ORM, migrations, built-in admin. You'll move fast here.

- [ ] Official Django tutorial ("Writing your first Django app" — the polls app). Do it by typing, not copying.
- [ ] Map the concepts: Models = ActiveRecord, Views/Templates = controllers/views, `manage.py migrate` = `rails db:migrate`, the Django admin = a free scaffolded admin panel.
- [ ] Django ORM: querysets, relationships, migrations, `select_related`/`prefetch_related` (your N+1 fix, Django-style).
- [ ] **Django REST Framework (DRF)** — serializers, viewsets, building a JSON API. This is how Django does what your Grape APIs do.
- [ ] Django settings, apps structure, and how a real project is organized.

**Resources:** official Django tutorial, DRF docs, "Django for APIs" (William Vincent) if you want a book.

**Deliverable:** A small Django + DRF app with 2–3 models and a REST API (e.g. a task/notes API). Push to GitHub.

---

## Week 4 — FastAPI + Pydantic

FastAPI is the lightweight, async, type-driven framework that most LLM tooling is built on. It'll feel like Grape but with strong typing baked in.

- [ ] FastAPI official tutorial (it's excellent — go top to bottom).
- [ ] **Pydantic** — data validation and schemas. Learn this *well*; it's everywhere in LLM/eval work (request/response models, tool schemas, config).
- [ ] Path/query params, request bodies, dependency injection, response models.
- [ ] `async`/`await` in FastAPI — a lot of LLM work is async, so get comfortable.
- [ ] **SQLAlchemy** basics (the standalone ORM FastAPI usually pairs with) — enough to connect a DB.
- [ ] Auto-generated OpenAPI/Swagger docs (you did Swagger in Rails — same idea, free here).

**Resources:** FastAPI docs (fastapi.tiangolo.com), Pydantic docs, SQLAlchemy docs.

**Deliverable:** A FastAPI service with Pydantic models and a couple of endpoints, Dockerized. Push to GitHub.

---

## Weeks 5–6 — The LLM + evaluation layer

This is what turns "Python developer" into "LLM-eval Python developer." You already know these concepts from MCP — now do them in Python.

- [ ] Call the Anthropic API and OpenAI API from Python (SDKs). Simple chat completion first.
- [ ] **Function calling / tool use, end to end** in Python: define tools (JSON schema), let the model request a call, execute it, feed the result back, loop. Read Anthropic's tool-use docs + the Prompt Engineering Guide's function-calling page.
- [ ] Understand the **agent loop**: tool decision → execution → observation → next step. Build a tiny agent that uses 2–3 real tools.
- [ ] **Study SWE-bench** (swebench.com / the SWE-bench GitHub repo). Read how tasks are built from real GitHub issues and *verified by running the repo's test suite*. The repo-validation job is literally this.
- [ ] Hands-on drill — do this for 2–3 trending Python open-source libraries:
  - [ ] Clone the repo.
  - [ ] **Dockerize it and get its test suite running locally.**
  - [ ] Pick a real closed issue, find the PR that fixed it, and understand the fix + how tests verified it.
- [ ] Learn to read unreadable codebases fast (this is a listed skill: "navigate complex real-world codebases").

**Resources:** Anthropic tool-use docs, OpenAI function-calling docs, promptingguide.ai (agents/function-calling), SWE-bench GitHub + paper.

**Deliverable:** A working command-line agent (Python) that uses function calling with 2–3 tools. Push to GitHub.

---

## Weeks 7–8 — Flagship portfolio project + apply

Build ONE project that signals all three roles at once, then apply everywhere.

- [ ] **Mini eval harness** — a Python tool that:
  - [ ] takes an open-source repo,
  - [ ] spins it up in Docker,
  - [ ] applies a candidate code patch,
  - [ ] runs the test suite,
  - [ ] reports pass/fail with logs.
  This is SWE-bench in miniature — the exact motion these teams do daily. Make it clean, with a good README.
- [ ] Make 2–4 small PRs to Python open-source projects (docs fixes, small bugs count). "History of contributing to open-source" is a listed bonus, and you already have the habit — just in Python now.
- [ ] Update your resume: add a **Python + LLM-eval** section and re-lead with your MCP / function-calling / OAuth work. That's your headline, not a footnote.
- [ ] Apply to all three tracks (you already did the Trainer role in Week 0 — now the Python Developer + Repo Validation roles).
- [ ] Prep for their process: some use an AI video interview + a coding/analysis screen. Practice explaining your reasoning clearly in English — that's half of what they grade.

**Deliverable:** Flagship eval-harness repo + updated resume + applications submitted.

---

## Honest notes

- **Django/FastAPI depth:** one week each gets you productive, not expert. Depth keeps building through your projects. That's normal and enough to apply.
- **These are mostly contractor roles:** fixed hours/week (often 20/30/40), 4-hr PST overlap, sometimes ~1-month contracts with extensions based on performance, no benefits. Great for breaking into AI-eval work and putting it on your resume — just go in knowing the shape of the deal.
- **Don't over-study frameworks for the eval roles specifically.** The repo-validation job is about running and testing *other people's* code, not building web apps. Django/FastAPI make you a stronger general Python dev (and matter for the "Senior Python Developer" label), but Weeks 5–6 are the ones that win the eval jobs.

---

## Start today

1. Install Python + `uv`, confirm your toolchain.
2. Apply to the LLM Trainer – Agent Function call role.
3. Begin the Ruby → Python mapping (Weeks 1–2).
