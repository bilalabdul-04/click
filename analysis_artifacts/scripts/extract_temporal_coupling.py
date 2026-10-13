import subprocess
import json
from collections import defaultdict
from pathlib import Path
import itertools

REPO_DIR = Path("click-repo")

def get_temporal_coupling():
    # Get all commits with their changed files
    # Exclude merge commits (-m or not having merge in subject)
    cmd = ["git", "log", "--no-merges", "--name-only", "--format=COMMIT:%H"]
    res = subprocess.check_output(cmd, cwd=REPO_DIR).decode("utf-8", errors="ignore")
    
    commits = []
    current_commit = None
    current_files = []
    
    for line in res.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith("COMMIT:"):
            if current_commit and current_files:
                commits.append((current_commit, current_files))
            current_commit = line.replace("COMMIT:", "")
            current_files = []
        else:
            # We are interested in productive python modules in src/click/
            f = line.replace("\\", "/")
            if f.startswith("src/click/") and f.endswith(".py"):
                mod_name = Path(f).name
                current_files.append(mod_name)
                
    if current_commit and current_files:
        commits.append((current_commit, current_files))
        
    # Analyze co-changes
    # Filter out bulk commits that touch > 10 click files at once (e.g. repo renames or lint passes)
    file_commits = defaultdict(set)
    pair_commits = defaultdict(set)
    
    valid_commit_count = 0
    for cid, files in commits:
        unique_files = sorted(list(set(files)))
        if len(unique_files) > 10:
            # Skip massive refactorings/bulk formatting commits
            continue
        valid_commit_count += 1
        for f in unique_files:
            file_commits[f].add(cid)
        for f1, f2 in itertools.combinations(unique_files, 2):
            pair_commits[(f1, f2)].add(cid)
            
    print(f"Analyzed {len(commits)} commits, {valid_commit_count} non-bulk commits touching click modules.")
    
    coupling_results = []
    for (f1, f2), shared in pair_commits.items():
        c_shared = len(shared)
        if c_shared < 5:  # threshold of minimal shared revisions
            continue
        c1 = len(file_commits[f1])
        c2 = len(file_commits[f2])
        # Degree of coupling relative to each and Jaccard
        deg1 = round((c_shared / c1) * 100, 1) if c1 > 0 else 0
        deg2 = round((c_shared / c2) * 100, 1) if c2 > 0 else 0
        jaccard = round((c_shared / (c1 + c2 - c_shared)) * 100, 1)
        coupling_results.append({
            "file_a": f1,
            "file_b": f2,
            "shared_commits": c_shared,
            "commits_a": c1,
            "commits_b": c2,
            "coupling_a_to_b": deg1,
            "coupling_b_to_a": deg2,
            "jaccard_similarity": jaccard
        })
        
    coupling_results.sort(key=lambda x: x["shared_commits"], reverse=True)
    
    print("\n--- TOP TEMPORAL COUPLING PAIRS (CodeScene Code Coupling) ---")
    for cr in coupling_results[:15]:
        print(f"{cr['file_a']} <-> {cr['file_b']}: {cr['shared_commits']} shared commits | Coupling: {cr['coupling_a_to_b']}% / {cr['coupling_b_to_a']}% (Jaccard: {cr['jaccard_similarity']}%)")
        
    out_path = Path("analysis/temporal_coupling.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(coupling_results, f, indent=2)
    print(f"\nSaved coupling results to {out_path}")
    return coupling_results

if __name__ == "__main__":
    get_temporal_coupling()
