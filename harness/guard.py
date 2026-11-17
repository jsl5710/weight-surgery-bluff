"""Regression guard for Paper 1 surgery sessions.

An edit is rolled back when mean big-head validation F1 falls by more than
`max_drop` points relative to the unedited model.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class GuardDecision:
    accept: bool
    drop: float
    reason: str


def check_big_head(baseline_f1: float, edited_f1: float, max_drop: float = 1.0) -> GuardDecision:
    drop = baseline_f1 - edited_f1
    if drop > max_drop:
        return GuardDecision(False, drop, f"big-head F1 fell {drop:.2f} points (limit {max_drop:.2f})")
    return GuardDecision(True, drop, "within limit")


def subspace_overlap(u_orig, u_edit) -> float:
    """Overlap of two orthonormal bases (columns), in [0, 1].

    Mean squared cosine of the principal angles. Used for the spectral check on
    the top-r singular directions of an edited matrix. The flag threshold (tau)
    is set in the pre-registration.
    """
    import numpy as np

    s = np.linalg.svd(u_orig.T @ u_edit, compute_uv=False)
    return float(np.mean(s**2))
