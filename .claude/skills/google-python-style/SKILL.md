---
name: google-python-style
description: Enforces Google's Python Style Guide (google.github.io/styleguide/pyguide.html) when writing, editing, or reviewing Python code. Covers naming conventions, formatting, indentation, import ordering, Google-style docstrings, common anti-patterns (mutable default arguments, bare except, string concatenation in loops, power features, etc.), and a structured Google-style code review process (architecture intent, test coverage, performance, style). Use this whenever writing new Python code, editing existing Python files, reviewing a Python PR/diff, or when the user mentions Python style, PEP 8, Google style guide, pylint, or "how should I review this Python code." In multi-language repos, pair with sibling Google style skills for other languages (e.g. google-cpp-style, google-java-style) so all languages stay consistent with their respective Google style guide.
---

# Google Python Style

Applies Google's official Python Style Guide to code generation, editing, and
review. Source of truth: https://google.github.io/styleguide/pyguide.html
(mirrors https://github.com/google/styleguide). This skill paraphrases and
operationalizes that guide — it is not a verbatim copy.

Use this skill for two distinct jobs, and know which one you're doing:

1. **Writing/editing Python** — apply the conventions in this file automatically,
   without being asked each time.
2. **Reviewing Python code** — follow the 5-step review process in
   `references/code_review_checklist.md`, which goes beyond style into
   architecture, tests, and performance.

For quick generation tasks, the "Core Conventions" and "Anti-Patterns" sections
below are usually enough. Load the `references/` files when you need the exact
naming table, full docstring formats, or the review checklist.

---

## Core Conventions (apply by default)

**Naming** (see `references/naming_and_style.md` for the full table)
- `lower_with_under` for modules, packages, functions, methods, variables, parameters.
- `CapWords` for classes and exceptions.
- `CAPS_WITH_UNDER` for module- or class-level constants.
- Leading single underscore (`_name`) for internal/protected names. Avoid
  leading double underscore ("dunder" name-mangling) — it hurts readability
  and testability.
- No single-character names except: loop counters (`i, j, k`), `e` for
  exceptions, `f` for file handles in `with`, unconstrained private TypeVars
  (`_T`), or names matching an established mathematical/paper notation (cite
  the source in a comment if so).
- Never encode the type in the name (`id_to_name_dict` → just `id_to_name`).
- Filenames: `.py` extension, no dashes, `lower_with_under.py`.

**Formatting**
- 4-space indentation, never tabs. 2-space indent is not allowed.
- Max line length 80 characters (exceptions: long imports, URLs/paths in
  comments, pylint disable comments — see reference for the full exception list).
- No semicolons to end lines or join statements.
- No backslash line continuation — use implicit joining inside `()`/`[]`/`{}`.
- Two blank lines between top-level defs, one blank line between methods.
- No whitespace inside `()`/`[]`/`{}`, none before `,`/`;`/`:`, none before an
  open paren/bracket that starts an arg list or index.
- Never align `=`, `:`, or `#` vertically across lines — it's a maintenance burden.
- Prefer the `Black` or `Pyink` auto-formatter over hand-formatting when the
  project has one configured; these rules describe what that formatter enforces.

**Imports**
- `import x` for packages/modules; `from x import y` for a specific module;
  `import y as z` only for standard abbreviations (e.g. `import numpy as np`).
- Never `from module import ClassOrFunction` for arbitrary symbols — import
  the module. (Exception: `typing`/`collections.abc` symbols are imported directly.)
- One import per line. No relative imports — always the full package path.
- Group in this order, each group sorted lexicographically by full path:
  1. `from __future__ import ...`
  2. standard library
  3. third-party packages
  4. sub-package / local imports
- Imports go after the module docstring, before globals/constants.

**Docstrings** (Google style, `"""triple double quotes"""`, PEP 257)
- One-line summary ≤ 80 chars, ending in `.`/`?`/`!`, then a blank line, then
  more detail if useful.
- Module docstring: one-line summary + description + optional usage example.
- Function/method docstring required when the function is public API,
  nontrivial, or has non-obvious logic. Include `Args:`, `Returns:` (or
  `Yields:` for generators), `Raises:` sections as needed — see
  `references/naming_and_style.md` for exact formatting and an example.
- Class docstring: one-line summary of what an *instance represents* (not
  "a class that…"), plus an `Attributes:` section for public attributes.
- Overridden methods decorated with `@override` don't need a new docstring
  unless behavior materially differs from the base method.

**Type annotations**
- Encouraged on public APIs and on code that's error-prone or hard to
  understand; not required everywhere.
- Use `X | None`, not implicit `x: str = None`.
- Prefer abstract types (`collections.abc.Sequence`) in signatures over
  concrete ones (`list`) unless a concrete type is actually required.
- Don't annotate `self`/`cls`; use `typing.Self` only when needed for correct typing.

---

## Anti-Patterns to Avoid (flag or auto-fix these)

Full list with wrong/right examples in `references/antipatterns.md`. The
highest-value ones to catch automatically:

1. **Mutable default argument** — `def f(a, b=[]):` → use `b: Sequence | None = None` and set `b = []` inside if `b is None`. Empty tuple `()` is fine as a default since it's immutable.
2. **Bare/broad `except:`** or `except Exception:` that swallows errors — only acceptable when re-raising or at a genuine isolation boundary (e.g. don't crash a worker thread).
3. **`assert` used for input validation** — asserts can be stripped at runtime; raise `ValueError`/a real exception for anything the API must guarantee.
4. **String concatenation with `+=` in a loop** — can be quadratic; build a list and `''.join()`, or use an `io.StringIO`.
5. **Comparing booleans with `== True/False`**, or `if len(x) == 0:` instead of `if not x:`.
6. **`x = x or []`** instead of `if x is None: x = []` — silently treats other falsy values (`0`, `''`) as "unset."
7. **"Power features"** — metaclasses, bytecode hacks, dynamic inheritance, reflection via `getattr` for control flow, monkeypatching. Avoid unless there's a clear, necessary win; standard-library uses (`abc.ABCMeta`, `dataclasses`, `enum`) are fine.
8. **`@staticmethod`** — avoid; use a module-level function instead unless integrating with an API that requires it. Limit `@classmethod` to named constructors or class-wide state.
9. **Catch-all `import os, sys` on one line** — one import per line.
10. **f-strings as the first argument to logging calls** (`logging.info(f'...')`) — use `%`-style with the literal pattern string first so unexpanded messages stay queryable and lazy: `logging.info('...%s', val)`.
11. **Relative imports** — always use the full package path.
12. **Not closing files/sockets/stateful resources explicitly** — use `with`, or `contextlib.closing()` if the object doesn't support `with`. Don't rely on `__del__`/garbage collection timing.

---

## Code Review Process

When asked to review Python code (a PR, a diff, or a file), don't just check
formatting. Follow the structured 5-step process in
`references/code_review_checklist.md`:

1. Pre-screen — is the change reasonably sized and scoped?
2. Architectural intent — does the change do what its description claims, and does the design fit the codebase?
3. Test coverage — do tests exist and actually exercise the new logic/edge cases?
4. Performance and correctness — algorithmic complexity, resource handling, concurrency issues.
5. Style — naming, formatting, docstrings, anti-patterns from this file.

Report style issues concisely (point to the rule, don't just say "wrong");
save the bulk of review commentary for architecture, tests, and correctness —
those are where senior-engineer judgment adds the most value.

---

## Cross-Language Consistency

If the project uses more than one language, don't apply Python conventions to
other files. Check whether a sibling skill exists for the language in
question (e.g. `google-cpp-style`, `google-java-style`, `google-go-style`,
`google-typescript-style`) and use that instead for non-Python files. If no
such skill is installed, say so explicitly rather than guessing — mixing style
guides across languages is worse than flagging the gap.
