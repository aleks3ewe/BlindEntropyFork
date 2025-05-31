#!/usr/bin/env python3
"""
BlindEntropyFork proof-harvester
--------------------------------
• YYYY-MM-DD_TaskNN_[before|after].jpg
• log_template.csv, (Date, TaskID) without Proof and with Done!=Y
• SHA-256: Done=Y, Proof=<hash>
• Proof/used/YYYY-MM/
• Marks anomalies from anomaly_log.jsonl → column Anomaly
--------------------------------
"""

import csv
import json
import re
import shutil
import sys
from pathlib import Path

from blindentropyfork.utils import ots_stamp, sha256

ROOT = Path(__file__).resolve().parent.parent.parent
PROOF_DIR = ROOT / "proof"
CSV_PATH = ROOT / "logs" / "log_template.csv"
ANOMALY_LOG = ROOT / "logs" / "anomaly_log.jsonl"
USED_DIR = PROOF_DIR / "used"

name_re = re.compile(r"(\d{4}-\d{2}-\d{2})_Task(\d{1,2})_.*\.(jpg|png)$", re.I)


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


def build_anomaly_map():
    result = {}
    if ANOMALY_LOG.exists():
        with ANOMALY_LOG.open(encoding="utf-8") as f:
            for line in f:
                entry = json.loads(line)
                key = (entry["date"], entry["group"])
                result.setdefault(key, []).append(entry["code"])
    return result


def main():
    header, rows = load_log()
    idx = {k: header.index(k) for k in ["Date", "Group", "TaskID", "Done", "Proof", "Anomaly"]}

    for month in ["2025-06", "2025-07"]:
        for pic in (PROOF_DIR / month).glob("*.*"):
            m = name_re.match(pic.name)
            if not m:
                continue
            date, task_id = m.group(1), str(int(m.group(2)))

            for row in rows:
                if row[idx["Date"]] == date and row[idx["TaskID"]] == task_id and is_empty(row[idx["Proof"]]):
                    file_hash = sha256(pic)
                    row[idx["Proof"]] = file_hash
                    row[idx["Done"]] = "Y"
                    dest = USED_DIR / month
                    dest.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(pic), dest / pic.name)
                    print(f"✔ {pic.name} → logged & moved, hash {file_hash[:8]}…")
                    break
            else:
                print(f"⚠ {pic.name}: matching row not found or already filled")

    anomalies = build_anomaly_map()
    for row in rows:
        key = (row[idx["Date"]], row[idx["Group"]])
        if key in anomalies:
            row[idx["Anomaly"]] = ",".join(anomalies[key])

    save_log(header, rows)
    if not ots_stamp(CSV_PATH):
        print("⚠️  OTS stamping failed for log_template.csv")
        sys.exit("Error: OTS stamping failed for critical file.")

    date_prefix = max(row[idx["Date"]] for row in rows if row[idx["Date"]])
    ots_file = CSV_PATH.with_suffix(".csv.ots")

    if ots_file.exists():
        dest_dir = ROOT / "all_ots"
        dest_dir.mkdir(exist_ok=True)
        dest_name = f"{date_prefix}_log_template_dayend.csv.ots"
        shutil.move(str(ots_file), str(dest_dir / dest_name))
        print(f"📦 Dayend OTS saved → all_ots/{dest_name}")
    else:
        print("⚠️  Dayend OTS not found!")


if __name__ == "__main__":
    main()
