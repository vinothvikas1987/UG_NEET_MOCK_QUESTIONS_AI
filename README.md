# NEET Question Generator

### AI-Powered Question Generation for Medical Entrance Exam Preparation

A fine-tuned language model that generates NEET-style multiple-choice questions across Physics, Chemistry, Botany, and Zoology, trained on official NEET question papers from 2019-2025.

**[Request Model Access](mailto:vinoth.vikas1987@gmail.com?subject=NEET%20Model%20Access%20Request)**

---

## What This Model Does

Given a subject and topic from the NEET syllabus, the model generates complete MCQs with:
- Question stem
- 4 options
- Correct answer

### Example Output

**Input:** `Generate a Physics question on the topic 'Kinematics' without a diagram.`

```
Subject: Physics
Topic: Kinematics

Q12. A particle moves along a straight line such that its displacement
x varies with time t as x = at + bt². The acceleration of the particle is:

Options:
1. a
2. 2b
3. a + 2b
4. 2a

Correct Answer: Option 2
```

---

## Model Specifications

| Property | Value |
|----------|-------|
| **Base Model** | Qwen2.5-7B |
| **Fine-Tuning Method** | LoRA (Low-Rank Adaptation) |
| **Training Data** | NEET (UG) papers 2019-2025 |
| **Training Examples** | 756 instruction-completion pairs |
| **Total Parameters** | 7.61B |
| **VRAM Required** | ~4.5 GB (4-bit quantized) |

---

## Coverage

| Subject | Topics | Example Topics |
|---------|--------|----------------|
| **Physics** | 20 | Kinematics, Thermodynamics, Optics, Electrostatics |
| **Chemistry** | 20 | Atomic Structure, Organic Chemistry, Chemical Bonding |
| **Botany** | 10 | Cell Biology, Genetics, Plant Physiology, Ecology |
| **Zoology** | 9 | Animal Kingdom, Human Physiology, Reproduction |

---

## Evaluation Results

| Metric | Score |
|--------|-------|
| Format Compliance | 94% |
| Answer Accuracy | 87% |
| Topic Relevance | 91% |
| NEET Pattern Match | 89% |

---

## Training Methodology

The model was trained on real NEET question papers extracted from official PDFs (2019-2025):

1. **Data Extraction**: OCR extraction from 21 official NEET papers
2. **Cleaning**: Structured into JSON with question, options, and answers
3. **Classification**: Organized by subject and topic per NTA syllabus
4. **Fine-Tuning**: LoRA fine-tuning on Qwen2.5-7B with 4-bit quantization

See [docs/methodology.md](docs/methodology.md) for complete details.

---

## Sample Outputs

See [docs/samples.md](docs/samples.md) for example outputs across all subjects and topics.

---

## Model Access

The model weights are available via gated access on Hugging Face.

### How to Request Access

1. **Send an email** to: [vinoth.vikas1987@gmail.com](mailto:vinoth.vikas1987@gmail.com?subject=NEET%20Model%20Access%20Request)
2. **Include**: Your name, organization, and intended use case
3. **Receive**: Model access link and usage instructions

### What You Get

- Full model weights (BF16 safetensors)
- 4-bit quantized version (for consumer GPUs)
- Inference code and documentation
- Commercial license (MIT)

---

## Use Cases

- **Educational Platforms**: Generate unlimited practice questions
- **NEET Preparation Apps**: Integrate question generation
- **Question Banks**: Create customized question sets
- **Research**: Study NEET question patterns

---

## Hardware Requirements

| Precision | VRAM | Example GPUs |
|-----------|------|--------------|
| BF16 (full) | ~15 GB | A10G, A100, RTX 4090 |
| 4-bit (quantized) | ~4.5 GB | T4, RTX 3060+ |

---

## License

MIT License - See [LICENSE](LICENSE) for details.

---

## Contact

**Vinoth Vikas**
- Email: [vinoth.vikas1987@gmail.com](mailto:vinoth.vikas1987@gmail.com)
- Model Access: [Request Here](mailto:vinoth.vikas1987@gmail.com?subject=NEET%20Model%20Access%20Request)

---

<div align="center">

**Built for NEET aspirants**

[Request Model Access](mailto:vinoth.vikas1987@gmail.com?subject=NEET%20Model%20Access%20Request)

</div>
