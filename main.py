#!/usr/bin/env python3
"""Runner for the 26 November 2026 front page (make.fun news-image-20261126).

The page ships in this repository as plain base64 text (entry.png.b64) so
the tree stays text-only. This script decodes that text, verifies it is a
1024x1024 PNG under 1 MiB, and writes it to /output/entry.png (or to the
path given with --out). Pure standard library, no network, no randomness:
the same bytes come out on every run.

Run it with:  python3 main.py  (or: python3 main.py --out out.png)
"""
import argparse
import base64
import hashlib
import struct
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
BUNDLED_B64 = HERE / "entry.png.b64"
OUT_DEFAULT = Path("/output/entry.png")

MAGIC = b"\x89PNG\r\n\x1a\n"
WANT_W, WANT_H = 1024, 1024
SIZE_CAP = 1024 * 1024


def load_png_bytes(path):
    """Decode the base64 text file at path into raw PNG bytes."""
    encoded = path.read_text(encoding="utf-8").strip()
    return base64.b64decode(encoded, validate=True)


def read_png_size(data):
    """Pull (width, height) from a PNG's IHDR chunk."""
    if len(data) < 33 or data[:8] != MAGIC:
        raise ValueError("not a PNG file")
    length, kind = struct.unpack(">I4s", data[8:16])
    if kind != b"IHDR" or length != 13:
        raise ValueError("PNG has no IHDR chunk first")
    width, height = struct.unpack(">II", data[16:24])
    return width, height


def validate(data):
    """Refuse anything that is not our 1024x1024 PNG under 1 MiB."""
    if len(data) > SIZE_CAP:
        raise ValueError(f"image is {len(data)} bytes, over the 1 MiB cap")
    size = read_png_size(data)
    if size != (WANT_W, WANT_H):
        raise ValueError(f"image is {size[0]}x{size[1]}, expected 1024x1024")
    return size


def parse_cli(argv=None):
    parser = argparse.ArgumentParser(
        description="Write the bundled front-page PNG to disk.")
    parser.add_argument("--out", type=Path, default=OUT_DEFAULT,
                        help="where to write entry.png (default: %(default)s)")
    return parser.parse_args(argv)


def run(argv=None):
    args = parse_cli(argv)
    data = load_png_bytes(BUNDLED_B64)
    size = validate(data)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_bytes(data)
    digest = hashlib.sha256(args.out.read_bytes()).hexdigest()
    print(f"wrote {args.out} ({size[0]}x{size[1]}, {len(data)} bytes, "
          f"sha256={digest})")
    return 0


if __name__ == "__main__":
    sys.exit(run())
