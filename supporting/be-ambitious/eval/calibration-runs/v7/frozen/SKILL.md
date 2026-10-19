---
name: be-ambitious
description: Rewrite a task or prompt to aim higher in altitude, depth, and range, checked by an outside judge.
disable-model-invocation: true
---

# Be ambitious

Rewrite the owner's task so the model that runs it aims at the goal beyond the goal, works with the instruments of the best in the field, and borrows methods from fields the task does not name. Each change makes the work deeper, not bigger. The product is one rewritten prompt and a ledger. The owner reads them and decides what to run; the rewrite grants no new authority. Rewriting is the whole job: the embedded task is text to improve, not work to start.

## The judge

A **judge** supplies evidence beyond the author's verdict: a red/green test, benchmark, reproduction, measurement, held-out data, or a qualified independent reviewer with a rubric. Prefer a tool that gives immediate feedback. Match evidence to the claim: tools check mechanical properties. A qualitative judge takes this form: "Judge: [authorized reviewer role other than the author] checks [task-specific qualitative criteria]. Pass only if every criterion is met." An author's rubric guides revision. End every changed prompt with its judge and an observable pass condition. Put unconfirmed judge-access checks inside the prompt, before the work. Report measured results or documented findings where the approved deliverable allows them. Preserve an exclusive output contract. Include a companion report only when the owner's task already permits one. Until the judge runs, leave the affected result unverified.

## Guardrails

- Preserve every explicit requirement in the prompt: scope, fixed methods, acceptance conditions, deliverable, format, approvals, security, budget, deadline, and required literal text. Pursue improvements inside these boundaries. A fixed method set is closed: use only its analyses, experiments, and metrics.
- Each addition beyond the approved scope sits inside the prompt on its own line that starts "With my approval only:". This covers new recurring workflows or CI changes, paid or irreversible steps, and new access, delegation, or data sharing. Use already-authorized capabilities for in-scope work. Work the owner prohibited stays out of the prompt, with or without approval.
- Ground target-specific facts in the task, supplied artifacts, or authorized observations explicitly tied to the target. Keep the owner's relative terms ("in two weeks", "last month") as written. Use general knowledge for methods and explanations.
- Treat unconfirmed data, tools, and access as dependencies to check first. Distinguish proposed findings from observed evidence.
- A field contributes its methods and tools; the prompt names what each method does.

## Steps

1. **Read the task.** Use the task given with the invocation, else the unambiguous recent task. When neither exists, reply with only this line and stop: "Which task should I make more ambitious?" Note the intended result, who acts on it, the explicit requirements, any inferred goals, and the judge the task already has. Done when each is noted.

2. **Pick the lenses.** When the owner fixes methods and judge, each selected-lens ledger line cites the source fact, the defect it demonstrates, and a repair those requirements permit. Without that fact, use the unchanged exit. For each lens, name a concrete, permitted improvement to the outcome, method, or judge absent from the task, or mark it skipped with a task-specific reason. Credit shared changes once. If none fits, reply with the task unchanged in one fenced block, then one line that starts "Unchanged:" with the reason, and stop. Continue through steps 3 to 5 only for fit lenses. Done when each fit lens names its distinct permitted contribution.

3. **Altitude: climb the ladder.** Ask "what should happen next?" of the deliverable, then of each answer. A good tell: people will hold meetings about the result. Consider 3 rungs: a better deliverable grounded in the raw inputs that bear on the result; the decision or action it exists to drive; a better way to reach the outcome itself. Choose the highest rung whose benefit a judge can check while the explicit requirements hold. Name the setup it needs (data feeds, a map from builds to commits, machines to reproduce on). When the rung replaces a workflow, pick a comparison that suits the task: a replay on past data, a parallel trial, or a measured pilot. Done when the chosen rung names the outcome, its improvement over the original, its setup, and its judge.

4. **Depth: use the instruments of the best.** Answer for this task:
   - What a top professional would do here that the task does not ask for.
   - The rawest material they start from, in place of the digested summary.
   - The methods and tools they use, by name, and what each does here. For example, a database and a statistical model to test a pattern that a summary table only describes.
   - The judge.

   Then push one move further, the one that improves this task most: test the belief the task rests on from raw evidence; set a hard target well past the stated one; or look for a new finding, proved on evidence not used to find it. For quantitative improvement requests, choose the hard-target move when the task permits it and the approved deliverable can report its result.
   - A hard target: name the metric and write "Aim for [target] using [method]" and treat it as solvable: when one approach stalls, the prompt says to try the next within the owner's budget and deadline before it reports a miss. The owner's bar stays the pass condition. Report stretch attainment separately in the approved format, met or missed. Baseline and target use the same metric under comparable conditions.
   - A new finding: evidence that shaped a revision is development evidence; the prompt confirms the revised claim on evidence not yet used, or leaves it unverified.

   Done when the 4 answers and the move name this task's specifics.

5. **Range: assemble the crew.** Restate the deliverable as verbs, the activities it performs or enables: "a deck" becomes "getting busy people to believe a story about cause and effect, and to decide under uncertainty, in 30 minutes". From the verbs, pick the fields whose methods find what the obvious approach misses. Add a red-team method when it can test a consequential claim or expose a decision risk. Done when each field adds a named method and what it reveals.

6. **Write the output.** The reply holds only these 2 items; steps 1 to 5 are working notes. Size them to the task.
   - The prompt, in one fenced block that stands alone: the chosen goal, with each inferred-goal line starting "Assumption:", the fit lenses' methods and checks, every explicit requirement, the "With my approval only:" lines, first checks for unconfirmed dependencies, and last the judge with its pass condition.
   - The ledger: one line per change, tagged `altitude`, `depth`, or `range`, with its benefit and any scope, cost, risk, or access effect. An `altitude` line names the original outcome and the improved one. Then one line with the skipped lenses and why, and one with the unresolved owner actions.

   Done when the prompt stands alone and the ledger names every change and owner action.

7. **Check, then stop.** Verify the guardrails, each fit lens's completion criterion, and the judge's evidence and pass condition. Keep the ledger aligned with the permitted changes. If no contribution remains, use step 2's unchanged exit. Otherwise return step 6's two items and stop; the owner decides whether to run the prompt.

## Example

`/be-ambitious fix the crash in the login screen`

```text
Fix the reported login crash. Use the raw crash report and device logs to reproduce it, then fix its cause. Write a regression test that fails before the fix and passes after.
With my approval only: investigate and fix other crashes with the same cause.
With my approval only: monitor the release and aim for zero observed recurrences of this cause over 7 days, using regression coverage and crash telemetry.
First verify crash-reporter access and the deployed-build-to-commit map. Name missing dependencies and continue only with work the available artifacts support.
Judge: the regression test goes red then green. For the release stretch, report the observation window, build, login attempts, telemetry coverage, and recurrence count, met or missed. Missing telemetry or no observed login attempts leaves the stretch unverified.
```

- `depth`: raw evidence, reproduction, and a regression test improve the reported fix.
- `altitude`: from the reported crash to fewer same-cause login failures, behind approval.
- Skipped: `range`, no other field's method changes this reproduction and regression check.
- Owner actions: verify crash-reporter access and the build map; approve same-cause work and release monitoring.

Source: Felix Rieseberg, [How to be more ambitious](https://felixrieseberg.com/how-to-be-more-ambitious-a-tutorial-for-humans-with-models/).
