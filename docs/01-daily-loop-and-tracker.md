# The Ravi Python + LLM Mentor System

How the mentoring system works, and the exact phrases that trigger each behavior.

> **Where things live:** week numbers come from [`../Ravi_Python_LLM_Learning_Plan.md`](../Ravi_Python_LLM_Learning_Plan.md) (the single source of truth for the schedule). Your live state lives in [`../PROGRESS.md`](../PROGRESS.md). Your daily lessons for Weeks 1–3 live in [`07-python-fundamentals.md`](07-python-fundamentals.md).

---

## What this is

This repo is a **guided 14-week programme** that turns a senior Rails developer into an interview-ready senior Python developer with an LLM-eval / function-calling specialty. Claude acts as a **mentor, not a code generator**. You write 100% of the Python; Claude explains, maps Ruby→Python, reviews your code, interviews you, and keeps score.

The system runs on a **daily loop**: you start a session, Claude assigns the day's task, you build it, Claude reviews it, you get interviewed, and the tracker gets updated. Repeat for ~84 working days (6 days/week × 14 weeks).

## The files

| File | What it is | Who edits it |
|---|---|---|
| `Ravi_Python_LLM_Learning_Plan.md` | The 14-week map. **Single source of truth for the schedule.** | You (rarely) |
| `docs/07-python-fundamentals.md` | Day-by-day beginner lessons for Weeks 1–3. **Start here.** | Nobody (reference) |
| `PROGRESS.md` | The tracker (current state): checkboxes, deliverables, dates, mistakes log, applications, interview weak-spots. | **Claude, end of each session** |
| `docs/01-daily-loop-and-tracker.md` | This file — how the system works and the trigger phrases. | You (rarely) |
| `CLAUDE.md` | Persistent mentor rules, inherited by every subfolder, so Claude behaves the same in every new chat window. | You (rarely) |

Everything else in the repo is **code you write** — the fundamentals package, the CLI tool, the Flask service, the Django app, the FastAPI service, the CLI agent, and the flagship eval harness.

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
| `OVERRIDE CODE RULE: show me and I'll explain it back` | Deliberately suspends the no-code rule **for one specific thing**. Claude first gives one last hint. If you confirm, it shows a **minimal reference** — the smallest snippet that unblocks you — then **requires you to re-type it in your own file and explain it back**, and **logs the override** in the tracker. |

Use the override rarely and on purpose. It exists so you're never truly stuck for hours — but every use is a signal of a gap, and the tracker keeps count. If overrides cluster on one topic, that's your next drill. The phrase must be typed verbatim; nothing else unlocks it (see `CLAUDE.md` §3).

### Tracking
| Type this | What Claude does |
|---|---|
| `Log a mistake: <description>` | Adds a row to the Recurring Mistakes log with the Ruby-ism behind it and the rule to remember. |
| `Update the tracker` | Syncs `PROGRESS.md` on demand (Claude also does this automatically at `Wrap up`). |
| `Log application: <role/company/date>` | Records a job application in the Applications log. |
| `Review my mistakes` | Reads back your recurring-mistakes log and turns the top offenders into today's warm-up drill. |

## How progress is tracked

`PROGRESS.md` is the single source of truth for **your current state** (the *schedule* lives in the plan file). At every `Wrap up` — and any time you type `Update the tracker` — Claude will:

1. **Check off** the granular tasks you completed and stamp the **date done**.
2. **Set status** on in-flight tasks using the tracker's legend: `[ ]` todo · `[~]` in progress · `[x]` done · `[-]` cut/skipped.
3. **Paste the GitHub link** into the deliverable row when a deliverable ships.
4. **Append to the Recurring Mistakes log** any pattern it saw in your code (especially Ruby-isms leaking into Python).
5. **Update Interview Weak Spots** based on how you did in the day's questions.
6. **Log applications and overrides.**

You should be able to open `PROGRESS.md` cold on any morning and know exactly what to do next — that's what `Start today` reads.

## Weekly rhythm and deliverables

Each phase ends in **one GitHub deliverable**. The authoritative week-by-week table lives in [`../Ravi_Python_LLM_Learning_Plan.md`](../Ravi_Python_LLM_Learning_Plan.md); the short version:

- **Week 0:** working env (Python 3.12+, uv, VS Code + Pylance) **+ your first job application.**
- **Weeks 1–3:** Python fundamentals — one contact-book program grown from a print statement into a tested, typed, packaged CLI. **First Python repo on GitHub.**
- **Weeks 4–5:** `evalctl` — typed, streaming CLI, plus the shared `contracts/` schemas.
- **Week 6:** Flask ingestion & webhook service (your first web framework).
- **Weeks 7–8:** Django + DRF platform core, including the N+1 before/after story.
- **Week 9:** Dockerized FastAPI + Pydantic async gateway.
- **Week 10:** SWE-bench methodology, Docker, reading real repos, first OSS PRs.
- **Weeks 11–12:** CLI agent using function calling with 2–3 real tools.
- **Weeks 13–14:** flagship mini eval-harness (SWE-bench in miniature) + resume + applications to all 3 tracks.

Honest expectation setting is baked into the plan: one or two weeks on a framework makes you productive, not expert. For your target eval roles, **Weeks 10–14 matter most** — running and testing *other people's* code, not building web apps.

## Making it stick across chat windows

`CLAUDE.md` already exists in the repo root and does this automatically: the no-code rule is absolute, the escape hatch is the verbatim override phrase, the daily loop runs every session, and `PROGRESS.md` stays current. It is inherited in every subfolder, so any window you open behaves like the same mentor.

One thing it is careful about, and you should be too: you are **senior at programming and a beginner at Python.** Those are different claims. Conflating them is exactly what produced an earlier curriculum that opened with `mypy --strict` before a single line of Python had been written.

## Getting the most out of it

- **Type everything.** The rule isn't a gimmick — muscle memory is the whole point.
- **Attempt before hint.** Struggle for 10–15 min before `Hint`. The stuck moment is where learning happens.
- **Answer interview questions out loud / in writing before reading the talking points.** Half your target interviews grade how clearly you *explain*.
- **Let the mistakes log drive review days.** Your recurring Ruby-isms are your personalized syllabus.
- **Ship the deliverable even if imperfect.** A B-grade repo on GitHub beats an A-grade one still on your laptop.
- **Tooling is not progress.** Config work feels productive because it resembles Rails work you already know. If you're polishing configuration instead of writing Python, that's the signal — go write the program.
