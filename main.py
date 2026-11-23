#!/usr/bin/env python3
"""Copy the pre-rendered front page to the output directory.

The image is rendered by render.py (in the notes directory) and stored in
this repository as entry.png. This program only copies it, verifies the copy
by SHA-256 and size, and exits 0. Standard library only.
"""
import hashlib
import os
import shutil
import sys

EXPECTED_SHA256 = "c98c72ba6271ca27a1e6ff1bf45616053261093ca89501c0806bb048f45352c5"
MAX_BYTES = 1048576


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    with open(src, "rb") as f:
        data = f.read()
    if len(data) > MAX_BYTES:
        print("entry.png exceeds 1 MiB", file=sys.stderr)
        return 1
    if hashlib.sha256(data).hexdigest() != EXPECTED_SHA256:
        print("entry.png sha256 mismatch", file=sys.stderr)
        return 1
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        print("entry.png is not a PNG", file=sys.stderr)
        return 1
    # The hash is pinned so a corrupted or swapped image can never be
    # submitted silently: both runs of the program must produce these bytes.
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    targets = {out_dir, "/output"}
    for out_dir in targets:
        os.makedirs(out_dir, exist_ok=True)
        dst = os.path.join(out_dir, "entry.png")
        shutil.copyfile(src, dst)
        with open(dst, "rb") as f:
            copied = f.read()
        if hashlib.sha256(copied).hexdigest() != EXPECTED_SHA256:
            print("copy to %s failed verification" % out_dir, file=sys.stderr)
            return 1
    print("entry.png: %d bytes, sha256 %s" % (len(data), EXPECTED_SHA256))
    return 0


if __name__ == "__main__":
    sys.exit(main())
