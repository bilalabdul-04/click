# PA1483 Software Architecture - Assignment 2 Data & Analysis Artifacts

## Overview
This directory contains raw measurement data, analysis scripts, generated architectural figures, and reproduction steps for the architectural quality attribute assessment of **Pallets Click**.

- **Target System**: [Pallets Click](https://github.com/pallets/click)
- **Analyzed Quality Attributes**: Modifiability, Testability, Performance
- **Analyzed Source Commit**: 2247b35ea1c47c727d7a06e51fa280e12a863ff6

## Repository Structure
- data/: Raw extracted JSON metrics for Git history churn, AST cyclomatic complexity & coupling, pytest branch coverage, and performance benchmarks.
- scripts/:
  - nalysis_data_collector.py: Collects git statistics, computes AST McCabe Cyclomatic Complexity & Afferent/Efferent coupling, parses pytest-cov outputs, and runs performance microbenchmarks.
  - generate_charts.py: Generates all publication-quality architecture figures and metric graphs.
  - capture_gittruck.py: Automates headless screenshot capture of the local GitTruck visualization workspace.
- igures/: Rendered diagrams and metric evaluation plots used in the final report.

## Reproduction Steps
1. **Prerequisites**: Python 3.10+, Node.js, pytest, pytest-cov, matplotlib.
2. **Run Metrics Extraction**:
   `ash
   python analysis_artifacts/scripts/analysis_data_collector.py
   `
3. **Run Test Coverage**:
   `ash
   PYTHONPATH=src python -m pytest tests/ --cov=click --cov-branch --cov-report=json:cov.json
   `
4. **Generate Figures**:
   `ash
   python analysis_artifacts/scripts/generate_charts.py
   `
