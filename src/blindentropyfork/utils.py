import hashlib
import subprocess
from pathlib import Path


def ots_stamp(path: Path) -> bool:
    ots_file = path.parent / (path.name + ".ots")
    if ots_file.exists():
        print(f"ℹ️  OTS already exists: {ots_file.name}")
        return True
    try:
        subprocess.run(["ots", "stamp", str(path)], check=True, timeout=60)
        print(f"⏲️  OTS stamp ok: {ots_file.name}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"⚠️  OTS stamp failed: {e}")
        return False


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()
