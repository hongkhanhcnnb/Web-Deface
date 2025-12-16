# collector/merge_integrity_feature.py
import os, pandas as pd
from datetime import datetime, timedelta

CHAIN_FILE = "data/final/web_deface_dataset_chain.csv"
INT_LOG = "data/logs/file_integrity.log"
OUT_FILE = "data/final/web_deface_dataset_hybrid.csv"

def load_events(path):
    events = []
    if not os.path.exists(path):
        return events
    for line in open(path):
        parts = line.strip().split(",")
        try:
            ts = datetime.fromisoformat(parts[0])
            events.append(ts)
        except:
            pass
    return sorted(events)

def main():
    df = pd.read_csv(CHAIN_FILE)

    # CHUẨN HOÁ: đọc timestamp từ access.log, nhưng ghi theo local-time
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

    # convert về UTC (trừ 7 giờ)
    df["timestamp_utc"] = df["timestamp"] - pd.Timedelta(hours=7)

    events = load_events(INT_LOG)

    if not events:
        df["file_changed"] = 0
    else:
        first_change = events[0]

        df["file_changed"] = (df["timestamp_utc"] >= first_change).astype(int)

    # output cuối
    df.to_csv(OUT_FILE, index=False)
    print(f"[OK] Hybrid dataset written -> {OUT_FILE}")
    print(df["file_changed"].value_counts())

if __name__ == "__main__":
    main()
