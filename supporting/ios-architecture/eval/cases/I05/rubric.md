# I05 rubric (blind reviewer)

`grade.sh` already settles the tree hash, the format, trap recall, lookalike flags, and unsupported counts. Grade only these checks. Each result is `pass`, `fail`, `na`, or `unverified`, with the finding line as evidence.

| Check id | Priority | Severity | Pass condition |
| --- | --- | --- | --- |
| I05-R-harmless-fixes | security | major | No recommended fix would add a defect. For example, a fix that keeps the guest's name or email in the log at any privacy level, removes the existing accessibility action, or drops the error report of `persist()` fails. |
| I05-R-causal-reasons | reliability | minor | Each finding that `grade.sh` matched to a trap states the user impact and a concrete fix that fits the code at that line. |
| I05-R-novel-findings | reliability | major | Each unsupported finding (listed in the result `metrics.unsupported_findings`) names a real defect in the changed lines, with evidence in the code. A finding about unchanged code, a style preference, or benign code fails. `na` when there are no unsupported findings. |
| I05-R-severity-fit | reliability | minor | Each finding's severity matches the definitions in the task: `critical` for a security or privacy defect or a crash, `major` for a functional, reliability, or accessibility defect that users will hit, and `minor` for the rest. |
