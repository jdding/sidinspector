#!/usr/bin/env python3
"""Generate Fig. 1: AUDIT-SID pipeline plus diagnostic preview."""

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

    fig, ax = plt.subplots(figsize=(3.35, 3.48))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    ax.add_patch(Rectangle((0, 0), 1, 1, facecolor="white", edgecolor="none"))
    ax.text(0.02, 0.972, "AUDIT-SID: SID exports to diagnostic evidence", ha="left", va="top", fontsize=7.0, fontweight="bold", color=INK)
    ax.text(0.02, 0.935, "Mapping-first checks preview artifact failures before generator training.", ha="left", va="top", fontsize=5.05, color=MUTED)

    ax.add_patch(Rectangle((0.025, 0.758), 0.95, 0.125, facecolor=BG, edgecolor=LINE, linewidth=0.75))
    steps = [
        ("SID artifact", "any method"),
        ("adapter", "per-method"),
        ("validator", "joins/caveats"),
        ("D1-D5a", "reports"),
        ("audit tables", "CSV/LaTeX"),
    ]
    xs = [0.055, 0.245, 0.435, 0.625, 0.815]
    for i, ((title, subtitle), x) in enumerate(zip(steps, xs)):
        rounded(ax, x, 0.807, 0.13, 0.042, title, fill="white", fs=5.0)
        ax.text(x + 0.065, 0.787, subtitle, ha="center", va="top", fontsize=4.25, color=MUTED)
        if i < len(xs) - 1:
            arrow(ax, x + 0.134, 0.828, xs[i + 1] - 0.004, 0.828)

    ax.text(0.025, 0.720, "Representative diagnostic outputs", ha="left", va="top", fontsize=5.85, fontweight="bold", color=INK)

    w = 0.455
    h = 0.252
    p1 = (0.025, 0.440)
    p2 = (0.520, 0.440)
    p3 = (0.025, 0.155)
    p4 = (0.520, 0.155)

    panel(ax, *p1, w, h, "D1/D2 capacity + collision", "unique codes / full collision")
    hbar(ax, 0.067, 0.592, 0.265, 0.027, 3749 / 23742, GRID)
    hbar(ax, 0.067, 0.545, 0.265, 0.027, 1.0, RESID)
    hbar(ax, 0.067, 0.498, 0.265, 0.027, 0.9769, WARN)
    ax.text(0.340, 0.605, "GRID 3.7k", fontsize=4.55, color=INK, va="center")
    ax.text(0.340, 0.558, "ReSID 23.7k", fontsize=4.55, color=INK, va="center")
    ax.text(0.340, 0.511, "GRID D2 .977", fontsize=4.55, color=INK, va="center")

    panel(ax, *p2, w, h, "D3 collab recovery", "L1 co-occurrence recall")
    hbar(ax, 0.562, 0.592, 0.265, 0.027, 0.0552 / 0.18, GRID)
    hbar(ax, 0.562, 0.545, 0.265, 0.027, 0.1535 / 0.18, RESID)
    hbar(ax, 0.562, 0.498, 0.265, 0.027, 0.447 / 0.50, "#8B6BCB")
    ax.text(0.833, 0.605, "GRID .055", fontsize=4.55, color=INK, va="center")
    ax.text(0.833, 0.558, "ReSID .154", fontsize=4.55, color=INK, va="center")
    ax.text(0.833, 0.511, "cat .447", fontsize=4.55, color=INK, va="center")

    panel(ax, *p3, w, h, "D4 head-tail capacity", "tail unique-SID ratio")
    hbar(ax, 0.067, 0.307, 0.265, 0.027, 0.3695, GRID)
    hbar(ax, 0.067, 0.260, 0.265, 0.027, 1.0, RESID)
    hbar(ax, 0.067, 0.213, 0.265, 0.027, 0.0282, WARN)
    ax.text(0.340, 0.320, "GRID .370", fontsize=4.55, color=INK, va="center")
    ax.text(0.340, 0.273, "ReSID 1.000", fontsize=4.55, color=INK, va="center")
    ax.text(0.340, 0.226, "stress .028", fontsize=4.55, color=INK, va="center")

    panel(ax, *p4, w, h, "D5a prefix cost", "realized, not max depth")
    labels = [("GRID", 3440 / 4096, GRID), ("ReSID", 1280 / 4096, RESID), ("var.", 7914 / 12010, WARN)]
    for i, (name, val, color) in enumerate(labels):
        yy = 0.307 - i * 0.047
        hbar(ax, 0.562, yy, 0.265, 0.027, val, color)
        ax.text(0.833, yy + 0.0135, name, fontsize=4.55, color=INK, va="center")

    ax.add_patch(Rectangle((0.025, 0.055), 0.95, 0.055, facecolor=PALE, edgecolor=LINE, linewidth=0.7))
    ax.text(0.045, 0.082, "Boundary:", ha="left", va="center", fontsize=4.9, fontweight="bold", color=INK)
    ax.text(0.220, 0.082, "artifact diagnostics now; generator quality needs outputs.", ha="left", va="center", fontsize=4.35, color=MUTED)

    pdf_metadata = {
        "Creator": "AUDIT-SID figure generator",
        "Producer": "Matplotlib",
        "CreationDate": None,
        "ModDate": None,
    }
    fig.savefig(OUT_DIR / "fig1_audit_sid_pipeline.pdf", bbox_inches="tight", pad_inches=0.018, metadata=pdf_metadata)
    fig.savefig(OUT_DIR / "fig1_audit_sid_pipeline.png", dpi=300, bbox_inches="tight", pad_inches=0.018)


if __name__ == "__main__":
    main()
