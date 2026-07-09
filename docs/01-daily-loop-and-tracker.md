# The Ravi Python + LLM Mentor System

Two deliverables below, both ready to paste into your repo:

- **(A)** `README_MENTOR.md` — how the whole system works and the exact phrases that trigger each behavior.
- **(B)** `PROGRESS.md` — the tracker Claude updates at the end of every session.

---

---

# (A) `README_MENTOR.md` — How to Use This Mentor System

## What this is

This repo is a **guided 8-week bootcamp** that turns a senior Rails developer into an interview-ready senior Python developer with an LLM-eval / function-calling specialty. Claude acts as a **mentor, not a code generator**. You write 100% of the Python; Claude explains, maps Ruby→Python, reviews your code, interviews you, and keeps score.

The system runs on a **daily loop**: you start a session, Claude assigns the day's task, you build it, Claude reviews it, you get interviewed, and the tracker gets updated. Repeat for ~40 working days.

## The files

| File | What it is | Who edits it |
|---|---|---|
| `Ravi_Python_LLM_Learning_Plan.md` | The 8-week curriculum (the map). Rarely changes. | You (rarely) |
| `PROGRESS.md` | The tracker (the current state): weekly checkboxes, deliverables, dates, mistakes log, applications, interview weak-spots. | **Claude, end of each session** |
| `README_MENTOR.md` | This file — how the system works and the trigger phrases. | You (rarely) |
| `CLAUDE.md` *(recommended, optional)* | Persistent mentor rules so Claude behaves the same in every new chat window without re-briefing. See "Making it stick" below. | You (once) |

Everything else in the repo is **code you write** — the CLI tool, Django app, FastAPI service, CLI agent, and the flagship eval harness.

## The one rule that shapes everything: the CODE RULE (ABSOLUTE)

Claude will **never write Python for you** — not a solution, not scaffolding, not a fix-in-place, not even a one-line syntax demo. This is deliberate. You are already a strong programmer; the only way Python moves from "I can read it" to "I think in it" is by typing every line yourself.

What Claude **will** do:
- Explain concepts in plain English.
- Map Ruby idioms to Python idioms (describing Ruby, and Ruby code, is fine).
- Give you English pseudocode / numbered step lists.
- Link you to the official docs.
- **Review** Python you have already written and tell you what's wrong and why.

What Claude will **not** do: hand you Python. If you ask "just show me how to write it," the default answer is a hint, not code — unless you deliberately pull the escape hatch (below).

## How a typical day works (the daily loop)

1. **You open the repo and type `Start today`.**
   Claude reads `PROGRESS.md`, tells you exactly where you are (week, next task, next deliverable), and assigns **today's task** with **acceptance criteria** — what "done" looks like — but no code.
2. **You build it.** You type the Python yourself. When stuck, you ask for a `Hint` or a Ruby→Python explanation. Claude nudges; it does not solve.
3. **You get it reviewed.** Type `Review my code` (with the file path). Claude reads what you wrote and gives targeted feedback: correctness, idiom, type hints, tests — pointing at problems and directions, never rewriting the file for you.
4. **You get interviewed.** Type `Interview me` (or Claude does this automatically at wrap-up). 2–3 questions on today's topic. Conceptual questions get **model-answer talking points** after you attempt them; coding questions are stated as **problem + acceptance criteria only**.
5. **You wrap up.** Type `Wrap up`. Claude updates `PROGRESS.md`: checks off completed tasks, records the date, logs any recurring mistakes it noticed, updates your interview weak-spots, and confirms tomorrow's starting point.

A full session is roughly: 5 min orient → 2–3 hrs build → 20 min review → 15 min interview → tracker update.

## Trigger phrases (type these verbatim, or close to them)

Claude recognizes intent, so slight wording changes are fine. These are the canonical phrases.

### Session control
| Type this | What Claude does |
|---|---|
| `Start today` / `Start today's session` | Reads the tracker, states where you are, assigns today's task + acceptance criteria (no code). |
| `Where am I?` / `Status` | Summarizes current week, % through the plan, next deliverable, open blockers. |
| `Wrap up` / `I'm done for today` | Reviews the day, updates `PROGRESS.md`, logs mistakes, ends with 2–3 interview questions. |
| `Skip this` / `Defer to later` | Marks a task deferred in the tracker with a reason; keeps you moving. |

### Learning help (still zero code)
| Type this | What Claude does |
|---|---|
| `Hint` / `Nudge me` | One escalating hint. Ask again for `Hint 2`, `Hint 3` — each reveals more, still no Python. |
| `Explain X the Ruby way` | Ruby→Python analogy in plain English (e.g. "blocks vs. `with`", "Hash vs. dict"). |
| `Am I on the right track?` | Conceptual sanity check on your approach before you sink hours in. |
| `Unblock me` | Diagnostic questions to find where your mental model is off. |

### Code review
| Type this | What Claude does |
|---|---|
| `Review my code <path>` | Reviews what you wrote: correctness, idiom, type hints, tests. Flags issues + explains why; never edits the file. |
| `Is this idiomatic?` | Focused Ruby-ism → Python-ism style pass (are you writing Python, or Ruby in Python syntax?). |
| `Review my tests` | Checks pytest structure: fixtures, parametrize, coverage of edge cases. |

### Interview practice
| Type this | What Claude does |
|---|---|
| `Interview me` | 2–3 mixed questions on the current topic. Conceptual → talking points after you try; coding → problem + acceptance criteria only. |
| `Grill me on X` | Targeted question set on one topic (e.g. `Grill me on Pydantic`, `Grill me on select_related`). |
| `Mock interview` | A longer simulated senior-Python screen (~20–30 min): a mix of concept + a design/coding prompt, then a **scorecard** with strengths, gaps, and what to drill. |
| `Explain-back check` | Claude asks you to teach a concept back to it, then grades your explanation (interviews are half about explaining clearly). |

### The override / "show me" escape hatch
| Type this | What Claude does |
|---|---|
| `Override: show me` / `Show me the answer` | Deliberately suspends the no-code rule **for one specific thing**. Claude first warns you and gives one last hint. If you confirm, it shows a **minimal reference** — the smallest snippet that unblocks you — then **requires you to re-type it in your own file and explain it back**, and **logs the override** in the tracker so you can see how often you reach for it. |

Use the override rarely and on purpose. It exists so you're never truly stuck for hours — but every use is a signal of a gap, and the tracker keeps count. If overrides cluster on one topic, that's your next drill.

### Tracking
| Type this | What Claude does |
|---|---|
| `Log a mistake: <description>` | Adds a row to the Recurring Mistakes log with the Ruby-ism behind it and the rule to remember. |
| `Update the tracker` | Syncs `PROGRESS.md` on demand (Claude also does this automatically at `Wrap up`). |
| `Log application: <role/company/date>` | Records a job application in the Applications log. |
| `Review my mistakes` | Reads back your recurring-mistakes log and turns the top offenders into today's warm-up drill. |

## How progress is tracked

`PROGRESS.md` is the single source of truth. At every `Wrap up` (and any time you type `Update the tracker`), Claude will:

1. **Check off** the granular tasks you completed and stamp the **date done**.
2. **Set status** on in-flight tasks (`TODO` / `WIP` / `DONE` / `BLOCKED` / `SKIP`).
3. **Paste the GitHub link** into the deliverable row when a week's deliverable ships.
4. **Append to the Recurring Mistakes log** any pattern it saw in your code (especially Ruby-isms leaking into Python).
5. **Update Interview Weak Spots** based on how you did in the day's questions.
6. **Log applications and overrides.**

You should be able to open `PROGRESS.md` cold on any morning and know exactly what to do next — that's what `Start today` reads.

## Weekly rhythm and deliverables

Each week ends in **one GitHub deliverable**. The tracker's per-week table shows the granular steps; the Deliverables Summary shows the shippable artifacts. Cadence:

- **Week 0:** working env (Python 3.12+, uv, VS Code + Pylance) **+ your first job application submitted.**
- **Weeks 1–2:** Python-CLI file/JSON processor, type-hinted, passing pytest suite.
- **Week 3:** Django + DRF app (2–3 models + REST API).
- **Week 4:** Dockerized FastAPI + Pydantic service.
- **Weeks 5–6:** CLI agent using function calling with 2–3 tools.
- **Weeks 7–8:** flagship mini eval-harness (SWE-bench in miniature) + updated resume + applications to all 3 tracks.

Honest expectation setting is baked into the plan: one week each on Django/FastAPI makes you productive, not expert. For your target eval roles, **Weeks 5–6 matter most** — running and testing *other people's* code, not building web apps.

## Making it stick across chat windows (recommended)

Because each new chat starts fresh, drop a short `CLAUDE.md` in the repo root that tells Claude, every time: the no-code rule is absolute, the escape hatch is `Override: show me`, treat Ravi as a senior dev (skip beginner pedagogy), run the daily loop, and keep `PROGRESS.md` current. Then any window you open behaves like the same mentor. (Ask Claude to help you draft `CLAUDE.md` in English — you'll still write any code yourself, but this file is config, not Python.)

## Getting the most out of it

- **Type everything.** The rule isn't a gimmick — muscle memory is the whole point.
- **Attempt before hint.** Struggle for 10–15 min before `Hint`. The stuck moment is where learning happens.
- **Answer interview questions out loud / in writing before reading the talking points.** Half your target interviews grade how clearly you *explain*.
- **Let the mistakes log drive review days.** Your recurring Ruby-isms are your personalized syllabus.
- **Ship the deliverable even if imperfect.** A B-grade repo on GitHub beats an A-grade one still on your laptop.

---

---

# (B) `PROGRESS.md` — Progress Tracker Template

Copy everything below into `PROGRESS.md`. Claude keeps it updated.

---

```markdown
# Ravi — Python + LLM-Eval Progress Tracker

Last updated: ____-__-__  ·  Updated by: Claude at session wrap-up

## Snapshot
- **Start date:** ____-__-__
- **Current week:** Week __
- **Today's focus:** ______________________________
- **Next deliverable due:** ______________________________
- **Sessions completed:** __  ·  **Current streak (days):** __
- **Override ("show me") count:** __   ← keep this low; clusters = your next drill

## Status legend
`TODO` not started · `WIP` in progress · `DONE` complete · `BLOCKED` stuck (see notes) · `SKIP` deferred (see notes)
Checkbox: `[ ]` open · `[x]` complete

---

## Week 0 — Setup + First Application (2–3 days)
Deliverable: working env + 1 job application submitted.

| ✓ | Task | Status | Deliverable / Proof (URL or note) | Date Done |
|---|---|---|---|---|
| [ ] | Confirm Python 3.12+ available (3.14 installed — use it; 3.11 is too old) | TODO | | |
| [ ] | Install `uv` | TODO | | |
| [ ] | Set up VS Code + Pylance | TODO | | |
| [ ] | Hello-world script runs | TODO | | |
| [ ] | Create a venv (via uv) | TODO | | |
| [ ] | Install a package into the venv | TODO | | |
| [ ] | **Apply to LLM Trainer role (application #1)** | TODO | | |

---

## Weeks 1–2 — Python for Someone Who Already Programs
Deliverable: Python CLI tool (file/JSON processor) with type hints + passing pytest suite on GitHub.
Goal: **think in Python, don't translate.**

| ✓ | Task | Status | Deliverable / Proof | Date Done |
|---|---|---|---|---|
| [ ] | Ruby→Python syntax diffs: indentation, `None`/`True`/`False`, f-strings, no `end` | TODO | | |
| [ ] | Data structures: list / dict / set / tuple (when to use which) | TODO | | |
| [ ] | Comprehensions: list, dict, set | TODO | | |
| [ ] | Type hints: `list[int]`, `dict[str, X]`, `Optional`, `\|` unions | TODO | | |
| [ ] | Install + run `mypy` clean on your code | TODO | | |
| [ ] | Stdlib tour: `collections`, `itertools` | TODO | | |
| [ ] | Stdlib tour: `pathlib`, `datetime`, `json` | TODO | | |
| [ ] | `dataclasses` | TODO | | |
| [ ] | Context managers (`with`) — vs. Ruby blocks/ensure | TODO | | |
| [ ] | Decorators | TODO | | |
| [ ] | Generators (`yield`) | TODO | | |
| [ ] | pytest: assertions (RSpec-style), fixtures, parametrize | TODO | | |
| [ ] | Drill: rewrite Ruby script #1 in idiomatic Python | TODO | | |
| [ ] | Drill: rewrite Ruby script #2 in idiomatic Python | TODO | | |
| [ ] | **Deliverable: CLI file/JSON processor + type hints + passing pytest, pushed to GitHub** | TODO | repo: | |

---

## Week 3 — Django (the Rails analog)
Deliverable: Django + DRF app, 2–3 models + REST API on GitHub.

| ✓ | Task | Status | Deliverable / Proof | Date Done |
|---|---|---|---|---|
| [ ] | Official polls tutorial parts 1–4 (typed, not copied) | TODO | | |
| [ ] | Official polls tutorial parts 5–7 | TODO | | |
| [ ] | Map Models = ActiveRecord; views/templates; `manage.py migrate` = `rails db:migrate`; free admin | TODO | | |
| [ ] | ORM: querysets, relationships, migrations | TODO | | |
| [ ] | `select_related` / `prefetch_related` (the N+1 fix) | TODO | | |
| [ ] | DRF: serializers, viewsets, JSON API | TODO | | |
| [ ] | Settings / apps / project structure | TODO | | |
| [ ] | **Deliverable: Django + DRF app (2–3 models + REST API), pushed to GitHub** | TODO | repo: | |

---

## Week 4 — FastAPI + Pydantic
Deliverable: Dockerized FastAPI service w/ Pydantic models + endpoints on GitHub.
Note: **learn Pydantic well — it's everywhere in LLM/eval work.**

| ✓ | Task | Status | Deliverable / Proof | Date Done |
|---|---|---|---|---|
| [ ] | FastAPI tutorial top-to-bottom | TODO | | |
| [ ] | Pydantic validation + schemas (deep) | TODO | | |
| [ ] | Path + query params, request bodies | TODO | | |
| [ ] | Dependency injection | TODO | | |
| [ ] | Response models | TODO | | |
| [ ] | `async` / `await` | TODO | | |
| [ ] | SQLAlchemy basics | TODO | | |
| [ ] | Auto OpenAPI / Swagger docs | TODO | | |
| [ ] | Dockerize the service | TODO | | |
| [ ] | **Deliverable: Dockerized FastAPI + Pydantic service, pushed to GitHub** | TODO | repo: | |

---

## Weeks 5–6 — LLM + Evaluation Layer  ← MOST IMPORTANT FOR TARGET ROLES
Deliverable: CLI agent (Python) using function calling with 2–3 tools on GitHub.

| ✓ | Task | Status | Deliverable / Proof | Date Done |
|---|---|---|---|---|
| [ ] | Call the Anthropic API from Python | TODO | | |
| [ ] | Call the OpenAI API from Python | TODO | | |
| [ ] | Function calling end-to-end: define tools via JSON schema → model requests call → execute → feed result back → loop | TODO | | |
| [ ] | The agent loop: decision → execution → observation → next | TODO | | |
| [ ] | Study SWE-bench: tasks from real GitHub issues, verified by the repo's test suite | TODO | | |
| [ ] | OSS lib #1: clone → Dockerize → get test suite running locally | TODO | repo: | |
| [ ] | OSS lib #1: pick a closed issue + its fix PR → understand how tests verified it | TODO | | |
| [ ] | OSS lib #2: clone → Dockerize → run tests → trace a fixed issue | TODO | repo: | |
| [ ] | OSS lib #3 (optional): clone → Dockerize → run tests → trace a fixed issue | TODO | repo: | |
| [ ] | Skill: read an unfamiliar codebase fast | TODO | | |
| [ ] | **Deliverable: CLI agent w/ function calling + 2–3 tools, pushed to GitHub** | TODO | repo: | |

---

## Weeks 7–8 — Flagship Portfolio + Apply
Deliverable: flagship eval-harness repo + updated resume + applications to all 3 tracks.

| ✓ | Task | Status | Deliverable / Proof | Date Done |
|---|---|---|---|---|
| [ ] | Flagship: takes an OSS repo → spins it up in Docker | TODO | repo: | |
| [ ] | Flagship: applies a candidate code patch | TODO | | |
| [ ] | Flagship: runs the test suite | TODO | | |
| [ ] | Flagship: reports pass/fail with logs (SWE-bench in miniature) | TODO | | |
| [ ] | Small OSS PR #1 | TODO | PR: | |
| [ ] | Small OSS PR #2 | TODO | PR: | |
| [ ] | Small OSS PR #3 (optional) | TODO | PR: | |
| [ ] | Small OSS PR #4 (optional) | TODO | PR: | |
| [ ] | Update resume: Python + LLM-eval section, **leading with MCP / function-calling / OAuth** | TODO | | |
| [ ] | Apply — Track 1: LLM Trainer (Agent Function call) | TODO | | |
| [ ] | Apply — Track 2: Senior Python Developer | TODO | | |
| [ ] | Apply — Track 3: LLM Evaluation & Repository Validation | TODO | | |
| [ ] | Prep AI video interview | TODO | | |
| [ ] | Prep coding/analysis screen — practice explaining reasoning in clear English (half the grade) | TODO | | |

---

## Deliverables Summary (the shippable artifacts)

| Week | Deliverable | Status | GitHub URL | Shipped Date |
|---|---|---|---|---|
| 0 | Working env + application #1 | TODO | | |
| 1–2 | Python CLI (file/JSON) + type hints + pytest | TODO | | |
| 3 | Django + DRF app (2–3 models + REST API) | TODO | | |
| 4 | Dockerized FastAPI + Pydantic service | TODO | | |
| 5–6 | CLI agent w/ function calling (2–3 tools) | TODO | | |
| 7–8 | Flagship mini eval-harness | TODO | | |
| 7–8 | Updated resume (Python + LLM-eval) | TODO | | |

---

## Recurring Mistakes / Notes Log  (Claude appends every session)

The point of this log: your Ruby instincts leaking into Python. Recurring rows become warm-up drills (`Review my mistakes`).

| Date | Mistake / Pattern | Ruby-ism behind it | Rule to remember | Status |
|---|---|---|---|---|
| _e.g. 2026-07-09_ | _Used a `for` loop where a comprehension was clearer_ | _Rails `.each` reflex_ | _Reach for list/dict comprehensions first_ | recurring |
| | | | | |
| | | | | |

Status: `recurring` (still happening) · `resolved` (not seen in 3+ sessions)

---

## Interview Weak Spots  (Claude maintains — drives `Grill me on X`)

| Topic | Confidence (1–5) | Last tested | Notes / what to drill |
|---|---|---|---|
| Type hints & mypy | | | |
| Comprehensions & generators | | | |
| Context managers / decorators | | | |
| pytest (fixtures, parametrize) | | | |
| Django ORM & N+1 (select/prefetch) | | | |
| Pydantic validation | | | |
| async / await | | | |
| Function calling / agent loop | | | |
| Reading & testing unfamiliar repos | | | |
| Explaining reasoning clearly (verbal) | | | |

---

## Applications Log

| Date | Role / Track | Company | Channel | Status | Notes |
|---|---|---|---|---|---|
| | LLM Trainer (Track 1) | | | applied | Week 0 first application |
| | | | | | |

Status values: `applied` · `screen` · `interview` · `offer` · `rejected` · `ghosted`

---

## Override Log ("show me" escape hatch uses)

| Date | Topic | What was shown | Why stuck | Re-typed & explained back? |
|---|---|---|---|---|
| | | | | |

Clusters here = your next scheduled drill. Fewer over time = you're internalizing Python.
```

---

Both documents are self-contained and ready to paste. `README_MENTOR.md` governs behavior; `PROGRESS.md` is the living state Claude updates at every `Wrap up`. If you want, the next step is drafting the optional `CLAUDE.md` (English config, no Python) so every fresh chat window enforces the no-code rule and the daily loop automatically.
