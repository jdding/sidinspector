#!/usr/bin/env python3
"""Generate the AUDIT-SID artifact-contract figure."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch


ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "paper" / "figures"
OUT_DIR.mkdir(parents=True, exist_ok=True)


def add_box(ax, x, y, w, h, title, lines, color, edge="#334155", fontsize=5.0, title_size=5.9):
    box = FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle="round,pad=0.012,rounding_size=0.012",
        linewidth=0.8,
        edgecolor=edge,
        facecolor=color,
    )
    ax.add_patch(box)
    ax.text(
        x + 0.018,
        y + h - 0.042,
        title,
        ha="left",
        va="top",
        fontsize=title_size,
        fontweight="bold",
        color="#0f172a",
    )
    if lines:
        ax.text(
            x + 0.018,
            y + h - 0.095,
            "\n".join(lines),
            ha="left",
            va="top",
            fontsize=fontsize,
            linespacing=0.96,
            color="#334155",
        )


def add_label(ax, x, y, text, color="#334155", weight="normal", size=6.6):
    ax.text(x, y, text, ha="left", va="center", fontsize=size, color=color, fontweight=weight)


def add_arrow(ax, xy0, xy1, color="#64748b"):
    arrow = FancyArrowPatch(
        xy0,
        xy1,
        arrowstyle="-|>",
        mutation_scale=8,
        linewidth=0.75,
        color=color,
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

    fig, ax = plt.subplots(figsize=(7.15, 2.55))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    ax.text(0.02, 0.955, "AUDIT-SID maps heterogeneous SID exports to comparable audit evidence", ha="left", va="top", fontsize=8.0, fontweight="bold", color="#0f172a")
    ax.plot([0.02, 0.98], [0.925, 0.925], color="#CBD5E1", linewidth=0.8)

    add_label(ax, 0.02, 0.82, "1. contract", "#0f766e", "bold", size=6.8)
    input_y, input_h = 0.76, 0.12
    input_boxes = [
        (0.16, "sid_assignments", ["required"], "#dcfce7"),
        (0.37, "item_metadata", ["semantic slices"], "#ecfeff"),
        (0.58, "interactions", ["D3/D4"], "#fef9c3"),
        (0.79, "generator_outputs", ["optional D7"], "#fee2e2"),
    ]
    for x, title, lines, color in input_boxes:
        add_box(ax, x, input_y, 0.18, input_h, title, lines, color, fontsize=4.9, title_size=6.3)

    add_label(ax, 0.02, 0.55, "2. diagnostics", "#6d28d9", "bold", size=6.8)
    add_box(
        ax,
        0.16,
        0.48,
        0.15,
        0.13,
        "validation gate",
        ["join coverage", "depth + caveats"],
        "#f1f5f9",
        fontsize=4.8,
        title_size=6.1,
    )

    metric_boxes = [
        (0.34, "D1", ["util."], "#ede9fe"),
        (0.46, "D2", ["collision"], "#ede9fe"),
        (0.58, "D3", ["collab"], "#ede9fe"),
        (0.70, "D4", ["tail"], "#ede9fe"),
        (0.82, "D5a", ["cost"], "#ede9fe"),
    ]
    for x, title, lines, color in metric_boxes:
        add_box(ax, x, 0.49, 0.095, 0.115, title, lines, color, fontsize=4.65, title_size=6.2)

    add_box(ax, 0.34, 0.375, 0.25, 0.07, "optional D6", ["refresh churn"], "#eef2ff", fontsize=4.6, title_size=5.8)
    add_box(ax, 0.63, 0.375, 0.285, 0.07, "future D7", [], "#fff1f2", fontsize=4.6, title_size=5.8)

    add_label(ax, 0.02, 0.205, "3. evidence role", "#475569", "bold", size=6.8)
    evidence = [
        (0.16, "main exports", ["GRID + ReSID"], "#e0f2fe"),
        (0.37, "controls", ["sanity SIDs"], "#f8fafc"),
        (0.58, "resource tables", ["stability + D6"], "#f8fafc"),
        (0.79, "backlog", ["paper-only rows"], "#f8fafc"),
    ]
    for x, title, lines, color in evidence:
        add_box(ax, x, 0.11, 0.18, 0.13, title, lines, color, fontsize=4.8, title_size=5.9)

    add_arrow(ax, (0.25, 0.75), (0.235, 0.61))
    add_arrow(ax, (0.60, 0.75), (0.58, 0.61))
    add_arrow(ax, (0.88, 0.75), (0.77, 0.445), color="#dc2626")
    add_arrow(ax, (0.60, 0.375), (0.60, 0.24))

    add_label(ax, 0.16, 0.675, "v0 computes D1-D5a from mappings + metadata/interactions", "#6d28d9", "bold", size=5.9)
    add_label(ax, 0.63, 0.335, "requires generator traces; not claimed in v0", "#be123c", "bold", size=5.45)
    add_label(ax, 0.02, 0.045, "Claim boundary: mapping/diagnostic evidence now; downstream generator quality later.", "#0f172a", "bold", size=6.2)

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
