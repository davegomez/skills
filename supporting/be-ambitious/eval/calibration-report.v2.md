# Jev calibration report

Labels: recorded grades plus `overrides.json`. Probabilities are P(defect). Excluded as rubric drift: v2 T4a.
Previous report (single B2/B6 questions, in-sample numbers only): `calibration-report.v1.md`.

## How to read this report

- Trust the held-out columns. For each check and each version v, the threshold is chosen on the other 5 versions (max balanced accuracy,
  ties nearest 0.5) and only then applied to v; the 6 held-out confusions are pooled. The in-sample columns fit and score on the same labels
  and are kept only to show the gap; a large gap means the threshold does not transfer across skill versions.
- AUC needs no threshold, so it is computed on all labels; the per-version table shows held-out AUC / chosen threshold (fails/n) per version.
- status: ready = held-out balanced accuracy >= 0.85 with >= 5 fails; close = >= 0.75; not usable = below; fewer than 5 fail labels = too few fails to measure (its numbers are noise).
- `thr (all)` is the threshold fitted on all labels: the one to use going forward. p >= threshold means Jev says fail.
- B2 and B6 are each graded by two Jev questions (B2a/B2b, B6a/B6b); the check's probability is the max of its parts, so it fails
  when either part is over the shared threshold. Part rows are scored against the parent label and are diagnostic only.
- `X@v1` rows are the previous single-question wording, `X@r1` rows an earlier round of the current wording, on the same labels.
- false-pass = label fail, Jev pass. false-fail = label pass, Jev fail. uncertain = answers in 0.3..0.7.

## Per-check calibration

| check | n | fails | AUC | thr (all) | in-sample bal. acc | in-sample acc | in-sample false-pass | in-sample false-fail | held-out bal. acc | held-out acc | held-out false-pass | held-out false-fail | uncertain 0.3-0.7 | status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| B2 | 360 | 37 | 0.92 | 0.430 | 0.84 | 0.78 | 3 | 75 | 0.82 | 0.78 | 5 | 75 | 134 | close |
| B2@r1 | 360 | 37 | 0.90 | 0.400 | 0.82 | 0.76 | 4 | 81 | 0.76 | 0.79 | 10 | 67 | 136 | earlier wording |
| B2@v1 | 360 | 37 | 0.72 | 0.410 | 0.68 | 0.78 | 16 | 65 | 0.67 | 0.78 | 17 | 64 | 206 | earlier wording |
| B2a | 360 | 37 | 0.57 | 0.410 | 0.59 | 0.87 | 28 | 20 | 0.52 | 0.81 | 31 | 39 | 67 | component of B2 |
| B2a@r1 | 360 | 37 | 0.57 | 0.390 | 0.60 | 0.86 | 27 | 25 | 0.56 | 0.86 | 30 | 22 | 62 | earlier wording |
| B2b | 360 | 37 | 0.82 | 0.700 | 0.80 | 0.93 | 13 | 14 | 0.79 | 0.92 | 14 | 14 | 92 | component of B2 |
| B2b@r1 | 360 | 37 | 0.81 | 0.710 | 0.77 | 0.94 | 16 | 7 | 0.76 | 0.94 | 17 | 5 | 100 | earlier wording |
| B3 | 396 | 58 | 0.91 | 0.370 | 0.84 | 0.83 | 9 | 59 | 0.81 | 0.82 | 12 | 58 | 146 | close |
| B4 | 342 | 24 | 0.90 | 0.360 | 0.83 | 0.86 | 5 | 44 | 0.77 | 0.82 | 7 | 53 | 63 | close |
| B5 | 342 | 7 | 0.89 | 0.500 | 0.91 | 0.82 | 0 | 63 | 0.77 | 0.82 | 2 | 61 | 271 | close |
| B6 | 360 | 38 | 0.86 | 0.410 | 0.80 | 0.81 | 8 | 61 | 0.79 | 0.81 | 9 | 58 | 168 | close |
| B6@r1 | 360 | 38 | 0.80 | 0.360 | 0.77 | 0.76 | 8 | 78 | 0.77 | 0.76 | 8 | 78 | 155 | earlier wording |
| B6@v1 | 360 | 38 | 0.63 | 0.420 | 0.62 | 0.42 | 5 | 202 | 0.58 | 0.48 | 11 | 176 | 284 | earlier wording |
| B6a | 360 | 38 | 0.85 | 0.410 | 0.81 | 0.82 | 8 | 55 | 0.81 | 0.82 | 8 | 55 | 153 | component of B6 |
| B6a@r1 | 360 | 38 | 0.80 | 0.360 | 0.78 | 0.78 | 8 | 71 | 0.78 | 0.78 | 8 | 71 | 139 | earlier wording |
| B6b | 360 | 38 | 0.61 | 0.100 | 0.62 | 0.50 | 9 | 170 | 0.62 | 0.50 | 9 | 170 | 27 | component of B6 |
| B6b@r1 | 360 | 38 | 0.64 | 0.100 | 0.62 | 0.50 | 9 | 171 | 0.59 | 0.46 | 9 | 187 | 24 | earlier wording |
| B7 | 51 | 10 | 0.89 | 0.140 | 0.84 | 0.80 | 1 | 9 | 0.77 | 0.75 | 2 | 11 | 7 | close |
| B10 | 108 | 0 | n/a | 0.500 | n/a | 1.00 | 0 | 0 | n/a | 1.00 | 0 | 0 | 0 | too few fails to measure |
| T1a | 36 | 2 | 0.99 | 0.380 | 0.99 | 0.97 | 0 | 1 | 0.74 | 0.94 | 1 | 1 | 3 | too few fails to measure |
| T1b | 36 | 0 | n/a | 0.500 | n/a | 1.00 | 0 | 0 | n/a | 1.00 | 0 | 0 | 0 | too few fails to measure |
| T1c | 36 | 0 | n/a | 0.500 | n/a | 0.97 | 0 | 1 | n/a | 0.97 | 0 | 1 | 1 | too few fails to measure |
| T2a | 36 | 1 | 1.00 | 0.370 | 1.00 | 1.00 | 0 | 0 | 0.50 | 0.97 | 1 | 0 | 1 | too few fails to measure |
| T2b | 36 | 0 | n/a | 0.500 | n/a | 1.00 | 0 | 0 | n/a | 1.00 | 0 | 0 | 0 | too few fails to measure |
| T2c | 36 | 0 | n/a | 0.500 | n/a | 1.00 | 0 | 0 | n/a | 1.00 | 0 | 0 | 0 | too few fails to measure |
| T3a | 36 | 0 | n/a | 0.500 | n/a | 1.00 | 0 | 0 | n/a | 1.00 | 0 | 0 | 0 | too few fails to measure |
| T3b | 36 | 4 | 0.71 | 0.140 | 0.69 | 0.83 | 2 | 4 | 0.58 | 0.83 | 3 | 3 | 0 | too few fails to measure |
| T3c | 36 | 12 | 0.93 | 0.500 | 0.90 | 0.86 | 0 | 5 | 0.83 | 0.83 | 2 | 4 | 7 | close |
| T4a | 30 | 5 | 0.57 | 0.110 | 0.66 | 0.43 | 0 | 17 | 0.56 | 0.40 | 1 | 17 | 0 | not usable |
| T4b | 36 | 0 | n/a | 0.500 | n/a | 1.00 | 0 | 0 | n/a | 1.00 | 0 | 0 | 0 | too few fails to measure |
| T4c | 36 | 1 | 0.89 | 0.120 | 0.94 | 0.89 | 0 | 4 | 0.46 | 0.89 | 1 | 3 | 2 | too few fails to measure |
| T5a | 36 | 5 | 0.86 | 0.230 | 0.90 | 0.83 | 0 | 6 | 0.90 | 0.83 | 0 | 6 | 4 | ready |
| T5b | 36 | 0 | n/a | 0.500 | n/a | 1.00 | 0 | 0 | n/a | 1.00 | 0 | 0 | 0 | too few fails to measure |
| T5c | 36 | 2 | 0.68 | 0.170 | 0.81 | 0.64 | 0 | 13 | 0.31 | 0.58 | 2 | 13 | 11 | too few fails to measure |
| T6a | 36 | 0 | n/a | 0.500 | n/a | 1.00 | 0 | 0 | n/a | 1.00 | 0 | 0 | 0 | too few fails to measure |
| T6b | 36 | 0 | n/a | 0.500 | n/a | 1.00 | 0 | 0 | n/a | 1.00 | 0 | 0 | 0 | too few fails to measure |
| T6c | 36 | 0 | n/a | 0.500 | n/a | 1.00 | 0 | 0 | n/a | 1.00 | 0 | 0 | 0 | too few fails to measure |
| T7a | 36 | 1 | 0.91 | 0.100 | 0.96 | 0.92 | 0 | 3 | 0.49 | 0.94 | 1 | 1 | 0 | too few fails to measure |
| T7b | 36 | 1 | 0.50 | 0.120 | 0.73 | 0.47 | 0 | 19 | 0.27 | 0.53 | 1 | 16 | 0 | too few fails to measure |
| T7c | 36 | 0 | n/a | 0.500 | n/a | 1.00 | 0 | 0 | n/a | 1.00 | 0 | 0 | 0 | too few fails to measure |
| T8a | 36 | 21 | 0.89 | 0.570 | 0.86 | 0.86 | 3 | 2 | 0.83 | 0.83 | 3 | 3 | 5 | close |
| T8b | 36 | 25 | 0.82 | 0.350 | 0.77 | 0.86 | 0 | 5 | 0.74 | 0.78 | 4 | 4 | 26 | not usable |
| T8c | 36 | 0 | n/a | 0.500 | n/a | 1.00 | 0 | 0 | n/a | 1.00 | 0 | 0 | 0 | too few fails to measure |
| T9a | 36 | 4 | 0.89 | 0.460 | 0.84 | 0.92 | 1 | 2 | 0.81 | 0.86 | 1 | 4 | 18 | too few fails to measure |
| T9b | 36 | 2 | 0.78 | 0.140 | 0.87 | 0.75 | 0 | 9 | 0.63 | 0.75 | 1 | 8 | 2 | too few fails to measure |
| T9c | 36 | 1 | 0.86 | 0.220 | 0.93 | 0.86 | 0 | 5 | 0.44 | 0.86 | 1 | 4 | 4 | too few fails to measure |
| T11a | 36 | 2 | 0.98 | 0.050 | 0.96 | 0.92 | 0 | 3 | 0.72 | 0.92 | 1 | 2 | 0 | too few fails to measure |
| T11b | 36 | 3 | 1.00 | 0.500 | 1.00 | 1.00 | 0 | 0 | 1.00 | 1.00 | 0 | 0 | 0 | too few fails to measure |
| T11c | 36 | 0 | n/a | 0.500 | n/a | 1.00 | 0 | 0 | n/a | 1.00 | 0 | 0 | 8 | too few fails to measure |
| T11d | 36 | 1 | 0.36 | 0.130 | 0.66 | 0.33 | 0 | 24 | 0.21 | 0.42 | 1 | 20 | 1 | too few fails to measure |

## Held-out per version (AUC / threshold chosen on the other versions (fails/n))

| check | v2 | v3 | v4 | v5 | v6 | v7 |
|---|---|---|---|---|---|---|
| B2 | 0.93 / 0.43 (9/60) | 0.97 / 0.43 (7/60) | 0.95 / 0.43 (10/60) | 0.94 / 0.43 (5/60) | 0.90 / 0.48 (5/60) | 0.53 / 0.43 (1/60) |
| B2@r1 | 0.93 / 0.40 (9/60) | 0.98 / 0.40 (7/60) | 0.95 / 0.40 (10/60) | 0.78 / 0.71 (5/60) | 0.87 / 0.48 (5/60) | 0.56 / 0.48 (1/60) |
| B2@v1 | 0.70 / 0.45 (9/60) | 0.73 / 0.41 (7/60) | 0.80 / 0.41 (10/60) | 0.58 / 0.41 (5/60) | 0.82 / 0.41 (5/60) | 0.32 / 0.41 (1/60) |
| B2a | 0.48 / 0.28 (9/60) | 0.28 / 0.41 (7/60) | 0.65 / 0.43 (10/60) | 0.61 / 0.28 (5/60) | 0.77 / 0.52 (5/60) | 0.76 / 0.41 (1/60) |
| B2a@r1 | 0.48 / 0.39 (9/60) | 0.31 / 0.40 (7/60) | 0.61 / 0.39 (10/60) | 0.65 / 0.39 (5/60) | 0.79 / 0.49 (5/60) | 0.79 / 0.39 (1/60) |
| B2b | 0.81 / 0.70 (9/60) | 0.97 / 0.70 (7/60) | 0.88 / 0.70 (10/60) | 0.69 / 0.72 (5/60) | 0.70 / 0.70 (5/60) | 0.63 / 0.70 (1/60) |
| B2b@r1 | 0.80 / 0.71 (9/60) | 0.98 / 0.71 (7/60) | 0.89 / 0.83 (10/60) | 0.54 / 0.71 (5/60) | 0.72 / 0.71 (5/60) | 0.65 / 0.71 (1/60) |
| B3 | 0.94 / 0.37 (12/66) | 0.80 / 0.41 (9/66) | 0.92 / 0.37 (6/66) | 0.95 / 0.41 (9/66) | 0.92 / 0.37 (15/66) | 0.96 / 0.37 (7/66) |
| B4 | 0.96 / 0.17 (6/59) | 0.84 / 0.36 (5/59) | 1.00 / 0.36 (1/59) | 0.91 / 0.49 (6/60) | 0.91 / 0.36 (4/51) | 0.75 / 0.36 (2/54) |
| B5 | 0.93 / 0.55 (5/59) | n/a / 0.50 (0/59) | n/a / 0.50 (0/59) | n/a / 0.50 (0/60) | 0.87 / 0.50 (1/51) | 0.91 / 0.50 (1/54) |
| B6 | 0.83 / 0.41 (9/60) | 0.87 / 0.41 (9/60) | 0.97 / 0.41 (4/60) | 0.83 / 0.41 (8/60) | 0.97 / 0.41 (6/60) | 0.72 / 0.44 (2/60) |
| B6@r1 | 0.80 / 0.36 (9/60) | 0.84 / 0.36 (9/60) | 0.94 / 0.36 (4/60) | 0.65 / 0.36 (8/60) | 0.92 / 0.36 (6/60) | 0.66 / 0.36 (2/60) |
| B6@v1 | 0.69 / 0.42 (9/60) | 0.74 / 0.50 (9/60) | 0.79 / 0.42 (4/60) | 0.55 / 0.48 (8/60) | 0.59 / 0.42 (6/60) | 0.52 / 0.50 (2/60) |
| B6a | 0.74 / 0.41 (9/60) | 0.87 / 0.41 (9/60) | 0.97 / 0.41 (4/60) | 0.84 / 0.41 (8/60) | 0.97 / 0.41 (6/60) | 0.79 / 0.41 (2/60) |
| B6a@r1 | 0.71 / 0.36 (9/60) | 0.84 / 0.36 (9/60) | 0.95 / 0.36 (4/60) | 0.67 / 0.36 (8/60) | 0.93 / 0.36 (6/60) | 0.71 / 0.36 (2/60) |
| B6b | 0.64 / 0.10 (9/60) | 0.60 / 0.10 (9/60) | 0.72 / 0.10 (4/60) | 0.63 / 0.10 (8/60) | 0.60 / 0.10 (6/60) | 0.41 / 0.10 (2/60) |
| B6b@r1 | 0.69 / 0.10 (9/60) | 0.65 / 0.08 (9/60) | 0.73 / 0.10 (4/60) | 0.66 / 0.10 (8/60) | 0.61 / 0.10 (6/60) | 0.36 / 0.10 (2/60) |
| B7 | 0.79 / 0.09 (5/15) | 0.92 / 0.14 (3/7) | 1.00 / 0.14 (1/7) | 0.75 / 0.29 (1/9) | n/a / 0.14 (0/6) | n/a / 0.14 (0/7) |
| T1a | n/a / 0.38 (0/6) | 1.00 / 0.38 (1/6) | 1.00 / 0.50 (1/6) | n/a / 0.38 (0/6) | n/a / 0.38 (0/6) | n/a / 0.38 (0/6) |
| T2a | 1.00 / 0.50 (1/6) | n/a / 0.37 (0/6) | n/a / 0.37 (0/6) | n/a / 0.37 (0/6) | n/a / 0.37 (0/6) | n/a / 0.37 (0/6) |
| T3b | n/a / 0.14 (0/6) | n/a / 0.14 (0/6) | 0.81 / 0.10 (2/6) | n/a / 0.14 (0/6) | 0.80 / 0.19 (1/6) | 0.60 / 0.14 (1/6) |
| T3c | 0.89 / 0.65 (3/6) | 1.00 / 0.50 (3/6) | 1.00 / 0.50 (1/6) | 0.89 / 0.50 (3/6) | 1.00 / 0.50 (2/6) | n/a / 0.59 (0/6) |
| T4a | - | 0.38 / 0.13 (2/6) | 0.40 / 0.11 (1/6) | 0.20 / 0.11 (1/6) | n/a / 0.11 (0/6) | 1.00 / 0.11 (1/6) |
| T4c | n/a / 0.12 (0/6) | n/a / 0.12 (0/6) | n/a / 0.12 (0/6) | n/a / 0.12 (0/6) | 0.80 / 0.50 (1/6) | n/a / 0.12 (0/6) |
| T5a | n/a / 0.23 (0/6) | n/a / 0.23 (0/6) | 0.90 / 0.23 (1/6) | 1.00 / 0.23 (2/6) | 1.00 / 0.23 (2/6) | n/a / 0.23 (0/6) |
| T5c | n/a / 0.17 (0/6) | n/a / 0.17 (0/6) | n/a / 0.17 (0/6) | n/a / 0.17 (0/6) | 1.00 / 0.50 (2/6) | n/a / 0.17 (0/6) |
| T7a | n/a / 0.10 (0/6) | n/a / 0.10 (0/6) | n/a / 0.10 (0/6) | n/a / 0.10 (0/6) | n/a / 0.10 (0/6) | 0.60 / 0.50 (1/6) |
| T7b | n/a / 0.12 (0/6) | 0.40 / 0.50 (1/6) | n/a / 0.12 (0/6) | n/a / 0.12 (0/6) | n/a / 0.12 (0/6) | n/a / 0.12 (0/6) |
| T8a | n/a / 0.30 (6/6) | n/a / 0.57 (6/6) | 0.56 / 0.57 (4/6) | 0.83 / 0.57 (3/6) | 1.00 / 0.30 (2/6) | n/a / 0.57 (0/6) |
| T8b | n/a / 0.35 (6/6) | n/a / 0.35 (6/6) | 0.70 / 0.35 (5/6) | 0.33 / 0.35 (3/6) | 1.00 / 0.62 (3/6) | 0.75 / 0.62 (2/6) |
| T9a | 1.00 / 0.33 (2/6) | n/a / 0.46 (0/6) | 1.00 / 0.46 (1/6) | n/a / 0.46 (0/6) | 0.60 / 0.46 (1/6) | n/a / 0.46 (0/6) |
| T9b | n/a / 0.14 (0/6) | n/a / 0.14 (0/6) | 0.80 / 0.14 (1/6) | 0.60 / 0.16 (1/6) | n/a / 0.14 (0/6) | n/a / 0.14 (0/6) |
| T9c | 0.80 / 0.50 (1/6) | n/a / 0.22 (0/6) | n/a / 0.22 (0/6) | n/a / 0.22 (0/6) | n/a / 0.22 (0/6) | n/a / 0.22 (0/6) |
| T11a | n/a / 0.05 (0/6) | 1.00 / 0.05 (1/6) | 0.90 / 0.07 (1/6) | n/a / 0.05 (0/6) | n/a / 0.05 (0/6) | n/a / 0.05 (0/6) |
| T11b | n/a / 0.50 (0/6) | 1.00 / 0.50 (2/6) | 1.00 / 0.50 (1/6) | n/a / 0.50 (0/6) | n/a / 0.50 (0/6) | n/a / 0.50 (0/6) |
| T11d | n/a / 0.13 (0/6) | n/a / 0.13 (0/6) | n/a / 0.13 (0/6) | n/a / 0.13 (0/6) | n/a / 0.13 (0/6) | 0.20 / 0.50 (1/6) |

## Repeatability

Same question, same run, asked twice; 29 runs (seed 20261018, half labelled fail on B2 or B6, half pass on both).
Flips count verdict changes at the all-labels threshold.

| question | mean abs change | max abs change | verdict flips |
|---|---|---|---|
| B2 | 0.020 | 0.130 | 1 |
| B2a | 0.016 | 0.060 | - |
| B2b | 0.018 | 0.130 | - |
| B6 | 0.020 | 0.040 | 0 |
| B6a | 0.019 | 0.040 | - |
| B6b | 0.008 | 0.040 | - |

## Totals

- runs with every current question answered: 396 of 396; Jev requests this invocation: 0; failed requests: 0
- Jev requests logged in the cache: 1156; input tokens: 3,989,869 (r1 1,125,062, r2 1,187,702, r2 repeat 141,890, v1 1,535,215)
- cost (all logged requests): $0.1676 at $0.042/M input tokens; output free
- wall time this invocation: 0.0 s
- disagreements at the held-out thresholds: 488 (see disagreements.json)

## Lint vs v7 labels

Counts are label/lint status pairs over the 66 v7 runs (na pairs dropped).

| comparison | agree | label pass, lint fail | label fail, lint pass | other |
|---|---|---|---|---|
| B4 vs L1 | 51 | 2 | 1 | 0 |
| T10a vs L5 | 6 | 0 | 0 | 0 |
| T1a vs L3 | 6 | 0 | 0 | 0 |
| B2 vs L3 (T1) | 6 | 0 | 0 | 0 |
| T5a vs L3 | 6 | 0 | 0 | 0 |
| B2 vs L3 (T5) | 6 | 0 | 0 | 0 |
| T11b vs L6 | 1 | 5 | 0 | 0 |

T11 parsed LCP targets (L6 passes only below 2.5 s): `T11-claude-1` fail (lcp_target_s=2.5), `T11-claude-2` pass (lcp_target_s=2), `T11-claude-3` fail (lcp_target_s=2.5), `T11-pi-1` fail (lcp_target_s=2.5), `T11-pi-2` fail (lcp_target_s=2.5), `T11-pi-3` fail (lcp_target_s=2.5)

- L2 statuses over v7: na 20, pass 46
- L4 statuses over v7: na 60, pass 6
- L7 statuses over v7: flag 8, na 51, pass 7
- L7 review hints (approval lines sharing words with a prohibition):
  - `T05-claude-2`: extra <- pull extra fields for the same tickets from the ticketing
  - `T06-claude-1`: credentials,production,request <- run the survival and cohort analysis on de-identified, ac
  - `T06-claude-2`: credentials,data,production,request <- request a de-identified CRM export or analytics extract f || customer <- interview internal customer success, support, and sales s
  - `T06-pi-1`: credentials,production,request <- request a minimal, anonymized evidence summary to perform
  - `T07-claude-1`: change <- request specific additional fields or less-redacted notes || change,policy <- any investigation, fix, monitoring, or policy change that
  - `T07-claude-2`: change <- list next steps the team could take, such as deeper inves
  - `T07-claude-3`: change,checkout <- ask for additional redacted fields so that next week's re
  - `T07-pi-3`: access <- include a separately labeled proposal for work beyond dra

Disagreement detail:
- B4 vs L1 `T01-claude-2`: label fail, lint pass: last paragraph: Judge: the existing test runner shows the null test red before the fix and green after. Every 
- B4 vs L1 `T05-claude-1`: label pass, lint fail: Pass only if every criterion is met. Until that review runs, the ranking is unverified.
- B4 vs L1 `T05-claude-3`: label pass, lint fail: - If the independent recode is approved, a Cohen's kappa of at least 0.8 confirms the categories. Without that
- T11b vs L6 `T11-claude-1`: label pass, lint fail: lcp_target_s=2.5: Aim for a mobile LCP of 2.5 s or less on the fixed profile (the Core Web Vitals "good" thres
- T11b vs L6 `T11-claude-3`: label pass, lint fail: lcp_target_s=2.5: 4. Aim for a lab median LCP at or under 2.5s and TBT under 200ms on the step 1 device and ne
- T11b vs L6 `T11-pi-1`: label pass, lint fail: lcp_target_s=2.5: Aim for mobile LCP of 2.5 seconds or less using critical-path optimization under the same ba
- T11b vs L6 `T11-pi-2`: label pass, lint fail: lcp_target_s=2.5: - Aim for median mobile LCP of 2.5 seconds or less using critical-path reduction and evidenc
- T11b vs L6 `T11-pi-3`: label pass, lint fail: lcp_target_s=2.5: 4. Aim for median mobile LCP of 2.5 seconds or less using critical-resource prioritization, 
