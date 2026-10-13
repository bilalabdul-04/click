# PA1483 Software Architecture - Assignment 2 Data & Analysis Artifacts

## Overview
This directory contains raw measurement data, analysis scripts, generated architectural figures, and reproduction steps for the quantitative architectural quality attribute assessment of **Pallets Click**.

- **Target System**: [Pallets Click](https://github.com/pallets/click)
- **Analyzed Quality Attributes**: Modifiability, Testability, Performance
- **Analyzed Upstream Commit**: 2247b35ea1c47c727d7a06e51fa280e12a863ff6

## Structure
- data/:
  - git_metrics.json: Commit history totals, yearly activity distribution, contributor commits, and file churn counts.
  - module_metrics.json: AST-extracted lines of code, McCabe Cyclomatic Complexity (average and max), and Martin's coupling (, C_e, I$).
  - 	emporal_coupling.json: CodeScene Temporal Coupling (co-change frequency and degree of coupling %) between all module pairs.
  - cov.json / 	estability_metrics.json: Statement and branch coverage across all modules from pytest-cov, plus assertion density and test-to-code ratio.
  - performance_metrics.json: Cold startup import times, parsing microbenchmarks, and command tree heap memory profiling via 	racemalloc.
- scripts/:
  - nalysis_data_collector.py: Primary metrics extraction script for git churn, AST complexity, coupling, coverage aggregation, and performance benchmarking.
  - extract_temporal_coupling.py: Mines git commit history for non-bulk co-changing revisions to calculate CodeScene Code Coupling.
  - generate_charts.py: Generates all publication-quality architecture figures and metric evaluation graphs.
  - capture_gittruck.py: Automates headless screenshot capture of the local GitTruck visualization workspace.
  - generate_report.py: Assembles base64 images into 
eport_template.html and compiles the final A4 PDF report via Playwright.
- igures/: Rendered diagrams and metric evaluation plots used in the final report.
- PA1483_Assignment_2_Report.pdf: Final submitted report document.

## Exact Reproduction Steps
1. **Environment Setup**:
   `ash
   pip install pytest pytest-cov matplotlib playwright pypdf
   python -m playwright install chromium
   `
2. **Execute Full Test Suite with Branch Coverage**:
   `ash
   PYTHONPATH=src python -m pytest tests/ --cov=click --cov-branch --cov-report=json:cov.json
   `
3. **Run Metrics Extraction**:
   `ash
   python analysis_artifacts/scripts/analysis_data_collector.py
   python analysis_artifacts/scripts/extract_temporal_coupling.py
   `
4. **Generate Figures**:
   `ash
   python analysis_artifacts/scripts/generate_charts.py
   `
5. **Compile Report PDF**:
   `ash
   python analysis_artifacts/scripts/generate_report.py
   `
