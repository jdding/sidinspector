#!/usr/bin/env python3
"""Generate Fig. 1: SIDInspector pipeline plus diagnostic preview."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle


ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "paper" / "figures"
OUT_DIR.mkdir(parents=True, exist_ok=True)

INK = "#172033"
MUTED = "#5B667A"
LINE = "#CBD3DF"
BG = "#F7F9FC"
GRID = "#4B78C2"
RESID = "#18A085"
WARN = "#C65F2E"
PALE = "#EEF3FA"


def rounded(ax, x, y, w, h, text, fill="#FFFFFF", edge=LINE, fs=5.5, weight="bold"):
    patch = FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle="round,pad=0.010,rounding_size=0.016",
        linewidth=0.85,
        edgecolor=edge,
        facecolor=fill,
    )
    ax.add_patch(patch)
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs, color=INK, fontweight=weight)


def arrow(ax, x0, y0, x1, y1):
    ax.add_patch(
        FancyArrowPatch(
            (x0, y0),
            (x1, y1),
            arrowstyle="-|>",
            mutation_scale=8,
            linewidth=0.75,
            color=MUTED,
            shrinkA=2,
            shrinkB=2,
        )
    )


def panel(ax, x, y, w, h, title, note):
    ax.add_patch(Rectangle((x, y), w, h, facecolor="#FFFFFF", edgecolor=LINE, linewidth=0.8))
    ax.text(x + 0.016, y + h - 0.035, title, ha="left", va="top", fontsize=5.55, color=INK, fontweight="bold")
    ax.text(x + 0.016, y + 0.028, note, ha="left", va="bottom", fontsize=4.35, color=MUTED)


def hbar(ax, x, y, w, h, value, color):
    ax.add_patch(Rectangle((x, y), w, h, facecolor="#EBEEF3", edgecolor="none"))
    ax.add_patch(Rectangle((x, y), max(0.0, min(value, 1.0)) * w, h, facecolor=color, edgecolor="none"))


def main():
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
        }
    )

    fig, ax = plt.subplots(figsize=(3.55, 3.05))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    ax.add_patch(Rectangle((0, 0), 1, 1, facecolor="white", edgecolor="none"))
    ax.text(0.02, 0.972, "SID exports to diagnostics", ha="left", va="top", fontsize=6.8, fontweight="bold", color=INK)
    ax.text(0.02, 0.935, "Adapter checks plus finding preview.", ha="left", va="top", fontsize=4.8, color=MUTED)

    ax.add_patch(Rectangle((0.025, 0.758), 0.95, 0.125, facecolor=BG, edgecolor=LINE, linewidth=0.75))
    steps = [
        ("SID artifact", "any method"),
        ("adapter", "per-method"),
        ("validator", "joins/caveats"),
        ("D1-D5", "reports"),
        ("tables", "CSV/LaTeX"),
    ]
    xs = [0.055, 0.245, 0.435, 0.625, 0.815]
    for i, ((title, subtitle), x) in enumerate(zip(steps, xs)):
        rounded(ax, x, 0.807, 0.13, 0.042, title, fill="white", fs=5.0)
        ax.text(x + 0.065, 0.787, subtitle, ha="center", va="top", fontsize=4.25, color=MUTED)
        if i < len(xs) - 1:
            arrow(ax, x + 0.134, 0.828, xs[i + 1] - 0.004, 0.828)

    ax.text(0.025, 0.720, "Diagnostic preview", ha="left", va="top", fontsize=5.75, fontweight="bold", color=INK)

    w = 0.455
    h = 0.252
    p1 = (0.025, 0.440)
    p2 = (0.520, 0.440)
    p3 = (0.025, 0.155)
    p4 = (0.520, 0.155)

    panel(ax, *p1, w, h, "D3 inversion", "learned address != behavior")
    hbar(ax, 0.067, 0.592, 0.265, 0.027, 0.4470 / 0.4470, "#8B6BCB")
    hbar(ax, 0.067, 0.545, 0.265, 0.027, 0.1535 / 0.4470, RESID)
    hbar(ax, 0.067, 0.498, 0.265, 0.027, 0.0796 / 0.4470, GRID)
    ax.text(0.338, 0.605, "cat 0.447", fontsize=4.0, color=INK, va="center")
    ax.text(0.338, 0.558, "ReSID 0.154", fontsize=4.0, color=INK, va="center")
    ax.text(0.336, 0.511, "GRID 0.052-0.080", fontsize=3.45, color=INK, va="center")

    panel(ax, *p2, w, h, "Capacity ablation", "same GRID path, larger budget")
    hbar(ax, 0.562, 0.592, 0.265, 0.027, 3857 / 9874, GRID)
    hbar(ax, 0.562, 0.545, 0.265, 0.027, 1.0, "#6A8FD4")
    hbar(ax, 0.562, 0.498, 0.265, 0.027, 0.7785 / 0.9759, WARN)
    ax.text(0.832, 0.605, "uniq 3.9k", fontsize=4.0, color=INK, va="center")
    ax.text(0.832, 0.558, "cap 9.9k", fontsize=4.0, color=INK, va="center")
    ax.text(0.832, 0.511, "D2 0.779", fontsize=4.0, color=INK, va="center")

    panel(ax, *p3, w, h, "Ranking context", "D3 Spearman, fixed protocol")
    hbar(ax, 0.067, 0.307, 0.265, 0.027, 0.9429, RESID)
    hbar(ax, 0.067, 0.260, 0.265, 0.027, 0.8857, RESID)
    hbar(ax, 0.067, 0.213, 0.265, 0.027, 0.9429, RESID)
    ax.text(0.338, 0.320, "cand 0.943", fontsize=4.0, color=INK, va="center")
    ax.text(0.338, 0.273, "R@20 0.886", fontsize=4.0, color=INK, va="center")
    ax.text(0.338, 0.226, "NDCG 0.943", fontsize=4.0, color=INK, va="center")

    panel(ax, *p4, w, h, "Cross-vertical + alias risk", "dataset and alias diagnostics")
    labels = [
        ("AB cat 0.968", 0.9684 / 0.9684, "#8B6BCB"),
        ("Sports 0.055", 0.0550 / 0.9684, GRID),
        ("alias 3.86x", 3.86 / 3.86, WARN),
    ]
    for i, (name, val, color) in enumerate(labels):
        yy = 0.307 - i * 0.047
        hbar(ax, 0.562, yy, 0.265, 0.027, val, color)
        ax.text(0.832, yy + 0.0135, name, fontsize=4.0, color=INK, va="center")

    ax.add_patch(Rectangle((0.025, 0.055), 0.95, 0.055, facecolor=PALE, edgecolor=LINE, linewidth=0.7))
    ax.text(0.045, 0.082, "Boundary:", ha="left", va="center", fontsize=4.9, fontweight="bold", color=INK)
    ax.text(0.220, 0.082, "D1-D5 now; D6 refresh pairs and D7 traces are extensions.", ha="left", va="center", fontsize=4.35, color=MUTED)

    pdf_metadata = {
        "Creator": "SIDInspector figure generator",
        "Producer": "Matplotlib",
        "CreationDate": None,
        "ModDate": None,
    }
    fig.savefig(OUT_DIR / "fig1_audit_sid_pipeline.pdf", bbox_inches="tight", pad_inches=0.018, metadata=pdf_metadata)
    fig.savefig(OUT_DIR / "fig1_audit_sid_pipeline.png", dpi=300, bbox_inches="tight", pad_inches=0.018)


if __name__ == "__main__":
    main()
