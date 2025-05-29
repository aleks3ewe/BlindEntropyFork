#!/usr/bin/env python3
"""
BlindEntropyFork daily roll (for A/B/C).

Format CSV (+ auto-header):
Date,Group,Raw,TaskID,EncTaskID,Done,Anomaly,PreHash,Proof
"""

import argparse
import csv
import datetime as dt
import hashlib
import sys
from pathlib import Path

import requests
from encrypt_utils import encrypt_task_id

ROOT = Path(__file__).resolve().parent
CSV_PATH = ROOT / "log_template.csv"
PRE_DIR = ROOT / "Proof" / "prethought"
USED_PRE_DIR = ROOT / "Proof" / "used" / "prethought"
NUM_TASKS = 25
QRNG_API = "https://qrng.anu.edu.au/API/jsonI.php?length=1&type=uint8"


def fetch_qrng_byte() -> int:
    r = requests.get(QRNG_API, timeout=10)
    r.raise_for_status()
    return int(r.json()["data"][0])


def sha256_of_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def newest_prethought() -> Path:
    files = [f for f in PRE_DIR.glob("*") if f.is_file()]
    if not files:
        sys.exit("❌ No prethought (A4). Write the file in Proof/prethought/ and repeat.")
    return max(files, key=lambda f: f.stat().st_mtime)


def today_str() -> str:
    return dt.datetime.now().strftime("%Y-%m-%d")


def already_rolled(group: str) -> bool:
    if not CSV_PATH.exists():
        return False
    with CSV_PATH.open(newline="", encoding="utf-8") as f:
        rdr = csv.reader(f)
        next(rdr, None)  # header
        return any(row[0] == today_str() and row[1] == group for row in rdr)


def append_row(row: list[str]) -> None:
    file_exists = CSV_PATH.exists()
    with CSV_PATH.open("a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if not file_exists:
            w.writerow(
                ["Date", "Group", "Raw", "TaskID", "EncTaskID",
                 "Done", "Anomaly", "PreHash", "Proof"]
            )
        w.writerow(row)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--group", choices=["A", "B", "C"], required=True,
                    help="A = human-action; B = control; C = cloud-based AI")
    ap.add_argument("--key", help="256-bit AES-GCM hex key (C only).")
    args = ap.parse_args()

    if already_rolled(args.group):
        sys.exit("⚠️ The cast for this group is already logged today.")

    raw = fetch_qrng_byte()
    task_id = raw % NUM_TASKS + 1

    pre_hash = proof = "—"
    done = "N"
    enc_task_id = "—"

    if args.group == "A":
        pre_file = newest_prethought()
        pre_hash = sha256_of_file(pre_file)
        USED_PRE_DIR.mkdir(parents=True, exist_ok=True)
        pre_file.rename(USED_PRE_DIR / pre_file.name)

    elif args.group == "C":
        if not args.key:
            sys.exit("❌ For group C, --key <HEX256> is mandatory.")
        enc_task_id = encrypt_task_id(args.key, task_id)
        task_id = "—"

    row = [
        today_str(),
        args.group,
        str(raw),
        str(task_id),
        enc_task_id,
        done,
        "—",
        pre_hash,
        proof,
    ]
    append_row(row)

    print(f"✅ {args.group}-roll write: Raw={raw}, TaskID={task_id}" +
          (f", Enc={enc_task_id[:12]}…" if args.group == "C" else ""))


if __name__ == "__main__":
    main()
