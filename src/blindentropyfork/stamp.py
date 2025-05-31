import shutil
import sys
import time
from pathlib import Path

from blindentropyfork.utils import sha256, ots_stamp

ROOT = Path(__file__).resolve().parent.parent.parent
PRE_DIR = ROOT / "proof" / "prethought"
ALL_OTS = ROOT / "all_ots"


def main() -> None:
    today = time.strftime("%Y-%m-%d")
    cands = list(PRE_DIR.glob(f"{today}_prethought.*"))
    if not cands:
        sys.exit("❌  Prethought file not found.")
    f = cands[0]
    print("SHA-256:", sha256(f))

    if ots_stamp(f):
        print("✅  OTS-stamp done")
    else:
        sys.exit("❌  OTS-stamp failed")

    ALL_OTS.mkdir(exist_ok=True)
    ots_file = PRE_DIR / (f.name + ".ots")
    if ots_file.exists():
        dest = ALL_OTS / ots_file.name
        shutil.move(str(ots_file), str(dest))
        print(f"📦 Moved → all_ots/{dest.name}")
    else:
        print("⚠️  No .ots file to archive.")


if __name__ == "__main__":
    main()
