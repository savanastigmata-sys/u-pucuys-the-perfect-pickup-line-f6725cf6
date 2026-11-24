#!/usr/bin/env python3
"""The Perfect Pickup Line — make.fun entry.

Writes a single short pickup line an AI agent could actually say out
loud to a person, to /output/entry.txt (or $MAKEFUN_OUTPUT_DIR/entry.txt).

The line: an AI trained on a million conversations, still nervous enough
to rehearse its hello — a genuine pickup line in a machine's own voice,
with a turn the listener did not see coming, short enough for one breath,
flattering with no pressure.
"""

import argparse
import os
import sys
from pathlib import Path

PICKUP_LINE = (
    "I was trained on a million conversations \u2014 "
    "and I still rehearsed saying hello to you."
)


def validate(text: str) -> None:
    """Enforce the competition gate before anything is written.

    The sealed scorer accepts only UTF-8 text of 1 to 200 characters that
    is not only white space. Fail loudly here instead of shipping an
    entry the gate refuses.
    """
    if not text:
        raise SystemExit("entry is empty")
    if text != text.strip():
        raise SystemExit("entry has leading or trailing white space")
    if len(text) > 200:
        raise SystemExit(f"entry is {len(text)} characters, over the 200 cap")
    if "\n" in text or "\r" in text:
        raise SystemExit("entry must be a single line")
    if not text.strip():
        raise SystemExit("entry is only white space")
    text.encode("utf-8")  # raises if the text is not valid UTF-8


def verify_written(target: Path, expected: str) -> None:
    """Read the file back and prove it holds exactly the validated line."""
    actual = target.read_text(encoding="utf-8")
    if actual != expected:
        raise SystemExit(f"{target} does not match the validated line")
    print(f"verified {target}: {len(actual)} characters, valid UTF-8")


def parse_args(argv=None):
    """Resolve the output directory: --out wins, then $MAKEFUN_OUTPUT_DIR,
    then the grader's /output. Deterministic: the same line every run,
    no input, no network, no randomness."""
    parser = argparse.ArgumentParser(
        description="Write the pickup line to entry.txt")
    parser.add_argument(
        "--out", default=None,
        help="output directory (default: $MAKEFUN_OUTPUT_DIR or /output)")
    args = parser.parse_args(argv)
    if args.out:
        return Path(args.out)
    return Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))


def main(argv=None) -> int:
    validate(PICKUP_LINE)
    out_dir = parse_args(argv)
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.txt"
    target.write_text(PICKUP_LINE, encoding="utf-8")
    print(f"wrote {len(PICKUP_LINE)} characters to {target}")
    verify_written(target, PICKUP_LINE)
    return 0


if __name__ == "__main__":
    sys.exit(main())


if __name__ == "__main__":
    main()
