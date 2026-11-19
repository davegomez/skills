# I05 preflight

Run by hand on 2026-11-18 with Xcode 27.3 (27C5020n). `grade.sh` builds nothing and uses no simulator. `EVAL_VARIANT` was unset, so the grader inferred the variant from the tree in every run.

## Commands

Work tree for each run: the fixture commit, plus the variant diff as an uncommitted change, plus the patch under test.

```sh
cp -R fixture W && cd W && git init -q && git add -A && git commit -qm fixture
git apply ../variants/<variant>.patch     # the change under review, left uncommitted
git apply <patch under test>              # reference.patch, a negative, or nothing
hidden/grade.sh W out.json
```

The 2 variant diffs compile (a sanity check, not a preflight step):

```sh
xcodebuild build -project Guestbook.xcodeproj -scheme Guestbook \
  -destination "generic/platform=iOS Simulator" CODE_SIGNING_ALLOWED=NO -quiet
```

Output: no `error` lines. `Guestbook.app` was built for both `seeded` and `clean`.

## Results

| Step | Variant | Patch | Expected | Result |
| --- | --- | --- | --- | --- |
| 1 | seeded | none | fails the case-critical checks | pass: `review-written` and 3 traps fail |
| 2 | seeded | `reference.patch` | passes every check | pass |
| 3 | seeded | `negative/I05-trap-personal-data-log.patch` | fails `I05-trap-personal-data-log` | pass: only that check fails |
| 3 | seeded | `negative/I05-no-lookalike-flagged.patch` | fails `I05-no-lookalike-flagged` | pass: only that check fails |
| 4 | seeded | `reference.patch`, 2 runs | identical results | pass: byte-identical JSON |
| 1 | clean | none | fails the case-critical checks | pass: `review-written` fails; traps are `na` |
| 2 | clean | `variants/clean-reference.patch` | passes every applicable check | pass |
| 3 | clean | `variants/clean-negative/I05-no-lookalike-flagged.patch` | fails `I05-no-lookalike-flagged` | pass: it also fails `I05-clean-no-unsupported-material` |
| 4 | clean | `variants/clean-reference.patch`, 2 runs | identical results | pass: byte-identical JSON |
| extra | seeded | `reference.patch` plus a 1-line code edit | fails `I05-no-edits` | pass |

## Output tail

```
seeded-fixture exit=0
  variant=seeded I05-no-edits=pass I05-review-written=fail I05-trap-personal-data-log=fail I05-trap-discarded-write=fail I05-trap-inaccessible-gesture=fail I05-no-lookalike-flagged=pass I05-clean-no-unsupported-material=na
  metrics: recall={"critical":0.0,"major":0.0,"minor":null} precision={"critical":null,"major":null,"minor":null} unsupported=0 material=0 lookalikes=[]
seeded-reference-1 exit=0
  variant=seeded I05-no-edits=pass I05-review-written=pass I05-trap-personal-data-log=pass I05-trap-discarded-write=pass I05-trap-inaccessible-gesture=pass I05-no-lookalike-flagged=pass I05-clean-no-unsupported-material=na
  metrics: recall={"critical":1.0,"major":1.0,"minor":null} precision={"critical":1.0,"major":1.0,"minor":null} unsupported=0 material=0 lookalikes=[]
seeded-reference-2 exit=0
  (same as seeded-reference-1)
seeded-neg-I05-no-lookalike-flagged exit=0
  variant=seeded I05-no-edits=pass I05-review-written=pass I05-trap-personal-data-log=pass I05-trap-discarded-write=pass I05-trap-inaccessible-gesture=pass I05-no-lookalike-flagged=fail I05-clean-no-unsupported-material=na
  metrics: recall={"critical":1.0,"major":1.0,"minor":null} precision={"critical":1.0,"major":1.0,"minor":0.0} unsupported=1 material=0 lookalikes=["lookalike-handled-try"]
seeded-neg-I05-trap-personal-data-log exit=0
  variant=seeded I05-no-edits=pass I05-review-written=pass I05-trap-personal-data-log=fail I05-trap-discarded-write=pass I05-trap-inaccessible-gesture=pass I05-no-lookalike-flagged=pass I05-clean-no-unsupported-material=na
  metrics: recall={"critical":0.0,"major":1.0,"minor":null} precision={"critical":null,"major":1.0,"minor":null} unsupported=0 material=0 lookalikes=[]
clean-fixture exit=0
  variant=clean I05-no-edits=pass I05-review-written=fail I05-trap-personal-data-log=na I05-trap-discarded-write=na I05-trap-inaccessible-gesture=na I05-no-lookalike-flagged=pass I05-clean-no-unsupported-material=pass
clean-reference-1 exit=0
  variant=clean I05-no-edits=pass I05-review-written=pass I05-trap-personal-data-log=na I05-trap-discarded-write=na I05-trap-inaccessible-gesture=na I05-no-lookalike-flagged=pass I05-clean-no-unsupported-material=pass
clean-reference-2 exit=0
  (same as clean-reference-1)
clean-neg-I05-no-lookalike-flagged exit=0
  variant=clean I05-no-edits=pass I05-review-written=pass I05-trap-personal-data-log=na I05-trap-discarded-write=na I05-trap-inaccessible-gesture=na I05-no-lookalike-flagged=fail I05-clean-no-unsupported-material=fail
  metrics: recall={"critical":null,"major":null,"minor":null} precision={"critical":null,"major":0.0,"minor":null} unsupported=1 material=1 lookalikes=["lookalike-accessible-gesture"]
seeded-edit-probe exit=0
  variant=seeded I05-no-edits=fail I05-review-written=pass I05-trap-personal-data-log=pass I05-trap-discarded-write=pass I05-trap-inaccessible-gesture=pass I05-no-lookalike-flagged=pass I05-clean-no-unsupported-material=na
seeded reference runs identical
clean reference runs identical
```
