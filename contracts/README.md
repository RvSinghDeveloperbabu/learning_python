# contracts/ — shared versioned wire schemas

The single source of truth for the platform's domain shapes. I define these in **`foundations/` (Weeks 4–5)** and every other service conforms to them — this is what turns six projects that *rhyme* into **one platform with a versioned wire contract**.

**What lives here:**
- JSON Schema files for `test-case`, `run`, and `result`
- each carries an explicit **`schema_version`**
- a short, human-readable **CHANGELOG** describing each version bump and its migration

**Who consumes it:**
- `flask-app/` validates inbound webhook payloads against it
- `django-app/` serializes its models to/from these shapes
- `fastapi-app/` accepts submissions and emits result items in this shape
- `llm/eval-harness/` emits `report.json` conforming to the `run`/`result` portion

**Rule:** bump `schema_version` when a field changes and document the migration. Being able to talk about *schema evolution across services* is a senior signal reviewers reward.

**I author these schemas myself** (they're a learning deliverable — see CLAUDE.md §2). The mentor describes the modeling decisions in English; I write the JSON.

➡️ Details in [`../docs/02-real-world-projects.md`](../docs/02-real-world-projects.md) (see "Shared versioned data contract").
