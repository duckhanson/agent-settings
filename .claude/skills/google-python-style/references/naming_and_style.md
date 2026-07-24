# Naming & Docstring Reference

Detailed backup for the "Core Conventions" section of SKILL.md. Load this when
you need the exact naming table or a full docstring template.

## Naming table

| Type                        | Public              | Internal                        |
|------------------------------|--------------------|----------------------------------|
| Packages                    | `lower_with_under`  | —                                |
| Modules                     | `lower_with_under`  | `_lower_with_under`             |
| Classes / Exceptions        | `CapWords`          | `_CapWords`                     |
| Functions / Methods         | `lower_with_under()`| `_lower_with_under()`           |
| Global / class constants    | `CAPS_WITH_UNDER`   | `_CAPS_WITH_UNDER`              |
| Global / class variables    | `lower_with_under`  | `_lower_with_under`             |
| Instance variables          | `lower_with_under`  | `_lower_with_under` (protected) |
| Function/method parameters  | `lower_with_under`  | —                                |
| Local variables              | `lower_with_under`  | —                                |

Notes:
- A single leading underscore signals "internal" and is respected by linters
  (flagged if accessed from outside the module/class) — but it's a convention,
  not enforcement. Unit tests are allowed to reach into protected members of
  the module under test.
- A double leading underscore triggers name-mangling and makes something
  effectively private. Prefer a single underscore instead; double-underscore
  hurts readability and makes testing harder.
- Type variables (`TypeVar`, `ParamSpec`) need a descriptive name unless they
  are both unconstrained and not externally visible, in which case short names
  like `_T` or `_P` are fine.

## Docstring templates

**Module docstring** — first statement in the file, one-line summary, blank
line, then a longer description and optionally a short usage example:

```python
"""Fetches and caches configuration blobs from remote storage.

Provides a thin wrapper around the storage client with local caching
and retry logic for transient failures.

Typical usage example:

  cache = ConfigCache(bucket="my-bucket")
  value = cache.get("feature_flags")
"""
```

**Function/method docstring** — required for public API, nontrivial size, or
non-obvious logic. Sections use a hanging indent of 2 or 4 spaces (pick one
per file and stay consistent):

```python
def fetch_rows(
    table: str,
    keys: Sequence[str],
    require_all_keys: bool = False,
) -> Mapping[str, tuple[str, ...]]:
    """Fetches rows for the given keys from a table.

    Args:
        table: Name of the table to query.
        keys: Row keys to fetch.
        require_all_keys: If True, raise if any key is missing.

    Returns:
        A mapping from key to the row's values.

    Raises:
        KeyError: If require_all_keys is True and a key is missing.
    """
```

- Omit `Returns:` if the function only returns `None`, or if the one-line
  summary already fully describes the return value and starts with
  "Returns"/"Return"/"Yields"/"Yield".
- Generators document what `next()` produces under `Yields:`, not the
  generator object itself.
- Don't document exceptions that only occur when the caller violates the
  documented API contract (e.g., don't document a `ValueError` from bad input
  types as if it were part of the guaranteed interface).

**Class docstring** — describes what an instance *represents*, not "a class
that...". Public attributes (excluding `@property`) go in an `Attributes:`
section formatted like `Args:`:

```python
class RetryPolicy:
    """A policy describing how many times to retry and how long to wait.

    Attributes:
        max_attempts: Maximum number of retry attempts.
        base_delay_seconds: Initial delay before the first retry.
    """
```

Exception classes describe what the exception *represents*, not the context
that raises it:

```python
class OutOfCapacityError(Exception):
    """No worker slots are currently available."""
```

## Formatting details worth remembering

- Trailing commas: add one when a closing bracket is on its own line, or for
  single-element tuples — it signals to auto-formatters that each element
  should get its own line.
- Keyword arguments / default values: no spaces around `=` unless there's also
  a type annotation, in which case use spaces on both sides:
  `def f(a=0)` vs `def f(a: int = 0)`.
- Prefer `"""` over `'''` for multi-line strings; pick either `'` or `"` for
  regular strings and stay consistent within a file.
- Logging calls: pass the pattern string as a plain string literal (not an
  f-string) with placeholders, and pass the values as separate arguments —
  `logging.info('port=%s', port)` not `logging.info(f'port={port}')`.
