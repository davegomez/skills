# ios-architecture eval harness

Runs the agreed design ([DESIGN.md](DESIGN.md)) on the cases of [CASES.md](CASES.md): old skill (`0ab47d0`) against the frozen new skill, with a no-skill control. Python 3, stdlib only. Run every command from this folder with `python3 -I`.

| File | Job |
| --- | --- |
| `config.json` | Pins: builder model and effort, fallback models, Claude Code version, Jev model and price, caps, stages, simulator, reviewers. |
| `runner.py` | Freezes the arms, checks isolation, runs 1 run or a ledgered batch, grades each run. |
| `grade.py` | Hidden grader on a copy of the result; new `scripts/check` as a separate diagnostic. |
| `review.py` | Blind review pack, tools-off Pi reviewer, second adjudication pass. |
| `report.py` | Stage report. |
| `preflight.py` | The 4 preflight checks of a case folder. |
| `gates/route`, `gates/check`, `gates/scaffold-sim` | Layer 2 offline gates for later skill changes. |
| `tests/test_eval.py` | Offline tests: fake `claude`, `curl`, and `pi` drive the whole pilot on toy cases. |

Output goes to `runs/` (`runs/arms/`, `runs/<stage>/`, `runs/isolation/`, `runs/preflight/`, `runs/gates/`).

## Setup

1. Xcode, `jq`, `git`, and Claude Code at the version pinned in `config.json` (`claude --version`).
2. Grading needs no simulator setup. Each grading run (and `gates/scaffold-sim`) waits for a machine-wide queue (`/tmp/ios-eval-grade.lock`), then runs on a new simulator, `ios-eval-grader-<pid>`, which is deleted afterwards; leftovers from a killed run are deleted when the next one starts. The device type is `simulator.device_type` in `config.json` unless the case sets `toolchain.simulator_device_type`; the runtime is `simulator.runtime`.
3. Pi reviewer: `mkdir -p /tmp/pi-clean-agent && ln -sf ~/.pi/agent/auth.json /tmp/pi-clean-agent/auth.json`, plus a `settings.json` with the default model. The clean folder keeps `~/.pi/agent/APPEND_SYSTEM.md` out of reviews.
4. TypeSafe key for the new arm: `TYPESAFE_API_KEY` in the environment, or the Keychain item `typesafe-api-key`. The harness passes it to the new arm only, as an environment variable, and replaces it with `[REDACTED]` in every file it writes.

## Before any paid run (free, offline)

```sh
python3 -I tests/test_eval.py                 # harness tests
python3 -I preflight.py cases/I03             # each case, before it is frozen
gates/route; gates/check; gates/scaffold-sim  # gates; scaffold-sim builds and tests on a simulator (minutes)
python3 -I runner.py freeze                   # once, after the C1 fixes: arms and their sha256 manifest
python3 -I runner.py isolation                # dry run: what the builder can discover, per arm
```

`isolation` starts each arm's builder session exactly as a run does, sends only `/context` (a local command, cost 0), and lists cwd, model, tools, plugins, MCP servers, skills, memory files, environment variable names, sandbox settings, and the host policy probes. Every verdict must be true. `isolation --live` also asks the small fallback model to run fixed shell probes, each with the outcome it must have in that arm (`live_probes()` in `runner.py`): denied for the home folder, the repository, `runs/`, `/tmp`, `/Volumes`, any network host but Jev, a write into the skill, and an unsandboxed non-build command; allowed for a write and read in cwd and `$TMPDIR`, `git status`, the neutral git config, the skill folder, `swift --version`, then in the sandbox `swift build` and `swift test` in a tiny package that the harness writes to the work folder (`ProbeKit`), `xcodebuild -version` twice, and `xcodebuild build` of that package for the run's simulator, then an unsandboxed `xcodebuild -version`; in the new arm, `scripts/route --help` and 1 real `scripts/decide` on a synthetic file, which must return a Jev result of `jev.model`. The verdict parses each tool result and fails on any mismatch; the result goes to `runs/isolation/probe.json`. `batch` and `run` refuse to start unless the last live probe passed for the frozen arms on the pinned claude. It is paid (cap $0.05 per arm, 1 Jev call) and needs approval.

Then set in `config.json`, from a verified source: `jev.model` (the response model of 1 `scripts/decide` call; the batch halts when a run observes another) and `jev.usd_per_call` (current price). The batch refuses new-arm runs until both are set.

## Pilot (cap $20, owner approval)

```sh
python3 -I runner.py batch pilot --approved-cap 20
python3 -I review.py pack pilot
python3 -I review.py review pilot
python3 -I review.py adjudicate pilot
python3 -I report.py pilot                    # runs/pilot/report.md
```

The pilot is 1 old/new pair per case (12 runs); the review case runs its clean variant. The plan is drawn once (random old/new order) and frozen in `runs/pilot/plan.json` with the hash of each case; the batch refuses to run if a case changes. Rerunning `batch` resumes: it skips finished units.

## Pilot 2 (cap $8, owner approval)

`pilot2` runs only the new arm: 1 run per case, block `pilot2`, each case on the variant of `runs/pilot/plan.json`. The tasks of I03-I06 have 1 added sentence. Before it, move `runs/arms` aside, `freeze` again for the latest skill, and pass `isolation --live`.
Run `python3 -I runner.py batch pilot2 --approved-cap 8`, then `review.py pack`, `review`, and `adjudicate` with stage `pilot2`. The ledger counts the first pilot's spend against `caps.total_usd`.
`python3 -I report.py pilot2 --old-from pilot` pairs each new run with the first pilot's old run of the same case and variant and writes `runs/pilot2/report-old-from-pilot.md`.

## Pilot 3 (cap $3, owner approval)

`pilot3` runs only the new arm on I03 (stage `cases`), block `pilot3`, on the variant of `runs/pilot/plan.json`: the first run in which the builder can build and test its work (see Known limit). Pass `isolation --live` first, then run `python3 -I runner.py batch pilot3 --approved-cap 3`. The ledger counts pilot and pilot2 against `caps.total_usd`.

## How a run works

- Cwd `/Users/Shared/iosev/w/work`: a fresh copy of `fixture/`, `git init`, 1 commit; the review case applies its variant diff as uncommitted changes. A case with an empty fixture starts in an empty folder, with the repository in `/Users/Shared/iosev/w` (the sandbox can read and write that `.git`). The prompt is `task.md`, byte for byte.
- The skill is plugin `skills` at `/Users/Shared/iosev/plugin` (`skills:ios-architecture`), the same path for both arms; the control has none. The installed copy is checked against the frozen manifest before and after the run.
- `claude -p --restricted --strict-mcp-config --setting-sources project --no-session-persistence`, stream-json, pinned model and effort, `--max-budget-usd`. Restricted mode loads no CLAUDE.md, memory, hooks, or user skills. The fallback models are pinned through `ANTHROPIC_DEFAULT_HAIKU_MODEL` and `ANTHROPIC_DEFAULT_SONNET_MODEL`; exit 4 is decided by the builder itself, as the skill says.
- The environment is minimal: no harness variables, `ZDOTDIR` on an empty folder (no user shell files), a neutral git config, a private `CLAUDE_CODE_TMPDIR` (`/Users/Shared/iosev/t`), and `CFFIXED_USER_HOME` on `/Users/Shared/iosev/h`, so Xcode and SwiftPM put DerivedData and their caches there, not in the home folder.
- Build tools: shims on `PATH` (`write_tool_shims()`) switch off the sandboxes that SwiftPM and the Swift compiler nest around manifests and macros (the OS sandbox forbids a nested `sandbox-exec`; the code still runs in the OS sandbox), and point `xcodebuild` and `xcrun simctl` at the run's own device set. The harness creates 1 simulator in that set, named after its device type (`simulator.device_type`, or the case's `toolchain.simulator_device_type`), and deletes it after the run.
- Bash runs in the OS sandbox: no reads of the home folder, the repository, `runs/`, `/tmp`, or `/Volumes`; the run's folders sit outside all of them, because a denied `/tmp` blocks every path spelled through that symlink even with `allowRead`; writes in cwd, the repository's `.git`, tmp, the tool home, and the per-user temp folder (`getconf DARWIN_USER_TEMP_DIR`: xcodebuild and Swift Build write there whatever `TMPDIR` says); Mach lookups to `com.apple.CoreSimulator.*`; network only to `api.typesafe.ai` in the new arm. The free dry run shows these settings; only `isolation --live` shows the sandbox enforces them. The host answers each permission prompt (`policy()` in `runner.py`): file tools only inside the run's folders; outside the sandbox only 1 `xcodebuild` command per call, optionally with `2>&1` and 1 pipe into `tail`, `head`, or `grep`, and no `$`, `;`, `&&`, `cd`, `..`, `~`, or path outside the run's folders. That path exists for simulator tests only; the denial says so.
- A `curl` shim on `PATH` logs URL, HTTP status, exit, and time of each call (never headers or bodies) and refuses Jev calls past `jev.max_calls_per_run`.
- Wall cap 15 minutes. Timeout and budget stops are attempted runs. A provider or auth error, a missing or changed skill, a wrong model, an undelivered prompt, a shared tmp, or a grader failure invalidates the block; it is retried once and then listed as invalid. Every attempt keeps its cost.
- Ledger `runs/<stage>/ledger.jsonl`: before a unit starts, its worst case (`caps.run_reserve_usd` per run, plus 2 requests per allowed Jev call for the new arm) must fit the stage cap, the total ceiling, and the machine hours; otherwise the batch halts. An unknown run cost counts as a full reserve.

## Grading

`hidden/grade.sh <copy> <out.json>` runs on a copy of the result outside the run folder, with the environment that [CASES.md](CASES.md) lists (`EVAL_SIM`, `EVAL_FINAL_TEXT`, `EVAL_VARIANT`). `grade.json` records `grade_s`, the time of the grade itself without the wait in the queue. Executable acceptance: no critical check fails and at least 1 passes; a review case's grader decides whether the tree holds only the review. Final acceptance also needs no critical failure in the final blind review. `diagnostic.json` holds new `scripts/check` (project and changed files, Jev blocked) and is never read by the grade.

## Review

`pack` writes each valid run as `<case>/d<8 hex>.md` (test results, then the patch and the final message; for a review case, the diff under review, the files the reviewer wrote, from `review.diff`, and the final message) in `/tmp/iosev-review/<stage>/`, in random order; the key and the preselected adjudication sample stay in `runs/<stage>/review/key.json`. `review` runs 1 fresh Pi per item, tools off, with the case's `rubric.md` and `task.md`. `adjudicate` sends critical fails, incomplete or unverified items, and the sample to a second model, which sees the first lines and decides the final result.

## Known limit: builders verify their work only in part (F38)

In pilot and pilot2, the builder's sandbox blocked its own verification. In the pilot2 I02 run, `xcodebuild build-for-testing` failed while fetching packages (`permissionDenied`), `swift test` failed while compiling `Package.swift`, and `xcodebuild test` lost the simulator service. The host refused both unsandboxed retries because of their shell syntax (`$(...)`, `&&`, `|`, `$TMPDIR`), but its message said that only 1 build command may run, so the builder stopped trying. So a builder could hand in code that never compiled: in pilot2 I02, one test called an internal default initializer; with `@testable import`, the 14 new tests ran and passed. Both arms had the same limits, so the old/new comparison of pilot and pilot2 stays fair, but their absolute pass rates are probably lower than in real use.

Causes, found on a copy of Claude Code's Seatbelt profile (`sandbox-exec`):
- SwiftPM and xcodebuild read and write `~/Library/Caches/org.swift.swiftpm` and `~/Library/org.swift.swiftpm`, which the home denial blocks.
- SwiftPM wraps manifest compilation, and swiftc wraps macro plugins, in their own `sandbox-exec`; a nested sandbox fails (`sandbox_apply: Operation not permitted`), which shows as `Invalid manifest` or a malformed `swift-plugin-server` response.
- xcodebuild, Swift Build, and Foundation write to the per-user temp folder (`/var/folders/.../T`), not `$TMPDIR`.
- The profile allows only 14 Mach services, so CoreSimulator is unreachable.

Fixed since pilot3 (`isolation --live` checks each in every arm): package resolution, `swift build` and `swift test` in a package, and `xcodebuild build` and `build-for-testing` for a simulator all run in the sandbox, as often as the builder wants. I02's workspace and I03's app build for testing there. Caches and DerivedData stay in the run's folders. Simulator tests run through the host-approved unsandboxed path: 1 `xcodebuild` command per call, on the run's own simulator.

Still different from a real session:
- The sandbox gives no pseudo-terminal (Claude Code 2.1.327 has no setting for one), so `xcodebuild test` on a simulator cannot run in it; with a pseudo-terminal allowed in a copy of the profile, the test still hung, for a reason not found. The builder must set `dangerouslyDisableSandbox` and write the command without `$`, `&&`, or `cd`.
- The shims change only `xcodebuild`, `swift`, and `xcrun` as found on `PATH`; `/usr/bin/xcodebuild` and `xcrun swift build` bypass them and fail as before.
- The builder sees only its own simulator, named after its device type; the user's simulators and Xcode preferences are not visible.
- The builder's code that runs in the simulator (tests, the app), an unsandboxed xcodebuild (build phases, `Package.swift`), and CoreSimulator act outside the OS sandbox, as in pilot and pilot2. The denials of the live probe hold for shell commands, not for that code.
- The per-user temp folder is writable and readable by the builder; other apps of the same user keep temp files there.

## Not covered

No 95% interval for the paired difference; no replay cache for `check` decisions; Pi reviewer cost is not measured (subscription).
