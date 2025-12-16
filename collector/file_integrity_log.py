import os
import hashlib
import time
from datetime import datetime

WEB_FILE = "data/web/index.html"
LOG_FILE = "data/logs/file_integrity.log"
BASELINE_FILE = "data/logs/baseline.hash"

os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

def file_hash(path):
    if not os.path.exists(path):
        return None
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def main():
    current_hash = file_hash(WEB_FILE)
    if current_hash is None:
        print(f"[ERROR] File not found: {WEB_FILE}")
        return

    # Baseline
    if os.path.exists(BASELINE_FILE):
        with open(BASELINE_FILE) as b:
            baseline = b.read().strip()
        print("[OK] Baseline loaded.")
    else:
        with open(BASELINE_FILE, "w") as b:
            b.write(current_hash)
        baseline = current_hash
        print("[OK] Baseline created.")

    print("[WATCHER] Monitoring index.html ...")
    prev_hash = current_hash

    while True:
        new_hash = file_hash(WEB_FILE)
        if new_hash != prev_hash:
            ts = datetime.utcnow().isoformat()
            with open(LOG_FILE, "a") as f:
                f.write(f"{ts},{prev_hash},{new_hash}\n")
            print(f"[ALERT] File changed at {ts}")

            prev_hash = new_hash

        time.sleep(1)

if __name__ == "__main__":
    main()
