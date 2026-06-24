# NEET Question Generator

A fine-tuned Qwen2.5-7B model that generates NEET-style multiple choice questions across Physics, Chemistry, Botany, and Zoology.

**Try the demo:** [Hugging Face Space](https://huggingface.co/vinothvikas1987/UG_NEET_MOCK_QUESTIONS_AI)

**Model:** [vinothvikas1987/qwen-lora-finetune-merged](https://huggingface.co/vinothvikas1987/qwen-lora-finetune-merged)

## Features

- Generate NEET MCQs for any subject/topic in the official NEET syllabus
- Covers 20 Physics topics, 20 Chemistry topics, 10 Botany topics, 9 Zoology topics
- Trained on real NEET question papers (2019–2025)
- Outputs structured questions with 4 options and correct answer

## Limitations

- **Text-only**: Cannot generate or render diagrams/images
- Generates questions based on pattern recognition from past papers

## Usage

Try the free demo on Hugging Face Spaces (limited to 5 questions).

For unlimited access, contact: vinothvikas1987@gmail.com

## Architecture

- Base model: Qwen2.5-7B
- Fine-tuned with LoRA on NEET question data
- Quantized to 4-bit for efficient inference
