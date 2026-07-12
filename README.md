# MoECat-LLM

[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)
[![Stars](https://img.shields.io/github/stars/NeuronPulse/MoECat-LLM.svg)](https://github.com/NeuronPulse/MoECat-LLM)
[![Forks](https://img.shields.io/github/forks/NeuronPulse/MoECat-LLM.svg)](https://github.com/NeuronPulse/MoECat-LLM)
[![Issues](https://img.shields.io/github/issues/NeuronPulse/MoECat-LLM.svg)](https://github.com/NeuronPulse/MoECat-LLM/issues)
[![Last Commit](https://img.shields.io/github/last-commit/NeuronPulse/MoECat-LLM.svg)](https://github.com/NeuronPulse/MoECat-LLM)

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Node.js](https://img.shields.io/badge/node.js-14+-green.svg)](https://nodejs.org/)
[![Scratch](https://img.shields.io/badge/Scratch-3.0-orange.svg)](https://scratch.mit.edu/)
[![Unsloth](https://img.shields.io/badge/Unsloth-QLoRA-purple.svg)](https://github.com/unslothai/unsloth)
[![Kaggle](https://img.shields.io/badge/Kaggle-T4--GPU-blue.svg)](https://www.kaggle.com/)
[![DeepSeek](https://img.shields.io/badge/DeepSeek-R1--Distill--Qwen--8B-red.svg)](https://huggingface.co/deepseek-ai)

---

## Overview

**MoECat** is an end-to-end reasoning distillation pipeline for Scratch 3.0 algorithm education. The project converts 3K+ raw `.sb3` algorithm works into standard scratchblocks pseudocode, then distills them via a top-tier reasoning LLM into high-quality JSONL corpora with `<think>` tags and deep algorithmic breakdowns, and finally fine-tunes lightweight MoE/LLM models under Kaggle's free dual-T4 GPU constraints.

## Pipeline

```
.sb3 Raw Files
    |
    v
[1] Node.js AST Converter       (.sb3 --> scratchblocks pseudocode)
    |
    v
[2] LLM Distillation Skill      (single-item / read-and-destroy --> JSONL with <think>)
    |
    v
[3] Kaggle Fine-tuning          (Unsloth 4-bit QLoRA, dual T4)
    |
    v
MoECat Series Models
```

| Stage | Tool | Output |
|-------|------|--------|
| Scratch Parsing | Node.js + sb3 parser | scratchblocks text |
| CoT Distillation | DeepSeek-R1-Distill-Qwen-8B | JSONL with `<think>` reasoning |
| Fine-tuning | Unsloth + QLoRA 4-bit | LoRA adapter weights |

## Target Model

**DeepSeek-R1-Distill-Qwen-8B**

## Project Structure

```
MoECat-LLM/
├── dataset_pipeline/
│   └── scratch_scraper.py       # Scratch project batch scraper with metadata extraction
├── fine_tune/                   # (planned) Unsloth QLoRA training scripts
├── examples/                    # (planned) Advanced Scratch algorithm examples
├── LICENSE
└── README.md
```

## License

[Apache-2.0](LICENSE)
