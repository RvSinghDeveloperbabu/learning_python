# llm/agent-cli/ — function-calling agent  (Weeks 11–12)

**Premise:** a provider-agnostic command-line **agent** that *acts* on repositories under guardrails, using real tools. It implements the full tool-use loop by hand — define JSON-schema tools → the model requests a call → I execute it → feed the result back → loop — with proper stop conditions.

**Proves:** the exact skill behind the LLM-Trainer / Agent-Function-Call role, in Python — and it's my differentiator (I already built an MCP + function-calling system; this shows it in Python). Message-history reconstruction, tool schemas, agent-loop control, and safety.

**MVP (must-build):**
- 2–3 genuinely useful tools (e.g. `read_file`, `search_code`, `run_tests`/`run_shell` sandboxed)
- the complete tool-use loop across **both** providers (Anthropic + OpenAI)
- agent loop with stop conditions + max-steps
- structured decision **trace/logging**; guardrails (tool-input validation, timeouts, no destructive ops); **secret redaction** in logs
- pytest incl. a mocked model driving the loop

**Cut line:** `apply_patch` is the internal thing to drop first if time is tight.

**Reuse note:** the normalized message/response model is shared learning with `fastapi-app/` — build it once, reuse it here. This agent's subprocess sandbox is a *different* isolation model from the eval-harness's Docker sandbox — reuse instinct, not code.

**I scaffold this myself** (`uv init`, structure). Mentor guides, doesn't author.

➡️ Full spec: [`../../docs/02-real-world-projects.md`](../../docs/02-real-world-projects.md) · Curriculum: [`../../docs/05-curriculum-llm-and-flagship.md`](../../docs/05-curriculum-llm-and-flagship.md)
