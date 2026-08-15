---
name: han-lab-plot-style
description: >
  Apply MIT Han Lab (Song Han 韓松) paper figure style when generating
  experiment plots. Trigger whenever the user asks to plot, visualize, or
  generate figures for research results, benchmarks, ablation studies,
  throughput/latency/accuracy comparisons, or any experiment data intended
  for inclusion in a research paper or presentation. Also trigger when the
  user says "Han Lab style", "plot like Song Han's paper", "論文風格畫圖",
  or "generate publication-quality figures". Use this skill even for casual
  requests like "make a bar chart of my results" or "plot this data" when
  the context suggests a research or paper setting.
---

# Han Lab Plot Style

Matplotlib style matching MIT Han Lab papers (AWQ, SmoothQuant, StreamingLLM,
QServe, etc.). Ground truth: StreamingLLM ICLR 2024 memory/latency figure.

Driver: `.claude/skills/han-lab-plot-style/smoke.py` — generates the
reference two-panel figure to verify the style is correct.

---

## Prerequisites

```
pip install matplotlib numpy   # or: pip3 install matplotlib numpy
```

Matplotlib 3.x, NumPy 2.x. No display needed — `mpl.use("Agg")` for headless.

---

## Run (smoke test)

```bash
python3 .claude/skills/han-lab-plot-style/smoke.py /tmp
# prints:
#   OK  /tmp/han_lab_smoke.png
#   OK  /tmp/han_lab_smoke.pdf
```

Open `/tmp/han_lab_smoke.png` to visually verify the style.
Expected: two grouped bar panels, shared legend above, bold serif, burgundy bars.

---

## Core Philosophy

Han Lab figures are **dense, bold, and print-safe**:
- **Serif bold font throughout** — all text uses bold serif (Times New Roman → DejaVu Serif fallback)
- **Complete box frame** — all four spines visible, closed rectangle
- **Solid horizontal grid lines** — light gray `#BBBBBB`, solid `-` (NOT dashed)
- **Two-color palette** — baseline `#D3D3D3`, proposed method `#8B1A1A` (deep burgundy)
- **Shared legend above all panels** — `fig.legend` outside plot area
- **Value annotations above every bar** — integer, bold, tight to bar top
- **Wide bars nearly touching** — `BAR_W=0.35` per bar for 2-method groups

---

## 1. Global rcParams (copy verbatim)

```python
import matplotlib as mpl
mpl.use("Agg")   # headless; omit if display is available
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

mpl.rcParams.update({
    "text.usetex":           False,        # use matplotlib engine, NOT LaTeX
    "font.family":           "serif",
    "font.serif":            ["Times New Roman", "DejaVu Serif", "Times"],
    "mathtext.fontset":      "stix",       # serif math symbols
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
    "axes.spines.top":       True,         # closed box frame
    "axes.spines.right":     True,
    "axes.spines.left":      True,
    "axes.spines.bottom":    True,
    "axes.linewidth":        0.8,
    "axes.grid":             True,
    "axes.grid.axis":        "y",
    "grid.linestyle":        "-",          # solid, NOT "--"
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
    "pdf.fonttype":          42,           # embed fonts as TrueType
    "ps.fonttype":           42,
})
```

---

## 2. Color Palette

```python
HAN_COLORS = {
    "ours":       "#8B1A1A",   # deep burgundy — proposed method
    "ours_mid":   "#A52A2A",   # slightly lighter alternative
    "baseline":   "#D3D3D3",   # light gray — all baselines
    "baseline_2": "#BEBEBE",   # slightly darker (2nd baseline)
    "grid":       "#BBBBBB",
}
PALETTE_2 = ["#D3D3D3", "#8B1A1A"]              # 1 baseline + ours
PALETTE_3 = ["#D3D3D3", "#BEBEBE", "#8B1A1A"]   # 2 baselines + ours
PALETTE_4 = ["#D3D3D3", "#BEBEBE", "#A0A0A0", "#8B1A1A"]
```

**Critical rules:**
- `edgecolor = facecolor` on every bar (same-color rule — `edgecolor="white"` detaches bars from x-axis)
- Exception: legend patch handles use `edgecolor="black"`
- Never use `★` (U+2605) in labels — use `(Ours)` suffix; Times New Roman lacks this glyph

---

## 3. Bar Width

```python
BAR_W = 0.35   # 2 methods; use 0.25 for 3, 0.20 for 4
```

No hatch on grouped comparison bars — color differentiates alone.

---

## 4. Figure Sizes

```python
FIGSIZE_1COL  = (3.5, 3.0)   # single panel
FIGSIZE_2COL  = (7.0, 3.0)   # two panels (most common)
FIGSIZE_3COL  = (7.0, 2.8)   # three panels
FIGSIZE_SQ    = (3.2, 3.2)   # scatter / Pareto
```

---

## 5. Legend: Shared Above All Panels

**Multi-panel** — `fig.legend` + `tight_layout(rect=...)`. Do NOT use
`constrained_layout=True` here — it ignores external legends and causes overlap.

```python
legend_handles = [
    mpatches.Patch(facecolor="#D3D3D3", edgecolor="black", linewidth=0.8, label="Baseline"),
    mpatches.Patch(facecolor="#8B1A1A", edgecolor="black", linewidth=0.8, label="Ours"),
]

fig, axes = plt.subplots(1, 2, figsize=(7.0, 3.0))   # NOT constrained_layout=True

fig.legend(
    handles=legend_handles,
    loc="upper center",
    bbox_to_anchor=(0.5, 1.00),
    ncol=len(legend_handles),
    frameon=False,
    prop={"weight": "bold", "size": 12},
    handlelength=1.2,
    handleheight=1.2,
    columnspacing=1.5,
)
fig.tight_layout(rect=[0, 0, 1, 0.88])   # reserve top 12% for legend
```

**Single-panel exception** — use `ax.legend` instead:

```python
ax.legend(
    handles=legend_handles,
    loc="upper left",
    frameon=False,
    prop={"weight": "bold", "size": 9},
    handlelength=1.2,
    handleheight=1.2,
)
```

---

## 6. Grouped Bar Chart (primary pattern)

```python
from collections import OrderedDict

def han_grouped_bar(ax, data: dict, x_labels: list,
                    ours_key: str = None, ylabel: str = "",
                    bar_width: float = 0.35):
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
        for bar in bars:
            h = bar.get_height()
            if h == 0: continue
            ax.text(bar.get_x() + bar.get_width() / 2, h + y_max * 0.01,
                    f"{int(round(h))}", ha="center", va="bottom",
                    fontsize=9, fontweight="bold", color="black")

    ax.set_xticks(x)
    ax.set_xticklabels(x_labels, fontweight="bold")
    ax.set_ylabel(ylabel, fontweight="bold")
    ax.set_ylim(0, y_max)
    ax.set_axisbelow(True)
    for lbl in ax.get_xticklabels() + ax.get_yticklabels():
        lbl.set_fontweight("bold")
```

---

## 7. Line Plot

```python
def han_line_plot(ax, data: dict, x_vals, ours_key=None, xlabel="", ylabel=""):
    markers = ["o", "s", "^", "D", "v"]
    for i, (name, y) in enumerate(data.items()):
        is_ours = (name == ours_key)
        color = HAN_COLORS["ours"] if is_ours else HAN_COLORS["baseline"]
        ax.plot(x_vals, y, color=color,
                linewidth=2.2 if is_ours else 1.6,
                marker=markers[i % len(markers)], markersize=6,
                zorder=5 if is_ours else 3, label=name)
    ax.set_xlabel(xlabel, fontweight="bold")
    ax.set_ylabel(ylabel, fontweight="bold")
```

---

## 8. Stacked Breakdown Bar

```python
def han_stacked_bar(ax, data: dict, x_labels: list,
                    ylabel="Memory (GB)", bar_width=0.55):
    x = np.arange(len(x_labels))
    bottom = np.zeros(len(x_labels))
    colors = [HAN_COLORS["ours"], HAN_COLORS["baseline"], "#BEBEBE"]
    hatches = ["", "///", "..."]   # hatch allowed on upper segments only
    for i, (comp, vals) in enumerate(data.items()):
        vals = np.array(vals)
        color = colors[i % len(colors)]
        ax.bar(x, vals, width=bar_width, bottom=bottom,
               label=comp, color=color,
               hatch=hatches[i % len(hatches)],
               edgecolor=color, linewidth=0.8, zorder=3)
        bottom += vals
    ax.set_xticks(x)
    ax.set_xticklabels(x_labels, fontweight="bold")
    ax.set_ylabel(ylabel, fontweight="bold")
    ax.set_ylim(0, bottom.max() * 1.20)
    ax.set_axisbelow(True)

# Reference line above stacked bars — must be zorder=4 (bars are zorder=3)
ax.axhline(ref_value, color=COL_REF, linestyle="-", linewidth=1.2, zorder=4)
```

---

## 9. Log-Scale Grouped Bar

```python
ax.set_yscale("log")
ax.set_ylim(1, y_hi)   # y_lo >= 1

# Labels inside bars
def annotate_bars_inside(ax, bars, fontsize=7):
    for bar in bars:
        h = bar.get_height()
        if h <= 0: continue
        y_pos = h * 0.88 if h >= 2 else h * 1.15
        va    = "top"    if h >= 2 else "bottom"
        c     = "white"  if bar.get_facecolor()[:3] == (0.545, 0.102, 0.102) else "black"
        ax.text(bar.get_x() + bar.get_width() / 2, y_pos,
                f"{int(round(h))}", ha="center", va=va,
                fontsize=fontsize, fontweight="bold", color=c, zorder=6)

# Improvement arrow (geometric midpoint for log scale)
def annotate_improvement_arrow(ax, x_base, h_base, x_ours, h_ours,
                                ratio_text, arrow_color="#8B1A1A", fontsize=8):
    x_mid = (x_base + x_ours) / 2
    y_top, y_bot = h_base * 0.85, h_ours * 1.15
    ax.annotate("", xy=(x_mid, y_bot), xytext=(x_mid, y_top),
                arrowprops=dict(arrowstyle="->,head_width=0.25,head_length=0.15",
                                color=arrow_color, lw=1.5, shrinkA=0, shrinkB=0),
                zorder=7)
    ax.text(x_mid, (y_top * y_bot) ** 0.5, ratio_text,
            ha="center", va="center", fontsize=fontsize, fontweight="bold",
            color=arrow_color, zorder=8,
            bbox=dict(boxstyle="round,pad=0.15", facecolor="white",
                      edgecolor="none", alpha=0.85))
```

---

## 10. Axis Conventions

```python
ax.set_ylim(0, max_val * 1.20)
ax.set_yticks([0, 25, 50, 75, 100])   # clean round multiples, set manually
ax.set_ylabel(r"Latency ($\mu$s)", fontweight="bold")   # mathtext, NOT raw µ
for lbl in ax.get_xticklabels() + ax.get_yticklabels():
    lbl.set_fontweight("bold")
```

---

## 11. Save / Export

```python
fig.savefig("figure.pdf", dpi=300, bbox_inches="tight", pad_inches=0.05)
fig.savefig("figure.png", dpi=300, bbox_inches="tight", pad_inches=0.05)
plt.close(fig)
```

---

## 12. React / Recharts Variant (claude.ai artifact)

```jsx
const HAN_COLORS = { ours: "#8B1A1A", baseline: "#D3D3D3", grid: "#BBBBBB" };

// CartesianGrid: strokeDasharray="" (solid), stroke="#BBBBBB", vertical={false}
// XAxis/YAxis: tick={{ fontFamily:"serif", fontWeight:"bold", fontSize:11 }}
// Legend: layout="horizontal", verticalAlign="top", align="center",
//         wrapperStyle={{ fontWeight:"bold", fontSize:12 }}, iconType="square"
// Bar: isAnimationActive={false}
// LabelList: position="top", style={{ fontWeight:"bold", fontSize:9, fill:"black" }}
//            formatter={v => Math.round(v)}
```

---

## Gotchas

- **`constrained_layout=True` + `fig.legend` = overlap.** Use plain
  `plt.subplots(...)` + `fig.tight_layout(rect=[0, 0, 1, 0.88])` instead.
  The `rect` reserves the top 12% for the legend.
- **`★` (U+2605) raises `Glyph 9733 missing`.** Times New Roman lacks it.
  Use `"Method (Ours)"` suffix instead.
- **Raw Unicode `µ` in ylabel raises a warning and may not render bold.**
  Use `r"Latency ($\mu$s)"` with `mathtext.fontset="stix"`.
- **`edgecolor="white"` detaches bars from x-axis.** Always set
  `edgecolor = facecolor`.
- **Reference `axhline` hidden behind bars.** Set `zorder=4` (bars are `zorder=3`).
- **Legend patch contrast.** `#D3D3D3` and `#BEBEBE` look nearly identical
  in the legend. Use `edgecolor="black"` on all legend patches.
- **Legend floating too high, big blank gap above the panels.** Caused by
  pushing `bbox_to_anchor`'s y above `1.00` (e.g. `1.06`) *and* shrinking
  `tight_layout`'s `rect` top at the same time (e.g. `0.84`) — the two
  compound, and `savefig(..., bbox_inches="tight")` then crops around
  wherever the legend actually landed, leaving dead space between it and
  the axes/titles. Keep `bbox_to_anchor=(0.5, 1.00)` fixed; only adjust
  `rect`'s top value (e.g. `0.90` instead of `0.88`) if two-line titles
  need more headroom. Real fix confirmed 2026-08-11 (see
  experiments/pass_offload/analysis/plot_bm19_summary_bars.py's own git
  history): `1.06`/`0.84` → `1.00`/`0.90` closed the gap.

---

## Quick Checklist

- [ ] `font.family="serif"`, `font.weight="bold"`, `text.usetex=False`
- [ ] `mathtext.fontset="stix"` — special chars via `r"$\mu$"` not `µ`
- [ ] All four spines visible (closed box frame)
- [ ] Grid: solid `-`, `#BBBBBB`, y-axis only
- [ ] Colors: baseline `#D3D3D3`, ours `#8B1A1A` — no other hues
- [ ] No hatch on grouped bars; `edgecolor == facecolor`
- [ ] Value annotation above every bar, `fontweight="bold"`, integer
- [ ] Multi-panel: `fig.legend` + `tight_layout(rect=[0,0,1,0.88])`
- [ ] Single-panel: `ax.legend`
- [ ] Legend patches: `edgecolor="black"`
- [ ] No `★` — use `(Ours)` suffix
- [ ] `ax.set_axisbelow(True)` — grid behind bars
- [ ] Save: 300 DPI, PDF + PNG, `pdf.fonttype=42`
