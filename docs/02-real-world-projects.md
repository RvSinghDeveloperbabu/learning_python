# Real-World Projects — Building an LLM Evaluation & Agent Platform (Rails → Python, Senior Portfolio)

A single, coherent product built in six standalone pieces. Each project is independently completable and resume-worthy on its own, but they share one domain (orgs, projects, eval suites, test cases, model/provider configs, runs, results, metrics, patches, sandboxes) and one versioned wire contract, so the portfolio reads as *one platform a company would actually run*, not six disconnected demos. Every line of code is written by you; these specs describe architecture, data models, and algorithms in plain English only.

---

## How to read this document

- **Six projects, each with the full 12-section spec.** MVP (must-build) vs STRETCH (senior bonus) is marked in every project so you can ship even when time is tight.
- **The schedule is honest (see below): this is a 10-week plan, not 8.** Two items are pre-designated "cut if behind" swing items so the portfolio still lands if you overrun.
- **All acceptance criteria are self-verifiable** by you (behavior, tests pass, `mypy` clean, endpoints return X, edge case Y handled) — no dependency on anyone writing code for you.

---

## The platform, and how it maps to your target roles

You are building the components of a realistic **LLM Evaluation & Agent Platform** — the same class of system your target employers build:

- **evalctl** — the pure-Python data layer: validate and report on eval datasets and run logs.
- **Flask ingestion gateway** — the always-on front door where distributed runners POST results.
- **Django platform core** — the multi-tenant system of record: who evaluates what, and every run's results.
- **FastAPI LLM gateway** — the async door to expensive provider APIs, with fan-out, cost, and resilience.
- **agent-cli** — a provider-agnostic function-calling agent that *acts* on repos under guardrails.
- **eval-harness** — a SWE-bench-in-miniature harness that objectively proves whether a patch fixes a repo.

| Target role | Primary projects | What it proves |
|---|---|---|
| **LLM Trainer — Agent Function Call** | agent-cli (P5), FastAPI gateway (P4) | You built the tool-use loop by hand across two providers, with correct message-history reconstruction and stop-condition control. |
| **Senior Python Developer** | Django core (P3), FastAPI (P4), evalctl (P1) | Typed (`mypy --strict`), ORM performance under load, async correctness, contract-first APIs, tests + CI + Docker. |
| **LLM Evaluation & Repository Validation** | eval-harness (P6), agent-cli trace (P5), evalctl (P1) | You compute the exact metrics eval teams live by and objectively grade patches in a hermetic sandbox with a rigorous result-vs-error taxonomy. |

**Non-negotiable priority order** if you must cut: P6 and P5 are the two you cannot skip; P1 is the cheap foundation everything else consumes; the web-framework slots (P2/P3/P4) are where you buy back time.

---

## The honest schedule (10 weeks, with swing items)

The original week labels over-allocated the budget by roughly 40% (they consumed weeks 1–8 with *zero* weeks for Flask, and several projects' own day-estimates exceeded their one-week labels). Committing to a realistic schedule up front is itself a senior signal:

| Weeks | Project | Notes |
|---|---|---|
| 1–2 | **P1 — evalctl** | Cheap foundation. Also produces the shared contract (below). |
| 3 | **P2 — Flask ingestion** | **SWING ITEM #1.** Tight 3–4 day core. If behind, drop it and fold its HMAC + idempotency signals into P4's stretch webhook endpoint. |
| 4–5 | **P3 — Django core** | Deepest ORM signal; genuinely a 2.5–3 week project. |
| 6 | **P4 — FastAPI gateway** | **SWING ITEM #2 lives here:** the OpenAI adapter is stretch; MVP ships Anthropic + a fake adapter. |
| 7–8 | **P5 — agent-cli** | Differentiator. `apply_patch` is the internal cut line. |
| 9–10 | **P6 — eval-harness** | Flagship / centerpiece. |

**Alternative (recommended if time is genuinely tight):** cut to five pillars — P1, P3, P5, P6, plus **one** service slot (FastAPI wins: async is the newest muscle and most on-theme). Drop standalone Flask and fold its crown-jewel signals (HMAC-over-raw-bytes verification + the idempotency decision matrix) into P4 as a stretch webhook endpoint. That reclaims 5–8 days and removes the redundant third web framework. This document keeps all six so you have the option, but treat Flask as the first thing to cut.

---

## Shared versioned data contract (`contracts/`) — build this in P1

Do **not** re-model the domain independently in each repo. In **P1 (evalctl)**, define one canonical JSON schema for `test-case`, `run`, and `result`, each carrying an explicit **`schema_version`**, and publish it as a tiny standalone `contracts/` artifact (JSON Schema files plus a short human-readable changelog).

- **P2 (Flask)** validates inbound webhook payloads against this shape and persists it.
- **P3 (Django)** models its `EvalSuite`/`TestCase`/`Run`/`Result` to serialize to/from this shape.
- **P4 (FastAPI)** accepts eval-run submissions and emits result items in this shape.
- **P6 (eval-harness)** emits its `report.json` conforming to the `run`/`result` portion.

This turns "six demos that rhyme" into "one platform with a versioned wire contract," makes the "independently completable but coherent" claim literally true, and gives you a real **schema-evolution across services** story — exactly the senior narrative reviewers reward. Bump `schema_version` when a field changes and document the migration.

---

## Shared provider-abstraction learning (P4 ↔ P5)

P4 and P5 both normalize Anthropic + OpenAI, so **split the responsibility deliberately instead of building the adapter layer twice:**

- **P4 owns throughput/cost/fan-out** (bounded concurrency, retries, cost accounting).
- **P5 owns the tool-use loop** (message-history reconstruction, tool schemas, stop conditions).
- The **normalized message/response model is shared learning** — ideally the same small internal package consumed by both. Build it once in whichever you tackle first (P4, chronologically) and reuse it in P5.

Likewise, **P5's `run_tests` sandbox and P6's Docker sandbox are different isolation models** (in-process subprocess jail vs. a full hermetic container). Flag them as *reuse of instinct, not code* — don't rebuild P6's container lifecycle inside P5.

---

## Platform secrets model (applies to every project)

One posture across the whole platform, stated once so it's consistent:

- **Everything sensitive comes from the environment** (12-factor): DB URLs, provider API keys, HMAC secrets, `SECRET_KEY`. A committed `.env.example` documents required vars; the real `.env` is gitignored; nothing sensitive is ever baked into a Docker image.
- **Store references, not raw secrets, in the database** (e.g. Django `ProviderCredential`, FastAPI `ProviderCredential`): a pointer to an env var / secret manager, never the key value in a column in prod.
- **Never store the raw key you issue** — API keys are stored hashed (P4), a display `prefix` kept for humans.
- **Redaction at the logging boundary** (P5 trace, P2/P4 structured logs): API keys, HMAC secrets, and full signatures are never logged; log correlation/delivery IDs instead — and add a test that greps the output for the secret and asserts zero matches.

---

## Three corrected headline claims

Reviewers probe headline claims first; these three were false or soft in the draft and are corrected in the specs below:

1. **evalctl "constant memory over multi-GB logs"** — true for counts/sums/pass-rate/cost, but exact p50/p95 require holding the latency sample per group (O(sample) memory). The claim is corrected, and a streaming-quantile option is offered as stretch to make the strong version hold.
2. **FastAPI "batch submit returns <100 ms regardless of batch size"** — false for large batches, because N item rows are inserted before returning 202. Corrected to "returns fast for typical batches via **bulk insert**; the *fan-out* (not the persist) is backgrounded."
3. **eval-harness "same verdict on a stranger's machine"** — pinning the base image digest is not enough if OSS repos resolve transitive deps differently over time. Corrected: each task **vendors a lockfile** (or the harness snapshots the resolved dependency set into the report).

---

## Table of contents

1. [Project 1 — `evalctl`: Typed, streaming CLI for eval data (Weeks 1–2)](#project-1--evalctl-typed-streaming-cli-for-eval-data-weeks-12)
2. [Project 2 — Flask Eval Results Ingestion & Webhook Service (Week 3, swing)](#project-2--flask-eval-results-ingestion--webhook-service-week-3-swing)
3. [Project 3 — Django Eval Platform Core Backend (Weeks 4–5)](#project-3--django-eval-platform-core-backend-weeks-45)
4. [Project 4 — FastAPI Async Eval Runner / LLM Gateway (Week 6)](#project-4--fastapi-async-eval-runner--llm-gateway-week-6)
5. [Project 5 — `agent-cli`: Provider-Agnostic Function-Calling Agent (Weeks 7–8)](#project-5--agent-cli-provider-agnostic-function-calling-agent-weeks-78)
6. [Project 6 — `eval-harness`: Mini SWE-bench-Style Evaluation Harness (Weeks 9–10, flagship)](#project-6--eval-harness-mini-swe-bench-style-evaluation-harness-weeks-910-flagship)

---

# Project 1 — `evalctl`: Typed, streaming CLI for eval data (Weeks 1–2)

*Folder: `foundations/` (installs as `evalctl`)*

A production-grade, typed CLI for validating and reporting on LLM evaluation datasets and run logs. This is your "think in Python" project: no web framework, no ORM — just clean, typed, well-tested Python a data/ML team would actually keep in their toolbox. **It also produces the shared `contracts/` schema the rest of the platform consumes.**

### 1. Premise

Every team that evaluates LLMs produces two streams of JSONL: **eval datasets** (test cases — prompt, expected answer, tags, metadata) and **run logs** (what a model actually produced per case — output, pass/fail, latency, token counts, cost, provider). These files are large, messy, and generated by many different scripts, so they drift out of schema constantly. `evalctl` is the tool an ML/eval engineer runs to *trust their data before they trust their metrics*: it validates both file types against a strict schema, joins runs back to their dataset cases, filters and slices, and computes the headline numbers a team reports — pass rate, latency p50/p95, total and per-case cost — then exports both a human-readable table and a machine-readable JSON report for CI. The users are ML engineers, eval/QA engineers, and the CI pipeline itself (which calls `evalctl` and fails the build if pass rate drops below a threshold).

### 2. Why it's senior-level

- **Streaming, not slurping.** Real run logs are hundreds of MB to multiple GB. `json.load` into a list will OOM. You process lazily with generators, holding roughly constant memory for counts/sums — and you must be able to *prove* it. (See the honest memory story in §4.)
- **Schema validation on untrusted input.** Files come from other people's buggy scripts: missing fields, wrong types, NaN latencies, negative costs, duplicate IDs, truncated last lines, mixed encodings, BOMs. A senior tool reports *which line failed and why* and keeps going (or fails fast) per an explicit policy — never a raw traceback.
- **Correct statistics.** p50/p95 are easy to get subtly wrong (interpolation method, empty/singleton sets, off-by-one on percentile rank). Cost/pass-rate must handle divide-by-zero and partial data.
- **A real typed surface.** `mypy --strict` clean across the package — no `Any` leaks, no untyped dicts. This forces domain modeling with dataclasses instead of dictionaries — the single biggest habit shift from dynamic Ruby.
- **Deterministic, exit-code-aware CLI.** Stable output, meaningful exit codes, `--format json` for machines, graceful broken-pipe handling (`evalctl … | head`).
- **A test suite that pins behavior** — golden-file report tests, parametrized edge cases, and a large-file performance test.

### 3. Feature set

> **Scope trim (applied):** the MVP was tightened. `--group-by`, CSV export, and `--since/--until` moved to late-MVP/stretch. Ship **validate + stats + join + json/table + threshold gate** first.

**MVP (must-build)**

- **The `contracts/` schema.** Define the canonical `test-case`, `run`, and `result` JSON shapes with `schema_version`; the rest of the platform consumes these. This is a first-class deliverable, not an afterthought.
- `evalctl validate <file> --kind dataset|run` — stream-validate a JSONL file against the schema; report a summary (N valid, N invalid) and a per-error list (`line 4213: field 'latency_ms' expected number, got null`). Exit non-zero if any record is invalid (unless `--lenient`).
- `evalctl stats <run-file>` — compute and print headline metrics: total records, pass rate, latency p50/p95 (+ mean/min/max), total cost, cost per case, error count. Respects filters.
- **Filtering flags** shared across commands: `--tag`, `--model`, `--provider`, `--status pass|fail|error` — composable (AND semantics).
- **Join / enrich:** `evalctl report --dataset cases.jsonl --run runs.jsonl` — join each run to its dataset case by `case_id`, report unmatched runs (orphans) and un-run cases (coverage gaps).
- **Dual export:** `--format table` (aligned human report) and `--format json` (stable, machine-readable, `schema_version`-stamped). `--output <path>` writes via `pathlib`.
- **Threshold gate:** `--fail-under-pass-rate 0.9` / `--fail-over-p95 2000` so CI can enforce SLAs via exit code.
- Streaming ingestion via generators; robust per-line error handling; meaningful exit codes; `--verbose`/`--quiet`.
- Full `mypy --strict` compliance and a pytest suite.

**STRETCH (senior bonus)**

- **`--since`/`--until`** timestamp filters (timezone-aware, normalized to UTC).
- **Grouped aggregation** `--group-by tag|model|provider` (per-group pass rate + p95 + cost).
- **CSV export** — scoped to the **flat per-record or per-group table only** (CSV cannot represent the nested `Report`; do not claim "dual export" over the nested schema).
- **`evalctl diff --baseline old.jsonl --candidate new.jsonl`** — regression report: cases that flipped pass→fail, pass-rate/p95/cost deltas. The money feature for an eval platform.
- **Streaming quantiles** (P²/t-digest/reservoir) so the "constant memory" claim holds even for percentiles.
- **Config file** (`evalctl.toml`) merged with CLI (CLI wins); **`--sample N --seed 42`**; **`--percentiles 50,90,95,99`**; **progress/throughput to stderr**; **gzip transparency** (`.jsonl.gz`); **plugin custom metric**; **`--strict-cost`** reconciliation against a shipped price table.

### 4. Architecture & data model

Layered so the core logic is pure and testable, and I/O + CLI live at the edges.

```
          argv
           |
   +----------------+        CLI layer (Typer): parse args, wire
   |  cli / commands |        filters, choose formatter, set exit code
   +----------------+
           |
   +----------------+        Ingest: pathlib open (+gzip), stream
   |  io / ingest    | -----> lines -> parse JSON -> validate ->
   +----------------+        yield Record | ValidationError  (generator)
           |
   +----------------+        Core (pure, no I/O):
   |  model + metrics|   - dataclasses: DatasetCase, RunRecord, Report
   |  + filters      |   - filters (predicates), join, aggregation
   +----------------+   - metrics: pass_rate, percentile, cost
           |
   +----------------+        Render: table / json formatters
   |  report / render|        + threshold gate -> exit code
   +----------------+
           |
        stdout / file
```

**Entities (dataclasses, frozen where possible):**

- **DatasetCase**: `case_id`, `prompt`, `expected: str | None`, `tags: tuple[str, ...]`, `metadata: Mapping[str, JsonValue]`. Immutable. Mirrors the `test-case` contract shape.
- **RunRecord**: `case_id`, `run_id`, `model`, `provider`, `status` (Enum PASS/FAIL/ERROR), `output: str | None`, `latency_ms: float`, `prompt_tokens: int`, `completion_tokens: int`, `cost_usd: float`, `timestamp: datetime`, `error: str | None`. Mirrors the `result` contract shape.
- **ValidationError**: `line_number`, `field: str | None`, `message`, `raw` (truncated). Carries *where* and *why*; never raised as a bare exception across the streaming boundary.
- **Report**: `total`, `valid`, `invalid`, `pass_rate`, `latency` (a `LatencyStats` sub-dataclass p50/p95/mean/min/max), `total_cost`, `cost_per_case`, `groups`, `coverage` (matched/orphans/gaps), `schema_version`.

**Relationships & key flows:**

- One DatasetCase ↔ many RunRecords, joined on `case_id`. `report` materializes the *dataset* index (datasets are small) and streams the *runs* against it, keeping the big file lazy.
- **Validation flow:** open → iterate lines with a 1-based index → parse JSON → coerce/validate into the dataclass → yield a typed record or a `ValidationError`. Callers pick policy (fail-fast vs. collect-and-continue).
- **Metrics flow:** filtered stream of `RunRecord` → single pass accumulates counts, cost sum. **Percentiles need the full sample**, so the latency list is held **only when percentiles are requested** — this is the one bounded, per-group O(sample) memory cost.

> **Corrected headline claim (memory).** Advertise: *"Constant memory for counts, sums, pass-rate, and cost regardless of file size; exact percentiles are the one bounded O(sample-per-group) cost, documented — with a streaming-quantile mode (stretch) that makes even percentiles constant-memory."* Do **not** claim uniform constant memory while shipping exact percentiles.

**Type aliases:** define `JsonValue` (recursive union) and `Status` once; thread real types everywhere so `mypy --strict` has no untyped-dict escape hatch.

### 5. Tech & libraries

- **Python 3.12+** — modern typing (`X | Y`, `type` aliases, `Self`).
- **uv** — dependency + venv manager; your `pyproject.toml` home. Industry-standard replacement for pip/poetry workflows.
- **Typer** (on Click) — declarative, type-hint-driven CLI; derives the parser from typed signatures, reinforcing the type-first habit. (Know `argparse` conceptually; explain the choice in the README.)
- **dataclasses** (stdlib) — `frozen=True`, `slots=True` on the hot record type.
- **pathlib, json, gzip, csv, enum, datetime, statistics** (stdlib) — `statistics.quantiles` is your reference to test your own percentile against.
- **collections** (`Counter`, `defaultdict`) + **itertools** (`islice`, `groupby` on *sorted* data, `chain`).
- **mypy `--strict`** — the point of the project.
- **ruff** — lint + format.
- **pytest** + **pytest-cov**; **hypothesis** (stretch) for property-testing the percentile function.
- **rich** (optional) — pretty tables; keep `--format json` plain and pipe-safe.
- **Pydantic is intentionally NOT used here.** You meet it in P4. Hand-rolling validation over dataclasses is the learning goal — it teaches you what a schema layer *does* before a library hides it.

### 6. Milestone breakdown

~10–12 working days at 3–4 hrs/day. Each milestone is a shippable increment with its own tests.

- **M1 — Skeleton & tooling (Day 1).** `uv init`, package layout (`src/evalctl/`), ruff + mypy-strict config, pytest wired, `evalctl --version`, CI-ready scripts. First green commit.
- **M2 — Domain model + `contracts/` (Days 1–2).** `Status` enum, `JsonValue`, all dataclasses, and the published JSON Schema files with `schema_version`. Types that `mypy --strict` accepts; a couple of construction tests.
- **M3 — Streaming ingest + JSON parse (Days 2–3).** `pathlib` reader yielding `(line_number, raw_line)`; generator parsing each line. Handle blank lines, trailing newline, UTF-8/BOM, truncated final line. Prove laziness via `islice` on an infinite source.
- **M4 — Schema validation (Days 3–4).** Field-by-field coercion into dataclasses; precise `ValidationError`. Fail-fast vs. collect policy. `validate` command end-to-end with non-zero exit on invalid.
- **M5 — Metrics core (Days 4–5).** Pure `pass_rate`, `percentile` (documented method, correct on empty/singleton), `LatencyStats.from_samples`, cost aggregation. Cross-check percentile against `statistics.quantiles`. `stats` command prints headline numbers.
- **M6 — Filters + join (Days 6–7).** Composable predicate filters (`--tag/--model/--provider/--status`); `report` indexes the dataset and streams runs; coverage report (orphans/gaps).
- **M7 — Formatters, export & gate (Days 7–8).** Aligned table; stable JSON (`schema_version`, key-ordered, deterministic). `--output` via pathlib. Threshold-gate flags → exit codes. Broken-pipe handling for `| head`.
- **M8 — Test hardening & performance (Days 8–9).** Golden-file report tests, parametrized edge cases, a synthetic large-file memory/throughput test, coverage ≥ 85%.
- **M9 — Docs, packaging, polish + STRETCH (Days 10–12).** README with real usage + `--help` transcript, console-script install, Dockerfile, CI (ruff + mypy + pytest). Then 1–2 stretch features (`diff` is highest-value; streaming quantiles makes the memory claim airtight).

### 7. Acceptance criteria (per milestone, all self-verifiable)

- **M1:** `uv run evalctl --version` prints a version; `uv run mypy --strict src` and `uv run ruff check` pass; `uv run pytest` collects and passes ≥1 test.
- **M2:** Constructing a `RunRecord` with a wrong field type is a mypy error (verify by temporarily miswriting one); frozen dataclasses raise `FrozenInstanceError` on mutation (a test asserts it). The published schema files validate a hand-written sample record.
- **M3:** A 3-line file yields 3 parsed items; a truncated final line produces exactly one `ValidationError` at the right line number, not a crash; the reader consumes `islice(infinite_source, 5)` without hanging.
- **M4:** `validate` on a clean file exits 0 ("N valid, 0 invalid"); on a file with a `null` latency, exits non-zero and prints `line X: latency_ms …`; `--lenient` exits 0 while still listing errors on stderr. Every error carries a line number.
- **M5:** On a hand-computed latency sample, p50/p95 match by-hand values and `statistics.quantiles`; `pass_rate` of an all-error set is 0.0 with no `ZeroDivisionError`; empty input yields a well-defined report (zeros/N-A), not an exception.
- **M6:** `--tag foo --model gpt-x` returns only records matching both; a run with an unknown `case_id` appears in orphans; a case with no runs appears in coverage gaps; join totals equal the ungrouped totals.
- **M7:** `--format json` output is byte-stable across two runs on the same input and parses back to the same report; piping table output to `head -5` doesn't raise `BrokenPipeError`; `--fail-under-pass-rate 0.99` exits non-zero when the real rate is lower; `--output out.json` creates the file.
- **M8:** `pytest` green with coverage ≥ 85%; golden report tests fail loudly on format change; a ~1M-line synthetic file processes with roughly constant memory (measured via `tracemalloc`/`resource`) and hits a throughput you record in the README.
- **M9:** `uv build` produces a wheel; `evalctl` runs as an installed console script; `docker run` executes it against a mounted file; CI green on a fresh clone.

### 8. Testing strategy

- **Fixtures (`conftest.py`):** small canonical `dataset.jsonl` / `run.jsonl` as `tmp_path` files; a "dirty" fixture with one of each error class (bad type, missing field, dup id, truncated line, empty line, BOM). A factory helper building `RunRecord`/`DatasetCase` with overridable defaults (mirrors FactoryBot).
- **Parametrize aggressively:** one test over a table of `(input line, expected ValidationError field/message)`; percentile tests over `(samples, percentile, expected)`.
- **Golden-file tests:** `report --format json` vs. a committed expected JSON; a `--update-goldens` flag to regenerate intentionally.
- **Property-based (stretch, hypothesis):** percentile within `[min, max]`; p50 ≤ p95; sort invariance.
- **Streaming/memory test:** a lazily-yielding synthetic source; assert the pipeline handles more records than could fit if materialized, and peak memory doesn't scale with record count.
- **CLI integration:** Typer's `CliRunner` — assert exit codes, machine-format stdout, errors on stderr, threshold-gate exit codes.
- **Don't test** Typer/json/stdlib themselves.

### 9. Deployment / ops

- **Local:** `uv sync` then `uv run evalctl …`; a `justfile`/`Makefile` with `lint`, `typecheck`, `test`, `check` targets so `make check` is the one command CI and you both run.
- **Packaging:** console-script entry point; `uv build`; document `uvx evalctl` / `pipx install`.
- **Docker:** small multi-stage image, non-root, `ENTRYPOINT ["evalctl"]`, `docker run --rm -v $PWD:/data evalctl stats /data/run.jsonl`.
- **Config/secrets:** none sensitive; `evalctl.toml` (stretch) holds defaults only. Precedence: CLI flag > env var > config file > default.
- **No migrations** (no DB) — note in the README that this is deliberately stateless and stream-oriented.
- **CI (GitHub Actions):** matrix on 3.12/3.13; `ruff check`, `mypy --strict`, `pytest --cov` with a coverage floor; build wheel and Docker image on tags.

### 10. Ruby/Rails bridge

- **dataclasses + `frozen=True` ≈ immutable value objects / `Struct` / `Data.define`.** `mypy --strict` is the compiler you never had — treat its errors like Sorbet/`# typed: strict`.
- **Generators (`yield`) ≈ Ruby `Enumerator` / `.lazy`.** Streaming JSONL line-by-line ≈ `File.foreach(path)` returning an Enumerator instead of `File.read.split("\n")`.
- **pytest fixtures + parametrize ≈ RSpec `let`/`before` + shared examples.** `conftest.py` ≈ `spec_helper.rb`; `CliRunner` ≈ an RSpec integration spec.
- **Typer subcommands + exit codes ≈ a Thor/Rake CLI** with `exit(1)` on failure.

### 11. Senior signals & portfolio angle

- **The artifact that says "I write real Python, not translated Ruby."** README lead: *"A streaming, strictly-typed CLI for LLM eval data — `mypy --strict` clean, constant-memory over multi-GB logs for counts/costs, CI-gate ready."*
- **Directly on-narrative for LLM Evaluation and LLM Trainer roles:** you compute exactly the metrics those teams live by and validate exactly the artifacts they generate. "I built the ingestion/validation/metrics layer of an eval harness" — true and standalone.
- **Highlight:** the streaming architecture with the memory-flat benchmark number, the strict-typing story, per-line actionable errors, the exit-code/CI-gate design, and golden-file testing. Include a real `--help` transcript and a sample JSON report.
- **Show the `diff` feature** if you build it — regression detection is the most "senior eval engineer" capability.
- **Name your tradeoffs** (generators over pandas; hand-rolled validation over Pydantic *here*; the percentile-memory honesty) — the loudest senior signal there is.

### 12. Common pitfalls

- **Materializing the big file.** Any `list(...)`, `json.load`, `.readlines()`, or `sorted()` over the full run stream defeats the project. Sort/group only within bounded data; document where you hold a sample (percentiles).
- **`Any` leaking through JSON.** `json.loads` returns `Any`; convert to dataclasses immediately; forbid `Any` in your own signatures.
- **Percentile bugs.** Decide and document your method; handle empty/single-element inputs; cross-check `statistics.quantiles`. Off-by-one quietly ships wrong SLAs.
- **Printing tracebacks at users.** Turn parse/validation errors into `ValidationError` reports; reserve exceptions for programmer bugs.
- **Mixing machine and human output on stdout.** Keep `--format json` byte-clean; logs/progress to stderr; handle `BrokenPipeError`.
- **Non-deterministic JSON.** Sort keys, round costs to fixed precision, serialize deterministically, or golden tests flap.
- **`groupby` on unsorted data** (stretch) — sort by the group key first or use `defaultdict`.
- **Timezone-naive timestamps** (stretch `--since/--until`) — parse to timezone-aware, normalize to UTC on ingest.
- **Over-engineering the plugin/config stretch** before the MVP is rock-solid.

---

# Project 2 — Flask Eval Results Ingestion & Webhook Service (Week 3, swing)

*Folder: `flask-app/`*

> **SWING ITEM #1.** This is the first thing to cut if you fall behind. If you drop it, fold its two crown-jewel signals — **HMAC-over-raw-bytes verification** and the **idempotency decision matrix** — into P4's stretch webhook endpoint. If you keep it, budget honestly (see below).

A production-shaped Flask microservice: the "front door" where distributed eval runners POST their results. It authenticates callers, verifies payload integrity, deduplicates retries, persists to Postgres, offloads heavy work to a durable outbox worker, and exposes a small JSON API plus a read-only dashboard.

### 1. Premise

In an LLM eval platform the compute-heavy work happens on ephemeral **runners** — CI jobs, GPU workers, spot instances that spin up, do work, and die. They need a durable, always-on endpoint to report results to. This service is that endpoint: an **ingestion gateway** receiving `run.started` / `case.completed` / `run.finished` webhook events from many untrusted runners, proving each event is authentic and un-tampered, storing the canonical record of every run, and letting the platform team query run status over a JSON API and a lightweight ops dashboard. Same class of service as GitHub's webhook receivers or Stripe's event ingest — small surface, high correctness bar. **Payloads conform to the shared `contracts/` schema from P1.**

Consumers: (a) **runners** (machine clients, authenticated by API key + HMAC), (b) **platform engineers** browsing the dashboard, (c) **downstream services** polling the JSON API.

### 2. Why it's senior-level

A deliberately *narrow* service, which is exactly why senior concerns have nowhere to hide:

- **Untrusted input over the network.** Authenticate (API key), verify integrity (HMAC over the raw body), reject replay (timestamp window + idempotency key). Getting HMAC *actually correct* — raw bytes, constant-time compare, signature covers the timestamp — is a classic senior/junior divider.
- **Exactly-once over an at-least-once transport.** Webhook senders retry; naive persistence double-counts. A retried delivery must be a no-op that returns the original response.
- **Sync boundary vs. async work — done durably.** The HTTP handler returns `202 Accepted` quickly; validation-then-scoring-then-aggregation happens off the request path in a **durable outbox worker** (see the fix in §3), which survives restarts.
- **Concurrency correctness.** Two runners (or two retries) hitting the same run simultaneously → DB-level uniqueness constraints and transaction thinking, not app-level "check then insert" (which races).
- **Schema evolution.** Version the payload schema (via the shared contract) and run migrations.
- **Observability & ops.** Structured logs with a delivery id, health checks, graceful config/secrets.
- **Explicit framework tradeoff.** Choosing Flask (assemble-your-own) over Django and defending it is itself a senior signal.

### 3. Feature set

> **Worker fix (applied):** the MVP worker is a **DB-outbox table drained by a separate `flask process-deliveries` command** using a poll loop with `SELECT … FOR UPDATE SKIP LOCKED` — **not** a `ThreadPoolExecutor`. A thread pool inside a gunicorn worker loses jobs on restart and re-creates the "enqueue-before-commit" footgun this project warns about, contradicting the durable/exactly-once narrative. The outbox survives restarts, demonstrates the pattern you're expected to know, and makes RQ a genuine stretch rather than a rewrite.

> **Scope fix (applied):** MVP is realistically **5–6 days**, not 2.5–3, for someone new to SQLAlchemy 2.0 and Alembic. If time-boxed, cut the dashboard to **one read-only list route, smoke-tested — no detail page** for MVP.

**MVP (must-build):**

- **App-factory + blueprints:** `create_app(config)`; routes split into `ingest`, `api`, and `dashboard` blueprints.
- **Webhook ingest** `POST /v1/webhooks/eval` that:
  - authenticates via `X-Api-Key` mapped to a `Client`,
  - verifies `X-Signature` = HMAC-SHA256 over `timestamp + "." + raw_body` with that client's secret,
  - rejects stale requests (timestamp outside ±5 min),
  - enforces **idempotency** via an `Idempotency-Key` header,
  - validates the JSON payload against the shared schema,
  - **writes a `WebhookDelivery` + an outbox row in one transaction**, returns **202** quickly.
- **Payload validation** with typed Pydantic v2 schemas → structured 422 listing field errors.
- **Persistence:** SQLAlchemy 2.0 models + Flask-Migrate/Alembic migrations for `Client`, `Run`, `TestCaseResult`, `WebhookDelivery`, `IdempotencyRecord`, and the **`Outbox`** table.
- **Durable processing:** `flask process-deliveries` drain-worker — poll loop, claim rows with `FOR UPDATE SKIP LOCKED`, do the "expensive" work (validate cross-field invariants, upsert results, recompute run aggregates like pass-rate / mean-score), mark the delivery processed. Handle exceptions (increment attempts, mark failed).
- **JSON query API:** `GET /v1/runs` (paginated, filter by status/suite/client), `GET /v1/runs/<id>` (with aggregates), `GET /v1/runs/<id>/results` (paginated).
- **Minimal dashboard:** one server-rendered read-only list of recent runs with status badges + pass-rate. (Detail page is stretch.)
- **Health/readiness:** `GET /healthz` (liveness), `GET /readyz` (DB connectivity).
- **Structured logging** with a per-request correlation id.
- **Test suite** (pytest) + **mypy clean** on the source package.

**STRETCH (senior bonus):**

- **RQ + Redis** replacing the outbox drain: real durable queue, `rq worker`, retry with exponential backoff, a **dead-letter** flow, `GET /v1/queue/stats`.
- **Dead-letter & replay:** exhausted deliveries land in a DLQ table; a dashboard button / CLI re-enqueues.
- **Dashboard run-detail page.**
- **Rate limiting** per API key (Flask-Limiter) → 429 with `Retry-After`.
- **Prometheus** `/metrics`.
- **HMAC key rotation:** two active secrets (current + previous) verify during a rotation window.
- **Cursor-based pagination.**
- **Outbound webhooks:** fire a signed `run.finished` to a subscriber URL — be both sides of the contract.
- **OpenAPI spec** at `/openapi.json` (your Swagger background).

### 4. Architecture & data model

```
   Runner (untrusted)                Flask ingest (sync, fast)             Outbox drain (durable)
 ┌──────────────────┐   POST /v1/    ┌───────────────────────────┐       ┌────────────────────┐
 │ signs body:      │  webhooks/eval │ 1 auth: X-Api-Key -> Client│ row   │ claim FOR UPDATE   │
 │ HMAC(secret,     │ ─────────────► │ 2 verify HMAC (raw bytes)  │ ────► │   SKIP LOCKED      │
 │  ts + "." + body)│  X-Signature   │ 3 ts freshness window      │outbox │ validate invariants│
 │ Idempotency-Key  │  X-Timestamp   │ 4 idempotency lookup       │       │ upsert results     │
 └──────────────────┘  Idempotency…  │ 5 validate schema          │       │ recompute run agg. │
         ▲                           │ 6 tx: WebhookDelivery+Outbox│      │ mark delivery done │
         │        202 Accepted       │ 7 commit -> return 202     │       └─────────┬──────────┘
         └───────────────────────────┴───────────────────────────┘                 │
                                              │ SQLAlchemy                          │
                                              ▼                                     ▼
                                       ┌──────────────────────  Postgres  ──────────────────────┐
                                       │ Client · Run · TestCaseResult · WebhookDelivery ·        │
                                       │ IdempotencyRecord · Outbox · (DeadLetter)                │
                                       └──────────────────────────────────────────────────────────┘
                                              ▲
                          GET /v1/runs ...    │      Dashboard (Jinja)  GET /  ─── read-only list
                          (api blueprint) ────┘      (dashboard blueprint)
```

**Entities & relationships:**

- **Client** — a runner/tenant: `id`, `name`, `api_key` (unique, indexed), `hmac_secret` (+ optional `hmac_secret_previous` for rotation), `active`, `created_at`. Has many Runs and WebhookDeliveries.
- **Run** — one eval-suite execution: `id`, `external_run_id` (from runner; **unique per client** — the run's idempotency anchor), `client_id`, `suite_name`, `model_name`, `provider`, `status` (`running`/`completed`/`failed`), aggregates `total_cases`/`passed_cases`/`failed_cases`/`mean_score`, `started_at`/`finished_at`. Has many TestCaseResults.
- **TestCaseResult** — one case outcome: `id`, `run_id`, `case_key` (**unique per run** — prevents double-counting on retry), `passed`, `score`, `latency_ms`, `error`, `payload` (JSONB).
- **WebhookDelivery** — the audit ledger of one received HTTP delivery: `id`, `client_id`, `delivery_id`, `event_type`, `raw_body` (or hash), `signature_valid`, `status` (`received`/`processing`/`processed`/`failed`), `attempts`, `error`, `created_at`, `processed_at`.
- **Outbox** — the durable work queue: `id`, `delivery_id` (FK), `status` (`pending`/`claimed`/`done`/`failed`), `attempts`, `claimed_at`, `available_at` (for backoff). Drained by `process-deliveries`.
- **IdempotencyRecord** — `key` (unique, `Idempotency-Key` + client scope), `request_fingerprint` (body hash — detect key reuse with a *different* body), `response_status`, `response_body`, `created_at`, TTL. A repeat with the same key replays the stored response.
- **DeadLetter** (stretch) — deliveries that exhausted retries, with failure reason, for manual replay.

**Key flows:**

1. **Ingest (sync, fast):** raw-body capture → API-key lookup → HMAC verify → timestamp window → idempotency check (short-circuit if seen) → schema validate → **one transaction:** insert `WebhookDelivery` + `IdempotencyRecord` + `Outbox(pending)` → commit → return 202. No scoring here. (Committing the outbox row *inside the same transaction* is what removes the enqueue-before-commit race — there is no separate broker to get ahead of the commit.)
2. **Process (durable drain):** `process-deliveries` claims pending outbox rows with `FOR UPDATE SKIP LOCKED` → **upsert** Run by `(client_id, external_run_id)`; upsert TestCaseResults by `(run_id, case_key)` → recompute Run aggregates → mark delivery `processed` and outbox `done`. On exception: increment attempts, set `available_at` for backoff, or DLQ after N attempts.
3. **Query:** API reads Runs/results with pagination + filters; dashboard renders the list as HTML.

**External integrations:** Postgres (persistence), Redis (RQ — stretch), optional outbound subscriber URL (stretch). No LLM calls — it *ingests* results.

### 5. Tech & libraries

- **Flask** — the micro-framework; you assemble your own stack (the whole point — see §10).
- **app-factory + Blueprints** — testable, modular; app-per-test-config.
- **SQLAlchemy 2.0** (typed `Mapped[...]`) + **Flask-SQLAlchemy**.
- **Flask-Migrate** (Alembic) — migrations; the Rails-migrations analog.
- **Pydantic v2** — payload validation against the shared contract, structured 422s. (Consistent with P4.)
- **stdlib for the worker** — the outbox drain is a Flask CLI command with a poll loop; **RQ + Redis** is the stretch upgrade.
- **Jinja2** — the dashboard list.
- **hmac** + **hashlib** + **`hmac.compare_digest`** — constant-time compare. Using stdlib correctly *is* the signal.
- **pytest** + **pytest-flask** (or `app.test_client()`) + **factory_boy** + **Faker**.
- **mypy** + **ruff**.
- **structlog** (or stdlib `logging` + JSON formatter) — correlation id.
- **python-dotenv** / env config; a `Config` hierarchy (`Dev`/`Test`/`Prod`).
- **Flask-Limiter** (stretch); **prometheus-client** (stretch).
- **gunicorn** — production WSGI.
- **Docker + docker-compose** — app + Postgres (+ Redis stretch).
- **uv** — dependency & venv.

### 6. Milestone breakdown

Sized to ~3–4 hrs/day, **budgeted honestly at 5–6 days for the MVP** (M0–M6). M7–M8 are stretch.

- **M0 — Skeleton & app factory (0.25 day).** `uv` project, `create_app()`, three blueprints registered, `Config` classes, `/healthz`, ruff+mypy, one smoke test.
- **M1 — Data model & migrations (0.75 day).** All SQLAlchemy models incl. the **Outbox** table + the critical unique constraints (`Client.api_key`, `(client_id, external_run_id)`, `(run_id, case_key)`, `IdempotencyRecord.key`). Initial migration; seed a `Client`.
- **M2 — Auth + HMAC + freshness (0.75 day).** Ingest resolves client by API key, verifies HMAC over `timestamp.raw_body` with constant-time compare, enforces ±5-min window. Persist `WebhookDelivery` with `signature_valid`. 202 / 401 / 400.
- **M3 — Validation + idempotency (0.75 day).** Pydantic schemas per event; 422 with field errors. Idempotency: same key + same body → replay stored response; same key + different body → **409 Conflict** (pick one — no waffling); new key → process.
- **M4 — Outbox drain worker (1 day).** Write the outbox row in the ingest transaction; `flask process-deliveries` claims with `FOR UPDATE SKIP LOCKED`, upserts Run + TestCaseResults, recomputes aggregates, marks processed. Handle worker exceptions (mark failed, record error, backoff).
- **M5 — JSON query API (0.75 day).** `GET /v1/runs` (pagination + filters), `/runs/<id>`, `/runs/<id>/results`. Consistent error envelope, 404s, query-param validation.
- **M6 — Dashboard (list only) + logging + docs (0.75 day).** One Jinja run-list with badges/pass-rate. Structured logs with correlation id. README with diagram, setup, Flask-vs-Django writeup. **Shippable MVP.**
- **M7 — RQ/Redis + retries + DLQ (stretch, 0.5–1 day).** Swap the drain for RQ; exponential backoff; dead-letter table + replay; `queue/stats`.
- **M8 — Hardening (stretch, 0.5–1 day).** Flask-Limiter, Prometheus `/metrics`, HMAC key rotation, OpenAPI spec, outbound `run.finished`, dashboard detail page.

### 7. Acceptance criteria (self-verifiable)

- **M0:** `flask run` boots; `/healthz` → 200 JSON; mypy + ruff clean; smoke test green.
- **M1:** `flask db upgrade` creates all tables; a DB shell shows the unique indexes. Inserting two `TestCaseResult`s with the same `(run_id, case_key)` raises `IntegrityError` (prove the constraint, don't rely on app logic).
- **M2:** Correct signature → 202; flip one body byte → 401; reuse a signature with a 10-min-old timestamp → 400. A `WebhookDelivery` row is written in all cases with `signature_valid` correct. Verified via a test that computes HMAC the way the client would. Self-review: no `==` on raw signatures.
- **M3:** Same payload twice with the same `Idempotency-Key` → second returns the *identical* body/status and creates **no** new rows. Same key + mutated body → **409**. Malformed payload → 422 listing offending fields.
- **M4:** After a `run.finished` sequence, `Run.status = completed` and `passed_cases`/`failed_cases`/`mean_score` match posted cases. **Kill the drain worker mid-batch, restart it, and pending outbox rows still process (durability).** A delivery whose processing always raises ends up `failed` with an error recorded; the ingest endpoint returns 202 *before* work completes (verify processing is off the request path).
- **M5:** `GET /v1/runs?status=completed&limit=2` returns ≤2 + a next-page indicator; unknown id → 404 with the standard envelope; bad `limit` (`-1`, `abc`) → 422.
- **M6:** Dashboard list renders correct pass-rates; every log line for a request carries the same correlation id; README explains the Flask/Django tradeoff.
- **M7:** A job that always throws lands in the DLQ after N attempts and can be replayed; `queue/stats` reports depth.
- **M8:** Exceeding the per-key limit → 429 with `Retry-After`; `/metrics` exposes counters; a signature made with the *previous* secret still verifies during rotation.
- **Global:** `pytest` green, `mypy` clean on `src/`, coverage on auth + idempotency + drain paths ≥ ~85%.

### 8. Testing strategy

- **App/config fixtures:** `create_app(TestConfig)` against a transactional test DB; wrap each test in a rolled-back transaction. Run at least one **CI pass against Postgres** (you rely on JSONB, `FOR UPDATE SKIP LOCKED`, and DB constraints — SQLite won't enforce some).
- **Signing helper:** a test helper producing valid `X-Signature`/`X-Timestamp`/`Idempotency-Key` for a body+secret — reused across ingest tests. Independently reimplementing the client side is how you *prove* your server verification.
- **Auth/HMAC unit tests:** valid, tampered body, wrong key, missing headers, expired timestamp, previous-secret (stretch).
- **Idempotency tests:** replay returns stored response with no new rows; key-reuse-with-different-body → 409; **concurrent-duplicate** (fire two identical requests; assert exactly one Run) — exercises the DB unique constraint.
- **Validation tests:** table-driven invalid payloads → 422 with expected field paths.
- **Drain-worker tests:** call the drain function directly against seeded outbox rows; assert aggregate math and the failure/backoff path; assert `SKIP LOCKED` claiming doesn't double-process (two concurrent drains).
- **API tests:** pagination boundaries, filters, 404s, query-param validation.
- **Factories:** `factory_boy` for `Client`/`Run`/`TestCaseResult`; `Faker` for realistic values.
- **Don't over-test** Jinja rendering — one smoke assertion (page 200s and contains a run id).

### 9. Deployment / ops

- **Docker:** multi-stage `Dockerfile` running **gunicorn**; the drain worker started as a separate process/service (`flask process-deliveries`).
- **docker-compose:** `web`, `worker`, `postgres` (+ `redis` stretch); healthchecks; web waits for a healthy DB.
- **Config/secrets:** per the platform secrets model — all config from env (`DATABASE_URL`, `SECRET_KEY`, per-client HMAC secrets seeded via a management command, `REDIS_URL`); `.env.example` committed, `.env` gitignored.
- **Migrations:** `flask db upgrade` as a release/entrypoint step; never `db.create_all()` in prod.
- **Local run:** documented two-line quickstart + a signing script description that posts a signed sample event and shows it on the dashboard.
- **CI:** ruff → mypy → pytest against a Postgres service container.
- **Ops surface:** `/healthz` (liveness) vs `/readyz` (DB reachable); structured JSON logs to stdout.

### 10. Ruby/Rails bridge

- **App factory + blueprints ≈ a lean Rails assembled by hand.** Flask is to Rails roughly what **Sinatra** is to Rails: micro, explicit, you choose every component. Put the Flask-vs-Django contrast front-and-center.
- **SQLAlchemy + Flask-Migrate ≈ ActiveRecord + `rails db:migrate`,** but the session/transaction boundary is explicit (closer to `ActiveRecord::Base.transaction` everywhere). Alembic ≈ `db/migrate`.
- **The outbox drain ≈ a Sidekiq-less durable job table you poll,** the pattern many Rails shops hand-roll before reaching for Sidekiq — `FOR UPDATE SKIP LOCKED` is the same "claim a row for exactly one worker" move.
- **HMAC webhook verification ≈ verifying a GitHub/Stripe/Shopify webhook in a Rails controller** — `compare_digest` ≈ `Rack::Utils.secure_compare`, read the **raw** body before parsing.
- **Pydantic schemas ≈ Grape entities / strong params + a validation layer,** decoupled from the ORM.
- **RQ + Redis ≈ Sidekiq** (stretch).

### 11. Senior signals & portfolio angle

- **Security correctness under adversarial input** — HMAC over raw bytes, constant-time compare, replay window, key rotation. Supports the LLM Trainer / Senior Python narratives.
- **Idempotency & exactly-once thinking** — the strongest "run things in production" signal. Highlight the "same key/same body vs same key/different body vs concurrent duplicate" matrix.
- **Durable outbox** — shows you know an HTTP handler shouldn't do heavy work *and* that at-least-once delivery needs a restart-safe queue, not a thread pool.
- **DB-constraint-first correctness** — dedup via unique indexes, not app-level check-then-insert. Say so.
- **Deliberate framework tradeoff** — a README section: "Why Flask here and Django for the platform app."
- **README must include:** the ASCII diagram, request lifecycle, the auth/idempotency decision matrix, the Flask-vs-Django rationale, a signed-`curl` quickstart, test/mypy/CI badges.

### 12. Common pitfalls

- **Parsing the body before verifying HMAC.** Capture `request.get_data()` once, verify, *then* parse.
- **Using `==` to compare signatures.** Always `hmac.compare_digest`.
- **Signing only the body, not the timestamp.** Sign `timestamp.body`; enforce a freshness window.
- **App-level "check then insert" for dedup.** Rely on a DB unique constraint and catch `IntegrityError`.
- **Doing scoring/aggregation in the request handler.** Write the outbox row and return 202.
- **Enqueuing before the DB commit.** The outbox pattern avoids this by writing the work row *inside* the same transaction; there is no external broker to race the commit.
- **Using a thread pool as the "queue."** It loses jobs on restart — the exact anti-pattern this project warns about. Use the outbox drain.
- **Flask dev server / `db.create_all()` in prod.** Use gunicorn + Alembic.
- **Testing only against SQLite.** Run a Postgres CI pass (JSONB, `SKIP LOCKED`, constraints).
- **Global mutable state across requests.** Watch app-context vs request-context lifetimes.
- **Leaking secrets in logs.** Log the delivery/correlation id, never the raw secret or full signature.
- **Over-investing in the dashboard.** One read-only list for MVP.

---

# Project 3 — Django Eval Platform Core Backend (Weeks 4–5)

*Folder: `django-app/` · Django + DRF · The system of record for the whole platform*

> **Relabeled to Weeks 4–5** (honest: internally 14–16 days). This is a 2.5–3 week project; the schedule reflects it.

### 1. Premise

You're building the **control-plane backend** for the LLM Evaluation Platform — the system a company uses to organize who evaluates which models against which test suites, and to store the record of every run and its results. Think of it as the Datadog/W&B-style backend for LLM quality. It is multi-tenant (**organizations**), has **users with roles** (owner/admin/member/viewer), and is the authoritative source of truth other services (P4, P5, P6) read from and write to via the shared `contracts/` shapes. This is deliberately the *system of record*, not the compute layer — its job is correct data modeling, a clean API, permissions, and query performance under real data volumes.

### 2. Why it's senior-level

- **Multi-tenant data isolation** — every query scoped to the caller's org; a cross-tenant leak is a security incident. A permissions + queryset problem, not a decorator you sprinkle on.
- **Non-trivial relational modeling** — 8 entities with one-to-many, many-to-many-through, and JSON result payloads. Migrations must be reversible and safe.
- **ORM performance under load** — the results/metrics endpoints N+1 badly by default. You *demonstrate* the problem (query counts) and *fix* it with `select_related`/`prefetch_related`, computing aggregates in SQL (`annotate`/`aggregate`), not Python.
- **Correctness under concurrency** — run + child result creation, and counter increments, need transactions and `select_for_update`.
- **API surface a real client depends on** — pagination, filtering, ordering, versioning, consistent error envelopes, object-level permissions.
- **Ops-readiness** — Django admin configured so on-call can inspect and fix data; Docker + migrations + seed.

### 3. Feature set

> **Scope trims (applied):** collapse ProviderConfig + ModelConfig into **one `ModelConfig`** (with a `provider` string) for MVP — split back in stretch. **Defer throttling to stretch.** Keep the trio that *is* the signal: the `assertNumQueries` N+1 before/after, the cross-tenant isolation negative test, and SQL `annotate/aggregate`, plus chainable managers and `select_for_update`.

> **Single source of truth (applied):** aggregates live in **one place — the `Metric` row** (one-to-one with Run). Drop the denormalized aggregate fields on `Run` so they can't drift.

**MVP (must-build):**

- Relational schema + migrations for: Organization, User (custom — decided at M1), Membership (role), Project, EvalSuite, TestCase, **ModelConfig** (with `provider` string), Run, Result, Metric.
- Token/session auth + **org-scoped access**: authenticated users only see data in orgs they're a member of.
- **Role-based permissions**: viewer (read), member (create/run), admin (manage suites/configs/members), owner (delete org) — enforced at object level.
- Full **DRF API**: ViewSets + routers for every resource, with **nested serializers** (a Run serialized with its suite summary and its results; an EvalSuite with its test-case count).
- **Pagination**, **filtering** (django-filter: project, suite, status, model, date range), **ordering**, **search**.
- **Django admin** for ops: list displays, filters, search, `raw_id_fields`, read-only computed columns, inlines (TestCases under EvalSuite; Results under Run), `list_select_related`.
- **ORM depth, demonstrated:**
  - A test asserting the query *count* before the fix (N+1) and after (constant), via `assertNumQueries` / `CaptureQueriesContext`.
  - `select_related` for FKs, `prefetch_related` for reverse/M2M.
  - **Aggregations/annotations** — run-level pass rate, avg score, p50/p95 latency, count by status — computed in SQL, exposed on the API.
  - **Custom managers + querysets** — e.g. `Run.objects.for_org(org).completed().with_scores()`.
  - **Transactions** — run creation + result seeding is atomic; the counter path uses `select_for_update`.
- A **status lifecycle** on Run (pending → running → completed/failed) with valid-transition enforcement.
- pytest suite (pytest-django) with **factory_boy**, covering models, serializers, permissions, and query-count assertions.

**STRETCH (senior bonus):**

- **Throttling** (per-user and per-org, tighter on trigger-run).
- **Split ModelConfig back into ProviderConfig + ModelConfig** (two-table config).
- **Celery + Redis** task that "triggers a run": the API enqueues a job that walks the lifecycle and writes result rows (LLM call simulated), showing async orchestration and idempotency.
- **Custom permission classes** (`IsOrgAdminOrReadOnly`, object-level `IsSameOrg`).
- **API versioning** (`/api/v1/…`) with a v1/v2 serializer divergence.
- **Soft delete / audit fields** (`created_by`, `updated_at`, `is_archived`) + a manager hiding archived rows.
- **OpenAPI schema** (drf-spectacular).
- **DB constraints** (unique-together, check constraints on status/score range) at the database level.

### 4. Architecture & data model

**Entities (words):**

- **Organization** — the tenant boundary. Has many Memberships, Projects.
- **User** — global identity. Joins orgs *through* Membership. **Custom User decided at M1.**
- **Membership** — join table (User ↔ Organization) carrying `role`. Unique on (user, org). Your `has_many :through` with an attribute on the join.
- **Project** — belongs to an Organization. Groups EvalSuites and ModelConfigs. `created_by` (User).
- **EvalSuite** — belongs to a Project. Has many TestCases (e.g. "toxicity-v3", "sql-generation").
- **TestCase** — belongs to an EvalSuite. `input`, `expected`, `weight`, `metadata` (JSONField). Serializes to the shared `test-case` shape.
- **ModelConfig** — belongs to a Project. Holds `provider` (string), model name, temperature, max tokens, plus a **reference** to provider credentials (never a raw key). (Stretch splits the credential half into ProviderConfig.)
- **Run** — the central event. Belongs to Project; references one EvalSuite and one ModelConfig. Has `status`, `triggered_by` (User), timestamps. **Aggregates live in the related Metric row, not on Run.** Has many Results.
- **Result** — belongs to a Run and a TestCase. `output`, `score` (0–1), `passed`, `latency_ms`, `error`, `raw` (JSONField). One Result per (run, test_case) — unique together. Serializes to the shared `result` shape.
- **Metric** — one-to-one with Run. The single source of aggregates: `pass_rate`, `avg_score`, `p50_latency`, `p95_latency`, `total_cases`, `failed_cases`. Written when a run completes.

**Key flows:**

1. **Create suite + cases** → member POSTs an EvalSuite, then TestCases.
2. **Configure model** → admin creates a ModelConfig.
3. **Trigger run** → member POSTs `/runs` with suite_id + model_config_id. API validates org scope, creates Run(status=pending) in a transaction, and (MVP) synchronously or (stretch) via Celery generates Result rows, computes the Metric, flips status to completed.
4. **Read results** → GET `/runs/{id}` (nested results) or `/runs/{id}/metrics` (aggregates). This is where N+1 lives and gets fixed.

**Diagram:**

```
Organization ─<Membership>─ User
     │                        │ triggered_by / created_by
     ├── Project ──┬── EvalSuite ──< TestCase
     │             ├── ModelConfig
     │             └── Run ──< Result >── TestCase
     │                  │
     │                  └── Metric (1:1 aggregates — single source of truth)
```

**External integrations:** none for MVP (the "LLM call" is simulated so the platform stays deterministic and testable). Stretch adds Redis (Celery). Real provider calls belong to P4 — this backend stores what that produces.

### 5. Tech & libraries

| Tool | Why (Rails analog) |
|---|---|
| **Django 5.x** | Batteries-included; ORM + admin + migrations are the point. ≈ Rails. |
| **Django REST Framework** | ViewSets, serializers, permissions, pagination. ≈ Grape + serializers, more integrated. |
| **django-filter** | Declarative query-param filtering. ≈ Ransack / manual scopes. |
| **pytest + pytest-django** | Runner + DB fixtures; `assertNumQueries`. ≈ RSpec + database_cleaner. |
| **factory_boy** | Test builders with associations. ≈ FactoryBot. |
| **mypy + django-stubs** | Static typing on models/serializers/services. A senior signal. |
| **ruff** | Lint + format. ≈ RuboCop. |
| **PostgreSQL** | JSONField, constraints, aggregations. Avoid SQLite beyond quick local runs. |
| **psycopg (v3)** | Postgres driver. |
| **uv** | Project/venv/deps. ≈ Bundler. |
| **Celery + Redis** *(stretch)* | Async run execution. ≈ Sidekiq. |
| **drf-spectacular** *(stretch)* | Auto OpenAPI/Swagger. ≈ grape-swagger. |
| **Docker + docker-compose** | Reproducible Postgres/Redis + app. |

### 6. Milestone breakdown

Sized to 3–4 hrs/day; ~14–16 days across Weeks 4–5. MVP lands at M6.

- **M1 — Skeleton & tooling (1 day).** `uv` project, Django + DRF, Postgres via compose, settings split (base/dev/test), ruff + mypy + pytest-django, a health endpoint + one passing test. **Custom User decided now.**
- **M2 — Core schema & migrations (2 days).** Organization, Membership, Project, EvalSuite, TestCase, ModelConfig. Reversible migrations. `__str__`, Meta ordering, `unique_together`/constraints. factory_boy factories.
- **M3 — Runs, Results, Metric + lifecycle (1.5 days).** Run/Result/Metric models, status enum, valid-transition logic, transactional run creation that seeds Results and computes the Metric (simulated scores). Unique (run, test_case). Custom manager/queryset skeleton.
- **M4 — DRF API layer (2.5 days).** Serializers (incl. nested Run→Results, Suite→cases-count), ViewSets + routers, pagination, ordering, django-filter, search. Consistent error responses.
- **M5 — Auth, org scoping & permissions (2 days).** Token auth, org membership resolution, base queryset scoping so every endpoint is tenant-isolated, role-based + object-level permission classes.
- **M6 — ORM depth: N+1, aggregations, managers (2 days).** Write the failing `assertNumQueries` proving N+1 on runs/results list, fix with `select_related`/`prefetch_related`, add `annotate`/`aggregate` for pass-rate/avg-score/p50/p95, finish chainable querysets, add `select_for_update` on the counter path. **← MVP complete.**
- **M7 — Django admin for ops (1 day).** Registered models with list_display/filters/search, inlines, read-only computed columns, `raw_id_fields`, `list_select_related`.
- **M8 — Stretch: throttling + Celery async runs + versioning (1.5–2 days).** Per-user/per-org throttles (tight on trigger-run); Redis broker; idempotent run task; API returns 202 + polling; `/api/v1/` namespace + a v2 serializer variation; split ModelConfig/ProviderConfig.
- **M9 — Polish, OpenAPI, README, seed (1 day).** drf-spectacular schema, seed command, README with the N+1 before/after story and query counts, final mypy/ruff/pytest green.

### 7. Acceptance criteria (per milestone)

- **M1:** `docker-compose up` starts Postgres; `pytest` green; health endpoint 200 JSON; mypy + ruff clean.
- **M2:** `migrate` then `migrate <app> zero` both succeed (reversible). Duplicate Membership (same user+org) raises `IntegrityError`. All factories build valid objects.
- **M3:** A run created via a service/manager produces N Result rows (N = suite's test-case count) and exactly one Metric, all in one transaction — verify by forcing an exception mid-way and asserting *nothing* was written (rollback). Invalid transition (completed → running) is rejected.
- **M4:** Every resource has list/retrieve/create/update/delete where appropriate; list endpoints paginate (assert `next`/`count`), filter (`?status=completed&model=…` narrows), order. Nested Run response includes results + suite summary in one payload.
- **M5:** A user in Org A gets 404/403 (not 200) for Org B's objects — a test proves cross-tenant isolation. A viewer gets 403 on create; a member succeeds; only admin can add members.
- **M6:** A test asserts the runs-list endpoint issues a **bounded, constant** number of queries regardless of row count (`assertNumQueries`), and the pre-fix version demonstrably issued O(N). Pass-rate/avg-score/p50/p95 in the API match hand-computed values and are produced by SQL aggregation (verify via `.query`/query capture, not Python loops). Custom queryset methods chain.
- **M7:** In admin, opening a Run detail with 500 results doesn't explode query count; filters and search work; a non-engineer could find "all failed runs for project X this week."
- **M8:** Exceeding the trigger-run rate limit returns 429; triggering a run returns 202; polling shows pending→running→completed; re-delivering the same task does not double-write results (idempotent). `/api/v1/runs` works; v2 serializer differs as documented.
- **M9:** `/api/schema` + Swagger UI render all endpoints; `seed` populates a demo org end-to-end; README shows before/after query counts; full suite + mypy + ruff green in CI.

### 8. Testing strategy

- **Runner:** pytest + pytest-django; `@pytest.mark.django_db`; a test Postgres. Keep DB-less unit tests fast.
- **Factories:** factory_boy for every model with `SubFactory`; a `RunFactory` that can optionally build child results.
- **Layered tests:** model/manager (constraints, `unique_together`, status transitions, chaining, aggregation math); serializer (nested representation, read/write field separation, validation); permission/tenant (parametrized over roles; the cross-org isolation test is the headline); API/integration (`APIClient`, pagination/filter/order); performance (`CaptureQueriesContext`/`assertNumQueries` locks in the N+1 fix so a regression fails CI).
- **Stretch Celery:** run tasks **eagerly** (`CELERY_TASK_ALWAYS_EAGER=True`), mock the simulated scoring so results are deterministic; assert idempotency by invoking twice.
- **Coverage targets:** every permission branch and every status transition; chase the risky paths (tenant scoping, transactions, aggregation math), not 100%.

### 9. Deployment / ops

- **docker-compose:** `web` (Django), `db` (Postgres), (stretch) `redis` + a `worker` (Celery).
- **Config via env** (django-environ or `os.environ`): `DATABASE_URL`, `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`, throttle rates. Provider credentials stored as *references*, never raw keys. `.env.example`.
- **Settings split:** base/dev/prod/test; prod turns off DEBUG, enforces `ALLOWED_HOSTS`, uses gunicorn.
- **Migrations** run as an explicit step (entrypoint/make target), never auto-applied silently. `seed` management command for demo data.
- **CI:** Postgres service; ruff → mypy → pytest on push.
- **Observability touch:** structured logging + DRF exception handling returning a consistent error envelope; log slow queries in dev.

### 10. Ruby/Rails bridge

- **ActiveRecord → Django ORM.** `has_many :through` with a role column *is* Membership. Rails **scopes** map to **custom QuerySet methods**; `includes(:results)` ≈ `prefetch_related`; `joins`/`.references` ≈ `select_related`; `ActiveRecord::Base.transaction` ≈ `with transaction.atomic()`; `lock!`/`SELECT … FOR UPDATE` ≈ `select_for_update()`.
- **Grape → DRF.** Grape entities ≈ serializers (nested ≈ nested); mounts/routers ≈ routers + ViewSets; `params do … end` ≈ serializer validation; `rescue_from` ≈ DRF exception handler; grape-swagger ≈ drf-spectacular.
- **RSpec → pytest.** `describe/context/it` ≈ functions + `parametrize`; `let`/`before` ≈ fixtures; FactoryBot ≈ factory_boy; `expect(…).to change{…}` ≈ `assertNumQueries` / row-count assertions.
- **Rails console/admin → Django shell + admin.** `rails c` ≈ `manage.py shell`; the **admin** has no clean Rails equivalent — configuring it well (inlines, `list_select_related`) is a differentiator.

### 11. Senior signals & portfolio angle

- **Lead with the N+1 story** — before query count → after constant count, with the `select_related`/`prefetch_related` diff and the `assertNumQueries` regression test. Directly on-target for Senior Python Developer.
- **Multi-tenant isolation as a security property** — a test proving Org A cannot read Org B's data, enforced at the queryset layer. Exactly the rigor LLM-eval/repo-validation employers want.
- **Aggregations in SQL, not Python** — pass-rate/avg-score/p50/p95 via `annotate`/`aggregate` proves you think about *where* computation happens.
- **Contract discipline** — versioning, pagination, OpenAPI show you build APIs other teams depend on. (Throttling is stretch but reinforces this.)
- **Ops-readiness** — configured admin + Docker + CI.
- **README framing:** open with "system of record for an LLM eval platform," a data-model diagram, the N+1 before/after, the tenant-isolation test, and a one-line map from each feature to its Rails analog.

### 12. Common pitfalls

- **Deciding the User model late.** Decide at M1 (custom User or a Profile FK) and commit.
- **Testing on SQLite, deploying on Postgres.** JSONField, constraints, and some aggregations differ. Postgres everywhere, including CI.
- **"Fixing" N+1 you can't see.** Capture real query counts so before/after is provable — that evidence *is* the deliverable.
- **Tenant scoping in views only.** Centralize in a base queryset/permission mixin; test the negative case.
- **DRF permissions ≠ object-level by default.** `has_permission` gates the endpoint; add `has_object_permission` for per-row checks; test a viewer *and* a cross-org member.
- **Non-atomic run creation.** Wrap it and force-fail a test to prove rollback.
- **Aggregating in Python.** Push it into the DB.
- **Serializers that trigger queries per row.** A `SerializerMethodField` hitting the DB per object N+1s even after you fix the viewset — prefetch/annotate what the serializer reads.
- **Two sources of aggregate truth.** You chose the Metric row — do not also denormalize onto Run.
- **Celery non-idempotency (stretch).** Guard with unique constraints + get-or-create; test double-delivery.
- **Over-building.** M1–M6 is the resume-worthy MVP; treat throttling/Celery/versioning/OpenAPI as bonuses.

---

# Project 4 — FastAPI Async Eval Runner / LLM Gateway (Week 6)

*Folder: `fastapi-app/`*

A FastAPI service that fronts multiple LLM providers, validates everything with Pydantic v2, and orchestrates concurrent, resilient, observable calls for eval runs. **P4 owns throughput/cost/fan-out; it builds the normalized message/response model that P5 reuses for its tool-use loop.**

> **Scope fix (applied):** MVP ships **one real adapter (Anthropic — your model IDs there are authoritative) + a fake adapter.** The **OpenAI adapter is stretch (SWING ITEM #2).** Your concurrency/orchestration tests use a fake adapter anyway, so the pattern is fully demonstrated without two live SDKs. Realistic MVP is 10–12 days if you try to do everything; the one-week slot assumes this trim.

### 1. Premise

You're building the **LLM Gateway** the rest of the platform calls instead of hitting Anthropic/OpenAI directly. Internal teams (and your own P6 eval-harness) POST an *eval-run request* — a model profile plus a batch of test cases — and the gateway fans those out as bounded, concurrent async calls, records every result (tokens, cost, latency, errors) in Postgres, and streams progress back. It also exposes a single-completion endpoint with SSE streaming for interactive use. It's the internal "AI platform" tier every company building on LLMs needs: one authenticated, rate-limited, retry-aware, cost-tracked door to expensive third-party APIs. **Eval-run submissions and result items use the shared `contracts/` shapes.**

### 2. Why it's senior-level

- **Async correctness under real I/O.** Getting concurrency wrong (blocking the event loop with a sync DB driver, `time.sleep`, or CPU-bound work) silently destroys throughput. You must prove you never block the loop.
- **Bounded fan-out & backpressure.** Naive `asyncio.gather` over 5,000 cases exhausts memory and gets you 429'd. You need semaphores, queues, and per-profile concurrency ceilings.
- **Failure is the normal case.** Per-call timeouts, bounded retries with jittered backoff, and a circuit breaker so one degraded provider doesn't cascade.
- **DI & lifecycle.** Shared async clients and DB engines created once at startup, injected, closed cleanly.
- **Data modeling for an async ORM.** Async SQLAlchemy forces explicit sessions, no lazy loading — different muscles than ActiveRecord.
- **Contract-first API.** Auto OpenAPI, typed request/response models, strict `mypy`.
- **Multi-tenant auth, rate limiting, cost accounting.**

### 3. Feature set

**MVP (must-build)**
- Pydantic v2 models for: single completion, batch eval-run submission, run status, result items — with `field_validator`/`model_validator` enforcing invariants; aligned with the shared contract.
- `pydantic-settings` `Settings` for all config (provider keys, DB URL, concurrency limits, timeouts) from env.
- Provider abstraction (one Protocol/ABC: `complete`, `stream`) with **one real adapter (Anthropic, async SDK) + a fake adapter**. The **normalized message/response model built here is the package P5 reuses.**
- FastAPI DI for provider clients, config, DB session, and the authenticated caller.
- `POST /v1/completions` — single completion, non-streaming, normalized response (text, usage, cost, latency).
- `POST /v1/completions/stream` — **SSE streaming** of tokens (core requirement).
- `POST /v1/eval-runs` — submit a batch; **bulk-insert** run + items as `queued`; return `202` with a run id; processing happens concurrently in the background with a **bounded** fan-out.
- `GET /v1/eval-runs/{id}` — status + aggregate counts; `GET /v1/eval-runs/{id}/items` — paginated results.
- Per-call **timeout + bounded retry** (jittered exponential backoff) on retryable errors only.
- **Async SQLAlchemy** persistence + **Alembic** (async `env.py`).
- **API-key auth** (hashed keys, org-scoped) as a FastAPI dependency.
- Auto OpenAPI docs; strict `mypy`; pytest suite mocking providers.
- **Dockerized** (multi-stage) + docker-compose (app + Postgres).

**STRETCH (senior bonus)**
- **OpenAI adapter** (the second real provider — SWING ITEM #2).
- **Circuit breaker** per provider/model profile (open on threshold, half-open probe).
- **Rate limiting** — per-org token bucket (in-process or Redis) → `429` with `Retry-After`.
- **SSE progress stream for eval-runs** (`GET /v1/eval-runs/{id}/events`).
- **Cost + usage accounting** with a pricing table per model, aggregated per run and per org.
- **Idempotency keys on run submission** (dedupe retried POSTs) — *this is where P2's idempotency signal folds in if you drop standalone Flask.*
- **Signed inbound webhook endpoint** (HMAC over raw bytes + timestamp window) — *the P2 crown-jewel signal, folded here if Flask is cut.*
- **Structured logging** (structlog) + correlation IDs + **Prometheus** `/metrics`.
- **Graceful shutdown / cancellation** — in-flight items cancelled on SIGTERM; run marked `interrupted`.
- **OpenTelemetry** traces; durable-queue note (swap `BackgroundTasks` for Redis/Arq).

### 4. Architecture & data model

```
        client (eval-harness / curl)
                 │  API key
                 ▼
        ┌─────────────────────────┐
        │        FastAPI app       │
        │  ┌────────────────────┐  │
        │  │ routers (Depends)  │  │  ← auth, config, db session, providers injected
        │  ├────────────────────┤  │
        │  │ Pydantic v2 models │  │  ← validate in/out; generate OpenAPI + tool schemas
        │  ├────────────────────┤  │
        │  │ orchestrator       │  │  ← Semaphore + gather, retries, timeouts, breaker
        │  ├────────────────────┤  │
        │  │ provider registry  │──┼──► AsyncAnthropic ─► api.anthropic.com  (MVP)
        │  │ (adapters via DI)  │──┼──► AsyncOpenAI    ─► api.openai.com     (stretch)
        │  └────────────────────┘  │
        └───────────┬──────────────┘
                    │ async SQLAlchemy (asyncpg)
                    ▼
             Postgres (runs, items, usage, keys)
```

**Layers**
- **Routers** — thin; validate via Pydantic, resolve dependencies, delegate.
- **Provider adapters** — one Protocol (`complete`, `stream`), one real implementation (Anthropic) + a fake for tests. Each translates the gateway's normalized request into the SDK call and the response back into the normalized shape (text, `usage`, finish reason, error class). **This normalized model is shared with P5.**
- **Provider registry** — a dependency mapping a *model profile* (logical alias) → adapter + upstream model id + limits. Created once in lifespan; holds the shared async SDK client (which owns its httpx pool); closed on shutdown.
- **Orchestrator** — runs a run's items through a bounded `asyncio.gather` (Semaphore = the profile's concurrency ceiling), wrapping each call in timeout + retry (+ breaker stretch), writing each result as it lands.

**Entities (recurring platform domain):** Organization; **ApiKey** (`hashed_key`, `prefix`, `scopes`, `revoked_at` — never the raw key); **ProviderCredential** (reference to the secret, not the value); **ModelProfile** (`alias`, `provider`, `upstream_model` config, `default_params`, `timeout_s`, `max_concurrency`, `rate_limit`); **EvalRun** (`status` ∈ `queued`/`running`/`succeeded`/`partial`/`failed`/`interrupted`, `total`, `completed`, `failed`, `concurrency`, timestamps, optional `idempotency_key`); **EvalRunItem** (`index`, `input`, `expected`, `status`, `output_text`, `tokens_in`, `tokens_out`, `cost_usd`, `latency_ms`, `attempts`, `error_type`, `error_detail`); **UsageRecord** (stretch rollups). Relationships: Org 1—* {ApiKey, ProviderCredential, ModelProfile, EvalRun}; EvalRun 1—* EvalRunItem; EvalRun *—1 ModelProfile.

**Key flows**
1. **Single completion:** auth → validate → registry resolves adapter → `await adapter.complete(req)` with timeout/retry → normalize → (log usage) → return. Streaming variant returns SSE from the adapter's async token stream.
2. **Eval-run submit:** auth → validate batch → **one transaction: bulk-insert `EvalRun(queued)` + N `EvalRunItem(queued)`** → schedule background processing → return `202 {run_id}`. Background task marks run `running`, fans out under the Semaphore, updates each item + run counters as results arrive, sets terminal status.
3. **Poll/subscribe:** `GET /eval-runs/{id}` for aggregates; SSE events endpoint (stretch) for live per-item completion.

### 5. Tech & libraries

- **FastAPI** — routing, DI (`Depends`), lifespan, auto OpenAPI, `StreamingResponse`.
- **Pydantic v2** + **pydantic-settings** — validation, `field_validator`/`model_validator`, `computed_field`, JSON-Schema generation (feeds OpenAPI *and* future tool/function schemas), typed config from env.
- **anthropic** (`AsyncAnthropic`) — official async SDK (built on httpx); async `create` + streaming. **OpenAI** (`AsyncOpenAI`) is the stretch second adapter. Model ids live in `ModelProfile` config — pull current ids from the provider's Models API/docs rather than hard-coding.
- **httpx** — async HTTP under the SDK; also the test client (`AsyncClient` + `ASGITransport`).
- **SQLAlchemy 2.0 async** + **asyncpg** — async ORM/engine; `AsyncSession`, async `sessionmaker`. asyncpg (never psycopg2 sync) keeps the loop unblocked.
- **Alembic** — migrations (async-capable `env.py`).
- **tenacity** — declarative retry (stop-after-attempts, wait-exponential-jitter, retry-on-exception-type).
- **A circuit breaker** (`aiobreaker`/`purgatory` or hand-rolled) — stretch.
- **slowapi**/`limits` or a Redis token bucket (**redis.asyncio**) — rate limiting (stretch).
- **sse-starlette** (`EventSourceResponse`) — SSE (MVP can use raw `StreamingResponse`).
- **structlog** + **prometheus-fastapi-instrumentator** — observability (stretch).
- **uv**; **pytest**, **pytest-asyncio**, **respx** (mock provider HTTP), **polyfactory**, **testcontainers**/async-sqlite, **freezegun**.
- **Docker** (multi-stage) + **docker-compose** + **uvicorn** (behind **gunicorn** with uvicorn workers in prod).

### 6. Milestone breakdown (Week 6; with explicit risk buffer)

> **Risk-buffer note (applied):** **M5 (async SQLAlchemy + async Alembic) is the highest-risk day** — no-lazy-load discipline and async `env.py` config eat a day+ for a newcomer. **Front-load M5 and give it a buffer day**; discover greenlet errors on day 2, not day 6.

- **M1 — Scaffold, config, health (~3 hrs).** uv project; app factory + lifespan skeleton; `Settings`; `GET /healthz`; mypy/ruff; Dockerfile + compose stub. MVP.
- **M2 — Pydantic domain models + OpenAPI (~4 hrs).** Normalized `CompletionRequest`/`CompletionResponse`, `EvalRunCreate`, `EvalRunItemIn`, `EvalRunView`, `EvalRunItemView`, `ModelProfile`, provider enum. Validators (non-empty messages; max-tokens within profile bounds; mutually exclusive fields; alias must resolve). Confirm `/docs`. MVP.
- **M5-early — Async persistence + migrations (front-loaded, ~4–5 hrs + buffer).** Async engine/session dependency; ORM models; Alembic async `env.py`; verify no sync DB access on the async path. **Do this before the orchestrator.** MVP.
- **M3 — Provider abstraction + single completion (~4 hrs).** Adapter interface; **Anthropic implementation** + a fake, created in lifespan and injected; registry resolving profile→adapter; `POST /v1/completions`. No blocking calls. MVP.
- **M4 — SSE streaming (~3–4 hrs).** `POST /v1/completions/stream`: adapter `stream()` yields tokens; SSE `StreamingResponse` with correct framing + terminal event; handle mid-stream errors and client disconnects. MVP.
- **M6 — Batch eval-run orchestration (~4 hrs).** `POST /v1/eval-runs` **bulk-inserts** run+items and schedules background processing; orchestrator fans out under `Semaphore(profile.max_concurrency)`; per-item results written as they complete; run counters + terminal status; `GET` status + paginated items. MVP.
- **M7 — Resilience + auth (~4 hrs).** Per-call timeout; tenacity retry on retryable errors only (429/5xx/timeouts, not 4xx); API-key auth dependency (hash + lookup + org scoping). Stretch within the day: breaker, token-bucket rate limiting, idempotency key. MVP = timeout+retry+auth.
- **M8 — Observability, tests, ship (~4 hrs).** structlog + correlation IDs + `/metrics` (stretch); full pytest suite (see §8); finalize Docker + compose; README with diagram + run instructions. MVP = tests + Docker + README. (OpenAI adapter here if time allows.)

### 7. Acceptance criteria (self-verifiable)

- **M1:** `docker compose up` serves `/healthz` → `200`. Missing required env var → app fails fast with a clear Pydantic settings error. `mypy` clean.
- **M2:** Invalid payloads (empty messages, max-tokens over profile cap, unknown provider) → `422` with field-level detail. `/openapi.json` includes every model. Round-trip serialize/deserialize is lossless.
- **M5:** Alembic `upgrade head` builds the schema; a completion persists an item row with tokens/latency. Attempting a sync DB driver or lazy-load raises/greenlet-errors — confirming you're genuinely async. `mypy` clean.
- **M3:** `POST /v1/completions` returns normalized text + usage + latency (provider mocked). Overriding the adapter via a dependency override changes behavior with no code edits — proves DI. No `time.sleep`/sync HTTP on the request path (verify by grep + a loop-blocking test).
- **M4:** Streaming emits multiple SSE chunks then a terminal event; a mid-stream provider error surfaces as an error event, not a hang; client disconnect stops upstream work (no leaked task).
- **M6 (corrected):** Submitting a run **persists via bulk insert** and returns `202` quickly for typical batches; the endpoint returns *before* provider calls complete (**the fan-out, not the persist, is backgrounded** — for very large batches the persist is bounded by the bulk insert, not by per-row inserts). With a fake adapter that records concurrent in-flight count, the **observed max concurrency never exceeds the profile ceiling.** Run ends `succeeded`/`partial` with counts matching item statuses. Polling shows `queued → running → terminal`.
- **M7:** A forced 429 from the fake provider triggers exactly the configured retries with increasing backoff, then succeeds or records a terminal error (assert attempt count + timing). A non-retryable `400` is **not** retried. Missing/invalid API key → `401`; valid key scoped to org A cannot read org B's runs → `403/404`. (Stretch) breaker opens after N failures and short-circuits; rate limit → `429 + Retry-After`.
- **M8:** `pytest` green including a concurrency test and an SSE test; coverage on validators, adapter, orchestrator, auth. `docker compose up` from a clean checkout runs migrations and serves traffic. README renders with the diagram + a working curl example. `mypy` (strict) and ruff clean.

**Perf targets (corrected):** batch submit returns fast for typical batches (persist uses bulk insert; only the fan-out is backgrounded); 50 concurrent upstream calls against a fake ~200 ms provider complete in roughly `max(200 ms × ceil(50/concurrency))`, proving true concurrency (not serial); gateway's own per-call overhead (excluding provider time) < ~15 ms p95 in tests.

### 8. Testing strategy

- **Unit — Pydantic models & validators:** valid/invalid cases, boundary values, mutually-exclusive fields; assert error locations. **polyfactory** to generate valid instances.
- **Adapter:** mock provider HTTP with **respx**; assert request translation and response normalization, including error mapping (429 → retryable, 400 → non-retryable). (Second adapter's fixtures added when OpenAI stretch lands.)
- **API/integration:** drive the app with **httpx `AsyncClient` + `ASGITransport`** under `pytest-asyncio`; override provider/DB/auth deps with fakes.
- **DB layer:** **testcontainers-postgres** (exercises asyncpg) or async SQLite for speed; a fresh-schema fixture yielding an `AsyncSession`.
- **Concurrency:** a fake adapter incrementing/decrementing a shared counter tracking the max — assert it never exceeds the ceiling; assert wall-clock matches bounded-parallel expectation.
- **Retry/timeout:** fake adapter failing K times then succeeding; assert attempt count and that 4xx isn't retried (patch sleep / control time).
- **SSE:** consume the streaming response; assert the event sequence + terminal marker; test client-disconnect cancellation.
- **Auth/tenancy:** missing key, revoked key, cross-org access.
- **Fixtures:** shared `app`, `client`, `db_session`, `fake_provider`, `api_key`. Keep external I/O fully mocked so the suite is deterministic.

### 9. Deployment / ops

- **Docker:** multi-stage, `uv`-installed deps, non-root, `uvicorn` (dev) / `gunicorn -k uvicorn.workers.UvicornWorker` (prod), container `HEALTHCHECK` on `/healthz`.
- **compose:** `app` + `postgres` (+ `redis` for rate-limit/queue stretch); app waits for DB healthy; env-file config.
- **Config/secrets:** per the platform secrets model — everything via env through `Settings`; provider keys and DB URL never in the image; `.env.example`.
- **Migrations:** Alembic as a one-shot step before the app serves; document `alembic upgrade head` / `revision --autogenerate`.
- **Local run:** `uv run uvicorn …` for hot-reload; `docker compose up` for the stack.
- **Graceful shutdown:** lifespan closes provider clients + DB engine; in-flight items cancelled on SIGTERM (stretch).
- **CI:** ruff + `mypy` + pytest (Postgres service or testcontainers) on push.

### 10. Ruby/Rails bridge

- **Pydantic v2 ≈ strong params + `ActiveModel`/`dry-validation` + Grape entities, unified** — one class is your validation, type, serializer, *and* JSON-Schema/OpenAPI source.
- **FastAPI `Depends` ≈ Rails DI you hand-roll** (service objects, `around_action`, current-user resolution) — but first-class and composable; tests override it like a stub.
- **Async SQLAlchemy ≈ ActiveRecord, but explicit** — no implicit connection, no lazy `has_many` mid-request; you `await` and eager-load deliberately. Alembic ≈ `db/migrate`.
- **`asyncio.gather` + `Semaphore` ≈ a Sidekiq batch / `concurrent-ruby` pool, in-process and cooperative.** SSE ≈ `ActionController::Live`; tenacity ≈ `retriable`; `pydantic-settings` ≈ Rails credentials/`ENV`/`config`.

### 11. Senior signals & portfolio angle

- **Provable async correctness** — the concurrency test and "no blocking on the loop" test are the headline.
- **Resilience matrix** — timeouts × retries × (breaker) × rate limits, applied *only* to the right error classes.
- **Contract-first, typed, documented** — strict `mypy` + auto OpenAPI + validated I/O.
- **Ties to your differentiator** — this gateway is the sibling of your MCP + function-calling work; same normalized-request/tool-schema instincts, now productionized. **The normalized model here is literally reused by P5.**
- **README highlights:** the architecture diagram; a short "why Pydantic is everywhere in LLM tooling" note (every boundary is loosely-typed JSON you don't control — inbound requests, provider responses, tool argument schemas, structured-output contracts, config — and Pydantic v2 is the single source of truth for runtime validation, static types, JSON-Schema generation, and fast (de)serialization); the resilience design; the concurrency proof; and one line connecting to `eval-harness`/`agent-cli`. Include a curl-to-SSE example and a `docker compose up` quickstart.

### 12. Common pitfalls

- **Blocking the event loop** — sync DB drivers (psycopg2), `time.sleep`, `requests`, CPU-bound work in `async def`. Use asyncpg/httpx/async SDKs; offload unavoidable sync work to a thread executor.
- **Unbounded `gather`** — always gate with a Semaphore / worker pool / chunking.
- **Timeout × retry multiplication** — a 30 s timeout with 3 retries is a 120 s worst case. Budget total time.
- **Creating clients per request** — instantiate the SDK client and DB engine once in lifespan; close on shutdown.
- **Retrying non-retryable errors** — never retry 400/422/auth; only 429/5xx/timeouts/connection errors.
- **SSE gotchas** — proxies buffer SSE (disable buffering / set headers); handle client disconnect to cancel upstream work; always send a terminal event; surface mid-stream errors as an event.
- **Inserting N rows one-by-one on submit** — use bulk insert so the 202 stays fast; the *fan-out* is what's backgrounded, not the persist.
- **`BackgroundTasks` durability** — fine for MVP; note runs die on restart; a durable queue (Redis/Arq) is the production answer (stretch).
- **Async SQLAlchemy footguns** — no lazy loading (eager-load or greenlet errors); one session per request scope; give each fan-out task its own session or serialize writes.
- **Pydantic v1 vs v2 drift** — use v2 (`@field_validator`, `model_dump()`, `model_config`) consistently.
- **Breaker/limiter state across workers** — in-process state isn't shared across gunicorn workers; for multi-worker correctness the counters belong in Redis (call this out even if MVP is single-worker).
- **Secrets in the image / logs** — keep provider keys in env/secret store; don't log full prompts/keys.
- **Reading whole responses into memory** — stream large completions.

---

# Project 5 — `agent-cli`: Provider-Agnostic Function-Calling Agent (Weeks 7–8)

*Folder: `llm/agent-cli/`*

> **Note on model IDs:** Anthropic strings below are current and authoritative (verified via the Anthropic SDK skill): default `claude-opus-4-8`; cheaper/faster tiers `claude-sonnet-5` and `claude-haiku-4-5`. For OpenAI, model IDs drift — do **not** hardcode from memory; pull the live list from OpenAI's `/v1/models` and pin exact strings in a central model registry (M4). "Registry, not literals" is itself a senior signal.

A command-line coding/agent runner — a minimal, production-shaped Aider/Claude-Code — that a platform team would embed to let an LLM *act* on a repository under strict guardrails. It is the "agent" component of the platform: eval suites (P6) can drive it to attempt tasks, and every run emits a structured trace the harness consumes as ground truth. **It reuses the normalized message/response model built in P4.**

### 2. Why it's senior-level

- **The full tool-use loop, by hand** — request → model asks for tool(s) → validate → execute → feed results back → loop, with correct message-history reconstruction (the #1 source of API 400s).
- **Provider abstraction** — Anthropic and OpenAI have genuinely different wire shapes (block-based vs. `tool_calls` array; parsed `input` dict vs. JSON-string `arguments`; `stop_reason` vs. `finish_reason`). You design a normalized internal model both map to. **This is the same normalized model from P4 — reuse, don't re-derive.**
- **Agent-loop control theory** — stop conditions, `max_steps`, token/cost budgets, retry/backoff, graceful abort, idempotent trace flushing on crash/Ctrl-C.
- **Sandboxing & guardrails** — subprocess timeouts and process-group kills, command allowlists, path-traversal/symlink jails, dry-run patch application with backups, tool-output truncation, human-in-the-loop confirmation for mutating ops.
- **Observability** — a structured, replayable trace of *every decision*, with secret redaction.
- **Senior Python craft** — Pydantic v2 schemas, `mypy --strict`, typed provider protocols, deterministic mocking of the LLM boundary, CI, a non-root Docker image.

### 3. Feature set

> **Cut line (applied):** the mutating tools are the internal cut line. If behind, ship **read_file + search_code + run_tests** for a demoable MVP and make **apply_patch the first stretch** — but note this weakens the "self-heal failing test" narrative, so cut only under time pressure.

**MVP (must-build)**
- CLI: `agent run "<task>" [--provider anthropic|openai] [--model …] [--workdir PATH] [--read-only] [--auto-approve] [--max-steps N] [--budget-tokens N]`; plus `agent tools list` and `agent trace show <run_id>`.
- Provider abstraction with **two working adapters** (Anthropic SDK, OpenAI SDK) behind one protocol, driving the identical loop. (Reuses P4's normalized model.)
- Normalized internal message/tool-call model; adapters serialize to and parse from each provider's wire format.
- Tool registry where each tool = a Pydantic input model (→ JSON schema) + a handler + metadata (mutating?, timeout, max-output). Registry emits provider-specific tool schemas.
- **Tools**: `read_file`, `search_code` (ripgrep-backed), `run_tests` (sandboxed pytest/command with timeout), `apply_patch` (unified-diff, dry-run + backup). *(If behind: apply_patch → stretch.)*
- The agent loop with correct stop conditions: natural stop, `max_steps`, token/cost budget, fatal-error policy, user abort.
- Guardrails: input validation (bad args → `is_error` tool result, model retries), path jail, subprocess timeout + process-group kill, command allowlist, output truncation, `--read-only` blocks mutating tools, confirmation gate for mutating tools (`--auto-approve` to skip).
- Structured JSONL trace per run (structlog), with secret redaction and token/cost accounting. **Trace conforms to the `run` portion of the shared contract where applicable.**
- Tests (unit + loop tests with a scripted fake provider), `mypy --strict` clean, ruff clean, README.

**STRETCH (senior bonus)**
- **MCP integration** — consume tools from an MCP server, or expose the agent's own tools over MCP (leverages your MCP/OAuth background; strong differentiator).
- Parallel tool calls; streaming output with `rich`; prompt caching of the stable system prompt + tool definitions; provider-neutral "reasoning effort" knob; resume/replay from trace; cost-aware model routing; a `run_eval` tool + "self-heal failing test" workflow closing the loop with P6.

### 4. Architecture & data model

```
        agent run "task"
              │
        ┌─────▼─────┐   config: flags > env > .agent.toml > defaults
        │    CLI    │   (Typer)
        └─────┬─────┘
              │ RunConfig
        ┌─────▼───────────────────────────────────────┐
        │              Agent Loop / Orchestrator        │
        │  send → parse tool calls → validate →         │
        │  execute (guarded) → append results → repeat  │
        │  stop: final | max_steps | budget | abort |   │
        │        fatal_error                            │
        └──┬───────────────┬───────────────────┬────────┘
           │               │                   │
   ┌───────▼──────┐ ┌──────▼───────┐   ┌───────▼────────┐
   │  Provider    │ │ Tool Registry│   │  Trace Writer  │
   │  (protocol)  │ │ + JSON schema│   │  JSONL + redact│
   │ Anthropic /  │ └──────┬───────┘   └───────┬────────┘
   │ OpenAI adapt.│        │                   │
   └──────────────┘ ┌──────▼───────┐   ./.agent/runs/<id>.jsonl
                    │   Sandbox    │
                    │ path jail,   │
                    │ timeouts,    │
                    │ allowlist    │
                    └──────────────┘
```

**Provider protocol (words).** One method, roughly `generate(normalized_messages, tool_specs, params) -> normalized_response`. Each adapter (a) serializes the normalized message list to its wire format, (b) serializes tool specs to its schema shape, (c) calls its SDK, (d) parses the response back into the normalized model, (e) reports usage. The loop only ever touches the normalized model — **the same one P4 established.**

**Normalized internal model (words).** A message is a role plus an ordered list of parts: `text`, `tool_call` (`{call_id, name, args: dict}`), or `tool_result` (`{call_id, content, is_error}`). A normalized response carries assistant text, a list of `tool_call`s, a `stop_reason` enum (`final`/`tool_calls`/`max_tokens`/`refusal`/`error`), and `usage`.

**Provider tool-use shapes (the seam you normalize over):**

| | Anthropic (Messages API) | OpenAI (Chat Completions) |
|---|---|---|
| Tool def | `{name, description, input_schema}` (+ optional `strict`) | `{type:"function", function:{name, description, parameters}}` (+ optional `strict`) |
| Model wants a tool | content block `{type:"tool_use", id, name, input(dict)}`; `stop_reason == "tool_use"` | `message.tool_calls[]` = `{id, function:{name, arguments(JSON string)}}`; `finish_reason == "tool_calls"` |
| Echo assistant turn | append the assistant's **entire** `content` (incl. tool_use blocks) | append the assistant `message` (incl. `tool_calls`) |
| Return results | **one** user message whose content is a list of `{type:"tool_result", tool_use_id, content, is_error?}` — all together | **one `role:"tool"` message per call**, each `{tool_call_id, content}` |
| Natural stop | `stop_reason == "end_turn"` | `finish_reason == "stop"` |
| Force tool | `tool_choice: auto/any/tool/none` | `tool_choice: auto/none/required/{function}` |

Two normalization traps to handle explicitly (both get dedicated headline tests): OpenAI `arguments` is a **string that may be invalid JSON** (parse defensively; malformed → `is_error` result so the model self-corrects); Anthropic wants all tool results in a **single** user turn while OpenAI wants **one message per call** — your serializer owns that difference.

**Entities / data model (persisted as the trace + config; SQLite optional):** `RunConfig`; `Run` (id, config snapshot, status `completed`/`max_steps`/`budget_exceeded`/`aborted`/`failed`, final text, total usage/cost); `Step` (kind `model_request`/`model_response`/`tool_call`/`tool_result`, payload); `ToolCall` (call_id, name, raw args, validated args, status, output, error, duration_ms); `ToolSpec` (name, description, JSON schema, `mutating`, timeout_s, max_output_bytes); `Patch` (target path, diff, applied, backup path).

**External integrations:** Anthropic SDK, OpenAI SDK, `ripgrep` binary, the host subprocess/filesystem (jailed), and — stretch — an MCP server as a tool source.

### 5. Tech & libraries

- **Python 3.12 + uv + pyproject.**
- **`anthropic`, `openai`** — official SDKs (retries, typed errors, streaming).
- **`pydantic` v2** — tool input models → JSON schema; `RunConfig` + settings validation.
- **`typer`** — type-hint-driven CLI (Thor/rake analog); `click` fallback.
- **`rich`** — human console output, diff highlighting; keep trace (machine) and console (human) renderers separate.
- **`structlog`** — two renderers: JSON to trace, pretty to console. Your Lograge analog.
- **`tenacity`** — explicit retry/backoff on provider errors, with per-attempt tracing.
- **`ripgrep`** — fast `search_code`; document as a dependency with a pure-Python `os.walk`+`re` fallback.
- **`pytest` + `pytest-cov` + `pytest-mock`**; `tmp_path` fixtures for filesystem tools.
- **`mypy` (strict) + `ruff`.**
- **Docker** — non-root image with ripgrep, runs against a mounted repo.

### 6. Milestone breakdown

~3–4 hrs/day over ~10–12 working days (Weeks 7–8). Each milestone is independently demoable.

- **M1 — Skeleton + provider protocol (Days 1–2).** uv project, Typer CLI, `RunConfig`, structlog console+JSON, the `Provider` protocol, and a *no-tools* one-shot on **both** providers. **Import/reuse P4's normalized model here.**
- **M2 — Tool registry + schema generation (Days 2–3).** Tool interface (Pydantic model + handler + metadata). Implement `read_file` and `search_code` (read-only). Registry emits Anthropic-shaped and OpenAI-shaped schemas. `agent tools list`.
- **M3 — Tool-use loop, one provider (Days 3–5).** Full loop for Anthropic: detect `tool_use`, echo assistant content correctly, execute, return `tool_result`, loop to `end_turn`. Demo: "read `X` and summarize it."
- **M4 — Provider-agnostic loop (Days 5–6).** Implement the OpenAI adapter for the full loop; the *same* task runs on `--provider openai`. Central model registry (verify OpenAI ids against the live endpoint).
- **M5 — Loop hardening (Days 6–8).** Stop conditions (`max_steps`, token/cost budget, fatal-error policy), retry/backoff via tenacity, graceful Ctrl-C that flushes the trace, output truncation.
- **M6 — Mutating tools + sandbox + guardrails (Days 8–10).** `run_tests`/`run_shell` (jailed cwd, timeout, process-group kill, allowlist) and `apply_patch` (dry-run, backup, path jail). Confirmation gate; `--read-only` and `--auto-approve`. *(apply_patch is the cut line if behind.)*
- **M7 — Structured trace + inspect (Days 10–11).** Complete JSONL trace; secret redaction; token/cost accounting; `agent trace show <run_id>` renders a readable timeline.
- **M8 — Tests, CI, Docker, README (Days 11–12).** Fill coverage, `mypy --strict` + ruff clean, GitHub Actions (lint + type + test + fake-provider smoke), Dockerfile, README with the architecture diagram + a recorded demo run.

### 7. Acceptance criteria

- **M1:** `agent run "say hi"` prints a reply from Anthropic and (with `--provider openai`) from OpenAI. `mypy --strict` + `ruff` clean. A JSON trace line is written for request/response.
- **M2:** `agent tools list` shows `read_file` and `search_code` with valid JSON schemas. A unit test asserts the Anthropic and OpenAI schemas are structurally valid and derive from the same Pydantic model. Bad args raise a catchable validation error.
- **M3:** "read `<file>` and summarize" causes exactly one `read_file` call, the result is fed back, the model produces a final answer. Trace: request → tool_use → tool_result → end_turn. A malformed/oversized read returns an `is_error` result and the model recovers rather than crashing.
- **M4 (headline traps):** The identical task completes on both providers with the same tool invoked. Adapter unit tests parse recorded Anthropic and OpenAI wire responses into identical normalized objects, and serialize a normalized history into each correct wire shape. **OpenAI `arguments` that are invalid JSON produce an `is_error` result, not an exception** (dedicated test). **Anthropic tool results are emitted in a single user turn** (dedicated test).
- **M5:** `--max-steps 2` on a task needing more stops with status `max_steps`. Small `--budget-tokens` stops with `budget_exceeded`. Ctrl-C mid-run leaves a complete, valid trace file (assert it parses). A simulated 429/500 is retried with backoff and each attempt appears in the trace.
- **M6:** A `read_file`/`apply_patch` with `../` or a symlink escaping `--workdir` is refused (unit test asserts the jail). A denied command (`rm -rf`) is blocked. `run_tests` on a hanging command is killed at the timeout (wall-clock < timeout + slack, child process group gone). `apply_patch` applies cleanly, writes a backup, and is revertible from the backup. `--read-only` makes every mutating tool refuse.
- **M7:** The trace is valid JSONL; replaying/parsing reconstructs the run's steps. Grep the trace for your API key → zero matches (redaction proven). Computed cost equals `Σ usage × registry prices` within rounding.
- **M8:** CI green (lint + mypy + tests); coverage ≥ ~85% on core loop/tools/guardrails. `docker run` executes a fake-provider task end to end. README shows a real recorded run.

### 8. Testing strategy

- **The LLM boundary is mocked, deterministically.** A `FakeProvider` yields a *scripted sequence* of normalized responses (tool_call → tool_call → final). Loop tests run offline and assert: tools executed in order, results fed back correctly, stop conditions honored, trace emitted.
- **Adapter tests use recorded wire fixtures.** Save sanitized real Anthropic and OpenAI JSON responses once; test parse-in and serialize-out against them — proving provider parity without spending tokens.
- **Tool handler tests use `tmp_path`.** Real throwaway dir. Cover happy path + every guardrail: traversal (`..`, absolute, URL-encoded), symlink escape, oversized-output truncation, timeout + process-group kill, denied command, patch dry-run failure, backup/restore.
- **Golden-trace tests.** Run a fake-provider task; assert the emitted JSONL matches an expected structure (normalize timestamps/ids).
- **Property/edge tests.** Malformed OpenAI `arguments`, empty tool result, multiple parallel tool calls in one response, model that never stops (→ `max_steps`).
- **Factories/fixtures.** Builder helpers for `RunConfig`, normalized messages, tool specs.
- **Gated live integration test.** One `@pytest.mark.integration` test (skipped unless `RUN_LIVE=1`) hits a real cheap model (`claude-haiku-4-5`) with a trivial task, to catch SDK/schema drift. Never in default CI.

### 9. Deployment / ops

- **Local run:** `uv sync`; console-script entrypoint so `agent` is on PATH. Config precedence: **CLI flags > env vars > `.agent.toml` > defaults.**
- **Secrets:** `ANTHROPIC_API_KEY` / `OPENAI_API_KEY` from env only; never written to trace/logs (redaction filter + a test that proves it).
- **Persistence:** traces to `./.agent/runs/<run_id>.jsonl`; optional SQLite index for `Run`/`Step`.
- **"Migrations":** no server DB in MVP; if you add SQLite for run history, version the schema and include a tiny migration step.
- **Docker:** multi-stage, non-root, `ripgrep` installed, `WORKDIR` a mounted repo, keys as env. `docker run --rm -v $PWD:/repo -e ANTHROPIC_API_KEY … agent run "…" --workdir /repo`.
- **CI:** matrix 3.11/3.12 → ruff → `mypy --strict` → pytest+coverage → a fake-provider smoke run. Live test excluded.

### 10. Ruby/Rails bridge

- **Provider protocol + adapters** ≈ ActiveJob queue adapters / ActiveRecord connection adapters — one interface, swappable backends, `Protocol`/ABC instead of duck typing.
- **Tool registry + Pydantic schemas** ≈ Grape params + strong params + ActiveModel/dry-validation — validation + JSON-schema generation in one.
- **Agent loop with stop conditions/retries** ≈ a state machine (AASM) plus Sidekiq's `retry`/`retry_on`/`sidekiq_retries_exhausted` — bounded retries, terminal states, idempotent side effects.
- **structlog trace** ≈ Lograge; `agent trace show` is your log viewer.
- **Guardrails (path jail, allowlist, confirmation)** ≈ strong params + Pundit + input sanitization; the sandbox is your "never trust input at the boundary" instinct applied to model output.
- **CLI (Typer)** ≈ Thor / rake. And crucially: this whole project is the **Python re-implementation of the MCP + function-calling server you already built.**

### 11. Senior signals & portfolio angle

- **LLM Trainer — Agent Function Call:** you built the tool-use loop *by hand*, on two providers, with correct history reconstruction and stop-condition control. Call this out first.
- **Senior Python Developer:** typed (`mypy --strict`), Pydantic-schema-driven, tested at the right seam (mock the LLM, not everything), CI'd, Dockerized, clean adapter/registry architecture.
- **LLM Evaluation & Repository Validation:** the structured, replayable trace *is* an eval artifact; the "self-heal failing test" workflow shows repository validation end to end and hands off to P6.
- **README must include:** the architecture diagram; a plain-English walkthrough of the tool-use loop and the provider-normalization seam (with the shape table); the security/guardrail model; a recorded demo (the agent making a real failing test pass); a "design decisions & trade-offs" section (why a manual loop over a framework); and one sentence connecting it to your MCP/OAuth background. Add a 30-second asciinema/GIF.

### 12. Common pitfalls

- **History reconstruction:** echo the assistant's tool-request turn *before* the tool results; every tool call needs a matching result. Anthropic wants all `tool_result`s in **one** user message; OpenAI wants **one `role:"tool"` message per call** — don't leak one provider's shape into the other.
- **OpenAI `arguments` is a JSON string and may be malformed** — parse defensively; on failure return an `is_error` tool result. Never `assert`/crash on model output.
- **No `max_steps` → infinite loop / runaway cost.** Enforce a hard step cap *and* a token/cost budget from day one.
- **Context-window blow-up** from a giant `read_file`/test log — truncate with a "[truncated N bytes]" note; test it.
- **Hung subprocess** — set timeouts and kill the **process group**; verify the child is actually dead.
- **Path traversal / symlink escape** — resolve to canonical paths and assert containment; cover `..`, absolute, symlinks, URL-encoded traversal.
- **Leaking API keys** into traces/logs — redact at the logging layer; test-grep the trace for the key.
- **Model ID drift** — centralize in a registry; use `claude-opus-4-8` (verified); verify OpenAI ids against the live endpoint.
- **Divergent stop-reason semantics** — normalize into your own enum.
- **Cost table staleness** — the shipped price table is a **snapshot with a date, not authoritative**; say so in the README.
- **Pydantic v1 vs v2** confusion; **mypy vs SDK types** at the boundary — type the normalized model strictly, quarantine provider typing in adapters.
- **Streaming too early** — keep MVP non-streaming.
- **Splitting tool results across turns** (Anthropic) — a subtle correctness bug; return them together.

---

# Project 6 — `eval-harness`: Mini SWE-bench-Style Evaluation Harness (Weeks 9–10, flagship)

*Folder: `llm/eval-harness/`*

> **FLAGSHIP / Portfolio Centerpiece.** You already built the agent side (MCP + OAuth + function-calling); this is the other half employers care about: taking a *candidate patch* and *objectively proving* whether it fixes a repo, in a hermetic, reproducible sandbox. This is the literal daily motion of a repo-validation / LLM-eval job. **Its `report.json` conforms to the `run`/`result` portion of the shared `contracts/` schema.**

### 1. Premise

`eval-harness` answers one question reliably: *"Does this patch actually fix this repo?"* You feed it a **task** — a Git repo URL, a base commit, a candidate patch (unified diff), and the test command — and it spins up an isolated Docker sandbox, checks out the exact commit, applies the patch, runs the suite under strict timeouts and resource limits, parses results, and emits a structured **verdict** (resolved / unresolved / error) with captured logs and artifacts. It ships a small curated dataset of real OSS Python repos so anyone can clone it and reproduce identical results. Users: ML/eval engineers grading model-generated code, CI-adjacent tooling teams, researchers benchmarking coding agents — exactly the people interviewing you.

### 2. Why it's senior-level

- **Hermetic isolation & security.** You execute untrusted patches and test code — containers with dropped capabilities, no host secrets mounted, network egress control, non-root execution, cleanup guarantees even on crash.
- **Resource governance & failure taxonomy.** Wall-clock timeouts, CPU/memory limits, OOM detection, disk quotas, and the hard part: distinguishing *"tests failed"* (a legitimate result) from *"the harness broke"* (an infrastructure error). Never conflate them.
- **Reproducibility as a first-class feature.** Same task in → same verdict out, on your machine and a stranger's. Pinned base images, **pinned dependency resolution** (see the fix below), deterministic parsing, content-addressed task IDs.
- **Parsing hostile, heterogeneous output.** Reliably extract per-test PASS/FAIL/ERROR/SKIP without being fooled by output that *prints* "PASSED."
- **Concurrency & backpressure (stretch).** N sandboxes in parallel without exhausting the host.
- **Observability.** Structured logs, captured stdout/stderr artifacts, timing breakdowns, a machine-readable report schema.
- **Operational polish.** A clean CLI with good exit codes, a stellar README, graceful Ctrl-C, no orphaned containers/volumes.

### 3. Feature set

> **Scope trims (applied):** curate **2–3 tiny tasks, not 3–5**; lead with **JUnit-XML parsing only** (drop the fragile summary-regex parser to stretch — XML also makes the "prints '1 passed' but actually failed" adversarial test trivial); pick the **`docker` CLI via subprocess over the SDK** for MVP (SDK is a refinement, cutting SDK-learning overhead).

> **OOM fix (applied):** your platform is **darwin**; Docker Desktop's Linux VM reports memory limits / OOM-kills differently from native Linux cgroups, so "reports `ERROR (oom)`" may be flaky/unobservable on your Mac. Make **OOM detection best-effort in MVP, verified in CI on a Linux runner, with the macOS caveat documented.** The wall-clock **timeout** criterion stays MVP (reliably verifiable everywhere).

> **Reproducibility fix (applied):** pinning the base image digest is not enough if OSS repos resolve transitive deps differently over time. **Each curated task must vendor a lockfile** (or the harness snapshots the resolved dependency set into the report). Say so in the reproducibility statement.

#### MVP (must-build)

- **Task spec model**: repo URL, base commit SHA, patch (unified diff), test command, and the success sub-selection (`FAIL_TO_PASS` — tests that should flip failing→passing; `PASS_TO_PASS` — tests that must stay green). **Plus a vendored lockfile (or a snapshot mechanism) per task.**
- **Dataset loader**: read a directory or YAML/JSON file of tasks; validate each with a schema; assign a stable content-hashed `task_id`.
- **Docker sandbox lifecycle** (via `docker` CLI subprocess): pull the digest-pinned base image, create a container per run, copy the repo in (or clone inside), run commands, tear everything down — always, even on failure/interrupt.
- **Deterministic environment setup**: clone → hard checkout base commit → clean tree → install deps **from the vendored lockfile** → apply patch (fail loudly if it doesn't apply).
- **Test execution under limits**: run the command with a wall-clock timeout, a memory cap, and a CPU cap; capture stdout, stderr, and exit code separately.
- **Result parsing**: parse **pytest JUnit XML** into per-test statuses; compute the verdict from `FAIL_TO_PASS`/`PASS_TO_PASS` semantics.
- **Verdict + report**: `RESOLVED` (all FAIL_TO_PASS now pass AND all PASS_TO_PASS still pass), `UNRESOLVED` (patch applied and tests ran but criteria unmet), `ERROR` (patch didn't apply, setup failed, timeout, OOM, container error). Emit a JSON report (shared-contract-conformant) + human-readable summary.
- **Artifacts**: per-run logs + raw report under `runs/<task_id>/<run_id>/`.
- **CLI**: `run` a single task, `run` a dataset, `show` a past run, `list` tasks. Sensible exit codes.
- **Reproducibility**: pinned base image **digest**, vendored lockfiles, and the same task producing the same verdict across machines.
- **Excellent README**: quickstart, architecture diagram, verdict taxonomy, how to add a task, reproducibility notes (including the dependency-pinning story).

#### STRETCH (senior bonus)

- **Summary-line regex parser** as a fallback where JUnit XML isn't available.
- **`docker` Python SDK** in place of CLI subprocess (typed control of limits/lifecycle).
- **Thin FastAPI service**: `POST /runs`, `GET /runs/{id}` — reusing P4 muscle.
- **Parallel runs**: a bounded worker pool (`--workers N`), per-run container/temp isolation, aggregate `resolved_rate`.
- **Multi-runner support**: unittest and tox parsers behind the same interface.
- **Image caching / layer reuse**: pre-built per-repo images.
- **Golden patches & regression suite**: known-good/known-bad patches per repo, asserted in CI (test the tester).
- **Cost/timing telemetry** per phase; run comparison / leaderboard; OpenTelemetry spans.

### 4. Architecture & data model

**Entities:**

- **Task** — the immutable unit: `task_id` (content hash), `repo_url`, `base_commit`, `patch`, `env_setup` (install commands referencing the vendored lockfile), `test_command`, `fail_to_pass`, `pass_to_pass`, optional `timeout_s`, `mem_limit`, `cpu_limit`, `lockfile_ref`. Belongs to a **Dataset**.
- **Dataset** — a named collection of Tasks (YAML/JSON file or directory), versioned.
- **Run** — one execution: `run_id`, `task_id`, `started_at`, `finished_at`, `status` (verdict), `phase_timings`, `image_digest`, `resolved_deps_snapshot`, `harness_version`, artifact paths. A Task has many Runs.
- **TestResult** — parsed per-test outcome: `node_id`, `outcome` (passed/failed/error/skipped).
- **Report** — the computed verdict object: verdict enum, which FAIL_TO_PASS passed, which PASS_TO_PASS regressed, error subcategory if any, raw counts. Conforms to the shared `run`/`result` shape.

**Relationships:**

```
Dataset 1──*  Task 1──*  Run 1──*  TestResult
                          Run 1──1  Report
```

**Key flow (single run):**

```
┌──────────┐   ┌───────────────┐   ┌──────────────────────────────┐
│  CLI /   │──▶│ Task loader + │──▶│         Orchestrator          │
│  API     │   │  validation   │   │  (owns the run lifecycle)     │
└──────────┘   └───────────────┘   └───────────────┬──────────────┘
                                                     │
              ┌──────────────────────────────────────▼───────────────┐
              │                 Sandbox (Docker)                      │
              │  1 clone repo   2 checkout base_commit   3 clean tree │
              │  4 install deps (lockfile)  5 apply patch (fail→ERROR)│
              │  6 run test_command under timeout+mem+cpu limits      │
              │     capture stdout/stderr/exit-code + JUnit XML        │
              └───────────────────────────┬──────────────────────────┘
                                          │ raw logs + junit.xml
                              ┌───────────▼───────────┐
                              │  JUnit-XML parser      │──▶ TestResult[]
                              └───────────┬───────────┘
                                          │
                              ┌───────────▼───────────┐
                              │  Verdict computer      │──▶ Report (RESOLVED/…)
                              └───────────┬───────────┘
                                          │
                              ┌───────────▼───────────┐
                              │ Artifact writer:       │
                              │ runs/<task>/<run>/…    │
                              └───────────────────────┘
```

**Design boundaries (clean seams):**

- **Sandbox interface** — a `Sandbox` protocol (`setup`, `exec(cmd, timeout, limits) -> (stdout, stderr, exit_code, killed_reason)`, `copy_in`, `teardown`). The Docker-CLI implementation lives behind it; a fast "local/subprocess" fake enables no-Docker unit tests (never for untrusted code).
- **Parser interface** — `parse(raw_output) -> list[TestResult]`, JUnit-XML implementation first; unittest/tox and the summary-regex fallback as stretch.
- **Orchestrator** — a pure-ish coordinator that calls Sandbox + Parser + Verdict; owns the error taxonomy and guarantees teardown (context manager / `try/finally`).
- **Persistence** — MVP is the filesystem (`runs/…` JSON). Stretch adds SQLite (SQLModel) so the API can query runs.

**External integrations:** Docker daemon (via the `docker` CLI), Git (clone/checkout inside the container), the repos' own package managers (pip/uv) inside the container.

### 5. Tech & libraries

| Tool / Library | Role | Why |
|---|---|---|
| **Python 3.12 + uv** | Project + deps | Consistent; fast, lockfile-based, reproducible. |
| **Docker** (Engine) | Sandbox isolation | Industry-standard hermetic, resource-limited execution of untrusted code. |
| **`docker` CLI via subprocess** | Container control (MVP) | Simpler, mirrors how SWE-bench shells out; cuts SDK-learning overhead. SDK is a stretch refinement. |
| **Pydantic v2** | Task/Report schemas | Strict validation of untrusted task specs; clean report serialization. |
| **Typer** (or Click) | CLI | Ergonomic subcommands, typed args, good exit codes. |
| **Rich** | CLI output | Readable summaries, colored verdicts, parallel-run progress. |
| **structlog** | Structured logs | Machine-parseable phase logs. |
| **pytest + pytest-mock** | Your own test suite | Test the harness; mock the Docker layer. |
| **pytest JUnit-XML export** | Result source *inside* tasks | The robust status source (MVP parses this only). |
| **PyYAML** | Dataset files | Human-friendly task definitions. |
| **mypy (strict)** | Type safety | Protocols make the seams provable. |
| **ruff** | Lint/format | Fast, standard. |
| **tenacity** (optional) | Retries on flaky infra ops (image pull, clone) | Distinguish transient infra failure from real failure. |
| **FastAPI + uvicorn** (stretch) | Thin API | Reuse P4 skills. |
| **SQLModel / SQLite** (stretch) | Run persistence for API | Lightweight, queryable history. |

> **Reproducibility note to bake in:** pin the base image by **digest** (`python@sha256:…`, not `:3.12`); **vendor a lockfile per task** (or snapshot the resolved dependency set); record `image_digest`, `resolved_deps_snapshot`, and `harness_version` in every Report. Without the lockfile, the "reproducible" claim is false within weeks.

### 6. Milestone breakdown

~14–16 working days at 3–4 hrs/day (Weeks 9–10). MVP is M1–M7; 8–9 are stretch.

> **Risk-buffer note (applied):** **M2 (Docker lifecycle) and M4 (resource limits/timeouts) hide multi-day yak-shaves** on macOS Docker. Give each an explicit buffer.

- **M1 — Skeleton & task model (1.5 days).** `uv` project, ruff/mypy config, package layout. **Task**, **Dataset**, **Report**, **TestResult** Pydantic models. Content-hash `task_id`. Loader that reads + validates a YAML dataset (including `lockfile_ref`).
- **M2 — Sandbox abstraction + Docker lifecycle (2.5 days + buffer).** The `Sandbox` protocol. Docker-CLI implementation: create container from the digest-pinned image, `exec` capturing stdout/stderr/exit-code, guaranteed teardown via context manager. Prove no orphaned containers after success, failure, or Ctrl-C.
- **M3 — Repo setup & patch application (2 days).** Inside the sandbox: clone → hard checkout `base_commit` → clean tree → `env_setup` install **from the lockfile**. Apply the diff; if it doesn't apply, produce `ERROR (patch_failed)` rather than crashing.
- **M4 — Resource limits & timeouts (1.5 days + buffer).** Wall-clock timeout that kills the **container**; memory limit; CPU limit. Classify: `TIMEOUT`, `OOM` (best-effort; verify in Linux CI), generic non-zero exit. A killed run is `ERROR`, not `UNRESOLVED`.
- **M5 — Result parsing & verdict engine (2 days).** Parse **JUnit XML** into `TestResult[]`. Verdict: `RESOLVED` iff every `FAIL_TO_PASS` passes and every `PASS_TO_PASS` still passes; else `UNRESOLVED`; setup/infra problems → `ERROR` with a subcategory.
- **M6 — Orchestrator, artifacts & CLI (2 days).** Wire loader→sandbox→parser→verdict. Persist `runs/<task_id>/<run_id>/` with logs, raw output, `report.json`. Typer CLI: `run <task|dataset>`, `list`, `show <run_id>`; Rich summary; meaningful exit codes.
- **M7 — Dataset of real repos, reproducibility & README (2 days).** Curate **2–3** tiny OSS Python tasks (fast suites), each with a known patch **and a vendored lockfile**. Verify same-verdict reproducibility across a fresh clone. Write the flagship README.
- **M8 — STRETCH: parallel runs (1.5 days).** Bounded worker pool (`--workers N`), per-run container/temp isolation, aggregate `resolved_rate`.
- **M9 — STRETCH: thin API + persistence (1.5 days).** FastAPI `POST /runs` / `GET /runs/{id}`, SQLite-backed history, background execution. Plus the summary-regex parser and `docker` SDK refinements.

### 7. Acceptance criteria (self-verifiable)

- **M1** — `mypy --strict` clean. A valid dataset loads to typed Task objects; an invalid one (missing `base_commit`, malformed diff, missing `lockfile_ref`) raises a clear validation error. The same task file always yields the same `task_id`; changing any field changes it.
- **M2** — After a successful run, a failed run, and a `Ctrl-C` mid-run, `docker ps -a` shows **zero** leftover harness containers (verify by name prefix). `exec` returns distinct stdout, stderr, and exit code for a command that writes to both and exits non-zero.
- **M3** — A cleanly-applying patch proceeds to tests; a corrupted patch yields `ERROR (patch_failed)` with an explaining log — no traceback leaks. Re-running gives the identical outcome (clean tree each time). Deps install from the vendored lockfile, not the latest resolution.
- **M4** — An infinite-loop test command is killed at the timeout and reported `ERROR (timeout)`; total wall time is within a few seconds of the limit. **OOM detection is best-effort: verified on a Linux CI runner; the README documents that OOM classification may not be observable under Docker Desktop on macOS.**
- **M5** — Given a captured JUnit-XML fixture, the parser returns the right passed/failed/skipped counts and correct per-node outcomes. A crafted test that *prints* "1 passed" but actually fails is still parsed as failed (you read the XML, not stdout). A patch that fixes FAIL_TO_PASS but breaks a PASS_TO_PASS test is `UNRESOLVED`, and the report names the regressed test.
- **M6** — `eval-harness run <dataset>` exits `0` when all tasks resolve, non-zero otherwise; `show <run_id>` reprints a prior verdict from disk without re-running. Every run leaves a complete `report.json` matching the Report schema (validate by re-loading with Pydantic).
- **M7** — A teammate (or you, in a clean clone with only Docker + uv) runs the quickstart and reproduces the documented verdicts for all dataset tasks. README contains: architecture diagram, the full verdict/error taxonomy, add-a-task instructions, and the reproducibility statement (pinned image digest **and** vendored lockfiles present in reports).
- **M8 (stretch)** — `--workers 4` over an 8-task dataset completes faster than serial, produces identical per-task verdicts, and shows no container-name collisions or shared-temp contamination. Peak container count never exceeds `N`.
- **M9 (stretch)** — `POST /runs` returns a run id immediately; `GET /runs/{id}` transitions `queued → running → done` and returns the same verdict the CLI would. OpenAPI docs render. Restarting the API preserves run history (SQLite).

### 8. Testing strategy

- **Layer tests by trust boundary.** A fast **fake Sandbox** behind the `Sandbox` protocol lets the orchestrator, parser, and verdict engine be unit-tested with **no Docker at all** (milliseconds, CI everywhere). Reserve real-Docker tests for a marked, opt-in integration suite.
- **Parser tests from fixtures.** Capture real JUnit XML from your dataset repos once; assert exact parsed results. Include adversarial fixtures (misleading pass/fail strings in test output; empty output; a crashed interpreter).
- **Verdict truth table.** Parametrized cases covering the matrix (all FAIL_TO_PASS pass / some don't; all PASS_TO_PASS hold / one regresses; empty lists; setup error) → exactly one verdict + subcategory.
- **Factories/fixtures for Tasks.** A small builder producing valid Task objects with overridable fields.
- **Lifecycle/teardown tests.** Assert the context manager tears down even when the body raises (spy on the fake sandbox's `teardown`).
- **Integration tests (`@pytest.mark.docker`).** Against the curated dataset: known-good patch → `RESOLVED`; known-bad → `UNRESOLVED`; broken → `ERROR`. These are your **golden tests** and the strongest correctness proof.
- **Timeout/OOM tests.** Deterministic hanging/over-allocating tasks; assert the correct error subcategory and bounded wall time. **OOM assertion runs in Linux CI only.**
- **Type + lint gates.** `mypy --strict` + `ruff` in CI.
- **Idempotency/reproducibility test.** Run the same task twice; assert identical verdict and parsed counts.

### 9. Deployment / ops

- **Runs locally with Docker.** Prereqs: Docker Engine + `uv`. Quickstart: `uv sync`, then `eval-harness run datasets/starter.yaml`.
- **Config & secrets.** No secrets required for public OSS repos (keep it that way). Config (default timeout, mem/cpu caps, base image digest, runs dir) via a typed Pydantic Settings object from env / `.env`. Never mount host secrets into task containers — document this as a deliberate security choice.
- **Base image pinning.** Ship a documented base image referenced by **digest**; README explains how to rebuild/repin. **Vendored lockfiles per task are part of the reproducibility contract.**
- **Artifacts & retention.** `runs/` is the on-disk record; document a `--keep`/cleanup policy and that artifacts are safe to delete.
- **CI (GitHub Actions).** Two jobs: (1) fast — lint + mypy + no-Docker unit tests on every push; (2) integration — the `@pytest.mark.docker` golden tests **on a Linux runner** (they also verify OOM classification). Cache the base image / uv resolution.
- **Migrations (stretch API).** If you add SQLite via SQLModel, include a tiny init/migration step; keep the schema versioned in the Report.
- **Graceful shutdown.** Trap SIGINT/SIGTERM → tear down live containers → non-zero exit. Document that no orphaned resources remain.

### 10. Ruby/Rails bridge

- **Docker sandbox ≈ a hermetic RSpec+DB run in CI.** You already isolate specs with a clean DB and `DatabaseCleaner`/transactional fixtures; here "clean state" is a fresh container + hard-checked-out commit + reset tree — same instinct, stronger boundary (a whole OS, not just a DB transaction).
- **Task/Report Pydantic models ≈ ActiveModel + strong params / a serializer.** Validating an untrusted task spec is Rails strong-params + model validations; the Report is your serializer / Grape entity — a typed, versioned response contract.
- **Verdict taxonomy ≈ deliberate exit codes + `rescue_from`.** "Tests failed" is a valid *result*; "the harness broke" is an *error* — never a 500-dressed-as-404, the same discipline you use separating `RecordNotFound` from a `500`.
- **Sandbox/Parser protocols ≈ Ruby duck typing made explicit** — your interfaces with a fake for tests are the typed cousin of injecting a test double, now enforced by mypy.

### 11. Senior signals & portfolio angle

This is the project that makes an interviewer for **LLM Evaluation / Repository Validation** and **Agent Function-call** roles lean in — SWE-bench in miniature, their actual product. Lead the README with:

- **"I understand evaluation correctness, not just execution."** The FAIL_TO_PASS / PASS_TO_PASS semantics and the strict separation of *result* vs *infrastructure error* show you know why naive harnesses give garbage numbers. Put the verdict taxonomy near the top.
- **Security-first execution of untrusted code.** Non-root, dropped capabilities, resource caps, no host-secret exposure, guaranteed teardown. Say it explicitly.
- **Reproducibility engineering.** Digest-pinned images + **vendored lockfiles / snapshotted deps** + recorded harness version + deterministic JUnit-XML parsing → same verdict anywhere. This is exactly what repo-validation teams obsess over.
- **Clean seams + strict typing.** Protocol-based Sandbox/Parser, `mypy --strict`, a fake-sandbox suite that runs without Docker.
- **Golden regression suite for the harness itself** (stretch-adjacent) — known-good/known-bad patches asserted in CI = you test the tester.
- **The through-line with your MCP work:** *"I built the agent side (MCP + OAuth + function-calling) and the evaluation side (this harness) — I can both run coding agents and objectively grade them."* A rare, hire-worthy combination for all three roles.

In the README, include: architecture diagram, the verdict/error taxonomy table, a 60-second quickstart with real output, an "add a task in 5 minutes" guide, the reproducibility statement (with the dependency-pinning story), and a short "security model" section.

### 12. Common pitfalls

- **Conflating "tests failed" with "harness failed."** A non-applying patch, a timeout, or an OOM is `ERROR`, never `UNRESOLVED`. Bake this into the verdict engine and test it.
- **Parsing stdout naively.** Prefer JUnit XML over regexing human summaries; add adversarial parser fixtures.
- **Orphaned containers/volumes.** Context manager + `try/finally`; a test that forces an exception mid-run and asserts cleanup.
- **Non-reproducible base image.** Pin by digest and record it in every report.
- **Unpinned transitive dependencies.** The base-image pin is necessary but insufficient — **vendor a lockfile per task** (or snapshot resolved deps into the report), or the "reproducible" claim is false within weeks.
- **Dirty working tree between runs.** Start each run from a pristine tree (fresh clone or `git reset --hard && git clean -fdx`).
- **Timeout that doesn't actually kill the container.** Ensure the timeout tears down the *container*; verify wall time is bounded.
- **Assuming OOM classification works the same on macOS.** Docker Desktop's Linux VM reports OOM differently; make it best-effort, verify in Linux CI, document the caveat.
- **Choosing heavy dataset repos.** Curate 2–3 small, fast, well-behaved OSS Python repos.
- **Over-scoping the API/parallelism before MVP is solid.** M1–M7 is a complete, shippable product.
- **Running untrusted code without network/privilege limits.** Set the security posture early — it's a selling point.
- **Silent dependency-install failures.** A non-zero setup step is `ERROR (setup_failed)`; capture its log.

**File location (absolute):** `/Users/ravikumar/Desktop/MyWorkspace/workspace/study/python_learning/llm/eval-harness/` with its own `pyproject.toml`, `README.md`, `datasets/` (each task vendoring a lockfile), `src/eval_harness/`, `tests/` (with a `@pytest.mark.docker` integration subset), and a `runs/` artifacts directory.

---

## Closing note on shipping

Build in priority order under time pressure: **P6 and P5 are non-negotiable**, **P1** is the cheap foundation and the home of the shared `contracts/`, and the web-framework slots (**P2 Flask, then P4's OpenAI adapter**) are the designated swing items. Ship every project's MVP before touching any stretch. If week 8 arrives and P6 hasn't started, cut P2 entirely and fold its HMAC + idempotency signals into P4's stretch webhook endpoint — that keeps the flagship on schedule while preserving the security signal. Name your tradeoffs in every README: that is the loudest senior signal in the whole portfolio.
