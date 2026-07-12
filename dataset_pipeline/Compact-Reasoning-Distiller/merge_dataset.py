import os
import sys
import json
from collections import Counter

REPO_ROOT = os.environ.get("SCRATCH_REPO", "/content/drive/MyDrive/ScratchRepository")
OUTPUT_FILE = os.environ.get("OUTPUT_FILE", "moecat_dataset.jsonl")


def merge():
    if not os.path.exists(REPO_ROOT):
        print(f"ERROR: Repo not found at {REPO_ROOT}", file=sys.stderr)
        sys.exit(1)

    entries = []
    categories = Counter()

    for name in os.listdir(REPO_ROOT):
        folder = os.path.join(REPO_ROOT, name)
        if not os.path.isdir(folder) or not name.isdigit():
            continue
        entry_path = os.path.join(folder, "dataset_entry.json")
        if not os.path.exists(entry_path):
            continue
        try:
            with open(entry_path, "r", encoding="utf-8") as f:
                entry = json.load(f)
            entries.append(entry)
            cat = entry.get("metadata", {}).get("tech_category", "unknown")
            categories[cat] += 1
        except (json.JSONDecodeError, KeyError):
            continue

    if not entries:
        print("No dataset entries found.")
        return

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for entry in entries:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    print(f"Merged {len(entries)} entries into {OUTPUT_FILE}")
    print("Category breakdown:")
    for cat, count in categories.most_common():
        print(f"  {cat}: {count}")


if __name__ == "__main__":
    merge()
