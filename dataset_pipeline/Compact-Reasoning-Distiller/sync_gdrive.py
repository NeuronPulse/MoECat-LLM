import os
import sys
import subprocess

RCLONE_REMOTE = os.environ.get("RCLONE_REMOTE", "gdrive:ScratchRepository")
LOCAL_REPO = os.environ.get("SCRATCH_REPO", "./ScratchRepository")


def sync_from_gdrive():
    print(f"[*] Syncing from {RCLONE_REMOTE} to {LOCAL_REPO}...")
    try:
        subprocess.run(
            [
                "rclone", "sync", RCLONE_REMOTE, LOCAL_REPO,
                "--progress",
                "--exclude", "*/project.json",
                "--exclude", "downloaded_registry.json",
            ],
            check=True,
        )
        print(f"[*] Sync complete.")
    except FileNotFoundError:
        print("ERROR: rclone not installed. Install: https://rclone.org/install/", file=sys.stderr)
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"ERROR: rclone sync failed: {e}", file=sys.stderr)
        sys.exit(1)


def count_projects():
    if not os.path.exists(LOCAL_REPO):
        return 0, 0, 0
    total = 0
    ready = 0
    done = 0
    for name in os.listdir(LOCAL_REPO):
        folder = os.path.join(LOCAL_REPO, name)
        if not os.path.isdir(folder) or not name.isdigit():
            continue
        total += 1
        has_code = os.path.exists(os.path.join(folder, "project.scratchblocks"))
        has_entry = os.path.exists(os.path.join(folder, "dataset_entry.json"))
        if has_code and has_entry:
            done += 1
        elif has_code:
            ready += 1
    return total, ready, done


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--status":
        total, ready, done = count_projects()
        print(f"Total: {total} | Ready: {ready} | Done: {done} | Remaining: {ready}")
    else:
        sync_from_gdrive()
        total, ready, done = count_projects()
        print(f"[*] Status: {total} total, {ready} ready, {done} done")
