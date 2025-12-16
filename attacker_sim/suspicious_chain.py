import requests
import time
import random

BASE = "http://127.0.0.1:5000"

payloads = [
    "admin", "scan", "../../../../etc/passwd",
    "<script>alert(1)</script>",
    "SELECT+*+FROM+users",
    "' OR '1'='1",
    "DROP+TABLE+users",
]

ATTACKER_IP = "10.10.10.10"      
headers = {"X-Forwarded-For": ATTACKER_IP}

def main():
    for i in range(00):
        q = random.choice(payloads)
        try:
            requests.get(BASE + "/danger?q=" + q, headers=headers, timeout=1)
        except:
            pass

        time.sleep(0.01)

    print("[OK] suspicious_chain done.")

if __name__ == "__main__":
    main()
