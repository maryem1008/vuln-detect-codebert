# vuln-detect-codebert

Vulnerability detection in C/C++ source-code functions using the Devign dataset, a TF-IDF + Logistic Regression baseline, and CodeBERT fine-tuning.

> **Current status:** Dataset preparation and the baseline model are complete. CodeBERT fine-tuning is instrumented and debugged, but the full GPU retrain is intentionally on hold because the larger CPU smoke test did not yet demonstrate reliable learning.

## Project goals

This project evaluates whether a pretrained code language model can classify source-code functions as vulnerable or non-vulnerable. The workflow includes:

1. Acquire and document the Devign dataset.
2. Deduplicate and create reproducible stratified train/validation/test splits.
3. Establish a classical TF-IDF + Logistic Regression baseline.
4. Fine-tune `microsoft/codebert-base` for binary classification.
5. Capture reproducible diagnostics for labels, classifier initialization, optimizer inclusion, learning rate, logits, predictions, and loss curves.

## Dataset

The original Kaggle access path was unavailable in the build environment. The dataset used for this project was therefore obtained from the public Hugging Face mirror:

- Dataset: [`DetectVul/devign`](https://huggingface.co/datasets/DetectVul/devign)
- Original rows: 27,318
- Rows removed during exact normalized-code deduplication: 1,401
- Final deduplicated rows: 25,917
- Split method: stratified random split after deduplication
- Random seed: 42

Final processed split sizes:

| Split | Rows | Label 0 | Label 1 |
|---|---:|---:|---:|
| Train | 20,733 | 11,204 | 9,529 |
| Validation | 2,592 | 1,400 | 1,192 |
| Test | 2,592 | 1,401 | 1,191 |

The processed JSONL files contain real function code and integer labels:

- `data/processed/train.jsonl`
- `data/processed/validation.jsonl`
- `data/processed/test.jsonl`
- `data/processed/splits.json`

The redundant raw mirror under `data/raw/` is excluded from the Git repository. The processed JSONL files are tracked with Git LFS.

## Environment

The environment is pinned in [`requirements.txt`](requirements.txt). Important versions include:

- Python 3.12
- PyTorch 2.14.1
- Transformers 5.20.2
- Datasets 5.1.0
- Accelerate 1.15.0
- scikit-learn 1.9.1

`accelerate` is required by the installed Transformers version for `Trainer` and is included in the current requirements file. The Colab notebook also checks for and installs it defensively.

## Repository layout

```text
vuln-detect-codebert/
├── data/
│   └── processed/
│       ├── train.jsonl
│       ├── validation.jsonl
│       ├── test.jsonl
│       └── splits.json
├── models/
│   └── baseline/
│       ├── logistic_regression.joblib
│       └── tfidf_vectorizer.joblib
├── notebooks/
│   └── train_codebert.ipynb
├── reports/
│   ├── baseline_confusion_matrix.png
│   ├── baseline_results.json
│   ├── eda/
│   └── codebert_diagnostics/
├── src/
│   ├── prepare_data.py
│   ├── baseline.py
│   └── train_codebert.py
├── requirements.txt
└── RUNLOG.md
```

## Data preparation

The data-preparation script performs raw export, exploratory analysis, normalized-code deduplication, and reproducible stratified splits:

```bash
python src/prepare_data.py
```

The exact dataset source, deduplication method, split counts, and decisions are recorded in [`RUNLOG.md`](RUNLOG.md) and `data/processed/splits.json`.

## Baseline model

The baseline uses:

- TF-IDF features
- Unigrams and bigrams
- Maximum vocabulary size: 100,000
- Logistic Regression classifier

Run the baseline with:

```bash
python src/baseline.py
```

Test-set results:

| Metric | Score |
|---|---:|
| Accuracy | 0.60995 |
| Precision | 0.56966 |
| Recall | 0.61797 |
| F1 | 0.59283 |
| ROC-AUC | 0.66102 |

The serialized baseline model and vectorizer are under `models/baseline/`, with metrics under `reports/baseline_results.json`.

## CodeBERT training configuration

The intended full fine-tuning configuration is:

- Base model: `microsoft/codebert-base`
- Maximum sequence length: 256 tokens
- Batch size: 8 per device for training, 16 for evaluation
- Epochs: 3
- Initial learning rate: `2e-5`
- Optimizer: AdamW (`adamw_torch`)
- Scheduler: linear
- Weight decay: 0.01
- Seed: 42
- Mixed precision: enabled automatically when CUDA is available

For the full dataset:

```text
ceil(20,733 / 8) × 3 epochs = 7,776 training steps
10% warmup = 777 warmup steps
```

The script calculates this from the actual selected dataset length. A bounded smoke test calculates its own value from its smaller selected subset; it does not reuse the full-run value.

## CodeBERT diagnostics

`src/train_codebert.py` now verifies and records:

- Newly initialized classifier parameters are trainable.
- `classifier.dense` and `classifier.out_proj` parameters are included in the optimizer.
- The configured and effective learning rates.
- Raw label samples before and after tokenization.
- Raw logits and predictions during evaluation.
- Prediction and label class distributions.
- Per-epoch training and evaluation loss.
- Learning-rate values across the training run.

Run the no-training diagnostics check with:

```bash
python src/train_codebert.py --diagnostics-only
```

Run a small CPU smoke test with:

```bash
python src/train_codebert.py --smoke-test
```

The diagnostics are written under `reports/codebert_diagnostics/`:

- `optimizer_diagnostics.json`
- `evaluation_samples.jsonl`
- `loss_curve.json`
- `training_log_history.json`

## Current CodeBERT results and stop condition

The initial reported Colab run produced precision, recall, and F1 equal to zero, ROC-AUC approximately 0.499, and test loss approximately 0.690. The diagnostics confirmed that this was not caused by labels being constant or the classifier head being excluded from the optimizer.

A larger bounded CPU test was then run using:

- 1,500 training examples
- 500 validation examples
- 500 test examples
- One full epoch
- 188 training steps
- 18 warmup steps

Results:

| Metric | Score |
|---|---:|
| Aggregate training loss | 0.69465 |
| Validation loss | 0.68197 |
| Test loss | 0.69227 |
| Test precision | 0.4750 |
| Test recall | 0.0819 |
| Test F1 | 0.1397 |
| Test ROC-AUC | 0.50735 |

Predictions were no longer constant, but the loss remained close to `ln(2)` and ROC-AUC remained near random. This test therefore did not meet the criterion for starting the full GPU retrain. No final CodeBERT checkpoint or trustworthy full-dataset CodeBERT metrics are claimed yet.

## Colab notebook

[`notebooks/train_codebert.ipynb`](notebooks/train_codebert.ipynb) is intended for a CUDA-enabled Google Colab runtime. It includes environment checks, project-layout detection, dependency handling, training, evaluation, and artifact packaging.

Before running the full GPU job, confirm that the diagnostics output shows:

- Classifier parameters in the optimizer.
- Non-constant labels and predictions.
- A decreasing training-loss curve across the run.
- Non-random validation/test ROC-AUC.

## Reproducibility notes

- Dataset split seed: 42
- Training seed: 42
- Processed datasets are versioned with Git LFS.
- Raw downloaded mirrors are intentionally not versioned.
- Full CodeBERT training has not yet been accepted as complete because the current smoke-test evidence is insufficient.

## License and data provenance

This repository documents the engineering workflow and experiments. Review the licenses and terms of the original Devign dataset, Hugging Face mirror, CodeBERT model, and all source repositories before redistribution or commercial use.


