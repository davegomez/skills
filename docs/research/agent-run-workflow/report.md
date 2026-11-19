# Token consumption audit: costo, 2026-11-09 to 2026-11-16

## 1. Method and limits

Data sources (all measured):

- Claude Code session logs: `~/.claude/projects/*/*.jsonl` and `*/subagents/*.jsonl` (with `.meta.json` for the agent type, model, and effort). The window is 7 days, from 2026-11-09T15:50Z. The scan found 13,562 API responses in all projects. Of these, 11,932 are in the 2 costo projects (`-Users-dave-Development-personal-costo` and `...-costo-apps-core`).
- Pi reviewer logs: `~/.pi/agent/sessions/*/*.jsonl`. Pi records the tokens and the list cost for each call.
- Repository files: the orchestration briefs and rules, the agent role files, the skills, and the docs that the agents read.

The scripts are in this folder: `scan.py` (collects), `report.py` and `report2.py` (tables). Run `python3 -I scan.py 7 && python3 -I report.py`.

Limits:

- "Weighted units" are an estimate of relative cost. They use the Anthropic list-price ratios: uncached input 1, cache write (5 min) 1.25, cache write (1 h) 2, cache read 0.1, output 5. They use the same price for all models. The real price of `claude-fable-5-2` relative to `claude-opus-5-5` is not in the logs, so the model split in money is not measured.
- Tool output size is measured in characters. Tokens are about characters / 4 (estimate). Image reads are counted apart, at about 1.6k tokens each (estimate).
- The task classes (build, review, correction) come from the agent `description` text. This is a keyword match, so the class shares are approximate.
- The savings figures in section 4 are estimates from a simulation on the measured per-call data. They are not measured results.

## 2. Breakdown of consumption

### 2.1 Totals (measured)

| Item | Value |
|---|---|
| costo share of all Claude Code weighted units, 7 days | 89.0% (`apps-core` folder 55.9%, root 33.1%) |
| API calls | 11,932 (main 2,590, subagents 9,342) |
| Cache read tokens | 2,136.9M |
| Cache write tokens | 45.4M (5 min 36.2M, 1 h 9.3M) |
| Output tokens | 11.5M (thinking 4.8M) |
| Uncached input tokens | less than 0.1M |
| Weighted units | 334.9M |
| Weighted share | cache read 63.8%, cache write 19.0%, output 17.1% |
| Pi reviews (OpenAI `gpt-6.1-sol`) | 62 sessions, 4,112 calls, 433.6M tokens (420.2M cache read), list cost $82.38 |

### 2.2 By agent type (weighted share of costo)

| Agent | Instances | Share | Calls per instance p50 / p90 / max | Final context p50 / p90 |
|---|---|---|---|---|
| `worker-high` (Opus 5.5) | 82 | 56.8% | 79 / 128 / 332 | 217k / 355k |
| main (orchestrator) | 36 | 28.3% | 13 / 195 / 288 | 66k / 412k |
| `general-purpose` (Opus 5.5 high 9.7%, Sonnet 1.4%) | 36 | 11.8% | 44 / 70 / 90 | 190k / 280k |
| `worker-medium` | 24 | 2.3% | 17 / 36 / 48 | 71k / 118k |
| `Explore` | 4 | 0.5% | 11 / 28 / 63 | 73k / 113k |
| `worker-low` (Haiku 5.5) | 9 | 0.2% | 5 / 5 / 6 | 41k / 46k |

By model: Opus 5.5 75.7%, Fable 5.2 21.9% (main sessions only, effort `high` and `xhigh`), Sonnet 5.5 2.2%, Haiku 5.5 0.2%.

### 2.3 By work stream (measured, weighted share)

- The 10 largest of 36 sessions use 91.7%. 8 of these 10 are Rust core work (handoffs after A7, review3, A9, A10, A11, and the guide reviews).
- Run A10: 38.1M units, 13 commits, 2.9M per commit, 11.4%.
- Run A11: 41.2M units, 13 commits, 3.2M per commit, 12.3%.
- Run A12: 47.4M units, 10 commits, 4.7M per commit, 14.1%.
- The session that holds A8 and A9 (`047a2185`): 65.3M units, 19.5%.

### 2.4 By task class of subagents (approximate, weighted share)

| Class | Share |
|---|---|
| Build (first pass) | 37.3% (`worker-high`) + 4.3% (others) |
| Correction rounds after a review or a failed gate | 16.9% |
| Review agents on the Claude side (Pi is extra) | 5.7% |
| Research and fact checks | 6.1% |
| Device proofs | 4.5% |

### 2.5 What enters the context (measured)

| Tool | Results | Characters | Average | Max |
|---|---|---|---|---|
| `Read`, text | 1,639 | 16.4M (about 4.1M tokens) | 10k | 629k |
| `Read`, images | 349 | about 0.56M tokens (estimate) | n/a | n/a |
| `Bash` | 8,005 | 18.5M (about 4.6M tokens) | 2.3k | 29.7k |
| context-mode | 719 | 3.6M | 5.1k | 41k |
| Chrome | 180 | 1.9M | 10k | 104k |

About 9M tokens of tool output enter the contexts. The logs show 2,137M cache read tokens. Thus, on average, each token in a context is read again about 230 times. The cost driver is the number of calls multiplied by the size of the context. The size of one tool result is a smaller driver.

## 3. Findings

F1. The cost is the context re-read on each call. Cache reads are 63.8% of the weighted units. The main context is 204k tokens at p50 and 451k at p90 (max 714k). The subagent context is 158k at p50 and 299k at p90. Each API call at 200k costs about 20k weighted units before the model writes anything.

F2. Long-lived `worker-high` agents are the largest single cost. 28 of 155 subagents ran more than 100 calls. These 28 agents use 32.9% of all units. Examples: "Build Account Settings revamp" 270 calls, "Device proof two-factor and deletion" 332 calls, "A12 P2b CostoCore object" 160 calls.

F3. The work is serial, and half of it is exploration. Workers send 1.19 tool calls per API call. 46% of worker tool calls only read or search: `grep -n` 937, `sed -n` 781, `cat` 350, `wc -l` 144, plus `Read`. Each serial call re-reads the full context.

F4. Agents read the same large documents again and again. In one session, 10 to 14 different agents read the same guide pages (`docs/architecture/native/02-numbers-and-units.md` by 14 agents, `09-ffi-api.md` by 13). Inside one agent, 382 reads repeat a file that the agent already read. `docs/prd/rust-core.md` (148 KB) was read 44 times. The guide is 550 KB. Workers also read the `rust-architecture` skill references 71 times (19 files, 56 KB of Markdown).

F5. Rework is large. Correction workers use 16.9%. Run A12 had 19 workers. 9 of them were corrections or follow-ups, and phase P3 had 4 correction rounds. Cost per commit went up from 2.9M (A10) to 4.7M (A12).

F6. Reviews run in 2 systems. Claude review agents use 5.7%. Pi ran 62 review sessions with 66 calls each on average, at $82.38 list cost. Some of the Claude reviews used `worker-high`, which is a coding role.

F7. The orchestrator does its own exploration and keeps a very large context. Main sessions used `cat` 118 times, `sed -n` 92, `grep -n` 74, and `rex block` 46 (pane polls). Main calls with a context above 200k use 18.6% of all units. Each run starts from a handoff file, but no restart occurs inside a run.

F8. The role default sends mechanical work to the most expensive role. 88 of 161 spawns were `worker-high`. These include "Fold A12 correction commits", "Write ADR 0042 and records", and correction rounds with the fault already found. `general-purpose` research ran on Opus at high effort (9.7%). Sonnet and Haiku together did 2.4% of the work.

F9. Some instructions increase the work. Each item has a real purpose, but the scope is too wide:
- `~/.claude/agents/worker-high.md`: "Run the full test suite for the code you touched." This conflicts with the memory rule `feedback_targeted_gates.md` (targeted gates for workers, full gates 1 time per branch).
- Spawn prompts: "Read [the brief] in full, then read the rules file that it names in full" (rules files are 7.7 KB to 9.5 KB), and "Invoke the rust-architecture skill before you read or edit code" in each worker.
- Memory rules "read primary docs in full" (`feedback_root_cause_over_patch.md`) and "check current docs before claims, also when a subagent reports it" (`feedback_check_current_docs_before_claims.md`). These cause full-document reads and a second check of the same fact.
- `~/.agents/AGENTS.md`: "Start at `worker-high`", with no rule that sends a correction with a known fix to a lower role.

F10. The fixed prefix is about 34k tokens per worker and 45k per main session at the first call. The re-read of this prefix uses about 13% of all units (estimate from first-call size multiplied by calls). Part of the prefix is not used in costo. The `paper`, `affinity`, `safari-mcp`, `superlogical`, and `blindfold` servers had 0 calls in 7 days, but their instructions and tool names load in each session. `MEMORY.md` is 19.4 KB and loads in each main session. Its exact token share was not measured.

F11. These items are not problems: cache rebuilds above 100k tokens use 3.3%, there were 9 compactions in 7 days, and uncached input is near 0. The prompt cache works.

## 4. Recommendations, ranked by expected impact

Each saving is an estimate. The estimates overlap, so do not add them.

| Code | Change | Finding | Saving (estimate) | Effort | Risk |
|---|---|---|---|---|---|
| A1 | Keep each worker task small: at most about 60 calls. Split a phase into sub-steps at natural boundaries, with a written handoff file. | F1, F2 | up to 15% (simulation: split at 60 calls, 15k handoff) | medium | medium: a new worker can explore again. The handoff file must name the files and decisions. |
| A2 | Cut correction rounds: put the reviewer checklist into the brief, have the worker check its diff against it before the report, and stop at 2 rounds, then ask the owner. | F5 | 6% to 8% (half of the 16.9%) | medium | low: the quality bar stays. It moves earlier. |
| A3 | Put a context pack in each brief: the exact guide sections (path and heading or line range), quoted where short. Tell the worker to use `Grep`, then `Read` with `offset` and `limit`, and never read a full PRD. | F4, F9 | 5% to 10% | low | low: the orchestrator already reads these sections. |
| A4 | Tell workers to send independent reads and searches in 1 response (parallel tool calls). Prefer 1 `grep` with context lines to a `grep` and then a `sed -n`. | F3 | 5% to 10% (exploration calls down by a third) | low | very low |
| A5 | Restart the orchestrator at each phase boundary with the handoff file that the runs already use. Send orchestrator exploration to `Explore` on Sonnet. | F7 | 6% to 8% (simulation: restart every 60 to 100 calls) | low | low: the handoff pattern exists and works. |
| A6 | Change the role rule: a correction with each finding located and the fix stated, a commit fold, and a decision record go to `worker-medium`. Reviews use a reviewer agent, not `worker-high`. | F6, F8 | 2% to 4% | low | medium: watch the correction rate of `worker-medium`. |
| A7 | Run research, fact checks, and file searches on Sonnet at medium effort. Keep design reviews and security paths on Opus. | F8 | 3% to 5% (of the 9.7% Opus `general-purpose`) | low | medium: check the fact-check quality on 1 run first. |
| A8 | Make `worker-high.md` agree with the targeted-gates rule: targeted tests during the task, the full gate 1 time per branch by script. | F9 | 1% to 3% | very low | low: the full gate still runs before the finish. |
| A9 | Remove the costo-unused MCP servers from costo sessions. Move old run entries out of `MEMORY.md`. Measure the prefix with `/context` before and after. | F10 | 2% to 4% | low | very low |
| A10 | Review consolidation: 1 review per phase batch, and the reviewer gets the diff, the brief, and the named guide sections, not the full guide. Track Pi calls per review. | F6 | Pi cost down 30% to 50%; Claude 2% to 3% | low | low |
| A11 | Mark or move the superseded sections of `docs/prd/rust-core.md`, because the guide is the authority over them. | F4 | 1% to 2% | medium | low |

Expected combined effect of A1 to A5: about 25% to 35% fewer weighted units per commit. This is an estimate, and the A13 run must confirm it.

Not recommended:
- Do not lower effort on security paths, concurrency, or design choices.
- Do not drop the Pi review or the TDD rule. They catch faults, and a missed fault costs a correction round, which is the most expensive item here.
- Do not change the main model from Fable 5.2 without a price figure and a quality comparison. The logs do not give the price.

## 5. Implementation plan

Phase 1, before run A13 (instruction changes, low risk): A3, A4, A8, A9, A6.
- Success criteria: tools per API call at or above 1.6 (now 1.19). Exploration share of worker tool calls at or below 35% (now 46%). Repeated in-agent reads at or below 150 per week (now 382). First-call prefix 5k tokens smaller.

Phase 2, during run A13 (workflow changes): A1, A2, A5, A7.
- Success criteria: worker calls p50 at or below 50 (now 79). Worker final context p50 at or below 150k (now 217k). Correction share at or below 8% (now 16.9%). Units per commit at or below 2.5M (A10 2.9M, A11 3.2M, A12 4.7M).

Phase 3, after A13: A10, A11, and a decision on A7 from the A13 data.

Quality guardrails (all phases): all gates pass at the finish, high-severity review findings per phase do not increase, and there are no reopened tickets or regressions after a finish. If a guardrail fails, revert the last change before you continue.

## 6. Tracking method

- Run `scan.py 7` and `report.py` 1 time per week and at the end of each run. Add 1 row per run to a CSV.
- Metrics for each run: weighted units per commit, correction share, review share, worker calls p50 and p90, worker final context p50, tools per API call, exploration share, repeated reads, Pi calls and list cost, and the quality guardrails above.
- Name each spawn with the run and phase in `description` (this is the current practice, for example "A12 P3 review corrections"). The scripts group by this text.
- Compare A13 against the A10 to A12 baseline in section 2.3. One run is a small sample, so make the final decision after 2 runs.
