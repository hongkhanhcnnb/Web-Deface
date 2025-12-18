import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.metrics import classification_report, confusion_matrix

FILE = "data/final/web_deface_dataset_hybrid.csv"


def main():
    
    # 1. Load dữ liệu
    df = pd.read_csv(FILE)

    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

    # 2. Gom session 1.5 giây
    df["session"] = df["timestamp"].astype("int64") // 1_500_000_000
    groups = df.groupby("session")

    session_features = []
    session_labels = []

    # 3. Trích xuất feature + label cho session
    for sid, g in groups:

        # Label session
        # 0 = normal, 1 = anomaly
        label = 1 if ((g["y"] == 1).any() or (g["y"] == 2).any()) else 0
        session_labels.append(label)

        entropy_var = g["entropy"].var() if len(g) > 1 else 0.0
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

    # 4. TRAIN CHỈ TRÊN NORMAL
    X_train = X[y == 0] 

    print(f"Training on NORMAL sessions only: {len(X_train)} samples")

    clf = IsolationForest(
        n_estimators=500,
        contamination="auto", 
        random_state=42
    )

    clf.fit(X_train)

    # 5. TEST TRÊN TOÀN BỘ SESSION
    pred = clf.predict(X)
    pred = (pred == -1).astype(int)  # -1 → anomaly (1)

    # 6. Đánh giá
    print("\n=== Isolation Forest (Train-only-Normal) ===")
    print(classification_report(
        y, pred,
        target_names=["normal", "anomaly"],
        zero_division=0
    ))

    print("Confusion Matrix:")
    print(confusion_matrix(y, pred))

    print(f"\nTotal sessions: {len(y)}")
    print(f"Actual anomalies: {y.sum()}")
    print(f"Detected anomalies: {pred.sum()}")


if __name__ == "__main__":
    main()
