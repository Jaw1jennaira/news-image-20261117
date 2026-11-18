#!/usr/bin/env python3
"""Entry program: copy the bundled front-page image to the output dir.

The image (entry.png, 1024x1024, rendered at build time by render.py)
is the entry; this program only copies it, so two runs write byte-identical
output. Standard library only; no network.
"""
import os
import shutil


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    here = os.path.dirname(os.path.abspath(__file__))
    shutil.copyfile(os.path.join(here, "entry.png"),
                    os.path.join(out_dir, "entry.png"))


if __name__ == "__main__":
    main()
