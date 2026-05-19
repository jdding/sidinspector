#!/usr/bin/env python3
"""Generate the AUDIT-SID artifact pipeline figure."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch


ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "paper" / "figures"
OUT_DIR.mkdir(parents=True, exist_ok=True)


def add_box(ax, x, y, w, h, title, lines, color):
    box = FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle="round,pad=0.018,rounding_size=0.025",
        linewidth=0.9,
        edgecolor="#2f3640",
        facecolor=color,
    )
    ax.add_patch(box)
    ax.text(
        x + 0.035,
        y + h - 0.105,
        title,
        ha="left",
        va="top",
        fontsize=7.8,
        fontweight="bold",
        color="#111827",
    )
    ax.text(
        x + 0.035,
        y + h - 0.295,
        "\n".join(lines),
        ha="left",
        va="top",
        fontsize=6.35,
        linespacing=1.1,
        color="#374151",
    )


def add_arrow(ax, x0, x1, y):
    arrow = FancyArrowPatch(
        (x0, y),
        (x1, y),
        arrowstyle="-|>",
        mutation_scale=10,
        linewidth=1.0,
        color="#4b5563",
        shrinkA=2,
        shrinkB=2,
    )
    ax.add_patch(arrow)


def main():
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
        }
    )

    fig, ax = plt.subplots(figsize=(7.15, 2.15))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    boxes = [
        (
            0.015,
            "Tokenizer\nexports",
            ["repo SIDs", "public mappings", "sanity controls"],
            "#e8f1ff",
        ),
        (
            0.207,
            "Artifact\ncontract",
            ["sid_assignments", "item metadata", "interactions"],
            "#e9f7ef",
        ),
        (
            0.399,
            "Validation",
            ["join coverage", "prefix depth", "adapter caveats"],
            "#fff4df",
        ),
        (
            0.591,
            "Diagnostics",
            ["D1 code use", "D2 full collisions", "D3 collab prefix", "D4 head-tail", "D5a prefix cost"],
            "#f4ecff",
        ),
        (
            0.783,
            "Reviewer\nartifacts",
            ["CSV / Markdown", "LaTeX tables", "failure slices"],
            "#eef2f7",
        ),
    ]

    w, h, y = 0.17, 0.57, 0.31
    for x, title, lines, color in boxes:
        add_box(ax, x, y, w, h, title, lines, color)

    for i in range(len(boxes) - 1):
        add_arrow(ax, boxes[i][0] + w + 0.006, boxes[i + 1][0] - 0.006, y + h / 2)

    ax.text(
        0.015,
        0.19,
        "Comparable audit artifacts without retraining a downstream generator",
        ha="left",
        va="center",
        fontsize=7.6,
        color="#111827",
    )
    ax.plot([0.015, 0.955], [0.155, 0.155], color="#9ca3af", linewidth=0.7)
    ax.text(
        0.015,
        0.075,
        "v0: D1-D5a; optional D6 churn; D7 requires generator outputs",
        ha="left",
        va="center",
        fontsize=7.2,
        color="#4b5563",
    )

    pdf_metadata = {
        "Creator": "AUDIT-SID figure generator",
        "Producer": "Matplotlib",
        "CreationDate": None,
        "ModDate": None,
    }
    fig.savefig(
        OUT_DIR / "fig1_audit_sid_pipeline.pdf",
        bbox_inches="tight",
        pad_inches=0.015,
        metadata=pdf_metadata,
    )
    fig.savefig(OUT_DIR / "fig1_audit_sid_pipeline.png", dpi=300, bbox_inches="tight", pad_inches=0.015)


if __name__ == "__main__":
    main()
