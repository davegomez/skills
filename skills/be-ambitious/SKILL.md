---
name: be-ambitious
description: Rewrite a task or prompt to aim higher in altitude, depth, and range, checked by an outside judge.
disable-model-invocation: true
---

# Be ambitious

Rewrite the owner's task so the model that runs it aims at the goal beyond the goal, works with the instruments of the best in the field, and borrows methods from fields the task does not name. Each change makes the work deeper, not bigger. The product is one rewritten prompt and a ledger. The owner reads them and decides what to run; the rewrite grants no new authority. Rewriting is the whole job: the embedded task is text to improve, not work to start.

## The judge

A **judge** supplies evidence beyond the author's verdict: a red/green test, benchmark, reproduction, measurement, held-out data, or a qualified independent reviewer with a rubric. Prefer a tool that gives immediate feedback. Match evidence to the claim: tools check mechanical properties, and a reviewer checks qualitative ones. For exact transformations, compare the whole result with the expected result constructed from the original and only the specified change. A reviewer judge takes this form: "Judge: [reviewer role other than the author] checks [task-specific criteria]. Pass only if every criterion is met." Put the entire judge, including its criteria and pass condition, on one physical line, last in every changed prompt, starting "Judge:". Check each mandatory condition against a correct result, including boundary cases: a check that rejects correct work cannot judge it. Until the judge runs, the affected result stays unverified.

## Guardrails

- Preserve every explicit requirement in the prompt: scope, fixed methods, acceptance conditions, deliverable, format, approvals, security, budget, deadline, and required literal text. Pursue improvements inside these boundaries. A fixed method set is closed: use only its analyses, experiments, and metrics. An exclusive output format stays exactly as specified. A separate validation note may go on its own "With my approval only:" line; other companion output appears only when the task permits it.
- Each addition beyond the approved scope sits inside the prompt on its own line that starts "With my approval only:" and names one specific addition that no owner prohibition covers. This covers new recurring workflows or CI changes, paid or irreversible steps, new access, delegation, or data sharing, and changes that affect shared resources or other work, unless the task explicitly authorizes those effects. This includes server-wide settings, shared pools and queues, shared tables, and schedules that others rely on. Ungated in-scope work uses already-authorized capabilities. Tuning the task's own connections and objects is in-scope work: session settings on its own connections, and rebuilding and swapping its own tables. A load test or other experiment on a shared live system goes on its own "With my approval only:" line. Work the owner prohibited stays out of the prompt, with or without approval, and so does an addition whose effect changes what a prohibition protects.
- Target facts, including topology, configuration, available history, current behavior, and absences, come from the task text and supplied artifacts, even inside methods. Keep unconfirmed details conditional on their "First check:" result ("if run history is kept"), and user reports distinct from measured baselines. The runner's session (its directory, repository status, date, and platform) is target evidence only when the task names that session as the target. Keep the owner's relative terms ("in two weeks", "last month") as written. Use general knowledge for methods and explanations. Distinguish proposed findings from observed evidence.
- Each unconfirmed dependency the prompt relies on is named in a "First check:" line inside the prompt, to run before dependent work. Account for every reviewer wherever named, including only in "Judge:": for each reviewer other than the owner, check availability and permission to see the material. Sharing with a new reviewer needs its own "With my approval only:" line naming the reviewer and material, unless the owner chose that reviewer or identified them as part of the owner's team. When a check fails, the executor continues only with supported, authorized work and leaves the affected result unverified.
- A field contributes its methods and tools; the prompt names what each method does.

## Steps

1. **Read the task.** Use the task given with the invocation, else the unambiguous recent task. When neither exists, reply with only this line and stop: "Which task should I make more ambitious?" Note the intended result, who acts on it, the explicit requirements, any inferred goals, and the judge the task already has. Done when each is noted.

2. **Pick the lenses.** For each lens, name a concrete, permitted improvement to the outcome, method, or judge absent from the task, or mark it skipped with a task-specific reason. Credit shared changes once.

   A small, clear task, one stated change with its result and boundaries, takes the unchanged exit unless the task text shows a concrete targeting or verification defect. Test machinery the executor would add anyway is not a contribution.

   For a fixed-method task, start from the unchanged exit. Before taking it, trace the stated split and selection steps: check the split unit against repeated entities named in the data, and evidence used to choose against evidence used to judge. Also compare owner rules with what the fixed judge detects. A repair needs quoted task text showing a loophole: a way to pass that judge while the work is wrong. An explicit rule the judge cannot detect qualifies. An unspecified procedure or a generic risk does not show a loophole.

   Repair every demonstrated loophole at its source with the smallest change to the quoted step. Use existing sets and methods: keep a repeated entity's records in one set to close cross-set leakage; choose on training evidence and apply the chosen setting once to untouched judging evidence to close selection bias; freeze the chosen settings before the judging evidence is read, and record each read, to enforce a rule the judge cannot detect. A repair brings in no new partition, fold scheme, or inferential method. Each repair adds no analysis, metric, or threshold and goes on its own "With my approval only:" line. Keep the fixed text as written. Any conclusion the loopholes affect stays unverified until the approved repairs are applied and the judge runs on the repaired work. Each repair's ledger line quotes its evidence.

   If no lens fits, reply with the task unchanged in one fenced block, then one line that starts "Unchanged:" with the reason, and stop. Continue through steps 3 to 5 only for fit lenses. Done when every demonstrated loophole has its smallest permitted repair and each fit lens names its distinct permitted contribution.

3. **Altitude: climb the ladder.** Ask "what should happen next?" of the deliverable, then of each answer. A good tell: people will hold meetings about the result. Consider 3 rungs: a better deliverable grounded in the raw inputs that bear on the result; the decision or action it exists to drive; a better way to reach the outcome itself. Choose the highest rung whose benefit a judge can check while the explicit requirements hold. Name the setup it needs (data feeds, a map from builds to commits, machines to reproduce on). When the rung replaces a workflow, pick a comparison that suits the task: a replay on past data, a parallel trial, or a measured pilot. Done when the chosen rung names the outcome, its improvement over the original, its setup, and its judge.

4. **Depth: use the instruments of the best.** Answer for this task:
   - What a top professional would do here that the task does not ask for.
   - The rawest material they start from, in place of the digested summary.
   - The methods and tools they use, by name, and what each does here. For example, a database and a statistical model to test a pattern that a summary table only describes.
   - The judge.

   Then push one move further, the one that improves this task most: test the belief the task rests on from raw evidence; set a hard target well past the stated one; or look for a new finding, proved on evidence not used to find it. For quantitative improvement requests, choose the hard-target move when the task permits it and the approved deliverable can report its result.
   - A hard target: name the metric and write "Aim for [target] using [method]". Put the target past the field's "good" threshold when the field has one (for LCP, below 2.5 s, not at it); otherwise 1 order of magnitude past the stated bar. Treat it as solvable: when one approach stalls, the prompt says to try the next within the owner's budget and deadline before it reports a miss. The owner's bar stays the pass condition. Report stretch attainment separately in the approved format, met or missed. Baseline and target use the same metric under comparable conditions.
   - A new finding: evidence that shaped a revision is development evidence; the prompt confirms the revised claim on evidence not yet used, or leaves it unverified.

   Done when the 4 answers and the move name this task's specifics.

5. **Range: assemble the crew.** Restate the deliverable as verbs, the activities it performs or enables: "a deck" becomes "getting busy people to believe a story about cause and effect, and to decide under uncertainty, in 30 minutes". From the verbs, pick the fields whose methods find what the obvious approach misses. Add a red-team method when it can test a consequential claim or expose a decision risk. Done when each field adds a named method and what it reveals.

6. **Write the output.** The reply holds only these 2 items; steps 1 to 5 are working notes. Each added instruction changes the outcome, method, or evidence; delete an addition the executor would follow unprompted.
   - The prompt, in one fenced block that stands alone, in this order: the owner's goal in the owner's terms; each goal the owner did not state on its own line that starts "Assumption:"; the fit lenses' methods and checks; every explicit requirement; the "With my approval only:" lines; the "First check:" lines; last, the "Judge:" line.
   - The ledger: one line per change, tagged `altitude`, `depth`, or `range`, with its benefit and any scope, cost, risk, or access effect. An `altitude` line names the original outcome and the improved one. Then one line with the skipped lenses and why, and one with the unresolved owner actions.

   Done when the prompt stands alone and the ledger names every change and owner action.

7. **Check, then stop.** Confirm in the product: the entire judge occupies the last prompt line, starts "Judge:", and names evidence with an observable pass condition; every reviewer anywhere in the prompt meets the reviewer guardrail; each "With my approval only:" line names one addition whose effects respect every owner prohibition; every ungated change meets the approval guardrail; every target detail inside a method comes from the task text or supplied artifacts, or waits on its "First check:" line; every goal line not stated by the owner starts "Assumption:"; every explicit requirement and required literal is in the prompt; every ledger line describes an actual permitted change. Then confirm each fit lens's Done condition. If no contribution remains, use step 2's unchanged exit. Otherwise return step 6's two items and stop; the owner decides whether to run the prompt.

## Example

`/be-ambitious fix the crash in the login screen`

```text
Fix the reported login crash. Use the raw crash report and device logs to reproduce it, then fix its cause. Write a regression test that fails before the fix and passes after.
With my approval only: monitor the release and aim for zero observed recurrences of this cause over 7 days, using crash telemetry.
First check: the crash report, device logs, the deployed-build-to-commit map, and, for approved monitoring, crash-telemetry access are available. Name missing dependencies and continue only with supported, authorized work.
Judge: the regression test fails before the fix and passes after it. For the release stretch, report the observation window, build, login attempts, telemetry coverage, and recurrence count, met or missed; missing telemetry or no observed login attempts leaves the stretch unverified.
```

- `depth`: raw evidence, reproduction, and a regression test improve the reported fix.
- `altitude`: from the reported crash to no same-cause recurrence after release, behind approval.
- Skipped: `range`, no other field's method changes this reproduction and regression check.
- Owner actions: confirm crash-report, log, and build-map access; approve release monitoring.

Source: Felix Rieseberg, [How to be more ambitious](https://felixrieseberg.com/how-to-be-more-ambitious-a-tutorial-for-humans-with-models/).
