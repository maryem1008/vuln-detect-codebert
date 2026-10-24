"""TF-IDF + Logistic Regression baseline for Devign."""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    precision_recall_fscore_support,
    roc_auc_score,
)

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data" / "processed"
REPORT_DIR = ROOT / "reports"
MODEL_DIR = ROOT / "models" / "baseline"


def load_jsonl(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle]


def main() -> None:
    train = load_jsonl(DATA_DIR / "train.jsonl")
    test = load_jsonl(DATA_DIR / "test.jsonl")
    x_train = [row["code"] for row in train]
    y_train = [int(row["label"]) for row in train]
    x_test = [row["code"] for row in test]
    y_test = [int(row["label"]) for row in test]

    vectorizer = TfidfVectorizer(
        analyzer="word",
        token_pattern=r"(?u)\b\w+\b|[^\w\s]",
        ngram_range=(1, 2),
        min_df=2,
        max_features=100_000,
        sublinear_tf=True,
    )
    train_matrix = vectorizer.fit_transform(x_train)
    test_matrix = vectorizer.transform(x_test)
    model = LogisticRegression(max_iter=300, class_weight="balanced", random_state=42, n_jobs=-1)
    model.fit(train_matrix, y_train)
    pred = model.predict(test_matrix)
    probability = model.predict_proba(test_matrix)[:, 1]

    precision, recall, f1, _ = precision_recall_fscore_support(
        y_test, pred, average="binary", zero_division=0
    )
    metrics = {
        "model": "tfidf_logistic_regression",
        "test_size": len(y_test),
        "accuracy": float(accuracy_score(y_test, pred)),
        "precision": float(precision),
        "recall": float(recall),
        "f1": float(f1),
        "roc_auc": float(roc_auc_score(y_test, probability)),
        "confusion_matrix": confusion_matrix(y_test, pred).tolist(),
        "classification_report": classification_report(y_test, pred, output_dict=True, zero_division=0),
        "vectorizer": {
            "ngram_range": [1, 2],
            "max_features": 100_000,
            "vocabulary_size": len(vectorizer.vocabulary_),
        },
    }
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    (REPORT_DIR / "baseline_results.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    import joblib
    joblib.dump(vectorizer, MODEL_DIR / "tfidf_vectorizer.joblib")
    joblib.dump(model, MODEL_DIR / "logistic_regression.joblib")

    cm = confusion_matrix(y_test, pred)
    fig, ax = plt.subplots(figsize=(4, 4))
    ax.imshow(cm, cmap="Blues")
    ax.set_title("TF-IDF + Logistic Regression confusion matrix")
    ax.set_xlabel("Predicted")
    ax.set_ylabel("Actual")
    for (row, col), value in __import__("numpy").ndenumerate(cm):
        ax.text(col, row, int(value), ha="center", va="center")
    fig.tight_layout()
    fig.savefig(REPORT_DIR / "baseline_confusion_matrix.png", dpi=150)
    plt.close(fig)
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
