import sys

from blindentropyfork.anomaly import main as anomaly_main
from blindentropyfork.proof import main as proof_main
from blindentropyfork.roll import main as roll_main
from blindentropyfork.stamp import main as stamp_main


def stamp_entry() -> None:  # bef-stamp
    sys.exit(stamp_main())


def anom_entry() -> None:  # bef-anom
    sys.exit(anomaly_main())


def roll_entry() -> None:  # bef-roll
    sys.exit(roll_main())


def proof_entry() -> None:  # bef-proof
    sys.exit(proof_main())
