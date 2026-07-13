# Daily Session Interview Questions — with model answers

> The 2–3 questions the mentor asks at the end of each session, tied to what you built that day.
>
> **How to study:** cover the answer, say your own answer *out loud* first (explaining clearly is roughly half the grade in your target interviews), then check it against the model answer.
>
> Newest session on top.

---

## 2026-07-13 · Week 0 — toolchain setup (Python, uv, venvs, VS Code)

### Q1. When Python runs `import httpx`, how does it decide whether it can find the package — and what does a virtual environment change about that?

**Model answer.**
- Python searches an ordered list of directories — the **module search path** (visible as `sys.path`) — checking each for something named `httpx`. Found → load it. Reaches the end without finding it → `ModuleNotFoundError`.
- The key directory on that list is **`site-packages`**, where installed third-party packages live.
- A **virtual environment** changes *which* `site-packages` is on the path. Each venv has its own interpreter and its own `site-packages`. Run through the venv's interpreter → its `site-packages` is on the path → httpx is found. Run system Python → a different `site-packages` (without httpx) is on the path → import fails.
- So isolation isn't files being "locked" to a folder; it's **which interpreter you run, and therefore which package folder is visible.**

**Ruby anchor:** `sys.path` ≈ `$LOAD_PATH`; `require` searches it the same way. Bundler points the load path at the bundle's gems; a venv does the equivalent, but as a whole separate interpreter + package directory you choose explicitly.

**My gap this time:** had the isolation intuition, missed the mechanism (`sys.path` → `site-packages`). Re-ask.

### Q2. What is `__name__` at runtime, why is it sometimes `"__main__"` and sometimes not, and what problem does the `if __name__ == "__main__":` guard prevent?

**Model answer.**
- Every module gets a built-in variable `__name__` when it's loaded.
- Run a file **directly** → Python sets its `__name__` to the string `"__main__"`.
- **Import** the file from another module → its `__name__` is the module's real name (like `"main"`), not `"__main__"`.
- So the guard asks: *"Am I being run directly, or imported?"* The block runs only when the file is run directly.
- It lets one file be both a **runnable program** and an **importable library**. Without it, importing the file to reuse a single function would also run its top-level program code as a side effect.

**Ruby anchor:** same as `if __FILE__ == $0` — run this only when this file is the program being executed, not when it's `require`d.

**My gap this time:** new idiom, no answer. Re-ask in a later mock.
