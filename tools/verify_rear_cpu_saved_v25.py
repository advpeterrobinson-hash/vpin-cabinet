#!/usr/bin/env python3
from __future__ import annotations

import pathlib
import zipfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
MASTER = ROOT / "cad" / "master" / "vpin-master.FCStd"

REQUIRED = (
    "REAR CPU SERVICE - BACKDOOR / PULL-OUT SHELF (ACTIVE)",
    "CAB-PC-REAR-DOOR-002-R1 - CLOSED",
    "PC-REAR-SHELF-002-R1 - CASE-SIZED BOARD / STOWED",
    "OPEN PC CASE 265x440x128 - ROTATED / BOLTED DIRECT TO BOARD",
    "REARWARD THROUGH MAIN-CABINET BACKDOOR; PLAYFIELD STAYS CLOSED",
)

DIAG_TOKENS = ("REAR CPU", "RearCPU", "PC-REAR", "BACKDOOR", "OPEN PC CASE")


def main() -> int:
    print("REAR CPU SAVED-FILE VERIFY v0.25")
    print("=" * 72)
    if not MASTER.exists():
        print(f"FAIL master missing: {MASTER}")
        return 1

    try:
        with zipfile.ZipFile(MASTER, "r") as zf:
            bad = zf.testzip()
            if bad:
                print(f"FAIL corrupt FCStd member: {bad}")
                return 1
            xml = zf.read("Document.xml").decode("utf-8", errors="replace")
    except Exception as exc:
        print(f"FAIL cannot read FCStd: {exc}")
        return 1

    ok = True
    for text in REQUIRED:
        found = text in xml
        print(f"{'PASS' if found else 'FAIL'} {text}")
        ok = ok and found

    if not ok:
        print("\nDiagnostic rear/CPU strings actually present in Document.xml:")
        hits = []
        for token in DIAG_TOKENS:
            start = 0
            while True:
                i = xml.find(token, start)
                if i < 0:
                    break
                lo = max(0, i - 90)
                hi = min(len(xml), i + 180)
                snippet = " ".join(xml[lo:hi].split())
                if snippet not in hits:
                    hits.append(snippet)
                start = i + len(token)
        if hits:
            for s in hits[:20]:
                print("  ", s)
        else:
            print("  (none: rear CPU subsystem is not serialized in the current FCStd)")

    print("STATUS", "PASS - rear CPU serialized" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
