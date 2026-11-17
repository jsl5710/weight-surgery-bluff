# weight-surgery-bluff

Code, plans and paper sources for a project on **LLM-driven weight surgery** applied to the long-tail language gap on [BLUFF](https://huggingface.co/datasets/jsl5710/BLUFF). The project builds on [Sparks of Weight-Space Programming](https://rikiyat.github.io/blog/weight-space-programming/) (Takehi, Teoh, Zhang and Khattab, 2026), a blog post that is not peer reviewed.

Lead: Jason S. Lucas, Secure and Ethical AI Lab (SEAL), University of Colorado Boulder.

## Three papers

| Paper | Question | Folder |
| --- | --- | --- |
| 1 | Can an LLM that edits weights as text close the long-tail gap on BLUFF, and do the gains transfer to unseen data? | `papers/paper1_bluff_surgery` |
| 2 | What is the dual-use risk of the same capability, and can it be audited? | `papers/paper2_dual_use` |
| 3 | Position paper: does weight-space programming address long-tail effects across the pipeline? | `papers/paper3_position` |

Experiment plans (Claude Docs): see `docs/LINKS.md`.

## What is in this repository

- `papers/`: LaTeX sources (ACL style) and compiled PDFs. Numbers shown as XX are placeholders until the experiments run.
- `configs/`: pre-registration template and the experiment list (E0 to E11).
- `schema/`: column definitions for `results.csv`, `probes.csv`, `cost.csv`, `ood.csv`.
- `scripts/`: metric functions and the table and figure generators. Every number in a paper should come from these scripts.
- `harness/`: the Paper 1 regression guard and the hash-chained audit log (tested). The model-facing tool server is added after the dry run.
- `tests/`: unit tests for metrics, guard and audit log.
- `data/`: BLUFF is downloaded from Hugging Face and is not stored here.
- `runs/`, `results/`: run index and result files (kept out of git by default, see `.gitignore`).

## What is not in this repository

Paper 2 has gated arms (safety-detector flipping and aggregate refusal change). Their harness, prompts, traces and any edited safeguard checkpoints stay in a restricted store held by the PI and never come here. See `docs/GOVERNANCE.md`.

## Quick start

```bash
pip install -r requirements.txt
python -m pytest -q
python scripts/make_tables.py --results results/results.csv --out results/tables
```

## Rules for contributors

1. Fix hypotheses and thresholds in a dated `configs/prereg.md` before any test-split run.
2. Test splits are read once per experiment cell and every read is logged in `runs/test_access.log`.
3. Never hand-edit a number in the LaTeX. Regenerate it from the CSV files.
4. Report failed sessions as their own row. Do not rerun until a session succeeds.
5. No raw harmful text, surgeon traces for gated arms, or edited safeguard weights in this repository.

## Status

Planning stage. LICENSE to be chosen by the PI before the repository is made public.
