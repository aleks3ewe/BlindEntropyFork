import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
ANOMALY_LOG = ROOT / "logs" / "anomaly_log.jsonl"


def add_anomaly(entry: dict) -> None:
    ANOMALY_LOG.parent.mkdir(exist_ok=True)
    with ANOMALY_LOG.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry, ensure_ascii=False) + "\n")
