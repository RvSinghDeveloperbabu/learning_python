# foundations/ — `evalctl`  (Weeks 4–5)

**Premise:** a typed command-line tool that ingests eval datasets and run logs (JSONL), validates them against a schema, filters/aggregates, computes metrics (pass rate, latency p50/p95, cost), and exports human + machine reports. This is my "think in Python" project and the data layer the rest of the platform consumes.

**Proves:** idiomatic, type-hinted Python; `mypy --strict`; dataclasses; pathlib/json; **generators** for streaming large files; a real `pytest` suite; robust error handling; a clean CLI (argparse or Typer).

**Also produces:** the shared, versioned JSON schemas in [`../contracts/`](../contracts/) (test-case / run / result) that Flask, Django, FastAPI, and the eval-harness all conform to.

**MVP (must-build) — see full spec for acceptance criteria:**
- load + validate JSONL against the schema; clear errors on malformed rows
- filter/aggregate; compute pass rate, latency p50/p95, cost
- stream large logs without loading everything into memory (generators)
- human-readable + JSON report output
- type-hinted throughout, `mypy` clean, pytest suite (incl. empty-input & malformed-JSON cases)

**I scaffold this myself** as milestone 1: `uv init` here, set up `pyproject.toml`, package layout, and tooling. The mentor describes what belongs where — it does not write it.

➡️ Full spec (architecture, milestones, testing, pitfalls): [`../docs/02-real-world-projects.md`](../docs/02-real-world-projects.md) · Curriculum: [`../docs/04-curriculum-core-python-and-web.md`](../docs/04-curriculum-core-python-and-web.md)
