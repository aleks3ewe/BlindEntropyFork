#!/usr/bin/env python3
"""
BlindEntropyFork daily roll script
---------------------------------
1. Get the newest file in Proof/prethought/
2. SHA-256 hash -> pre_hash
3. Fetch 1 quantum byte from ANU QRNG
4. Compute task_id = raw % 25 + 1
5. Append a line to log_template.csv:
   Date,Raw,TaskID,Done,Anomaly,PreHash,Proof
---------------------------------
"""

import csv
import datetime as dt
import hashlib
import requests
import sys
from pathlib import Path

ROOT = Path(r"")
PRE_DIR = ROOT / "Proof" / "prethought"
USED_DIR = ROOT / "Proof" / "used" / "prethought"
CSV_PATH = ROOT / "log_template.csv"
NUM_TASKS = 25
QRNG_API = "https://qrng.anu.edu.au/API/jsonI.php?length=1&type=uint8"


def newest_prethought(directory: Path) -> Path:
    files = [f for f in directory.glob("*") if f.is_file()]
    if not files:
        sys.exit("❌  No prethought file found – record A4 before running script.")
    return max(files, key=lambda f: f.stat().st_mtime)


def sha256_of_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def fetch_qrng_byte() -> int:
    r = requests.get(QRNG_API, timeout=10)
    r.raise_for_status()
    return int(r.json()["data"][0])


def already_rolled_today(csv_file: Path, today: str) -> bool:
    if not csv_file.exists():
        return False
    with csv_file.open("r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        # skip header
        next(reader, None)
        return any(row[0] == today for row in reader)


def append_csv(row):
    file_exists = CSV_PATH.exists()
    with CSV_PATH.open("a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Date", "Raw", "TaskID", "Done", "Anomaly", "PreHash", "Proof"])
        writer.writerow(row)


def main():
    today = dt.datetime.now().strftime("%Y-%m-%d")

    if already_rolled_today(CSV_PATH, today):
        sys.exit("⚠️  Roll already logged for today; aborting.")

    pre_file = newest_prethought(PRE_DIR)
    pre_hash = sha256_of_file(pre_file)
    raw = fetch_qrng_byte()
    task_id = raw % NUM_TASKS + 1

    row = [today, raw, task_id, "N", "—", pre_hash, ""]
    append_csv(row)

    USED_DIR.mkdir(parents=True, exist_ok=True)
    pre_file.rename(USED_DIR / pre_file.name)

    print(f"✅ Roll complete {today}")
    print(f"  Raw byte : {raw}")
    print(f"  Task ID  : {task_id}")
    print(f"  PreHash  : {pre_hash}")
    print("  Row appended to log_template.csv")


if __name__ == "__main__":
    main()
