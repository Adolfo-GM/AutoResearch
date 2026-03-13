import json
import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

plt.switch_backend('agg')

JSON_PATH = os.path.join("logger_research", "research_data.json")
OUTPUT_PATH = os.path.join("logger_research", "benchmark_chart.png")

def main():
    if not os.path.exists(JSON_PATH):
        sys.exit(1)
    
    with open(JSON_PATH, "r") as f:
        try:
            data = json.load(f)
        except:
            sys.exit(1)
    
    if not data:
        sys.exit(0)

    for i, entry in enumerate(data):
        if "experiment_index" not in entry:
            entry["experiment_index"] = i

    df = pd.DataFrame(data)
    df["loss"] = pd.to_numeric(df["loss"], errors="coerce")
    df = df.sort_values("experiment_index")

    df['status'] = 'FAILED'
    current_min = float('inf')
    for i in df.index:
        if df.loc[i, 'loss'] < current_min:
            df.at[i, 'status'] = 'PASSED'
            current_min = df.loc[i, 'loss']

    print(f"\n{'Exp #':<7} {'Status':<10} {'Name':<20} {'Loss':<12} {'Branch'}")
    print("-" * 85)
    for _, row in df.iterrows():
        print(f"#{row['experiment_index']:<6} {row['status']:<10} {row['research_name']:<20} {row['loss']:<12.6f} {row['filename_in_saver']}")

    passed_df = df[df["status"] == "PASSED"].copy()
    
    if not passed_df.empty:
        fig, ax = plt.subplots(figsize=(12, 6))

        ax.plot(passed_df["experiment_index"], passed_df["loss"], 
                color="#27ae60", linewidth=2, marker='o', 
                markersize=8, markerfacecolor="#2ecc71", markeredgecolor="black",
                label="Best Progress")

        ax.step(passed_df["experiment_index"], passed_df["loss"], where="post", 
                color="#27ae60", alpha=0.3, linestyle='--')


        ax.set_xlabel("Experiment #", fontsize=10)
        ax.set_ylabel("Loss", fontsize=10)
        ax.set_title(f"AutoResearch: {len(passed_df)} Improvements Found", fontsize=12, loc='left')
        ax.grid(True, alpha=0.15)
        
        max_idx = df["experiment_index"].max()
        ax.set_xlim(left=0, right=max(1, max_idx * 1.05))

        y_min, y_max = passed_df["loss"].min(), passed_df["loss"].max()
        if len(passed_df) > 1:
            margin = (y_max - y_min) * 0.15
            ax.set_ylim(y_min - margin, y_max + margin)
        else:
            ax.set_ylim(y_min * 0.9, y_min * 1.1)

        plt.tight_layout()
        plt.savefig(OUTPUT_PATH, dpi=150)

if __name__ == "__main__":
    main()
