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
fig, ax = plt.subplots(figsize=(10, 6.5), dpi=300)
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis('off')

# Title
ax.text(50, 96, "Pallets Click: Module Decomposition View (Layered Style)", ha='center', va='center', fontsize=13, fontweight='bold')

# Layer boxes
layers = [
    ("Layer 4: Presentation & CLI Entry", 75, 16, ["decorators.py", "shell_completion.py"], "#e1f5fe", "#0288d1"),
    ("Layer 3: Core Command & Context Model", 52, 16, ["core.py (Command, Group, Context, Parameter)"], "#e8f5e9", "#388e3c"),
    ("Layer 2: Domain Utilities & Type System", 29, 16, ["types.py", "formatting.py", "termui.py", "parser.py"], "#fff3e0", "#f57c00"),
    ("Layer 1: Foundations & Infrastructure", 6, 16, ["utils.py", "exceptions.py", "globals.py", "_compat.py"], "#f3e5f5", "#7b1fa2"),
]

for title, y_bottom, h, modules, bg_color, border_color in layers:
    rect = patches.FancyBboxPatch((8, y_bottom), 84, h, boxstyle="round,pad=1", ec=border_color, fc=bg_color, lw=1.5, zorder=1)
    ax.add_patch(rect)
    ax.text(12, y_bottom + h - 3, title, fontsize=10.5, fontweight='bold', color=border_color)
    mod_str = "   |   ".join(modules)
    ax.text(50, y_bottom + h/2 - 1.5, mod_str, ha='center', va='center', fontsize=9.5, color="#212121",
            bbox=dict(boxstyle="square,pad=0.5", fc="#ffffff", ec="#cccccc", lw=0.8))

# Arrows representing <<allowed to use>>
arrow_props = dict(facecolor='#424242', edgecolor='#424242', width=1.5, headwidth=7, headlength=8, shrink=0.05)
for y_start in [75, 52, 29]:
    ax.annotate("", xy=(50, y_start), xytext=(50, y_start - 7),
                arrowprops=dict(arrowstyle="<-", lw=1.8, color="#37474f"))
    ax.text(53, y_start - 4, "<<allowed to use>>", fontsize=8.5, fontstyle='italic', color="#455a64", va='center')

# Lazy import note between decorators and core
ax.annotate("", xy=(22, 68), xytext=(22, 75),
            arrowprops=dict(arrowstyle="->", lw=1.2, color="#c2185b", linestyle="dashed"))
ax.text(11, 71.5, "lazy import", fontsize=8, color="#c2185b", fontweight="bold")

plt.tight_layout()
plt.savefig(OUTPUT_DIR / "decomposition_view.png", dpi=300)
plt.close()
print("Saved decomposition_view.png")

# ==========================================
# 3. Performance Tactic View (Deferred Loading & Lazy Imports)
# ==========================================
fig, ax = plt.subplots(figsize=(10, 6.2), dpi=300)
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis('off')

ax.text(50, 96, "Performance Tactic: Lazy Subcommand Resolution & Deferred Loading", ha='center', va='center', fontsize=12.5, fontweight='bold')

# Boxes representing sequence flow
steps = [
    (10, 75, "1. CLI Invocation", "Terminal executes `mycli subcmd`.\nCold startup process spawned.", "#e3f2fd", "#1976d2"),
    (10, 52, "2. Fast Root Import", "Only root command module & Click decorators loaded.\nHeavy subcommands bypassed.", "#e8f5e9", "#2e7d32"),
    (10, 29, "3. Lazy Group Match", "Group.get_command(ctx, 'subcmd') checks lazy registry.\nOnly target subcommand module imported on demand.", "#fff8e1", "#fbc02d"),
    (10, 6, "4. Fast Execution & Exit", "Target handler executes, output formatted via Pager/Echo.\nUnused command branches never loaded into memory.", "#fce4ec", "#c2185b"),
]

for x, y, title, desc, bg, border in steps:
    rect = patches.FancyBboxPatch((x, y), 80, 17, boxstyle="round,pad=0.8", ec=border, fc=bg, lw=1.5)
    ax.add_patch(rect)
    ax.text(x + 3, y + 13, title, fontsize=10.5, fontweight='bold', color=border)
    ax.text(x + 3, y + 5.5, desc, fontsize=9.2, color="#263238")

for y in [75, 52, 29]:
    ax.annotate("", xy=(50, y - 6), xytext=(50, y),
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
    if data["sloc"] > 50: # focus on substantive modules
        mod_names.append(m + ".py")
        churns.append(data["git_churn"])
        ccns.append(data["avg_ccn"])
        slocs.append(data["sloc"])

fig, ax = plt.subplots(figsize=(9, 5.5), dpi=300)
sizes = [s * 0.45 for s in slocs]
colors = [c * ch for c, ch in zip(ccns, churns)]

scatter = ax.scatter(churns, ccns, s=sizes, c=colors, cmap="YlOrRd", edgecolors="black", linewidth=1.2, alpha=0.85, zorder=3)
cbar = plt.colorbar(scatter)
cbar.set_label("Hotspot Risk (Git Churn × Avg CCN)", rotation=270, labelpad=15)

for i, name in enumerate(mod_names):
    offset_x = 4 if churns[i] < 200 else -20
    offset_y = 0.15 if ccns[i] < 6 else -0.25
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
# 5. Test Branch Coverage per Module
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
# 6. Performance Benchmarks
# ==========================================
with open(OUTPUT_DIR / "performance_metrics.json", "r") as f:
    perf_m = json.load(f)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.2), dpi=300)

# Subplot 1: Startup latency distribution
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

# Subplot 2: Parse latency microbenchmark
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

print("ALL ARCHITECTURAL PLOTS GENERATED SUCCESSFULLY IN ./analysis/")
