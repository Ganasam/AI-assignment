import pandas as pd
import matplotlib.pyplot as plt
import sys

def main():
    csv_file = sys.argv[1] if len(sys.argv)>1 else "csp_metrics.csv"
    df = pd.read_csv(csv_file)
    if 'time_ms' in df.columns:
        df['time_ms'] = df['time_ms'].astype(float)
    else:
        raise RuntimeError('CSV missing time_ms column')
    plt.figure(figsize=(6,4))
    plt.bar(df['mode'], df['time_ms'], color=['#4C72B0','#DD8452'])
    plt.title("CSP runtime by Method")
    plt.ylabel("Time (ms)")
    out = "csp_time.png"
    plt.savefig(out, bbox_inches='tight')
    print(f"Saved plot: {out}")
    plt.show()

if __name__ == '__main__':
    main()
