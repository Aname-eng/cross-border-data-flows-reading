"""Build source-grounded visual assets for the Quarto presentation."""
from __future__ import annotations

from pathlib import Path

import fitz
import matplotlib.pyplot as plt
from matplotlib import font_manager
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "presentation" / "assets"
SOURCE = OUT / "source"
OUT.mkdir(parents=True, exist_ok=True)
SOURCE.mkdir(parents=True, exist_ok=True)

PAPER = "#F7F4EC"
INK = "#102A2E"
MUTED = "#62706D"
TEAL = "#177C7B"
CORAL = "#D06449"
GOLD = "#D6A23D"
VIOLET = "#6956A6"
GREEN = "#3C8A66"
LINE = "#D8D4C8"

font_candidates = [
    Path("C:/Windows/Fonts/msyh.ttc"),
    Path("C:/Windows/Fonts/simhei.ttf"),
]
for font_path in font_candidates:
    if font_path.exists():
        font_manager.fontManager.addfont(font_path)
        plt.rcParams["font.family"] = font_manager.FontProperties(fname=font_path).get_name()
        break
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["svg.fonttype"] = "none"
plt.rcParams["svg.hashsalt"] = "ccwz-explorable-deck"


def save_svg(fig: plt.Figure, name: str) -> None:
    path = OUT / name
    fig.savefig(
        path,
        format="svg",
        facecolor=PAPER,
        transparent=False,
        bbox_inches="tight",
        metadata={"Date": None},
    )
    plt.close(fig)
    path.write_text(
        "\n".join(line.rstrip() for line in path.read_text(encoding="utf-8").splitlines()) + "\n",
        encoding="utf-8",
    )


# CCWZ Table 2, foreign-country data importance xi*=1, trade-feasible interval.
fig, ax = plt.subplots(figsize=(11.6, 4.1))
fig.patch.set_facecolor(PAPER)
ax.set_facecolor(PAPER)
rows = [
    ("仅商品贸易", 0.75, 1.22, CORAL),
    ("双向数据流", 0.48, 1.61, TEAL),
]
for y, (label, lo, hi, color) in enumerate(reversed(rows)):
    ax.plot([lo, hi], [y, y], color=color, lw=18, solid_capstyle="round", alpha=.95)
    ax.scatter([lo, hi], [y, y], s=92, color=PAPER, edgecolor=color, linewidth=3, zorder=4)
    ax.text(-.02, y, label, ha="right", va="center", color=INK, fontsize=17, fontweight="bold")
    ax.text(lo, y+.28, f"{lo:.2f}", ha="center", va="bottom", color=color, fontsize=14, fontweight="bold")
    ax.text(hi, y+.28, f"{hi:.2f}", ha="center", va="bottom", color=color, fontsize=14, fontweight="bold")
    ax.text((lo+hi)/2, y-.31, f"区间宽度 {hi-lo:.2f}", ha="center", va="top", color=MUTED, fontsize=12)
ax.axvline(1, color=GOLD, lw=2.2, linestyle=(0, (3, 4)), zorder=0)
ax.text(1, 1.55, "两国数据重要性相同  ξ = ξ*=1", ha="center", va="bottom", color=GOLD, fontsize=13, fontweight="bold")
ax.set_xlim(0, 1.75)
ax.set_ylim(-.75, 1.85)
ax.set_yticks([])
ax.set_xticks(np.arange(0, 1.76, .25))
ax.set_xlabel("本国数据重要性 ξ", color=MUTED, fontsize=13)
ax.tick_params(axis="x", colors=MUTED, labelsize=11, length=0)
for spine in ax.spines.values():
    spine.set_visible(False)
ax.grid(axis="x", color=LINE, lw=1, zorder=-2)
fig.tight_layout(pad=1.0)
save_svg(fig, "table2-intervals.svg")


# Bounded usable-data service: same level and local elasticity at Phi=1.
phi = np.linspace(.22, 5.0, 500)
g_bounded = np.exp(1 - 1 / phi)
g_power = phi
fig, ax = plt.subplots(figsize=(10.8, 4.6))
fig.patch.set_facecolor(PAPER)
ax.set_facecolor(PAPER)
ax.plot(phi, g_power, color=CORAL, lw=3, label=r"原幂函数  $g(\Phi)=\Phi$")
ax.plot(phi, g_bounded, color=GREEN, lw=4, label=r"有界服务  $g(\Phi)=\exp(1-1/\Phi)$")
ax.axhline(np.e, color=GREEN, alpha=.6, lw=1.8, linestyle=(0, (5, 4)))
ax.text(4.95, np.e+.08, r"上界 $e$", ha="right", va="bottom", color=GREEN, fontsize=13)
ax.scatter([1], [1], s=110, color=GOLD, edgecolor=PAPER, linewidth=2, zorder=5)
ax.annotate("同一基准点与局部弹性", xy=(1, 1), xytext=(1.65, .42), color=INK, fontsize=13,
            arrowprops=dict(arrowstyle="->", color=GOLD, lw=2))
ax.set_xlim(.2, 5)
ax.set_ylim(0, 5.2)
ax.set_xlabel(r"企业数据存量 $\Phi/\bar\Phi$", color=MUTED, fontsize=13)
ax.set_ylabel("有效数据服务（归一化）", color=MUTED, fontsize=13)
ax.tick_params(colors=MUTED, labelsize=11, length=0)
for spine in ax.spines.values():
    spine.set_visible(False)
ax.grid(color=LINE, lw=1)
ax.legend(frameon=False, loc="upper left", fontsize=13)
fig.tight_layout(pad=1)
save_svg(fig, "bounded-service.svg")


# Normalized tail curves used to distinguish theta regimes.
L = np.linspace(.02, 2.15, 500)
fig, ax = plt.subplots(figsize=(10.8, 4.6))
fig.patch.set_facecolor(PAPER)
ax.set_facecolor(PAPER)
for theta, color, label in [
    (.7, GREEN, r"$\theta<1$：成本控制尾部"),
    (1.0, GOLD, r"$\theta=1$：比较系数"),
    (4/3, TEAL, r"开放基准 $\theta=4/3$"),
    (20/3, CORAL, r"封闭基准 $\theta=20/3$"),
]:
    value = -L + L**theta
    value = np.clip(value, -1.3, 7)
    ax.plot(L, value, color=color, lw=3, label=label)
ax.axhline(0, color=INK, lw=1.2)
ax.axvline(1, color=LINE, lw=1.2)
ax.set_xlim(0, 2.15)
ax.set_ylim(-1.25, 7)
ax.set_xlabel(r"一次性数据采购 $L$（归一化）", color=MUTED, fontsize=13)
ax.set_ylabel(r"$-L+L^\theta$（归一化）", color=MUTED, fontsize=13)
ax.tick_params(colors=MUTED, labelsize=11, length=0)
for spine in ax.spines.values():
    spine.set_visible(False)
ax.grid(color=LINE, lw=1)
ax.legend(frameon=False, loc="upper left", fontsize=12, ncols=2)
fig.tight_layout(pad=1)
save_svg(fig, "theta-regimes.svg")


# Crop the author's calibration table and statement from the NBER revision.
pdf = ROOT / "build" / "papers" / "core" / "CCWZ-2025-NBER-w31416.pdf"
if pdf.exists():
    with fitz.open(pdf) as doc:
        page = doc[16]  # PDF page 17; printed p.15.
        rect = page.rect
        clip = fitz.Rect(rect.x0 + 38, rect.y0 + 30, rect.x1 - 38, rect.y1 - 45)
        pix = page.get_pixmap(matrix=fitz.Matrix(2.1, 2.1), clip=clip, alpha=False)
        pix.save(SOURCE / "ccwz-calibration-table.png")
else:
    print(f"warning: source PDF missing; kept existing crop if present: {pdf}")

print(f"built presentation assets in {OUT}")
