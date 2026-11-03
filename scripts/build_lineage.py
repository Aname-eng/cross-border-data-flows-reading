"""Validate the canonical lineage table and publish its website copy.

`research/citation-lineage.csv` is hand-adjudicated evidence.  Earlier versions
of this script rebuilt it from a hard-coded list and could silently restore
stale relationship labels.  The research table is now the single source of
truth; this script only validates stable IDs and copies it to `docs/assets/`.
"""
from __future__ import annotations

import csv
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "research" / "citation-lineage.csv"
TARGET = ROOT / "docs" / "assets" / "citation-lineage.csv"
EXPECTED_FIELDS = [
    "lineage_id",
    "year",
    "work",
    "role",
    "relationship_to_ccwz",
    "main_change_or_relevance",
    "evidence_status",
    "verification_limit",
    "source_id",
]

with SOURCE.open(encoding="utf-8-sig", newline="") as handle:
    reader = csv.DictReader(handle)
    rows = list(reader)
    if reader.fieldnames != EXPECTED_FIELDS:
        raise SystemExit(f"unexpected lineage schema: {reader.fieldnames}")

ids = [row["lineage_id"] for row in rows]
if len(ids) != len(set(ids)):
    duplicates = sorted({item for item in ids if ids.count(item) > 1})
    raise SystemExit(f"duplicate lineage IDs: {duplicates}")
if not rows:
    raise SystemExit("lineage table is empty")

TARGET.parent.mkdir(parents=True, exist_ok=True)
shutil.copyfile(SOURCE, TARGET)
print(f"validated and published {len(rows)} lineage rows")
