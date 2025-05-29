#!/usr/bin/env python3
"""
BlindEntropyFork proof-harvester
--------------------------------
• YYYY-MM-DD_TaskNN_[before|after].jpg
• log_template.csv, (Date, TaskID) without Proof and with Done!=Y
• SHA-256: Done=Y, Proof=<hash>
• Proof/used/YYYY-MM/
--------------------------------
"""

import csv
import hashlib
import re
import shutil
from pathlib import Path

ROOT = Path(r"")
PROOF_DIR = ROOT / "Proof"
CSV_PATH = ROOT / "log_template.csv"
USED_DIR = PROOF_DIR / "used"

name_re = re.compile(r"(\d{4}-\d{2}-\d{2})_Task(\d{1,2})_.*\.(jpg|png)$", re.I)


def sha256_of_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def load_log():
    with CSV_PATH.open(newline="", encoding="utf-8") as f:
        rdr = list(csv.reader(f))
    header, rows = rdr[0], rdr[1:]
    return header, rows


def save_log(header, rows):
    with CSV_PATH.open("w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerows([header] + rows)


def is_empty(proof_field: str) -> bool:
    return proof_field.strip() in {"", "—", "-"}


def main():
    header, rows = load_log()
    idx = {k: header.index(k) for k in ["Date", "TaskID", "Done", "Proof"]}

    for month in ["2025-06", "2025-07"]:
        for pic in (PROOF_DIR / month).glob("*.*"):
            m = name_re.match(pic.name)
            if not m:
                continue
            date, task_id = m.group(1), str(int(m.group(2)))

            for row in rows:
                if row[idx["Date"]] == date and row[idx["TaskID"]] == task_id and is_empty(row[idx["Proof"]]):
                    file_hash = sha256_of_file(pic)
                    row[idx["Proof"]] = file_hash
                    row[idx["Done"]] = "Y"
                    dest = USED_DIR / month
                    dest.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(pic), dest / pic.name)
                    print(f"✔ {pic.name} → logged & moved, hash {file_hash[:8]}…")
                    break
            else:
                print(f"⚠ {pic.name}: matching row not found or already filled")

    save_log(header, rows)


if __name__ == "__main__":
    main()
