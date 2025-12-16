import os, pandas as pd
import math
from datetime import datetime

IN_LOG = "data/logs/access.log"
OUT_FILE = "data/raw/logs_v2.csv"

os.makedirs("data/raw", exist_ok=True)

# Hàm tính entropy chuỗi (độ hỗn loạn payload / path)
def entropy(s):
    if not s:
        return 0
    freq = {}
    for c in s:
        freq[c] = freq.get(c, 0) + 1
    e = 0
    for f in freq.values():
        p = f / len(s)
        e -= p * math.log2(p)
    return e

# Parse một dòng log
def parse_line(line):
    s = line.strip()
    if not s:
        return None

    parts = s.split()
    
    # 1. Tách label (normal / suspicious / deface)
    label = parts[-1].lower()
    if label not in {"normal", "suspicious", "deface"}:
        return None

    parts = parts[:-1]

     # 2. Parse timestamp (hỗ trợ nhiều định dạng)
    ts = None
    used = 0
    for n in (1,2,3):
        try:
            candidate = " ".join(parts[:n])
            try:
                dt = datetime.fromisoformat(candidate)
            except:
                dt = None
                for fmt in ("%Y-%m-%d %H:%M:%S",
                            "%Y-%m-%d %H:%M:%S.%f"):
                    try:
                        dt = datetime.strptime(candidate, fmt)
                        break
                    except:
                        pass
            if dt:
                ts = dt.isoformat()
                used = n
                break
        except:
            pass

    if ts is None:
        ts = datetime.utcnow().isoformat()

    # 3. Parse các trường còn lại
    rem = parts[used:]
    if len(rem) < 2:
        return None

    ip = rem[0]
    method = rem[1]
    path = rem[2] if len(rem) > 2 else ""

    # 4. Trích xuất feature cho ML / IDS
    return {
        "timestamp": ts,
        "ip": ip,
        "method": method,
        "path": path,
        "label": label,

        "is_post": 1 if method.lower()=="post" else 0,
        "path_len": len(path),
        "path_depth": path.count("/"),
        "hour": datetime.fromisoformat(ts).hour,
        "entropy": entropy(path),
        "keyword_flag": 1 if any(k in path.lower() for k in ["admin","cmd","upload","panel"]) else 0
    }

def main():
    rows = []
    for line in open(IN_LOG, encoding="utf-8", errors="ignore"):
        r = parse_line(line)
        if r:
            rows.append(r)

    df = pd.DataFrame(rows)
    df = df.sort_values("timestamp").reset_index(drop=True)

    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["rate"] = df.groupby("ip")["timestamp"].diff().dt.total_seconds().fillna(1)
    df["rate"] = 1 / df["rate"]

    df.to_csv(OUT_FILE, index=False)
    print(f"[OK] Parsed logs -> {OUT_FILE}")
    print(df["label"].value_counts())

if __name__ == "__main__":
    main()
