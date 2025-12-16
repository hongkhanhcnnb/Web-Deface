import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.ensemble import RandomForestClassifier

df = pd.read_csv("data/final/web_deface_dataset_hybrid.csv")

required = [
    "method","path",
    "is_post","path_len","path_depth",
    "entropy","keyword_flag","rate",
    "chain_score","file_changed","y"
]

missing = [c for c in required if c not in df.columns]
if missing:
    raise ValueError("missing:", missing)

X = df.drop(columns=["label","y"], errors="ignore")
y = df["y"]

cat_features = ["method","path"]
num_features = [
    "is_post","path_len","path_depth",
    "entropy","keyword_flag","rate",
    "chain_score","file_changed"
]

preprocess = ColumnTransformer([
    ("cat", OneHotEncoder(handle_unknown="ignore"), cat_features),
    ("num", "passthrough", num_features)
])

model = Pipeline([
    ("prep", preprocess),
    ("clf", RandomForestClassifier(
        n_estimators=400,
        class_weight="balanced",
        random_state=42
    ))
])

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.3,
    random_state=42,
    stratify=y
)

model.fit(X_train, y_train)
pred = model.predict(X_test)

print("\n=== Classification Report ===")
print(classification_report(
    y_test, pred,
    target_names=["normal","suspicious","deface"]
))

print("=== Confusion Matrix ===")
print(confusion_matrix(y_test, pred))
