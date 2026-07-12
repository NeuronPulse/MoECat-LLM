---
name: Compact-Reasoning-Distiller
description: Distill scratchblocks pseudocode into high-quality JSONL with deep chain-of-thought reasoning for MoECat model training.
---

# Compact Reasoning Distiller Skill

Use this skill when the user wants to convert scratchblocks code into distilled reasoning JSONL entries with `<think>` tags.

## Workflow

1. Read the target scratchblocks file or raw `.sb3` project from the dataset pipeline.
2. Analyze the algorithmic structure: control flow, data structures, custom blocks, and edge cases.
3. Generate a single JSONL entry containing:
   - `instruction`: the original prompt or project description
   - `input`: scratchblocks pseudocode
   - `output`: final answer or result
   - `thought`: deep reasoning trace wrapped in `<think>` tags, covering algorithm decomposition, design decisions, and complexity analysis
4. Write the entry to the output JSONL file.
5. Destroy the intermediate data (read-and-destroy pattern) to keep memory clean.

## Output Schema

```json
{
  "instruction": "string",
  "input": "string (scratchblocks code)",
  "output": "string (expected result)",
  "thought": "<think>...algorithmic reasoning trace...</think>"
}
```

## Important

- One item at a time. Do not batch.
- Each reasoning trace must cover: goal decomposition, key algorithm used, edge cases handled, and time/space complexity.
- Use `<think>` tags consistently, no variations.
- After processing, discard the source data immediately.
