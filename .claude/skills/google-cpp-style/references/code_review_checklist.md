# Google-Style Code Review Checklist (C++)

Same five-step shape as the Python skill's checklist, with C++-specific risk
areas folded into each step. Work through them in order.

## Step 1 — Pre-screen

- Reasonably scoped diff, or does it bundle an unrelated refactor with a
  feature change?
- Does it include tests for new/changed behavior?
- Does the description match what the diff actually does?

## Step 2 — Architectural intent

- Does the header/API design fit how the rest of the codebase does things
  (e.g. existing ownership conventions, existing use of `absl::Status`-style
  error handling vs. something new and inconsistent)?
- Is ownership of any dynamically-allocated object unambiguous from the
  public API (smart pointer types, comments, or both)?
- Are new public types/functions justified, or is there something existing
  that already does this?
- Any new use of inheritance — is it a genuine "is-a" relationship, or would
  composition be clearer? Is multiple *implementation* inheritance being
  introduced (discouraged)?
- Are new macros defining part of a public API surface? (Should almost
  always be a function/template/`constexpr` instead.)

## Step 3 — Test coverage

- Do tests cover new/changed logic, not just the happy path?
- Are edge cases covered: null/empty inputs, boundary values, error/failure
  paths (especially anything using `absl::Status` or similar)?
- For anything touching ownership or lifetimes: is there a test that would
  catch a use-after-free, double-free, or leak (e.g. via sanitizers in CI)?
- Are RTTI/`dynamic_cast` usages (if any) confined to tests, as the style
  guide expects?

## Step 4 — Performance & correctness

- Any obvious quadratic-or-worse patterns (repeated linear scans, string
  concatenation in a loop, unnecessary copies of large objects)?
- Ownership/lifetime: any reference or raw pointer parameter that could
  outlive the object it points to? Any object with a non-trivial destructor
  given static/global storage duration?
- Const-correctness: are parameters/methods that don't mutate state marked
  `const`? Missing `const` is a real correctness/thread-safety signal, not
  just style.
- Thread-safety: any static/global mutable state accessed without
  synchronization? Any reliance on the atomicity of built-in operations?
- Exception safety: does anything `throw`/`catch`? (Should not, in Google
  C++ code — see antipatterns.md #1.)
- Casts: any C-style casts, or `reinterpret_cast`/`const_cast` used without
  clear justification?

## Step 5 — Style

Only after the above — check against `SKILL.md`'s "Core Conventions" and
`antipatterns.md`:
- Naming (naming table in `naming_and_style.md` — remember functions are
  `CapWords()` in C++, unlike Python).
- Header self-containment, include order/grouping.
- Class declaration order (public/protected/private, and the ordering within
  each).
- `explicit` on single-argument constructors/conversion operators.
- `override`/`final` on virtual overrides.
- Formatting — usually auto-fixable by `clang-format`/`cpplint`; call it out
  only if the formatter isn't configured or isn't catching it.

## Delivering the review

- Lead with ownership/lifetime/correctness findings — these are where C++
  reviews add the most value over what a linter catches.
- Group style findings at the end, phrased as pointers to the rule
  ("Google style: mark this constructor explicit — see antipatterns.md #3")
  rather than just "this is wrong."
- Distinguish must-fix (memory safety, UB, data races, security) from
  nice-to-have (naming, minor readability).
- If the project has an established local convention that differs from the
  global guide, don't force the global rule — local consistency wins.
