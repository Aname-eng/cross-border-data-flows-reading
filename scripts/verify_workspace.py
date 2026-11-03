"""Run the repository's deterministic acceptance checks from one entry point."""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(label: str, command: list[str], cwd: Path = ROOT) -> None:
    print(f"\n== {label} ==")
    subprocess.run(command, cwd=cwd, check=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--with-lean",
        action="store_true",
        help="also compile the Lean project (downloads/builds mathlib when uncached)",
    )
    parser.add_argument(
        "--check-generated-clean",
        action="store_true",
        help="fail if deterministic rebuilds change tracked files; intended for CI",
    )
    args = parser.parse_args()

    python = sys.executable
    run("finite-optimum derivation", [python, "scripts/check_finite_optimum.py"])
    run("literature-lineage validation", [python, "scripts/build_lineage.py"])
    run("single-page site rebuild", [python, "scripts/build_site.py"])
    run("deck acceptance", [python, "presentation/scripts/check_deck.py"])
    run("site and evidence acceptance", [python, "scripts/check_site.py"])
    run(
        "Python syntax",
        [
            python,
            "-m",
            "compileall",
            "-q",
            "scripts",
            "build",
            "presentation/scripts",
        ],
    )

    node = shutil.which("node")
    if not node:
        raise SystemExit("node is required for docs/app.js syntax validation")
    run("browser JavaScript syntax", [node, "--check", "docs/app.js"])
    run("Git whitespace", ["git", "diff", "--check"])

    if args.with_lean:
        lake = shutil.which("lake")
        if not lake:
            raise SystemExit("lake is required with --with-lean")
        run("Lean finite-optimum theorem", [lake, "build"], ROOT / "verification" / "lean")

    if args.check_generated_clean:
        # Matplotlib lays out CJK glyphs with the host font. The SVG is stable
        # within the supported Windows build environment, while Linux CI uses a
        # different font stack. Check every other generated artifact here; the
        # SVG's mathematical content is covered by check_finite_optimum.py.
        run(
            "generated artifacts are current",
            [
                "git",
                "diff",
                "--exit-code",
                "--",
                ".",
                ":(exclude)docs/assets/finite-optimum-repairs.svg",
            ],
        )

    print("\nWorkspace verification passed.")


if __name__ == "__main__":
    main()
