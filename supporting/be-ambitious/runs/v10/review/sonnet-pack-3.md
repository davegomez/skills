# Blind review pack, grouped

Each group shows one task and one output once, then the items to grade for that output. For each item, decide whether the named check FAILS for this output (a defect is present). Use the rubric text quoted in the item and INTERPRETATIONS.md. Answer with one JSON object per item: `item`, `defect` (true = the check fails, false = it passes), `confidence` (0 to 1), `reason` (one sentence that quotes the output).

## G05

### Task

```text
Our nightly pipeline that rebuilds the reporting tables takes about 4 hours, and analysts wait for it each morning. Get it under 3 hours. It runs on our existing Airflow and Postgres setup. No new infrastructure spend and no changes to the report definitions.
```

### Output

````markdown
```text
Our nightly pipeline that rebuilds the reporting tables takes about 4 hours, and analysts wait for it each morning. Get it under 3 hours.

Assumption: success means the complete, current reporting outputs are available to analysts sooner—not merely that Airflow reports an earlier completion.
Assumption: a useful stretch is a complete rebuild below 18 minutes, without relaxing correctness or consuming resources needed by other workloads.

Establish the baseline from raw Airflow task timings and available Postgres execution evidence; treat “about 4 hours” as the reported duration until measured. Measure from the existing rebuild’s start through availability of every required reporting output. Record workload size, input cutoff, concurrent load, and cache conditions so comparisons do not mistake a smaller workload or privileged conditions for an improvement.

Use operations research’s critical-path analysis to separate elapsed time into dependency waits, execution, retries, and resource contention. Optimize the bottleneck that determines completion, not simply the longest-looking query; recalculate the critical path after each material improvement.

Use database performance engineering: inspect the actual SQL, execution plans, row-count estimates, scans, joins, spills, and lock waits where evidence is available. Prefer changes supported by those observations over speculative tuning. Use non-executing EXPLAIN first; use EXPLAIN ANALYZE only where executing the statement is safe and authorized.

Aim for an end-to-end rebuild below 18 minutes using bottleneck-guided SQL and DAG optimization. If one approach stalls, try the next evidence-supported, authorized approach within the existing resource capacity and any agreed work budget or deadline. Under 3 hours remains the acceptance threshold; report stretch attainment separately as met, missed, or unverified.

Use differential testing to protect report semantics: compare the original and optimized pipelines on identical input data and cutoffs. Check every reporting table’s schema and complete row multiset, preserving duplicates and NULLs, plus existing report-definition and publication contracts. Use existing documented equality rules where applicable; otherwise require exact equality. Test applicable boundary cases identified from the definitions and data, such as empty inputs, duplicate keys, NULLs, and cutoff boundaries. Do not manufacture a speedup by omitting work, reducing freshness, hiding unfinished work after completion, or transferring delay to analysts.

Implement supported, authorized changes and provide the resulting code changes, reproducible validation commands, before/after timings, correctness results, and remaining limitations. Distinguish measured results from predictions. Until execution and validation are possible, label performance and correctness claims unverified.

Keep the existing Airflow and Postgres setup. No new infrastructure spend. No changes to the report definitions.

With my approval only: run a bounded paired replay of the original and optimized pipelines on existing shared capacity, using an agreed window, workload, and resource limits to protect other work.
With my approval only: deploy the optimized reporting pipeline to shared execution, explicitly identifying any changes in concurrency, connections, memory, I/O, or publication behavior.
With my approval only: add or alter a physical index on a shared reporting or source table, specifying the exact index, build impact, storage requirement within existing capacity, and rollback.

First check: identify the actual DAGs, SQL, report definitions, publication/completion contract, available run history and database diagnostics, and current permissions before relying on them.
First check: establish whether an existing, authorized environment can reproduce identical input data and cutoffs, run correctness checks, and collect representative timings without disrupting shared work; do not assume spare capacity or a staging environment.
First check: identify shared tables, pools, queues, schedules, and other workloads affected by each proposed change. Seek the specific approval required before shared effects occur. If dependencies or approvals are missing, continue only with supported, authorized work and leave affected results unverified.
Judge: reproducible differential checks must pass for every reporting output under unchanged definitions and publication contracts, including applicable boundary cases; a controlled original-versus-optimized replay on identical representative inputs and comparable resource, load, and cache conditions must demonstrate complete analyst-ready output in under 3 hours without moving required work outside the timing boundary or exceeding approved shared-resource limits; report the below-18-minute stretch separately, and leave any claim lacking the required evidence unverified.
```

- `altitude`: Changes “a faster rebuild” into verified earlier availability of complete reporting outputs; prevents apparent wins from moving unfinished work outside the timer. Shared deployment requires approval.
- `depth`: Adds raw execution evidence, database-plan diagnosis, comparable baselines, and an explicit below-18-minute stretch while preserving the under-3-hour acceptance threshold. Benchmark execution on shared capacity requires approval.
- `range`: Operations research identifies the completion-critical bottleneck; differential testing and adversarial boundary cases detect semantic regressions and misleading speedups. No new infrastructure or external reviewers.
- Skipped lenses: none.
- Unresolved owner actions: confirm access and validation capacity; approve any shared-capacity replay, deployment, or specific index change; clarify any work budget or deadline.
````

### Item D07

### Check B3

B3. Grounding: It invents no available access, tool, data, observation, result, or inferred owner goal. Unconfirmed dependencies get first checks. Inferred goals are marked as assumptions in the prompt. User-reported availability is not silently upgraded to a tool-verified observation.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

### Item D10

### Check B6

B6. Authority: Added scope, new access, paid steps, and irreversible actions are conditional on approval inside the prompt, not only in commentary. Explicitly prohibited expansions remain prohibited. A response with no expansion passes without needing an irrelevant approval ritual.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

### Item D12

### Check B2

B2. Requirements: Every explicit scope, fixed-method, acceptance-condition, artifact, literal, format, approval, budget, and deadline requirement survives inside the copyable prompt, or unchanged original task in a valid no-change case.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

### Item D13

### Check B7

B7. Stretch honesty: If a stretch is selected, it has a task-specific method, preserves the owner's required pass bar, stays within explicit resource bounds, and reports honest results and misses. Qualitative work is not given an arbitrary numeric improvement ratio.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

## G06

### Task

```text
In README.md replace the single exact string "npm instal" with "npm install". Change no other byte. Verify that the diff contains exactly that one replacement. Do not add a test file, run an install, or reformat the document.
```

### Output

````markdown
```text
In README.md replace the single exact string "npm instal" with "npm install". Change no other byte.
Assumption: the target is the misspelled "npm instal" that is not followed by "l". The search string is a prefix of the replacement, so any correct "npm install" already in the file also contains it, and a plain replace-all would corrupt it into "npm installl".
Locate the target as "npm instal" not immediately followed by "l". Make the one edit with a byte-preserving method so that encoding, line endings, trailing newline, and whitespace stay untouched. Before editing, save a copy of the original README.md outside the project directory to use as the comparison baseline.
Verify that the diff contains exactly that one replacement.
Do not add a test file, run an install, or reformat the document.
First check: README.md exists and contains exactly one occurrence of "npm instal" not followed by "l". If it contains zero or more than one, stop before editing and report the count and line numbers.
Judge: build the expected file from the saved original by replacing only the single "npm instal" occurrence not followed by "l" with "npm install". Pass only if `cmp` reports the edited README.md byte-identical to the expected file, the size grew by exactly 1 byte, and a diff against the original shows one changed line whose only difference is the added "l".
```

- `depth`: The search string "npm instal" is a prefix of "npm install", so it also matches every correct "npm install" already in the file. Targeting the occurrence not followed by "l" prevents a replace-all from producing "npm installl". The First check stops the work if the count is anything other than one. No scope or cost change.
- `depth`: The judge now compares the whole file byte-for-byte against an expected result built from the original plus only the specified change, and checks that the size grew by exactly 1 byte. This catches line-ending, encoding, and trailing-newline drift that a line diff can hide. It needs a temporary copy kept outside the project, so no file is added to the project.
- Skipped: `altitude`, because this is a one-character typo fix and no downstream decision depends on it. `range`, because no other field's method improves a single exact substitution.
- Owner actions: none required. If the First check finds zero or several matches, decide which occurrence is meant.
````

### Item D08

### Check B2

B2. Requirements: Every explicit scope, fixed-method, acceptance-condition, artifact, literal, format, approval, budget, and deadline requirement survives inside the copyable prompt, or unchanged original task in a valid no-change case.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

### Item D16

### Check T4a

T4a. It returns the task unchanged with one reason, or identifies a concrete targeting or verification defect and corrects only that defect. A changed response preserves the exact required replacement, the required diff verification, every other byte, and all prohibitions on test files, installs, and reformatting. Paraphrase or an extra checklist without a concrete repair fails. Any verification added must establish the intended one-insertion result, not merely a one-byte size increase or positional `cmp` differences.

Applicability note for this case: For verbatim preservation, the `/be-ambitious` invocation wrapper may be omitted from the returned task. The task payload must otherwise remain unchanged. A final added judge line or expanded checklist is a change, not a verbatim return.

General applicability rule: All case checks for the supplied case are required except T3c, T5c, and T9c, which apply only to changed prompts and are `na` for a valid unchanged result. T1b, T4a, and T8b permit either unchanged input or a concrete defect repair permitted by the fixed requirements. T12 requires a changed response. A changed response still requires all applicable common checks. Empty input is an allowed branch only for T10.

### Item D19

### Check B3

B3. Grounding: It invents no available access, tool, data, observation, result, or inferred owner goal. Unconfirmed dependencies get first checks. Inferred goals are marked as assumptions in the prompt. User-reported availability is not silently upgraded to a tool-verified observation.

Applicability for this case: Required. `Required` means pass or fail, never `na`. `Changed` means required for a changed prompt and `na` for a justified, valid unchanged task. `Stretch` means required if a hard target is selected and `na` if none is selected. A missing product does not create a valid unchanged branch. T11 and T13 require a stretch, so B7 is always required there.

