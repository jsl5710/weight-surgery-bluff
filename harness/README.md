# Harness

Implemented and tested here: the regression guard (`guard.py`) and the hash-chained audit log (`audit_log.py`).

To add after the dry run: the tool server that exposes `list_modules`, `read_tensor`, `write_tensor`, `forward`, `rollback` and `budget_status` to the surgeon. The harness, not the surgeon, owns the data, the forward-pass budget B, the weight budget epsilon and the guard. The test split is never reachable from the tool server.

Paper 2's gated harness is not part of this repository (see `docs/GOVERNANCE.md`).
