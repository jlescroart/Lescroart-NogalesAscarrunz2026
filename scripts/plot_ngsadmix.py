#!/usr/bin/env python3

#Script created by Jonas Lescroart with Copilot on 16MAY2026.

import argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.patches import Patch


# ----------------------------
# Global styling (publication + SVG editable text)
# ----------------------------
mpl.rcParams["svg.fonttype"] = "none"   # editable text in Inkscape
mpl.rcParams["font.family"] = "sans-serif"
mpl.rcParams["font.size"] = 10


# ----------------------------
# Read qopt file
# ----------------------------
def read_qopt(qopt_file):
    return pd.read_csv(qopt_file, sep=r"\s+", header=None)


# ----------------------------
# Read map file
# Expected format:
# Ind0   SampleID
# ----------------------------
def read_map(map_file):
    m = pd.read_csv(map_file, sep=r"\s+", engine="python", header=None)

    if m.shape[1] < 2:
        raise ValueError("Map file must have at least 2 columns: IndX, SampleID")

    m.columns = ["ind", "sample"]

    # Ensure order consistency
    m["index"] = m["ind"].str.replace("Ind", "").astype(int)
    m = m.sort_values("index")

    return m


# ----------------------------
# Generate distinct colors
# ----------------------------
def get_colors(K):
    cmap = plt.get_cmap("tab20")

    if K <= 20:
        return [cmap(i) for i in range(K)]
    else:
        # extend beyond 20 if needed
        return [cmap(i % 20) for i in range(K)]


# ----------------------------
# Plot function
# ----------------------------
def plot_admixture(qopt_df, map_df, out_svg):

    n, K = qopt_df.shape

    if len(map_df) != n:
        raise ValueError("Map and qopt must have same number of individuals")

    colors = get_colors(K)

    fig_width = max(10, n * 0.25)
    fig, ax = plt.subplots(figsize=(fig_width, 4.5))

    x = np.arange(n)
    bottom = np.zeros(n)

    # ----------------------------
    # Stacked bars
    # ----------------------------
    for k in range(K):
        ax.bar(
            x,
            qopt_df[k],
            bottom=bottom,
            width=1.0,
            color=colors[k],
            edgecolor="none"
        )
        bottom += qopt_df[k]

    # ----------------------------
    # Sample labels
    # ----------------------------
    ax.set_xticks(x)
    ax.set_xticklabels(map_df["sample"], rotation=90, fontsize=7)

    # ----------------------------
    # Axis labels
    # ----------------------------
    ax.set_xlabel("Individuals")
    ax.set_ylabel("Ancestry proportion")

    ax.set_ylim(0, 1)
    ax.set_xlim(-0.5, n - 0.5)

    # Clean spines
    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)

    # ----------------------------
    # Dominant ancestry separators
    # ----------------------------
    dominant = qopt_df.idxmax(axis=1)

    for i in range(1, n):
        if dominant[i] != dominant[i - 1]:
            ax.axvline(i - 0.5, color="black", linewidth=0.7)

    # ----------------------------
    # Legend (top, horizontal)
    # ----------------------------
    legend_elements = [
        Patch(facecolor=colors[k], label=f"Cluster {k+1}")
        for k in range(K)
    ]

    ax.legend(
        handles=legend_elements,
        loc="lower center",
        bbox_to_anchor=(0.5, 1.02),
        ncol=K,
        frameon=False,
        fontsize=9,
        handlelength=1.5,
        columnspacing=1.2
    )

    # ----------------------------
    # Layout
    # ----------------------------
    plt.tight_layout()

    # ----------------------------
    # Save SVG
    # ----------------------------
    plt.savefig(
        out_svg,
        format="svg",
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()


# ----------------------------
# CLI
# ----------------------------
def main():
    parser = argparse.ArgumentParser(
        description="Plot NGSadmix qopt (publication-grade SVG)"
    )
    parser.add_argument("-q", "--qopt", required=True)
    parser.add_argument("-m", "--map", required=True)
    parser.add_argument("-o", "--out", required=True)

    args = parser.parse_args()

    qopt_df = read_qopt(args.qopt)
    map_df = read_map(args.map)

    plot_admixture(qopt_df, map_df, args.out)


if __name__ == "__main__":
    main()
