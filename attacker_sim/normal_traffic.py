import requests
import time
import random

BASE = "http://127.0.0.1:5000"

paths = [
    "/", "/about", "/contact",
    "/news", "/products", "/blog",
    "/assets/logo.png", "/static/main.css",
]

def main():
    for i in range(4000):
        p = random.choice(paths)
        try:
            requests.get(BASE + p, timeout=1)
        except:
            pass

        if i % 400 == 0:
            print(f"[NORMAL] {i}/4000")

        time.sleep(0.003)

    print("[OK] normal_traffic done.")

if __name__ == "__main__":
    main()
