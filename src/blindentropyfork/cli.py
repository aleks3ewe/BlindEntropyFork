import sys

from blindentropyfork.proof import main as proof_main
from blindentropyfork.roll import main as roll_main


def stamp_entry() -> None:  # bef-stamp
    script_path = "scripts/stamp_prethought.py"
    with open(script_path, "rb") as f:
        code = compile(f.read(), script_path, 'exec')
        exec(code, {'__name__': '__main__', '__file__': script_path})


def anom_entry() -> None:  # bef-anom
    script_path = "scripts/log_anomaly.py"
    with open(script_path, "rb") as f:
        code = compile(f.read(), script_path, 'exec')
        exec(code, {'__name__': '__main__', '__file__': script_path})


def roll_entry() -> None:  # bef-roll
    sys.exit(roll_main())


def proof_entry() -> None:  # bef-proof
    sys.exit(proof_main())
