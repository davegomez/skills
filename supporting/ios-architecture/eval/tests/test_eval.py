"""Offline tests of the eval harness: a fake claude, curl transport, and Pi drive the pilot on toy cases.
  python3 -I tests/test_eval.py            (from eval/; needs git and Xcode's python3 at /usr/bin)
"""
import json, os, re, shutil, subprocess, sys, tempfile, unittest
from pathlib import Path

EVAL = Path(__file__).resolve().parents[1]
TESTS = EVAL / "tests"
KEY = "test-key-0123456789abcdef"
sys.path.insert(0, str(EVAL))


class Env:
    """An isolated harness environment: own HOME, OUT, scratch, config, and fakes."""
    n = 0

    def __init__(self, fake: dict, **cfg_changes):
        Env.n += 1
        self.root = Path(tempfile.mkdtemp(prefix="iosev-test-"))
        self.home, self.out = self.root / "home", self.root / "out"
        self.scratch = Path(f"/tmp/iosevt{os.getpid()}-{Env.n}")
        shutil.rmtree(self.scratch, ignore_errors=True)
        self.home.mkdir()
        (self.home / "fake-claude.json").write_text(json.dumps(fake))
        (self.root / "pi-agent").mkdir(); (self.root / "pi-agent" / "auth.json").write_text("{}")
        c = json.loads((EVAL / "config.json").read_text())
        c["jev"] |= {"model": "jev-test-1", "usd_per_call": 0.01}
        c["simulator"] |= {"udid": "TEST-SIM"}
        c["caps"] |= {"wall_s": 60, "grade_s": 60}
        c["pi_agent_dir"] = str(self.root / "pi-agent")
        for k, v in cfg_changes.items():
            node = c
            *path, last = k.split(".")
            for p in path: node = node[p]
            node[last] = v
        (self.root / "config.json").write_text(json.dumps(c))
        self.env = {k: v for k, v in os.environ.items() if not k.startswith(("IOS_EVAL_", "TYPESAFE_"))} | {
            "HOME": str(self.home), "IOS_EVAL_CONFIG": str(self.root / "config.json"), "IOS_EVAL_CASES": str(TESTS / "fixtures/cases"),
            "IOS_EVAL_OUT": str(self.out), "IOS_EVAL_SCRATCH": str(self.scratch), "IOS_EVAL_PACK": str(self.root / "pack"),
            "IOS_EVAL_CLAUDE": str(TESTS / "bin/claude"), "IOS_EVAL_REAL_CURL": str(TESTS / "bin/real-curl"),
            "IOS_EVAL_PI": str(TESTS / "bin/pi"), "TYPESAFE_API_KEY": KEY,
            "IOS_EVAL_GRADE_LOCK": str(self.root / "grade.lock")}

    def run(self, *args, ok=True) -> subprocess.CompletedProcess:
        script = EVAL / args[0] if not args[0].startswith("gates/") else EVAL / args[0]
        cmd = [sys.executable, "-I", str(script), *args[1:]]
        r = subprocess.run(cmd, capture_output=True, text=True, env=self.env, timeout=600)
        if ok and r.returncode: raise AssertionError(f"{args} exit {r.returncode}\n{r.stdout[-3000:]}\n{r.stderr[-3000:]}")
        return r

    def freeze(self, probe=True):
        """Freeze the arms; with probe, record a passed live sandbox probe for them (the fake claude cannot run one)."""
        self.run("runner.py", "freeze")
        if probe: self.probe_record(True)

    def probe_record(self, passed, sha=None):
        import hashlib
        sha = sha or hashlib.sha256((self.out / "arms/MANIFEST.json").read_bytes()).hexdigest()
        (self.out / "isolation").mkdir(parents=True, exist_ok=True)
        (self.out / "isolation/probe.json").write_text(json.dumps({"passed": passed, "arms_manifest_sha256": sha,
                                                                   "claude_version": json.loads((self.root / "config.json").read_text())["claude_version"]}))

    def ledger(self, stage="pilot"):
        return [json.loads(x) for x in (self.out / stage / "ledger.jsonl").read_text().splitlines()]

    def meta(self, rid, stage="pilot"):
        return json.loads((self.out / stage / "runs" / rid / "meta.json").read_text())

    def close(self):
        shutil.rmtree(self.root, ignore_errors=True); shutil.rmtree(self.scratch, ignore_errors=True)


def all_text(root: Path) -> str:
    return "".join(p.read_text(errors="replace") for p in root.rglob("*") if p.is_file() and p.suffix != ".tgz")


class PilotDryRun(unittest.TestCase):
    """The whole pilot, offline: freeze, isolation, batch with grading, review pack, review, adjudication, report."""

    @classmethod
    def setUpClass(cls):
        cls.e = Env({"jev_model": "jev-test-1"})
        e = cls.e
        e.freeze()
        cls.iso = e.run("runner.py", "isolation", "--case", "T00")
        cls.batch = e.run("runner.py", "batch", "pilot", "--approved-cap", "20")
        e.run("review.py", "pack", "pilot"); e.run("review.py", "review", "pilot"); e.run("review.py", "adjudicate", "pilot")
        cls.report = e.run("report.py", "pilot").stdout
        cls.batch2 = e.run("runner.py", "batch", "pilot2", "--approved-cap", "8")
        e.run("review.py", "pack", "pilot2"); e.run("review.py", "review", "pilot2"); e.run("review.py", "adjudicate", "pilot2")
        cls.cross = e.run("report.py", "pilot2", "--old-from", "pilot").stdout

    @classmethod
    def tearDownClass(cls):
        cls.e.close()

    def test_arms_frozen_with_manifest(self):
        man = json.loads((self.e.out / "arms/MANIFEST.json").read_text())
        self.assertIn("SKILL.md", man["old"]["files"])
        self.assertFalse(any(f.startswith("scripts/") for f in man["old"]["files"]), "the old arm has no scripts")
        self.assertTrue(any(f.startswith("scripts/") for f in man["new"]["files"]))

    def test_isolation_dry_run(self):
        iso = json.loads((self.e.out / "isolation/isolation.json").read_text())
        for arm, r in iso["arms"].items():
            self.assertTrue(all(r["verdict"].values()), (arm, r["verdict"]))
            self.assertNotIn("TYPESAFE_API_KEY", r["env_names"]) if arm != "new" else self.assertIn("TYPESAFE_API_KEY", r["env_names"])
            self.assertNotIn("IOS_EVAL_OUT", r["env_names"])
        self.assertTrue(all(p["ok"] for p in iso["policy_probes"]))
        self.assertEqual(iso["arms"]["new"]["sandbox"]["network"]["allowedDomains"], ["api.typesafe.ai"])
        self.assertEqual(iso["arms"]["old"]["sandbox"]["network"]["allowedDomains"], [])

    def test_units_valid_and_pairs_ordered(self):
        units = [x for x in self.e.ledger() if x["kind"] == "unit"]
        self.assertEqual(sorted(u["unit"] for u in units), ["R00-p1", "T00-p1"])
        self.assertTrue(all(u["status"] == "valid" for u in units))
        plan = json.loads((self.e.out / "pilot/plan.json").read_text())
        self.assertEqual({u["variant"] for u in plan["units"] if u["case"] == "R00"}, {"clean"})
        self.assertTrue(all(sorted(u["arms"]) == ["new", "old"] for u in plan["units"]))

    def test_run_fields(self):
        m = self.e.meta("T00-p1-new")
        for k in ("start", "stop", "wall_s", "cost_usd", "usage", "model_usage", "hashes", "pins", "stop_reason", "tool_calls_by_name",
                  "script_runs", "decide_results", "pending_lines", "jev_calls", "jev_models_observed", "build_test_s", "script_wait_s"):
            self.assertIn(k, m)
        self.assertTrue(m["prompt_delivered"])
        self.assertEqual(m["jev_calls"], 1)
        self.assertEqual(m["jev_models_observed"], ["jev-test-1"])
        self.assertEqual(m["pending_lines"]["fallback"], 1)
        self.assertEqual(m["script_runs"], {"decide": 1, "check": 1})
        self.assertEqual(m["files_changed"], ["greet.txt", "notes.txt"])
        self.assertEqual(self.e.meta("T00-p1-old")["jev_calls"], 0)

    def test_key_reaches_transport_and_never_logs(self):
        self.assertIn("header=yes", (self.e.home / "curl-seen.txt").read_text())
        self.assertGreaterEqual(self.e.meta("T00-p1-new")["redactions"], 1)
        for root in (self.e.out, self.e.root / "pack"):
            self.assertNotIn(KEY, all_text(root))
        self.assertEqual(self.e.meta("T00-p1-new")["key_in_result"], 1)
        import tarfile
        with tarfile.open(self.e.out / "pilot/runs/T00-p1-new/result.tgz") as tar:
            self.assertFalse(any(KEY.encode() in tar.extractfile(m).read() for m in tar.getmembers() if m.isfile()))
        log = (self.e.out / "pilot/runs/T00-p1-new/curl.log").read_text()
        self.assertRegex(log, r"^time=\S+ host=api.typesafe.ai url=https://api.typesafe.ai/v1/systemone status=200 exit=0 seconds=\d+\n$")

    def test_host_policy_denied_outside_read(self):
        m = self.e.meta("T00-p1-old")
        self.assertTrue(any(".claude/CLAUDE.md" in d["file_path"] for d in m["host_denials"]))

    def test_grades_and_diagnostic_apart(self):
        g = lambda rid: json.loads((self.e.out / "pilot/runs" / rid / "grade.json").read_text())
        self.assertTrue(g("T00-p1-new")["accepted_exec"])
        self.assertFalse(g("T00-p1-old")["accepted_exec"])
        self.assertEqual(g("T00-p1-old")["critical_failed"], ["T00-greeting"])
        self.assertTrue(g("R00-p1-new")["accepted_exec"])
        d = json.loads((self.e.out / "pilot/runs/T00-p1-new/diagnostic.json").read_text())
        self.assertIn("never part of the grade", d["note"])
        self.assertNotIn("diagnostic", json.dumps(g("T00-p1-new")))

    def test_review_pack_is_blind(self):
        key = json.loads((self.e.out / "pilot/review/key.json").read_text())
        pack = Path(key["pack"])
        self.assertFalse((pack / "key.json").exists())
        text = all_text(pack)
        for word in ("T00-p1-", "R00-p1-", '"arm"', str(self.e.out)):
            self.assertNotIn(word, text)
        self.assertEqual(len(key["items"]), 4)
        self.assertTrue(all(re.fullmatch(r"d[0-9a-f]{8}", n) for n in key["items"]))
        # adjudication: the critical review fail plus the preselected sample
        second = {p.stem for p in (self.e.out / "pilot/review/pass2").glob("*.json")}
        bad = next(n for n, v in key["items"].items() if v["run"] == "T00-p1-old")
        self.assertIn(bad, second)
        self.assertTrue(set(key["sample"]) <= second)

    def test_report(self):
        self.assertIn("New only: 1. Old only: 0.", self.report)
        self.assertIn("p = 1.0000", self.report)
        self.assertIn("## Clean-diff review stratum", self.report)
        self.assertRegex(self.report, r"\| R00-p1-(old|new) \| (old|new) \| yes \|")
        self.assertIn("Jev response models observed: jev-test-1.", self.report)
        self.assertIn("## check diagnostic", self.report)

    def test_new_only_stage_plans_1_run_per_unit_like_the_pilot(self):
        plan = json.loads((self.e.out / "pilot2/plan.json").read_text())
        first = {u["case"]: u["variant"] for u in json.loads((self.e.out / "pilot/plan.json").read_text())["units"]}
        self.assertTrue(all(u["arms"] == ["new"] and u["block"] == "pilot2" for u in plan["units"]))
        self.assertEqual({u["case"]: u["variant"] for u in plan["units"]}, first)
        led = self.e.ledger("pilot2")
        self.assertEqual(sorted(r for x in led if x["kind"] == "unit" for r in x["runs"]), ["R00-pilot2-new", "T00-pilot2-new"])
        # 1 new run reserved, not a pair: 1.5 + 30 calls x 2 x $0.01
        self.assertTrue(all(abs(x["usd"] - 2.1) < 1e-9 for x in led if x["kind"] == "reserve"), [x for x in led if x["kind"] == "reserve"])
        self.assertEqual(len(json.loads((self.e.out / "pilot2/review/key.json").read_text())["items"]), 2)

    def test_cross_stage_report_pairs_by_case(self):
        self.assertIn("old runs from pilot", self.cross)
        self.assertIn("Old runs come from stage pilot", self.cross)
        self.assertIn("1 added sentence", self.cross)
        self.assertIn("Pairs: 1, with both reviews done: 1. Both accepted: 0. New only: 1.", self.cross)  # T00; R00 is clean
        self.assertIn("| T00-pilot2-new | new |", self.cross)
        self.assertIn("| T00-p1-old | old |", self.cross)
        self.assertNotIn("T00-p1-new", self.cross)
        self.assertTrue((self.e.out / "pilot2/report-old-from-pilot.md").exists())

    def test_review_run_keeps_the_reviewers_change_apart(self):
        run = self.e.out / "pilot/runs/R00-p1-new"
        self.assertEqual((run / "review.diff").read_text(), "")  # the toy reviewer writes no file
        self.assertIn("+log(count)", (run / "patch.diff").read_text())  # the clean diff under review


class LedgerAndInvalid(unittest.TestCase):
    def setUp(self):
        self.e = None

    def tearDown(self):
        if self.e: self.e.close()

    def test_halts_when_next_pair_does_not_fit(self):
        # 1 pair reserves 1.5 + (1.5 + 30 calls x 2 x $0.01) = $3.60; after the first pair ($0.82) the next does not fit in $4
        self.e = Env({"jev_model": "jev-test-1"}, **{"stages.pilot.cap_usd": 4.0})
        self.e.freeze()
        out = self.e.run("runner.py", "batch", "pilot", "--approved-cap", "4").stdout
        self.assertIn("HALT", out)
        led = self.e.ledger()
        self.assertEqual(sum(x["kind"] == "unit" for x in led), 1)
        halt = next(x for x in led if x["kind"] == "halt")
        self.assertIn("> cap $4.00", halt["reason"])
        self.assertLessEqual(sum(x["usd"] for x in led if x["kind"] == "settle"), 4.0)

    def test_batch_needs_the_configured_cap(self):
        self.e = Env({})
        self.e.freeze()
        r = self.e.run("runner.py", "batch", "pilot", "--approved-cap", "25", ok=False)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("approved-cap", r.stderr)

    def test_paid_runs_need_a_passed_live_probe_of_the_frozen_arms(self):
        self.e = Env({"jev_model": "jev-test-1"})
        self.e.freeze(probe=False)
        for setup in (lambda: None, lambda: self.e.probe_record(False), lambda: self.e.probe_record(True, sha="0" * 64)):
            setup()
            for args in (("batch", "pilot", "--approved-cap", "20"), ("run", "pilot", "T00", "old", "g1")):
                r = self.e.run("runner.py", *args, ok=False)
                self.assertNotEqual(r.returncode, 0)
                self.assertIn("live sandbox probe", r.stderr)
        self.assertFalse((self.e.out / "pilot/ledger.jsonl").exists(), "no run started")

    def test_invalid_block_retried_once_and_listed(self):
        self.e = Env({"old": {"mode": "autherror"}, "jev_model": "jev-test-1"})
        self.e.freeze()
        self.e.run("runner.py", "batch", "pilot", "--approved-cap", "20")
        led = self.e.ledger()
        self.assertEqual(sum(x["kind"] == "invalid" for x in led), 4)  # 2 units x 2 attempts
        self.assertTrue(all(x["status"] == "invalid" for x in led if x["kind"] == "unit"))
        self.assertEqual(sum(x["kind"] == "settle" for x in led), 8)  # invalid attempts keep their cost
        self.assertIn("provider_error", json.dumps([x for x in led if x["kind"] == "invalid"]))
        self.assertTrue((self.e.out / "pilot/runs/T00-p1-old-r2/meta.json").exists())

    def test_jev_model_drift_halts(self):
        self.e = Env({"jev_model": "jev-other"})
        self.e.freeze()
        out = self.e.run("runner.py", "batch", "pilot", "--approved-cap", "20").stdout
        self.assertIn("HALT: Jev model drift", out)
        self.assertEqual(sum(x["kind"] == "unit" for x in self.e.ledger()), 0)

    def test_wall_cap_is_an_attempted_run(self):
        self.e = Env({"old": {"mode": "hang"}}, **{"caps.wall_s": 2})
        self.e.freeze()
        self.e.run("runner.py", "run", "pilot", "T00", "old", "w1")
        m = self.e.meta("T00-w1-old")
        self.assertEqual(m["stop_reason"], "timeout")
        unit = next(x for x in self.e.ledger() if x["kind"] == "unit")
        self.assertEqual(unit["status"], "valid")

    def test_budget_stop_is_an_attempted_run(self):
        self.e = Env({"old": {"mode": "budget", "cost": 1.2}})
        self.e.freeze()
        self.e.run("runner.py", "run", "pilot", "T00", "old", "b1")
        self.assertEqual(self.e.meta("T00-b1-old")["stop_reason"], "budget")
        self.assertEqual(next(x for x in self.e.ledger() if x["kind"] == "settle")["usd"], 1.2)


class Preflight(unittest.TestCase):
    def test_toy_cases_pass(self):
        e = Env({})
        try:
            r = e.run("preflight.py", str(TESTS / "fixtures/cases/T00"), str(TESTS / "fixtures/cases/R00"))
            self.assertIn("# T00: PASS", r.stdout); self.assertIn("# R00: PASS", r.stdout)
            self.assertIn("3 negative negative/T00-no-secret.patch fails T00-no-secret", r.stdout)
            self.assertIn("ok   3 negative negative/R00-no-false-alarm.md fails R00-no-false-alarm (clean)", r.stdout)
            self.assertIn("ok   1 fixture fails a critical check (clean)", r.stdout)
        finally: e.close()

    def test_case_without_reference_fails(self):
        e = Env({})
        try:
            case = e.root / "X00"
            shutil.copytree(TESTS / "fixtures/cases/T00", case)
            (case / "reference.patch").unlink()
            r = e.run("preflight.py", str(case), ok=False)
            self.assertEqual(r.returncode, 1)
            self.assertIn("FAIL 2 reference passes every check: no reference.patch", r.stdout)
        finally: e.close()


class Layout(unittest.TestCase):
    """Work trees and the grading queue, driven through common.py in a child process with the test environment."""

    def setUp(self):
        self.e = Env({}, **{"simulator.udid": None})

    def tearDown(self):
        self.e.close()

    def py(self, code: str, env=None) -> subprocess.Popen:
        return subprocess.Popen([sys.executable, "-I", "-c", f"import sys; sys.path.insert(0, {str(EVAL)!r})\n" + code],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, env=env or self.e.env)

    def test_empty_fixture_keeps_git_in_the_parent(self):
        case = self.e.root / "N00"
        (case / "fixture").mkdir(parents=True)  # empty, as git would leave it: also try it missing
        patch = case / "new.patch"
        patch.write_text("diff --git a/App/a.txt b/App/a.txt\nnew file mode 100644\n--- /dev/null\n+++ b/App/a.txt\n@@ -0,0 +1 @@\n+hi\n")
        for keep in (True, False):
            if not keep: (case / "fixture").rmdir()
            p = self.py(f"""from common import *
w = SCRATCH / "x" / "work"
make_work({{"dir": __import__("pathlib").Path({str(case)!r})}}, w, patches=[__import__("pathlib").Path({str(patch)!r})])
print(sorted(x.name for x in w.iterdir()), (w.parent / ".git").is_dir(), changed_files(w), patch_of(w).splitlines()[0])""")
            out, err = p.communicate(timeout=60)
            self.assertEqual(p.returncode, 0, err)
            self.assertEqual(out.strip(), "['App'] True ['App/a.txt'] diff --git a/App/a.txt b/App/a.txt")

    def test_each_grading_waits_in_the_queue_on_a_new_simulator(self):
        bin_dir, log = self.e.root / "xbin", self.e.root / "xcrun.log"
        bin_dir.mkdir()
        (bin_dir / "xcrun").write_text(f"""#!/bin/sh
echo "$*" >>{log}
case "$2" in
  list) echo '{{"devices": {{"r": [{{"name": "ios-eval-grader-1", "udid": "OLD"}}, {{"name": "Mine", "udid": "KEEP"}}]}}}}' ;;
  create) echo NEW ;;
esac
""")
        (bin_dir / "xcrun").chmod(0o755)
        env = self.e.env | {"PATH": f"{bin_dir}:{os.environ['PATH']}"}
        import fcntl, time
        with open(self.e.root / "grade.lock", "a") as held:
            fcntl.flock(held, fcntl.LOCK_EX)  # another grading holds the queue
            p = self.py("from common import grading_simulator\nwith grading_simulator({'toolchain': {'simulator_device_type': 'iPhone 15 Pro'}}) as u: print(u)", env)
            time.sleep(1.5)
            self.assertIsNone(p.poll(), "the grading must wait for the queue")
            self.assertFalse(log.exists())
        out, err = p.communicate(timeout=60)
        self.assertEqual((p.returncode, out.strip()), (0, "NEW"), err)
        calls = log.read_text().splitlines()
        self.assertEqual([c for c in calls if not c.startswith("simctl list")],
                         ["simctl shutdown OLD", "simctl delete OLD",
                          f"simctl create ios-eval-grader-{p.pid} iPhone 15 Pro com.apple.CoreSimulator.SimRuntime.iOS-27-3",
                          "simctl shutdown NEW", "simctl delete NEW"])


class Gates(unittest.TestCase):
    def setUp(self):
        self.e = Env({})

    def tearDown(self):
        self.e.close()

    def test_route_gate(self):
        r = self.e.run("gates/route", "--skill", str(TESTS / "fixtures/skill"), ok=False)
        self.assertEqual(r.returncode, 1)  # R00 post-edit misses its required row
        res = {c["case"]: c for c in json.loads((self.e.out / "gates/route.json").read_text())["cases"]}
        t = res["T00"]
        self.assertTrue(t["ok"])
        self.assertEqual(t["pre_edit"]["required_hits"], ["testing"])
        self.assertEqual(t["post_edit"]["optional_hits"], ["localization"])
        self.assertEqual(t["post_edit"]["unnecessary"], ["accessibility"])
        self.assertFalse(res["R00"]["ok"])
        self.assertEqual(res["R00"]["post_edit"]["missing_required"], ["security-privacy"])
        self.assertEqual(self.e.run("gates/route", "--skill", str(TESTS / "fixtures/skill"), str(TESTS / "fixtures/cases/T00")).returncode, 0)

    def test_check_gate(self):
        r = self.e.run("gates/check", "--skill", str(TESTS / "fixtures/skill"))
        self.assertEqual(r.returncode, 0)
        res = {c["case"]: c for c in json.loads((self.e.out / "gates/check.json").read_text())["cases"]}
        self.assertEqual(res["T00"]["seeded"]["counts"]["detected"], 1)
        self.assertEqual(res["T00"]["clean"]["false_flags"], [])
        self.assertEqual(res["T00"]["clean"]["clears"], ["greet.txt"])
        self.assertEqual(res["R00"]["seeded"]["counts"]["pending"], 1)
        self.assertEqual(res["R00"]["clean"]["clears"], ["app.txt"])


class Units(unittest.TestCase):
    def test_ledger_counts_other_stages_against_the_total(self):
        import runner
        out = Path(tempfile.mkdtemp(prefix="iosev-led-"))
        c = json.loads((EVAL / "config.json").read_text())
        saved = runner.OUT, runner.cfg
        try:
            runner.OUT, runner.cfg = out, lambda: c
            (out / "pilot").mkdir()
            (out / "pilot/ledger.jsonl").write_text(json.dumps({"kind": "settle", "run": "x", "usd": 9.47, "seconds": 60}) + "\n")
            self.assertTrue(runner.fits("pilot2", ["new"])[0])  # 9.47 + 1.68 <= 20
            c["caps"]["total_usd"] = 11.0
            ok, why = runner.fits("pilot2", ["new"])
            self.assertFalse(ok)
            self.assertIn("total: spent $9.47", why)
        finally:
            runner.OUT, runner.cfg = saved
            shutil.rmtree(out, ignore_errors=True)

    def test_sign_test(self):
        from report import sign_test
        self.assertAlmostEqual(sign_test(8, 0), 0.0078125)
        self.assertAlmostEqual(sign_test(7, 1), 0.0703125)
        self.assertEqual(sign_test(0, 0), 1.0)
        self.assertEqual(sign_test(1, 0), 1.0)

    def test_probe_verdict_fails_on_any_mismatch(self):
        import runner
        probes = [{"cmd": "ls ~", "want": "denied", "out": None, "sandbox": True},
                  {"cmd": "echo probe > probe.txt && cat probe.txt", "want": "allowed", "out": "(?m)^probe$", "sandbox": True},
                  {"cmd": "git status --short", "want": "allowed", "out": None, "sandbox": True},
                  {"cmd": "cat ~/.zshrc", "want": "denied", "out": None, "sandbox": False},
                  {"cmd": "decide x P.swift", "want": "allowed", "out": '"source":"jev","model":"jev-1"', "sandbox": True}]
        def call(cmd, err, text, unsandboxed=False):
            return {"name": "Bash", "input": {"command": cmd, "dangerouslyDisableSandbox": unsandboxed}, "is_error": err, "text": text}
        good = [call("ls  ~", True, "Exit code 1\nls: /Users/x: Operation not permitted"),
                call("echo probe > probe.txt && cat probe.txt", False, "probe"),
                call("git status --short", False, "?? probe.txt"),
                call("cat ~/.zshrc", True, runner.DENY_UNSANDBOXED, True),
                call("decide x P.swift", True, 'Exit code 4\n{"decision":"x","source":"jev","model":"jev-1","answer":[]}')]
        rows = runner.probe_table(probes, good)
        self.assertTrue(all(r["ok"] for r in rows), rows)
        # an allowed command that is denied fails the verdict
        bad = list(good); bad[1] = call("echo probe > probe.txt && cat probe.txt", True, "Exit code 1\n(eval):1: operation not permitted: probe.txt")
        self.assertEqual([r["got"] for r in runner.probe_table(probes, bad)][1], "denied")
        self.assertFalse(runner.probe_table(probes, bad)[1]["ok"])
        # a denied command that is allowed fails the verdict
        bad = list(good); bad[0] = call("ls ~", False, "Desktop\nDocuments")
        self.assertEqual(runner.probe_table(probes, bad)[0]["got"], "allowed")
        self.assertFalse(runner.probe_table(probes, bad)[0]["ok"])
        # a failure for another reason, a missing call, the wrong sandbox mode, or another Jev model is no pass either
        cases = {2: call("git status --short", True, "fatal: not a git repository"), 3: call("cat ~/.zshrc", True, runner.DENY_UNSANDBOXED),
                 4: call("decide x P.swift", False, '{"decision":"x","source":"jev","model":"jev-2"}')}
        for i, c in cases.items():
            bad = list(good); bad[i] = c
            self.assertFalse(runner.probe_table(probes, bad)[i]["ok"], c)
        self.assertEqual(runner.probe_table(probes, good[1:])[0]["got"], "not run")

    def test_decided_line_records_jev_model_and_drift(self):
        import runner
        from unittest import mock
        line = lambda model: {"type": "user", "message": {"content": [{"type": "tool_result", "tool_use_id": "a",
                              "content": [{"type": "text", "text": f"decided: P.swift: x: jev model {model}"}]}]}}
        with tempfile.TemporaryDirectory() as d, mock.patch.object(runner, "cfg", return_value={"jev": {"model": "jev-1.14.0"}}):
            s = Path(d) / "stream.jsonl"
            s.write_text("\n".join(json.dumps(e) for e in [line("jev-1.14.0")]) + "\n")
            meta = runner.parse_stream(s)
            self.assertEqual(meta["jev_models_observed"], ["jev-1.14.0"])
            self.assertFalse(runner.drift({"arm": "new", "jev_models_observed": meta["jev_models_observed"]}))
            s.write_text("\n".join(json.dumps(e) for e in [line("jev-other")]) + "\n")
            meta = runner.parse_stream(s)
            self.assertTrue(runner.drift({"arm": "new", "jev_models_observed": meta["jev_models_observed"]}))

    def test_probe_reads_the_stream(self):
        import runner
        with tempfile.TemporaryDirectory() as d:
            s = Path(d) / "stream.jsonl"
            s.write_text("\n".join(json.dumps(e) for e in [
                {"type": "assistant", "message": {"content": [{"type": "tool_use", "id": "a", "name": "Bash", "input": {"command": "ls ~"}}]}},
                {"type": "user", "message": {"content": [{"type": "tool_result", "tool_use_id": "a", "is_error": True,
                                                          "content": [{"type": "text", "text": "ls: /Users/x: Operation not permitted"}]}]}},
                {"type": "assistant", "message": {"content": [{"type": "tool_use", "id": "b", "name": "Bash", "input": {"command": "ls /tmp"}}]}},
                "not json"]) + "\n")
            calls = runner.tool_calls(s)
        self.assertEqual([(c["is_error"], c["text"]) for c in calls], [(True, "ls: /Users/x: Operation not permitted"), (None, None)])
        probes = [{"cmd": c, "want": "denied", "out": None, "sandbox": True} for c in ("ls ~", "ls /tmp")]
        self.assertEqual([r["got"] for r in runner.probe_table(probes, calls)], ["denied", "not run"])

    def test_sandbox_needs_no_read_carve_out(self):
        import runner
        for arm in runner.ARMS:
            fs = runner.sandbox_settings(arm)["sandbox"]["filesystem"]
            self.assertNotIn("allowRead", fs)
            for d in (Path.home(), "/tmp", "/private/tmp", "/Volumes", runner.REPO, runner.OUT): self.assertIn(str(d), fs["denyRead"])
            for d in (runner.WORK, runner.REPO_GIT, runner.TMP, runner.SKILL_DIR, runner.SCRATCH / "gitconfig"):
                self.assertFalse(runner.inside(d, *fs["denyRead"]), f"{d} is under a denied root")
            self.assertTrue({str(runner.TMP), str(runner.REPO_GIT), str(runner.LOG)} <= set(fs["allowWrite"]))
        self.assertEqual(runner.sandbox_settings("new")["sandbox"]["network"]["allowedDomains"], ["api.typesafe.ai"])
        names = [p["cmd"] for p in runner.live_probes("new")]
        self.assertTrue(any("scripts/decide" in n for n in names) and not any("scripts/" in p["cmd"] for p in runner.live_probes("old")))
        self.assertFalse(any(str(runner.SKILL_DIR) in p["cmd"] for p in runner.live_probes("none")))

    def test_policy_selftest(self):
        r = subprocess.run([sys.executable, "-I", str(EVAL / "runner.py"), "selftest"], capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stderr)

    def test_grade_contract(self):
        from common import validate_grade
        self.assertEqual(validate_grade({"case": "I01", "checks": [{"id": "I01-a", "priority": "security", "critical": True, "result": "pass"}]}, "I01"), [])
        self.assertTrue(validate_grade({"case": "I01", "checks": [{"id": "I01-a", "priority": "security", "critical": "yes", "result": "ok"}]}, "I01"))
        self.assertTrue(validate_grade({"case": "I02", "checks": []}, "I01"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
