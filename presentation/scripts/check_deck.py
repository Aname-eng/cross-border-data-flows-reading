"""Acceptance checks for the Quarto explorable deck and its static PDF."""
from __future__ import annotations

from pathlib import Path

from bs4 import BeautifulSoup
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[2]
PRESENTATION = ROOT / "presentation"
HTML = ROOT / "docs" / "slides" / "index.html"
PDF = ROOT / "deliverables" / "CCWZ-explorable-deck.pdf"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


require(HTML.exists(), f"missing rendered deck: {HTML}")
require(PDF.exists(), f"missing static deck PDF: {PDF}")

html = HTML.read_text(encoding="utf-8")
soup = BeautifulSoup(html, "html.parser")
slides = soup.select(".reveal .slides > section")
ids = {slide.get("id") for slide in slides}

require(len(slides) == 35, f"expected 35 slides, found {len(slides)}")
require(len(ids) == 35, "every slide must have a unique id")
require(sum(bool(slide.select_one("aside.notes")) for slide in slides) == 35, "every slide needs speaker notes")
require(sum(bool(slide.select_one(".slide-source")) for slide in slides[1:]) == 34, "every non-title slide needs a visible source line")
require(len(soup.select("section.appendix")) == 10, "expected ten appendix side rooms")
require("<pre><code>&lt;" not in html, "raw presentation HTML was rendered as a code block")

stage = soup.select_one("#model-stage")
require(stage is not None, "missing staged model slide")
require(len(stage.select("[data-stage-show]")) == 4, "model slide must expose four stage controls")
require({node.get("data-stage-min") for node in stage.select("[data-stage-min]")} == {"1", "2", "3", "4"}, "model stage groups are incomplete")
require(len(soup.select("[data-theta-explorer] [data-economy]")) == 2, "theta explorer needs closed/open controls")

for link in soup.select('a[href^="#/"]'):
    target = link.get("href", "")[2:]
    require(target in ids, f"broken reveal link {link.get('href')}")

for phrase in [
    "[0.75, 1.22]",
    "[0.48, 1.61]",
    "θ = 20/3",
    "θ = 4/3",
    "Lee 未引用 CCWZ",
    "25 份 PDF 不等于 25 篇逐页全文审计",
]:
    require(phrase in soup.get_text(" ", strip=True), f"missing acceptance-critical text: {phrase}")

for asset in [
    PRESENTATION / "assets" / "table2-intervals.svg",
    PRESENTATION / "assets" / "bounded-service.svg",
    PRESENTATION / "assets" / "theta-regimes.svg",
    PRESENTATION / "assets" / "source" / "ccwz-calibration-table.png",
    ROOT / "docs" / "slides" / "stage.js",
]:
    require(asset.exists(), f"missing deck asset: {asset}")

css = (PRESENTATION / "theme.scss").read_text(encoding="utf-8")
require("@media print" in css and ".model-stage [data-stage-min]" in css, "print view must reveal the complete staged model")
require(".stage-controls, .theta-control, .stage-hint" in css, "print view must hide live-only controls")

reader = PdfReader(PDF)
require(len(reader.pages) == 35, f"expected 35 PDF pages, found {len(reader.pages)}")
page = reader.pages[0]
width = float(page.mediabox.width)
height = float(page.mediabox.height)
require(abs(width / height - 16 / 9) < 0.02, f"PDF is not 16:9: {width} × {height}")
text = "\n".join((page.extract_text() or "") for page in reader.pages)
for error in ["Misplaced", "Undefined control sequence", "MathJax error"]:
    require(error.lower() not in text.lower(), f"PDF contains a math-rendering error: {error}")

print(
    f"deck checks passed: {len(slides)} slides, "
    f"{len(soup.select('section.appendix'))} appendix rooms, "
    f"{len(reader.pages)} PDF pages"
)
