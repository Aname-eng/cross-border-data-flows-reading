"""Build the single-page research site from the Markdown sources."""
from __future__ import annotations

import csv
import html
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content"
DOCS = ROOT / "docs"
ASSETS = DOCS / "assets"
TEMPLATE = ROOT / "scripts" / "site-template.html"
PANDOC = shutil.which("pandoc")
if not PANDOC:
    raise SystemExit("pandoc is required")


def md_to_html(path: Path, prefix: str) -> str:
    args = [
        PANDOC,
        str(path),
        "--from=markdown+tex_math_dollars+raw_html+link_attributes",
        "--to=html5",
        "--mathjax",
        "--wrap=none",
        f"--id-prefix={prefix}-",
    ]
    result = subprocess.run(args, cwd=ROOT, check=True, capture_output=True, text=True, encoding="utf-8")
    fragment = result.stdout
    # Paths in the untouched analysis still refer to its original project tree.
    fragment = fragment.replace('href="课件/公式讲解.pdf"', 'href="assets/公式讲解.pdf"')
    fragment = fragment.replace('href="公式讲解.tex"', 'href="../archive/公式讲解.tex"')
    fragment = fragment.replace('src="../docs/assets/', 'src="assets/')
    return fragment


def source_table() -> str:
    path = ROOT / "research" / "source-ledger.csv"
    with path.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    headers = ["编号", "来源", "年份/版本", "类型", "用途"]
    fields = ["source_id", "title", "year_version", "source_type", "use"]
    head = "".join(f"<th>{html.escape(label)}</th>" for label in headers)
    body = []
    for row in rows:
        cells = "".join(f"<td>{html.escape(row.get(field, ''))}</td>" for field in fields)
        body.append(f"<tr>{cells}</tr>")
    return f"<table><thead><tr>{head}</tr></thead><tbody>{''.join(body)}</tbody></table>"


fragments = {
    "{{REPORT}}": md_to_html(CONTENT / "完整汇报.md", "report"),
    "{{FINITE_OPTIMUM}}": md_to_html(CONTENT / "有限最优复核与修复.md", "finite"),
    "{{EXTENSION_OVERVIEW}}": md_to_html(CONTENT / "扩展现实基础.md", "extensions"),
    "{{ROUTE_A}}": md_to_html(CONTENT / "routes" / "路线A-安全许可与合规.md", "route-a"),
    "{{ROUTE_B}}": md_to_html(CONTENT / "routes" / "路线B-质量饱和与算力.md", "route-b"),
    "{{ROUTE_C}}": md_to_html(CONTENT / "routes" / "路线C-训练研发与能力积累.md", "route-c"),
    "{{FULL_ANALYSIS}}": md_to_html(CONTENT / "论文解析.md", "analysis"),
    "{{SOURCE_TABLE}}": source_table(),
}
analysis_lines = len((CONTENT / "论文解析.md").read_text(encoding="utf-8").splitlines())
page = TEMPLATE.read_text(encoding="utf-8").replace("{{ANALYSIS_LINES}}", str(analysis_lines))
for marker, value in fragments.items():
    page = page.replace(marker, value)
leftovers = [part for part in ("{{REPORT}}", "{{FINITE_OPTIMUM}}", "{{FULL_ANALYSIS}}") if part in page]
if leftovers:
    raise SystemExit(f"Unreplaced markers: {leftovers}")
DOCS.mkdir(parents=True, exist_ok=True)
ASSETS.mkdir(parents=True, exist_ok=True)
(DOCS / "index.html").write_text(page, encoding="utf-8")

# Auxiliary source and evidence downloads exposed by the site.
for source, name in [
    (ROOT / "research" / "source-ledger.csv", "source-ledger.csv"),
    (ROOT / "research" / "claim-evidence-matrix.csv", "claim-evidence-matrix.csv"),
    (ROOT / "research" / "finite-optimum-check.json", "finite-optimum-check.json"),
    (ROOT / "deliverables" / "公式讲解.pdf", "公式讲解.pdf"),
]:
    if source.exists():
        shutil.copyfile(source, ASSETS / name)

# Standalone, print-oriented HTML used to produce the detailed-analysis PDF.
analysis_fragment = fragments["{{FULL_ANALYSIS}}"]
analysis_html = f"""<!doctype html>
<html lang=\"zh-CN\"><head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">
<title>生产、贸易与跨境数据流动：逐步解析</title>
<link rel=\"stylesheet\" href=\"styles.css\">
<style>
@page {{ size: A4; margin: 20mm 18mm 22mm; }}
body {{ background: white; }}
.pdf-cover {{ min-height: 86vh; display:flex; flex-direction:column; justify-content:center; max-width:52rem; margin:auto; break-after:page; }}
.pdf-cover h1 {{ font-family:'Noto Serif SC','Songti SC',serif; font-size:3.1rem; line-height:1.25; margin:.7rem 0 1.2rem; }}
.pdf-cover p {{ color:#5d6965; }}
.pdf-cover .rule {{ width:7rem; height:5px; background:#b85d3d; margin-bottom:2rem; }}
.pdf-body {{ max-width:52rem; margin:auto; }}
.pdf-body > h1:first-child {{ display:none; }}
@media print {{
  .pdf-cover {{ min-height:245mm; }}
  .prose h1,.prose h2 {{ break-after:avoid; }}
  .prose h2 {{ break-before:page; }}
  .prose h3,.prose h4 {{ break-after:avoid; }}
  .prose table,.prose pre,.prose blockquote,.prose .math.display {{ break-inside:avoid; }}
  a {{ color:inherit; text-decoration:none; }}
}}
</style>
<script>window.MathJax={{tex:{{inlineMath:[['$','$']],displayMath:[['$$','$$']]}},options:{{skipHtmlTags:['script','noscript','style','textarea','pre','code']}}}};</script>
<script defer src=\"https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js\"></script>
</head><body>
<section class=\"pdf-cover\"><div class=\"rule\"></div><p class=\"eyebrow\">云鹰读书会 · 完整解析</p><h1>生产、贸易与<br>跨境数据流动</h1><p>模型推导、文献脉络与可扩展方向</p><p>Qing Chang · Lin William Cong · Liyong Wang · Longtian Zhang</p><p>本版逐字保留既有解析，只改变排版。</p></section>
<article class=\"prose pdf-body\">{analysis_fragment}</article>
</body></html>"""
(DOCS / "逐步解析.html").write_text(analysis_html, encoding="utf-8")

print(f"Built {DOCS / 'index.html'}")
print(f"Built {DOCS / '逐步解析.html'}")
print(f"Analysis lines: {analysis_lines}")
