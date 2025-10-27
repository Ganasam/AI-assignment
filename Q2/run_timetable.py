import time
import csv
import os
import matplotlib.pyplot as plt
from csp_timetable import generate_instance, solve_bt_heuristics, solve_bt_forward_checking


def run_and_measure(instance, solver_fn, name, find_all=False, max_solutions=1):
    t0 = time.perf_counter()
    sols, stats = solver_fn(instance, find_all=find_all, max_solutions=max_solutions)
    t1 = time.perf_counter()
    elapsed = stats.time() if hasattr(stats, 'time') else (t1 - t0)
    return {
        'method': name,
        'time_s': elapsed,
        'backtracks': stats.backtracks,
        'solutions': stats.solutions,
    }

def save_csv(rows, path='timetable_metrics.csv'):
    keys = ['method', 'time_s', 'backtracks', 'solutions']
    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        for r in rows:
            writer.writerow(r)
    print(f"Saved metrics CSV: {path}")


def plot_comparison(rows, out='timetable_comparison.png'):
    methods = [r['method'] for r in rows]
    times = [r['time_s'] for r in rows]
    backtracks = [r['backtracks'] for r in rows]
    solutions = [r['solutions'] for r in rows]

    fig, axes = plt.subplots(1, 3, figsize=(12, 4), constrained_layout=True)

    x = range(len(methods))
    axes[0].bar(x, times, color='#4C72B0')
    axes[0].set_title('Time (s)')
    axes[0].set_xticks(x)
    axes[0].set_xticklabels(methods, rotation=25)

    axes[1].bar(x, backtracks, color='#DD8452')
    axes[1].set_title('Backtracks')
    axes[1].set_xticks(x)
    axes[1].set_xticklabels(methods, rotation=25)

    axes[2].bar(x, solutions, color='#55A868')
    axes[2].set_title('Solutions Found')
    axes[2].set_xticks(x)
    axes[2].set_xticklabels(methods, rotation=25)

    plt.suptitle('Timetable CSP Solver Comparison')
    plt.savefig(out, dpi=150)
    plt.close(fig)
    print(f"Saved plot: {out}")


def main():
    inst = generate_instance(num_classes=8, num_timeslots=4, num_rooms=4, num_teachers=5, seed=42)

    rows = []
    rows.append(run_and_measure(inst, solve_bt_heuristics, 'Backtracking+Heuristics'))
    rows.append(run_and_measure(inst, solve_bt_forward_checking, 'Backtracking+ForwardChecking'))

    save_csv(rows)
    plot_comparison(rows)


if __name__ == '__main__':
    main()
