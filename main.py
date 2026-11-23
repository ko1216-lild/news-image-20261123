#!/usr/bin/env python3
"""Entry program for the news-image-20261123 make.fun bounty.

The repository ships a pre-composed poster, entry.png, summing up the
world news of Monday 23 November 2026. This program delivers it to the
grader by copying it into the output directory under the name entry.png.
It uses only the Python standard library and no network.
"""

import hashlib
import os
import shutil
from pathlib import Path

IMAGE_NAME = "entry.png"


def output_dir() -> Path:
    # In the grader's container the output directory is /output; outside
    # it, MAKEFUN_OUTPUT_DIR stands in for that directory.
    return Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    source = Path(__file__).resolve().parent / IMAGE_NAME
    target_dir = output_dir()
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / IMAGE_NAME
    shutil.copyfile(source, target)
    # The program runs twice and both runs must write the same bytes, so
    # fail loudly rather than hand the grader a truncated or altered copy.
    if digest(target) != digest(source):
        raise SystemExit(f"integrity check failed: {target} differs from {source}")


if __name__ == "__main__":
    main()
