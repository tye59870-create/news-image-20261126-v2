#!/usr/bin/env python3
"""Decode the entry image and hand it to the judge.

Reads entry.png.b64 (base64 text of a PNG), checks that it really is a
1024x1024 PNG under 1 MiB, and writes the decoded bytes to
/output/entry.png unless --out names another path. Exits non-zero on any
failed check so a bad build can never be submitted by accident.
"""

import argparse
import base64
import os
import struct
import sys

PNG_SIG = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1024 * 1024
WANT_W, WANT_H = 1024, 1024


def fail(msg):
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(1)


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--in", dest="src",
                    default=os.path.join(here, "entry.png.b64"),
                    help="base64 input file (default: entry.png.b64 next "
                         "to this script)")
    ap.add_argument("--out", default="/output/entry.png",
                    help="PNG output path (default: /output/entry.png)")
    args = ap.parse_args()

    if not os.path.isfile(args.src):
        fail(f"input not found: {args.src}")

    raw = open(args.src, "rb").read()
    try:
        png = base64.b64decode(raw, validate=True)
    except Exception as exc:  # noqa: BLE001 - any decode failure is fatal
        fail(f"base64 decode failed: {exc}")

    if len(png) > MAX_BYTES:
        fail(f"PNG is {len(png)} bytes, over the 1 MiB limit")
    if len(png) < 33 or png[:8] != PNG_SIG:
        fail("not a PNG file (bad signature)")
    if png[12:16] != b"IHDR":
        fail("not a PNG file (first chunk is not IHDR)")
    width, height = struct.unpack(">II", png[16:24])
    if (width, height) != (WANT_W, WANT_H):
        fail(f"PNG is {width}x{height}, expected "
             f"{WANT_W}x{WANT_H}")

    out_dir = os.path.dirname(os.path.abspath(args.out))
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
    with open(args.out, "wb") as fh:
        fh.write(png)
    print(f"wrote {args.out} ({width}x{height}, {len(png)} bytes)")


if __name__ == "__main__":
    main()
