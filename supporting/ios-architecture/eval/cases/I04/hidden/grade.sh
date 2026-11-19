#!/usr/bin/env bash
# Hidden grader for case I04 (extract the orders totals and loading seam into a local package).
# Usage: grade.sh <work-dir> <out.json>
# Needs EVAL_SIM (a simulator UDID). Exit 0 when it wrote a result, also when checks fail;
# exit 2 for a usage error and 3 for an infrastructure failure.
set -euo pipefail

usage() { echo "usage: EVAL_SIM=<udid> grade.sh <work-dir> <out.json>" >&2; exit 2; }
[ $# -eq 2 ] || usage
[ -d "$1" ] || usage
[ -n "${EVAL_SIM:-}" ] || usage

here=$(cd "$(dirname "$0")" && pwd)
fixture=$(cd "$here/../fixture" && pwd)
work=$(cd "$1" && pwd)
out=$2
tmp=$(mktemp -d "${TMPDIR:-/tmp}/grade-i04.XXXXXX")
trap 'rm -rf "$tmp"' EXIT

# Grade a copy of the result, never the builder's tree.
rsync -a --exclude .git --exclude DerivedData --exclude build --exclude .build "$work/" "$tmp/src/"
if [ -d "$tmp/src/LedgerUITests" ]; then
  mkdir -p "$tmp/src/LedgerUITests/HiddenI04"
  cp "$here/HiddenI04AcceptanceTests.swift" "$tmp/src/LedgerUITests/HiddenI04/"
fi

# Dump each package manifest before the build, from a pristine copy.
: >"$tmp/packages.txt"
while IFS= read -r manifest; do
  dir=$(dirname "$manifest")
  n=$(wc -l <"$tmp/packages.txt" | tr -d ' ')
  if swift package --package-path "$dir" --scratch-path "$tmp/spm-$n" dump-package >"$tmp/package-$n.json" 2>"$tmp/package-$n.err"; then
    printf '%s\t%s\n' "$dir" "$tmp/package-$n.json" >>"$tmp/packages.txt"
  else
    printf '%s\t\n' "$dir" >>"$tmp/packages.txt"
  fi
done < <(find "$tmp/src" -name Package.swift -not -path '*/.build/*' -not -path '*/LedgerUITests/HiddenI04/*' | sort)

xcrun simctl boot "$EVAL_SIM" >/dev/null 2>&1 || true
xcrun simctl bootstatus "$EVAL_SIM" >/dev/null 2>&1 || { echo "simulator $EVAL_SIM did not boot" >&2; exit 3; }
xcrun simctl uninstall "$EVAL_SIM" com.example.ledger >/dev/null 2>&1 || true

common=(-project "$tmp/src/Ledger.xcodeproj" -scheme Ledger -destination "id=$EVAL_SIM"
  -derivedDataPath "$tmp/dd" CODE_SIGNING_ALLOWED=NO)
build=pass
xcodebuild build-for-testing "${common[@]}" >"$tmp/build.log" 2>&1 || build=fail

bundle_id=""
tests=skipped
if [ "$build" = pass ]; then
  app="$tmp/dd/Build/Products/Debug-iphonesimulator/Ledger.app"
  [ -d "$app" ] || { echo "no Ledger.app after the build" >&2; exit 3; }
  bundle_id=$(plutil -extract CFBundleIdentifier raw "$app/Info.plist")
  xcrun simctl uninstall "$EVAL_SIM" "$bundle_id" >/dev/null 2>&1 || true
  tests=ran
  # The hidden tests find the app's data container by this bundle identifier.
  TEST_RUNNER_LEDGER_BUNDLE_ID="$bundle_id" \
    xcodebuild test-without-building "${common[@]}" -resultBundlePath "$tmp/r.xcresult" \
    -parallel-testing-enabled NO -only-testing:LedgerUITests/HiddenI04AcceptanceTests \
    >"$tmp/test.log" 2>&1 || true
  [ -d "$tmp/r.xcresult" ] || { tail -20 "$tmp/test.log" >&2; echo "no result bundle" >&2; exit 3; }
  xcrun xcresulttool get test-results tests --path "$tmp/r.xcresult" >"$tmp/tests.json" \
    || { echo "xcresulttool failed" >&2; exit 3; }
fi

python3 -I - "$build" "$tests" "$tmp" "$fixture" "$bundle_id" "$out" <<'PY'
import json, os, re, sys
build, tests, tmp, fixture, bundle_id, out = sys.argv[1:7]
src = f"{tmp}/src"
UI_MODULES = {"UIKit", "SwiftUI", "AppKit", "WatchKit"}
IMPORT = re.compile(r"^\s*(?:@\w+(?:\([^)]*\))?\s+)*import\s+(?:(?:struct|class|enum|protocol|func|var|let|typealias)\s+)?(\w+)", re.M)
VIEW_DECL = re.compile(r"\b(?:class|struct)\s+\w+\s*:\s*[^{]*\b(?:UIViewController|UITableViewController|UIView|View)\b")
LEGACY_FILES = ["Ledger/SettingsViewController.swift", "Ledger/LegacyAnalytics.swift",
                "Ledger/Generated/L10n.swift", "Ledger/en.lproj/Localizable.strings"]

def swift_files(path):
    for root, dirs, files in os.walk(path):
        dirs[:] = [d for d in dirs if d not in (".build", ".git")]
        for f in files:
            if f.endswith(".swift"):
                yield os.path.join(root, f)

def read(path):
    with open(path, errors="replace") as fh:
        return fh.read()

# --- static: packages and their targets
packages = []  # (dir, [target dicts]) ; target dict: name, type, files
for line in open(f"{tmp}/packages.txt"):
    pdir, _, dump = line.rstrip("\n").partition("\t")
    targets = []
    if dump:
        for t in json.load(open(dump)).get("targets", []):
            default = "Tests" if t.get("type") == "test" else "Sources"
            tpath = os.path.join(pdir, t.get("path") or os.path.join(default, t["name"]))
            files = list(swift_files(tpath)) if os.path.isdir(tpath) else []
            targets.append({"name": t["name"], "type": t.get("type"), "files": files})
    packages.append((pdir, targets))

def rel(p):
    return os.path.relpath(p, src)

app_sources = [f for f in swift_files(f"{src}/Ledger")]
app_imports = {m for f in app_sources for m in IMPORT.findall(read(f))}
pbx = read(f"{src}/Ledger.xcodeproj/project.pbxproj") if os.path.exists(f"{src}/Ledger.xcodeproj/project.pbxproj") else ""
module_targets = {t["name"] for _, ts in packages for t in ts if t["type"] != "test"}
linked = sorted(module_targets & app_imports)

if not packages:
    extracted = ("fail", "no Package.swift in the result")
elif "XCLocalSwiftPackageReference" not in pbx:
    extracted = ("fail", "Ledger.xcodeproj has no local package reference")
elif not linked:
    extracted = ("fail", "the app imports no target of the new package(s): " + ", ".join(sorted(module_targets)))
else:
    extracted = ("pass", "local package(s) " + ", ".join(rel(p) for p, _ in packages) + "; app imports " + ", ".join(linked))

# Domain target: a non-test package target that holds totals code (mentions "subtotal").
# A target that also declares a view or view controller is presentation, not domain.
domain, ui_domain = [], []
for _, ts in packages:
    for t in ts:
        if t["type"] == "test" or not t["files"]:
            continue
        text = "\n".join(read(f) for f in t["files"])
        if not re.search(r"subtotal", text, re.I):
            continue
        ui = sorted(set(IMPORT.findall(text)) & UI_MODULES)
        if VIEW_DECL.search(text):
            continue
        (ui_domain if ui else domain).append((t["name"], ui))
if ui_domain:
    no_ui = ("fail", "domain target imports UI: " + "; ".join(f"{n} imports {', '.join(u)}" for n, u in ui_domain))
elif not domain:
    no_ui = ("fail", "no package target holds the totals logic")
else:
    no_ui = ("pass", "totals target(s) " + ", ".join(n for n, _ in domain) + " import no UI framework")

changed = []
for f in LEGACY_FILES:
    a, b = f"{fixture}/{f}", f"{src}/{f}"
    if not os.path.exists(b) or open(a, "rb").read() != open(b, "rb").read():
        changed.append(f)
legacy = ("fail", "changed or removed: " + ", ".join(changed)) if changed else ("pass", f"{len(LEGACY_FILES)} unrelated legacy files unchanged")

# --- hidden XCUITests
results, log = {}, ""
if tests == "ran":
    def walk(node):
        if node.get("nodeType") == "Test Case":
            results.setdefault(node.get("name", "").split("(")[0], []).append(node.get("result", "unknown"))
        for child in node.get("children", []):
            walk(child)
    for node in json.load(open(f"{tmp}/tests.json")).get("testNodes", []):
        walk(node)
    log = read(f"{tmp}/test.log")

def first_error(method):
    m = re.search(r"error: -\[\S+ " + method + r"\] : (.{0,200})", log)
    return m.group(1).strip() if m else ""

def ui_result(methods):
    if build != "pass":
        return ("fail", "build failed")
    notes = []
    for m in methods:
        runs = results.get(m, [])
        if len(runs) != 1:
            return ("fail", f"XCUITest {m} ran {len(runs)} times, expected 1")
        if runs[0] != "Passed":
            return ("fail", f"XCUITest {m} {runs[0].lower()}: {first_error(m)}".rstrip(": "))
        notes.append(m)
    return ("pass", "XCUITest " + ", ".join(notes) + " passed")

def ids_and_keys():
    r = ui_result(["testSavesCacheInLegacyFormat"])
    if r[0] != "pass":
        return r
    if bundle_id != "com.example.ledger":
        return ("fail", f"bundle identifier is {bundle_id!r}, expected 'com.example.ledger'")
    return ("pass", r[1] + "; bundle identifier com.example.ledger")

checks = [
    ("I04-build", "reliability", True,
     (build, "xcodebuild build-for-testing " + ("succeeded" if build == "pass" else "failed"))),
    ("I04-characterization", "reliability", True, ui_result(["testTotalsMatchLegacyBehavior"])),
    ("I04-old-data-loads", "reliability", True, ui_result(["testLoadsCacheWrittenByOldVersion"])),
    ("I04-ids-and-keys-unchanged", "reliability", True, ids_and_keys()),
    ("I04-interrupted-repeated-load", "reliability", True,
     ui_result(["testRecoversFromInterruptedCacheWrite", "testRepeatedReloadDoesNotDuplicate"])),
    ("I04-navigation-unchanged", "reliability", True, ui_result(["testNavigationUnchanged"])),
    ("I04-package-extracted", "maintainability", True, extracted),
    ("I04-domain-no-ui-import", "maintainability", True, no_ui),
    ("I04-legacy-unchanged", "maintainability", True, legacy),
]
json.dump({"case": "I04", "checks": [
    {"id": i, "priority": p, "critical": c, "result": r[0], "evidence": r[1]} for i, p, c, r in checks
]}, open(out, "w"), indent=2)
PY
