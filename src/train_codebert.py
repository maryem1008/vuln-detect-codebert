"""Fine-tune CodeBERT for binary Devign vulnerability classification."""
from __future__ import annotations

import inspect
import json
from pathlib import Path

import numpy as np
import torch
from datasets import Dataset
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, roc_auc_score
from transformers import AutoModelForSequenceClassification, AutoTokenizer, Trainer, TrainingArguments

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data" / "processed"
OUTPUT_DIR = ROOT / "models" / "codebert"
MODEL_NAME = "microsoft/codebert-base"
MAX_LENGTH = 256


def load_jsonl(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle]


def make_dataset(rows: list[dict]) -> Dataset:
    return Dataset.from_dict({"code": [r["code"] for r in rows], "labels": [int(r["label"]) for r in rows]})


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"torch={torch.__version__}; cuda_available={torch.cuda.is_available()}; device={device}")
    print(f"TrainingArguments signature: {inspect.signature(TrainingArguments)}")
    print(f"Trainer signature: {inspect.signature(Trainer)}")

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME, num_labels=2)
    train_ds = make_dataset(load_jsonl(DATA_DIR / "train.jsonl"))
    val_ds = make_dataset(load_jsonl(DATA_DIR / "validation.jsonl"))
    test_ds = make_dataset(load_jsonl(DATA_DIR / "test.jsonl"))

    def tokenize(batch):
        return tokenizer(batch["code"], truncation=True, max_length=MAX_LENGTH)

    train_ds = train_ds.map(tokenize, batched=True, remove_columns=["code"])
    val_ds = val_ds.map(tokenize, batched=True, remove_columns=["code"])
    test_ds = test_ds.map(tokenize, batched=True, remove_columns=["code"])

    def compute_metrics(eval_pred):
        logits, labels = eval_pred
        probabilities = torch.softmax(torch.tensor(logits), dim=-1)[:, 1].numpy()
        predictions = np.argmax(logits, axis=-1)
        return {
            "accuracy": accuracy_score(labels, predictions),
            "precision": precision_score(labels, predictions, zero_division=0),
            "recall": recall_score(labels, predictions, zero_division=0),
            "f1": f1_score(labels, predictions, zero_division=0),
            "roc_auc": roc_auc_score(labels, probabilities),
        }

    args_kwargs = dict(
        output_dir=str(OUTPUT_DIR),
        num_train_epochs=3,
        per_device_train_batch_size=8,
        per_device_eval_batch_size=16,
        learning_rate=2e-5,
        weight_decay=0.01,
        logging_strategy="epoch",
        save_strategy="epoch",
        eval_strategy="epoch",
        load_best_model_at_end=True,
        metric_for_best_model="f1",
        greater_is_better=True,
        save_total_limit=2,
        report_to="none",
        seed=42,
        fp16=torch.cuda.is_available(),
    )
    training_args = TrainingArguments(**args_kwargs)
    trainer_kwargs = dict(
        model=model,
        args=training_args,
        train_dataset=train_ds,
        eval_dataset=val_ds,
        compute_metrics=compute_metrics,
    )
    trainer_signature = inspect.signature(Trainer).parameters
    if "processing_class" in trainer_signature:
        trainer_kwargs["processing_class"] = tokenizer
    else:
        trainer_kwargs["tokenizer"] = tokenizer
    trainer = Trainer(**trainer_kwargs)
    trainer.train()
    trainer.save_model(OUTPUT_DIR)
    tokenizer.save_pretrained(OUTPUT_DIR)
    test_metrics = trainer.evaluate(test_ds, metric_key_prefix="test")
    (OUTPUT_DIR / "test_metrics.json").write_text(json.dumps(test_metrics, indent=2), encoding="utf-8")
    print(json.dumps(test_metrics, indent=2))


if __name__ == "__main__":
    main()
