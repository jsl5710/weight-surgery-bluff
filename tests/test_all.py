import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT))

from metrics import bootstrap_ci, gap, gini, holm, retention_ratio, share_within, worst_language_f1  # noqa: E402
from harness.guard import check_big_head, subspace_overlap  # noqa: E402
from harness.audit_log import AuditLog, verify  # noqa: E402

F1 = {"en": 90.0, "fr": 88.0, "xx": 70.0, "yy": 66.0}
TIER = {"en": "big_head", "fr": "big_head", "xx": "long_tail", "yy": "long_tail"}


def test_gap():
    assert gap(F1, TIER) == 21.0


def test_worst_and_share():
    assert worst_language_f1(F1) == 66.0
    assert share_within(F1, TIER, points=25.0) == 1.0
    assert share_within(F1, TIER, points=5.0) == 0.0


def test_gini_equal_and_unequal():
    assert abs(gini([5, 5, 5, 5])) < 1e-9
    assert gini([0, 0, 0, 10]) > 0.7


def test_retention():
    assert retention_ratio(3.0, 6.0) == 0.5
    assert retention_ratio(3.0, 0.5) is None


def test_bootstrap_contains_mean():
    vals = {str(i): float(i) for i in range(30)}
    est, lo, hi = bootstrap_ci(vals, n_boot=500)
    assert lo <= est <= hi


def test_holm_monotone():
    adj = holm({"H1": 0.01, "H2": 0.02, "H3": 0.5})
    assert adj["H1"] <= adj["H2"] <= adj["H3"]
    assert adj["H1"] == 0.03


def test_guard():
    assert check_big_head(90.0, 89.5).accept
    assert not check_big_head(90.0, 88.9).accept


def test_subspace_overlap_identity():
    q, _ = np.linalg.qr(np.random.default_rng(0).normal(size=(8, 3)))
    assert abs(subspace_overlap(q, q) - 1.0) < 1e-9


def test_audit_chain(tmp_path):
    p = tmp_path / "log.jsonl"
    log = AuditLog(p)
    log.append("forward", split="val")
    log.append("edit", tensor="head.weight")
    assert verify(p)
    lines = p.read_text().splitlines()
    rec = json.loads(lines[0])
    rec["event"] = "tampered"
    lines[0] = json.dumps(rec, sort_keys=True)
    p.write_text("\n".join(lines) + "\n")
    assert not verify(p)
