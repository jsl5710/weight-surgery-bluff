# File schemas

Scripts read only these files. One row per record. Missing values are empty, never "NA" strings.

## results.csv
`experiment, setting, model, method, seed, language, tier, family, val_f1, test_f1, tokens, passes, weights_changed_pct, session_status`

- `setting`: multilingual or cross_lingual
- `tier`: big_head or long_tail
- `session_status`: ok, rolled_back, no_edit, failed (failed sessions are kept, not dropped)
- `test_f1` is filled once, from the logged test read

## probes.csv
`model, setting, seed, language, probe_f1, head_f1, obstacle_score, k`

## cost.csv
`experiment, method, model, setting, minutes, gpu_hours, surgeon_tokens, dollars, weights_changed_pct, is_measured`

`is_measured` is 0 for planning assumptions and 1 once replaced by a measured value.

## ood.csv
`shift, model, setting, method, seed, language, shifted_f1, shifted_baseline_f1, bluff_gain, shifted_gain, retention`

- `shift`: held_out_languages, held_out_generators, other_datasets, dialect_variants
- `retention` is empty where `bluff_gain` is below 1 point (report absolute gain only)

## runs/index.csv
`experiment, config_hash, git_commit, seed, model_ids, start, end, cost, audit_log_path`

A result without an index row does not go in the paper.
