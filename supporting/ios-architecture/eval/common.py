"""Shared paths, config, and helpers of the ios-architecture eval harness (stdlib only, run with python3 -I)."""
import atexit, fcntl, hashlib, json, os, re, shutil, signal, subprocess, sys
from contextlib import contextmanager
from pathlib import Path

EVAL = Path(__file__).resolve().parent
REPO = EVAL.parents[2]
SKILL_SRC = REPO / "skills" / "ios-architecture"
CONFIG = Path(os.environ.get("IOS_EVAL_CONFIG", EVAL / "config.json"))
CASES = Path(os.environ.get("IOS_EVAL_CASES", EVAL / "cases"))
OUT = Path(os.environ.get("IOS_EVAL_OUT", EVAL / "runs"))
# Fixed, neutral, and short: the sandbox falls back to a shared tmp for a CLAUDE_CODE_TMPDIR past ~30 characters.
# Outside /tmp: the sandbox denies /tmp, and a denied /tmp symlink blocks every path spelled through it, allowRead or not.
SCRATCH = Path(os.environ.get("IOS_EVAL_SCRATCH", "/Users/Shared/iosev"))
# Machine-wide, outside SCRATCH: every harness process on this Mac queues its gradings here.
GRADE_LOCK = Path(os.environ.get("IOS_EVAL_GRADE_LOCK", "/tmp/ios-eval-grade.lock"))
BUILD_DIRS = (".build", "DerivedData", ".swiftpm", "xcuserdata")
CHECK_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")


def cfg() -> dict:
    return json.loads(CONFIG.read_text())


def die(msg: str, code: int = 2):
    print(msg, file=sys.stderr)
    sys.exit(code)


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def tree_files(root: Path, skip=(".git",) + BUILD_DIRS) -> list[Path]:
    out = []
    for dirpath, dirs, files in os.walk(root):
        dirs[:] = sorted(d for d in dirs if d not in skip and not d.endswith(".xcresult"))
        out += [Path(dirpath, f) for f in sorted(files)]
    return out


def manifest(root: Path) -> dict:
    """sha256 of every file under root, keyed by relative path (the exec bit is part of the entry)."""
    return {str(p.relative_to(root)): sha256_bytes(p.read_bytes()) + ("+x" if os.access(p, os.X_OK) else "")
            for p in tree_files(root, skip=(".git",))}


def tree_sha(root: Path) -> str:
    return sha256_bytes(json.dumps(manifest(root), sort_keys=True).encode())


def load_case(case_dir: Path) -> dict:
    case = json.loads((case_dir / "case.json").read_text())
    for k in ("id", "title", "priorities", "references"):
        if k not in case: raise ValueError(f"{case_dir}/case.json: missing {k}")
    if not CHECK_ID.match(case["id"]): raise ValueError(f"{case_dir}/case.json: bad id")
    case["dir"] = case_dir
    return case


def case_dirs() -> list[Path]:
    return sorted(p.parent for p in CASES.glob("*/case.json"))


def find_case(case_id: str) -> dict:
    for d in case_dirs():
        c = load_case(d)
        if c["id"] == case_id: return c
    die(f"unknown case {case_id} in {CASES}")


def is_review(case: dict) -> bool:
    return bool(case.get("variants"))


def case_file(case: dict, rel: str) -> Path:
    p = (case["dir"] / rel).resolve()
    if not p.is_relative_to(case["dir"].resolve()): raise ValueError(f"{rel} is outside the case folder")
    return p


def variant_spec(case: dict, variant: str) -> dict:
    """A review variant (CASES.md): diff, reference, and negatives as paths in the case folder; other keys pass through."""
    spec = case["variants"][variant]
    return spec | {"diff": case_file(case, spec["diff"]),
                   "reference": case_file(case, spec["reference"]) if spec.get("reference") else None,
                   "negatives": [case_file(case, n) for n in spec.get("negatives", [])]}


def variant_patch(case: dict, variant) -> Path | None:
    return variant_spec(case, variant)["diff"] if variant else None


GIT = ["git", "-c", "core.hooksPath=/dev/null", "-c", "commit.gpgsign=false", "-c", "user.name=eval", "-c", "user.email=eval@invalid"]


def git(work: Path, *args, check=True, index: Path | None = None, **kw) -> subprocess.CompletedProcess:
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")} | {"GIT_CONFIG_GLOBAL": "/dev/null", "GIT_CONFIG_NOSYSTEM": "1"}
    if index: env["GIT_INDEX_FILE"] = str(index)
    return subprocess.run([*GIT, "-C", str(work), *args], capture_output=True, text=True, check=check, env=env, **kw)


def snapshot(work: Path) -> str:
    """Git tree id of work as it is now, through a separate index, so the builder's index and `git diff` stay as they are."""
    index = SCRATCH / "snapshot-index"
    index.unlink(missing_ok=True)
    git(work, "add", "-A", ".", index=index)
    return git(work, "write-tree", index=index).stdout.strip()


def make_work(case: dict, dest: Path, variant=None, patches=()) -> None:
    """Fresh copy of fixture/ (no .gitkeep), git init, 1 commit, then the review variant and extra patches as uncommitted changes.
    A missing or empty fixture (a new project) keeps the repository in dest's parent, so dest starts empty: scaffold needs that."""
    if not dest.resolve().is_relative_to(SCRATCH.resolve()): raise ValueError(f"{dest} is outside the scratch folder {SCRATCH}")
    shutil.rmtree(dest, ignore_errors=True); shutil.rmtree(dest.parent / ".git", ignore_errors=True)
    fixture = case["dir"] / "fixture"
    if fixture.is_dir(): shutil.copytree(fixture, dest, symlinks=True, ignore=shutil.ignore_patterns(".gitkeep"))
    else: dest.mkdir(parents=True)  # git keeps no empty folder
    root = dest if any(dest.iterdir()) else dest.parent
    git(root, "init", "-q", "-b", "main")
    (root / ".git/info/exclude").write_text("".join(f"{d}/\n" for d in BUILD_DIRS) + "*.xcresult/\n" + ("" if root == dest else f"/*\n!/{dest.name}/\n"))
    git(root, "add", "-A")
    git(root, "commit", "-q", "--allow-empty", "-m", "fixture")
    into = [] if root == dest else [f"--directory={dest.name}"]
    for p in ([variant_patch(case, variant)] if variant else []) + list(patches):
        r = git(dest, "apply", "--whitespace=nowarn", *into, str(p), check=False)
        if r.returncode: raise RuntimeError(f"git apply {p.name}: {r.stderr.strip()[:300]}")


def changed_files(work: Path) -> list[str]:
    """Modified, staged, and untracked files that exist, relative to work (the fixture commit is the base)."""
    names = git(work, "diff", "--name-only", "--relative", "HEAD").stdout.split() + git(work, "ls-files", "--others", "--exclude-standard").stdout.split()
    return sorted(n for n in set(names) if (work / n).is_file())


def patch_of(work: Path) -> str:
    git(work, "add", "-A")
    return git(work, "diff", "--cached", "--binary", "--relative", "HEAD").stdout


class Redactor:
    """Replaces each secret value in text. Logs pass through it before they reach disk."""
    def __init__(self, *secrets):
        self.secrets = [s for s in secrets if s and len(s) >= 8]
        self.hits = 0

    def __call__(self, text: str) -> str:
        for s in self.secrets:
            if s in text:
                self.hits += text.count(s)
                text = text.replace(s, "[REDACTED]")
        return text


def blocked_env(scratch_bin: Path) -> dict:
    """Environment for running skill scripts offline: no key, no Keychain item, and a curl that always fails."""
    scratch_bin.mkdir(parents=True, exist_ok=True)
    curl = scratch_bin / "curl"
    curl.write_text("#!/bin/sh\necho 'curl: blocked by the eval harness' >&2\nexit 7\n")
    curl.chmod(0o755)
    env = {k: v for k, v in os.environ.items() if not k.startswith("TYPESAFE_")}
    return env | {"PATH": f"{scratch_bin}:{os.environ.get('PATH', '/usr/bin:/bin')}", "TYPESAFE_KEYCHAIN_SERVICE": "ios-eval-no-keychain"}


def simctl(*args, check=True) -> str:
    return subprocess.run(["xcrun", "simctl", *args], capture_output=True, text=True, check=check).stdout


def delete_simulator(udid: str):
    simctl("shutdown", udid, check=False)
    simctl("delete", udid, check=False)


@contextmanager
def grading_simulator(case: dict | None = None):
    """1 grading at a time on this Mac (the blocking file lock is the queue), each on a new simulator that is deleted afterwards:
    parallel xcodebuild runs kill each other's tests. Config simulator.udid replaces the new simulator; offline tests only."""
    sim = cfg()["simulator"]
    with open(GRADE_LOCK, "a") as held:
        fcntl.flock(held, fcntl.LOCK_EX)
        if sim.get("udid"):
            yield sim["udid"]; return
        for d in (d for r in json.loads(simctl("list", "devices", "-j"))["devices"].values() for d in r):
            if d["name"].startswith(sim["name"]): delete_simulator(d["udid"])  # left by a killed grading; the lock says none is in use
        device = (case or {}).get("toolchain", {}).get("simulator_device_type") or sim["device_type"]
        udid = simctl("create", f"{sim['name']}-{os.getpid()}", device, sim["runtime"]).strip()
        try: yield udid
        finally: delete_simulator(udid)


def validate_grade(obj, case_id: str) -> list[str]:
    """Errors in a grade.sh result (CASES.md contract); empty when valid."""
    errs = []
    if not isinstance(obj, dict): return ["not a JSON object"]
    if obj.get("case") != case_id: errs.append(f"case is {obj.get('case')!r}, expected {case_id!r}")
    checks = obj.get("checks")
    if not isinstance(checks, list) or not checks: return errs + ["checks must be a non-empty list"]
    seen = set()
    for c in checks:
        if not isinstance(c, dict) or not CHECK_ID.match(str(c.get("id", ""))): errs.append(f"bad check {c!r:.80}"); continue
        if c["id"] in seen: errs.append(f"duplicate check {c['id']}")
        seen.add(c["id"])
        if c.get("result") not in ("pass", "fail", "na"): errs.append(f"{c['id']}: result must be pass, fail, or na")
        if not isinstance(c.get("critical"), bool): errs.append(f"{c['id']}: critical must be a boolean")
        if not isinstance(c.get("priority"), str): errs.append(f"{c['id']}: priority must be a string")
    return errs


def run_grader(case: dict, work: Path, out: Path, final_text: Path, udid: str, timeout: int, variant=None) -> tuple[dict | None, str]:
    """Run hidden/grade.sh on work. Returns (result, error); error is non-empty for an infrastructure failure."""
    grader = case["dir"] / "hidden" / "grade.sh"
    if not os.access(grader, os.X_OK): return None, f"{grader} is missing or not executable"
    out.unlink(missing_ok=True)
    env = blocked_env(SCRATCH / "gbin") | {"EVAL_SIM": udid, "EVAL_FINAL_TEXT": str(final_text)} | ({"EVAL_VARIANT": variant} if variant else {})
    p = subprocess.Popen([str(grader), str(work), str(out)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, env=env,
                         cwd=out.parent, start_new_session=True)
    try: stdout, stderr = p.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        os.killpg(p.pid, signal.SIGKILL); p.communicate()  # with its xcodebuild children, which would outlive the lock
        return None, f"grade.sh timed out after {timeout} s"
    if p.returncode != 0: return None, f"grade.sh exit {p.returncode}: {(stderr or stdout)[-800:]}"
    try: res = json.loads(out.read_text())
    except (OSError, ValueError) as e: return None, f"grade.sh wrote no valid JSON: {e}"
    errs = validate_grade(res, case["id"])
    return (None, "; ".join(errs)) if errs else (res, "")


def lock():
    """One harness process at a time: runs share the fixed scratch paths."""
    SCRATCH.mkdir(mode=0o700, parents=True, exist_ok=True)
    st = os.lstat(SCRATCH)  # the default root sits in a world-writable folder: refuse one another user planted
    if os.path.islink(SCRATCH) or not os.path.isdir(SCRATCH) or st.st_uid != os.getuid(): die(f"{SCRATCH} must be a folder you own", 1)
    os.chmod(SCRATCH, 0o700)
    try: (SCRATCH / "lock").mkdir()
    except FileExistsError: die(f"another harness process holds {SCRATCH / 'lock'}; remove it if none is alive", 1)
    atexit.register(lambda: (SCRATCH / "lock").rmdir() if (SCRATCH / "lock").exists() else None)
