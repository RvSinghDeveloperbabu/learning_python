# Python Fundamentals — Weeks 1–3 (start here)

> **Who this is for.** You are a senior engineer *and* a genuine beginner at Python. Both are true. This file assumes you already understand loops, objects, errors, and tests **as ideas** — and assumes you have never written Python. Every day names the Ruby thing you already own with `≈`.

## Read this before Day 1

**What you will NOT do for three weeks.** No `mypy --strict`. No comprehensions. No generators. No decorators. Those are real Python and you will learn them — in Weeks 4–5, on top of `evalctl`, once the basics are automatic. The "run ruff + mypy + pytest before you call it done" rule from the other curriculum docs **does not apply until Day 18.**

**Why tooling comes last, not first.** You lost five days to `[tool.mypy]` configuration before writing a single line of Python. That is not a discipline problem — config work *resembles* Rails work you already know, so it feels productive while you are actually stuck. Day 18 is the only tooling day in this file, and you arrive at it having already written sixteen working programs.

**One program, grown daily.** Days 1–18 build **one thing** — a contact book — from a single print statement into a tested, typed, packaged command-line tool. After Day 1 you never start from a blank file. You can always see the thing getting better.

**Cadence:** 6 days/week, 3–4 hrs/day. **Days 6 and 12 are flex days** — catch up, or rebuild an earlier program from memory. Do not skip them to get ahead; rebuilding from memory is where syntax stops being something you look up.

**How to use each day:** read first (~30% of your time), then build (~70%). The "Done when" list is yours to check *before* you ask me to review. If you cannot tick every box, you are not done — that is the whole point.

**Setup, once:** create a `fundamentals/` folder at the repo root and set it up as a `uv` project yourself. Keep `foundations/` untouched — that is your Week 4 project.

---

## WEEK 1 — Absolute basics

### Day 1 — Run a Python program at all

- **Focus:** the interpreter, running a file with `uv`, printing, variables, reading a command-line argument, and the `__main__` guard.
- **Read:** [Python tutorial §2](https://docs.python.org/3/tutorial/interpreter.html) and [§3 intro](https://docs.python.org/3/tutorial/introduction.html); [uv — running scripts](https://docs.astral.sh/uv/guides/scripts/).
- **Build:** a script that takes a name from the command line and greets that person. Put all the work inside a function called `main`, and call it under the `__main__` guard.
- **Done when:**
  - it runs with `uv run` and prints your greeting;
  - run with **no** argument, it prints a short usage line and **exits non-zero**;
  - a second file that imports the first one prints **nothing**.
- **Ruby ≈** `ruby script.rb` · `puts` · `if __FILE__ == $0`. That last one is the idiom you scored **weak** on in the 2026-07-13 mock interview — you are re-earning it as Day 1.

### Day 2 — Values: numbers, strings, f-strings, `None`, truthiness

- **Focus:** string interpolation, the two division operators, and which values Python treats as false.
- **Read:** [Python tutorial §3.1](https://docs.python.org/3/tutorial/introduction.html); [Real Python — f-strings](https://realpython.com/python-f-strings/); [Truth value testing](https://docs.python.org/3/library/stdtypes.html#truth-value-testing).
- **Build:** a tip calculator — read a bill amount and a tip percentage, print the formatted total to two decimal places.
- **Done when:**
  - a bill of `0` **still prints a total** (this proves you did not write a bare truthiness check where you meant "was a value given?");
  - the output shows exactly two decimal places;
  - your program can print one example of a value that is falsy and one that is `None`, and you can say why they are different things.
- **Ruby ≈** `#{}` → f-strings · `nil` → `None`, tested with `is None`, **never** `== None`.
- **⚠️ The trap:** Ruby treats only `nil` and `false` as falsy. Python also treats `0`, `0.0`, `0j`, `""`, `[]`, `{}`, `set()`, `()`, and `range(0)` as falsy. **The general rule:** an object is falsy if its `__bool__` returns `False`, or (failing that) its `__len__` returns `0` — which is why every empty container is falsy. Know the rule, not just the list; that's what makes the "name them from memory" question easy.

### Day 3 — Control flow: `if`/`elif`/`else`, `for`, `while`, `range`

- **Focus:** indentation as actual syntax; the absence of `end`.
- **Read:** [Python tutorial §4.1–4.4](https://docs.python.org/3/tutorial/controlflow.html).
- **Build:** FizzBuzz for 1–100, then a number-guessing loop that keeps asking until the guess is right.
- **Done when:**
  - FizzBuzz output matches the classic expected lines exactly;
  - the word `end` appears nowhere in your file;
  - the guessing loop terminates and exits `0`;
  - you deliberately mix a tab and spaces in one block, see the error, and can name it.
- **Ruby ≈** `elsif` → `elif` · no `end` — indentation **is** the block · `(1..n).each` → looping over `range`.
- **⚠️ The trap:** Ruby's `..` includes the last number; Python's `range` **excludes** it.

### Day 4 — Lists and tuples

- **Focus:** create, index, slice, append, iterate, length. **No comprehensions today** — plain loops only.
- **Read:** [Python tutorial §5.1 and §5.3](https://docs.python.org/3/tutorial/datastructures.html).
- **Build:** an in-memory to-do list — add an item, list all items numbered, remove one by position.
- **Done when:**
  - removing position 0 twice removes **two different items** (proving you understand the list re-indexes);
  - a negative index prints the last item;
  - a slice prints the sub-list you expected;
  - trying to change an element of a tuple raises `TypeError`, and you can say why.
- **Ruby ≈** Array → list · `<<` → the append method · negative indexing works like Ruby's · tuples are frozen, with no everyday Ruby twin.

### Day 5 — Dicts and sets

- **Focus:** key lookup, safe lookup, membership, iterating pairs, uniqueness.
- **Read:** [Python tutorial §5.5 and §5.4](https://docs.python.org/3/tutorial/datastructures.html).
- **Build:** **contact book v1** — store name → phone number, with add / look up / list-all. Keep a set of tags alongside it.
- **Done when:**
  - looking up a missing name with square brackets raises `KeyError` and **you have seen it happen**;
  - the same lookup done safely returns `None` instead of raising;
  - adding a duplicate to the set leaves its length unchanged;
  - listing all contacts iterates over pairs directly, not keys-then-lookup.
- **Ruby ≈** Hash → dict · `hash.key?` → the `in` operator · dicts keep insertion order, like Ruby hashes.
- **⚠️ The biggest Hash→dict trap:** `hash[:missing]` returns `nil` in Ruby. Python **raises** `KeyError`. And there is **no Symbol type** — in practice you use strings, though a dict key can be **any hashable value** (numbers, tuples, enums, frozensets — anything immutable enough to hash).

### Day 6 — Flex / review

Rebuild any Day 1–5 program from a **blank file**, without looking at your old code.

- **Done when:** one program is rewritten in under 30 minutes and still meets its original "Done when" list.

---

## WEEK 2 — Functions, objects, failure, files

### Day 7 — Functions

- **Focus:** defining functions, parameters, **explicit `return`**, default arguments, calling with named arguments.
- **Read:** [Python tutorial §4.7–4.8](https://docs.python.org/3/tutorial/controlflow.html).
- **Build:** refactor Day 5's contact book so every operation is its own function, and the body of the file contains nothing but the guarded call to `main`.
- **Done when:**
  - no logic runs at the top level of the file;
  - a function whose default is meant to be an empty collection returns a **fresh** empty result the second time you call it with no arguments — you demonstrate this yourself;
  - at least one function is called using named arguments.
- **Ruby ≈** keyword arguments map closely to Ruby 2+.
- **⚠️ Two traps:** Ruby's implicit "last expression is the return value" **does not exist** — a missing `return` silently gives you `None`. And default arguments are evaluated **once, when the function is defined** (Ruby evaluates them per call) — which is why that second bullet matters.

### Day 8 — Classes, part 1: constructor, `self`, attributes, printing

- **Focus:** defining a class, the constructor, the explicit receiver, and making instances print usefully.
- **Read:** [Python tutorial §9.1–9.4](https://docs.python.org/3/tutorial/classes.html); the data-model docs on `__init__` and `__repr__`.
- **Build:** a `Contact` class that replaces the loose values from Day 5. The contact book now holds a list of these objects.
- **Done when:**
  - printing an instance shows **your** representation, not `<... object at 0x...>`;
  - every method's first parameter is the receiver, and you can say why Python makes it explicit;
  - two instances built from identical data print identically but do **not** compare as equal — observe this, it sets up tomorrow.
- **Ruby ≈** `initialize` → `__init__` · `@name` → an attribute on `self` · `to_s`/`inspect` → `__str__`/`__repr__`.
- **⚠️ The break:** Ruby's receiver is invisible. Python's is a real, named, **first parameter in every method signature**.

### Day 9 — Classes, part 2: equality, properties, class methods, inheritance

- **Focus:** value equality and hashing, computed properties, class methods vs static methods, calling the parent, and the `_private` convention.
- **Read:** [Python tutorial §9.5](https://docs.python.org/3/tutorial/classes.html); the docs on `property` and `classmethod`.
- **Build:** give `Contact` value equality, one computed property, and a class method that builds an instance from a single line of text. Add one small subclass.
- **Done when:**
  - two contacts with equal values compare equal;
  - putting them in a set **fails until you also define hashing** — and you can explain why the two go together;
  - the property is read **without** parentheses;
  - the subclass calls up to the parent constructor.
- **Ruby ≈** `super` maps closely.
- **⚠️ Do not reach for `attr_accessor` habits:** plain Python attributes are already public. Use a property only when you need computation or validation. Python has **no enforced `private`** — a leading underscore is convention only.

### Day 10 — Exceptions and EAFP

- **Focus:** `try` / `except` / `else` / `finally`, the exception hierarchy, catching *specific* types, raising, and writing your own exception class.
- **Read:** [Python tutorial §8](https://docs.python.org/3/tutorial/errors.html); [built-in exception hierarchy](https://docs.python.org/3/library/exceptions.html).
- **Build:** harden the contact book — looking up an unknown name raises **your own** exception type, and the command-line layer catches it and reports cleanly.
- **Done when:**
  - an unknown contact exits **non-zero** with a one-line message and **no traceback**;
  - you have no bare `except` anywhere (ruff rule E722 would flag it);
  - a `finally` block demonstrably runs on **both** the success and the failure path;
  - your exception inherits from `Exception`, not `BaseException`, and you can say why.
- **Ruby ≈** `begin` / `rescue` / `ensure` / `else` maps almost one-to-one onto `try` / `except` / `finally` / `else`.
- **⚠️ Two differences:** there is **no Python equivalent of Ruby's `retry` keyword** — you write the loop yourself. And Python culture prefers **EAFP** ("try it, handle the failure") over the Rails habit of guard-clause checking first.

### Day 11 — Files and `pathlib`

- **Focus:** reading and writing text, using `with` (as a *consumer* of context managers), path objects, encoding.
- **Read:** [Python tutorial §7.2](https://docs.python.org/3/tutorial/inputoutput.html); [`pathlib` basic use](https://docs.python.org/3/library/pathlib.html).
- **Build:** the contact book saves to a file and reloads it when it starts.
- **Done when:**
  - contacts survive quitting and restarting the program;
  - a missing data file is **created**, not crashed on;
  - a path pointing into a folder that doesn't exist produces **your** Day 10 error message, not a raw traceback;
  - **no path anywhere is built by string concatenation or an f-string.**
- **Ruby ≈** `File.open(path) do |f| ... end` → the `with` statement — same guaranteed-cleanup idea, generalized · `File.join` → the `/` operator on path objects.

### Day 12 — Flex / review

Catch up, or rebuild the Day 8–9 class work from memory.

---

## WEEK 3 — Structure, data, tests, and the tooling gate

### Day 13 — Modules, imports, packages, entry points

- **Focus:** the forms of `import`, what makes a folder a package, absolute imports, and declaring a console command.
- **Read:** [Python tutorial §6](https://docs.python.org/3/tutorial/modules.html); [Packaging guide — entry points](https://packaging.python.org/en/latest/specifications/entry-points/).
- **Build:** split the contact book into **three modules** — the record type, storage, and the command-line layer — inside one package. Declare a console-script entry point.
- **Done when:**
  - the tool runs as a **named command** via `uv run`, not as a file path;
  - importing the record module **alone** produces no output and no side effects;
  - importing your package from a shell **outside** the project's environment fails, and you can name the mechanism that makes it fail.
- **Ruby ≈** `require` / `require_relative` — but **path-sensitive, with no Rails autoloading.** Nothing is found by convention.
- **📌 Note:** that last bullet is the `sys.path` → `site-packages` question you answered **passable-leaning-weak** on 2026-07-13. This is the re-ask.

### Day 14 — JSON and dataclasses

- **Focus:** turning objects into JSON and back; `dataclass` as shorthand for the class you hand-wrote on Days 8–9.
- **Read:** [`json` basic usage](https://docs.python.org/3/library/json.html); [`dataclasses`](https://docs.python.org/3/library/dataclasses.html).
- **Build:** switch storage from plain text to JSON, with records as dataclasses.
- **Done when:**
  - JSON → object → JSON round-trips with **no field lost and no type changed**;
  - a hand-corrupted JSON file produces your own error message, not a traceback;
  - you can state which of the methods you wrote by hand on Days 8–9 the decorator now generates for you.
- **Ruby ≈** `Struct` / `Data.define` → dataclass · `JSON.parse` / `JSON.generate` → the load/dump functions.
- **⚠️ The gap:** Python will **not** serialize your dataclass automatically — you convert it to a dict first.
- **📌 Why this order:** you meet dataclasses *after* writing classes by hand, so the decorator reads as shorthand instead of magic.

### Day 15 — Logging, and a first look at type hints

- **Focus:** diagnostics vs program output; log levels; annotating function signatures (annotations only — strict checking is Day 18).
- **Read:** [Logging HOWTO — basic tutorial](https://docs.python.org/3/howto/logging.html); [mypy type-hints cheat sheet](https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html) (skim the function-signature part only).
- **Build:** add levelled logging behind a verbosity flag, and annotate every function signature you have written.
- **Done when:**
  - the verbosity flag visibly changes what appears;
  - redirecting **stdout** to a file still shows your log lines on the terminal — proving logs go to stderr and data goes to stdout;
  - plain `mypy` (**not** strict) reports zero errors.
- **Ruby ≈** Rails' logger and its levels.
- **⚠️ The rule:** `print` is for the program's **output**; logging is for the program's **diagnostics**. Mixing them is what makes a command-line tool impossible to pipe.

### Day 16 — pytest, your first real suite

- **Focus:** how tests are discovered, plain `assert`, asserting that something raises, temporary directories.
- **Read:** [pytest — get started](https://docs.pytest.org/en/stable/getting-started.html); the docs on `pytest.raises` and `tmp_path`.
- **Build:** a real test suite for the contact book. *(This is where your empty `test_something.py` finally stops collecting zero tests.)*
- **Done when:**
  - `uv run pytest` collects **at least 5 tests** and all pass;
  - one test asserts your Day 10 exception is raised;
  - every filesystem test uses a temporary path, so no test touches your real data file;
  - **you delete one line of source, watch a specific test fail, then put it back.**
- **Ruby ≈** RSpec — but plain `assert` instead of `expect().to`, no `describe`/`it` DSL, files named `test_*.py` and functions named `test_*`.
- **📌 That last bullet is deliberate.** A suite that cannot fail is not a suite. This is the direct countermeasure to the *"declares done before verifying"* pattern logged twice in your tracker.

### Day 17 — pytest depth: fixtures, parametrize, patching, captured output

- **Focus:** shared setup by argument name, table-driven cases, replacing a dependency inside a test, capturing printed output.
- **Read:** [pytest fixtures](https://docs.pytest.org/en/stable/explanation/fixtures.html); [parametrize](https://docs.pytest.org/en/stable/how-to/parametrize.html); the docs on `monkeypatch` and `capsys`.
- **Build:** refactor Day 16's suite — move shared setup onto a fixture, turn the edge cases into one parametrized table, patch one dependency, and assert on printed output.
- **Done when:**
  - you have at least one fixture, one parametrized test with 3+ cases, one patched dependency, and one assertion on captured output;
  - the suite still passes;
  - the **test count went up** while duplicated setup **went down**.
- **Ruby ≈** fixtures ≈ `let` / `before`, but injected **by parameter name** rather than by scope · parametrize ≈ shared examples / table tests · patching ≈ `allow(...).to receive` · `conftest.py` ≈ `spec_helper.rb`.
- **📌 Why here:** mocking is demanded at the flagship in Week 14. Meeting it now, on your own small program, is far cheaper than meeting it for the first time at a Docker boundary.

### Day 18 — The tooling gate (graduation)

- **Focus:** ruff, mypy in strict mode, dev dependency groups — now, with sixteen working programs behind you.
- **Read:** [ruff configuration](https://docs.astral.sh/ruff/configuration/); [mypy getting started](https://mypy.readthedocs.io/en/stable/getting_started.html) and its strict-mode flags.
- **Build:** turn strict type checking on for the `fundamentals/` package and fix everything it reports.
- **Done when:**
  - `uv run ruff check` is clean;
  - `uv run mypy --strict` is clean with **zero** ignore comments;
  - `uv run pytest` is green;
  - all of it is committed and **pushed to GitHub — your first Python repo.**
- **Ruby ≈** ruff ≈ RuboCop (also a formatter, far faster) · a dev dependency group ≈ `group :development, :test do` in a Gemfile · mypy is a **separate external checker**, closest to Sorbet — the interpreter itself does not enforce it.
- **📌 Carry this into interviews, and get it right:** type annotations are **not enforced at runtime**, but they **are** evaluated, stored, and readable at runtime — which is exactly how dataclasses, Pydantic, and FastAPI work. Do not say "erased at runtime"; that is wrong, and it contradicts the work you will do in Weeks 9–12.

---

## What you did *not* learn here, and where it lives

These omissions are deliberate, not oversights. They all arrive in **Weeks 4–5** on top of `evalctl`, where they have real work to do:

- **Comprehensions** and generator expressions
- **Generators** (`yield`) — for streaming files too big for memory
- **Decorators** you write yourself, and **context managers** you author (you only *used* them on Day 11)
- **`itertools`** and **`functools`**
- **`Protocol`** and `TypedDict` — the typed version of duck typing
- **`Counter`** and `defaultdict`

You will meet every one of them with three weeks of working Python behind you, which is exactly the right time.

➡️ **Next:** [`../Ravi_Python_LLM_Learning_Plan.md`](../Ravi_Python_LLM_Learning_Plan.md) → Weeks 4–5, `evalctl`.
