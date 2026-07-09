# Weeks 5–8: Daily Curriculum — The LLM + Evaluation + Flagship Layer (Your Differentiator)

Orientation: This is the half of the plan that gets you hired. Weeks 1–4 prove you can write Python; Weeks 5–8 prove you can do the *job* of an LLM-eval / function-calling / repo-validation engineer. You already built an MCP server + OAuth + function-calling system in Ruby — Weeks 5–6 are you re-grounding that instinct in Python idioms and the industry-standard SWE-bench methodology. Weeks 7–8 turn it into a portfolio artifact and applications.

Cadence: 6 days/week, 3–4 hrs/day. Each day = Focus / Reading / Build (with acceptance criteria) / Pitfalls / Senior signal. Ruby anchors are called out so you map, not memorize. No Python is written for you — you type every line.

Canonical docs (bookmark these):
- Anthropic Messages API + tool use: `docs.claude.com/en/docs/build-with-claude/tool-use/overview` and `docs.claude.com/en/api/messages` (old `docs.anthropic.com` links redirect here)
- Anthropic "Building effective agents": `anthropic.com/research/building-effective-agents`
- Anthropic Python SDK: `github.com/anthropics/anthropic-sdk-python`
- OpenAI function calling guide: `platform.openai.com/docs/guides/function-calling`
- OpenAI Python SDK: `github.com/openai/openai-python`
- Prompting Guide agents: `promptingguide.ai/research/llm-agents`
- SWE-bench: site `swebench.com` · paper `arxiv.org/abs/2310.06770` · repo `github.com/SWE-bench/SWE-bench` · Verified `openai.com/index/introducing-swe-bench-verified`
- Docker: `docs.docker.com/get-started` · Dockerfile ref `docs.docker.com/reference/dockerfile`
- Pydantic: `docs.pydantic.dev/latest` · SQLAlchemy 2.0: `docs.sqlalchemy.org/en/20`

---

## WEEK 5 — LLM APIs, the Tool-Use Loop, and the Agent Loop Architecture

Goal by Friday: you can call both SDKs, run a full multi-turn tool-use loop by hand, and articulate the decision→execution→observation→next-action loop as an architecture, not a script.

### Day 1 — Anthropic SDK: the Messages API cold
- Focus: install `anthropic`, set `ANTHROPIC_API_KEY`, send a single Messages request, read the response object (`content` blocks, `stop_reason`, `usage`). Understand roles: system vs user vs assistant, and that the API is stateless — *you* resend the whole `messages` list each turn (Ruby analogy: no ActiveRecord session; think of it like rebuilding a request payload every call).
- Reading: Messages API reference; SDK README "Usage" section; skim the models/pricing page so you know Opus vs Sonnet vs Haiku cost tradeoffs.
- Build: a tiny script that takes a prompt from `argv`, calls Claude, prints the text and the token `usage`. Load the key from a `.env` (use `python-dotenv` or `os.environ`), never hard-code it.
- Acceptance: runs via `uv run`; missing key exits with a clear message, not a traceback; `.env` is git-ignored; prints input+output token counts.
- Pitfalls: committing keys; assuming the model "remembers" prior calls; treating `content` as a plain string (it's a list of typed blocks).
- Senior signal: you talk about the API as stateless and cost-metered from minute one, and you externalize secrets by reflex.

### Day 2 — OpenAI SDK + streaming + a thin provider abstraction
- Focus: same round-trip with `openai` (Chat Completions and note the newer Responses API exists). Compare the two SDKs' shapes: message list vs content blocks, `stop_reason` vs `finish_reason`. Add token streaming on both.
- Reading: OpenAI Python SDK README; function-calling guide intro (just the request/response shape today); Anthropic streaming docs.
- Build: extend Day 1 into a CLI that takes a `--provider anthropic|openai` flag and streams tokens to stdout as they arrive.
- Acceptance: both providers work behind one interface; streaming prints incrementally (not one final dump); unknown provider errors cleanly.
- Pitfalls: leaking provider-specific types past your boundary; forgetting to flush stdout; blocking the whole response when you meant to stream.
- Senior signal: you design a provider seam (Ruby: an adapter/duck-typed interface) so the rest of the code never knows which vendor it's talking to — exactly what eval harnesses need.

### Day 3 — Function calling / tool use: one tool, one round trip
- Focus: define a tool via JSON schema (name, description, `input_schema`), send it, detect when the model *requests* a call (`stop_reason: "tool_use"` / `finish_reason: "tool_calls"`), and read the requested arguments. Do NOT execute yet — just parse the request correctly.
- Reading: Anthropic tool-use overview + "How to implement tool use"; OpenAI function-calling guide (the schema + tool_call object sections).
- Build: define one tool (e.g., `get_weather(city)`); prompt so the model asks to call it; print the tool name and parsed arguments the model chose.
- Acceptance: your code branches on stop reason; it extracts the tool name + a typed args dict; it does not crash when the model answers directly without a tool.
- Pitfalls: vague tool descriptions (the description IS the prompt — the model picks tools off it); schema/response mismatch; assuming a tool will always be called.
- Senior signal: you already know this loop from your MCP work — say so, and frame the JSON schema as the contract between model and code.

### Day 4 — The full loop: execute, feed the result back, repeat until done
- Focus: complete the cycle — take the model's tool request, run the real function, append a `tool_result` (Anthropic) / tool message (OpenAI) back into `messages`, resend, and loop until `stop_reason` is `end_turn`/`stop`. This is the atom of every agent.
- Reading: re-read the "returning results to the model" sections of both tool-use guides; Prompting Guide "LLM Agents" intro.
- Build: turn Day 3 into a working single-tool agent that answers a question requiring the tool, feeds the result back, and returns a final natural-language answer.
- Acceptance: at least one real tool executes; the tool result is appended with the correct role/format; the loop terminates on a stop condition and never infinite-loops; a hard iteration cap exists.
- Pitfalls: forgetting to append the assistant's tool-request message before the tool result (breaks the transcript); wrong `tool_use_id` pairing; no max-turns guard.
- Senior signal: you build in a turn cap and treat the message list as an append-only transcript you own — reliability thinking, not demo thinking.

### Day 5 — Agent loop as architecture: multiple tools, dispatch, observation
- Focus: generalize to a registry of 2–3 tools with a dispatch step (name → handler), and reason about the loop as decision → execution → observation → next-decision. Handle parallel/multiple tool calls in one turn. Map to a state machine, not an if-ladder.
- Reading: Anthropic "Building effective agents" (workflows vs agents; when a loop is warranted); Prompting Guide agents pages on planning/memory/tool-use.
- Build: an agent with a tool registry (2–3 tools, e.g., calculator, file-reader, a mock API) and a single loop that dispatches whichever tools the model requests each turn.
- Acceptance: adding a new tool = registering it in one place (no loop edits); handles a turn with multiple tool calls; logs each decision/execution/observation step.
- Pitfalls: hard-coding tool dispatch in the loop body; ignoring the case of several tool calls per turn; no logging so failures are invisible.
- Senior signal: you separate the *loop mechanism* from the *tool set* (open/closed principle) and can whiteboard the agent loop as a cycle — the #1 thing "LLM Trainer – Agent Function call" interviews probe.

### Day 6 — Robustness + typed tool args with Pydantic (ship prep)
- Focus: production hardening — API error/timeout handling, retries with backoff, and validating tool arguments with Pydantic before executing (bad args → structured error back to the model, not a crash). This is the Pydantic-everywhere lesson from Week 4 applied to tools.
- Reading: Pydantic docs (models + validation); both SDKs' error/retry sections.
- Build: wrap each tool's inputs in a Pydantic model; on validation failure, return the error as a tool result so the model can self-correct; add retry on transient API errors.
- Acceptance: malformed model-supplied args produce a corrective tool_result, not an exception; transient failures retry with backoff and a cap; every tool has a typed input schema derived from/consistent with its Pydantic model.
- Pitfalls: catching bare `Exception`; retrying non-idempotent side effects; letting Pydantic errors bubble up instead of feeding them back to the model.
- Senior signal: you close the loop on *failure* — the model proposing bad args and your system coaching it back is the exact resilience eval interviewers look for.

Week 5 interview questions (talking-points reference — study these, don't just read):
1. "Walk me through the tool-use loop." — Model sends messages + tool schemas → model returns a tool_use request with args → your code validates + executes → you append the assistant request AND the tool_result to the transcript → resend the full list → repeat until a natural stop reason. Emphasize: API is stateless, transcript is append-only, you need a turn cap and error-feedback path.
2. "Why is the tool description so important?" — It's effectively prompt text; the model selects and fills tools purely from name/description/schema. Vague descriptions cause wrong-tool and bad-arg calls. The JSON schema is the contract.
3. "Workflow vs agent — when do you actually need a loop?" — Per Anthropic's framing: prefer the simplest thing; use fixed workflows when steps are known, use an agentic loop only when the path is dynamic and the model must decide next actions from observations. Unbounded loops = cost + reliability risk.

---

## WEEK 6 — SWE-bench Methodology + Clone→Dockerize→Run-Tests + Reading Codebases Fast

Goal by Friday: you can take an unfamiliar Python OSS repo, containerize it, get its test suite green, tie a real bug fix to the tests that verify it, and you understand SWE-bench well enough to explain how patches are graded. Ship the Weeks 5–6 CLI-agent deliverable.

### Day 1 — SWE-bench: the methodology, deeply
- Focus: what SWE-bench actually is — real GitHub issues + the repo state, where a candidate patch is graded by running the repo's own test suite (FAIL_TO_PASS = tests that must flip to passing; PASS_TO_PASS = tests that must stay green). Understand SWE-bench Verified and why it exists (noisy/underspecified tasks removed). This is the mental model your flagship harness will imitate.
- Reading: SWE-bench paper (`arxiv.org/abs/2310.06770`) — read intro, task construction, and evaluation sections; the site; OpenAI's SWE-bench Verified announcement.
- Build (writing, no code): a one-page written spec, in your own words, of the SWE-bench evaluation pipeline: inputs (repo@commit, issue, gold tests), steps (apply patch → install → run selected tests), and the exact pass criterion.
- Acceptance: your spec names FAIL_TO_PASS and PASS_TO_PASS and explains why both matter; explains why Docker/reproducible envs are non-negotiable.
- Pitfalls: thinking SWE-bench grades text similarity (it grades *test execution*); ignoring PASS_TO_PASS (a patch that fixes the bug but breaks other tests fails).
- Senior signal: you frame evaluation as "did the test suite verify the behavior," which is exactly the repo-validation role.

### Day 2 — Docker for reproducible test environments
- Focus: images vs containers, `Dockerfile` (`FROM`, `WORKDIR`, `COPY`, `RUN`, `CMD`), build vs run, mounting the repo, why pinned base images + pinned deps = reproducibility. Ruby analogy: a Dockerfile is a Gemfile.lock for the *entire OS + interpreter*.
- Reading: Docker get-started; Dockerfile reference; Python image docs on Docker Hub.
- Build: write a Dockerfile that builds a Python 3.x image, installs a trivial dependency, and runs a one-line command; build and run it.
- Acceptance: `docker build` succeeds; `docker run` executes your command; base image and Python version are pinned (no `:latest`).
- Pitfalls: `:latest` drift; giant images from copying `.git`/venvs (use `.dockerignore`); rebuilding everything on every code change (layer-cache ordering).
- Senior signal: you order layers for cache efficiency and pin versions — you think about reproducibility as a first-class property.

### Day 3 — Clone + Dockerize OSS lib #1, get the suite green
- Focus: pick a well-tested, medium-size pure-Python library (e.g., `httpx`, `click`, `flask`, `requests`, `pydantic` — pick one with a clear pytest suite and a CONTRIBUTING guide). Clone it, read its dev-setup docs, and reproduce its test suite inside Docker.
- Reading: the target repo's README + CONTRIBUTING + its CI config (`.github/workflows`) — CI is the ground truth for how maintainers run tests.
- Build: a Dockerfile (or use their dev container if provided) that installs the lib + test deps and runs `pytest` to green.
- Acceptance: the full suite (or a documented subset) runs in your container and passes; you can re-run reproducibly from a clean build; you noted which extras/test deps were needed.
- Pitfalls: missing system libs (compilers, headers); test deps hidden in `pyproject`/`tox`/`nox` extras; network-dependent tests you must skip/mark.
- Senior signal: you go straight to CI config to learn the canonical test command instead of guessing — the fastest path into any repo.

### Day 4 — Tie a closed issue to the fix PR to the tests that verified it
- Focus: in the same repo, find a closed bug issue with a linked merged fix PR. Read the PR diff and identify the test(s) added/changed — the FAIL_TO_PASS equivalent. Confirm you understand how the test would fail on the old code and pass on the new.
- Reading: the issue thread, the PR discussion, the diff (separate the test changes from the source changes).
- Build (writing): a short written trace: issue → root cause → source change → the specific test that now proves it. Optionally check out the parent commit and run just that test to watch it fail, then the fix commit to watch it pass.
- Acceptance: you can point to the exact test(s) that verify the fix and explain the failing→passing transition; you distinguish the behavior-verifying tests from regression guards.
- Pitfalls: conflating the fix with the test; assuming every PR adds a test (some don't — a signal in itself).
- Senior signal: you reason in "what test proves this behavior" — the core competency of LLM-eval / repo-validation work.

### Day 5 — Reading unfamiliar codebases fast (technique) + apply to lib #2
- Focus: a repeatable method — start at entry points (`__main__`, CLI, top-level `__init__`), map the package layout, read the tests to learn intended behavior, follow one feature end-to-end, use `grep`/ripgrep and "go to definition." Build a mental module map before reading line-by-line. Ruby analogy: same as landing in a legacy Rails monolith — read `routes.rb` and specs first.
- Reading: skim a second OSS repo's structure; Prompting Guide/agent-eng notes on code navigation are optional.
- Build (writing): a 1-page "codebase map" of lib #2 — top 5 modules and their responsibilities, the main data flow for one feature, and where the tests for it live — produced in under ~90 minutes.
- Acceptance: the map is accurate enough that you could locate where you'd make a hypothetical change; you found the feature's tests.
- Pitfalls: reading top-to-bottom alphabetically; getting lost in utils; not using the tests as documentation.
- Senior signal: you have a *system* for cold codebases and can state your time-boxed method aloud — directly tested in eval interviews ("here's an unfamiliar repo, find X").

### Day 6 — Dockerize lib #2 + ship the CLI-agent deliverable
- Focus: repeat the Docker+tests drill on lib #2 to prove it's a repeatable skill, then finalize and push the Weeks 5–6 GitHub deliverable: your function-calling CLI agent (2–3 tools, typed args, robust loop) with a README.
- Reading: revisit your Week 2 pytest habits; skim a couple of strong OSS READMEs as templates.
- Build: (a) lib #2 suite green in Docker; (b) polish the Day-6-Week-5 agent — README with architecture diagram of the loop, usage, and a pytest suite covering the dispatch + a validation-failure path.
- Acceptance: agent repo on GitHub is public, has type hints (mypy-clean), passing pytest, a README that explains the agent loop, and runs via `uv run`; both Dockerized libs documented in a short notes file.
- Pitfalls: shipping the agent with no tests or no README; leaving keys/`.env` tracked; a README that shows usage but never explains the loop.
- Senior signal: your README teaches the tool-use loop and names your prior MCP/OAuth work — recruiters see the differentiator in 30 seconds.

Week 6 interview talking-points reference:
1. "How does SWE-bench grade a patch?" — Apply the candidate patch to the repo@commit in an isolated env, install, run the designated tests; success = all FAIL_TO_PASS now pass AND all PASS_TO_PASS still pass. It's execution-based, not text-based. Verified removes ambiguous tasks.
2. "You're dropped into a 50k-line repo — how do you orient?" — Entry points → package/module map → read tests as spec → trace one feature end-to-end → grep + jump-to-def; time-boxed, produce a written map. CI config = canonical test command.
3. "Why Docker for evaluation?" — Determinism and isolation: pinned OS/interpreter/deps so a pass/fail is attributable to the patch, not the host. Layer caching + `.dockerignore` for speed; no `:latest`.

---

## WEEK 7 — Flagship: The Mini Eval-Harness (SWE-bench in Miniature)

Goal by Friday: a working CLI tool that takes an OSS repo + a candidate patch, spins it up in Docker, applies the patch, runs the test suite, and reports pass/fail with logs. This is your portfolio centerpiece — build it as a real project (typed, tested, documented).

### Day 1 — Design the harness (spec before code)
- Focus: architecture and interfaces. Define the pipeline stages as clean seams: `Config → RepoProvision → Patch → RunTests → Report`. Decide inputs (repo URL/path + commit, patch file, test command or auto-detect) and the report schema. Reuse the Week-6 SWE-bench spec.
- Reading: re-skim SWE-bench harness repo structure for inspiration (not to copy); Pydantic (for config + report models); `argparse`/`typer` docs for the CLI.
- Build (writing + skeleton design): a written design doc + module/interface plan (English + Pydantic model field lists, no logic). Define the `EvalResult` shape (per-test status, overall pass/fail, captured stdout/stderr, timings).
- Acceptance: every stage is an isolated unit with a typed input/output; the report schema is a Pydantic model; you can name the failure mode of each stage.
- Pitfalls: one giant `main()`; entangling Docker calls with reporting; no schema for results.
- Senior signal: you spec interfaces and data shapes first — the harness reads like a designed system, not a script.

### Day 2 — Repo provisioning + Docker spin-up
- Focus: implement the stage that clones/copies a repo at a given commit and builds a container able to install and test it. Support a configurable or auto-detected base image + install command.
- Reading: Docker CLI reference; the Python `subprocess` docs (running docker/git safely); optionally the `docker` Python SDK.
- Build: the provisioning module — given repo+commit, produce a ready-to-test container.
- Acceptance: from a clean state it fetches the exact commit and builds an image that has deps installed; failures (bad commit, build error) return a typed error, not a crash; the base image/install command is configurable.
- Pitfalls: shell-injection via unsanitized repo/patch inputs to subprocess; not pinning the checkout commit; leaking containers/images (clean up).
- Senior signal: you treat external inputs as untrusted and manage container lifecycle — security + ops awareness.

### Day 3 — Apply the candidate patch
- Focus: implement patch application (`git apply` / `patch`) inside the container against the checked-out commit, capturing whether it applied cleanly.
- Reading: `git apply` docs; how unified diffs work; SWE-bench's patch-application approach in the paper.
- Build: the patch stage — input a diff, apply it, report applied/failed-to-apply with the reject details.
- Acceptance: a valid patch applies and modifies files; a malformed/conflicting patch is reported as a clean "apply failed" result (distinct from a test failure); the pre-patch state is reproducible.
- Pitfalls: conflating "patch didn't apply" with "tests failed" — they're different outcomes and interviewers will probe this; path/strip-level (`-p`) mistakes; applying against the wrong commit.
- Senior signal: you model the three-way outcome (apply-fail vs test-fail vs pass) explicitly — the exact nuance SWE-bench harnesses must get right.

### Day 4 — Run the test suite + capture pass/fail + logs
- Focus: run the target's tests in the container (auto-detect or configured command; ideally support selecting specific tests like FAIL_TO_PASS/PASS_TO_PASS), capture exit code, stdout/stderr, and per-test results (parse pytest output or use `--junitxml`).
- Reading: pytest docs on exit codes, `-k`/node IDs, and JUnit XML output.
- Build: the test-runner stage returning a structured result (overall + optionally per-test), with full logs captured.
- Acceptance: exit code correctly maps to pass/fail; logs are captured even on timeout/crash; supports running a specified subset; timeouts are enforced so a hanging suite can't wedge the harness.
- Pitfalls: relying only on exit code when you need per-test granularity; losing logs on crash; no timeout; assuming every repo uses pytest.
- Senior signal: you capture evidence (logs, per-test status) so a result is *auditable* — evaluation is worthless if you can't show why.

### Day 5 — Report + CLI + tests + polish
- Focus: assemble the pipeline behind a CLI, emit a human-readable report and a machine-readable one (JSON via the Pydantic model), and write the harness's own pytest suite (mock the Docker/subprocess boundary so tests are fast and hermetic).
- Reading: pytest fixtures/monkeypatch; Typer/argparse for the CLI surface; JSON serialization from Pydantic.
- Build: end-to-end CLI (`eval-harness --repo … --commit … --patch … [--tests …]`) → prints pass/fail summary + writes a JSON report; unit tests for each stage with the external boundary mocked.
- Acceptance: one command runs the whole pipeline; outputs both pretty and JSON reports; mypy-clean; the harness's own tests pass; a distinct exit code for apply-fail vs test-fail vs pass.
- Pitfalls: untested harness (ironic and disqualifying); hitting real Docker in unit tests (slow/flaky — mock the seam); a report a human can't act on.
- Senior signal: you built an evaluator that is itself tested and produces auditable JSON — meta-quality that eval teams love.

### Day 6 — Real end-to-end run + README + demo
- Focus: run the harness on a *real* case — take one of the Week-6 fix PRs, feed the pre-fix commit + the PR's patch, and show FAIL_TO_PASS flipping green (and a broken patch producing a clear failure report). Write a README that frames this as SWE-bench-in-miniature and push to GitHub.
- Reading: strong OSS README examples; your own Week-6 issue→PR→test trace to reuse as the demo case.
- Build: a recorded/scripted demo run + a README with architecture diagram, the three outcome types, a real example, and a "how this mirrors SWE-bench" section.
- Acceptance: public repo, CI badge optional, real demo case documented with output, README explains methodology and ties to SWE-bench; links your agent repo and MCP/OAuth work.
- Pitfalls: demoing only the happy path (show an apply-fail and a test-fail too); a README without an architecture diagram.
- Senior signal: you can hand an interviewer a repo that *is* the job — "give me a repo and a patch, I'll tell you if it passes, with logs."

Week 7 interview talking-points reference:
1. "Design a system that validates a code patch against a repo." — Stages: provision (repo@commit in Docker) → apply patch → run selected tests → report. Isolated, typed I/O per stage; three outcomes (apply-fail / test-fail / pass); capture logs for auditability; enforce timeouts; sanitize external inputs.
2. "How do you keep evaluation deterministic?" — Pinned base image + pinned deps + exact commit; isolated container per run; no network in tests where avoidable; capture full environment in the report.
3. "How do you test the evaluator itself?" — Mock the Docker/subprocess boundary, unit-test each stage's success/failure paths, keep a small real end-to-end integration test behind a marker.

---

## WEEK 8 — OSS PRs, Resume, Applications, and Interview Prep

Goal by Friday: 2–4 merged/open small PRs, a resume with a Python + LLM-eval section leading with your differentiator, applications submitted to all three tracks, and interview reps done.

### Day 1 — Scope 2–4 small OSS contributions
- Focus: find genuinely small, real contributions in Python OSS you already Dockerized (docs fixes, type-hint additions, a small bug with a failing test, a flaky-test fix). Use your Week-6 repos — you already know how to run their suites, which is 80% of the barrier.
- Reading: each repo's CONTRIBUTING; "good first issue"/"help wanted" labels; recent merged PRs to learn the maintainers' style.
- Build (writing): a shortlist of 3–4 candidate issues with a one-line plan and the test you'd add/fix for each.
- Acceptance: each candidate is small, has a clear acceptance test, and fits the repo's contribution norms; at least one is a code (not docs-only) change.
- Pitfalls: overscoping (a 500-line refactor won't merge); ignoring the style guide; picking dead repos.
- Senior signal: you scope contributions like a maintainer — small, tested, aligned to conventions.

### Day 2 — Land the PRs
- Focus: implement, add/adjust tests, run the suite in your Docker setup, open PRs with clear descriptions (problem → fix → test proving it). Respond to CI.
- Reading: the repo's PR template + CI config; git branching/`gh pr create` (you already know git).
- Build: open 2+ PRs; each includes a test that verifies the change.
- Acceptance: PRs pass the repo's CI; each PR description names the verifying test; branch is clean and rebased.
- Pitfalls: PRs with no test; failing lint/format checks; wall-of-text descriptions.
- Senior signal: every PR ships with the test that proves it — the exact discipline of repo-validation roles.

### Day 3 — Resume: Python + LLM-eval section
- Focus: rewrite your resume to lead with the differentiator. New/updated section ordering: MCP server + OAuth + function-calling (your standout) → the CLI agent → the mini eval-harness (SWE-bench-in-miniature) → OSS PRs → Django/FastAPI competence. Translate Rails seniority into Python-role language.
- Reading: 2–3 real "LLM Trainer / LLM Evaluation / Senior Python" job descriptions — mirror their keywords honestly (tool use, function calling, agent loops, test-suite verification, Docker, Pydantic, FastAPI).
- Build (writing): a one-page resume section + 3 bullet-point project blurbs (impact + tech + verification).
- Acceptance: MCP/function-calling appears in the top third; each project bullet states what it does AND how it's verified/tested; no unbacked buzzwords.
- Pitfalls: burying the differentiator; listing tech without outcomes; claiming "expert" on one week of Django/FastAPI (say "working proficiency").
- Senior signal: your resume reads as an evaluation/agent engineer with deep prior systems experience, not a Python beginner.

### Day 4 — Applications to all three tracks
- Focus: apply to (1) LLM Trainer – Agent Function call, (2) Senior Python Developer, (3) LLM Evaluation & Repository Validation. Tailor the lead sentence of each to the track; link the agent repo + eval-harness repo + merged PRs.
- Reading: each posting's must-haves; company's product so your note is specific.
- Build (writing): submit a batch (aim 8–12 quality applications), each with a 2–3 sentence tailored intro and direct repo links.
- Acceptance: all three tracks covered; every application links live GitHub repos; intros are role-specific, not copy-paste.
- Pitfalls: spray-and-pray with dead links; identical cover notes; forgetting to make repos public.
- Senior signal: you lead with a working eval-harness and real PRs — proof over claims.

### Day 5 — Interview prep: conceptual talking points + coding-style problems
- Focus: consolidate the Weeks 5–7 talking-point banks and drill Senior-Python-depth topics (the interview PRIMARY): typing/mypy, generators/iterators, context managers, decorators, dataclasses/Pydantic, async/await, pytest design, plus the agent-loop and SWE-bench answers. Practice *saying* answers aloud (half the grade is clear English reasoning).
- Reading: your own Week 1–7 notes; Anthropic tool-use + "Building effective agents" once more for crisp phrasing.
- Build (writing): a Q&A flashcard set — ~15 conceptual (with 3–4 talking-point bullets each) and 5 coding-style problems stated as problem + acceptance criteria only (e.g., "write a retrying, rate-limited async client for the Messages API — criteria: backoff, cap, typed errors, tested" — you solve these yourself, no solutions provided).
- Acceptance: you can deliver each conceptual answer in <90 seconds aloud; each coding problem has crisp acceptance criteria you could code against.
- Pitfalls: memorizing without out-loud practice; coding problems without acceptance criteria; neglecting Senior-Python depth for only LLM topics.
- Senior signal: you explain *why*, not just *what*, and state acceptance criteria before coding — senior behavior.

### Day 6 — Mock AI video interview + coding/analysis screen
- Focus: full dress rehearsal. Record yourself answering 5 conceptual + walking through 1 coding-style problem and 1 "here's an unfamiliar repo, find/verify X" exercise on the clock. Review the recording for clarity and pacing.
- Reading: none new — perform.
- Build (writing/recording): a recorded mock (video for the AI-interview format) + a written self-critique with 3 fixes.
- Acceptance: you complete a timed conceptual round + a live repo-navigation demo using your Week-6 method; self-critique names concrete improvements.
- Pitfalls: rambling; silent problem-solving (narrate your reasoning — the format grades your English explanation); skipping the recording review.
- Senior signal: you narrate reasoning clearly under time and can cold-navigate a repo on camera — precisely what the AI video + analysis screens measure.

Final deliverables checklist (all on GitHub, links in resume):
- CLI function-calling agent (2–3 tools, typed, tested, README explains the loop) — Weeks 5–6
- Mini eval-harness (repo → Docker → apply patch → run tests → pass/fail + logs, tested, SWE-bench-framed README) — Week 7 flagship
- 2–4 OSS PRs, each with a verifying test — Week 8
- Resume with Python + LLM-eval section leading with MCP/function-calling/OAuth — Week 8
- Applications to all three tracks with live repo links — Week 8

Honest calibration: Weeks 5–7 are where eval/agent roles are won — they're about running and verifying *other people's* code, which is your MCP/function-calling instinct plus Docker plus the test-suite mindset. Depth on the tool-use loop, SWE-bench grading, and the eval-harness beats breadth everywhere else.
