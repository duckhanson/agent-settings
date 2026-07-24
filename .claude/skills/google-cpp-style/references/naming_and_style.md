# Naming & Formatting Reference (Google C++)

## Naming table

| Entity                              | Convention              | Example                         |
|--------------------------------------|--------------------------|----------------------------------|
| File names                          | `lower_snake_case`       | `url_table.h`, `url_table.cc`   |
| Type names (class/struct/enum/alias)| `CapWords`               | `UrlTable`, `UrlTableTester`     |
| Function/method names               | `CapWords()`             | `AddTableEntry()`, `DeleteUrl()`|
| Variable names (local, parameter)   | `lower_snake_case`       | `table_name`                    |
| Class/struct data members           | `lower_snake_case_`      | `num_entries_` (trailing `_`)   |
| Struct members (no invariants)      | `lower_snake_case`       | `count` (trailing `_` optional) |
| Constants (any fixed-for-lifetime value) | `kCamelCase`        | `kMaxOpenFiles`                  |
| Namespace names                     | `lower_snake_case`       | `websearch_result`               |
| Enumerators                         | `kCamelCase`             | `kMonday`, `kTuesday`            |
| Macros (avoid where possible)       | `CAPS_WITH_UNDER`        | `MYPROJECT_ROUND(x)`             |
| Template parameters                 | `CapWords` (types) or short single letters for generic parameters | `T`, `Iterator` |

Notes:
- Functions being `CapWords()` is the single biggest surprise for people
  coming from other Google style guides (Python uses `lower_with_under`).
  Double-check this when switching context between languages in the same
  review.
- "Constant" means static storage duration with a value fixed for the
  program's life, not just anything declared `const` — a `const` function
  parameter or local variable does *not* get the `k` prefix, only true
  constants do.
- Accessor methods are commonly named after the underlying member without a
  `Get`/`Set` prefix: `int count() const` paired with `void set_count(int c)`.

## File & header conventions

- Header guard format: `<PROJECT>_<PATH>_<FILE>_H_`, derived from the full
  project-relative path, e.g. `foo/bar/baz.h` in project `foo` guards with
  `FOO_BAR_BAZ_H_`.
- Every `.cc` file should generally have a matching `.h`; exceptions are unit
  test files and small `.cc` files containing only `main()`.
- Include order (blank line between each non-empty group, alphabetical
  within a group):
  1. The related header (e.g. `foo2.h` at the top of `foo2.cc`)
  2. C system headers (angle brackets, `.h`, e.g. `<unistd.h>`)
  3. C++ standard library headers (angle brackets, no extension, e.g. `<vector>`)
  4. Other libraries' headers
  5. Your project's headers

```cpp
#include "foo/server/fooserver.h"

#include <sys/types.h>
#include <unistd.h>

#include <string>
#include <vector>

#include "base/basictypes.h"
#include "foo/server/bar.h"
#include "third_party/absl/flags/flag.h"
```

## Formatting details

- 2-space indentation, no tabs.
- 80-character line limit.
- Opening brace on the same line as the function/class/control-statement
  header (K&R-ish "Google" style), not on its own line:

```cpp
if (condition) {
  DoSomething();
} else {
  DoSomethingElse();
}
```

- No space just inside parentheses: `Foo(a, b)` not `Foo( a, b )`.
- Spaces around binary operators: `x = a + b;` not `x=a+b;`.
- Prefer `int* x` (pointer binds to type) but stay consistent with the
  surrounding file if it already uses `int *x`.
- Namespace contents are not indented; closing brace gets a comment naming
  the namespace: `}  // namespace mynamespace`. Unnamed namespaces close with
  an empty comment: `}  // namespace`.

## Class declaration order

Within each of `public:`, `protected:`, `private:` (in that order, omitting
empty sections):

1. Types and type aliases
2. (structs only, optionally) non-static data members
3. Static constants
4. Factory functions
5. Constructors and assignment operators
6. Destructor
7. All other methods (static and non-static)
8. All other data members

```cpp
class UrlTable {
 public:
  using EntryMap = std::map<std::string, UrlTableEntry>;

  static constexpr int kDefaultCapacity = 100;

  static UrlTable* CreateWithCapacity(int capacity);

  UrlTable();
  UrlTable(const UrlTable&) = delete;
  UrlTable& operator=(const UrlTable&) = delete;
  ~UrlTable();

  void AddEntry(const std::string& url, const UrlTableEntry& entry);

 private:
  EntryMap entries_;
};
```
