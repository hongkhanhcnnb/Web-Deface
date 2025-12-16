# collector/integrity_check.py
# Small utility to check integrity and optionally print recent integrity log entries.
# It uses baseline.hash and file_integrity.log created by file_integrity_log.py

import os
from datetime import datetime

BASELINE_FILE = "data/logs/baseline.hash"
LOG_FILE = "data/logs/file_integrity.log"
WEB_FILE = "data/web/index.html"

def read_baseline():
    if not os.path.exists(BASELINE_FILE):
        return None
    with open(BASELINE_FILE, "r") as f:
        return f.read().strip()

def tail_log(n=10):
    if not os.path.exists(LOG_FILE):
        return []
    with open(LOG_FILE, "r") as f:
        lines = f.readlines()
    return [l.strip() for l in lines[-n:]]

def main():
    baseline = read_baseline()
    print(f"Baseline present: {bool(baseline)}")
    if baseline:
        print("Baseline hash:", baseline)
    print("Recent integrity log (last 10 lines):")
    for l in tail_log(10):
        print("  ", l)

if __name__ == "__main__":
    main()
