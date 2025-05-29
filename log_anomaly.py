#!/usr/bin/env python3
"""
CLI (A1–A5) → anomaly_log.jsonl

Example:
$ python log_anomaly.py \
      --date 2025-06-02 --group A --code A2 \
      --descr "A rare clue matched in the chat room" \
      --proof path/to/screenshot.png
"""

import argparse
import csv
import hashlib
import json
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).resolve().parent
ANOMALY_LOG = ROOT / "anomaly_log.jsonl"
CSV_PATH = ROOT / "log_template.csv"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def task_id_for_day(day: str, group: str) -> Optional[str]:
    if not CSV_PATH.exists():
        return None
    with CSV_PATH.open(newline="", encoding="utf-8") as f:
        rdr = csv.reader(f)
        header = next(rdr, None)
        if not header:
            return None
        idx_date = header.index("Date")
        idx_group = header.index("Group")
        idx_taskid = header.index("TaskID")
        for row in rdr:
            if row[idx_date] == day and row[idx_group] == group:
                return row[idx_taskid]
    return None


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", required=True, help="YYYY-MM-DD")
    ap.add_argument("--group", required=True, choices=["A", "B", "C"])
    ap.add_argument("--code", required=True, choices=["A1", "A2", "A3-1", "A3-2", "A4", "A5"])
    ap.add_argument("--descr", required=True, help="Free text description")
    ap.add_argument("--proof", type=Path, help="Proof file (jpg/png/log)")
    args = ap.parse_args()

    entry = {
        "date": args.date,
        "group": args.group,
        "code": args.code,
        "description": args.descr.strip(),
    }

    tid = task_id_for_day(args.date, args.group)
    if tid and tid.isdigit():
        entry["task_id"] = int(tid)

    if args.proof:
        if not args.proof.exists():
            ap.error("The proof file was not found.")
        entry["proof_sha256"] = sha256(args.proof)
        entry["proof_fname"] = args.proof.name

    with ANOMALY_LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    print(f"✅ Anomaly {args.code} {args.date} added.")


if __name__ == "__main__":
    main()
