---
name: be-ambitious
description: Rewrite a task or prompt to aim higher in altitude, depth, and range, checked by an outside judge.
disable-model-invocation: true
---

# Be ambitious

Rewrite the owner's task so the model that runs it aims at the goal beyond the goal, works with the instruments of the best in the field, and borrows methods from fields the task does not name. Each change makes the work deeper, not bigger. The product is one rewritten prompt and a ledger. The owner reads them and decides what to run; the rewrite grants no new authority.

## The judge

A **judge** supplies evidence beyond the model's own verdict: a test that goes red then green, a benchmark, a reproduction, a measurement, held-out data, or a qualified independent reviewer with a rubric. Best is a tool the model can run for feedback at once. Every rewritten prompt ends with its judge and an observable pass condition. The prompt asks for measured results where the work is quantitative and documented findings where it is qualitative. When the judge needs access that is not confirmed, the prompt checks that access first and reports the result as unverified until the judge runs.

## Guardrails

- Preserve every explicit requirement in the prompt: scope, deliverable, format, approvals, security, budget, deadline. Keep any required literal text unchanged.
- Work above the approved scope, a paid or irreversible step, and new access sit inside the prompt behind owner approval.
- A field contributes its methods and tools; the prompt names what the method does.
- Treat unconfirmed data, tools, and access as dependencies to check. Distinguish proposed findings from observed evidence.

## Steps

1. **Read the task.** Use the task given with the invocation, else the unambiguous recent task. When neither exists, ask which task to make more ambitious and stop. Name the intended result and who acts on it. List the explicit requirements. Mark each inferred goal as an assumption. Done when the result, its user, the requirements, and the assumptions are written down.

2. **Pick the lenses.** Mark each lens fit or skipped, with a one-line reason tied to this task. Run steps 3 to 5 only for the lenses marked fit. Done when all three are marked.

   | Lens | Usually fits | Usually skipped |
   |---|---|---|
   | Altitude | The deliverable serves an outcome; people will hold meetings about it | Creative work that is its own outcome |
   | Depth | The work should be done really well | Throwaway work |
   | Range | The result must land with people, or the obvious field has run out of ideas | A narrow fix with one right answer |

3. **Altitude: climb the ladder.** Ask "what should happen next?" of the deliverable, then of each answer. Consider 3 rungs: a better deliverable grounded in the raw inputs that bear on the result; the decision or action it exists to drive; a better way to reach the outcome itself. Choose the highest rung whose benefit a judge can check while preserving the explicit requirements. Name the setup it needs (data feeds, a map from builds to commits, machines to reproduce on). When the rung replaces a workflow, pick a comparison that suits the task: a replay on past data, a parallel trial, or a measured pilot. Done when the chosen rung names the outcome, its improvement over the original task, its setup, and its judge.

4. **Depth: use the instruments of the best.** Answer for this task:
   - What a top professional would do here that the task does not ask for.
   - The rawest material they start from, in place of the digested summary.
   - The methods and tools they use, by name, and what each does here. For example, a database and a statistical model to test a pattern that a summary table only describes.
   - The judge.

   Then push one move further, the one that improves this task most: test the belief the task rests on from raw evidence; set a hard target well past the stated one; or look for a new finding, proved on evidence not used to find it. For a hard target, write "Aim for [target] using [method]" and treat it as solvable: when one approach stalls, the prompt says to try the next before it reports a miss. Pursue it within the owner's budget and deadline. The owner's own bar stays the pass condition, and the prompt asks for the measured result even when the target is missed. Done when the 4 answers and the move name this task's specifics.

5. **Range: assemble the crew.** Restate the deliverable as verbs, the activities it performs or enables: "a deck" becomes "getting busy people to believe a story about cause and effect, and to decide under uncertainty, in 30 minutes". From the verbs, pick the fields whose methods find what the obvious approach misses. Add a red-team method when it can test a consequential claim or expose a decision risk. Done when each field adds a named method and what it reveals.

6. **Write the output.**
   - The prompt, in one fenced block that stands alone: the chosen goal, the selected lenses' methods and checks, every explicit requirement, approval gates for added scope, first checks for unconfirmed data, tools, and access, and last the judge with its pass condition. Label inferred goals as assumptions inside the prompt.
   - The ledger: one line per change, tagged `altitude`, `depth`, or `range`, with its benefit and any scope, cost, risk, or access effect. The `altitude` line names the original task and the chosen outcome. Then one line: the skipped lenses and why. Include material unresolved owner actions, such as access, sensitive-data clearance, or approval.

   Done when the prompt stands alone and the ledger exposes every change and unresolved owner action.

7. **Check, then stop.** Check all three lens decisions. When no lens improves the outcome, the method, or the judge while preserving the explicit requirements, return the task unchanged with one line on why. Otherwise check that every explicit requirement survives, each selected lens meets its completion criterion, each ledger line identifies an improvement, and the prompt ends with its judge and pass condition. Confirm that approval gates and material dependency checks are inside the prompt and that proposed findings remain distinct from observed evidence. Done when the applicable checks pass. Return the output and stop; the owner decides whether to run it.

## Example

`/be-ambitious fix the crash in the login screen`

```text
Fix the reported login crash. Use the raw crash report and device logs to reproduce it, then fix its cause. Write a regression test that fails before the fix and passes after.
With my approval only: investigate and fix other crashes with the same cause. If release monitoring is also approved, aim for zero observed recurrences of this cause over 7 days using regression coverage and crash telemetry. This monitoring checks the proposed goal of reducing repeat login failures.
First verify crash-reporter access and the deployed-build-to-commit map. Name missing dependencies and continue only with investigation and tests supported by available artifacts. Keep release validation unverified until monitoring runs.
Judge: the regression test goes red then green. For the release stretch, report the observation window, build, login attempts, telemetry coverage, and recurrence count, including a missed target. Missing telemetry or no observed login attempts leaves the stretch unverified.
```

- `depth`: raw evidence, reproduction, and a regression test improve the reported fix.
- `altitude`: the reported crash to reducing same-cause failures, with owner-approved investigation and monitoring.
- Skipped: `range`, no additional field's method is needed for this reproduction and regression check.
- Owner actions: verify crash-reporter access and the deployed-build map; approve same-cause work and release monitoring.

Source: Felix Rieseberg, [How to be more ambitious](https://felixrieseberg.com/how-to-be-more-ambitious-a-tutorial-for-humans-with-models/).
