---
name: Compact-Reasoning-Distiller
description: Distill scratchblocks pseudocode into high-quality JSONL with deep chain-of-thought reasoning for MoECat model training.
---

# Compact Reasoning Distiller Skill

Process Scratch projects one-by-one from local ScratchRepository. Each project gets a dataset_entry.json with reasoning trace.

## Setup

Set `SCRATCH_REPO` if not using default path:

```bash
export SCRATCH_REPO="/mnt/googledrive/ScratchRepository"
```

## Tools

### get_unprocessed_id.py

Returns a random project ID that has metadata.json + project.scratchblocks but no dataset_entry.json.

```bash
python dataset_pipeline/Compact-Reasoning-Distiller/get_unprocessed_id.py
```

Output: a numeric project ID string, or "NONE" if all done.

### merge_dataset.py

Combines all dataset_entry.json files into a single JSONL file.

```bash
python dataset_pipeline/Compact-Reasoning-Distiller/merge_dataset.py
```

## Agent Workflow

1. Run `get_unprocessed_id.py` to get next ID
2. Read `{REPO}/{ID}/metadata.json` for project context (title, author, category)
3. Read `{REPO}/{ID}/project.scratchblocks` for the actual code
4. Analyze the algorithm: control flow, data structures, custom blocks, edge cases
5. Write `{REPO}/{ID}/dataset_entry.json` with this schema
6. Repeat from step 1 until "NONE"
7. Run `merge_dataset.py` to combine all entries

## Dataset Entry Schema

```json
{
  "instruction": "Analyze this Scratch project and explain its algorithm.",
  "input": "<scratchblocks code here>",
  "output": "<brief summary of what the project does>",
  "thought": "<think><reasoning trace></think>",
  "metadata": {
    "project_id": "12345678",
    "project_title": "A* Pathfinding Visualizer",
    "original_author": "username",
    "tech_category": "A* Pathfinding",
    "complexity_tags": ["graph", "heuristic", "pathfinding"]
  }
}
```

## Reasoning Trace Requirements

Each `<think>` block must cover:

1. **Goal decomposition** - what the project does, broken into sub-tasks
2. **Algorithm identification** - core algorithm or pattern used
3. **Key blocks analysis** - which Scratch blocks implement the logic
4. **Edge cases** - boundary conditions handled
5. **Complexity** - time/space complexity estimate

## Important

- Process one project at a time
- Do not skip projects - every entry counts
- Use `<think>` tags consistently
- dataset_entry.json existence = project marked done
