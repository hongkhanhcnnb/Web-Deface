import pandas as pd

LOG_FILE = "data/raw/logs_v2.csv"
OUT_FILE = "data/final/web_deface_dataset_chain.csv"

def main():
    # 1. Load log đã được tiền xử lý
    df = pd.read_csv(LOG_FILE)
    
    # 2. Chuẩn hóa nhãn (label → y)
    if "y" not in df.columns:
        mapping = {"normal":0, "suspicious":1, "deface":2}
        df["y"] = df["label"].map(mapping)

    # 3. Tính chain_score (điểm hành vi theo chuỗi tấn công)
    df["chain_score"] = (
        (df["keyword_flag"] == 1).astype(int) * 3 +
        (df["entropy"] > 2.0).astype(int) * 2 +
        (df["path"].str.contains("passwd|select|script|drop", case=False, regex=True)).astype(int) * 3 +
        (df["rate"] > 2).astype(int) * 2 +
        (df["is_post"] == 1).astype(int)
    )

    df.to_csv(OUT_FILE, index=False)

    print(f"[OK] Attack-chain saved -> {OUT_FILE}")
    print(df["chain_score"].value_counts().sort_index())

if __name__ == "__main__":
    main()
