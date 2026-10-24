"""Prepare the Devign dataset for vulnerability detection.

The script keeps a raw JSONL export of the Hugging Face rows, then performs
normalization-based exact deduplication before creating fresh stratified splits.
"""
from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from datasets import load_dataset
from sklearn.model_selection import train_test_split

ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw" / "huggingface_devign"
PROCESSED_DIR = ROOT / "data" / "processed"
EDA_DIR = ROOT / "reports" / "eda"
SEED = 42

IDENTIFIER_RE = re.compile(r"\b[A-Za-z_][A-Za-z0-9_]*\b")
STRING_RE = re.compile(r'("(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\')', re.S)
COMMENT_RE = re.compile(r"//.*?$|/\*.*?\*/", re.M | re.S)
KEYWORDS = {
    "if", "else", "for", "while", "do", "switch", "case", "default", "break",
    "continue", "return", "sizeof", "typedef", "struct", "union", "enum", "const",
    "volatile", "static", "extern", "inline", "void", "char", "short", "int", "long",
    "float", "double", "signed", "unsigned", "bool", "true", "false", "NULL",
}


def canonicalize(code: str) -> str:
    code = COMMENT_RE.sub(" ", code or "")
    code = STRING_RE.sub(" STR ", code)

    def replace_identifier(match: re.Match[str]) -> str:
        token = match.group(0)
        return token if token in KEYWORDS else " VAR "

    code = IDENTIFIER_RE.sub(replace_identifier, code)
    return re.sub(r"\s+", " ", code).strip()


def row_to_jsonable(row: dict) -> dict:
    result = {}
    for key, value in row.items():
        if isinstance(value, np.ndarray):
            value = value.tolist()
        result[key] = value
    return result


def write_jsonl(path: Path, rows: list[dict]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def extract_label(row: dict) -> int:
    value = row.get("target", row.get("label"))
    if isinstance(value, bool):
        return int(value)
    return int(value)


def extract_code(row: dict) -> str:
    return str(row.get("func") or row.get("code") or row.get("func_clean") or "")


def main() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    EDA_DIR.mkdir(parents=True, exist_ok=True)

    dataset = load_dataset("DetectVul/devign")
    raw_rows: list[dict] = []
    source_split_counts = {}
    for split_name, split in dataset.items():
        rows = [row_to_jsonable(row) for row in split]
        source_split_counts[split_name] = len(rows)
        write_jsonl(RAW_DIR / f"{split_name}.jsonl", rows)
        raw_rows.extend(rows)

    before_count = len(raw_rows)
    labels = [extract_label(row) for row in raw_rows]
    code_lengths = [len(extract_code(row)) for row in raw_rows]
    projects = [str(row.get("project", "unknown")) for row in raw_rows]
    cwe_values = [row.get("cwe") or row.get("CWE") or row.get("cwe_type") for row in raw_rows]

    seen: set[str] = set()
    deduped: list[dict] = []
    duplicate_count = 0
    for row in raw_rows:
        normalized = canonicalize(extract_code(row))
        digest = hashlib.sha256(normalized.encode("utf-8")).hexdigest()
        if digest in seen:
            duplicate_count += 1
            continue
        seen.add(digest)
        item = dict(row)
        item["label"] = extract_label(row)
        item["code"] = extract_code(row)
        item["normalized_hash"] = digest
        deduped.append(item)

    after_count = len(deduped)
    dedup_labels = [int(row["label"]) for row in deduped]
    indices = np.arange(after_count)
    train_idx, temp_idx = train_test_split(
        indices, test_size=0.20, random_state=SEED, stratify=dedup_labels
    )
    temp_labels = [dedup_labels[i] for i in temp_idx]
    val_idx, test_idx = train_test_split(
        temp_idx, test_size=0.50, random_state=SEED, stratify=temp_labels
    )

    splits = {
        "train": [deduped[i] for i in train_idx],
        "validation": [deduped[i] for i in val_idx],
        "test": [deduped[i] for i in test_idx],
    }
    for split_name, rows in splits.items():
        write_jsonl(PROCESSED_DIR / f"{split_name}.jsonl", rows)

    def counts(rows: list[dict]) -> dict[str, int]:
        return {str(k): int(v) for k, v in sorted(Counter(int(r["label"]) for r in rows).items())}

    metadata = {
        "dataset": "DetectVul/devign",
        "source_splits": source_split_counts,
        "raw_count_before_deduplication": before_count,
        "deduplicated_count": after_count,
        "near_duplicate_rows_removed": duplicate_count,
        "deduplication_method": "SHA-256 of whitespace-normalized code with comments, strings, and non-keyword identifiers normalized",
        "near_duplicate_threshold": "exact match after identifier normalization (conservative hash-based approximation)",
        "split_method": "stratified random split after deduplication",
        "split_ratios": {"train": 0.80, "validation": 0.10, "test": 0.10},
        "seed": SEED,
        "split_counts": {name: len(rows) for name, rows in splits.items()},
        "split_label_counts": {name: counts(rows) for name, rows in splits.items()},
    }
    (PROCESSED_DIR / "splits.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")

    cwe_counter = Counter(str(value) for value in cwe_values if value is not None)
    eda = {
        "dataset": "DetectVul/devign",
        "raw_rows": before_count,
        "deduplicated_rows": after_count,
        "class_balance_raw": {str(k): int(v) for k, v in sorted(Counter(labels).items())},
        "class_balance_deduplicated": {str(k): int(v) for k, v in sorted(Counter(dedup_labels).items())},
        "code_length_characters": {
            "min": int(min(code_lengths)), "max": int(max(code_lengths)),
            "mean": float(np.mean(code_lengths)), "median": float(np.median(code_lengths)),
            "p95": float(np.percentile(code_lengths, 95)),
        },
        "project_counts": {str(k): int(v) for k, v in sorted(Counter(projects).items())},
        "cwe_type_frequency": {k: int(v) for k, v in cwe_counter.most_common()},
    }
    (EDA_DIR / "eda_summary.json").write_text(json.dumps(eda, indent=2), encoding="utf-8")

    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    axes[0].bar([str(k) for k in sorted(Counter(labels))], [Counter(labels)[k] for k in sorted(Counter(labels))])
    axes[0].set_title("Raw class balance")
    axes[0].set_xlabel("Label")
    axes[0].set_ylabel("Functions")
    axes[1].hist(code_lengths, bins=50, color="#3366cc")
    axes[1].set_title("Raw code length distribution")
    axes[1].set_xlabel("Characters")
    axes[1].set_ylabel("Functions")
    fig.tight_layout()
    fig.savefig(EDA_DIR / "class_balance_and_code_length.png", dpi=150)
    plt.close(fig)

    report = [
        "# Devign EDA Report", "", f"- Raw rows: **{before_count:,}**",
        f"- Rows after normalization-based deduplication: **{after_count:,}**",
        f"- Removed near-duplicate rows: **{duplicate_count:,}**", "",
        "## Class balance", json.dumps(eda["class_balance_raw"], indent=2), "",
        "## Project/source breakdown", json.dumps(eda["project_counts"], indent=2), "",
        "## Code length", json.dumps(eda["code_length_characters"], indent=2), "",
        "## CWE frequency", json.dumps(eda["cwe_type_frequency"], indent=2), "",
        "The source dataset does not expose a populated CWE field in the downloaded rows when this report is generated." if not cwe_counter else "CWE frequencies are included above.",
    ]
    (EDA_DIR / "eda_report.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    print(json.dumps(metadata, indent=2))
    print(json.dumps(eda, indent=2))


if __name__ == "__main__":
    main()
