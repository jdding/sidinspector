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

INK = "#172033"
MUTED = "#5B667A"
LINE = "#CBD3DF"
BLUE = "#DCEBFF"
BLUE_EDGE = "#3675C7"
TEAL = "#DFF6F2"
TEAL_EDGE = "#158A7B"
AMBER = "#FFF2CC"
AMBER_EDGE = "#B98010"
ROSE = "#FDE6E8"
ROSE_EDGE = "#B54654"
GRAY = "#F4F6F8"


def box(ax, xy, wh, title, body=None, fill=GRAY, edge=LINE, title_size=7.2, body_size=5.9):
    x, y = xy
    w, h = wh
    patch = FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle="round,pad=0.012,rounding_size=0.018",
        linewidth=0.9,
        edgecolor=edge,
        facecolor=fill,
    )
    ax.add_patch(patch)
    ax.text(x + w / 2, y + h * 0.63, title, ha="center", va="center", fontsize=title_size, fontweight="bold", color=INK)
    if body:
        ax.text(x + w / 2, y + h * 0.31, body, ha="center", va="center", fontsize=body_size, color=MUTED)


def arrow(ax, start, end, color=MUTED):
    ax.add_patch(
        FancyArrowPatch(
            start,
            end,
            arrowstyle="-|>",
            mutation_scale=9,
            linewidth=0.9,
            color=color,
            shrinkA=3,
            shrinkB=3,
        )
    )


def section_label(ax, x, y, label):
    ax.text(x, y, label, ha="left", va="center", fontsize=6.2, color=MUTED, fontweight="bold")


def main():
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
        }
    )

    fig, ax = plt.subplots(figsize=(3.35, 3.65))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    ax.text(0.02, 0.975, "From SID exports to auditable evidence", ha="left", va="top", fontsize=8.2, fontweight="bold", color=INK)
    ax.text(0.02, 0.936, "Mapping-first checks before generator training", ha="left", va="top", fontsize=6.0, color=MUTED)
    ax.plot([0.02, 0.98], [0.905, 0.905], color=LINE, linewidth=0.8)

    section_label(ax, 0.02, 0.858, "1  inputs")
    inputs = [
        (0.08, "SID map", "required", TEAL, TEAL_EDGE),
        (0.30, "metadata", "semantic", BLUE, BLUE_EDGE),
        (0.52, "interactions", "D3 / D4", AMBER, AMBER_EDGE),
        (0.74, "generator", "D7 hook", ROSE, ROSE_EDGE),
    ]
    for x, title, body, fill, edge in inputs:
        box(ax, (x, 0.775), (0.18, 0.085), title, body, fill, edge, title_size=6.2, body_size=5.1)

    arrow(ax, (0.50, 0.765), (0.50, 0.705))

    section_label(ax, 0.02, 0.680, "2  audit core")
    box(ax, (0.10, 0.565), (0.31, 0.125), "validator", "coverage, joins,\ndepth, caveats", GRAY, "#9AA6B7", title_size=7.0, body_size=5.6)
    box(ax, (0.50, 0.565), (0.40, 0.125), "D1-D5a diagnostics", "utilization, collision,\ncollab, tail, cost", "#EEE9FF", "#7662D9", title_size=7.0, body_size=5.6)
    arrow(ax, (0.41, 0.627), (0.50, 0.627))

    box(ax, (0.12, 0.450), (0.25, 0.065), "D6 optional", "refresh churn", "#EDF2FF", "#6A7FD3", title_size=6.1, body_size=5.1)
    box(ax, (0.58, 0.450), (0.28, 0.065), "D7 boundary", "needs traces", ROSE, ROSE_EDGE, title_size=6.1, body_size=5.1)
    arrow(ax, (0.50, 0.565), (0.37, 0.515), color="#6A7FD3")
    arrow(ax, (0.74, 0.565), (0.72, 0.515), color=ROSE_EDGE)

    arrow(ax, (0.50, 0.440), (0.50, 0.370))

    section_label(ax, 0.02, 0.342, "3  evidence roles")
    roles = [
        (0.07, "main", "GRID + ReSID", "#E5F3FF", BLUE_EDGE),
        (0.31, "stressors", "not methods", "#F8FAFC", "#8A96A8"),
        (0.55, "repo tables", "stability / D6", "#F8FAFC", "#8A96A8"),
        (0.79, "backlog", "paper-only", "#F8FAFC", "#8A96A8"),
    ]
    for x, title, body, fill, edge in roles:
        box(ax, (x, 0.245), (0.17, 0.092), title, body, fill, edge, title_size=6.1, body_size=4.9)

    ax.plot([0.05, 0.95], [0.175, 0.175], color=LINE, linewidth=0.7)
    ax.text(0.05, 0.126, "Claim boundary", ha="left", va="center", fontsize=6.2, fontweight="bold", color=INK)
    ax.text(0.33, 0.126, "artifact diagnostics now; generator quality later", ha="left", va="center", fontsize=5.7, color=MUTED)

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
