import json
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

OUTPUT_DIR = Path("analysis")
OUTPUT_DIR.mkdir(exist_ok=True)

# Set global styles
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['axes.labelsize'] = 11

# ==========================================
# 1. Activity Curve (2014 - 2026)
# ==========================================
with open(OUTPUT_DIR / "git_metrics.json", "r") as f:
    git_m = json.load(f)

years = list(git_m["commits_per_year"].keys())
commits = list(git_m["commits_per_year"].values())

fig, ax = plt.subplots(figsize=(9, 4.5), dpi=300)
bars = ax.bar(years, commits, color="#1f77b4", edgecolor="#0d47a1", width=0.65, zorder=3)
ax.grid(axis='y', linestyle='--', alpha=0.7, zorder=0)
ax.set_title("Pallets Click: Annual Commit Activity (2014 – 2026)", fontweight="bold", pad=12)
ax.set_xlabel("Year", labelpad=8)
ax.set_ylabel("Number of Commits", labelpad=8)
for bar in bars:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2.0, yval + 8, f"{int(yval)}", ha='center', va='bottom', fontsize=8, color="#333333")

ax.set_ylim(0, max(commits) + 60)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "activity_curve.png", dpi=300)
plt.close()
print("Saved activity_curve.png")

# ==========================================
# 2. Decomposition Architecture View
# ==========================================
fig, ax = plt.subplots(figsize=(11, 7.8), dpi=300)
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis('off')

# Title
ax.text(42, 96.5, "Pallets Click: Module Decomposition View (Layered Architecture Style)", ha='center', va='center', fontsize=12.5, fontweight='bold', color="#0d233a")

# Legend box at top right
legend_rect = patches.FancyBboxPatch((74, 91.5), 23, 7.5, boxstyle="round,pad=0.4", ec="#b0bec5", fc="#fafafa", lw=1)
ax.add_patch(legend_rect)
ax.text(75.5, 96.5, "Legend & Notation", fontsize=7.5, fontweight="bold", color="#37474f")
ax.plot([75.5, 80], [94.2, 94.2], color="#37474f", lw=1.6)
ax.text(81.5, 94.2, "Standard Dependency", fontsize=6.8, va='center', color="#455a64")
ax.plot([75.5, 80], [92.5, 92.5], color="#c2185b", lw=1.4, linestyle="dashed")
ax.text(81.5, 92.5, "Lazy Dynamic Import", fontsize=6.8, va='center', color="#c2185b")

# Layer boxes
layers = [
    ("Layer 4: Presentation & Interface", 69, 18, [
        ("decorators.py", "CLI decorators (@command, @group, @option)"),
        ("shell_completion.py", "Shell completion generators (Bash, Zsh, Fish, PS)")
    ], "#e1f5fe", "#0288d1"),
    ("Layer 3: Core Command & Execution Model", 46, 18, [
        ("core.py", "Core abstractions: Command, Group, Context, Parameter, Option, Argument")
    ], "#e8f5e9", "#2e7d32"),
    ("Layer 2: Domain Utilities & Type System", 23, 18, [
        ("types.py", "ParamType type conversion & validation"),
        ("parser.py", "POSIX/GNU token parser"),
        ("formatting.py", "Help text & table formatter"),
        ("termui.py", "Terminal interaction prompts & pagination")
    ], "#fff3e0", "#f57c00"),
    ("Layer 1: Foundations & Infrastructure", 1.5, 17, [
        ("utils.py", "Stream helpers & echo"),
        ("exceptions.py", "CLI exception hierarchy"),
        ("globals.py", "Thread-local context stack"),
        ("_compat.py", "Cross-version Python shims")
    ], "#f3e5f5", "#7b1fa2"),
]

for title, y_bottom, h, modules, bg_color, border_color in layers:
    rect = patches.FancyBboxPatch((4, y_bottom), 92, h, boxstyle="round,pad=0.8", ec=border_color, fc=bg_color, lw=1.5, zorder=1)
    ax.add_patch(rect)
    ax.text(6.5, y_bottom + h - 3, title, fontsize=10.2, fontweight='bold', color=border_color)
    
    n_mods = len(modules)
    w_mod = 88 / n_mods
    for idx, (m_name, m_desc) in enumerate(modules):
        mx = 6 + idx * w_mod
        my = y_bottom + 2.5
        mw = w_mod - 2.5
        mh = h - 6.8
        m_rect = patches.FancyBboxPatch((mx, my), mw, mh, boxstyle="square,pad=0.3", ec="#90a4ae", fc="#ffffff", lw=0.8, zorder=2)
        ax.add_patch(m_rect)
        ax.text(mx + mw/2, my + mh*0.65, m_name, ha='center', va='center', fontsize=9, fontweight='bold', color="#212121", zorder=3)
        ax.text(mx + mw/2, my + mh*0.28, m_desc, ha='center', va='center', fontsize=7.2, color="#546e7a", wrap=True, zorder=3)

# Downward <<allowed to use>> arrows
for y_conn in [69, 46, 23]:
    ax.annotate("", xy=(50, y_conn - 4), xytext=(50, y_conn),
                arrowprops=dict(arrowstyle="->", lw=2, color="#37474f"))
    ax.text(52, y_conn - 2.2, "<<allowed to use>>", fontsize=8.2, fontstyle='italic', color="#37474f", va='center')

# Lazy import arrow
ax.annotate("", xy=(16, 62), xytext=(16, 69),
            arrowprops=dict(arrowstyle="->", lw=1.5, color="#c2185b", linestyle="dashed"))
ax.text(6.5, 65.5, "<<lazy import>>", fontsize=7.8, color="#c2185b", fontweight="bold")

plt.tight_layout()
plt.savefig(OUTPUT_DIR / "decomposition_view.png", dpi=300)
plt.close()
print("Saved decomposition_view.png")

# ==========================================
# 3. Performance Tactic View (Deferred Loading & Lazy Imports)
# ==========================================
fig, ax = plt.subplots(figsize=(11, 7.5), dpi=300)
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis('off')

# Title & Tactical Goal Callout
ax.text(42, 96.5, "Performance Tactic: Deferred Subcommand Resolution & Lazy Loading", ha='center', va='center', fontsize=12, fontweight='bold', color="#0d233a")

benefit_rect = patches.FancyBboxPatch((74, 91.5), 23, 7.5, boxstyle="round,pad=0.4", ec="#2e7d32", fc="#e8f5e9", lw=1)
ax.add_patch(benefit_rect)
ax.text(75.5, 96.5, "Architectural Tactic Goal", fontsize=7.5, fontweight="bold", color="#2e7d32")
ax.text(75.5, 94.2, "\u2022 Cold import < 50 ms", fontsize=6.8, color="#1b5e20")
ax.text(75.5, 92.5, "\u2022 Tree heap < 1 MB", fontsize=6.8, color="#1b5e20")

steps = [
    (6, 69, "Step 1: Cold Invocation & Minimal Root Loading", 
     "Terminal invokes CLI (e.g. `mycli build --opt`). Python boots and imports `click` runtime in ~18 ms.\nOnly root command decorator and Click context are loaded into memory.", "#e3f2fd", "#1976d2"),
    (6, 47, "Step 2: Token Parsing & Root Dispatch", 
     "Parser processes command tokens in 25–65 µs. Matches target command identifier 'build'.\nRoot `click.Group` queries its lazy command registry instead of loading full tree.", "#e8f5e9", "#2e7d32"),
    (6, 25, "Step 3: Just-In-Time Dynamic Subcommand Import", 
     "`Group.get_command(ctx, 'build')` dynamically imports only the target module (`mycli.build`).\nUnrelated command subtrees (e.g., `deploy`, `monitor`) and their heavy dependencies remain unimported.", "#fff8e1", "#fbc02d"),
    (6, 3, "Step 4: Handler Execution, Stream Output & Clean Exit", 
     "Target handler executes with isolated `CliRunner`/`Context`. Stream output written via Pager/Echo.\nEntire memory footprint remains ~720 KB without bloated dependency loading.", "#fce4ec", "#c2185b"),
]

for x, y, title, desc, bg, border in steps:
    rect = patches.FancyBboxPatch((x, y), 88, 17, boxstyle="round,pad=0.8", ec=border, fc=bg, lw=1.5)
    ax.add_patch(rect)
    ax.text(x + 2.5, y + 13, title, fontsize=9.8, fontweight='bold', color=border)
    ax.text(x + 2.5, y + 5.5, desc, fontsize=8.6, color="#263238")

for y in [69, 47, 25]:
    ax.annotate("", xy=(50, y - 4.5), xytext=(50, y),
                arrowprops=dict(arrowstyle="->", lw=2, color="#37474f"))

plt.tight_layout()
plt.savefig(OUTPUT_DIR / "performance_tactic_view.png", dpi=300)
plt.close()
print("Saved performance_tactic_view.png")

# ==========================================
# 4. CodeScene Hotspots Map (Churn vs Cyclomatic Complexity)
# ==========================================
with open(OUTPUT_DIR / "module_metrics.json", "r") as f:
    mod_m = json.load(f)

mod_names = []
churns = []
ccns = []
slocs = []

for m, data in mod_m.items():
    if data["sloc"] > 50:
        mod_names.append(m + ".py")
        churns.append(data["git_churn"])
        ccns.append(data["avg_ccn"])
        slocs.append(data["sloc"])

fig, ax = plt.subplots(figsize=(9.5, 5.8), dpi=300)
sizes = [s * 0.45 for s in slocs]
colors = [c * ch for c, ch in zip(ccns, churns)]

scatter = ax.scatter(churns, ccns, s=sizes, c=colors, cmap="YlOrRd", edgecolors="black", linewidth=1.2, alpha=0.85, zorder=3)
cbar = plt.colorbar(scatter)
cbar.set_label("CodeScene Hotspot Score (Git Churn × Avg CCN)", rotation=270, labelpad=15)

for i, name in enumerate(mod_names):
    offset_x = 4 if churns[i] < 200 else -25
    offset_y = 0.15 if ccns[i] < 6 else -0.28
    ax.annotate(name, (churns[i], ccns[i]), textcoords="offset points", xytext=(offset_x, offset_y), fontsize=8.5, fontweight="bold")

ax.set_title("CodeScene Hotspot Map: Module Complexity vs. Commit Churn", fontweight="bold", pad=12)
ax.set_xlabel("Git Commit Churn (Modifications in Repository History)", labelpad=8)
ax.set_ylabel("Average McCabe Cyclomatic Complexity (CCN)", labelpad=8)
ax.grid(True, linestyle="--", alpha=0.6, zorder=0)

plt.tight_layout()
plt.savefig(OUTPUT_DIR / "modifiability_hotspots.png", dpi=300)
plt.close()
print("Saved modifiability_hotspots.png")

# ==========================================
# 5. CodeScene Temporal Coupling (Code Coupling)
# ==========================================
with open(OUTPUT_DIR / "temporal_coupling.json", "r") as f:
    tc_data = json.load(f)

top_tc = tc_data[:10]
pair_labels = [f"{item['file_a']} \u2194 {item['file_b']}" for item in top_tc]
shared_commits = [item["shared_commits"] for item in top_tc]
coupling_percentages = [item["coupling_b_to_a"] for item in top_tc]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 5.2), dpi=300)

y_pos = np.arange(len(pair_labels))

bars1 = ax1.barh(y_pos, shared_commits, color="#1976d2", edgecolor="#0d47a1", height=0.65, zorder=3)
ax1.set_yticks(y_pos)
ax1.set_yticklabels(pair_labels, fontsize=9, fontweight="bold")
ax1.invert_yaxis()
ax1.set_xlabel("Shared Git Commits (Co-Change Revisions)", labelpad=8)
ax1.set_title("Co-Change Frequency (Code Coupling)", fontweight="bold", pad=10)
ax1.grid(axis='x', linestyle='--', alpha=0.6, zorder=0)
for bar in bars1:
    w = bar.get_width()
    ax1.text(w + 0.6, bar.get_y() + bar.get_height()/2.0, f"{int(w)}", va='center', fontsize=8.5, color="#212121")
ax1.set_xlim(0, max(shared_commits) + 4)

bars2 = ax2.barh(y_pos, coupling_percentages, color="#e65100", edgecolor="#bf360c", height=0.65, zorder=3)
ax2.set_yticks(y_pos)
ax2.set_yticklabels([])
ax2.invert_yaxis()
ax2.set_xlabel("Degree of Coupling (% of Revisions Coupled)", labelpad=8)
ax2.set_title("CodeScene Coupling Degree (%)", fontweight="bold", pad=10)
ax2.grid(axis='x', linestyle='--', alpha=0.6, zorder=0)
for bar in bars2:
    w = bar.get_width()
    ax2.text(w + 1.2, bar.get_y() + bar.get_height()/2.0, f"{w:.1f}%", va='center', fontsize=8.5, color="#212121")
ax2.set_xlim(0, 90)

plt.suptitle("CodeScene Temporal Coupling Analysis: Co-Change Revisions Across Modules", fontsize=12, fontweight="bold", y=0.98)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "temporal_coupling.png", dpi=300)
plt.close()
print("Saved temporal_coupling.png")

# ==========================================
# 6. Test Branch Coverage per Module
# ==========================================
with open(OUTPUT_DIR / "testability_metrics.json", "r") as f:
    test_m = json.load(f)

cov_files = test_m["coverage"]["files"]
core_modules = ["core.py", "parser.py", "formatting.py", "types.py", "shell_completion.py", "testing.py", "termui.py", "decorators.py", "utils.py", "_compat.py", "_termui_impl.py"]

mod_labels = []
stmt_cov = []
branch_cov = []

for m in core_modules:
    if m in cov_files:
        info = cov_files[m]
        mod_labels.append(m)
        stmt_cov.append(info["percent_covered"])
        br_pct = round(info["covered_branches"] / info["num_branches"] * 100, 1) if info["num_branches"] > 0 else 100.0
        branch_cov.append(br_pct)

x = np.arange(len(mod_labels))
width = 0.38

fig, ax = plt.subplots(figsize=(10, 5), dpi=300)
rects1 = ax.bar(x - width/2, stmt_cov, width, label='Statement Coverage (%)', color="#2ca02c", edgecolor="#1b5e20", zorder=3)
rects2 = ax.bar(x + width/2, branch_cov, width, label='Branch Coverage (%)', color="#1f77b4", edgecolor="#0d47a1", zorder=3)

ax.set_ylabel('Coverage Percentage (%)', labelpad=8)
ax.set_title('Click Testability: Statement and Branch Coverage by Module', fontweight="bold", pad=12)
ax.set_xticks(x)
ax.set_xticklabels(mod_labels, rotation=35, ha="right", fontsize=9)
ax.set_ylim(0, 110)
ax.axhline(80, color='red', linestyle='--', linewidth=1, alpha=0.7, label='Target Threshold (80%)')
ax.grid(axis='y', linestyle='--', alpha=0.6, zorder=0)
ax.legend(loc='lower left', frameon=True)

plt.tight_layout()
plt.savefig(OUTPUT_DIR / "testability_coverage.png", dpi=300)
plt.close()
print("Saved testability_coverage.png")

# ==========================================
# 7. Performance Benchmarks
# ==========================================
with open(OUTPUT_DIR / "performance_metrics.json", "r") as f:
    perf_m = json.load(f)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.2), dpi=300)

times = [perf_m["import_overhead"]["min_ms"], perf_m["import_overhead"]["avg_ms"], perf_m["import_overhead"]["max_ms"]]
cats = ["Min Latency", "Average Latency", "Max Latency"]
b1 = ax1.bar(cats, times, color=["#4caf50", "#2196f3", "#ff9800"], edgecolor="#333333", width=0.55, zorder=3)
ax1.set_ylabel("Cold Startup Time (ms)")
ax1.set_title("Click CLI Import Overhead (30 Invocations)", fontweight="bold")
ax1.grid(axis='y', linestyle='--', alpha=0.6, zorder=0)
for bar in b1:
    yval = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2.0, yval + 0.4, f"{yval:.2f} ms", ha='center', va='bottom', fontsize=9)
ax1.set_ylim(0, max(times) + 4)

parse_cats = ["Simple Command", "Nested Group Dispatch"]
latencies = [perf_m["parse_dispatch_latency"]["simple_command_parse_us"], perf_m["parse_dispatch_latency"]["nested_group_parse_us"]]
b2 = ax2.bar(parse_cats, latencies, color=["#9c27b0", "#00bcd4"], edgecolor="#333333", width=0.45, zorder=3)
ax2.set_ylabel("Execution Latency (microseconds)")
ax2.set_title("Command Parsing Latency (10k Runs)", fontweight="bold")
ax2.grid(axis='y', linestyle='--', alpha=0.6, zorder=0)
for bar in b2:
    yval = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2.0, yval + 1.2, f"{yval:.1f} \u03bcs", ha='center', va='bottom', fontsize=9)
ax2.set_ylim(0, max(latencies) + 12)

plt.tight_layout()
plt.savefig(OUTPUT_DIR / "performance_benchmarks.png", dpi=300)
plt.close()
print("Saved performance_benchmarks.png")

print("ALL ARCHITECTURAL PLOTS GENERATED CLEANLY IN ./analysis/")
