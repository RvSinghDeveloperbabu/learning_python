# Curriculum Review Notes

> **Read this first (added 2026-07-20).** This review was written against the **original 8-week curriculum**, before the 14-week restructure and before [`07-python-fundamentals.md`](07-python-fundamentals.md) existed. Its findings remain valid as *analysis*; several are now **resolved** by the restructure. Each item below carries a **status marker** — `✅ CLOSED` (and where) or `🔲 OPEN`.
>
> **References are by topic, not by week/day coordinate.** Earlier versions of this file pointed at "Week 2 Day 5"-style locations; those broke twice across reschedules. Topic names survive renumbering.

---

## Verdict

The curriculum's BUILD/acceptance framing is genuinely self-verifiable (mypy/pytest/docker/query-count/`/docs` are all things Ravi checks himself), and nothing forces Claude to hand over code. The Ruby→Python analogies are mostly accurate and well-chosen. The real weaknesses were (1) one factually wrong talking-point that would produce a bad interview answer, (2) several **senior-Python-depth topics simply absent** despite "Senior Python Developer depth PRIMARY", and (3) exercises that could quietly dead-end a Python newcomer.

**The single biggest issue was not in this list at all:** the curriculum assumed a learner who already knew Python's basics. He did not. That is what the fundamentals phase now fixes, and it closes five of the findings below as a side effect.

---

## P0 — Correctness

**1. "Type hints are erased at runtime / zero runtime cost" is wrong and self-contradicting.** ✅ **CLOSED** — corrected in *the type-hints day* (`04-curriculum-core-python-and-web.md`, Weeks 4–5 Day 2) and *the tooling-gate day* (`07-python-fundamentals.md`, Day 18).
Annotations are *evaluated and stored* at definition time in `__annotations__` and are introspectable at runtime via `typing.get_type_hints()` — which is *precisely* why Pydantic, FastAPI, and dataclasses work. They are simply **not enforced** by the interpreter; mypy is a separate external static checker, not a "compile" step. Saying hints are "erased at runtime" is a wrong senior answer that contradicts his own later work.

**2. The GIL / concurrency model is never taught, yet it is one of the most-asked senior-Python interview questions.** 🔲 **OPEN**
The async material is solid, but there is zero coverage of the GIL, threads vs `multiprocessing` vs `asyncio`, or `concurrent.futures`. **Suggested fix:** an interview-reference talking-points block (no build required) — what the GIL is, why threads don't give CPU parallelism in CPython, when to reach for each concurrency model, and how it differs from Ruby's GVL. Table stakes for the Senior Python Developer track.

---

## P1 — Senior-depth topic gaps

**3. Python's class model is essentially skipped** — the curriculum jumped straight to `@dataclass` without teaching raw classes. ✅ **CLOSED** — *the two classes days* (`07-python-fundamentals.md`, Days 8–9) now cover explicit `self`, `__init__`/`__repr__`/`__eq__`/`__hash__`, `@property`, `@classmethod` vs `@staticmethod`, the `_private` convention, and `super()` — **before** *the dataclasses day* (Day 14), so the decorator reads as shorthand rather than magic. (MRO / multiple inheritance and `abc` remain untaught — a small residual gap.)

**4. Exception handling gets no dedicated coverage.** ✅ **CLOSED** — *the exceptions day* (`07-python-fundamentals.md`, Day 10) covers `try`/`except`/`else`/`finally`, the hierarchy, custom exception classes, and **EAFP vs LBYL**, with the Ruby anchors (`rescue`→`except`, `ensure`→`finally`, no Python equivalent of Ruby's `retry`, bare `except:` is an anti-pattern, catch `Exception` not `BaseException`).

**5. Advanced typing a senior interview expects is absent** — `Protocol`, `TypedDict`, `Literal`, `TypeVar`/`Generic`, `Callable`, `@overload`, `Final`, `cast`. ✅ **CLOSED (partially)** — *the structural-typing day* (`04-curriculum-core-python-and-web.md`, Weeks 4–5 Day 7) now teaches `Protocol`, `TypedDict`, and `Literal`, and explicitly forward-links them to the provider seam in `agent-cli` and the `Sandbox` protocol in `eval-harness`. `TypeVar`/`Generic`/`@overload` remain uncovered.

**6. Mocking is required at the flagship but never introduced.** ✅ **CLOSED** — *the pytest-depth day* (`07-python-fundamentals.md`, Day 17) introduces `monkeypatch`, `capsys`, fixtures, and parametrize on his own small program, weeks before the flagship demands mocking the Docker/subprocess boundary.

**7. `if __name__ == "__main__":`, the import system, and packaging entry points are never explicitly taught,** despite multiple CLI deliverables. ✅ **CLOSED** — the `__main__` guard is *Day 1* of the fundamentals; *the modules-and-entry-points day* (Day 13) covers import forms, packages, absolute imports, and `[project.scripts]` console entry points.

**8. The `logging` module is never mentioned,** yet later work assumes logging hygiene. ✅ **CLOSED** — *the logging day* (`07-python-fundamentals.md`, Day 15), including the stdout-vs-stderr distinction and why mixing `print` and logging makes a CLI unpipeable.

---

## P2 — Dead-end / friction risks

**9. `mypy --strict` + "no `Any` in your own signatures" on a JSON processor is a genuine trap.** 🔲 **OPEN**
`json.loads` returns `Any`, so the JSON round-trip acceptance criteria are quietly hard — strict mode fights him at the dynamic boundary, and the criteria forbid `# type: ignore`. **Suggested fix:** add a watch-out that the JSON/dynamic boundary is exactly where `Any` legitimately enters, and the senior move is to *contain* it (validate / `cast` / `TypedDict` at the edge, fully typed inside). That reframes the frustration as the actual lesson.

**10. Pylance (Pyright) strict and `mypy --strict` will disagree** and double-report, confusing a newcomer. 🔲 **OPEN**
**Suggested fix:** pick one as source of truth (the plan uses mypy) and set Pylance to "basic", or explicitly warn that the engines differ and mypy is the gate.

**11. The async-DB anti-pattern is the path of least resistance.** ✅ **CLOSED** — *the async + async-SQLAlchemy days* (`04-curriculum-core-python-and-web.md`, Week 9 Days 4–5) now make the choice explicit (async engine end-to-end, or keep DB routes sync), add the "no blocking calls on the request path" acceptance test, note that FastAPI runs plain `def` endpoints in a threadpool, and flag the day as the week's highest risk so it gets front-loaded.

**12. The Dockerize-a-library shortlist mixes easy and hard targets.** ✅ **CLOSED** — *the first Dockerize day* (`05-curriculum-llm-and-flagship.md`, Week 10 Day 3) now steers the first attempt to genuinely pure-Python suites (`click`, `flask`, `requests`) and explicitly warns off compiled-core libraries until a second pass.

---

## P3 — Acceptance-criteria & testing consistency

**13. The Django and FastAPI deliverables had no explicit test requirement.** ✅ **CLOSED** — the Django phase now requires the cross-tenant isolation test and the `assertNumQueries` before/after; the FastAPI phase requires a dependency-override test (which doubles as the DI lesson) and a loop-blocking check.

**14. The plan says "rewrite 2 Ruby scripts"; only one explicit rewrite exists.** 🔲 **OPEN**
Translating forces the "stop transliterating" lesson better than greenfield builds. **Suggested fix:** designate a second genuine Ruby→Python rewrite, ideally during the fundamentals flex days (Day 6 or Day 12).

**15. A few acceptance criteria are self-assessed rather than machine-verifiable** ("you can articulate…"). 🔲 **OPEN (informational)** — inherent to conceptual mastery and fine since the mentor reviews, but they should be flagged as "review-gated" so they aren't mistaken for done-when-green.

---

## P4 — Ruby→Python watch-out accuracy

**16. "There are no Symbols — dict keys are just strings" is an oversimplification.** ✅ **CLOSED** — *the dicts-and-sets day* (`07-python-fundamentals.md`, Day 5) now states that keys may be any **hashable** value, while keeping the practical "no Symbol type, use strings" guidance.

**17. The falsy-values list was incomplete** relative to its own "list them from memory" senior signal. ✅ **CLOSED** — *the values day* (Day 2) now gives the common set **and** the general rule (any object whose `__bool__` returns `False`, or whose `__len__` returns `0`).

**18. Ruby's is a GVL, and both LLM SDKs ship built-in retries.** ✅ **CLOSED** — the GVL contrast appears in the async material; the robustness day now notes the SDKs already back off on transient errors, so the exercise is about tuning and bounding, not reinventing.

**19. Minor enrichments that would land well for a senior.** 🔲 **OPEN** — `Counter` ≈ Ruby's `Enumerable#tally`; **naive vs timezone-aware `datetime`** as a classic bug; `__exit__` returning truthy suppresses exceptions, and `contextlib.ExitStack`.

---

## P5 — Optional enrichments

🔲 **OPEN** (all nice-to-have, none blocking):
- Mention **structured outputs / JSON-schema response modes** and **prompt caching** as eval-relevant stretch; note that **streaming + tool use** together is advanced (partial-JSON accumulation), so keeping them separate is deliberate.
- Introduce building a tool's JSON schema *from* its Pydantic model (single source of truth) — exactly what production tool-calling does.
- Add the P0/P1 topics (classes/dunders, exceptions/EAFP, GIL/concurrency, `Protocol`) to the interview flashcard set — currently under-represented versus the LLM topics.

---

## Summary of what the 14-week restructure closed

| Status | Findings |
|---|---|
| ✅ **Closed** | 1 (type-hints error), 3 (classes), 4 (exceptions), 5 (partially — `Protocol`/`TypedDict`/`Literal`), 6 (mocking), 7 (`__main__`/imports/entry points), 8 (logging), 11 (async-DB), 12 (Dockerize targets), 13 (API tests), 16, 17, 18 |
| 🔲 **Open** | 2 (**GIL/concurrency — highest-value remaining gap**), 9 (`Any` at the JSON boundary), 10 (Pylance vs mypy), 14 (second Ruby rewrite), 15 (review-gated criteria), 19, P5 items |

**Highest-value remaining work: finding #2.** The GIL and Python's concurrency model are still untaught and are among the most-asked senior-Python screening questions. Everything else open is polish.
