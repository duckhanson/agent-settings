---
name: google-cpp-style
description: Enforces Google's C++ Style Guide (google.github.io/styleguide/cppguide.html) when writing, editing, or reviewing C++ code. Covers naming conventions, formatting, header/include rules, exception-free error handling, ownership and smart pointer usage, casting rules, and common anti-patterns (raw new/delete, exceptions, non-explicit single-arg constructors, macros as APIs, etc.), plus a structured Google-style code review process (architecture intent, test coverage, performance, style). Use this whenever writing new C++ code, editing existing .cc/.h files, reviewing a C++ PR/diff, or when the user mentions C++ style, cpplint, Google C++ style guide, or "how should I review this C++ code." In multi-language repos, pair with sibling Google style skills for other languages (e.g. google-python-style, google-java-style) so all languages stay consistent with their respective Google style guide.
---

# Google C++ Style

Applies Google's official C++ Style Guide to code generation, editing, and
review. Source of truth: https://google.github.io/styleguide/cppguide.html
(mirrors https://github.com/google/styleguide). This skill paraphrases and
operationalizes that guide — it is not a verbatim copy. Google's C++ guide
targets C++20 currently (not C++23 features); check `references/` for the
version-specific notes if relevant.

Use this skill for two distinct jobs:

1. **Writing/editing C++** — apply the conventions below automatically.
2. **Reviewing C++ code** — follow the 5-step review process in
   `references/code_review_checklist.md` (shared structure with the Python
   skill, adapted for C++-specific risk areas like ownership and UB).

Load `references/` files when you need the exact naming table, the full
anti-pattern list with examples, or the review checklist.

---

## Core Conventions (apply by default)

**Naming** (full table in `references/naming_and_style.md`)
- Files: `lower_snake_case.h` / `lower_snake_case.cc`.
- Types (classes, structs, enums, type aliases, template parameters): `CapWords` (`UrlTable`, `PropertiesMap`).
- Functions and methods: `CapWords()` — yes, functions are CapWords in Google
  C++, unlike most other Google style guides (`AddTableEntry()`, `DeleteUrl()`).
  Accessors may match the variable name (`int count() const`).
- Variables (local, parameters): `lower_snake_case` (`table_name`).
- Class/struct data members: `lower_snake_case_` with a **trailing
  underscore** (`num_entries_`); struct members that behave like a plain data
  bag may omit it if the struct has no invariants.
- Constants (anything with static storage duration whose value is fixed for
  the program's life, `constexpr`, or otherwise): `kCamelCase` (`kMaxOpenFiles`).
- Namespaces: `lower_snake_case`, based on the project/path name; do not use
  inline namespaces.
- Macros (avoid macros in general — see Anti-Patterns): `CAPS_WITH_UNDER`.
- Enumerators: treated like constants — `kCamelCase`.

**Formatting**
- 2-space indentation. Never tabs.
- 80-character line limit.
- Spaces around binary operators, no spaces just inside parentheses.
- Braces: opening brace stays on the same line as the statement it belongs to
  (function, class, if/for/while); Google style does not use Allman/next-line
  braces.
- Pointer/reference `*`/`&` binds to the type in declarations where possible
  (`int* x`), but be consistent with surrounding code — this is a "be
  consistent" rule, not a hard requirement.
- Use `cpplint.py` to catch mechanical style violations; treat it the way the
  Python skill treats `pylint` — suppress with a reason when a warning is a
  false positive, don't silently ignore it.

**Headers & includes**
- Every `.h` must be self-contained (compiles on its own) with a `#define`
  guard named `<PROJECT>_<PATH>_<FILE>_H_`.
- Include order, blank line between each group, alphabetical within a group:
  1. The related header (for a `.cc` file implementing `foo.h`, that's `foo.h` first)
  2. C system headers
  3. C++ standard library headers
  4. Other libraries' headers
  5. Your project's headers
- Prefer `#include` over forward declarations unless there's a proven,
  necessary compile-time win.
- Don't rely on transitive includes — include what you directly use.

**Classes**
- Data members are `private` unless they're constants; expose access through
  accessor methods when needed.
- Declaration order within each access section: type aliases → static
  constants → factory functions → constructors/assignment → destructor →
  other methods → other data members. Sections ordered `public`, `protected`,
  `private` (omit empty ones).
- Mark single-argument constructors and conversion operators `explicit`
  unless an implicit conversion is genuinely intended (rare — see
  Anti-Patterns #3).
- Every class's public API must make clear whether it's copyable, move-only,
  or neither — declare or `= delete` the relevant constructors/operators
  rather than leaving it implicit and unobvious.
- Prefer composition over inheritance; when you do inherit, make it `public`,
  mark overrides with `override` (or `final`), and avoid multiple
  *implementation* inheritance (multiple interface inheritance is fine).

**Functions**
- Prefer return values over output parameters.
- Put all input-only parameters before output parameters.
- Keep functions short and focused; ~40 lines is the point to reconsider
  splitting, not a hard limit.
- Prefer normal leading-return-type syntax; use trailing return type
  (`auto f() -> int`) only where required (lambdas) or where it materially
  improves readability in template-heavy code.

**Types & casting**
- Use `int` for ordinary integers; use fixed-width types (`int64_t`,
  `uint32_t`, etc.) from `<cstdint>` only when you need a guaranteed size.
  Avoid `short`/`long`/`long long`.
- Only `float` and `double` — never `long double`.
- Never C-style casts (`(int)x`). Use, in order of preference: brace
  initialization (`int64_t{x}`) for arithmetic conversions, a function-style
  cast for class types, `absl::implicit_cast`/`static_cast` for up/related
  casts, `absl::down_cast`/`dynamic_cast` for down-casts, `const_cast` only to
  strip `const`, `reinterpret_cast` only for genuinely unsafe pointer/integer
  reinterpretation.
- Use `nullptr` for null pointers, never a literal `0` or `NULL`.
- Use `const` on any parameter, method, or non-local variable that the code
  doesn't need to mutate; mark methods `const` unless they change logical
  state.
- Use type deduction (`auto`) only when it makes code clearer or safer to a
  reader unfamiliar with the project — not merely to save typing.

---

## Anti-Patterns to Avoid (flag or fix these)

Full list with wrong/right examples in `references/antipatterns.md`. Highest-value:

1. **Throwing/catching C++ exceptions** — Google C++ code does not use
   exceptions. Signal errors via return values, `absl::Status`-style types,
   or (for truly unrecoverable conditions) `CHECK`/program termination —
   never `throw`/`try`/`catch` in new Google-style code.
2. **`new`/`delete` with manual lifetime tracking** — prefer `std::unique_ptr`
   for exclusive ownership, `std::shared_ptr` only when shared ownership is
   genuinely required (and prefer `shared_ptr<const T>` when possible).
   Never use `std::auto_ptr`.
3. **Non-`explicit` single-argument constructors / conversion operators** —
   these enable silent, surprising implicit conversions. Mark them `explicit`
   unless the type is deliberately designed to be interchangeable with another.
4. **C-style casts** — ambiguous between conversion and reinterpretation; use
   the appropriate C++-style cast instead (see Types & casting above).
5. **RTTI-based type switching** (`typeid`/chained `dynamic_cast` decision
   trees) — usually signals a design problem; prefer virtual dispatch or the
   Visitor pattern.
6. **Macros used to define API surface** — e.g. macros that expand into class
   members or generate public interfaces. Prefer `inline` functions, `enum`,
   `const`/`constexpr` variables, and templates. If a macro is unavoidable,
   `#define` right before use and `#undef` right after; never leave macros
   exported from a header.
7. **Static/global variables with non-trivial destructors** — forbidden
   unless trivially destructible; use a function-local `static` pointer/
   reference (leaked deliberately) for cases that truly need a global,
   non-trivial object.
8. **Using-directives** (`using namespace foo;`) — pollutes the namespace;
   always banned. Namespace aliases in headers are restricted to
   internal-only namespaces.
9. **Virtual calls from constructors/destructors** — never dispatch to a
   subclass override during construction/destruction; use a factory function
   or `Init()` method instead if subclass-specific setup is needed.
10. **Unsigned types to mean "never negative"** — unsigned wraps on
    underflow instead of erroring, which hides bugs. Use assertions/checks to
    express non-negativity; reserve unsigned types for bit patterns and
    modular arithmetic.
11. **Post-increment/decrement (`i++`) when the value isn't used** — prefer
    prefix (`++i`); it's never less efficient and often more.
12. **Overloading `&&`, `||`, comma, or unary `&`**, or defining
    `operator""` (user-defined literals) — all explicitly banned.

---

## Code Review Process

Same 5-step structure as the Python skill, adapted for C++ risk areas —
see `references/code_review_checklist.md`:

1. Pre-screen (scope, description accuracy, tests present)
2. Architectural intent (ownership model clarity, header/API design, does it
   fit existing patterns)
3. Test coverage (including sanitizer/UB-relevant edge cases)
4. Performance & correctness (lifetime/UB risks, unnecessary copies, const
   correctness, thread-safety of shared/static state)
5. Style (naming, formatting, anti-patterns from this file)

Lead with architecture/tests/correctness; group style feedback at the end.

---

## Cross-Language Consistency

Don't apply these C++ conventions to non-C++ files. Check whether a sibling
skill exists for the language in question (e.g. `google-python-style`,
`google-java-style`, `google-go-style`) and use that instead. If none is
installed, say so explicitly rather than guessing.
