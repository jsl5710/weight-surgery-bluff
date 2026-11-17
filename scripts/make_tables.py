"""Build paper tables from results.csv. Missing cells stay as XX.

Usage: python scripts/make_tables.py --results results/results.csv --out results/tables
"""
from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from metrics import gap

METHODS = ["B1", "B2", "B3", "B4", "B5", "B6", "S-L1", "S-L3"]
SETTINGS = ["multilingual", "cross_lingual"]


def table_gap(df: pd.DataFrame) -> str:
    """Table 1: big-head F1, long-tail F1 and gap by method and setting."""
    rows = []
    for method in METHODS:
        cells = [method]
        for setting in SETTINGS:
            sub = df[(df.method == method) & (df.setting == setting) & (df.session_status == "ok")]
            if sub.empty:
                cells += ["XX", "XX", "XX"]
                continue
            per_lang = sub.groupby("language").agg(f1=("test_f1", "mean"), tier=("tier", "first"))
            f1 = per_lang.f1.to_dict()
            tiers = per_lang.tier.to_dict()
            head = pd.Series({l: v for l, v in f1.items() if tiers[l] == "big_head"}).mean()
            tail = pd.Series({l: v for l, v in f1.items() if tiers[l] == "long_tail"}).mean()
            cells += [f"{head:.1f}", f"{tail:.1f}", f"{gap(f1, tiers):.1f}"]
        rows.append(" & ".join(cells) + r" \\")
    header = r"Method & \multicolumn{3}{c}{Multilingual} & \multicolumn{3}{c}{Cross-lingual} \\"
    return "\n".join([r"\begin{tabular}{lrrrrrr}", r"\toprule", header, r"\midrule", *rows, r"\bottomrule", r"\end{tabular}"])


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--results", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    df = pd.read_csv(args.results)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    (out / "tab_gap.tex").write_text(table_gap(df))
    print(f"wrote {out / 'tab_gap.tex'}")


if __name__ == "__main__":
    main()
