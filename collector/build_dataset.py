import pandas as pd

IN_CHAIN = "data/raw/logs_v2.csv"
OUT_CHAIN = "data/final/web_deface_dataset_chain.csv"

def main():
    df = pd.read_csv(IN_CHAIN)

    mapping = {"normal":0, "suspicious":1, "deface":2}
    df["y"] = df["label"].map(mapping)

    df.to_csv(OUT_CHAIN, index=False)

    print(f"[OK] Attack-chain saved -> {OUT_CHAIN}")
    print(df["y"].value_counts())

if __name__ == "__main__":
    main()
