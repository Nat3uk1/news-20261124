#!/usr/bin/env python3
"""Copy the bundled poster (entry.png) to the output directory.

Standard library only; no network access. The output directory comes
from MAKEFUN_OUTPUT_DIR, defaulting to /output. Writes entry.png and
prints the number of bytes written.
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    src = os.path.join(HERE, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    size = os.path.getsize(dst)
    print(f"Wrote {size} bytes to {dst}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
