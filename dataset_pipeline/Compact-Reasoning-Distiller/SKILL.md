---
name: Compact-Reasoning-Distiller
description: Distill scratchblocks pseudocode into high-quality JSONL with deep chain-of-thought reasoning for MoECat model training.
---

# Compact Reasoning Distiller Skill

Process Scratch projects one-by-one from a local ScratchRepository synced via rclone.

## Setup

1. Install rclone: https://rclone.org/install/
2. Configure rclone remote for Google Drive:
   ```bash
   rclone config
   # Create remote named "gdrive" pointing to your Google Drive ScratchRepository
   ```
3. Set environment variables (optional):
   ```bash
   export RCLONE_REMOTE="gdrive:ScratchRepository"
   export SCRATCH_REPO="./ScratchRepository"
   ```

## Tools

### sync_gdrive.py

Sync project files from Google Drive to local workspace.

```bash
python dataset_pipeline/Compact-Reasoning-Distiller/sync_gdrive.py
python dataset_pipeline/Compact-Reasoning-Distiller/sync_gdrive.py --status
```

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

```
1. sync_gdrive.py        # pull latest from Google Drive
2. get_unprocessed_id.py  # get next ID
3. Read metadata.json + project.scratchblocks
4. Analyze algorithm, generate reasoning
5. Write dataset_entry.json (project marked done)
6. Repeat 2-5 until "NONE"
7. merge_dataset.py       # combine all entries
```

## Per-Project Processing

1. Run `get_unprocessed_id.py` to get next project ID
2. Read `{SCRATCH_REPO}/{ID}/metadata.json` for project context
3. Read `{SCRATCH_REPO}/{ID}/project.scratchblocks` for the code
4. Analyze the algorithm: control flow, data structures, custom blocks
5. Write `{SCRATCH_REPO}/{ID}/dataset_entry.json`
6. Repeat until "NONE"

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

- Run sync_gdrive.py periodically to get new projects
- Process one project at a time
- Use `<think>` tags consistently
- dataset_entry.json existence = project marked done
