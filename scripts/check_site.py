"""Acceptance checks for the static site and generated deliverables."""
from __future__ import annotations

import csv
import json
import shutil
import subprocess
from pathlib import Path

from bs4 import BeautifulSoup
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
CONTENT = ROOT / "content"

checks: dict[str, bool] = {}

analysis = (CONTENT / "论文解析.md").read_text(encoding="utf-8")
checks["analysis_has_2051_lines"] = len(analysis.splitlines()) == 2051
checks["analysis_has_all_main_sections"] = all(
    marker in analysis
    for marker in [
        "## 1. 模型中有三种",
        "## 7. 从方程求稳态候选解",
        "## 12. 基于后续研究与现实制度",
        "## 14. 原式—解析—课件覆盖表",
    ]
)
checks["markdown_has_no_control_characters"] = all(
    ord(char) >= 32 or char in "\n\r\t"
    for path in CONTENT.rglob("*.md")
    for char in path.read_text(encoding="utf-8")
)

index = (DOCS / "index.html").read_text(encoding="utf-8")
soup = BeautifulSoup(index, "html.parser")
checks["single_page_has_five_content_sections"] = all(
    soup.select_one(selector) is not None
    for selector in ["#report", "#literature", "#finite-optimum", "#routes", "#full-analysis"]
)
checks["single_page_has_auditable_literature_lineage"] = all(
    text in soup.select_one("#literature").get_text()
    for text in [
        "Jones–Tonetti",
        "Trade in Data",
        "Ito–Tomiura",
        "20 条引用",
        "OpenAlex",
        "引用不等于扩展",
    ]
)
checks["single_page_has_three_route_panels"] = len(soup.select("[data-route-panel]")) == 3
checks["single_page_has_route_controls"] = len(soup.select("[data-route-choice]")) == 4
checks["single_page_embeds_full_analysis"] = "原式—解析—课件覆盖表" in soup.get_text()
checks["single_page_has_no_template_markers"] = not any(
    marker in index
    for marker in ["{{REPORT}}", "{{LITERATURE_LINEAGE}}", "{{FINITE_OPTIMUM}}", "{{FULL_ANALYSIS}}", "{{ROUTE_A}}"]
)
checks["single_page_has_no_control_characters"] = all(
    ord(char) >= 32 or char in "\n\r\t" for char in index
)
checks["finite_optimum_figure_exists"] = (DOCS / "assets" / "finite-optimum-repairs.svg").exists()
checks["evidence_downloads_exist"] = all(
    (DOCS / "assets" / name).exists()
    for name in [
        "source-ledger.csv",
        "claim-evidence-matrix.csv",
        "citation-lineage.csv",
        "google-scholar-citing-works.json",
        "finite-optimum-check.json",
    ]
)
with (ROOT / "research" / "source-ledger.csv").open(encoding="utf-8-sig", newline="") as handle:
    source_rows = list(csv.DictReader(handle))
with (ROOT / "research" / "claim-evidence-matrix.csv").open(encoding="utf-8-sig", newline="") as handle:
    claim_rows = list(csv.DictReader(handle))
with (ROOT / "research" / "citation-lineage.csv").open(encoding="utf-8-sig", newline="") as handle:
    lineage_rows = list(csv.DictReader(handle))
checks["expanded_literature_ledgers_are_complete"] = (
    len(source_rows) >= 62 and len(claim_rows) >= 39 and len(lineage_rows) >= 51
)
checks["google_scholar_snapshot_has_20_results"] = len(
    json.loads((ROOT / "research" / "google-scholar-citing-works.json").read_text(encoding="utf-8"))["results"]
) == 20

model_results = json.loads((ROOT / "research" / "finite-optimum-check.json").read_text(encoding="utf-8"))
checks["all_model_checks_pass"] = all(model_results["checks"].values())
checks["closed_exponent_is_20_over_3"] = abs(
    model_results["derived_exponents"]["closed_alpha_xi_rho_minus_1"] - 20 / 3
) < 1e-12
checks["open_exponent_is_4_over_3"] = abs(
    model_results["derived_exponents"]["open_alpha_xi_m_minus_1"] - 4 / 3
) < 1e-12

pdf = ROOT / "deliverables" / "逐步解析.pdf"
checks["analysis_pdf_exists"] = pdf.exists() and pdf.stat().st_size > 50_000
if pdf.exists():
    reader = PdfReader(pdf)
    checks["analysis_pdf_has_substantial_page_count"] = len(reader.pages) >= 40
    first_page_stream = reader.pages[0].get_contents().get_data()
    checks["analysis_pdf_first_page_has_content"] = len(first_page_stream) > 1_000
    pdftotext = shutil.which("pdftotext")
    if pdftotext:
        extracted = subprocess.run(
            [pdftotext, "-f", "1", "-l", "3", "-enc", "UTF-8", str(pdf), "-"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
        ).stdout
        checks["analysis_pdf_has_searchable_chinese"] = "生产、贸易" in extracted and "跨境数据" in extracted
else:
    checks["analysis_pdf_has_substantial_page_count"] = False
    checks["analysis_pdf_first_page_has_content"] = False

failed = [name for name, passed in checks.items() if not passed]
print(json.dumps({"checks": checks, "failed": failed}, ensure_ascii=False, indent=2))
if failed:
    raise SystemExit(1)
