"""Fine-tune CodeBERT for binary Devign vulnerability classification with diagnostics."""
from __future__ import annotations

import argparse
import inspect
import json
from pathlib import Path
from typing import Any

import numpy as np
import torch
from datasets import Dataset
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, roc_auc_score
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    Trainer,
    TrainerCallback,
    TrainingArguments,
)

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data" / "processed"
OUTPUT_DIR = ROOT / "models" / "codebert"
DIAGNOSTICS_DIR = ROOT / "reports" / "codebert_diagnostics"
MODEL_NAME = "microsoft/codebert-base"
MAX_LENGTH = 256
SEED = 42


def load_jsonl(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle]


def make_dataset(rows: list[dict]) -> Dataset:
    return Dataset.from_dict({"code": [r["code"] for r in rows], "labels": [int(r["label"]) for r in rows]})


def jsonable(value: Any) -> Any:
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, (np.integer, np.floating)):
        return value.item()
    if isinstance(value, dict):
        return {str(k): jsonable(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [jsonable(v) for v in value]
    return value


class TrainingDiagnosticsCallback(TrainerCallback):
    """Persist every Trainer log, including loss and effective learning rate."""

    def __init__(self) -> None:
        self.logs: list[dict] = []

    def on_log(self, args, state, control, logs=None, **kwargs):
        if logs:
            record = {"global_step": int(state.global_step), "epoch": state.epoch}
            record.update(jsonable(logs))
            self.logs.append(record)
            print("TRAIN_LOG", json.dumps(record, sort_keys=True))

    def on_train_end(self, args, state, control, **kwargs):
        DIAGNOSTICS_DIR.mkdir(parents=True, exist_ok=True)
        (DIAGNOSTICS_DIR / "training_log_history.json").write_text(
            json.dumps(jsonable(self.logs), indent=2), encoding="utf-8"
        )


def normalize_logits(raw_predictions: Any) -> np.ndarray:
    predictions = raw_predictions
    if isinstance(predictions, tuple):
        predictions = predictions[0]
    return np.asarray(predictions)


def build_metrics_logger(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)

    def compute_metrics(eval_pred):
        logits = normalize_logits(eval_pred.predictions if hasattr(eval_pred, "predictions") else eval_pred[0])
        labels = np.asarray(eval_pred.label_ids if hasattr(eval_pred, "label_ids") else eval_pred[1])
        probabilities = torch.softmax(torch.tensor(logits), dim=-1)[:, 1].numpy()
        predictions = np.argmax(logits, axis=-1)
        record = {
            "label_sample": labels[:16].tolist(),
            "logit_sample": logits[:8].tolist(),
            "prediction_sample": predictions[:16].tolist(),
            "label_values": sorted(np.unique(labels).astype(int).tolist()),
            "prediction_values": sorted(np.unique(predictions).astype(int).tolist()),
            "label_counts": {str(k): int(v) for k, v in zip(*np.unique(labels, return_counts=True))},
            "prediction_counts": {str(k): int(v) for k, v in zip(*np.unique(predictions, return_counts=True))},
        }
        with path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(jsonable(record)) + "\n")
        print("EVAL_DIAGNOSTICS", json.dumps(record, sort_keys=True))
        return {
            "accuracy": accuracy_score(labels, predictions),
            "precision": precision_score(labels, predictions, zero_division=0),
            "recall": recall_score(labels, predictions, zero_division=0),
            "f1": f1_score(labels, predictions, zero_division=0),
            "roc_auc": roc_auc_score(labels, probabilities) if len(np.unique(labels)) == 2 else 0.0,
        }

    return compute_metrics


def classifier_optimizer_diagnostics(model: torch.nn.Module, trainer: Trainer) -> dict:
    """Assert classifier params are trainable and present in the optimizer."""
    classifier_params = [(name, param) for name, param in model.named_parameters() if "classifier" in name]
    if not classifier_params:
        raise RuntimeError("No classifier parameters found in model.named_parameters().")
    frozen = [name for name, param in classifier_params if not param.requires_grad]
    if frozen:
        raise RuntimeError(f"Classifier parameters are frozen: {frozen}")
    for _, param in classifier_params:
        param.requires_grad_(True)

    trainer.create_optimizer()
    optimizer_param_ids = {id(param) for group in trainer.optimizer.param_groups for param in group["params"]}
    missing = [name for name, param in classifier_params if id(param) not in optimizer_param_ids]
    if missing:
        raise RuntimeError(f"Classifier parameters missing from optimizer: {missing}")

    parameter_groups = []
    for index, group in enumerate(trainer.optimizer.param_groups):
        names = [name for name, param in model.named_parameters() if id(param) in {id(p) for p in group["params"]}]
        parameter_groups.append({
            "group": index,
            "learning_rate": group.get("lr"),
            "weight_decay": group.get("weight_decay"),
            "parameter_count": len(group["params"]),
            "contains_classifier": any("classifier" in name for name in names),
        })
    diagnostics = {
        "classifier_parameter_names": [name for name, _ in classifier_params],
        "classifier_parameter_count": sum(param.numel() for _, param in classifier_params),
        "classifier_trainable": True,
        "classifier_in_optimizer": True,
        "optimizer_class": type(trainer.optimizer).__name__,
        "optimizer_parameter_groups": parameter_groups,
        "configured_learning_rate": trainer.args.learning_rate,
        "initial_optimizer_learning_rates": [group.get("lr") for group in trainer.optimizer.param_groups],
    }
    print("OPTIMIZER_DIAGNOSTICS", json.dumps(diagnostics, sort_keys=True))
    return diagnostics


def write_loss_curve(trainer: Trainer) -> None:
    history = jsonable(trainer.state.log_history)
    train_logs = [record for record in history if "loss" in record]
    eval_logs = [record for record in history if "eval_loss" in record]
    curve = {
        "train_loss_by_epoch": [
            {"epoch": record.get("epoch"), "step": record.get("step", record.get("global_step")), "loss": record["loss"], "learning_rate": record.get("learning_rate")}
            for record in train_logs
        ],
        "eval_loss_by_epoch": [
            {"epoch": record.get("epoch"), "step": record.get("step", record.get("global_step")), "eval_loss": record["eval_loss"], "eval_f1": record.get("eval_f1"), "eval_accuracy": record.get("eval_accuracy")}
            for record in eval_logs
        ],
        "full_log_history": history,
    }
    DIAGNOSTICS_DIR.mkdir(parents=True, exist_ok=True)
    (DIAGNOSTICS_DIR / "loss_curve.json").write_text(json.dumps(curve, indent=2), encoding="utf-8")
    print("LOSS_CURVE", json.dumps({"train": curve["train_loss_by_epoch"], "eval": curve["eval_loss_by_epoch"]}, sort_keys=True))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--diagnostics-only", action="store_true", help="Check optimizer and prediction/label flow without training.")
    parser.add_argument("--smoke-test", action="store_true", help="Train on a tiny subset for three epochs to verify loss/LR logging.")
    parser.add_argument("--smoke-train-samples", type=int, default=64)
    parser.add_argument("--smoke-eval-samples", type=int, default=32)
    parser.add_argument("--smoke-epochs", type=float, default=3.0)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    DIAGNOSTICS_DIR.mkdir(parents=True, exist_ok=True)
    eval_log_path = DIAGNOSTICS_DIR / "evaluation_samples.jsonl"
    if eval_log_path.exists():
        eval_log_path.unlink()

    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"torch={torch.__version__}; cuda_available={torch.cuda.is_available()}; device={device}")
    print(f"TrainingArguments signature: {inspect.signature(TrainingArguments)}")
    print(f"Trainer signature: {inspect.signature(Trainer)}")

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME, num_labels=2)
    train_ds = make_dataset(load_jsonl(DATA_DIR / "train.jsonl"))
    val_ds = make_dataset(load_jsonl(DATA_DIR / "validation.jsonl"))
    test_ds = make_dataset(load_jsonl(DATA_DIR / "test.jsonl"))
    run_output_dir = OUTPUT_DIR
    if args.smoke_test:
        train_ds = train_ds.select(range(min(args.smoke_train_samples, len(train_ds))))
        val_ds = val_ds.select(range(min(args.smoke_eval_samples, len(val_ds))))
        test_ds = test_ds.select(range(min(args.smoke_eval_samples, len(test_ds))))
        run_output_dir = DIAGNOSTICS_DIR / "smoke_model"
        print(f"SMOKE_TEST_DATA train={len(train_ds)} validation={len(val_ds)} test={len(test_ds)} epochs={args.smoke_epochs}")
    print("RAW_LABEL_SAMPLE", json.dumps({
        "train": train_ds["labels"][:16],
        "validation": val_ds["labels"][:16],
        "test": test_ds["labels"][:16],
        "train_unique": sorted(set(train_ds["labels"])),
        "validation_unique": sorted(set(val_ds["labels"])),
        "test_unique": sorted(set(test_ds["labels"])),
    }))

    def tokenize(batch):
        return tokenizer(batch["code"], truncation=True, max_length=MAX_LENGTH)

    train_ds = train_ds.map(tokenize, batched=True, remove_columns=["code"])
    val_ds = val_ds.map(tokenize, batched=True, remove_columns=["code"])
    test_ds = test_ds.map(tokenize, batched=True, remove_columns=["code"])
    for name, dataset in (("train", train_ds), ("validation", val_ds), ("test", test_ds)):
        assert "labels" in dataset.column_names, f"labels missing from {name}: {dataset.column_names}"
        print(f"TOKENIZED_LABEL_CHECK {name} columns={dataset.column_names} sample={dataset['labels'][:8]}")

    logging_callback = TrainingDiagnosticsCallback()
    training_args_signature = inspect.signature(TrainingArguments).parameters
    epochs = args.smoke_epochs if args.smoke_test else 3.0
    batches_per_epoch = (len(train_ds) + 8 - 1) // 8
    estimated_steps = max(1, int(np.ceil(batches_per_epoch * epochs)))
    args_kwargs = dict(
        output_dir=str(run_output_dir),
        num_train_epochs=epochs,
        per_device_train_batch_size=8,
        per_device_eval_batch_size=16,
        learning_rate=2e-5,
        lr_scheduler_type="linear",
        optim="adamw_torch",
        weight_decay=0.01,
        logging_strategy="epoch",
        logging_steps=1,
        save_strategy="epoch",
        eval_strategy="epoch",
        label_names=["labels"],
        prediction_loss_only=False,
        load_best_model_at_end=True,
        metric_for_best_model="eval_loss",
        greater_is_better=False,
        save_total_limit=2,
        report_to="none",
        seed=SEED,
        fp16=torch.cuda.is_available(),
    )
    if "warmup_ratio" in training_args_signature:
        args_kwargs["warmup_ratio"] = 0.1
    elif "warmup_steps" in training_args_signature:
        args_kwargs["warmup_steps"] = max(1, int(estimated_steps * 0.1))
    else:
        print("WARNING: installed TrainingArguments exposes neither warmup_ratio nor warmup_steps")
    print("TRAINING_ARGUMENTS_EFFECTIVE", json.dumps({
        "learning_rate": args_kwargs["learning_rate"],
        "lr_scheduler_type": args_kwargs["lr_scheduler_type"],
        "warmup": {key: args_kwargs[key] for key in ("warmup_ratio", "warmup_steps") if key in args_kwargs},
        "estimated_steps": estimated_steps,
    }, sort_keys=True))
    training_args = TrainingArguments(**args_kwargs)
    trainer_kwargs = dict(
        model=model,
        args=training_args,
        train_dataset=train_ds,
        eval_dataset=val_ds,
        compute_metrics=build_metrics_logger(eval_log_path),
        callbacks=[logging_callback],
    )
    trainer_signature = inspect.signature(Trainer).parameters
    if "processing_class" in trainer_signature:
        trainer_kwargs["processing_class"] = tokenizer
    else:
        trainer_kwargs["tokenizer"] = tokenizer
    trainer = Trainer(**trainer_kwargs)
    optimizer_diagnostics = classifier_optimizer_diagnostics(model, trainer)
    (DIAGNOSTICS_DIR / "optimizer_diagnostics.json").write_text(json.dumps(optimizer_diagnostics, indent=2), encoding="utf-8")

    if args.diagnostics_only:
        preview = test_ds.select(range(min(8, len(test_ds))))
        prediction = trainer.predict(preview, metric_key_prefix="diagnostic")
        logits = normalize_logits(prediction.predictions)
        raw = {
            "labels": prediction.label_ids.tolist(),
            "logits": logits.tolist(),
            "predictions": np.argmax(logits, axis=-1).tolist(),
        }
        print("RAW_PREDICTION_DIAGNOSTICS", json.dumps(raw))
        (DIAGNOSTICS_DIR / "diagnostic_predictions.json").write_text(json.dumps(raw, indent=2), encoding="utf-8")
        return

    trainer.train()
    write_loss_curve(trainer)
    trainer.save_model(run_output_dir)
    tokenizer.save_pretrained(run_output_dir)
    test_metrics = trainer.evaluate(test_ds, metric_key_prefix="test")
    test_metrics["diagnostics"] = {
        "optimizer": optimizer_diagnostics,
        "evaluation_samples": str(eval_log_path),
        "loss_curve": str(DIAGNOSTICS_DIR / "loss_curve.json"),
    }
    (OUTPUT_DIR / "test_metrics.json").write_text(json.dumps(jsonable(test_metrics), indent=2), encoding="utf-8")
    print(json.dumps(jsonable(test_metrics), indent=2))


if __name__ == "__main__":
    main()
