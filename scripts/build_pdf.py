"""Build the detailed-analysis PDF without modifying the Markdown source.

The checked-in PDF is canonical for collaborators.  This script uses an
installed XeLaTeX, or the local runtime cache created for the original deck.
"""
from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parent
BUILD = ROOT / "build" / "analysis-pdf"
BUILD.mkdir(parents=True, exist_ok=True)
SOURCE = ROOT / "content" / "论文解析.md"
TEX = BUILD / "analysis.tex"
PDF = ROOT / "deliverables" / "逐步解析.pdf"
DOCS_PDF = ROOT / "docs" / "assets" / "逐步解析.pdf"

pandoc = shutil.which("pandoc")
if not pandoc:
    raise SystemExit("pandoc is required")

subprocess.run(
    [
        pandoc,
        str(SOURCE),
        "--standalone",
        "--to=latex",
        "--top-level-division=section",
        "--shift-heading-level-by=1",
        "--toc",
        "--toc-depth=3",
        "--metadata=title:生产、贸易与跨境数据流动",
        "--metadata=subtitle:模型推导、文献脉络与可扩展方向",
        "--metadata=author:云鹰读书会解析",
        "--metadata=date:逐步解析排印版",
        "--variable=documentclass:ctexart",
        "--variable=classoption:fontset=windows",
        "--variable=fontsize:10.5pt",
        "--variable=geometry:top=2.0cm,bottom=2.1cm,left=2.05cm,right=2.05cm",
        "--variable=colorlinks:true",
        "--variable=linkcolor:teal",
        "--variable=urlcolor:teal",
        "--variable=toccolor:teal",
        "--syntax-highlighting=tango",
        "--output",
        str(TEX),
    ],
    cwd=ROOT,
    check=True,
)

# The compact local TeX runtime has fontspec but not unicode-math.  Pandoc's
# default XeTeX template loads unicode-math even though this document only
# needs ordinary LaTeX math fonts, so replace that one template block.
tex_source = TEX.read_text(encoding="utf-8")
tex_source = tex_source.replace(
    "  \\usepackage{unicode-math} % this also loads fontspec\n"
    "  \\defaultfontfeatures{Scale=MatchLowercase}\n"
    "  \\defaultfontfeatures[\\rmfamily]{Ligatures=TeX,Scale=1}\n",
    "  \\usepackage{fontspec}\n"
    "  \\defaultfontfeatures{Scale=MatchLowercase}\n"
    "  \\defaultfontfeatures[\\rmfamily]{Ligatures=TeX,Scale=1}\n",
)
tex_source = tex_source.replace("\\usepackage{lmodern}\n", "")
tex_source = tex_source.replace(
    "\\begin{document}\n",
    "\\begin{document}\n\\setlength{\\emergencystretch}{4em}\n\\sloppy\n",
    1,
)
TEX.write_text(tex_source, encoding="utf-8")

texroot = Path(os.environ.get("TEXLIVE_ROOT", "C:/texlive/2026"))
normal_engine = shutil.which("xelatex")
cache = WORKSPACE / ".build-ccwz"
if normal_engine:
    engine = Path(normal_engine)
    xebin = engine.parent
else:
    engine = cache / "xetex-runtime" / "bin" / "windows" / "xelatex.exe"
    xebin = engine.parent
if not engine.exists():
    raise SystemExit("XeLaTeX not found. Use docs/逐步解析.html and browser print, or provide TEXLIVE_ROOT.")
xdvipdfmx = texroot / "bin" / "windows" / "xdvipdfmx.exe"
if not xdvipdfmx.exists():
    raise SystemExit(f"xdvipdfmx not found at {xdvipdfmx}")

env = os.environ.copy()
env["PATH"] = str(xebin) + os.pathsep + str(texroot / "bin/windows") + os.pathsep + env["PATH"]
if cache.exists() and not normal_engine:
    env["TEXMFROOT"] = texroot.as_posix()
    env["TEXMFCNF"] = (texroot / "texmf-dist/web2c").as_posix()
    env["TEXMF"] = "{" + (cache / "texmf").as_posix() + "," + (texroot / "texmf-dist").as_posix() + "}"
    env["TEXMFVAR"] = cache.as_posix()
    env["TEXMFSYSVAR"] = cache.as_posix()
    env["TEXFORMATS"] = cache.as_posix() + os.pathsep
    env["FONTCONFIG_FILE"] = (cache / "fonts.conf").as_posix()


def run(args: list[str], log_name: str) -> None:
    log = BUILD / log_name
    with log.open("wb") as output:
        result = subprocess.run(args, cwd=BUILD, env=env, stdout=output, stderr=subprocess.STDOUT, timeout=300)
    if result.returncode:
        print(log.read_text(encoding="utf-8", errors="replace")[-8000:])
        raise SystemExit(f"PDF build failed; see {log}")


for pass_number in (1, 2):
    run(
        [str(engine), "--fmt=xelatex", "--no-pdf", "--interaction=nonstopmode", "--halt-on-error", TEX.name],
        f"xelatex-pass-{pass_number}.log",
    )
run([str(xdvipdfmx), "-o", "analysis.pdf", "analysis.xdv"], "xdvipdfmx.log")
PDF.parent.mkdir(parents=True, exist_ok=True)
DOCS_PDF.parent.mkdir(parents=True, exist_ok=True)
shutil.copyfile(BUILD / "analysis.pdf", PDF)
shutil.copyfile(BUILD / "analysis.pdf", DOCS_PDF)
print(f"Built {PDF}")
