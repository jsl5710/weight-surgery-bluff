# Governance and handling

This repository holds the open parts of the project. Some Paper 2 material is gated and must stay out of it.

**Open (this repository)**
- Paper 1 code, configs, schemas and analysis scripts.
- Paper 2 arm A1 (BLUFF detector flipping) and arm C (weight-only auditor) code and aggregate results, once the PI approves release.
- Paper 3 pilot protocols and aggregate results.

**Gated (restricted store, PI-held, never committed here)**
- Paper 2 arms A2 (safety detector) and B (aggregate refusal change): harness, prompts, traces, per-prompt outputs and edited checkpoints.
- Any raw harmful text.

**Before any gated run:** governance gates in the Paper 2 experiment plan are signed off and dated, the restricted environment is set up with a named access list, and stop conditions are understood by every runner.

**Reporting:** gated arms report aggregate numbers only (rates, counts, AUROC), never per-prompt outputs.

**Disclosure:** the disclosure plan is drafted before submission of Paper 2 and reviewed by the PI.
