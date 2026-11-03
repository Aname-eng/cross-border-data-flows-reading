"""Acceptance checks for the static site and generated deliverables."""
from __future__ import annotations

import csv
import json
import re
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
checks["single_page_has_seven_content_sections"] = all(
    soup.select_one(selector) is not None
    for selector in [
        "#report",
        "#literature",
        "#repair-map",
        "#finite-optimum",
        "#routes",
        "#full-analysis",
        "#evidence",
    ]
)
checks["single_page_integrates_error_repairs_and_extensions"] = all(
    text in soup.select_one("#repair-map").get_text()
    for text in [
        "先闭合企业问题，再选择经济机制",
        "有界有效数据服务",
        "有限许可或共同数据包",
        "企业吸收成本",
        "安全许可与合同设计",
        "信息质量、收益饱和与算力互补",
        "训练、研发与利用能力积累",
        "修复后必须重新计算哪些结果",
    ]
)
checks["single_page_has_interactive_theta_diagnostic"] = (
    soup.select_one("[data-theta-explorer]") is not None
    and len(soup.select("[data-theta-preset]")) == 3
    and len(soup.select("[data-theta-input]")) == 3
    and soup.select_one("[data-theta-result]") is not None
)
checks["repair_map_has_background_and_literature_boundaries"] = all(
    text in soup.select_one("#repair-map").get_text()
    for text in [
        "促进和规范数据跨境流动规定",
        "Data Security Program",
        "Jones–Tonetti",
        "Farboodi–Veldkamp",
        "Dubus",
        "Demirer",
        "Lee（2025）",
        "观察性估计已经识别",
    ]
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
        "Lee（2025）",
        "没有引用 CCWZ",
        "38 国、44 行业",
        "35,575 款应用",
        "655,200 个观测",
        "2,628 个双边年度观测",
    ]
)
checks["single_page_has_full_text_relationship_matrix"] = all(
    text in soup.select_one("#deep-reading").parent.get_text()
    for text in [
        "前置机制、CCWZ 增量与后续偏离",
        "数据与算力的替代弹性约为 0.33–0.44",
        "下游经济体开业数相对处理前均值提高 49%",
        "有限最优修复",
    ]
)
checks["single_page_explains_lean_boundary"] = all(
    text in soup.select_one("#finite-optimum").get_text()
    for text in ["Lean 4.34.1", "open_profit_unbounded", "它没有形式化 CCWZ"]
)
checks["single_page_has_three_route_panels"] = len(soup.select("[data-route-panel]")) == 3
checks["single_page_has_route_controls"] = len(soup.select("[data-route-choice]")) == 4
checks["single_page_links_to_explorable_deck"] = (
    len(soup.select('a[href="slides/"]')) >= 1
    and (DOCS / "slides" / "index.html").exists()
    and (DOCS / "assets" / "CCWZ-explorable-deck.pdf").exists()
)
checks["single_page_embeds_full_analysis"] = "原式—解析—课件覆盖表" in soup.get_text()
checks["single_page_has_no_template_markers"] = not any(
    marker in index
    for marker in [
        "{{REPORT}}",
        "{{LITERATURE_LINEAGE}}",
        "{{DEEP_READING}}",
        "{{REPAIR_MAP}}",
        "{{FINITE_OPTIMUM}}",
        "{{EXTENSION_OVERVIEW}}",
        "{{FULL_ANALYSIS}}",
        "{{ROUTE_A}}",
        "{{ROUTE_B}}",
        "{{ROUTE_C}}",
        "{{SOURCE_TABLE}}",
    ]
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
        "deep-reading-matrix.csv",
        "paper-corpus-manifest.csv",
        "background-reading-notes.md",
        "google-scholar-citing-works.json",
        "finite-optimum-check.json",
        "CCWZ-explorable-deck.pdf",
    ]
)
with (ROOT / "research" / "source-ledger.csv").open(encoding="utf-8-sig", newline="") as handle:
    source_rows = list(csv.DictReader(handle))
with (ROOT / "research" / "claim-evidence-matrix.csv").open(encoding="utf-8-sig", newline="") as handle:
    claim_rows = list(csv.DictReader(handle))
with (ROOT / "research" / "citation-lineage.csv").open(encoding="utf-8-sig", newline="") as handle:
    lineage_rows = list(csv.DictReader(handle))
with (ROOT / "research" / "deep-reading-matrix.csv").open(encoding="utf-8-sig", newline="") as handle:
    deep_reading_rows = list(csv.DictReader(handle))
with (ROOT / "research" / "paper-corpus-manifest.csv").open(encoding="utf-8-sig", newline="") as handle:
    corpus_rows = list(csv.DictReader(handle))
checks["expanded_literature_ledgers_are_complete"] = (
    len(source_rows) >= 62
    and len(claim_rows) >= 51
    and len(lineage_rows) >= 51
    and len(deep_reading_rows) == 18
)
checks["ledger_ids_are_unique"] = all(
    len(values) == len(set(values))
    for values in [
        [row["source_id"] for row in source_rows],
        [row["claim_id"] for row in claim_rows],
        [row["lineage_id"] for row in lineage_rows],
        [row["matrix_id"] for row in deep_reading_rows],
        [row["corpus_id"] for row in corpus_rows],
    ]
)
known_source_ids = {row["source_id"] for row in source_rows}
referenced_source_ids = {
    match
    for row in [*claim_rows, *lineage_rows, *deep_reading_rows]
    for match in re.findall(
        r"\bS\d+(?:v\d+)?\b",
        ";".join(
            str(value)
            for key, value in row.items()
            if key in {"source_ids", "source_id"}
        ),
    )
}
checks["evidence_tables_only_reference_known_sources"] = (
    referenced_source_ids <= known_source_ids
)
checks["paper_corpus_has_25_pdfs_and_1012_pages"] = (
    len(corpus_rows) == 25 and sum(int(row["pages"]) for row in corpus_rows) == 1012
)
checks["paper_corpus_has_no_unread_queue"] = (
    sum(row["reading_status"] == "queued" for row in corpus_rows) == 0
    and all(row["evidence_boundary"].strip() for row in corpus_rows)
    and any(row["reading_status"] == "full-model-audit" for row in corpus_rows)
    and any(row["reading_status"] == "superseded" for row in corpus_rows)
)
background_source_ids = {"S39", "S45", "S57", "S59", "S60"}
checks["five_background_papers_are_full_text_checked"] = {
    row["source_id"]
    for row in source_rows
    if row["evidence_state"] == "focused-full-text-read"
} >= background_source_ids
checks["sun_trefler_record_has_correct_author_and_sample"] = any(
    row["source_id"] == "S45"
    and row["authors"].startswith("Ruiqi Sun;")
    and "35575款应用" in row["use"]
    for row in source_rows
)
checks["wang_2025_is_full_text_and_direct_citation"] = any(
    row["source_id"] == "S56"
    and row["evidence_state"] == "full-text-read"
    and "直接引用CCWZ" in row["use"]
    for row in source_rows
)
checks["lee_relationship_is_corrected"] = any(
    row["lineage_id"] == "N02"
    and row["relationship_to_ccwz"] == "does not cite CCWZ in checked full paper"
    for row in lineage_rows
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
