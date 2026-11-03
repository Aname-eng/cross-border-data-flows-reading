"""Extract a page-delimited local corpus without erasing manual reading status.

By default, existing text files are kept so that manually corrected extraction is
not overwritten. Pass ``--refresh`` to regenerate every text file from its PDF.
The manifest is merged by ``group/filename``: stable IDs, reading status, and
human-written evidence boundaries survive every rebuild.
"""
from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path

import fitz

ROOT = Path(__file__).resolve().parents[1]
PAPER_ROOT = ROOT / "build" / "papers"
TEXT_ROOT = PAPER_ROOT / "text"
MANIFEST = ROOT / "research" / "paper-corpus-manifest.csv"
FIELDS = [
    "corpus_id",
    "group",
    "filename",
    "pages",
    "pages_with_text",
    "text_file",
    "title_metadata",
    "local_only",
    "reading_status",
    "evidence_boundary",
]


def load_existing() -> tuple[dict[tuple[str, str], dict[str, str]], int]:
    if not MANIFEST.exists():
        return {}, 0
    with MANIFEST.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    by_file = {(row["group"], row["filename"]): row for row in rows}
    numbers = [
        int(match.group(1))
        for row in rows
        if (match := re.fullmatch(r"P(\d+)", row.get("corpus_id", "")))
    ]
    return by_file, max(numbers, default=0)


def extract_pdf(pdf: Path) -> tuple[int, int, str]:
    with fitz.open(pdf) as doc:
        parts: list[str] = []
        nonempty = 0
        for number, page in enumerate(doc, 1):
            # NUL bytes break grep and downstream Markdown tooling but carry no
            # useful PDF text information.
            text = page.get_text("text").replace("\x00", "")
            if text.strip():
                nonempty += 1
            parts.append(f"\n\n===== PDF PAGE {number} =====\n\n{text}")
        title = doc.metadata.get("title", "") or ""
        return len(doc), nonempty, title


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--refresh",
        action="store_true",
        help="regenerate existing text files instead of preserving corrected copies",
    )
    args = parser.parse_args()

    TEXT_ROOT.mkdir(parents=True, exist_ok=True)
    existing, next_id = load_existing()
    rows: list[dict[str, object]] = []
    written = 0

    for pdf in sorted(PAPER_ROOT.glob("*/*.pdf")):
        rel = pdf.relative_to(PAPER_ROOT)
        key = (rel.parent.name, rel.name)
        previous = existing.get(key, {})
        pages, nonempty, metadata_title = extract_pdf(pdf)
        out = TEXT_ROOT / f"{rel.parent.name}--{rel.stem}.txt"

        if args.refresh or not out.exists():
            with fitz.open(pdf) as doc:
                parts = []
                for number, page in enumerate(doc, 1):
                    text = page.get_text("text").replace("\x00", "")
                    parts.append(f"\n\n===== PDF PAGE {number} =====\n\n{text}")
            out.write_text("".join(parts), encoding="utf-8")
            written += 1

        corpus_id = previous.get("corpus_id", "")
        if not corpus_id:
            next_id += 1
            corpus_id = f"P{next_id:02d}"

        rows.append(
            {
                "corpus_id": corpus_id,
                "group": rel.parent.name,
                "filename": rel.name,
                "pages": pages,
                "pages_with_text": nonempty,
                "text_file": out.relative_to(ROOT).as_posix(),
                "title_metadata": metadata_title or previous.get("title_metadata", ""),
                "local_only": previous.get("local_only", "yes"),
                "reading_status": previous.get("reading_status", "queued"),
                "evidence_boundary": previous.get(
                    "evidence_boundary",
                    "full PDF downloaded; focused reading pending",
                ),
            }
        )

    with MANIFEST.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)

    total_pages = sum(int(row["pages"]) for row in rows)
    print(
        f"Indexed {len(rows)} PDFs / {total_pages} pages; "
        f"wrote {written} text file(s); preserved manual reading fields."
    )


if __name__ == "__main__":
    main()
