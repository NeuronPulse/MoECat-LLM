import scratchattach as sa
import requests
import json
import re
import time
import os
from tqdm import tqdm

BASE_API = "api.scratch.mit.edu"
BASE_LOGIC = "projects.scratch.mit.edu"

REPO_ROOT = "/content/drive/MyDrive/ScratchRepository"
REGISTRY_PATH = f"{REPO_ROOT}/downloaded_registry.json"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) ScratchAgent/8.0"
}

BALANCED_TECH_KEYWORDS = [
    "3D Engine", "Raycasting", "Raytracer", "3D Wireframe", "3D Projection", "Fractal Pen",
    "Sorting Visualizer", "A* Pathfinding", "Binary Tree", "Search Algorithm", "Graph Traversal", "Dijkstra",
    "Neural Network", "Machine Learning", "AI Logic", "Physics Simulation", "Fluid Dynamics", "Rigid Body",
    "Matrix Calculation", "Audio Synthesizer", "Raycast 3D", "Physics Engine Base", "Vector Math",
    "Clone Control", "Custom Block", "Cloud Variable", "List Operations", "String Manipulation",
    "Timer Logic", "UI Framework", "Save Code System",
]


def clean_text(text):
    if not text:
        return ""
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = "\n".join(line.strip() for line in text.split("\n"))
    return text.strip()


def load_registry():
    if os.path.exists(REGISTRY_PATH):
        with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}


def save_registry(registry):
    with open(REGISTRY_PATH, "w", encoding="utf-8") as f:
        json.dump(registry, f, ensure_ascii=False, indent=2)


def setup_repo():
    if not os.path.exists(REPO_ROOT):
        os.makedirs(REPO_ROOT, exist_ok=True)
        print(f"[*] Initialized repo root: {REPO_ROOT}")


def download_file_with_bar(url, save_path, desc_msg):
    try:
        response = requests.get(url, headers=HEADERS, stream=True, timeout=20)
        if response.status_code != 200:
            return False, response.status_code

        total_size = int(response.headers.get("content-length", 0))
        progress_bar = tqdm(total=total_size, unit="B", unit_scale=True, desc=desc_msg, leave=True)

        with open(save_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    progress_bar.update(len(chunk))
        progress_bar.close()
        return True, 200

    except Exception as e:
        return False, str(e)


def run_pipeline(target_count_per_keyword=200):
    setup_repo()
    download_registry = load_registry()
    print(f"[*] Pipeline started. Registry has {len(download_registry)} entries")

    total_new_downloaded = 0

    for keyword in BALANCED_TECH_KEYWORDS:
        print(f"\n[*] Scraping category: {keyword}")

        success_for_keyword = 0
        offset = 0

        while success_for_keyword < target_count_per_keyword:
            try:
                limit = min(40, target_count_per_keyword - success_for_keyword)
                search_results = sa.search_projects(
                    query=keyword, mode="trending", limit=limit, offset=offset
                )

                if not search_results:
                    print(f"[*] No more results for [{keyword}] at offset {offset}")
                    break

                print(f"[*] [OFFSET: {offset}] Found {len(search_results)} candidates")

                for proj in search_results:
                    if success_for_keyword >= target_count_per_keyword:
                        break

                    p_id = str(proj.id)
                    project_dir = f"{REPO_ROOT}/{p_id}"

                    if p_id in download_registry:
                        continue

                    meta_url = f"https://{BASE_API}/projects/{p_id}"
                    time.sleep(0.4)

                    try:
                        meta_res = requests.get(meta_url, headers=HEADERS, timeout=10)
                        if meta_res.status_code != 200:
                            continue

                        meta_data = meta_res.json()
                        title = meta_data.get("title", "Untitled")
                        author_name = meta_data.get("author", {}).get("username", "Anonymous")
                        project_token = meta_data.get("project_token")
                        instructions = meta_data.get("instructions", "")
                        description = meta_data.get("description", "")

                        print(
                            f"[*] [{success_for_keyword + 1}/{target_count_per_keyword}] "
                            f"Category: {keyword} | ID: {p_id} | Title: {title}"
                        )

                        if not project_token:
                            print(f"[*] Project {p_id} token extraction failed, skipping")
                            continue

                        os.makedirs(project_dir, exist_ok=True)

                        code_url = f"https://{BASE_LOGIC}/{p_id}?token={project_token}"
                        save_path = f"{project_dir}/project.json"

                        success, status_info = download_file_with_bar(
                            url=code_url,
                            save_path=save_path,
                            desc_msg=f"[DL] {p_id}",
                        )

                        if success:
                            clean_desc = clean_text(f"{instructions} {description}")

                            metadata_payload = {
                                "project_id": p_id,
                                "project_title": title.strip(),
                                "clean_description": clean_desc,
                                "original_author": author_name,
                                "tech_category": keyword,
                                "project_url": f"https://scratch.mit.edu/projects/{p_id}",
                                "source_platform": "MIT Scratch Core Asset (v8.0)",
                                "license": "CC-BY-SA 2.0",
                                "scraped_timestamp": int(time.time()),
                            }

                            with open(f"{project_dir}/metadata.json", "w", encoding="utf-8") as f_meta:
                                json.dump(metadata_payload, f_meta, ensure_ascii=False, indent=2)

                            download_registry[p_id] = {
                                "title": title,
                                "author": author_name,
                                "category": keyword,
                                "timestamp": int(time.time()),
                            }
                            save_registry(download_registry)

                            total_new_downloaded += 1
                            success_for_keyword += 1
                            print(f"[*] Saved. Registry updated.")
                        else:
                            print(f"[*] Download failed: {status_info}")
                            if os.path.exists(project_dir) and not os.listdir(project_dir):
                                os.rmdir(project_dir)

                    except Exception as e:
                        print(f"[*] Error processing project {p_id}: {e}")

                    time.sleep(0.8)

                offset += 40

            except Exception as e:
                print(f"[*] Pagination error: {e}")
                time.sleep(3.0)
                offset += 40

    print(f"\n[*] Pipeline finished.")
    print(f"[*] New downloads: {total_new_downloaded}. Total registry: {len(download_registry)} entries.")


if __name__ == "__main__":
    run_pipeline(target_count_per_keyword=200)
