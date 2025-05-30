import subprocess
from pathlib import Path


def ots_stamp(path: Path) -> None:
    ots_file = path.parent / (path.name + ".ots")
    if ots_file.exists():
        print(f"ℹ️  OTS already exists: {ots_file.name}")
        return

    try:
        subprocess.run(["ots", "stamp", str(path)], check=True, timeout=60)
        print(f"⏲️  OTS stamp ok: {ots_file.name}")
    except subprocess.CalledProcessError as e:
        print(f"⚠️  OTS stamp failed: {e}")
