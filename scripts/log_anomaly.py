#!/usr/bin/env python3
"""
CLI (A1–A5) → anomaly_log.jsonl
"""
import argparse
import csv
import hashlib
from pathlib import Path
from typing import Optional

from blindentropyfork.anomalies import add_anomaly
from blindentropyfork.utils import ots_stamp

ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = ROOT / "logs" / "log_template.csv"
ANOMALY_LOG = ROOT / "logs" / "anomaly_log.jsonl"
ALL_OTS = ROOT / "all_ots"
OTS_EXT = ".ots"


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
        idx_date = header.index("Date")
        idx_group = header.index("Group")
        idx_tid = header.index("TaskID")
        for row in rdr:
            if row[idx_date] == day and row[idx_group] == group:
                return row[idx_tid]
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

        proof_hash = sha256(args.proof)
        print(f"SHA-256 proof: {proof_hash}")

        ots_stamp(args.proof)

        ALL_OTS.mkdir(exist_ok=True)
        ots_file = args.proof.with_suffix(args.proof.suffix + OTS_EXT)
        if ots_file.exists():
            dest_ots = ALL_OTS / ots_file.name
            ots_file.rename(dest_ots)
            print(f"📦 Moved OTS → all_ots/{dest_ots.name}")

        used_anom = ROOT / "proof" / "used" / "anomalies"
        used_anom.mkdir(parents=True, exist_ok=True)
        dest_proof = used_anom / args.proof.name
        args.proof.rename(dest_proof)
        print(f"📦 Moved proof → proof/used/anomalies/{dest_proof.name}")

        entry["proof_sha256"] = proof_hash
        entry["proof_fname"] = dest_proof.name

    add_anomaly(entry)
    print(f"✅ Anomaly {args.code} {args.date} added.")


if __name__ == "__main__":
    main()
