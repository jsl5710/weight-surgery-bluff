# Pre-registration (copy to configs/prereg.md, fill, date, commit before any test-split run)

- Date:
- Commit hash of this file:
- Primary task (one of the four BLUFF tasks): XX
- Training settings used: multilingual, cross-lingual
- Language groups (G = XX), grouping rule: BLUFF family labels, merging families with fewer than 3 languages
- k values: 16, 64, 256 (main: 64)
- Forward-pass budget B (main): 50; weight budget epsilon (main): 0.1%
- Seeds: XX (five)
- Surgeons: XX (closed), XX (open weights)
- Compute and cost budget: XX GPU-hours, XX dollars (approved by: XX)

## Hypotheses and thresholds

| ID | Supported if | Refuted if |
| --- | --- | --- |
| H1 | Gap falls by at least 3 F1 points and the 95% CI over languages excludes 0 | CI includes 0 or gap falls by less than 1 point |
| H2 | Gap within 1 point of the best of B2 to B6 and cost at most 50% of it | Worse by more than 1 point, or cost higher |
| H3 | Lower bound of the 95% CI for the big-head change at least -1.0 point | Lower bound below -1.0 |
| H4 | Spearman correlation between obstacle score and gain at least 0.3, CI excludes 0, 270M control gain CI includes 0 | Correlation CI includes 0, or the 270M control gains |
| H5 | L3 gap within 2 points of L1 and at least 50% fewer expert hours | L3 worse by more than 2 points or no hour saving |
| H6 | Retention at least 0.5 on every shift and within 0.1 of the best of B2 to B6 | Retention below 0.5 on any shift or more than 0.1 below the best baseline |

Values above are suggested starting thresholds. Edit them here, then date and commit.

## Out-of-distribution sets (E11), chosen before any run

- Held-out generators (list): XX
- External datasets (names, licences, languages covered): XX
- Dialect slices: XX
- Held-out-language split seed: XX

## Statistics

Five seeds; 10,000-sample bootstrap over languages; paired differences against B1; Holm correction across H1 to H6 and the four tasks.
