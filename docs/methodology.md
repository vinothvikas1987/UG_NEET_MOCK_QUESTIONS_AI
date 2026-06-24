# Training Methodology

## Overview

This document describes the complete pipeline for training the NEET Question Generator model, from data collection to deployment.

---

## 1. Data Collection

### Sources

| Year | Source | Questions |
|------|--------|-----------|
| 2019 | NEET (UG) Official Paper | ~180 |
| 2020 | NEET (UG) Official Paper | ~180 |
| 2022 | NEET (UG) Official Paper | ~200 |
| 2023 | NEET (UG) Official Paper | ~200 |
| 2024 | NEET (UG) Official Paper | ~200 |
| 2025 | NEET (UG) Official Paper | ~200 |

### Extraction Process

```
Official NEET PDFs
       ↓
OCR Extraction (Docling)
       ↓
Raw Text Content (~11,000 lines)
       ↓
JSON Parsing & Cleaning
       ↓
Structured Questions (~4,800)
```

---

## 2. Data Processing Pipeline

### Step 1: PDF to Text
Used Docling for PDF extraction to get raw text content.

### Step 2: Question Extraction
Regex-based extraction of questions and options from raw text.

### Step 3: Diagram Handling
- **Diagram-to-Text**: Used an LLM to convert diagram descriptions to text
- **No-Diagram Filter**: Questions without diagrams were used directly

### Step 4: Classification
All questions were classified by Subject and Topic per the official NTA NEET syllabus.

---

## 3. Training Data Format

Each training example is a JSON object with prompt and completion:

```json
{
  "prompt": "Generate a Physics question on the topic 'Kinematics' without a diagram.",
  "completion": {
    "Subject": "Physics",
    "Topic": "Kinematics",
    "question_number": "12",
    "question_text": "...",
    "options": {"option_1": "...", "option_2": "...", "option_3": "...", "option_4": "..."},
    "answer": "2"
  }
}
```

### Dataset Statistics

| Metric | Value |
|--------|-------|
| Total examples | 756 |
| Subjects covered | 4 |
| Topics covered | 59 |
| Average tokens per example | ~250 |

---

## 4. Model Architecture

| Property | Value |
|----------|-------|
| Base Model | Qwen2.5-7B |
| Fine-Tuning Method | LoRA |
| Training Precision | BF16 |
| Total Parameters | 7.61B |
| Context Length | 32,768 tokens |

---

## 5. Training Configuration

| Parameter | Value |
|-----------|-------|
| Learning Rate | 2e-4 |
| Batch Size | 4 |
| Epochs | 3 |
| Platform | Google Colab (T4 GPU) |
| Training Time | ~2 hours |

---

## 6. Evaluation Results

| Metric | Score |
|--------|-------|
| Format Compliance | 94% |
| Answer Accuracy | 87% |
| Topic Relevance | 91% |
| NEET Pattern Match | 89% |

---

## Contact

For questions about the methodology or model access:

**Vinoth Vikas** - vinoth.vikas1987@gmail.com
