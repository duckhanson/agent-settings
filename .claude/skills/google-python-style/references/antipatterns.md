# Python Anti-Patterns (Google Style Guide)

Each item: why it's a problem, the fix, before/after.

## 1. Mutable default argument

Default values are evaluated once, at function-definition time — not once per
call. A mutable default is shared and mutated across every call that doesn't
override it.

```python
# Wrong
def add_item(item, bucket=[]):
    bucket.append(item)
    return bucket

# Right
def add_item(item, bucket: list | None = None):
    if bucket is None:
        bucket = []
    bucket.append(item)
    return bucket

# Also fine: an empty tuple is immutable, so it's a safe default
def process(items: Sequence = ()):
    ...
```

## 2. Bare or overly broad `except`

`except:` (bare) or `except Exception:` catches things you almost never want
to catch silently — typos turned into `NameError`, `KeyboardInterrupt`,
`SystemExit`, test framework internals. Only acceptable when re-raising, or at
a genuine isolation boundary (e.g., preventing one bad task from crashing an
entire worker pool), and even then it should be logged.

```python
# Wrong
try:
    do_work()
except Exception:
    pass

# Right
try:
    do_work()
except (ConnectionError, TimeoutError) as e:
    logging.warning('do_work failed, will retry: %s', e)
```

## 3. `assert` for input validation

`assert` statements can be stripped when Python runs with the `-O` optimize
flag, so they must never be load-bearing for program correctness — only for
internal sanity checks you could delete without changing behavior. Guard
public API inputs with real exceptions instead.

```python
# Wrong
def connect(port):
    assert port >= 1024, "port must be >= 1024"
    ...

# Right
def connect(port):
    if port < 1024:
        raise ValueError(f'port must be >= 1024, got {port}')
    ...
```

(Exception: inside `pytest`-based test functions, `assert` is the normal and
expected way to verify results.)

## 4. String concatenation in a loop

Repeated `+=` on a string can degrade toward quadratic time because each
concatenation may create a new string. Prefer collecting pieces and joining
once.

```python
# Wrong
html = '<ul>'
for item in items:
    html += f'<li>{item}</li>'
html += '</ul>'

# Right
parts = ['<ul>']
parts.extend(f'<li>{item}</li>' for item in items)
parts.append('</ul>')
html = ''.join(parts)
```

## 5. Explicit boolean/length comparisons

Python's implicit truthiness is idiomatic and usually faster; explicit
comparisons add noise and edge-case bugs.

```python
# Wrong
if len(users) == 0:
    ...
if is_active == True:
    ...

# Right
if not users:
    ...
if is_active:
    ...
```

Still always use `is None` / `is not None` for `None` checks — never rely on
`None`'s falsiness when a caller might legitimately pass another falsy value
(`0`, `''`, `[]`).

## 6. `x = x or default`

This silently treats *any* falsy value — `0`, `''`, `False` — as "not
provided," which is usually not what's intended.

```python
# Wrong
def f(count=None):
    count = count or 10  # count=0 gets silently replaced with 10

# Right
def f(count=None):
    if count is None:
        count = 10
```

## 7. Power features

Metaclasses, bytecode manipulation, dynamic attribute injection via
`getattr`/`setattr` for control flow, monkeypatching modules at runtime — all
technically available, all much harder to read, debug, and maintain than they
look. Reserve them for cases with no reasonable alternative. Standard-library
uses of these techniques (`abc.ABCMeta`, `dataclasses`, `enum`) are fine to
rely on since the complexity is already contained and well-tested.

## 8. Unnecessary `@staticmethod`

A `@staticmethod` is a function that happens to live inside a class but
doesn't need `self` or `cls`. It gets none of the benefits of being a method
and adds indirection. Prefer a plain module-level function; reserve
`@staticmethod` for the rare case of conforming to a third-party API that
requires it. Limit `@classmethod` to named constructors (`from_config(...)`)
or genuinely class-wide state.

```python
# Prefer this
def normalize(value: str) -> str:
    return value.strip().lower()

# Over this
class Formatter:
    @staticmethod
    def normalize(value: str) -> str:
        return value.strip().lower()
```

## 9. Combined imports on one line

```python
# Wrong
import os, sys

# Right
import os
import sys
```

## 10. f-strings in logging calls

```python
# Wrong — always renders the string even if the logger drops the message,
# and loses the ability to query/aggregate by the raw pattern
logging.info(f'Processed {count} rows in {elapsed:.2f}s')

# Right
logging.info('Processed %d rows in %.2fs', count, elapsed)
```

## 11. Relative imports

```python
# Wrong (inside package foo.bar)
from . import helpers

# Right
from foo.bar import helpers
```

## 12. Not closing stateful resources explicitly

Relying on garbage collection / `__del__` to close files, sockets, or
similar resources is fragile — timing isn't guaranteed and lingering
references (exception tracebacks, globals) can keep things open far longer
than intended.

```python
# Wrong
f = open('data.txt')
data = f.read()

# Right
with open('data.txt') as f:
    data = f.read()
```
