import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.metrics import classification_report, confusion_matrix

FILE = "data/final/web_deface_dataset_hybrid.csv"


def main():
    df = pd.read_csv(FILE)

    # Parse timestamp về datetime
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

    # === Gom session theo cửa sổ thời gian (1.5 giây) ===
    df["session"] = (df["timestamp"].astype("int64") // 1_500_000_000)

    groups = df.groupby("session")

    session_features = []
    session_labels = []

    for sid, g in groups:
        # Label: suspicious/deface -> anomaly
        if (g["y"] == 1).sum() > 0 or (g["y"] == 2).sum() > 0:
            session_labels.append(1)
        else:
            session_labels.append(0)

        # Độ biến thiên entropy (phát hiện payload thay đổi bất thường)
        entropy_var = g["entropy"].var() if len(g) > 1 else 0.0

        # burst rate = số request / 1.5s
        burst_rate = len(g) / 1.5

        session_features.append([
            g["entropy"].mean(),
            g["entropy"].max(),
            entropy_var,              
            g["chain_score"].mean(),
            g["chain_score"].max(),
            g["keyword_flag"].sum(),
            g["is_post"].sum(),
            g["path_len"].mean(),
            g["rate"].mean(),
            g["file_changed"].max(),
            len(g),                   
            burst_rate                
        ])

    X = np.array(session_features)
    y = np.array(session_labels)

    # === Isolation Forest (tối ưu recall) ===
    clf = IsolationForest(
        n_estimators=500,
        contamination=0.38,
        max_samples='auto',
        random_state=42
    )

    pred = clf.fit_predict(X)
    pred = (pred == -1).astype(int)

    # Đánh giá
    print("\n=== Session-based Anomaly Detection (Optimized v2) ===")
    print(classification_report(y, pred, target_names=["normal", "anomaly"], zero_division=0))
    print("Confusion Matrix:")
    print(confusion_matrix(y, pred))

    print(f"\nTotal sessions: {len(y)}")
    print(f"Actual anomalies: {y.sum()}")
    print(f"Detected anomalies: {pred.sum()}")


if __name__ == "__main__":
    main()
