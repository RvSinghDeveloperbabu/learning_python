# Ravi's Python + LLM-Eval Learning Workspace

A mentored, project-driven path from **senior Ruby on Rails developer → senior Python developer + LLM-evaluation engineer.**

The rule that makes this work: **the mentor (Claude) never writes my code.** It explains, analogizes to Ruby, links docs, asks questions, and reviews what *I* write — but I type every line myself. That constraint is the whole point; typing it is where the learning happens.

**Where I actually am:** senior at *programming*, beginner at *Python*. Both are true. The plan starts with three weeks of genuine Python fundamentals for exactly that reason.

---

## How this workspace is organized

```text
python_learning/
├── CLAUDE.md                 ← the mentor contract (governs every session; read it once)
├── README.md                 ← you are here
├── PROGRESS.md               ← my live tracker; the mentor reads it to start and updates it to end each session
├── Ravi_Python_LLM_Learning_Plan.md   ← the 14-week map · SINGLE SOURCE OF TRUTH for the schedule
│
├── docs/
│   ├── 01-daily-loop-and-tracker.md         ← how a session + the mentor works (read first)
│   ├── 07-python-fundamentals.md            ← ⭐ Weeks 1–3, day by day. START HERE.
│   ├── 04-curriculum-core-python-and-web.md ← Weeks 4–9: evalctl, Flask, Django, FastAPI
│   ├── 05-curriculum-llm-and-flagship.md    ← Weeks 10–14: SWE-bench, agent, eval-harness
│   ├── 02-real-world-projects.md            ← full specs for all six projects + day estimates
│   ├── 03-learning-resources.md             ← curated links (official docs first)
│   └── 06-curriculum-review-notes.md        ← reviewer notes / known gaps (reference)
│
├── interview-prep/
│   ├── senior-python-interview-bank.md   ← senior Q bank (concept talking-points + coding problems)
│   └── daily-session-questions.md        ← the questions asked at each session's end, with model answers
│
└── (project folders — I scaffold each one myself with `uv`, as the first milestone of each project)
    ├── fundamentals/    — one contact-book program, grown daily          (Weeks 1–3)
    ├── foundations/     — evalctl: a typed CLI over eval run logs        (Weeks 4–5)
    ├── flask-app/       — results-ingestion & webhook service            (Week 6)
    ├── django-app/      — the platform's system of record (Django + DRF) (Weeks 7–8)
    ├── fastapi-app/     — async LLM gateway / eval-runner                (Week 9)
    ├── llm/agent-cli/   — function-calling agent with real tools         (Weeks 11–12)
    ├── llm/eval-harness/— flagship: SWE-bench-in-miniature               (Weeks 13–14)
    └── contracts/       — shared versioned JSON schemas (built in foundations)
```

**Reading order is not the file numbering.** Read **01 → 07 → 04 → 02 → 05**. (`07` is Weeks 1–3 and comes before `04`; the numbers are historical, the order above is correct.)

Each project folder is its **own Python project** — its own `uv`-managed virtualenv, `pyproject.toml`, tests, and README. I create that scaffolding myself (it's part of the learning); the mentor describes what belongs there but does not write it. The parent `CLAUDE.md` is inherited automatically in every sub-folder, so the mentor contract applies everywhere below.

---

## The projects are one product, not six demos

Everything is a real component of an **LLM Evaluation & Agent Platform** — the same class of system the target employers build. Each project stands alone as a portfolio piece, but they share one domain and one versioned wire contract, so together they read as *one platform a company would actually run.*

| Folder | Real-world project | What it proves to an interviewer |
|---|---|---|
| `fundamentals/` | a contact book grown from a print statement into a tested, packaged CLI | I can actually write Python |
| `foundations/` | `evalctl` — typed CLI: validate & report on eval datasets/run logs | idiomatic typed Python, pytest, generators over large files |
| `flask-app/` | webhook + results-ingestion service (HMAC auth, idempotency, outbox) | micro-framework, security correctness, durable background work |
| `django-app/` | system of record — orgs/suites/runs/results, DRF API, admin, N+1-free ORM | senior Django + DRF depth |
| `fastapi-app/` | async eval-runner / LLM gateway (Pydantic v2, streaming, retries) | async correctness, typed APIs |
| `llm/agent-cli/` | function-calling agent with 2–3 real tools + full agent loop | the MCP/tool-use differentiator, in Python |
| `llm/eval-harness/` | **flagship** — repo → Docker → apply patch → run tests → pass/fail report | the eval / repo-validation job, literally |

Full specs (premise, MVP vs. stretch, architecture, milestones, acceptance criteria, testing, Docker) live in **[docs/02-real-world-projects.md](docs/02-real-world-projects.md)**.

> **Honest schedule:** this is a **14-week** plan at **6 days/week**. Adding up the per-project day estimates comes to ~86 days against 84 available — so it fits every project's **MVP only**, with every stretch item dropped and about two days of slack. At five days a week it's closer to 17 weeks. The plan file carries an ordered list of cut lines and a mid-point checkpoint so that, if I slip, the **flagship is never what gets compressed.**

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

## Getting started

Week 0 (toolchain setup) is **done**: Python 3.13, `uv` proven, VS Code + Pylance working.

**Next step: open [docs/07-python-fundamentals.md](docs/07-python-fundamentals.md) and do Day 1.**

1. Create a `fundamentals/` folder and set it up as a `uv` project yourself.
2. Do Day 1 — one small program, well under an hour.
3. Keep going. Days 1–18 build **one** program from a print statement into a tested, typed, packaged CLI.

One thing deliberately deferred: **no `mypy --strict`, comprehensions, generators, or decorators for the first three weeks.** Tooling arrives on Day 18, once sixteen working programs are already written. Config work feels productive because it resembles Rails work — but writing Python is the actual job.

The **LLM Trainer – Agent Function Call** application is still open. It's not code, so the mentor can draft it with me — just ask.

---

## The rhythm

**~30% reading, ~70% writing code.** Every phase ships a GitHub deliverable. By week 14 the repo tells the story: a coherent, senior-level LLM-eval platform, built line by line, in Python.
