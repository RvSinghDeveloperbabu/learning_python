# Curriculum: LLM, Agent & Flagship (Weeks 10–14) — Your Differentiator

**Orientation:** This is the half of the plan that gets you hired. Weeks 1–9 prove you can write Python; Weeks 10–14 prove you can do the *job* of an LLM-eval / function-calling / repo-validation engineer. You already built an MCP server + OAuth + function-calling system in Ruby — this is you re-grounding that instinct in Python idioms and the industry-standard SWE-bench methodology.

**Cadence:** 6 days/week, 3–4 hrs/day. Each day = Focus / Reading / Build (with acceptance criteria) / Pitfalls / Senior signal. Ruby anchors are called out so you map, not memorize. **No Python is written for you — you type every line.**

**Prerequisite:** [`04-curriculum-core-python-and-web.md`](04-curriculum-core-python-and-web.md) through Week 9. You need Pydantic (Week 9), `Protocol` (Week 4–5 Day 7), generators, and a real pytest habit before starting here.

> **Week numbers come from [`../Ravi_Python_LLM_Learning_Plan.md`](../Ravi_Python_LLM_Learning_Plan.md)**, the single source of truth.

**Canonical docs (bookmark these):**
- Anthropic Messages API + tool use · Anthropic "Building effective agents" · Anthropic Python SDK
- OpenAI function calling guide · OpenAI Python SDK
- Prompting Guide — agents
- SWE-bench (site · paper · repo · Verified)
- Docker · Pydantic · SQLAlchemy 2.0

---

## WEEK 10 — SWE-bench methodology, Docker, reading real repos, first OSS PRs

*Goal by the end of the week: containerize an unfamiliar OSS repo, get its suite green, tie a real bug fix to the tests that verify it, explain how patches are graded — and land two small PRs.*

> **Why this comes before the agent.** The agent (Weeks 11–12) and the harness (Weeks 13–14) both assume you can take a stranger's repository and make its tests run in a container. Learn that on real repos first, with no LLM in the loop to confuse the failure signal.

### Day 1 — SWE-bench methodology, deeply
- **Focus:** how a benchmark built from real GitHub issues grades a patch by **running the repo's own test suite**.
- **Reading:** the SWE-bench site, paper (skim), and repo README; the SWE-bench Verified announcement and why it exists.
- **Build (writing, no code):** a one-page spec, in your own words, of the eval pipeline — inputs (repo@commit, issue text, gold tests), steps (apply patch → install → run selected tests), and the exact pass criterion.
- **Acceptance:** your spec names both **FAIL_TO_PASS** (tests that must flip from failing to passing) and **PASS_TO_PASS** (tests that must stay green) and explains why both matter; it explains why reproducible environments are non-negotiable.
- **Pitfalls:** describing it as "the model writes code and we eyeball it" — grading is **execution-based**, not text-similarity.
- **Senior signal:** You describe evaluation as an execution contract with an explicit result taxonomy, not a vibe check.

### Day 2 — Docker fundamentals
- **Focus:** images vs containers; `FROM`/`WORKDIR`/`COPY`/`RUN`/`CMD`; build vs run; mounting; pinning.
- **Reading:** Docker "Get started"; Docker's Python image docs.
- **Build:** a Dockerfile that builds a pinned Python image, installs one trivial dependency, and runs a single command.
- **Acceptance:** `docker build` succeeds; `docker run` executes your command; base image **and** Python version are pinned (no `:latest`).
- **Pitfalls:** `:latest` tags; `COPY . .` before dependency installation (destroys layer caching); running as root.
- **Ruby analogy:** a Dockerfile is a `Gemfile.lock` for the **entire OS + interpreter**.
- **Senior signal:** You can explain each layer and why order affects cache hits.

### Day 3 — Clone and Dockerize a real OSS library
- **Focus:** getting a stranger's test suite green in a container.
- **Reading:** the target repo's `CONTRIBUTING.md` and — critically — its `.github/workflows`. **CI config is ground truth for how maintainers actually run the tests.**
- **Build:** pick a **pure-Python** library with a clear pytest suite (`click`, `flask`, and `requests` are good first targets). Write a Dockerfile that installs it plus test dependencies and runs `pytest` to green.
- **Acceptance:** the full suite (or a documented subset) passes inside the container; reproducible from a clean build; you noted which extras/test deps were required.
- **Pitfalls:** picking a library with a **compiled core** (e.g. `pydantic`'s Rust internals) as your *first* target — you'll spend the day fighting toolchains instead of learning the method. Save those for a second pass.
- **Senior signal:** You read CI config first instead of guessing at the test command.

### Day 4 — Tie an issue to the test that proves the fix
- **Focus:** the FAIL_TO_PASS relationship, on a real repo.
- **Build (writing):** trace one closed issue → the merged PR that fixed it → the specific test(s) that verify it. Optionally check out the parent commit, watch the test fail, then check out the fix and watch it pass.
- **Acceptance:** you can point at the exact verifying test and explain the failing→passing transition; you can distinguish a behavior-verifying test from a regression guard.
- **Senior signal:** You treat "which test proves this?" as the first question about any change.

### Day 5 — Reading unfamiliar codebases fast
- **Focus:** a repeatable method — entry points → package layout → **read the tests as the spec** → follow one feature end to end → grep and go-to-definition.
- **Build (writing):** a one-page "codebase map" of a second library — top 5 modules and their responsibilities, the data flow for one feature, and where its tests live — **in under ~90 minutes**.
- **Acceptance:** the map is accurate enough to locate where a hypothetical change would go; you found that feature's tests.
- **Ruby analogy:** same as landing in a legacy Rails monolith — read `routes.rb` and the specs first.
- **Senior signal:** You have a *named, repeatable* orientation method, not "I just read around for a while."

### Day 6 — Land two OSS pull requests
- **Focus:** contributing to a repo you now understand.
- **Build:** shortlist 3–4 small issues in the repos you Dockerized (you already know how to run their suites — that's 80% of the barrier). Implement two, add or adjust the verifying test, run the suite in your Docker setup, and open the PRs described as **problem → fix → the test that proves it**.
- **Acceptance:** PRs pass the repo's CI; each description names the verifying test; branches are clean and rebased; **at least one is code, not docs-only**.
- **Pitfalls:** opening a large refactor as a first contribution; ignoring the project's own style and commit conventions.
- **Senior signal:** Your PR description reads like a bug report and its proof, not "fixed stuff."

**Week 10 interview questions:** (1) *"How does SWE-bench grade a patch?"* — execution-based; success = all FAIL_TO_PASS pass **and** all PASS_TO_PASS still pass. (2) *"You're dropped into a 50k-line repo — how do you orient?"* (3) *"Why Docker for evaluation?"*

---

## WEEKS 11–12 — `agent-cli`: the tool-use loop, by hand

*Goal: a provider-agnostic command-line agent that calls real tools under guardrails, with a structured trace.* Full spec: [`02-real-world-projects.md`](02-real-world-projects.md) → Project 5.

### Day 1 — Anthropic SDK: the Messages API
- **Focus:** content blocks, `stop_reason`, `usage`, roles — and the fact that **the API is stateless: you resend the whole message list every turn.**
- **Reading:** Messages API reference; SDK README usage; the models/pricing page (know the cost tradeoffs between tiers).
- **Build:** a script that takes a prompt from argv, prints the response text and the token usage. Key comes from a gitignored `.env`.
- **Acceptance:** runs via `uv run`; a missing API key produces a clear message, **not a traceback**; `.env` is gitignored; input and output token counts are printed.
- **Ruby analogy:** there's no ActiveRecord-style session here — think of it as rebuilding the whole request payload every call.

### Day 2 — OpenAI SDK + streaming on both
- **Focus:** comparing shapes — message list vs content blocks, `finish_reason` vs `stop_reason`; token streaming.
- **Build:** a CLI with a `--provider` flag that streams tokens to stdout from either provider.
- **Acceptance:** both providers sit behind **one interface**; streaming prints incrementally rather than in one dump; an unknown provider name fails cleanly.
- **Senior signal:** You designed a provider seam (Ruby: an adapter / duck-typed interface) rather than branching on strings everywhere. Use the `Protocol` you learned in Week 4–5.

### Day 3 — Function calling: parse only, do not execute
- **Focus:** the JSON tool schema (name, description, input schema); detecting that the model wants a tool; reading the arguments.
- **Build:** define one tool (e.g. a weather lookup). Print the chosen tool name and the parsed arguments. **Execute nothing yet.**
- **Acceptance:** your code branches on the stop reason, extracts the name and a typed argument dict, and doesn't crash when the model answers directly instead of calling a tool.
- **Pitfalls:** treating the tool description as documentation — **it is prompt text the model reads to decide.** The JSON schema is the contract.

### Day 4 — The full loop
- **Focus:** execute the tool, append the result in the correct role/format, resend, and loop until the model stops. **This is the atom of every agent.**
- **Build:** a single-tool agent that produces a final natural-language answer.
- **Acceptance:** at least one real tool executes; the result is appended with the correct role and shape; the loop terminates and **a hard iteration cap exists**.
- **Pitfalls:** no step cap (an agent that loops forever burns real money); mangling the message history so the model loses context.

### Day 5 — Agent loop as architecture
- **Focus:** a registry of 2–3 tools, dispatch by name, and the decision → execution → observation → next-decision cycle. **A state machine, not an if-ladder.**
- **Reading:** Anthropic "Building effective agents" (workflows vs agents); Prompting Guide on planning, memory, tool use.
- **Build:** an agent with a tool registry and a single dispatch loop.
- **Acceptance:** **adding a tool means registering it in one place** — no edits to the loop; multiple tool calls in one turn are handled; each decision/execution/observation is logged.

### Day 6 — Robustness: validation, retries, errors
- **Focus:** validating tool arguments with **Pydantic** before execution; API errors, timeouts, backoff.
- **Build:** a Pydantic input model per tool; a validation failure returns a **corrective tool result** to the model rather than raising.
- **Acceptance:** malformed arguments produce a corrective result the model can recover from, not an exception; transient failures retry with backoff and a cap; every tool has a typed schema consistent with its Pydantic model.
- **Note:** both SDKs already retry transient errors — your job is *tuning and bounding* that, not reinventing it.

### Days 7–12 — Build out `agent-cli` and ship (DELIVERABLE)
Work the milestones in [`02-real-world-projects.md`](02-real-world-projects.md) → Project 5: provider-agnostic loop → loop hardening (max steps, budgets, Ctrl-C flush, truncation) → real tools (`read_file`, `search_code`, `run_tests`) with a sandbox → structured trace → tests, Docker, README.

- **Acceptance highlights:** Ctrl-C mid-run leaves a **complete, parseable trace file**; a `../` or symlink path escape is refused; a destructive shell command is blocked; a hanging command is killed at timeout **with its child process group gone**; **grep the trace for your API key → zero matches**; a `FakeProvider` drives the whole suite so CI needs no network; `docker run` executes a fake-provider task end to end; **pushed to GitHub**.
- **Cut line:** `apply_patch` is the first thing to drop under time pressure — note that it weakens the "self-heal a failing test" narrative.
- **Senior signal:** You can draw the loop on a whiteboard and name every stop condition and guardrail.

**Weeks 11–12 interview questions:** (1) *"Walk me through the tool-use loop."* (2) *"Why is the tool description so important?"* (3) *"Workflow vs agent — when do you actually need a loop?"*

---

## WEEKS 13–14 — FLAGSHIP: the mini eval-harness

*Goal: a CLI that takes an OSS repo plus a candidate patch, runs it in Docker, applies the patch, runs the suite, and reports a verdict with logs.* Full spec: [`02-real-world-projects.md`](02-real-world-projects.md) → Project 6.

### Day 1 — Spec before code
- **Focus:** pipeline stages as clean seams: Config → RepoProvision → Patch → RunTests → Report. **Reuse your Week-10 SWE-bench spec.**
- **Build (writing + skeleton design):** a design doc and interface plan (English plus Pydantic field lists, no logic). Define the result type: per-test status, overall verdict, captured stdout/stderr, timings.
- **Acceptance:** every stage is an isolated unit with typed inputs and outputs; the report schema is a Pydantic model; you can name each stage's failure mode.

### Day 2 — Repo provisioning + Docker spin-up
- **Build:** a module taking repo + commit to a ready-to-test container, with a configurable base image and install command.
- **Acceptance:** fetches the exact commit and builds from clean state; a bad commit or build error returns a **typed error, not a crash**; after success, failure, **and Ctrl-C**, `docker ps -a` shows **zero** leftover harness containers.

### Day 3 — Apply the candidate patch
- **Build:** apply a unified diff inside the container against the checked-out commit.
- **Acceptance:** a valid patch applies and modifies files; a malformed or conflicting patch yields a clean "apply failed" result **distinct from a test failure**; dependencies install from the task's **vendored lockfile**, not the latest resolution.

### Day 4 — Run the suite with limits
- **Build:** run tests in-container with JUnit-XML output; capture exit code, stdout/stderr, and per-test results; enforce timeouts and resource limits.
- **Acceptance:** an infinite-loop command is killed at the timeout with total wall time within a few seconds of the limit; logs are captured **even on timeout or crash**; you can select a specific subset of tests.
- **Note:** OOM detection is best-effort on macOS (Docker Desktop's Linux VM reports it differently) — document the caveat, verify in Linux CI. The wall-clock timeout is the MVP guarantee.

### Day 5 — Assemble the CLI + test the evaluator itself
- **Build:** one command runs the pipeline and emits both a human summary and a JSON report. Write the harness's own pytest suite with the Docker/subprocess boundary **mocked** (you learned mocking in Week 3 Day 17 — this is why).
- **Acceptance:** **a crafted test that *prints* "1 passed" but actually fails is still parsed as failed** — you read the XML, not stdout; a patch that fixes FAIL_TO_PASS but breaks a PASS_TO_PASS is **UNRESOLVED** and the report **names the regressed test**; distinct exit codes for apply-failed vs tests-failed vs passed; mypy clean.
- **⚠️ The core rule:** `RESOLVED` iff every FAIL_TO_PASS passes **and** every PASS_TO_PASS still passes. `UNRESOLVED` = the patch applied and tests ran but criteria weren't met. `ERROR` = the patch didn't apply, setup failed, timeout, or OOM. **Never conflate "tests failed" with "the harness failed."**

### Day 6 — Real end-to-end demo + README (DELIVERABLE)
- **Build:** run it for real using a Week-10 fix PR — the pre-fix commit plus that PR's patch — showing FAIL_TO_PASS flipping green. Then run a deliberately broken patch and show the clear failure report. Write the README as "SWE-bench in miniature," with an architecture diagram and the three outcome types.
- **Acceptance:** public repo; the real demo case documented with actual output; a teammate with only Docker and `uv` reproduces your verdicts from a clean clone; README links your agent repo and your MCP/OAuth work.
- **Senior signal:** You can explain determinism (digest-pinned images, vendored lockfiles, recorded harness version) without hand-waving.

**Weeks 13–14 interview questions:** (1) *"Design a system that validates a code patch against a repo."* (2) *"How do you keep evaluation deterministic?"* (3) *"How do you test the evaluator itself?"*

---

## Alongside Weeks 13–14 — Resume, applications, interview prep (non-code)

These consume no build days and, being non-code, are the one place the mentor can actively draft *with* you.

- **Resume ordering:** MCP server + OAuth + function-calling (the standout) → CLI agent → mini eval-harness → OSS PRs → Django/FastAPI/Flask competence. Each bullet states what it does **and how it's verified**. Read 2–3 real job descriptions and mirror their keywords honestly. Say "working proficiency," never "expert," on one or two weeks of a framework.
- **Applications:** all three tracks — LLM Trainer (Agent Function Call), Senior Python Developer, LLM Evaluation & Repository Validation. Aim for 8–12 quality applications with a 2–3 sentence tailored intro and direct repo links.
- **Interview prep:** consolidate the talking-point banks from Weeks 10–14 plus the Senior-Python depth topics (typing/mypy, generators, context managers, decorators, dataclasses/Pydantic, async, pytest design). Build ~15 conceptual flashcards and 5 coding problems stated as **problem + acceptance criteria only**.
- **Mock run:** record five conceptual answers, one coding problem, and one "here's an unfamiliar repo, find and verify X" on the clock. Write a self-critique with three fixes.
- **⚠️ The format grades your English.** Silent problem-solving scores badly even when the code is right. Narrate your reasoning.

---

### Final deliverables checklist (all on GitHub, links in your resume)

1. Fundamentals package — Weeks 1–3
2. `evalctl` + `contracts/` — Weeks 4–5
3. Flask ingestion service — Week 6
4. Django + DRF platform core (with the N+1 story) — Weeks 7–8
5. FastAPI async gateway, Dockerized — Week 9
6. 2+ OSS PRs with verifying tests — Week 10
7. `agent-cli` function-calling agent — Weeks 11–12
8. **`eval-harness` flagship** — Weeks 13–14

**Honest calibration:** Weeks 10–14 are where eval and agent roles are won. Depth on the tool-use loop, SWE-bench grading, and the harness beats breadth everywhere else.
