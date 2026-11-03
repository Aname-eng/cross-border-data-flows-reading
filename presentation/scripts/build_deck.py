"""Build the Quarto deck, then publish a clean copy to docs/slides."""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PRESENTATION = ROOT / "presentation"
RENDERED = PRESENTATION / "_render"
PUBLISHED = ROOT / "docs" / "slides"
LOCAL_QUARTO = ROOT / "tools" / "quarto" / "Quarto" / "bin" / "quarto.exe"

quarto = shutil.which("quarto")
if not quarto and LOCAL_QUARTO.exists():
    quarto = str(LOCAL_QUARTO)
if not quarto:
    raise SystemExit("Quarto 1.11+ is required (PATH or tools/quarto/Quarto/bin/quarto.exe)")

subprocess.run([sys.executable, str(PRESENTATION / "scripts" / "build_assets.py")], cwd=ROOT, check=True)
if RENDERED.exists():
    shutil.rmtree(RENDERED)
subprocess.run([quarto, "render", str(PRESENTATION / "index.qmd")], cwd=ROOT, check=True)

rendered_index = RENDERED / "index.html"
if not rendered_index.exists():
    raise SystemExit(f"Quarto did not create {rendered_index}")
if PUBLISHED.exists():
    shutil.rmtree(PUBLISHED)
shutil.copytree(RENDERED, PUBLISHED)

# Quarto vendors a few files with trailing spaces. Normalize generated text so
# the committed static artifact passes Git's whitespace gate reproducibly.
text_suffixes = {".css", ".html", ".js", ".map", ".txt", ".yml"}
for path in PUBLISHED.rglob("*"):
    if not path.is_file() or path.suffix.lower() not in text_suffixes:
        continue
    text = path.read_text(encoding="utf-8")
    lines = [line.rstrip(" \t") for line in text.splitlines()]
    while lines and not lines[-1]:
        lines.pop()
    cleaned = "\n".join(lines) + "\n"
    path.write_text(cleaned, encoding="utf-8", newline="\n")

print(f"published {PUBLISHED / 'index.html'}")
print("static PDF: open docs/slides/?print-pdf and save 35 pages to deliverables/CCWZ-explorable-deck.pdf")
