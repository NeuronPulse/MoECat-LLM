import os
import sys
import random

REPO_ROOT = os.environ.get("SCRATCH_REPO", "/mnt/googledrive/ScratchRepository")


def get_unprocessed():
    if not os.path.exists(REPO_ROOT):
        print(f"ERROR: Repo not found at {REPO_ROOT}", file=sys.stderr)
        sys.exit(1)

    candidates = []
    for name in os.listdir(REPO_ROOT):
        folder = os.path.join(REPO_ROOT, name)
        if not os.path.isdir(folder) or not name.isdigit():
            continue
        has_meta = os.path.exists(os.path.join(folder, "metadata.json"))
        has_code = os.path.exists(os.path.join(folder, "project.scratchblocks"))
        has_entry = os.path.exists(os.path.join(folder, "dataset_entry.json"))
        if has_meta and has_code and not has_entry:
            candidates.append(name)

    if not candidates:
        print("NONE", file=sys.stderr)
        sys.exit(0)

    selected = random.choice(candidates)
    print(selected)


if __name__ == "__main__":
    get_unprocessed()
