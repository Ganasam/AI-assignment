import os
import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

def render_and_print_ascii(file_path, save_png=True):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = [ln.rstrip("\n") for ln in f.readlines()]
        if not lines:
            return
        header = lines[0] if lines[0].startswith("#") else ""
        grid_lines = lines[1:] if header else lines
        print(f"\n=== {os.path.basename(file_path)} ===")
        if header:
            print(header)
        for ln in grid_lines:
            print(ln)


        h = len(grid_lines)
        w = len(grid_lines[0]) if h > 0 else 0
        arr = np.zeros((h, w), dtype=int)
        mapping = {'.': 0, '#': 1, 'S': 2, 'G': 3, '*': 4}
        for r, ln in enumerate(grid_lines):
            for c, ch in enumerate(ln):
                arr[r, c] = mapping.get(ch, 0)

        if save_png and h > 0 and w > 0:
            cmap = mcolors.ListedColormap(['white', 'black', 'green', 'red', 'blue'])
            bounds = [-0.5, 0.5, 1.5, 2.5, 3.5, 4.5]
            norm = mcolors.BoundaryNorm(bounds, cmap.N)

            plt.figure(figsize=(7,7))
            plt.imshow(arr, cmap=cmap, norm=norm, origin='upper', interpolation='none')

            
            plt.grid(which='major', color='gray', linewidth=0.5)
            plt.xticks(np.arange(-0.5, w, 1))
            plt.yticks(np.arange(-0.5, h, 1))
            plt.tick_params(bottom=False, left=False, labelbottom=False, labelleft=False)
            plt.gca().set_aspect('equal', adjustable='box')

            plt.title(os.path.basename(file_path))
            outpng = os.path.splitext(file_path)[0] + ".png"
            plt.savefig(outpng, bbox_inches='tight', dpi=150)
            plt.close()
            print(f"Saved image: {outpng}")

    except Exception as e:
        print(f"Could not read/plot {file_path}: {e}")

csv_path = "a_star_metrics.csv"

if not os.path.exists(csv_path):
    print(f"CSV not found: {csv_path}. Run a_star.py first.")
else:
    df = pd.read_csv(csv_path)
    df["path_cost"] = pd.to_numeric(df.get("path_cost", pd.Series()), errors="coerce")
    df["time_ms"] = pd.to_numeric(df.get("time_ms", pd.Series()), errors="coerce")

    grouped = df.groupby("heuristic_name")[["path_cost","nodes_expanded","time_ms"]].mean()
    print("\nAverage Metrics:\n", grouped)

    if os.path.exists("last_grid.txt"):
        render_and_print_ascii("last_grid.txt")
    else:
        print("\n(last_grid.txt not found — enable saving grid in a_star.py)")

    for pfile in sorted(glob.glob("last_path_*.txt")):
        render_and_print_ascii(pfile)

    metrics = grouped.rename(columns={"path_cost": "path_length", "nodes_expanded": "nodes_expanded", "time_ms": "time_ms"})

    preferred_order = ["Manhattan", "Euclidean", "Chebyshev"]
    present = [h for h in preferred_order if h in metrics.index]
    
    other = [h for h in metrics.index if h not in present]
    plot_order = present + other
    metrics = metrics.reindex(plot_order)

    time_label = "Avg Time (ms)"
    time_vals = metrics["time_ms"].astype(float)
    if time_vals.max() < 1.0 and time_vals.max() > 0:
        time_vals = time_vals * 1000.0

    nodes_vals = metrics["nodes_expanded"].astype(float)
    path_vals = metrics["path_length"].astype(float)

    fig, axes = plt.subplots(1, 3, figsize=(14, 4), constrained_layout=True)

    x = np.arange(len(metrics.index))
    labels = list(metrics.index)

    axes[0].bar(x, time_vals, color="#2b83ba")
    axes[0].set_title(time_label)
    axes[0].set_xticks(x)
    axes[0].set_xticklabels(labels, rotation=25)
    axes[0].set_ylabel(time_label)

    axes[1].bar(x, nodes_vals, color="#fdae61")
    axes[1].set_title("Avg Nodes Expanded")
    axes[1].set_xticks(x)
    axes[1].set_xticklabels(labels, rotation=25)
    axes[1].set_ylabel("Nodes")

    axes[2].bar(x, path_vals, color="#abdda4")
    axes[2].set_title("Avg Path Length")
    axes[2].set_xticks(x)
    axes[2].set_xticklabels(labels, rotation=25)
    axes[2].set_ylabel("Path Length / Cost")

    outname = "metrics_comparison.png"
    plt.suptitle("Heuristic Comparison — A* Metrics", fontsize=14)
    plt.savefig(outname, dpi=150)
    print(f"Saved comparison plot: {outname}")
    plt.close(fig)