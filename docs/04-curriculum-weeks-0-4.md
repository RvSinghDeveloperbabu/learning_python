# Weeks 0-4: Concrete Daily Curriculum (Ravi)

**How to read this:** Each day is ~3-4 hrs, split roughly **30% READ / 70% BUILD**. You type every line of Python; acceptance criteria are things *you* can verify (mypy/pytest/output) so you know you're done before I review. "Watch-outs" are the Ruby-brain traps for that exact topic. The "senior signal" is the one sentence that tells an interviewer you actually own the concept.

Standing rule for every BUILD from Week 1 on: run it with `uv run`, keep it under version control, and before you call it done run `ruff check`, `mypy --strict`, and `pytest`.

---

## WEEK 0 — Environment + Apply (3 days)
**GitHub deliverable:** a repo with a working, reproducible Python env (pyproject + lockfile) and a committed README. **Also:** 1 job application submitted (LLM Trainer).

### Day 1 — Python 3.12+ via uv, the venv model
- **Focus:** uv as your version + env + dependency manager; how Python isolation actually works.
- **READ:** uv docs — "Getting started" + "Projects" + "Python versions" (`docs.astral.sh/uv/`). Skim Real Python "Python Virtual Environments: A Primer."
- **BUILD:** Init a uv project in the repo, pin Python to 3.12+ (you have 3.14 and 3.11 installed — force 3.12+ explicitly), create the venv, add one real dependency (e.g. `httpx` or `rich`), and write a tiny script that imports it and prints its version.
- **Acceptance:**
  - `uv run python --version` prints 3.12.x or higher (NOT 3.11).
  - `pyproject.toml` + `uv.lock` both exist and are committed.
  - Deleting `.venv` and running `uv sync` fully rebuilds a working env.
  - Your script runs via `uv run` and imports the installed package.
- **Ruby→Python watch-outs:** uv ≈ `rbenv` + `bundler` + `gem` fused into one tool. `pyproject.toml` ≈ `Gemfile` + `.gemspec`; `uv.lock` ≈ `Gemfile.lock`. There is no global "just works" load path like RubyGems — code outside the active venv can't see your deps. `uv run X` ≈ `bundle exec X`.
- **Senior signal:** You can explain why a locked, per-project venv makes builds reproducible and how uv resolves/pins versions — not just "I ran the installer."

### Day 2 — VS Code + Pylance + mypy + ruff, project hygiene
- **Focus:** editor type-checking, linting/formatting, repo layout.
- **READ:** Pylance/Python VS Code docs (type checking mode); ruff docs "Configuration"; mypy docs "Getting started."
- **BUILD:** Configure VS Code with Pylance in **strict/basic type-check mode**, add ruff + mypy as dev dependencies, add their config to `pyproject.toml`, and lay out a clean `src/`-style package with a `tests/` folder. Write a 3-line typed hello module.
- **Acceptance:**
  - Pylance shows type errors live in the editor (introduce a deliberate type mismatch and watch it flag, then fix).
  - `mypy --strict` runs clean on your hello module.
  - `ruff check` and `ruff format` run clean.
  - `.gitignore` excludes `.venv`, `__pycache__`, etc.; repo is pushed to GitHub.
- **Ruby→Python watch-outs:** ruff ≈ RuboCop (but 100x faster and also a formatter). mypy has no Ruby equivalent you've used daily — treat it as a compiler you'll run constantly. Package = a directory Python can import; unlike Rails autoloading, imports are explicit and path-sensitive.
- **Senior signal:** Your repo is CI-ready on day one (lint + typecheck + test config all declared in `pyproject.toml`).

### Day 3 — Ruby→Python orientation + APPLY
- **Focus:** mental model reset; get the first application out.
- **READ:** Real Python "Python vs Ruby" style comparison + the official Python tutorial §1-3 (skim, don't grind). Re-read the LLM Trainer job post.
- **BUILD:** Write the repo README (what the project is, how to set it up with uv, how to run tests). Draft and **submit** the LLM Trainer application — lead with your MCP server + OAuth + function-calling work.
- **Acceptance:** README renders correctly on GitHub with copy-pasteable setup steps; application submitted; note where/when you applied in a `notes.md` or the README.
- **Ruby→Python watch-outs:** Resist translating Ruby line-by-line this week; you're calibrating, not coding yet.
- **Senior signal:** You frame your MCP/function-calling experience as *the* differentiator for LLM roles without prompting.

---

## WEEK 1 — Core language: think in Python (5 days)
**Feeds:** Weeks 1-2 GitHub deliverable — a typed, tested JSON/file-processor CLI. Days below build the skills; Week 2 assembles the tool.

### Day 1 — Syntax deltas: indentation, None/True/False, f-strings, truthiness
- **Focus:** everything that's different at the token level; **truthiness** especially.
- **READ:** Python tutorial §4 (control flow); Real Python "Python's f-strings"; Real Python "Truth Value Testing."
- **BUILD:** Take a small Ruby script you already have (or write one: FizzBuzz + a bit of string munging like titthe-casing words and stripping punctuation) and re-implement it in idiomatic Python — no line-by-line transliteration.
- **Acceptance:** Byte-identical output to the Ruby version on the same input; uses f-strings for all interpolation; passes ruff; no leftover Ruby-isms (see below).
- **Ruby→Python watch-outs:**
  - **Truthiness is the #1 trap:** Ruby treats only `nil`/`false` as falsy. Python treats `0`, `0.0`, `""`, `[]`, `{}`, `set()`, and `None` as falsy too. A check meaning "was a value provided?" behaves differently — you often want an explicit `is None` test.
  - `nil` → `None`; test with `is None`/`is not None`, never `== None`.
  - No `end`; a stray space/tab changes meaning. `elif`, not `elsif`.
  - Ruby's implicit last-expression return does NOT exist — you must write `return`.
  - Integer division: Ruby `/` on two ints floors; Python `/` always yields a float, `//` is floor division.
  - Ruby ranges are inclusive by default; Python `range(stop)` excludes `stop`.
- **Senior signal:** You can list Python's full set of falsy values from memory and explain why `if not x:` and `if x is None:` are different checks.

### Day 2 — Data structures: list / dict / set / tuple
- **Focus:** the four core containers, their methods, mutability, when to reach for each.
- **READ:** Python tutorial §5 (data structures); Real Python "Lists and Tuples" + "Dictionaries."
- **BUILD:** A word-frequency counter: read a text file, normalize (lowercase, strip punctuation), count words, return the top-N as an ordered structure.
- **Acceptance:**
  - Correct counts, case-insensitive.
  - Returns top-N sorted by count desc, then alphabetically for ties.
  - Handles an empty file and a file with only punctuation without crashing.
  - Uses a set somewhere meaningful (e.g. stop-words) and returns tuples (immutable) rather than mutable rows.
- **Ruby→Python watch-outs:** Array→list, Hash→dict; **there are no Symbols** — dict keys are just strings. `<<` → `list.append`. Missing-key access: Ruby returns `nil`; Python raises `KeyError` (use `dict.get` or `in`). `arr.include?` → `x in list`; `hash.key?` → `key in dict`. dicts preserve insertion order (since 3.7), like Ruby hashes. Tuples are frozen — no append.
- **Senior signal:** You choose set/dict/list/tuple by their complexity and mutability guarantees, not by habit, and can state why membership testing on a set beats a list.

### Day 3 — Comprehensions + generator expressions
- **Focus:** list/dict/set comprehensions and the lazy generator-expression variant.
- **READ:** Real Python "When to Use a List Comprehension" + "Introduction to Python Generators" (comprehension section).
- **BUILD:** Rewrite Day 2's loops as comprehensions where it genuinely reads better; add a dict comprehension that maps word→count, and a generator-expression path for counting a large file without loading it all into memory.
- **Acceptance:** Same output as Day 2; at least one list, one dict comprehension, and one generator expression used appropriately; you can articulate which one is lazy and why the big-file path stays memory-flat.
- **Ruby→Python watch-outs:** Ruby's `arr.map{...}` → list comprehension; `arr.select{...}` → comprehension with an `if`; `map` + `select` chains collapse into one comprehension. **Don't over-nest** — a triple-nested comprehension is worse than a loop. Generator expressions (round-bracket form) are single-use and lazy — iterating twice yields nothing the second time (a real gotcha coming from eager Ruby enumerables).
- **Senior signal:** You reach for a generator expression instead of a list comprehension when the result is consumed once, and can explain the memory difference.

### Day 4 — Type hints + mypy strict
- **Focus:** annotating real code; `list[int]`, `dict[str, X]`, `Optional`/`| None`, unions.
- **READ:** mypy "Type hints cheat sheet"; Python docs `typing` intro; Real Python "Python Type Checking."
- **BUILD:** Fully annotate your Day 2-3 code (function params, returns, and any module-level structures) and get it through `mypy --strict`.
- **Acceptance:**
  - `mypy --strict` passes with zero errors and zero `# type: ignore`.
  - No `Any` in your own signatures.
  - Uses builtin generics (`list[str]`, `dict[str, int]`) and expresses "maybe absent" with `X | None`.
- **Ruby→Python watch-outs:** Coming from Sorbet/RBS this is familiar, but note: hints are erased at runtime (no enforcement — mypy is a *static* check, like a compiler pass, not `raise` on bad types). `Optional[X]` is exactly `X | None`. A function that "returns nothing" is typed `-> None`. Don't type a mutable default as the container type without understanding Day 5's trap.
- **Senior signal:** You treat `mypy --strict` green as the baseline, and can explain that annotations are compile-time only with zero runtime cost.

### Day 5 — Functions: *args/**kwargs, defaults, keyword-only, unpacking
- **Focus:** flexible signatures and the mutable-default-argument trap.
- **READ:** Python tutorial §4.7-4.9 (defining functions, arbitrary arg lists, unpacking); Real Python "Python args and kwargs."
- **BUILD:** A small configurable aggregator: a function that takes an iterable of records plus optional flags (via keyword-only args) and returns a summary. Include one function that accepts `*args` and one that accepts `**kwargs`, and use `*`/`**` unpacking at a call site.
- **Acceptance:**
  - You deliberately demonstrate you understand the **mutable default argument** pitfall (your code must not accumulate state across calls).
  - At least one keyword-only parameter (after a bare `*`).
  - mypy --strict clean.
- **Ruby→Python watch-outs:**
  - **Mutable default args** are the classic Python-only bug: a default list/dict is created ONCE at definition time and shared across every call — the idiom is to default to `None` and build the container inside. Ruby evaluates defaults per-call, so this will bite you.
  - Ruby blocks/procs don't map cleanly — Python `lambda` is single-expression only; pass named functions for anything real.
  - `**kwargs` ≈ Ruby's trailing options hash; `*args` ≈ Ruby splat.
- **Senior signal:** Asked "why does this function 'remember' its last call's list?" you immediately name the mutable-default-arg trap and give the `None`-default fix.

**Week 1 interview check (no code):** (1) "Walk me through Python's truthiness — which values are falsy?" (2) "What does `mypy --strict` buy you, and what does it NOT enforce at runtime?"

---

## WEEK 2 — Idioms, stdlib, testing → ship the CLI (5 days)
**GitHub deliverable (end of Day 5):** the typed, pytest-covered JSON/file-processor CLI.

### Day 1 — collections + pathlib
- **Focus:** `Counter`, `defaultdict`, `namedtuple`; filesystem work with `pathlib`.
- **READ:** Python docs `collections` (Counter, defaultdict); Real Python "Python's pathlib Module."
- **BUILD:** Refactor the word counter to use `Counter` (and `most_common`) and rewrite any directory/file traversal using `pathlib` (glob a folder of `.txt`/`.json` files).
- **Acceptance:** `Counter.most_common(n)` replaces your hand-rolled top-N; a `defaultdict` used where it removes a "key exists?" check; all path handling via `pathlib` (no string concatenation of paths, no `os.path`).
- **Ruby→Python watch-outs:** `defaultdict` ≈ `Hash.new(0)` / `Hash.new{|h,k| h[k]=[]}`. `pathlib`'s `/` operator joins paths (don't build paths with `+` or f-strings). `Path.glob`/`rglob` ≈ `Dir.glob`. `Counter` has no direct Ruby stdlib twin — it's a dict subclass.
- **Senior signal:** You reach for `Counter`/`defaultdict` reflexively instead of manually initializing dict entries.

### Day 2 — dataclasses, datetime, json, enum
- **Focus:** modeling records as `@dataclass`; JSON round-tripping; `datetime` parsing; `Enum`.
- **READ:** Python docs `dataclasses` + `enum`; Real Python "Working With JSON Data in Python" + "Data Classes."
- **BUILD:** Define a `@dataclass` for a record (typed fields), parse a JSON file into a list of these, and emit a JSON summary. Use an `Enum` for a categorical field and parse an ISO timestamp into a `datetime`.
- **Acceptance:**
  - JSON in → dataclasses → JSON out round-trips without data loss.
  - Dataclass fields are fully type-hinted; use `frozen=True` where the record should be immutable.
  - Enum used for the category (invalid categories are rejected/handled).
  - mypy --strict clean.
- **Ruby→Python watch-outs:** `@dataclass` ≈ `Struct`/`attr_accessor` but with types and free `__init__`/`__repr__`/`__eq__`. `json.loads`/`dumps` ≈ `JSON.parse`/`JSON.generate` — but Python won't serialize a dataclass automatically (you convert to dict first). Datetimes aren't JSON-native; you format/parse ISO strings yourself. `Enum` members are singletons — compare with `is`.
- **Senior signal:** You default to dataclasses (or Pydantic later) for structured data instead of passing bare dicts around.

### Day 3 — Generators (`yield`) + itertools/functools
- **Focus:** lazy streaming with `yield`; composing with `itertools`; `functools` (cache, reduce, partial).
- **READ:** Real Python "How to Use Generators and yield"; Python docs `itertools` (islice, groupby, chain) + `functools` (lru_cache, reduce).
- **BUILD:** A generator function that streams records from a large file one at a time (never holding all in memory); use `itertools.groupby`/`islice` to batch or group them, and cache an expensive pure function with `functools`.
- **Acceptance:** The reader is a generator (uses `yield`); memory stays flat regardless of file size; `groupby` used correctly (remember it needs sorted input); `lru_cache` measurably avoids recomputation.
- **Ruby→Python watch-outs:** `yield` in Python is NOTHING like Ruby's `yield` (which calls a block). Python `yield` produces a lazy iterator — closer to Ruby `Enumerator`/`lazy`. A generator is exhausted after one pass. `itertools.groupby` only groups *consecutive* equal keys (sort first!) — unlike Ruby's `group_by` which buckets globally. `functools.reduce` ≈ Ruby `inject`/`reduce`.
- **Senior signal:** You explain generators as lazy, single-pass iterators and know `groupby` requires pre-sorted input.

### Day 4 — Context managers + decorators
- **Focus:** the `with` protocol (`__enter__`/`__exit__` and `@contextmanager`); writing decorators.
- **READ:** Real Python "Context Managers and Python's with Statement" + "Primer on Python Decorators"; Python docs `contextlib`.
- **BUILD:** (a) A custom context manager (via `contextlib.contextmanager`) that times a block or manages a resource with guaranteed cleanup. (b) A decorator (timing or simple retry) applied to one of your functions, using `functools.wraps`.
- **Acceptance:** The context manager releases the resource even when an exception is raised inside the `with`; the decorator preserves the wrapped function's name/docstring (`functools.wraps`); both are type-annotated and mypy-clean.
- **Ruby→Python watch-outs:** `with` ≈ Ruby's `File.open(...) do |f| ... end` block-with-cleanup pattern, generalized. Decorators ≈ Ruby method wrapping / `alias_method` / `prepend`, but as first-class `@decorator` syntax. Forgetting `functools.wraps` silently mangles introspection (a subtle senior tell). A decorator that takes arguments needs an extra layer of nesting — understand why.
- **Senior signal:** You can explain the `__enter__`/`__exit__` protocol and guarantee cleanup-on-exception without a `begin/ensure` mindset leaking through.

### Day 5 — pytest + assemble the CLI (DELIVERABLE)
- **Focus:** `argparse` CLI wiring; pytest fixtures, parametrize, `tmp_path`.
- **READ:** pytest docs "Get Started" + "Fixtures" + "Parametrizing"; Python docs `argparse` tutorial.
- **BUILD:** Assemble everything into one CLI (JSON/file processor): takes an input path + options, streams + aggregates records, prints/writes a report. Write a real pytest suite.
- **Acceptance:**
  - `pytest` green; suite uses at least one **fixture** and one **parametrize**, and `tmp_path` for filesystem tests.
  - Edge cases covered: empty input, malformed JSON line, missing file (exits with a clear non-zero code/message).
  - `mypy --strict` and `ruff check` clean.
  - CLI runs end-to-end via `uv run`; README documents usage; **pushed to GitHub**.
- **Ruby→Python watch-outs:** pytest ≈ RSpec but with plain `assert` (no `expect().to`) and no `describe/it` DSL — test functions named `test_*`. Fixtures ≈ `let`/`before` but composed by function arguments (dependency injection by name). `parametrize` ≈ RSpec shared examples / table tests. `argparse` ≈ your Grape/OptionParser instincts — but define args declaratively.
- **Senior signal:** Your tests read like a spec of behavior (fixtures + parametrized edge cases), and you assert on exit codes/errors, not just happy paths.

**Week 2 interview check:** (1) "Difference between a list comprehension and a generator expression — when does it matter?" (2) "How do pytest fixtures work and how are they different from just calling a setup function?"

---

## WEEK 3 — Django + DRF (the Rails analog) (5 days)
**GitHub deliverable (Day 5):** Django + DRF app with 2-3 related models and a working REST API.
**Framing:** Django Model = ActiveRecord, `manage.py migrate` = `rails db:migrate`, free admin ≈ better ActiveAdmin, QuerySets are lazy like AR relations. Biggest Rails-brain shift: **you don't write migrations by hand — `makemigrations` generates them from model changes.**

### Day 1 — Setup, project vs app, models, migrations
- **Focus:** `startproject` vs `startapp`, settings, defining models, migrate. Official polls tutorial parts 1-2.
- **READ:** Django tutorial 1 & 2 (`docs.djangoproject.com/.../intro/tutorial01/`).
- **BUILD:** `uv add django`, create a project + one app, define 2 related models (e.g. a parent/child like Author→Book or Question→Choice), run `makemigrations` + `migrate`, register models in admin.
- **Acceptance:** dev server runs; both models appear and are editable in `/admin`; migrations committed; a superuser created.
- **Ruby→Python watch-outs:** A Django "project" holds many "apps" (a Rails app ≈ a Django app; the project ≈ the Rails app shell). Migrations are auto-generated from model diffs — don't hand-edit unless you must. `null=True` (DB) vs `blank=True` (validation) are separate concepts. No `save!` bang convention — `save()` and validation are decoupled from the ORM by default.
- **Senior signal:** You can explain the project/app split and that migrations are derived from declarative model state.

### Day 2 — ORM: querysets, relationships, CRUD
- **Focus:** the Django shell, `filter`/`exclude`/`get`/`annotate`, FK/M2M traversal.
- **READ:** Django "Making queries" topic guide; QuerySet API reference (skim).
- **BUILD:** In `python manage.py shell`, create records and run queries: filter, exclude, order, related-object lookups (forward and reverse), and one aggregate/annotate. Add a `__str__` and a model method or two.
- **Acceptance:** You can create, query, update, and delete via the shell; reverse relations (`parent.children.all()`-style) work; at least one `annotate`/aggregate returns correct numbers.
- **Ruby→Python watch-outs:** QuerySets are **lazy** — they don't hit the DB until iterated/sliced (like AR relations); chaining builds SQL. `.get()` raises `DoesNotExist`/`MultipleObjectsReturned` (≈ `find` raising RecordNotFound). Reverse FK accessor default name is `<model>_set` unless you set `related_name`. `filter` ≈ `where`; `exclude` ≈ `where.not`.
- **Senior signal:** You know exactly when a QuerySet executes and can describe lazy evaluation without hand-waving.

### Day 3 — Views, URLs, templates, admin
- **Focus:** request→URL→view→template flow; admin customization. Polls tutorial 3-4 (+7 for admin).
- **READ:** Django tutorial 3, 4, and 7.
- **BUILD:** A list view and a detail view for your parent model, wired through `urls.py`, rendering minimal templates; customize the admin (list_display, filters).
- **Acceptance:** list and detail pages render real data; URL routing works including a path parameter; admin shows customized columns/filters.
- **Ruby→Python watch-outs:** URLconf ≈ `routes.rb` but explicit per-app and included into the project. Class-based views ≈ Rails controllers-with-conventions but more explicit; function views are fine to start. Template language is NOT ERB — restricted logic, `{{ }}`/`{% %}`. `render()` ≈ Rails `render`.
- **Senior signal:** You can trace a request end-to-end (URLconf → view → template/context) and explain where you'd put business logic.

### Day 4 — DRF: serializers, viewsets, routers
- **Focus:** turning models into a JSON API. This is the part that matters for the deliverable.
- **READ:** DRF tutorial (`www.django-rest-framework.org/tutorial/`) parts on Serializers, Requests/Responses, ViewSets & Routers.
- **BUILD:** `uv add djangorestframework`; write serializers for your 2-3 models, `ModelViewSet`s, and register them with a router. Expose list/detail/create/update/delete.
- **Acceptance:** the browsable API returns valid JSON for all models; you can create and update via the API; nested relationship is represented in the serializer; invalid payloads return 400 with field errors.
- **Ruby→Python watch-outs:** DRF serializers ≈ Grape Entities / ActiveModel::Serializers but they also *validate and deserialize* (two-way), closer to `StrongParameters` + serializer fused. `ModelViewSet` gives you the full CRUD set like a Rails resourceful controller. Routers ≈ `resources :things`.
- **Senior signal:** You distinguish serialization from validation and can explain how a `ModelViewSet` + router collapses boilerplate.

### Day 5 — N+1, select_related / prefetch_related (DELIVERABLE)
- **Focus:** query performance — your strongest existing instinct, mapped to Django.
- **READ:** Django "Database access optimization" + `select_related`/`prefetch_related` reference.
- **BUILD:** Instrument query counts (django-debug-toolbar or `assertNumQueries` in a test). Prove a nested serializer triggers N+1, then fix it with `select_related` (FK/one-to-one) and `prefetch_related` (M2M/reverse). Finalize README + push.
- **Acceptance:** a test or toolbar screenshot shows the query count dropping to a constant after the fix; API still returns identical data; repo pushed with setup instructions.
- **Ruby→Python watch-outs:** `select_related` ≈ `includes`/`joins` for single-valued (FK) relations (SQL JOIN); `prefetch_related` ≈ `includes` for collections (separate query + Python-side join). Picking the wrong one doesn't error — it just doesn't help. This is the exact N+1 skill from your Rails work, renamed.
- **Senior signal:** You can look at a serializer and predict the query count, then name the right prefetch strategy.

**Week 3 interview check:** (1) "Explain N+1 in Django and how `select_related` differs from `prefetch_related`." (2) "When does a QuerySet actually hit the database?"

---

## WEEK 4 — FastAPI + Pydantic (5 days)
**GitHub deliverable (Day 5):** a Dockerized FastAPI service with Pydantic models + endpoints.
**Why this week matters most for LLM/eval roles:** Pydantic is everywhere in tool-calling and eval schemas — learn it *well*, not just enough.

### Day 1 — FastAPI basics, path/query params, first Pydantic model
- **Focus:** app scaffolding, GET endpoints, auto docs.
- **READ:** FastAPI tutorial "First Steps," "Path Parameters," "Query Parameters" (`fastapi.tiangolo.com/tutorial/`).
- **BUILD:** `uv add fastapi uvicorn`; a service with a few GET endpoints using typed path and query params, returning a Pydantic model.
- **Acceptance:** `uvicorn` serves; `/docs` (Swagger) auto-renders your endpoints; wrong-typed path/query params return a 422 automatically; response matches the Pydantic model.
- **Ruby→Python watch-outs:** Routing is decorator-based (`@app.get(...)`) — types in the signature drive parsing AND docs (no Grape `params do ... end` block needed; the type hints *are* the contract). No Rails-style convention-over-config — everything is explicit.
- **Senior signal:** You explain that FastAPI derives validation + OpenAPI docs from type hints, so the annotations are the single source of truth.

### Day 2 — Pydantic deep (validation, validators, settings)
- **Focus:** models, field constraints, custom validators, nested models, `BaseSettings`.
- **READ:** Pydantic docs (`docs.pydantic.dev`) — Models, Validators (field + model), Settings management.
- **BUILD:** Rich Pydantic models for your domain: field constraints (min/max/regex), a custom `field_validator` and a `model_validator` (cross-field rule), a nested model, and a `BaseSettings` config loaded from environment variables.
- **Acceptance:** bad input is rejected with clear 422 field errors; the cross-field validator fires correctly; settings load from real env vars; models are fully typed.
- **Ruby→Python watch-outs:** Pydantic ≈ ActiveModel validations + StrongParameters + coercion, but at the *type* boundary and much stricter. It **coerces** types by default (a numeric string may become an int) — know when you want strict mode. Validators run on construction, unlike AR validations you trigger with `valid?`. This is Pydantic **v2** — v1 syntax you'll find in old tutorials is different (`field_validator`, not `@validator`).
- **Senior signal:** You know Pydantic v2 validator syntax, coercion behavior, and use `BaseSettings` for 12-factor config.

### Day 3 — Request bodies, response_model, dependency injection
- **Focus:** POST/PUT bodies, output shaping with `response_model`, `Depends()`.
- **READ:** FastAPI tutorial "Request Body," "Response Model," "Dependencies."
- **BUILD:** POST/PUT endpoints accepting Pydantic bodies; use `response_model` to shape/filter output (hide internal fields); factor shared logic (e.g. pagination params or a fake "current settings") into a dependency via `Depends()`.
- **Acceptance:** a create endpoint validates the body and returns the `response_model` shape (excluded fields absent); at least one `Depends()` reused across two endpoints; 422 on invalid body.
- **Ruby→Python watch-outs:** `Depends()` ≈ Rails `before_action`/service-object injection, but resolved per-request and declared in the signature. `response_model` ≈ a Grape Entity controlling exposure — but it also validates the *outgoing* data. Request body model vs response model should often be *different* classes (input vs output DTOs).
- **Senior signal:** You separate input and output schemas and can explain FastAPI's dependency injection as testable, composable, per-request wiring.

### Day 4 — async/await + SQLAlchemy basics
- **Focus:** the async model; persistence with SQLAlchemy.
- **READ:** FastAPI "Concurrency and async/await"; Real Python "Async IO in Python"; SQLAlchemy 2.0 ORM quickstart.
- **BUILD:** Add persistence with SQLAlchemy (models + session), CRUD-backed endpoints. Make at least one endpoint genuinely `async` and be able to justify where async helps vs where it doesn't.
- **Acceptance:** data persists across requests; CRUD works via the API; you can articulate why you chose async or sync for each endpoint (and don't block the event loop with sync DB calls in an async route).
- **Ruby→Python watch-outs:** Ruby (MRI) is thread/GIL-based and mostly synchronous in your day-to-day; Python `async`/`await` is cooperative single-threaded concurrency — `await` yields control, it does NOT parallelize CPU work. Calling a blocking/sync function inside an `async def` stalls the whole event loop (a top FastAPI mistake). SQLAlchemy 2.0 style differs a lot from ActiveRecord — sessions are explicit, no implicit save.
- **Senior signal:** You explain what `await` actually does (yields to the event loop for I/O) and why blocking calls in async routes are a bug — not just "async is faster."

### Day 5 — Docker + finalize (DELIVERABLE)
- **Focus:** containerize and ship.
- **READ:** FastAPI "Deployment - Docker"; Docker's Python image docs.
- **BUILD:** Write a `Dockerfile` (uv-based, slim base) and `.dockerignore`; build and run the container serving your API.
- **Acceptance:** `docker build` succeeds; `docker run` serves the API and `/docs` works from the container; `.dockerignore` excludes `.venv`/caches; image doesn't ship dev-only junk; README documents build+run; **pushed to GitHub**.
- **Ruby→Python watch-outs:** No Rails asset pipeline to worry about, but pin the base image and lock deps (`uv.lock`) for reproducibility — same discipline as `Gemfile.lock`. Don't run as root; expose the right port; use a production server invocation (uvicorn) not `--reload` in the image.
- **Senior signal:** Your Dockerfile is small, layer-cached sensibly, and reproducible — you can explain each layer.

**Week 4 interview check:** (1) "What does `await` actually do, and what breaks if you call a blocking function in an async route?" (2) "How does Pydantic v2 validation/coercion work, and why is it central to tool-calling / LLM eval schemas?"

---

### Threading it together
- Weeks 1-2 → one repo (the typed, tested CLI). Weeks 3 and 4 → one repo each. That's **3 GitHub deliverables + 1 application** across Weeks 0-4 — exactly what the plan's résumé section needs before Weeks 5-6 (LLM/function-calling, where your MCP/OAuth background becomes the headline).
- Every day ends the same way: `ruff` clean, `mypy --strict` clean, `pytest` green, committed. If those three are green and the acceptance criteria are met, ping me for review.
