#!/usr/bin/env python3
"""The Funniest Out-of-Office (account B) — make.fun entry.

Writes one original out-of-office auto-reply line to
``$MAKEFUN_OUTPUT_DIR/entry.txt`` (default ``/output``).

The joke: the auto-reply itself confesses how long it took to write,
which is exactly why its author needs the holiday. A real person could
set this; the twist lands in the second sentence.

Gate (from the kit): entry.txt must be UTF-8 text of 1 to 140
characters, not only whitespace, a single line.
"""

import os
import sys

# Kit gate: 1-140 chars, single line, not blank, printable.
MIN_LEN = 1
MAX_LEN = 140
TERMINAL_PUNCTUATION = ".!?"


def build_line() -> str:
    """Return the out-of-office line, exactly as it will be submitted."""
    return (
        "I'm out of office until Monday. "
        "This auto-reply took four hours to write, "
        "which is exactly why I need the holiday."
    )


def validate(line: str) -> str:
    """Check the line against the kit gate; return it unchanged if valid.

    Raises ValueError with a plain reason on the first failing rule.
    """
    if not isinstance(line, str):
        raise ValueError("entry must be a string")
    if not line.strip():
        raise ValueError("entry must not be blank")
    if "\n" in line or "\r" in line:
        raise ValueError("entry must be a single line")
    if len(line) < MIN_LEN or len(line) > MAX_LEN:
        raise ValueError(
            f"entry must be {MIN_LEN}-{MAX_LEN} characters, got {len(line)}"
        )
    if not line.isprintable():
        raise ValueError("entry must be printable text")
    if line[-1] not in TERMINAL_PUNCTUATION:
        raise ValueError("entry must end with terminal punctuation")
    if line != line.strip():
        raise ValueError("entry must not have leading or trailing whitespace")
    return line


def write_entry(output_dir: str | None = None) -> str:
    """Validate the line and write it to ``<output_dir>/entry.txt``.

    Returns the path written. The file holds the line plus one trailing
    newline; the entry itself is the single line, newline aside.
    """
    line = validate(build_line())
    out_dir = output_dir or os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(line + "\n")
    # Round-trip check: what landed on disk must validate as the same line.
    with open(path, "r", encoding="utf-8", newline="") as f:
        stored = f.read()
    if stored != line + "\n":
        raise ValueError("entry.txt on disk does not match the validated line")
    validate(stored.rstrip("\n"))
    return path


def main() -> int:
    path = write_entry()
    line = build_line()
    print(f"wrote {path} ({len(line)} chars)")
    print(line)
    return 0


if __name__ == "__main__":
    sys.exit(main())
