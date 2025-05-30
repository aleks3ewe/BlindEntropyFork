#!/usr/bin/env python3
"""
Stamp today's prethought file (any extension):
proof/prethought/YYYY-MM-DD_prethought.*

Creates .ots and prints SHA-256.
Moves the .ots into all_ots/ (no duplicate prefix).
"""

import hashlib
import subprocess
import sys
import time
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PRE_DIR = ROOT / "proof" / "prethought"
ALL_OTS = ROOT / "all_ots"
today = time.strftime("%Y-%m-%d")

cands = list(PRE_DIR.glob(f"{today}_prethought.*"))
if not cands:
    sys.exit("❌  Prethought file not found.")
f = cands[0]

h = hashlib.sha256(f.read_bytes()).hexdigest()
print("SHA-256:", h)

try:
    subprocess.run(["ots", "stamp", str(f)], check=True)
    print("✅  OTS-stamp done")
except Exception as e:
    print("⚠️  OTS failed:", e)

ALL_OTS.mkdir(exist_ok=True)
ots_file = PRE_DIR / (f.name + ".ots")
if ots_file.exists():
    dest = ALL_OTS / ots_file.name
    shutil.move(str(ots_file), str(dest))
    print(f"📦 Moved → all_ots/{dest.name}")
else:
    print("⚠️  No .ots file to archive.")
