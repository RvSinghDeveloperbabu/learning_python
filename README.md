# Ravi's Python + LLM-Eval Learning Workspace

A mentored, project-driven path from **senior Ruby on Rails developer → senior Python developer + LLM-evaluation engineer.**

The rule that makes this work: **the mentor (Claude) never writes my code.** It explains, analogizes to Ruby, links docs, asks questions, and reviews what *I* write — but I type every line myself. That constraint is the whole point; typing it is where the learning happens.

---

## How this workspace is organized

```text
python_learning/
├── CLAUDE.md                 ← the mentor contract (governs every session; read it once)
├── README.md                 ← you are here
├── PROGRESS.md               ← my live tracker; the mentor reads it to start and updates it to end each session
├── Ravi_Python_LLM_Learning_Plan.md   ← the original 8-week plan (kept for reference)
│
├── docs/   (numbered in reading order — read 01 → 06)
│   ├── 01-daily-loop-and-tracker.md      ← how a session + the mentor works (read first)
│   ├── 02-real-world-projects.md         ← what you'll build: full specs for all 6 projects + the honest schedule
│   ├── 03-learning-resources.md          ← curated, senior-appropriate links (official docs first)
│   ├── 04-curriculum-weeks-0-4.md        ← day-by-day: Python foundations, Django, FastAPI
│   ├── 05-curriculum-weeks-5-8.md        ← day-by-day: LLM APIs, tool-use, agent, eval harness
│   └── 06-curriculum-review-notes.md     ← reviewer notes / known gaps to watch (reference)
│
├── interview-prep/
│   └── senior-python-interview-bank.md ← senior Q bank (mixed: concept talking-points + coding problems)
│
└── (project folders — I scaffold each one myself with `uv`, as the first milestone of each project)
    ├── foundations/     — evalctl: a typed CLI over eval datasets/run logs      (Weeks 1–2)
    ├── flask-app/       — results-ingestion & webhook service                    (Week 3, swing item)
    ├── django-app/      — the platform's system of record (Django + DRF)         (Weeks 4–5)
    ├── fastapi-app/     — async LLM gateway / eval-runner                         (Week 6)
    ├── llm/agent-cli/   — function-calling agent with real tools                  (Weeks 7–8)
    ├── llm/eval-harness/— flagship: SWE-bench-in-miniature                        (Weeks 9–10)
    └── contracts/       — shared versioned JSON schemas (built in foundations)
```

Each project folder is its **own Python project** — its own `uv`-managed virtualenv, `pyproject.toml`, tests, and README. I create that scaffolding myself (it's part of the learning); the mentor describes what belongs there but does not write it. The parent `CLAUDE.md` is inherited automatically in every sub-folder, so the mentor contract applies everywhere below.

---

## The projects are one product, not six demos

Everything is a real component of an **LLM Evaluation & Agent Platform** — the same class of system the target employers build. Each project stands alone as a portfolio piece, but they share one domain and one versioned wire contract, so together they read as *one platform a company would actually run.*

| Folder | Real-world project | What it proves to an interviewer |
|---|---|---|
| `foundations/` | `evalctl` — typed CLI: validate & report on eval datasets/run logs | idiomatic typed Python, pytest, generators over large files |
| `flask-app/` | webhook + results-ingestion service (HMAC auth, idempotency, jobs) | micro-framework, auth, background work |
| `django-app/` | system of record — orgs/suites/runs/results, DRF API, admin, N+1-free ORM | senior Django + DRF depth |
| `fastapi-app/` | async eval-runner / LLM gateway (Pydantic v2, streaming, retries) | async correctness, typed APIs |
| `llm/agent-cli/` | function-calling agent with 2–3 real tools + full agent loop | the MCP/tool-use differentiator, in Python |
| `llm/eval-harness/` | **flagship** — repo → Docker → apply patch → run tests → pass/fail report | the eval / repo-validation job, literally |

Full specs (premise, MVP vs. stretch, architecture, milestones, acceptance criteria, testing, Docker) live in **[docs/02-real-world-projects.md](docs/02-real-world-projects.md)**.

> **Honest schedule:** this is really a **10-week** plan, not 8 — the original labels under-budgeted by ~40% and had no slot for Flask. Flask and the OpenAI adapter are pre-designated "cut if behind" swing items so the portfolio still lands if I overrun. See the schedule in the projects doc.

---

## How a session works (the daily loop)

The mentor runs this ritual every session (full detail in `CLAUDE.md` §5):

1. **Reads `PROGRESS.md`** to see where I am and what recurs.
2. **States today's task** with crisp, checkable acceptance criteria.
3. **I write the code.** It mentors via the hint ladder and answers concept questions in English.
4. **Reviews what I wrote** like a staff engineer on a PR — points to the line, names the problem and the principle, and makes *me* fix it.
5. **Ends with 2–3 senior interview questions** on what I touched.
6. **Updates `PROGRESS.md`** — status, what I shipped, interview performance, recurring gaps.

## Phrases I can type

| I type… | The mentor… |
|---|---|
| *(just start working / paste code)* | reviews it and guides via the hint ladder |
| `interview me` (optionally `interview me on decorators`) | runs a senior mock interview, mixed format, grades me |
| `review my code` | does a full staff-level review of what I wrote |
| **`OVERRIDE CODE RULE: show me and I'll explain it back`** | the *only* escape hatch — unlocks a few lines max, attempt-first, and I must explain each line back (see `CLAUDE.md` §3) |

The hint ladder (when I'm stuck) climbs one rung at a time: **nudge → name the concept → point to the exact doc → English pseudocode → (locked) reveal.** No amount of "just this once" or frustration unlocks the reveal — only the verbatim override phrase does, and even then it's capped and logged.

---

## Getting started (Week 0)

Week 0 is toolchain setup — and it's a *learning task*, so I do it myself; the mentor guides. In short:

1. Confirm Python 3.12+ (`python3 --version`).
2. Install **`uv`** (Astral) and learn the basics — see [docs/03-learning-resources.md](docs/03-learning-resources.md).
3. Get VS Code + the Python/Pylance extensions working.
4. Start **Weeks 1–2** in `foundations/`: `uv init` a new project there and begin `evalctl` per [docs/04-curriculum-weeks-0-4.md](docs/04-curriculum-weeks-0-4.md).
5. Apply to the **LLM Trainer – Agent Function Call** role now (per the original plan — don't wait).

To begin a mentored session, just open this folder and say what you want to work on, or ask the mentor to **"start today's session."**

---

## The rhythm

**~30% reading, ~70% writing code.** Every week ships a GitHub deliverable. By week 10 the repo tells the story: a coherent, senior-level LLM-eval platform, built line by line, in Python.
