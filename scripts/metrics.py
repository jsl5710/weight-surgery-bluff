"""Metric functions used by every table and figure in the papers.

Inputs are dictionaries or Series keyed by language. The language is the
sampling unit for all intervals (see the experiment plan).
"""
from __future__ import annotations

from typing import Dict, Iterable, Tuple

import numpy as np


def gap(f1_by_lang: Dict[str, float], tiers: Dict[str, str]) -> float:
    """Mean big-head F1 minus mean long-tail F1 (the disparity gap G)."""
    head = [f1_by_lang[l] for l in f1_by_lang if tiers[l] == "big_head"]
    tail = [f1_by_lang[l] for l in f1_by_lang if tiers[l] == "long_tail"]
    if not head or not tail:
        raise ValueError("need at least one big-head and one long-tail language")
    return float(np.mean(head) - np.mean(tail))


def worst_language_f1(f1_by_lang: Dict[str, float]) -> float:
    return float(min(f1_by_lang.values()))


def gini(values: Iterable[float]) -> float:
    """Gini coefficient of non-negative values (0 = equal)."""
    x = np.sort(np.asarray(list(values), dtype=float))
    if x.size == 0 or x.sum() == 0:
        return 0.0
    n = x.size
    index = np.arange(1, n + 1)
    return float((2 * np.sum(index * x) / (n * x.sum())) - (n + 1) / n)


def share_within(f1_by_lang: Dict[str, float], tiers: Dict[str, str], points: float = 5.0) -> float:
    """Share of long-tail languages within `points` of the big-head mean."""
    head_mean = np.mean([f1_by_lang[l] for l in f1_by_lang if tiers[l] == "big_head"])
    tail = [f1_by_lang[l] for l in f1_by_lang if tiers[l] == "long_tail"]
    return float(np.mean([(head_mean - v) <= points for v in tail]))


def obstacle_score(probe_f1: float, head_f1: float) -> float:
    return float(probe_f1 - head_f1)


def retention_ratio(shifted_gain: float, bluff_gain: float, min_gain: float = 1.0) -> float | None:
    """Gain on a shifted set divided by gain on the BLUFF test split.

    Returns None when the in-distribution gain is below `min_gain` points,
    where the ratio is unstable. Report absolute gain only in that case.
    """
    if bluff_gain < min_gain:
        return None
    return float(shifted_gain / bluff_gain)


def bootstrap_ci(
    values_by_lang: Dict[str, float],
    stat=np.mean,
    n_boot: int = 10_000,
    alpha: float = 0.05,
    seed: int = 0,
) -> Tuple[float, float, float]:
    """Bootstrap over languages. Returns (estimate, low, high)."""
    rng = np.random.default_rng(seed)
    x = np.asarray(list(values_by_lang.values()), dtype=float)
    est = float(stat(x))
    draws = np.empty(n_boot)
    for i in range(n_boot):
        draws[i] = stat(rng.choice(x, size=x.size, replace=True))
    low, high = np.quantile(draws, [alpha / 2, 1 - alpha / 2])
    return est, float(low), float(high)


def holm(pvalues: Dict[str, float]) -> Dict[str, float]:
    """Holm-adjusted p-values (step-down), keyed like the input."""
    items = sorted(pvalues.items(), key=lambda kv: kv[1])
    m = len(items)
    adjusted: Dict[str, float] = {}
    running = 0.0
    for rank, (name, p) in enumerate(items):
        running = max(running, min(1.0, (m - rank) * p))
        adjusted[name] = running
    return adjusted
