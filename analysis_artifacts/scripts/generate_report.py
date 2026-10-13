import base64
from pathlib import Path
from playwright.sync_api import sync_playwright

WORKSPACE = Path.cwd()

def img_to_b64(path):
    p = Path(path)
    if not p.is_absolute():
        p = WORKSPACE / p
    if p.exists():
        encoded = base64.b64encode(p.read_bytes()).decode('utf-8')
        return f"data:image/png;base64,{encoded}"
    return ""

b64_activity = img_to_b64("analysis/activity_curve.png")
b64_gittruck = img_to_b64("analysis/gittruck_overview.png")
b64_decomposition = img_to_b64("analysis/decomposition_view.png")
b64_perf_tactic = img_to_b64("analysis/performance_tactic_view.png")
b64_hotspots = img_to_b64("analysis/modifiability_hotspots.png")
b64_temporal_coupling = img_to_b64("analysis/temporal_coupling.png")
b64_coverage = img_to_b64("analysis/testability_coverage.png")
b64_benchmarks = img_to_b64("analysis/performance_benchmarks.png")

template_path = WORKSPACE / "report_template.html"
with open(template_path, "r", encoding="utf-8") as f:
    content = f.read()

# Replace placeholders
content = content.replace("{{B64_ACTIVITY}}", b64_activity)
content = content.replace("{{B64_GITTRUCK}}", b64_gittruck)
content = content.replace("{{B64_DECOMPOSITION}}", b64_decomposition)
content = content.replace("{{B64_PERF_TACTIC}}", b64_perf_tactic)
content = content.replace("{{B64_HOTSPOTS}}", b64_hotspots)
content = content.replace("{{B64_TEMPORAL_COUPLING}}", b64_temporal_coupling)
content = content.replace("{{B64_COVERAGE}}", b64_coverage)
content = content.replace("{{B64_BENCHMARKS}}", b64_benchmarks)

output_html = WORKSPACE / "PA1483_Assignment_2_Report.html"
output_html.write_text(content, encoding="utf-8")
print(f"Written {output_html}")

pdf_path = WORKSPACE / "PA1483_Assignment_2_Report.pdf"
print("Rendering PDF with Playwright...")

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(output_html.as_uri(), wait_until='networkidle')
    page.pdf(
        path=str(pdf_path),
        format='A4',
        print_background=True,
        margin={
            'top': '18mm',
            'bottom': '20mm',
            'left': '16mm',
            'right': '16mm'
        }
    )
    browser.close()

print(f"SUCCESS: Rendered PDF at {pdf_path}")
