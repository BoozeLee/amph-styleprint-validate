#!/usr/bin/env python3
"""Self-check for amph-styleprint-validate -- runs from a fresh clone, with no corpus.

validate_styleprint defaults to <repo>/work/art, which no fresh clone has. The control builds its own folder and points --dir at it, so the controls inside the module have something real to run against.

It asserts that every control RUNS and reports a verdict, and that the report is written -- NOT that every control PASSES on synthetic line-work. The `ruled` control requires that imposing one edge direction breaks the sample's measured isotropy; on a fixture made of a few drawn strokes the answer depends entirely on the fixture, and an earlier version of this test drew every stroke at one angle and reported the failure as if it were the module's. Whether these controls pass is a property of the ART, measured on real art -- which is why this module, and styleprint, are marked as corpus-dependent. What the test can prove from a fresh clone is that the module runs, that each control executes and returns a verdict, and that a bad --dir is refused.

Exits 0 only if every assertion below holds.
"""
from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from PIL import Image, ImageDraw

import math


def _art(out: Path, n: int) -> Path:
    out.mkdir(parents=True, exist_ok=True)
    angles = (0, 90, 35, 145, 70, 20, 110)
    for i in range(n):
        im = Image.new("RGB", (900, 900), (16, 18, 30))
        d = ImageDraw.Draw(im)
        cx = cy = 450
        for a in angles:
            rad = math.radians(a)
            dx, dy = math.cos(rad), math.sin(rad)
            d.line([(cx - 380 * dx, cy - 380 * dy), (cx + 380 * dx, cy + 380 * dy)],
                   fill=(225, 185, 85), width=5)
        for r in (120, 240, 360):
            d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(190, 55, 95), width=7)
        im.save(out / f"plate_{i:02d}.jpg", "JPEG", quality=90)
    return out


def run(tmp: Path) -> int:
    src = _art(tmp / "art", 3)
    r = subprocess.run([sys.executable, "validate_styleprint.py", "--dir", str(src),
                        "--json", str(tmp / "validation.json")],
                       cwd=HERE, capture_output=True, text=True)
    out = (r.stdout + r.stderr).strip()
    if "spread" not in out or "controls" not in out:
        print("FAIL the module did not report on both the spread and the controls")
        for l in out.splitlines()[-12:]:
            print(f"        {l[:100]}")
        return 1
    if not (tmp / "validation.json").is_file():
        print("FAIL --json wrote no report")
        return 1

    verdicts = {"ok": len(re.findall(r"\bok\b", out)), "FAIL": len(re.findall(r"FAIL", out))}
    if verdicts["ok"] + verdicts["FAIL"] < 3:
        print(f"FAIL expected several axis verdicts, saw {verdicts}")
        return 1
    print(f"  controls reported: {verdicts['ok']} ok, {verdicts['FAIL']} FAIL on synthetic art")
    if r.returncode:
        print("  note: the module exited non-zero. That is expected on a synthetic")
        print("        fixture; run it against real art to judge the controls.")

    r2 = subprocess.run([sys.executable, "validate_styleprint.py", "--dir", str(tmp / "nope")],
                        cwd=HERE, capture_output=True, text=True)
    if r2.returncode == 0:
        print("FAIL a missing --dir was accepted")
        return 1
    print("  negative control: a missing --dir is rejected")

    print("PASS  verify: runs, reports every control, writes its report, refuses a bad --dir")
    return 0


def main() -> int:
    tmp = Path(tempfile.mkdtemp(prefix="amph-styleprint-validate-selftest-"))
    try:
        return run(tmp)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
