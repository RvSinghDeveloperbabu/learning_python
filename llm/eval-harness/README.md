# llm/eval-harness/ — SWE-bench in miniature  (Weeks 9–10 · FLAGSHIP)

**Premise:** given a task spec (repo URL, base commit, a candidate code patch, and the test command), spin up a **Docker sandbox**, check out the repo, apply the patch, run the repo's test suite in isolation (with timeouts + resource limits), parse the results, and report **pass/fail with captured logs and artifacts**. This is SWE-bench in miniature — the exact daily motion of the repo-validation job.

**Proves:** the LLM-Evaluation / Repository-Validation role directly — hermetic sandboxing, running and testing *other people's* code, a rigorous result-vs-error taxonomy, and reproducibility. **This is the portfolio centerpiece; it gets an excellent README.**

**MVP (must-build):**
- a task-spec format (repo, base commit, patch, test command)
- Docker sandbox lifecycle: checkout → apply patch → run tests, isolated, with timeouts + resource limits
- result parsing → `report.json` conforming to [`../../contracts/`](../../contracts/) + captured logs
- a small task dataset (a few real OSS Python repos)
- reproducibility (same input ⇒ same verdict); clean CLI
- clear taxonomy: patch-fails-to-apply vs. tests-fail vs. tests-pass vs. harness-error

**Stretch:** a thin API; parallel runs.

**Note:** this Docker sandbox is a *different, stronger* isolation model than `agent-cli`'s in-process subprocess jail — don't rebuild that container lifecycle inside the agent.

**I scaffold this myself** (`uv init`, structure, Dockerfile). Mentor guides, doesn't author.

➡️ Full spec: [`../../docs/02-real-world-projects.md`](../../docs/02-real-world-projects.md) · Curriculum: [`../../docs/05-curriculum-weeks-5-8.md`](../../docs/05-curriculum-weeks-5-8.md)
