#!/usr/bin/env python3
"""
Han Lab plot style smoke test.
Generates a two-panel StreamingLLM-style comparison figure.
Run: python3 .claude/skills/han-lab-plot-style/smoke.py [output_dir]
Output: han_lab_smoke.png (and .pdf) in output_dir (default: /tmp)
"""
import sys
import os
from collections import OrderedDict

import matplotlib as mpl
mpl.use("Agg")   # headless — no display needed
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# ── Han Lab global style ──────────────────────────────────────────────────
mpl.rcParams.update({
    "text.usetex":           False,
    "font.family":           "serif",
    "font.serif":            ["Times New Roman", "DejaVu Serif", "Times"],
    "mathtext.fontset":      "stix",
    "font.size":             11,
    "font.weight":           "bold",
    "axes.titlesize":        12,
    "axes.titleweight":      "bold",
    "axes.labelsize":        11,
    "axes.labelweight":      "bold",
    "xtick.labelsize":       10,
    "ytick.labelsize":       10,
    "legend.fontsize":       12,
    "lines.linewidth":       1.8,
    "lines.markersize":      5,
    "patch.linewidth":       0.8,
    "axes.spines.top":       True,
    "axes.spines.right":     True,
    "axes.spines.left":      True,
    "axes.spines.bottom":    True,
    "axes.linewidth":        0.8,
    "axes.grid":             True,
    "axes.grid.axis":        "y",
    "grid.linestyle":        "-",
    "grid.linewidth":        0.6,
    "grid.alpha":            0.4,
    "grid.color":            "#BBBBBB",
    "xtick.direction":       "in",
    "ytick.direction":       "in",
    "xtick.major.size":      4.0,
    "ytick.major.size":      4.0,
    "xtick.minor.visible":   False,
    "ytick.minor.visible":   False,
    "legend.frameon":        False,
    "legend.borderpad":      0.3,
    "legend.handlelength":   1.2,
    "legend.handleheight":   1.2,
    "figure.dpi":            150,
    "savefig.dpi":           300,
    "savefig.bbox":          "tight",
    "savefig.pad_inches":    0.05,
    "figure.facecolor":      "white",
    "axes.facecolor":        "white",
    "pdf.fonttype":          42,
    "ps.fonttype":           42,
})

HAN_COLORS = {
    "ours":       "#8B1A1A",
    "ours_mid":   "#A52A2A",
    "baseline":   "#D3D3D3",
    "baseline_2": "#BEBEBE",
    "grid":       "#BBBBBB",
}
PALETTE_2 = ["#D3D3D3", "#8B1A1A"]
PALETTE_3 = ["#D3D3D3", "#BEBEBE", "#8B1A1A"]
PALETTE_4 = ["#D3D3D3", "#BEBEBE", "#A0A0A0", "#8B1A1A"]


def annotate_bars(ax, bars, y_max, fontsize=9):
    for bar in bars:
        h = bar.get_height()
        if h == 0:
            continue
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            h + y_max * 0.01,
            f"{int(round(h))}",
            ha="center", va="bottom",
            fontsize=fontsize, fontweight="bold", color="black",
        )


def han_grouped_bar(ax, data, x_labels, ours_key=None, ylabel="", bar_width=0.35):
    n_methods = len(data)
    x = np.arange(len(x_labels))
    palette = PALETTE_2 if n_methods <= 2 else PALETTE_4
    y_max = max(max(v) for v in data.values()) * 1.20

    for i, (name, vals) in enumerate(data.items()):
        color = HAN_COLORS["ours"] if name == ours_key else palette[i]
        offset = (i - (n_methods - 1) / 2) * bar_width
        bars = ax.bar(
            x + offset, vals, bar_width,
            color=color, edgecolor=color, linewidth=0.8, zorder=3,
        )
        annotate_bars(ax, bars, y_max)

    ax.set_xticks(x)
    ax.set_xticklabels(x_labels, fontweight="bold")
    ax.set_ylabel(ylabel, fontweight="bold")
    ax.set_ylim(0, y_max)
    ax.set_axisbelow(True)
    for lbl in ax.get_xticklabels() + ax.get_yticklabels():
        lbl.set_fontweight("bold")


# ── Sample data (StreamingLLM-style) ─────────────────────────────────────
METHODS = ["Dense Attn", "Window Attn", "StreamingLLM (Ours)"]
OURS_KEY = "StreamingLLM (Ours)"

panels = [
    {
        "title": "Memory Usage",
        "ylabel": "Memory (GB)",
        "x_labels": ["1K", "2K", "4K", "8K"],
        "data": OrderedDict([
            ("Dense Attn",            [14, 28, 56, 112]),
            ("Window Attn",           [14, 14, 14, 14]),
            ("StreamingLLM (Ours)",   [10, 10, 10, 10]),
        ]),
        "yticks": [0, 28, 56, 84, 112],
    },
    {
        "title": "Decoding Latency",
        "ylabel": r"Latency (ms)",
        "x_labels": ["1K", "2K", "4K", "8K"],
        "data": OrderedDict([
            ("Dense Attn",            [42, 84, 168, 336]),
            ("Window Attn",           [42, 42, 42, 42]),
            ("StreamingLLM (Ours)",   [32, 32, 32, 32]),
        ]),
        "yticks": [0, 84, 168, 252, 336],
    },
]

fig, axes = plt.subplots(1, 2, figsize=(7.0, 3.0))

for ax, panel in zip(axes, panels):
    han_grouped_bar(ax, panel["data"], panel["x_labels"],
                    ours_key=OURS_KEY, ylabel=panel["ylabel"])
    ax.set_title(panel["title"], fontweight="bold", fontsize=12, pad=6)
    ax.set_yticks(panel["yticks"])

# Shared legend above all panels
legend_handles = [
    mpatches.Patch(facecolor="#D3D3D3", edgecolor="black", linewidth=0.8, label="Dense Attn"),
    mpatches.Patch(facecolor="#BEBEBE", edgecolor="black", linewidth=0.8, label="Window Attn"),
    mpatches.Patch(facecolor="#8B1A1A", edgecolor="black", linewidth=0.8, label="StreamingLLM (Ours)"),
]
fig.legend(
    handles=legend_handles,
    loc="upper center",
    bbox_to_anchor=(0.5, 1.00),
    ncol=3,
    frameon=False,
    prop={"weight": "bold", "size": 11},
    handlelength=1.2,
    handleheight=1.2,
    columnspacing=1.2,
)
# leave room for the external legend above the subplots
fig.tight_layout(rect=[0, 0, 1, 0.88])

out_dir = sys.argv[1] if len(sys.argv) > 1 else "/tmp"
png_path = os.path.join(out_dir, "han_lab_smoke.png")
pdf_path = os.path.join(out_dir, "han_lab_smoke.pdf")

fig.savefig(png_path, dpi=300, bbox_inches="tight", pad_inches=0.05)
fig.savefig(pdf_path, dpi=300, bbox_inches="tight", pad_inches=0.05)
plt.close(fig)

print(f"OK  {png_path}")
print(f"OK  {pdf_path}")
