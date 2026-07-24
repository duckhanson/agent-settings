# Google-Style Code Review Checklist (Python)

A senior-engineer review looks at more than formatting. Work through these
five steps in order; don't jump straight to style nits.

## Step 1 — Pre-screen

- Is the change reasonably scoped, or does it bundle unrelated changes
  (refactor + feature + formatting-only diffs all in one)? If so, suggest
  splitting before doing a deep review.
- Does the diff include tests for new/changed behavior? Note it now; verify
  depth in Step 3.
- Is the PR/commit description accurate — does it describe what the diff
  actually does?

## Step 2 — Architectural intent

- Does the change actually solve the stated problem, and is this the right
  place in the codebase for the logic to live?
- Does it fit existing patterns in the module/package, or does it introduce a
  parallel, inconsistent way of doing something the codebase already does
  elsewhere?
- Are new public functions/classes/modules justified, or could this reuse
  something that already exists?
- Are interfaces (function signatures, class APIs) minimal and stable, or do
  they leak implementation details that will be painful to change later?
- Flag anything that looks like premature abstraction (speculative
  generality for a "future" need that isn't concretely justified yet).

## Step 3 — Test coverage

- Do tests actually exercise the new/changed logic, not just the happy path?
- Are edge cases covered: empty inputs, `None`, boundary values, error paths?
- For bug fixes: is there a regression test that would have caught the bug?
- Do tests assert on behavior, not on implementation details that would break
  on a harmless refactor?
- Are test names descriptive (`test_<method>_<condition>`) rather than
  generic (`test_1`, `test_it_works`)?

## Step 4 — Performance & correctness

- Any obvious algorithmic complexity problems (quadratic behavior from
  string concatenation or repeated linear scans in a loop, N+1 query
  patterns, unnecessary copies of large structures)?
- Resource handling: are files/sockets/connections closed via `with` or
  `contextlib.closing()`? Any resource leaks on error paths?
- Concurrency: does the code rely on the atomicity of built-in types (dicts,
  variable assignment) across threads? Is `queue.Queue` or a proper lock used
  instead?
- Exception handling: are exceptions narrow and specific, or is
  `except Exception`/bare `except:` swallowing errors? (See
  `antipatterns.md` #2.)
- Mutable global state: is there any, and if so is it justified, prefixed
  with `_`, and accessed only through public functions/methods?

## Step 5 — Style

Only after the above — check against `SKILL.md`'s "Core Conventions" and
`antipatterns.md`:
- Naming conventions (naming table in `naming_and_style.md`).
- Docstrings present where required, correctly formatted.
- Import grouping/ordering, no relative imports, one per line.
- Formatting (line length, indentation, whitespace) — usually auto-fixable
  by Black/Pyink if the project has it configured; call it out only if the
  formatter isn't catching it.
- Any of the anti-patterns in `antipatterns.md`.

## Delivering the review

- Lead with architecture/tests/correctness findings — that's where judgment
  adds the most value.
- Group style findings together at the end, phrased as pointers to the rule
  ("Google style: avoid mutable default args — see antipatterns.md #1") not
  just "this is wrong."
- Distinguish must-fix (correctness, security, data loss risk) from
  nice-to-have (style, minor readability) so the author can prioritize.
- If something is a matter of local convention rather than the style guide
  (e.g. project already does X differently everywhere), don't force the
  global rule — consistency with surrounding code wins locally.
