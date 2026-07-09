### 14.18 Statistical rigor: single runs lie [Senior+/Staff] — Conceptual

A teammate reports "the new prompt improved pass rate from 71% to 74% — ship it." As the eval owner, why is that claim potentially meaningless, and how do you make eval comparisons trustworthy given stochastic model outputs?

**Talking points:**
- LLM outputs are **nondeterministic** — even at `temperature=0` you're not guaranteed identical outputs (batching/hardware/floating-point, provider changes). A single run per task is a **sample**, not a measurement; a 3-point move can be pure noise.
- Report **distributions, not point estimates**: run each task **N times**, report mean **with a confidence interval** (bootstrap, or a binomial CI on pass rate). For "can it solve this at all," use **pass@k**; for reliability, use pass rate over many samples.
- **Powering the comparison:** with a few hundred tasks, a 3-point difference may be within the CI — compute whether it's significant (a paired test like **McNemar** on per-task pass/fail, since it's the same tasks under two conditions). Don't compare two systems on *one prompt each*.
- Separate **eval variance** (sampling noise) from a **real** capability change; watch for **contamination** and **metric drift** when the judge, dataset, or scoring code changes underneath you.
- Practical: fix seeds where possible, pin the dataset, version the harness, and store per-sample results so CIs and significance can be recomputed later.
- Rails contrast: it's the flaky-test problem turned into a measurement problem — you can't `--only-failures` your way to a trustworthy benchmark; you need statistics.

---

### 14.19 Streaming responses and incremental tool-call assembly [Senior] — Conceptual/gotcha

An agent streams the model's response for low latency. A developer tries to parse and execute a tool call from the partial stream and hits malformed-JSON errors. Explain how streamed tool calls arrive and the correct handling.

**Talking points:**
- Streaming delivers **incremental deltas** (SSE-style events): text tokens arrive as text deltas, and a tool call's `input` arrives as a series of **partial JSON fragments** (`input_json_delta`) that only form valid JSON once the block is **complete**. Parsing/validating/executing mid-stream is the bug — you must **buffer the fragments per content block and assemble** before `json.loads` and schema-validation.
- You branch on the **terminal `stop_reason`** (from the final message event), not on partial content — don't act on a tool call until its block has ended and the turn's stop reason is known.
- Streaming buys **time-to-first-token / perceived latency** and progress display, but adds complexity: mid-stream connection drops (partial state — discard, don't execute), and you still can't execute anything until the tool `input` is whole.
- Same conversation-shape rules apply after assembly (one `tool_result` per `tool_use_id`, errors as `is_error`) — streaming changes *how you receive*, not *the protocol you honor*.
- Senior tell: separating "stream text to the user for UX" from "buffer tool_use JSON for correctness" — different completion conditions.

---

### 14.20 Prompt caching mechanics and token/cost accounting in the loop [Senior] — Conceptual

Agent loops resend a growing transcript every turn (Q14.14). Explain how prompt caching changes the cost/latency picture, why *ordering* your context matters, and how you'd do token accounting to enforce a budget. (Verify current provider specifics against docs.)

**Talking points:**
- Providers cache a **stable prefix** of the request; a cache *hit* on that prefix is much cheaper and faster than reprocessing it. So **put stable, reused content first** (system prompt, tool definitions, long fixed context) and **volatile content last** (the latest turn) — any change to the prefix **invalidates** the cache from that point on.
- The agent-loop tension: the transcript *grows*, so if you append and never mutate the early prefix, the stable head stays cacheable across turns — but **pruning/summarizing early history to fight context bloat *invalidates* the cache**. A real trade-off (cache savings vs context-window/quality) that a senior names rather than treating caching as free.
- **Cost is asymmetric:** output tokens typically cost more than input, and cached input reads cost less than fresh input — so budget logic must account for input/output/cache-read separately, not a single token count. Track usage per turn from response metadata and enforce a hard budget (Q14.2) against the *actual* accounted tokens.
- Caching helps cost/latency but **does not bound growth** — you still need context management (truncate large tool results *before* they enter the window). Caching and pruning solve different problems.
- Provider-specific details (cache breakpoints, TTL, minimum cacheable size, pricing) change — the senior move is to state the mechanism and **verify current numbers in the docs**, not quote from memory.

---

**Interviewer usage note.** Q14.4, 14.9, 14.14, and 14.19 are the fast gotchas — they separate someone who has *built* an agent loop from someone who has read about one. Q14.5, 14.6, 14.11, 14.12, 14.16, and 14.18 are the depth probes; for a candidate with real MCP/OAuth/function-calling experience, lead with Q14.12 and Q14.16 — the credential-boundary reasoning is the standout differentiator.

---

## 15. System Design & Behavioral

Conceptual questions include a Talking-points answer key; coding/design questions give a problem + acceptance criteria and What a strong answer demonstrates. Half the grade in the AI video-interview screen is clarity of reasoning in plain English — practice these *out loud*.

> Consolidation notes: the *mutable default* and *lambda-in-a-loop* gotchas are canonical in [Functions & Scope](#2-functions-scope--decorators) (Q5, Q2). They're worth keeping in a behavioral screen only as a fast "did you internalize Python's model coming from Ruby" filter — deliver them in 30 seconds and move on. The *blocking-call-in-async* debugging scenario (Q15.8 below) is a behavioral/framework variant of [Concurrency Q6](#6-concurrency--async); the GIL question (Q15.16) is the behavioral framing of [Concurrency Q1](#6-concurrency--async).

---

### 15.1 Your code-review philosophy [Senior] — Conceptual

You've joined a contract team and are handed 30 PRs a week to review in a language you're newer to (Python). What does your review optimize for, and how do you review *well* without becoming the bottleneck or the nitpicker?

**Talking points:**
- Separate three layers explicitly: (1) correctness & failure modes, (2) design/interface fit, (3) style/nits — treat only the first two as blocking. Push nits to the linter/formatter.
- Automate the boring layer first: `black`/`ruff` + `mypy` + CI means you never hand-review formatting or obvious type errors. (This is your RuboCop, but Python also gives you real static typing.)
- Review the *diff's blast radius*, not just the diff: what callers depend on this, what invariant could break silently, what's the rollback story.
- Ask questions instead of issuing verdicts ("what happens if this list is empty?") — surfaces reasoning and teaches, which matters more on short contracts.
- Distinguish "different from how I'd do it" from "wrong." As the newer-to-Python person, name that humility explicitly: defer on idiom, hold firm on correctness.
- Timeboxing: a 400-line PR gets "please split, I can't review this safely" rather than a rubber stamp.

---

### 15.2 Landing in a large, undocumented, unfamiliar codebase [Senior+/Staff] — Conceptual

You're dropped into a 200k-line Python repo you've never seen and given a bug to fix within days. Walk me through *exactly* how you build a mental model fast. This is a core skill for the target roles — treat it seriously.

**Talking points:**
- Start *outside in*: entry points (CLI `__main__`, web routes, `pyproject.toml` scripts, Dockerfile CMD) tell you how it's run. The test suite tells you what behavior the authors care about.
- Get it *running* before reading deeply — Docker up, tests green locally. You can't reason about code you can't execute (literally the SWE-bench workflow: reproduce, then localize).
- Localize with tooling, not eyeballs: `ripgrep` for the error string, `git log`/`git blame` on the suspect file, `git bisect` for a regression. Follow the stack trace to the top of user code, not framework internals.
- Read the *data model / schema first* — in Django that's `models.py`; the shape of the data constrains everything. (Your Rails instinct: open `db/schema.rb` and the models first — same move.)
- Trace one real request end-to-end with a debugger or strategic logging. Depth on one path beats shallow coverage of all paths.
- Write a failing test that reproduces the issue *before* fixing — proves you understand the bug and guards the fix.
- Know when to stop reading: you need the sub-graph your change touches and its callers, not the whole repo.

---

### 15.3 Async vs. background queue vs. cache — the decision, not the definitions [Senior+/Staff] — Conceptual

For a slow endpoint, when do you reach for `async`/`await`, when for a background job queue, and when for a cache — and when do these *not* help?

**Talking points:**
- `async` buys concurrency for **I/O-bound waiting** on a single thread — one worker juggles many in-flight waits. Does **nothing** for CPU-bound work, and (GIL) does not parallelize computation.
- A **queue** is for work that's slow, can happen *out of band*, or needs retries/durability — moves latency off the request path and adds backpressure. Your Sidekiq/ActiveJob instinct transfers directly.
- A **cache** attacks *repeated* work with a *read-heavy, staleness-tolerant* access pattern. If every request is unique or must be fresh, cache is wrong.
- Failure-mode literacy is the senior signal: async → "one blocking call poisons the loop"; queues → at-least-once delivery / idempotency / poison messages; caches → invalidation and stampede.
- Trap answer: reaching for async to "make it faster" when the bottleneck is a CPU-bound loop or a single slow query — the fix there is an index or an algorithm.
- Order of operations: measure first. Profile to know if you're I/O-bound or CPU-bound *before* choosing the tool.

---

### 15.4 Design an HTTP API for a long-running eval submission service [Senior] — Coding-style

**Problem:** Design the HTTP API for a service where clients submit a repo + candidate patch, the server runs the repo's test suite in isolation (minutes), and clients retrieve pass/fail + logs. Specify endpoints, resource model, status/error semantics, and how clients get results.

**Acceptance criteria:**
- Clear resource modeling and URL structure; correct verbs and status codes.
- A concrete answer for the long-running-job problem (the request can't block for minutes).
- Idempotency story for submission (retries must not double-run).
- Pagination and filtering for listing past runs; consistent, machine-parseable error shape.
- Authentication/authorization and rate-limiting addressed at least at a design level.
- Versioning strategy.

**What a strong answer demonstrates:**
- Async job pattern: `POST` returns `202 Accepted` + a job resource/URL, client polls `GET /jobs/{id}` (or webhooks/SSE) — not a synchronous 30-minute HTTP call.
- Idempotency keys or a client-supplied submission ID so retries are safe.
- Distinguishing 4xx (client's fault, don't retry) from 5xx (server's fault, retryable) in the contract.
- Cursor vs offset pagination trade-off.
- The *contract as a product*: stable, documented (OpenAPI/Swagger — you've done this in Grape), evolvable without breaking clients.
- Bonus: where Pydantic/FastAPI would enforce the request/response schema and auto-generate the doc.

---

### 15.5 What genuinely surprised you about Python coming from Rails? [Senior] — Conceptual

Tell me three things about Python/its ecosystem that surprised you — good or bad — and what you changed in your habits. (These roles grade communication; a vague answer is a red flag.)

**Talking points (pick the true ones and say them crisply):**
- **Explicit over convention.** Rails prizes magic (method_missing, autoloading, `params`); Python prizes explicitness — you import what you use, and Django is far less magical than Rails.
- **Real static typing exists and teams use it.** Type hints + `mypy` give a compile-ish net Ruby's Sorbet never made mainstream. You started annotating and running mypy in CI.
- **The GIL.** Threads don't parallelize CPU work — changed how you think about concurrency (async for I/O, multiprocessing/queues for CPU).
- **Mutable default arguments** — Ruby re-evaluates defaults each call, Python doesn't.
- **Packaging.** No single blessed path historically; `uv`/`pyproject.toml` is the modern answer, but the fragmentation surprised you vs Bundler's one true way.
- **Truthiness & `is` vs `==`.** Empty collections are falsy; `is` is identity not equality — a real bug source.
- The meta-move: don't just list surprises, say *what habit changed* — that signals seniority and self-awareness.

---

### 15.6 Fast Ruby→Python gotcha — the mutable default [Senior]

*(Behavioral-screen version; the full treatment is [Functions & Scope Q5](#2-functions-scope--decorators). Deliver in 30 seconds.)*

`def append_and_return(item, bucket=[])` appends `item` to `bucket` and returns it, called three times in a loop with no `bucket`. What does the third call return, why, and how do you explain the fix in one sentence?

**What a strong answer demonstrates:**
- Predicts the accumulation (`[a]`, `[a,b]`, `[a,b,c]`) — the default is built **once, at function-definition time**, and shared across calls.
- Names the rule and idiom (sentinel `None`, build the real object inside the body).
- The Rails contrast lands: `def f(bucket = [])` re-evaluates every call, so a Rubyist walks into it.
- Communication: explains it plainly ("the default is built once and reused, not rebuilt each call") — half the grade is the explanation.

---

### 15.7 Fast Ruby→Python gotcha — the loop of lambdas [Senior]

*(Behavioral-screen version; full treatment is [Functions & Scope Q2](#2-functions-scope--decorators). Deliver in 30 seconds.)*

`funcs = [lambda: i for i in range(3)]`, then all three are called. What prints, what's the mechanism, and where has this bitten real code?

**What a strong answer demonstrates:**
- Predicts `[2, 2, 2]` and names **late binding**: closures capture the variable `i`, not its value; by call time the loop finished and `i == 2`.
- One fix in words (default-arg capture, or a factory function).
- Real-world grounding: callbacks, deferred tasks, retry wrappers built in a loop.
- Rails contrast: Ruby block params are block-local, so `(0..2).map { |i| -> { i } }` each capture their own `i`.

---

### 15.8 Debug the async endpoint that "isn't concurrent" [Senior+/Staff] — Conceptual/find-the-bug

A teammate wrote an `async def` FastAPI endpoint to fetch three upstream services "concurrently," but under load it's no faster than the sync version and latency is terrible. Two smells: (a) inside the handler they call a normal blocking client / `time.sleep` / sync DB driver directly; (b) they `await` the three calls one after another instead of gathering them. Diagnose what each does to the event loop and how you'd confirm it.

**What a strong answer demonstrates:**
- A **blocking call inside a coroutine stalls the entire event loop** — one bad `requests.get`/`time.sleep`/sync-ORM call and every concurrent request on that worker waits. Fix: an async client or offloading to a thread/process pool.
- `await a; await b; await c` is sequential; true concurrency needs gathering the awaitables so they're in flight together.
- Confirm the diagnosis: timing/profiling, checking whether the hot-path libraries are async-native, load-testing.
- Connects to Q15.3: async only helps I/O-bound work, and only if nothing in the path blocks.
- Communication: explains "event loop" plainly (one cook juggling many pots; stand still stirring one and every other pot waits).

---

### 15.9 Cache design for a read-heavy endpoint [Senior] — Coding-style

**Problem:** An endpoint returns an expensive computed summary (multiple joins + aggregation), read thousands of times per minute, written rarely. Design a caching strategy: what you cache, where, invalidation, TTL, and cache-miss behavior under high concurrency.

**Acceptance criteria:**
- Names the cache key design and what layer the cache lives at (in-process vs shared/Redis) with the trade-off.
- Explicit invalidation story (not just TTL).
- Addresses the thundering-herd / cache-stampede problem on expiry.
- States the staleness tolerance and how the design honors it.

**What a strong answer demonstrates:**
- Treats **invalidation as the center** of the problem, not an afterthought. Write-through vs event-based bust vs TTL-only, with trade-offs.
- Distinguishes per-process cache (fast, but N inconsistent copies) from shared cache (consistent, network hop, contention point). (`Rails.cache`/`fetch` block — same model, and Django's cache framework mirrors it.)
- Stampede mitigation: single-flight/locking, jittered TTL, or serve-stale-while-revalidate.
- Ties the design back to the business's staleness tolerance — "cache only works because the data can be N seconds old."
- Knows when *not* to cache: unique-per-request data or hard-freshness requirements.

---

### 15.10 Design a durable pipeline for running untrusted candidate code [Senior+/Staff] — Coding-style

**Problem:** For an eval harness, design the background pipeline that takes a queued submission, runs an untrusted candidate patch's test suite in a container, and records the result. Thousands of submissions; the code may be buggy, malicious, or infinite-looping.

**Acceptance criteria:**
- Isolation and resource-limiting of untrusted execution (timeouts, CPU/memory caps, no network unless allowed).
- Idempotency / exactly-the-work-once semantics under at-least-once queue delivery.
- Poison-message handling, retries with limits, dead-letter routing.
- Observability: how you'd know a run hung, OOM'd, or the worker died mid-job.
- Backpressure / concurrency control so a spike doesn't melt the workers.

**What a strong answer demonstrates:**
- Treats "untrusted code" as a *security* problem: container isolation, hard timeouts, resource cgroups, network egress control (ties to [LLM-eval Q7](#14-llm-tooling-evaluation--agents) and [Security Q2](#11-security-untrusted-input--code-execution)).
- Queue-reliability literacy: at-least-once delivery means jobs *will* run twice — the design must be idempotent (dedupe by submission ID, upsert result-writes). The deep version of your Sidekiq experience.
- Failure taxonomy: transient failure (retry with backoff + cap) vs deterministic failure (candidate code is broken — that's a *result*, not an error) vs poison message (dead-letter it). Conflating "the candidate's tests failed" with "our job errored" is the classic mistake.
- Observability: heartbeats, timeouts that reclaim orphaned jobs, structured logs/metrics per run.
- This is the SWE-bench-in-miniature deliverable — a strong answer sounds like someone who has thought about *running other people's code safely*.

---

### 15.11 Architectural trade-off: when do you split the monolith? [Senior+/Staff] — Conceptual

A client's Python monolith is getting hard to work in and someone proposes breaking it into services. As the senior in the room, how do you reason about whether that's right — and what would make you argue *against* it?

**Talking points:**
- Default skepticism: distributed systems trade in-process function calls (reliable, fast, transactional) for network calls (unreliable, slow, eventually-consistent). You're buying operational complexity — do it only for a reason that outweighs that.
- Good reasons: independent scaling of one hot component, team/ownership boundaries (Conway's Law), independent deploy cadence, isolation of a risky/untrusted workload (Q15.10). Bad reasons: "monoliths are bad," resume-driven development.
- Modular monolith first: enforce module boundaries *inside* the process (clear interfaces, no cross-module DB reach-through) — most of the decoupling, none of the network tax, and it's reversible. (The "engines / bounded contexts before microservices" argument transfers wholesale.)
- The data question dominates: shared database vs per-service data, and what breaks when a once-atomic transaction now spans two services.
- Contractor lens: a 6-month contractor proposing a 2-year microservices migration is usually wrong — recommend what the *team that stays* can own and operate.
- Prefer decisions cheap to undo.

---

### 15.12 Estimating and scoping under uncertainty [Senior] — Conceptual

A client asks, "How long to add feature X?" in a codebase you've had two weeks. You genuinely don't know. How do you produce an estimate that's honest, useful, and doesn't set you up to fail?

**Talking points:**
- Estimate ranges and confidence, not single numbers: "2–4 days if the data model supports it; 1–2 weeks if it needs a migration and touches auth." Name the assumptions that move the number.
- Decompose before estimating — an estimate for an undecomposed task is a guess. The unknowns concentrate in a few pieces.
- Timeboxed spike for the biggest unknown: "give me a day to prototype the risky part, then I can give a real estimate." Converts uncertainty into information.
- Separate the *engineering* estimate from *padding for unknown-unknowns* and say which is which.
- Communicate what would change the estimate and commit to updating it — an estimate is a forecast, not a contract.
- Contractor lens: your estimate is a trust and scoping instrument; over-promising to win the work backfires. Under-promise on certainty, over-communicate on progress.

---

### 15.13 Explain a hard technical decision to a non-technical stakeholder [Senior] — Conceptual

These roles explicitly grade your English communication. Take one real decision — "run candidate code in isolated containers with hard timeouts," or "we need a queue here, not a bigger server" — and explain *why* to a non-technical client in under a minute, no jargon.

**Talking points (what graders look for):**
- Leads with the *why/impact* in their terms (cost, risk, UX, deadline), not the mechanism. "If we don't isolate this, one bad submission can take the whole service down — a customer-facing outage."
- One concrete analogy, not a lecture. (Queue = a ticketing line so a rush doesn't trample the counter; isolation = running each stranger's code in its own sealed room.)
- States the trade-off honestly, including the cost of the recommended path — reads as judgment, not salesmanship.
- Checks for understanding and invites the decision — stakeholders own the call, you own the recommendation.
- Structure: point → reason → trade-off → recommendation.
- Meta: this is half your evaluation for LLM-trainer / eval roles — practice saying your reasoning out loud, tightly, in plain English.

---

### 15.14 Reduce this API's chattiness — an interface-design problem [Senior] — Coding-style

**Problem:** A client team complains that rendering one screen requires 12 sequential calls to your API and it's slow over mobile networks. You own the API. Without just "adding a cache," redesign the interface to fix the round-trip problem. Describe options and your recommendation with trade-offs.

**Acceptance criteria:**
- At least two distinct interface-level approaches (not just caching or a bigger server).
- Explicit trade-offs: coupling, over-fetching, cacheability, versioning, complexity.
- A clear recommendation tied to *this* scenario (mobile, chatty, one screen).

**What a strong answer demonstrates:**
- Recognizes this as an N+1 problem at the *API* layer — the same instinct you use for `includes`/`select_related`, applied to network round-trips.
- Weighs options: a purpose-built aggregate/composite endpoint (BFF pattern), embedding related resources / `?expand=`, batch endpoints, or GraphQL — and each one's cost (aggregate endpoints couple to the client; GraphQL adds server complexity and caching pain).
- Distinguishes over-fetching (one fat call wasting bytes) from under-fetching (many small calls wasting round-trips) and picks the right failure for a mobile client.
- Recommends the smallest change that solves *this* problem, not the heavyweight solution reflexively.

---

### 15.15 The contractor's first two weeks and clean exit [Senior] — Conceptual

As a contractor, your value is judged on ramp-up speed and on what you leave behind. Describe how you'd structure your first two weeks on a new Python client engagement, and how you make sure the team isn't stranded when your contract ends.

**Talking points:**
- Week one reduces your own uncertainty: get the app running locally + tests green (Q15.2), read the data model, ship one tiny real change to exercise the whole pipeline (build → review → CI → deploy) and learn the team's actual process.
- Find the humans and the tribal knowledge fast — who owns what, what's fragile, what's the deploy story — because the codebase never documents the politics.
- Deliver value early and visibly; a small merged PR in week one buys trust for the bigger work.
- Leave-behind discipline: documented, tested code *not* dependent on you being reachable. No clever code only you understand.
- Explicit handoff: docs/READMEs, a short "here's the state, here's what I'd do next, here's the landmines" note, and pairing/knowledge-transfer before you roll off.
- Mindset: optimize for the team's long-run health over your own indispensability — counterintuitively, that's what gets contractors re-hired and referred.

---

### 15.16 The GIL and "parallel" threads [Senior+/Staff] — Conceptual gotcha

A developer runs a CPU-bound function (no I/O) across 8 threads on an 8-core machine expecting ~8x speedup. They measure roughly *no* speedup — sometimes slightly slower. Explain why, and what you'd actually reach for.

**What a strong answer demonstrates:**
- Names the **GIL**: CPython lets only one thread execute Python bytecode at a time, so threads don't parallelize CPU-bound work — they time-slice on one core, and thread-switching overhead can make it *slower*.
- Right tools: `multiprocessing` / a process pool (real parallelism, pay serialization + memory), or push the hot loop into a native/vectorized library (NumPy, C extension) that releases the GIL, or a queue of worker processes.
- The flip side: threads *are* fine for I/O-bound work, because the GIL is released while waiting on I/O — connecting back to Q15.3/Q15.8.
- Rails contrast: MRI Ruby has the same constraint (the GVL), so it should feel familiar — saying so signals real understanding, not memorized trivia.
- Awareness that this is version-sensitive (free-threaded / no-GIL CPython) earns staff-level credit — but the default mental model for production today is "GIL is there."

---

*End of bank. For a full study cycle, work one theme per session, do the gotchas cold first, then narrate a conceptual answer and two coding-prompt designs out loud before revealing the keys.*
