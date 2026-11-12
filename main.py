#!/usr/bin/env python3
"""Cutest picture entry: copy entry.png byte-for-byte to /output/entry.png.

Standard library only, no network, deterministic: the output is an exact
copy of the bundled entry.png, so two runs write identical bytes.
"""
import hashlib
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    src = os.path.join(HERE, "entry.png")
    dst = os.path.join(out_dir, "entry.png")
    with open(src, "rb") as f:
        if f.read(len(PNG_MAGIC)) != PNG_MAGIC:
            print("entry.png is not a PNG file", file=sys.stderr)
            sys.exit(1)
    shutil.copyfile(src, dst)
    src_digest = sha256_of(src)
    if src_digest != sha256_of(dst):
        print("copy integrity check failed", file=sys.stderr)
        sys.exit(1)
    if os.path.getsize(dst) != os.path.getsize(src):
        print("copy size mismatch", file=sys.stderr)
        sys.exit(1)
    print(f"wrote {dst} ({os.path.getsize(dst)} bytes, sha256 {src_digest})",
          file=sys.stderr)


if __name__ == "__main__":
    main()
