#!/bin/sh
# Offline tests for scripts/check, route, migration-sort, and decide.
# A fake curl and a fake security command in PATH stand in for the network and the Keychain.
set -u
here=$(cd "$(dirname "$0")" && pwd -P)
S=$(cd "$here/../../../skills/ios-architecture/scripts" && pwd -P)
fx=$here/fixtures
pass=0
fail=0

work=$(mktemp -d) || exit 2
trap 'rm -rf "$work"' EXIT HUP INT TERM

ok() { pass=$((pass + 1)); }
bad() { fail=$((fail + 1)); printf 'FAIL: %s\n' "$1"; }
# expect <name> <actual> <expected>
expect() { if [ "$2" = "$3" ]; then ok; else bad "$1"; printf '  expected: %s\n  actual:   %s\n' "$3" "$2"; fi; }
# has <name> <text> <fixed-string>
has() { if printf '%s\n' "$2" | grep -qF -- "$3"; then ok; else bad "$1"; printf '  missing: %s\n' "$3"; fi; }
hasnt() { if printf '%s\n' "$2" | grep -qF -- "$3"; then bad "$1"; printf '  unexpected: %s\n' "$3"; else ok; fi; }

# Fake curl: records argv, stdin, and the request body, answers with $STUB_BODY/<first question id>.json and $STUB_CODE.
mkdir -p "$work/bin"
cat >"$work/bin/curl" <<'EOF'
#!/bin/sh
printf '%s\n' "$@" >"$STUB_LOG.argv"
cat >"$STUB_LOG.stdin"
out=
body=
while [ $# -gt 0 ]; do
  case $1 in -o) out=$2; shift ;; --data-binary) body=${2#@}; shift ;; esac
  shift
done
cp "$body" "$STUB_LOG.body"
jq -r '.questions | keys[0]' "$body" >>"$STUB_LOG.calls"
[ "${STUB_EXIT:-0}" = 0 ] || exit "$STUB_EXIT"
cp "$STUB_BODY/$(jq -r '.questions | keys[0]' "$body").json" "$out"
printf '%s' "${STUB_CODE:-200}"
EOF
cat >"$work/bin/security" <<'EOF'
#!/bin/sh
[ -n "${STUB_KEYCHAIN:-}" ] || exit 44
printf '%s\n' "$STUB_KEYCHAIN"
EOF
chmod +x "$work/bin/curl" "$work/bin/security"
PATH=$work/bin:$PATH
STUB_LOG=$work/curl
export PATH STUB_LOG
unset TYPESAFE_API_KEY TYPESAFE_KEYCHAIN_SERVICE STUB_KEYCHAIN STUB_EXIT STUB_CODE STUB_BODY 2>/dev/null
called() { [ -f "$STUB_LOG.argv" ] && echo yes || echo no; }
reset_stub() { rm -f "$STUB_LOG.argv" "$STUB_LOG.stdin" "$STUB_LOG.body" "$STUB_LOG.calls"; }
profile() { # dir code_may_leave_machine
  printf '{"app_name": "Fixture", "store": "files", "code_may_leave_machine": %s}\n' "$2" >"$1/ios-architecture.json"
}

# ---------- check ----------
cp -R "$fx/project-good" "$work/good"
out=$("$S/check" "$work/good")
expect "check: good project passes" "$?:$out" "0:check: 0 violations, 0 pending decisions"

cp -R "$fx/project-bad" "$work/bad"
# The secret value is built here so that no file in the repository holds it.
printf 'let awsKey = "%s%s"\n' AKIA IOSFODNN7EXAMPLE >"$work/bad/Packages/Features/Orders/Sources/OrdersFeature/Secrets.swift"
out=$("$S/check" "$work/bad")
rc=$?
expect "check: bad project exits 1" "$rc" 1
got=$(printf '%s\n' "$out" | sed -nE 's/^([^ ]+:[0-9]+: [a-z0-9-]+):.*/\1/p')
expect "check: bad project violations match project-bad.expected" "$got" "$(cat "$fx/project-bad.expected")"

rules=$("$S/check" --rules | sed -nE 's/^([a-z0-9-]+) \(references\/.*/\1/p' | sort -u)
seen=$(cut -d' ' -f2 "$fx/project-bad.expected" | sort -u)
for r in $rules; do printf '%s\n' "$seen" | grep -qx "$r" && ok || bad "check: rule $r has no bad fixture"; done
for r in $rules; do printf '%s\n' "$out" | grep -q "^[^ ]*: $r: .* (references/[a-z-]*\.md)$" || bad "check: rule $r line has no reference"; done

out=$("$S/check" "$work/bad" App/Legacy/AppDelegate.swift)
rc=$?
got=$(printf '%s\n' "$out" | sed -nE 's/^([^ ]+:[0-9]+: [a-z0-9-]+):.*/\1/p' | paste -sd' ' -)
expect "check: file mode runs file rules only" "$rc:$got" "1:App/Legacy/AppDelegate.swift:7: print-log App/Legacy/AppDelegate.swift:8: task-detached App/Legacy/AppDelegate.swift:9: http-url"

view=Packages/Features/Checkout/Sources/CheckoutFeature/CheckoutView.swift
out=$("$S/check" "$work/good" "$view")
expect "check: no profile gives pending fallback decisions" "$?" 3
has "check: a fallback pending line names its next action" "$out" "pending: $view: check-personal-data-in-log: escalate=fallback tier=medium reason=code_may_not_leave_machine; next: run scripts/decide check-personal-data-in-log $view, give only its request object to a subagent of tier medium, record that answer with scripts/decide --resolve check-personal-data-in-log $view --answer <json> --source fallback, then run scripts/check again"
hasnt "check: no decided line without Jev" "$out" "decided:"

cp -R "$fx/project-good" "$work/goodjev"
profile "$work/goodjev" true
reset_stub
out=$(TYPESAFE_API_KEY=test-key-123 STUB_BODY=$fx/responses/clear "$S/check" "$work/goodjev" "$view")
expect "check: Jev clears the change set" "$?:$(printf '%s\n' "$out" | tail -1)" "0:check: 0 violations, 0 pending decisions"
out=$(TYPESAFE_API_KEY=test-key-123 STUB_BODY=$fx/responses/flag "$S/check" "$work/goodjev" "$view")
expect "check: Jev flag is a violation" "$?" 1
has "check: Jev violation line" "$out" "$view:7: check-business-rules-in-view: Move the rule into a pure function in the domain target, and call it from the view or the model. Jev p=0.98. (references/architecture.md)"
has "check: a flag counts when another question stays open" "$out" "$view:5: check-personal-data-in-log: Mark the number privacy: .private, or remove it from the log. Jev p=0.99. (references/security-privacy.md)"
has "check: a security decision below a threshold names a fallback subagent and the record command" "$out" "pending: $view: check-personal-data-in-log: escalate=fallback tier=medium reason=below_threshold; next: run scripts/decide check-personal-data-in-log $view, give only its request object to a subagent of tier medium, record that answer with scripts/decide --resolve check-personal-data-in-log $view --answer <json> --source fallback, then run scripts/check again"
has "check: a decided line names the Jev model" "$out" "decided: $view: check-business-rules-in-view: jev model jev-1.14.0"
has "check: a pending Jev result whose flag applies names the Jev model" "$out" "decided: $view: check-personal-data-in-log: jev model jev-1.14.0"
expect "check: the decided lines come before the summary" "$(printf '%s\n' "$out" | tail -3 | cut -d: -f1 | paste -sd' ' -)" "decided decided check"

# ---------- deviation markers ----------
cp -R "$fx/project-deviation" "$work/dev"
shop=Packages/Features/Shop/Sources/ShopFeature
out=$("$S/check" "$work/dev" "$shop/ShopReducer.swift")
expect "deviation: a marker suppresses the TCA import" "$?:$out" "0:suppressed: $shop/ShopReducer.swift:2: feature-vendor-import: deviation large-team
check: 0 violations, 0 pending decisions, 1 suppressed by deviation markers"
out=$("$S/check" "$work/dev" "$shop/ShopClient.swift")
expect "deviation: the marker suppresses the TCA module only" "$?:$out" "1:$shop/ShopClient.swift:3: feature-vendor-import: Feature code imports a third-party module. Wrap the vendor API behind a protocol. (references/project-setup.md)
suppressed: $shop/ShopClient.swift:2: feature-vendor-import: deviation large-team
check: 1 violations, 0 pending decisions, 1 suppressed by deviation markers"
out=$("$S/check" "$work/dev" "$shop/TokenCache.swift")
expect "deviation: a marker does not suppress a security rule" "$?:$(printf '%s\n' "$out" | sed -nE 's/^([^ ]+:[0-9]+: [a-z0-9-]+):.*/\1/p'):$(printf '%s\n' "$out" | grep -c '^suppressed:')" "1:$shop/TokenCache.swift:5: userdefaults-secret:0"
printf '// ios-architecture: deviation tca\nimport ComposableArchitecture\n' >"$work/dev/$shop/Unknown.swift"
out=$("$S/check" "$work/dev" "$shop/Unknown.swift")
expect "deviation: an unknown threshold id is a violation" "$?:$(printf '%s\n' "$out" | sed -nE 's/^([^ ]+:[0-9]+: [a-z0-9-]+):.*/\1/p' | paste -sd' ' -)" "1:$shop/Unknown.swift:1: deviation-unknown-threshold $shop/Unknown.swift:2: feature-vendor-import"
has "deviation: the unknown id line names the id" "$out" "unknown threshold: tca."

table=$(grep -v '^#' "$S/lib/deviation-rules.tsv" | cut -f1 | sort -u)
doc=$(sed -nE 's/^\| `([a-z0-9-]+)` \|.*/\1/p' "$S/../references/deviations.md" | sort -u)
expect "deviation: the table and references/deviations.md have the same ids" "$table" "$doc"
cp -R "$S/.." "$work/skill"
cp "$S/lib/deviation-rules.tsv" "$work/table.tsv"
for rule in userdefaults-secret check-personal-data-in-log check-trust-boundary-input keychain-accessible-always secret-value; do
  { cat "$work/table.tsv"; printf 'large-team\t%s\t-\n' "$rule"; } >"$work/skill/scripts/lib/deviation-rules.tsv"
  err=$("$work/skill/scripts/check" "$work/dev" "$shop/ShopReducer.swift" 2>&1 >/dev/null)
  expect "deviation: check refuses a table that lists $rule" "$?:$err" "2:check: invalid deviation table: large-team: $rule is a security or privacy rule"
done
{ cat "$work/table.tsv"; printf 'large-team\tno-such-rule\t-\n'; } >"$work/skill/scripts/lib/deviation-rules.tsv"
err=$("$work/skill/scripts/check" "$work/dev" "$shop/ShopReducer.swift" 2>&1 >/dev/null)
expect "deviation: check refuses a table with an unknown rule" "$?:$err" "2:check: invalid deviation table: large-team: unknown rule: no-such-rule"
cp "$work/table.tsv" "$work/skill/scripts/lib/deviation-rules.tsv"

# ---------- route ----------
rows() { printf '%s\n' "$1" | sed -n "s|^# $2: ||p"; }
out=$("$S/route" "$work/good" "$view" Packages/Features/Checkout/Package.swift App/MyApp/Info.plist App/MyApp/Resources/Localizable.xcstrings Packages/Features/Checkout/Sources/CheckoutDomain/Cart.swift)
expect "route: exit 0" "$?" 0
expect "route: view rows" "$(rows "$out" "$view")" "accessibility architecture localization native-ui-patterns navigation performance security-privacy testing ui-framework"
expect "route: manifest rows" "$(rows "$out" Packages/Features/Checkout/Package.swift)" "architecture concurrency project-setup testing"
expect "route: Info.plist rows" "$(rows "$out" App/MyApp/Info.plist)" "project-setup security-privacy"
expect "route: string catalog rows" "$(rows "$out" App/MyApp/Resources/Localizable.xcstrings)" "localization"
expect "route: domain rows" "$(rows "$out" Packages/Features/Checkout/Sources/CheckoutDomain/Cart.swift)" "architecture concurrency testing"
has "route: prints reference files" "$out" "references/accessibility.md"
has "route: prints the native-ui-patterns skill" "$out" "skill: native-ui-patterns"
hasnt "route: no reference file for the skill row" "$out" "references/native-ui-patterns.md"

printf 'struct Helper {\n    let x = 1\n}\n' >"$work/good/Helper.swift"
reset_stub
out=$("$S/route" "$work/good" Helper.swift)
expect "route: unrouted file without profile is pending" "$?:$(called)" "3:no"
has "route: unrouted pending line names its next action" "$out" "pending: Helper.swift: route: escalate=fallback tier=small reason=code_may_not_leave_machine; next: run scripts/decide route Helper.swift, give only its request object to a subagent of tier small, record that answer with scripts/decide --resolve route Helper.swift --answer <json> --source fallback, then run scripts/route again"

cp "$work/good/Helper.swift" "$work/goodjev/Helper.swift"
out=$(TYPESAFE_API_KEY=test-key-123 STUB_BODY=$fx/responses/route "$S/route" "$work/goodjev" Helper.swift)
expect "route: Jev routes an unrouted file" "$?:$(rows "$out" Helper.swift)" "0:architecture concurrency localization security-privacy testing"
has "route: a decided line names the Jev model" "$out" "decided: Helper.swift: route: jev model jev-1.14.0"

cat >"$work/good/BookCache.swift" <<'EOF'
struct BookCache {
    static let standard = BookCache(fileURL: URL.cachesDirectory.appending(path: "reading-list.json"))
    let fileURL: URL
    func load() throws -> [Book] {
        return try JSONDecoder().decode([Book].self, from: Data(contentsOf: fileURL))
    }
    func save(_ data: Data) throws {
        try data.write(to: fileURL, options: [.atomic, .completeFileProtectionUntilFirstUserAuthentication])
    }
}
EOF
out=$("$S/route" "$work/good" BookCache.swift)
has "route: a file cache routes to persistence" "$(rows "$out" BookCache.swift)" "persistence"
for line in 'let u = URL.documentsDirectory' 'let u = .applicationSupportDirectory' 'let d = Data(contentsOf: u)' 'try s.write(to: u, atomically: true, encoding: .utf8)' 'let p = NSFileProtectionComplete'; do
  printf '%s\n' "$line" >"$work/good/Store.swift"
  has "route: persistence pattern: $line" "$(rows "$("$S/route" "$work/good" Store.swift)" Store.swift)" "persistence"
done
printf 'struct Echo {\n    func emit(into output: inout String) { value.write(to: &output) }\n}\n' >"$work/good/Echo.swift"
out=$("$S/route" "$work/good" Echo.swift Helper.swift)
hasnt "route: a stream write has no persistence row" "$(rows "$out" Echo.swift)" "persistence"
hasnt "route: a file with no pattern has no persistence row" "$(rows "$out" Helper.swift)" "persistence"
rm "$work/good/BookCache.swift" "$work/good/Store.swift" "$work/good/Echo.swift"

cp -R "$fx/project-good" "$work/repo"
git -C "$work/repo" init -q
git -C "$work/repo" add -A
git -C "$work/repo" -c user.name=test -c user.email=test@example.com -c commit.gpgsign=false commit -qm base
printf '\n' >>"$work/repo/$view"
printf '# Notes\n' >"$work/repo/Notes.md"
out=$("$S/route" "$work/repo")
expect "route: default file set is the git change set" "$?:$(printf '%s\n' "$out" | grep '^# ' | cut -d: -f1 | paste -sd' ' -)" "0:# Notes.md # $view"
expect "route: a Markdown file has no row" "$(rows "$out" Notes.md)" "none"

cp -R "$fx/project-good" "$work/clean"
git -C "$work/clean" init -q
git -C "$work/clean" add -A
git -C "$work/clean" -c user.name=test -c user.email=test@example.com -c commit.gpgsign=false commit -qm base
planned=Packages/Features/Orders/Sources/OrdersDomain/Order.swift
reset_stub
out=$("$S/route" "$work/clean" "$view" "$planned" App/MyApp/MyApp.entitlements)
expect "route: pre-edit on a clean tree routes existing and planned files" "$?:$(called):$(printf '%s\n' "$out" | grep '^# ' | cut -d: -f1 | paste -sd' ' -)" "0:no:# $view # $planned # App/MyApp/MyApp.entitlements"
expect "route: an existing file routes by content" "$(rows "$out" "$view")" "accessibility architecture localization native-ui-patterns navigation performance security-privacy testing ui-framework"
expect "route: a planned file routes by path" "$(rows "$out" "$planned")" "architecture testing"
expect "route: a planned file routes by name" "$(rows "$out" App/MyApp/MyApp.entitlements)" "project-setup"
"$S/route" "$work/clean" ../Outside.swift >/dev/null 2>&1
expect "route: a planned path outside the project exits 2" "$?" 2
mkdir -p "$work/clean/${planned%/*}"
printf 'import Foundation\n\npublic struct Order: Sendable {\n    public let total: Decimal\n    public func formattedTotal() -> String { total.formatted(.currency(code: "USD")) }\n}\n' >"$work/clean/$planned"
out=$("$S/route" "$work/clean")
expect "route: post-edit routes the change set by content" "$?:$(rows "$out" "$planned")" "0:architecture concurrency localization testing"
has "route: post-edit prints the new reference" "$out" "references/localization.md"

# ---------- resolutions ----------
store=.ios-architecture/resolutions.jsonl
lines() { if [ -f "$1" ]; then wc -l <"$1" | tr -d ' '; else echo 0; fi; }
# resolve_all <project> <check-output> <source> <answer>: record 1 answer for each pending decision.
resolve_all() {
  printf '%s\n' "$2" | sed -n 's/^pending: \([^ ]*\): \([a-z-]*\):.*/\2 \1/p' | while read -r id file; do
    (cd "$1" && "$S/decide" --resolve "$id" "$file" --answer "$4" --source "$3" >/dev/null) || echo "resolve failed: $id $file"
  done
}

# Exit 3: the fallback answers, the record clears the check, and the rerun makes no call.
cp -R "$fx/project-good" "$work/res3"
profile "$work/res3" false
out=$("$S/check" "$work/res3" "$view")
expect "resolve: no profile permission gives exit 3" "$?" 3
err=$(cd "$work/res3" && "$S/decide" --resolve check-business-rules-in-view "$view" --answer '["no_such_label"]' --source fallback 2>&1)
expect "resolve: an invalid label is refused" "$?:$err:$(lines "$work/res3/$store")" "2:invalid answer for check-business-rules-in-view: use the labels of decisions/check-business-rules-in-view.json:0"
err=$(cd "$work/res3" && "$S/decide" --resolve check-business-rules-in-view "$view" --answer '[]' --source orchestrator 2>&1)
expect "resolve: a source that does not match the escalation is refused" "$?:$err" "2:decision check-business-rules-in-view escalates to fallback: --source orchestrator does not match"
err=$(cd "$work/res3" && "$S/decide" --resolve check-business-rules-in-view "$view" --answer '[] []' --source fallback 2>&1)
expect "resolve: an answer of 2 JSON values is refused" "$?" 2
expect "resolve: no failed resolve" "$(resolve_all "$work/res3" "$out" fallback '[]')" ""
expect "resolve: 1 record per pending decision" "$(lines "$work/res3/$store")" 2
expect "resolve: the record keys" "$(head -1 "$work/res3/$store" | jq -c '[keys, (.decision_sha256 | length), (.input_sha256 | length), .input, .source]')" '[["answer","decision","decision_sha256","input","input_sha256","source"],64,64,"'"$view"'","fallback"]'
reset_stub
out=$(TYPESAFE_API_KEY=test-key-123 "$S/check" "$work/res3" "$view")
expect "resolve: a recorded clear passes without a call" "$?:$(called)" "0:no"
expect "resolve: check prints each resolution and counts them" "$out" "resolved: $view: check-business-rules-in-view: source fallback
resolved: $view: check-personal-data-in-log: source fallback
check: 0 violations, 0 pending decisions, 2 resolved by recorded answers"

# A recorded flag still blocks.
cp -R "$fx/project-good" "$work/resflag"
profile "$work/resflag" false
out=$("$S/check" "$work/resflag" "$view")
(cd "$work/resflag" && "$S/decide" --resolve check-business-rules-in-view "$view" --answer '["business_rule_in_ui"]' --source fallback >/dev/null)
out=$("$S/check" "$work/resflag" "$view")
expect "resolve: a recorded flag is a violation" "$?" 1
has "resolve: the violation names the recorded source" "$out" "$view:7: check-business-rules-in-view: Move the rule into a pure function in the domain target, and call it from the view or the model. Recorded fallback answer. (references/architecture.md)"

# A stale record: the file changes, so the input hash changes and the decision escalates again.
printf '// logger.info("changed")\n' >>"$work/res3/$view"
out=$("$S/check" "$work/res3" "$view")
expect "resolve: a stale record escalates again" "$?:$(printf '%s\n' "$out" | grep -c '^pending: '):$(printf '%s\n' "$out" | grep -c '^resolved:')" "3:2:0"
resolve_all "$work/res3" "$out" fallback '[]' >/dev/null
expect "resolve: a new answer replaces the record of the same file" "$(lines "$work/res3/$store")" 2
jq -c '.decision_sha256 = ("0" * 64)' "$work/res3/$store" >"$work/stale.jsonl"
expect "resolve: the new records pass" "$("$S/check" "$work/res3" "$view" | tail -1)" "check: 0 violations, 0 pending decisions, 2 resolved by recorded answers"
cp "$work/stale.jsonl" "$work/res3/$store"
out=$("$S/check" "$work/res3" "$view")
expect "resolve: a record of another decision file is stale" "$?:$(printf '%s\n' "$out" | grep -c '^resolved:')" "3:0"

# A static violation wins over a resolved clear.
dbg=Packages/Features/Checkout/Sources/CheckoutFeature/Debug.swift
printf 'import os\n\nlet logger = Logger()\n\nfunc debugTotal(_ total: Int) {\n    logger.info("total \\(total)")\n    print(total)\n}\n' >"$work/res3/$dbg"
out=$("$S/check" "$work/res3" "$dbg")
resolve_all "$work/res3" "$out" fallback '[]' >/dev/null
out=$("$S/check" "$work/res3" "$dbg")
expect "resolve: a static violation wins over a resolved clear" "$?:$(printf '%s\n' "$out" | sed -nE 's/^([^ ]+:[0-9]+: [a-z0-9-]+):.*/\1/p')" "1:$dbg:7: print-log"
has "resolve: the resolved clear still shows" "$out" "resolved: $dbg: check-personal-data-in-log: source fallback"

# A security decision in the Jev band: the author (often the orchestrator) only flags; a fallback subagent clears.
mixed=$work/stub-mixed
mkdir "$mixed"
cp "$fx/responses/clear/business_rule_in_ui.json" "$fx/responses/band/number_sensitive.json" "$mixed/"
cp -R "$fx/project-good" "$work/res4"
profile "$work/res4" true
out=$(TYPESAFE_API_KEY=test-key-123 STUB_BODY=$mixed "$S/check" "$work/res4" "$view")
expect "resolve: a security decision in the Jev band escalates to fallback, not to the orchestrator" "$?:$(printf '%s\n' "$out" | grep -c 'check-personal-data-in-log: escalate=fallback tier=medium reason=below_threshold'):$(printf '%s\n' "$out" | grep -c 'escalate=orchestrator')" "3:1:0"
err=$(cd "$work/res4" && TYPESAFE_API_KEY=test-key-123 STUB_BODY=$mixed "$S/decide" --resolve check-personal-data-in-log "$view" --answer '[]' --source orchestrator 2>&1)
expect "resolve: an orchestrator clear of a security decision is refused" "$?:$err:$(lines "$work/res4/$store")" "2:decision check-personal-data-in-log is a security or privacy decision: the orchestrator can only flag it; a fallback subagent of tier medium that did not write the code clears it:0"
(cd "$work/res4" && TYPESAFE_API_KEY=test-key-123 STUB_BODY=$mixed "$S/decide" --resolve check-personal-data-in-log "$view" --answer '[]' --source fallback >/dev/null)
expect "resolve: a fallback clear of a pending security decision is recorded" "$?:$(jq -r '.source + " " + (.answer | tostring)' "$work/res4/$store")" "0:fallback []"
reset_stub
out=$(TYPESAFE_API_KEY=test-key-123 STUB_BODY=$mixed "$S/check" "$work/res4" "$view")
expect "resolve: band then fallback clear then exit 0" "$?:$(called):$(printf '%s\n' "$out" | tail -3 | paste -sd'|' -)" "0:yes:resolved: $view: check-personal-data-in-log: source fallback|decided: $view: check-business-rules-in-view: jev model jev-1.14.0|check: 0 violations, 0 pending decisions, 1 resolved by recorded answers"
expect "resolve: the rerun asks Jev only the unresolved decision" "$(cat "$STUB_LOG.calls")" business_rule_in_ui
cp "$fx/calibration/log/age-number.swift" "$work/res4/log.swift"
(cd "$work/res4" && TYPESAFE_API_KEY=test-key-123 STUB_BODY=$mixed "$S/decide" --resolve check-personal-data-in-log log.swift --answer '["number_sensitive"]' --source orchestrator >/dev/null)
expect "resolve: an orchestrator flag of a security decision is recorded" "$?:$(jq -r 'select(.input == "log.swift") | .source + " " + (.answer | tostring)' "$work/res4/$store")" '0:orchestrator ["number_sensitive"]'
out=$(TYPESAFE_API_KEY=test-key-123 STUB_BODY=$mixed "$S/check" "$work/res4" log.swift)
expect "resolve: a recorded orchestrator flag is a violation" "$?:$(printf '%s\n' "$out" | grep -c 'check-personal-data-in-log: .*Recorded orchestrator answer')" "1:1"
err=$(cd "$work/res4" && TYPESAFE_API_KEY=test-key-123 STUB_BODY=$fx/responses/flag "$S/decide" --resolve check-personal-data-in-log log.swift --answer '[]' --source fallback 2>&1)
expect "resolve: a fallback answer keeps each Jev flag" "$?:$err" '2:the answer drops a label that Jev flagged: ["number_sensitive"]'
err=$(cd "$work/res4" && TYPESAFE_API_KEY=test-key-123 STUB_BODY=$fx/responses/clear "$S/decide" --resolve check-personal-data-in-log log.swift --answer '[]' --source orchestrator 2>&1)
expect "resolve: a decision that Jev decides is not pending" "$?:$err" "2:decision check-personal-data-in-log is not pending: nothing to resolve"

# Choice and text decisions; the store falls back to the git work tree; route skips the store.
out=$(cd "$work/clean" && "$S/decide" --resolve out-of-bounds Read NFC tags --answer '"nfc"' --source fallback 2>&1)
expect "resolve: a Choice answer outside the options is refused" "$?" 2
out=$(cd "$work/clean" && "$S/decide" --resolve out-of-bounds Read NFC tags --answer '"none"' --source fallback)
expect "resolve: a no_match answer is recorded in the git work tree" "$?:$(jq -r '.input + " " + .answer' "$work/clean/$store")" "0:Read NFC tags none"
out=$(cd "$work/clean" && "$S/decide" out-of-bounds Read NFC tags)
expect "resolve: decide returns the recorded answer" "$?:$(printf '%s\n' "$out" | jq -c '[.source, .answer]')" '0:["fallback","none"]'
reset_stub
out=$("$S/route" "$work/clean")
expect "route: the resolution store has no row and no decision" "$?:$(called):$(rows "$out" "$store")" "0:no:none"
printf '{"code_may_leave_machine": false}\n' >"$work/clean/ios-architecture.json"
out=$("$S/route" "$work/clean")
expect "route: the profile has no row and no decision" "$?:$(called):$(rows "$out" ios-architecture.json):$(printf '%s\n' "$out" | grep -c '^pending:')" "0:no:none:0"
rm "$work/clean/ios-architecture.json"

# ---------- existing-app profile ----------
# An existing project holds a profile with only code_may_leave_machine.
cp -R "$fx/project-good" "$work/existing"
printf '{"code_may_leave_machine": true}\n' >"$work/existing/ios-architecture.json"
reset_stub
out=$(TYPESAFE_API_KEY=test-key-123 STUB_BODY=$fx/responses/clear "$S/check" "$work/existing" "$view")
expect "profile: check calls Jev with an existing-app profile" "$?:$(called):$(printf '%s\n' "$out" | tail -1)" "0:yes:check: 0 violations, 0 pending decisions"
reset_stub
out=$(TYPESAFE_API_KEY=test-key-123 STUB_BODY=$fx/responses/flag "$S/decide" check-business-rules-in-view "$work/existing/$view")
expect "profile: decide calls Jev with an existing-app profile" "$?:$(called):$(printf '%s\n' "$out" | jq -r .source)" "0:yes:jev"
printf '{"code_may_leave_machine": false}\n' >"$work/existing/ios-architecture.json"
reset_stub
out=$(TYPESAFE_API_KEY=test-key-123 STUB_BODY=$fx/responses/flag "$S/check" "$work/existing" "$view")
expect "profile: false in an existing-app profile escalates without a call" "$?:$(called):$(printf '%s\n' "$out" | grep -c 'reason=code_may_not_leave_machine')" "3:no:2"
printf '{}\n' >"$work/existing/ios-architecture.json"
reset_stub
out=$(TYPESAFE_API_KEY=test-key-123 STUB_BODY=$fx/responses/flag "$S/decide" check-business-rules-in-view "$work/existing/$view")
expect "profile: a profile without the field escalates without a call" "$?:$(called):$(printf '%s\n' "$out" | jq -r .reason)" "3:no:code_may_not_leave_machine"
(cd "$work/existing" && "$S/decide" --resolve check-business-rules-in-view "$view" --answer '[]' --source fallback >/dev/null)
expect "profile: the resolution store is in the folder of an existing-app profile" "$?:$(lines "$work/existing/$store")" "0:1"

# ---------- migration-sort ----------
mkdir "$work/legacy"
cp "$fx/calibration/layer/"*.swift "$work/legacy/"
out=$("$S/migration-sort" "$work/legacy")
expect "migration-sort: exit 3 with 1 pending file" "$?" 3
expect "migration-sort: grep pass" "$(printf '%s\n' "$out" | grep -v '^pending' | paste -sd' ' -)" "APIClient.swift: service (script) AppDelegate.swift: shell (script) CartTotalsTests.swift: test (script) Colors.generated.swift: none (script) Money.swift: domain (script) OrdersViewController.swift: feature (script)"
has "migration-sort: ambiguous file goes to decide" "$out" "pending: CheckoutViewController.swift: migration-layer: escalate=fallback tier=small reason=code_may_not_leave_machine; next: run scripts/decide migration-layer CheckoutViewController.swift, give only its request object to a subagent of tier small, record that answer with scripts/decide --resolve migration-layer CheckoutViewController.swift --answer <json> --source fallback, then run scripts/migration-sort again"
profile "$work/legacy" true
out=$(TYPESAFE_API_KEY=test-key-123 STUB_BODY=$fx/responses/choice "$S/migration-sort" "$work/legacy" CheckoutViewController.swift)
expect "migration-sort: Jev sorts the ambiguous file and names the model" "$?:$out" "0:CheckoutViewController.swift: feature (jev)
decided: CheckoutViewController.swift: migration-layer: jev model jev-1.14.0"

# ---------- decide ----------
d=$work/dp
mkdir "$d"
profile "$d" true
cp "$fx/project-good/$view" "$d/view.swift"
cp "$fx/calibration/log/age-number.swift" "$d/log.swift"
cp "$fx/calibration/layer/CheckoutViewController.swift" "$d/layer.swift"
printf 'struct Plain {}\n' >"$d/plain.swift"

reset_stub
out=$(TYPESAFE_API_KEY=test-key-123 STUB_BODY=$fx/responses/flag "$S/decide" check-business-rules-in-view "$d/view.swift")
expect "decide: decided exits 0" "$?" 0
expect "decide: decided result" "$(printf '%s\n' "$out" | jq -c '[.decision, .source, .model, .answer, .probabilities, has("escalate")]')" '["check-business-rules-in-view","jev","jev-1.14.0",["business_rule_in_ui"],{"business_rule_in_ui":0.98},false]'
expect "decide: key is not in curl argv" "$(grep -c test-key-123 "$STUB_LOG.argv")" 0
has "decide: curl reads its config from stdin" "$(cat "$STUB_LOG.argv")" "--config"
expect "decide: key goes to curl on stdin" "$(cat "$STUB_LOG.stdin")" 'header = "Authorization: Bearer test-key-123"'
has "decide: endpoint" "$(cat "$STUB_LOG.argv")" "https://api.typesafe.ai/v1/systemone"
hasnt "decide: key is not in the output" "$out" "test-key-123"

out=$(TYPESAFE_API_KEY=test-key-123 STUB_BODY=$fx/responses/band "$S/decide" check-personal-data-in-log "$d/log.swift")
expect "decide: a security decision below threshold exits 3" "$?" 3
expect "decide: a security decision below threshold escalates to a medium fallback" "$(printf '%s\n' "$out" | jq -c '[.source, .escalate, .fallback_tier, .reason, .answer, (.request.questions | keys)]')" '["jev","fallback","medium","below_threshold",[],["number_sensitive","public_value_sensitive"]]'

out=$(TYPESAFE_API_KEY=test-key-123 STUB_BODY=$fx/responses/clear "$S/decide" check-personal-data-in-log "$d/log.swift")
expect "decide: log check clears at a low score" "$?:$(printf '%s\n' "$out" | jq -c .answer)" "0:[]"

out=$(TYPESAFE_API_KEY=test-key-123 STUB_BODY=$fx/responses/log-low "$S/decide" check-personal-data-in-log "$d/log.swift")
expect "decide: log check clears at 0.25 or less" "$?:$(printf '%s\n' "$out" | jq -c '[.answer, has("escalate")]')" '0:[[],false]'
cp "$fx/calibration/trust/parsed-deeplink.swift" "$d/trust.swift"
out=$(TYPESAFE_API_KEY=test-key-123 STUB_BODY=$fx/responses/trust-low "$S/decide" check-trust-boundary-input "$d/trust.swift")
expect "decide: trust-boundary check clears only at 0.05 or less" "$?:$(printf '%s\n' "$out" | jq -c '[.answer, .escalate, .fallback_tier]')" '3:[[],"fallback","medium"]'
err=$(cd "$d" && TYPESAFE_API_KEY=test-key-123 STUB_BODY=$fx/responses/trust-low "$S/decide" --resolve check-trust-boundary-input trust.swift --answer '[]' --source orchestrator 2>&1)
expect "decide: an orchestrator clear of the trust-boundary check is refused" "$?:$err" "2:decision check-trust-boundary-input is a security or privacy decision: the orchestrator can only flag it; a fallback subagent of tier medium that did not write the code clears it"

reset_stub
out=$("$S/decide" check-personal-data-in-log "$d/log.swift")
expect "decide: no key exits 3 without a call" "$?:$(called)" "3:no"
expect "decide: no key result" "$(printf '%s\n' "$out" | jq -c '[.escalate, .fallback_tier, .reason, .answer]')" '["fallback","medium","no_api_key",null]'
expect "decide: escalation carries the exact question and input" "$(printf '%s\n' "$out" | jq -c '[.request.state.file.path, (.request.state.file.content | test("patient.age")), (.request.questions.number_sensitive.instructions | length > 0), (.request.thresholds | keys)]')" '["log.swift",true,true,["number_sensitive","public_value_sensitive"]]'

reset_stub
out=$(STUB_KEYCHAIN=kc-key-456 STUB_BODY=$fx/responses/clear "$S/decide" check-personal-data-in-log "$d/log.swift")
expect "decide: key from the Keychain" "$?:$(cat "$STUB_LOG.stdin")" '0:header = "Authorization: Bearer kc-key-456"'

reset_stub
out=$(TYPESAFE_API_KEY='bad key"' "$S/decide" check-business-rules-in-view "$d/view.swift")
expect "decide: invalid key exits 3 without a call" "$?:$(called):$(printf '%s\n' "$out" | jq -r .reason)" "3:no:invalid_api_key"

out=$(TYPESAFE_API_KEY=test-key-123 STUB_BODY=$fx/responses/flag STUB_CODE=500 "$S/decide" check-business-rules-in-view "$d/view.swift")
expect "decide: HTTP error escalates to fallback" "$?:$(printf '%s\n' "$out" | jq -r '[.escalate, .fallback_tier, .reason] | join(" ")')" "3:fallback small http_500"

out=$(TYPESAFE_API_KEY=test-key-123 STUB_BODY=$fx/responses/flag STUB_EXIT=28 "$S/decide" check-business-rules-in-view "$d/view.swift")
expect "decide: network error or timeout escalates to fallback" "$?:$(printf '%s\n' "$out" | jq -r .reason)" "3:network"

out=$(TYPESAFE_API_KEY=test-key-123 STUB_BODY=$fx/responses/bad "$S/decide" check-business-rules-in-view "$d/view.swift")
expect "decide: malformed answer escalates to fallback" "$?:$(printf '%s\n' "$out" | jq -r .reason)" "3:bad_response"

profile "$d" false
reset_stub
out=$(TYPESAFE_API_KEY=test-key-123 STUB_BODY=$fx/responses/flag "$S/decide" check-business-rules-in-view "$d/view.swift")
expect "decide: code_may_leave_machine false exits 3 without a call" "$?:$(called):$(printf '%s\n' "$out" | jq -r .reason)" "3:no:code_may_not_leave_machine"
rm "$d/ios-architecture.json"
out=$(TYPESAFE_API_KEY=test-key-123 STUB_BODY=$fx/responses/flag "$S/decide" check-business-rules-in-view "$d/view.swift")
expect "decide: missing profile exits 3 without a call" "$?:$(called):$(printf '%s\n' "$out" | jq -r .reason)" "3:no:code_may_not_leave_machine"
profile "$d" true

out=$(TYPESAFE_API_KEY=test-key-123 "$S/decide" check-personal-data-in-log "$d/plain.swift")
expect "decide: script pass answers without a call" "$?:$(called):$out" '0:no:{"decision":"check-personal-data-in-log","source":"script","answer":[],"probabilities":null}'

printf 'let logger = Logger()\nlogger.info("key %s%s")\n' AKIA IOSFODNN7EXAMPLE >"$d/secret.swift"
out=$(TYPESAFE_API_KEY=test-key-123 STUB_BODY=$fx/responses/flag "$S/decide" check-personal-data-in-log "$d/secret.swift")
expect "decide: a file with a secret never leaves the machine" "$?:$(called):$(printf '%s\n' "$out" | jq -r .reason)" "3:no:secret_in_input"

out=$(TYPESAFE_API_KEY=test-key-123 STUB_BODY=$fx/responses/choice "$S/decide" migration-layer "$d/layer.swift")
expect "decide: choice decided" "$?:$(printf '%s\n' "$out" | jq -c '[.answer, .probabilities.feature]')" '0:["feature",0.98]'
out=$(TYPESAFE_API_KEY=test-key-123 STUB_BODY=$fx/responses/choice-low "$S/decide" migration-layer "$d/layer.swift")
expect "decide: choice below threshold exits 4" "$?:$(printf '%s\n' "$out" | jq -r .escalate)" "4:orchestrator"
out=$(cd "$d" && TYPESAFE_API_KEY=test-key-123 STUB_BODY=$fx/responses/choice-low "$S/decide" --resolve migration-layer layer.swift --answer '"service"' --source orchestrator)
expect "decide: an orchestrator answer of a non-security decision is recorded" "$?:$(printf '%s\n' "$out" | jq -c '[.source, .answer]')" '0:["orchestrator","service"]'
out=$(TYPESAFE_API_KEY=test-key-123 STUB_BODY=$fx/responses/choice-low "$S/migration-sort" "$d" layer.swift)
expect "decide: the recorded orchestrator answer applies" "$?:$out" "0:layer.swift: service (orchestrator)"
rm "$d/$store"

reset_stub
out=$(cd "$d" && "$S/decide" out-of-bounds add a home screen widget for open orders)
expect "decide: out-of-bounds script pass" "$?:$(called):$(printf '%s\n' "$out" | jq -r '.source + " " + .answer')" "0:no:script lifecycle-extensions"
out=$(cd "$d" && TYPESAFE_API_KEY=test-key-123 STUB_BODY=$fx/responses/oob "$S/decide" out-of-bounds Let the user export all of their data as 1 file)
expect "decide: out-of-bounds below threshold exits 4" "$?:$(printf '%s\n' "$out" | jq -r '.request.state.concern')" "4:Let the user export all of their data as 1 file"
expect "decide: out-of-bounds sends the Choice and its Noul in 1 request" "$(jq -c '[.questions[].type]' "$STUB_LOG.body")" '["choice","noul"]'
expect "decide: out-of-bounds Choice has no none option" "$(jq -c '.questions.row.criteria | has("none")' "$STUB_LOG.body")" false
out=$(cd "$d" && TYPESAFE_API_KEY=test-key-123 STUB_BODY=$fx/responses/oob-row "$S/decide" out-of-bounds Remind the user of an order every morning)
expect "decide: out-of-bounds Noul high and Choice above threshold decides the row" "$?:$(printf '%s\n' "$out" | jq -c '[.source, .answer, .probabilities["lifecycle-extensions"], .probabilities.row_applies, has("escalate")]')" '0:["jev","lifecycle-extensions",0.97,0.96,false]'
out=$(cd "$d" && TYPESAFE_API_KEY=test-key-123 STUB_BODY=$fx/responses/oob-none "$S/decide" out-of-bounds Read NFC tags on product packaging)
expect "decide: out-of-bounds Noul low decides none" "$?:$(printf '%s\n' "$out" | jq -c '[.source, .answer, .probabilities.row_applies, has("escalate")]')" '0:["jev","none",0.04,false]'
out=$(cd "$d" && TYPESAFE_API_KEY=test-key-123 STUB_BODY=$fx/responses/oob-band "$S/decide" out-of-bounds Support a game controller)
expect "decide: out-of-bounds Noul in the band escalates" "$?:$(printf '%s\n' "$out" | jq -c '[.escalate, .answer, (.request.questions | keys), .request.thresholds.row_applies]')" '4:["orchestrator","lifecycle-extensions",["row","row_applies"],{"yes":0.7,"no":0.4}]'
out=$(cd "$d" && TYPESAFE_API_KEY=test-key-123 STUB_BODY=$fx/responses/oob-gate-only "$S/decide" out-of-bounds Support a game controller)
expect "decide: an answer without the companion Noul escalates to fallback" "$?:$(printf '%s\n' "$out" | jq -r .reason)" "3:bad_response"
jq 'del(.no_match)' "$S/../decisions/out-of-bounds.json" >"$work/skill/decisions/oob-no-match.json"
err=$(cd "$d" && "$work/skill/scripts/decide" oob-no-match x 2>&1)
expect "decide: a Noul in a choice decision needs no_match" "$?:$(printf '%s' "$err" | grep -c 'invalid decision file: .*/oob-no-match.json')" "2:1"
jq '.no_match = "lifecycle-extensions"' "$S/../decisions/out-of-bounds.json" >"$work/skill/decisions/oob-no-match.json"
err=$(cd "$d" && "$work/skill/scripts/decide" oob-no-match x 2>&1)
expect "decide: no_match is not a Choice option" "$?" 2
rm "$work/skill/decisions/oob-no-match.json"

"$S/decide" no-such-decision x >/dev/null 2>&1
expect "decide: unknown decision exits 2" "$?" 2
"$S/decide" ../decisions/route x >/dev/null 2>&1
expect "decide: path in decision id exits 2" "$?" 2
"$S/decide" route "$d/view.swift" "$d/log.swift" >/dev/null 2>&1
expect "decide: 2 files exit 2" "$?" 2
"$S/decide" route "$d/missing.swift" >/dev/null 2>&1
expect "decide: missing file exits 2" "$?" 2
ln -s "$d/view.swift" "$d/link.swift"
"$S/decide" route "$d/link.swift" >/dev/null 2>&1
expect "decide: symbolic link exits 2" "$?" 2

# ---------- mktemp template guard ----------
# macOS mktemp without a template ignores TMPDIR and writes in /var/folders, which a sandbox blocks.
# The shim fails unless the last argument is a path template, so a new call without one breaks this test.
mkdir -p "$work/guard"
cat >"$work/guard/mktemp" <<'EOF'
#!/bin/sh
last=
for a do last=$a; done
case $last in */*XXX) exec /usr/bin/mktemp "$@" ;; esac
printf 'mktemp without a template: %s\n' "$*" >&2
exit 97
EOF
chmod +x "$work/guard/mktemp"
gpath=$work/guard:$PATH
expect "guard: mktemp without a template fails" "$(PATH=$gpath mktemp -d 2>/dev/null; echo $?)" 97
out=$(PATH=$gpath "$S/check" "$work/good" 2>&1)
expect "guard: check uses a mktemp template" "$?:$out" "0:check: 0 violations, 0 pending decisions"
out=$(PATH=$gpath TYPESAFE_API_KEY=test-key-123 STUB_BODY=$fx/responses/route "$S/route" "$work/goodjev" Helper.swift 2>&1)
expect "guard: route uses a mktemp template" "$?" 0
hasnt "guard: route output" "$out" "mktemp without a template"
out=$(PATH=$gpath TYPESAFE_API_KEY=test-key-123 STUB_BODY=$fx/responses/flag "$S/decide" check-business-rules-in-view "$d/view.swift" 2>&1)
expect "guard: decide uses a mktemp template" "$?:$(printf '%s\n' "$out" | jq -r .source 2>/dev/null)" "0:jev"
out=$(PATH=$gpath "$S/migration-sort" "$work/legacy" Money.swift 2>&1)
expect "guard: migration-sort uses a mktemp template" "$?:$out" "0:Money.swift: domain (script)"

# ---------- decision files ----------
for spec in "$S"/../decisions/*.json; do
  id=$(basename "$spec" .json)
  expect "decisions: $id fields" "$(jq -r --arg id "$id" '[.id == $id, (.purpose | length > 0), (.primitive | IN("noul", "choice")), (.state_fields | length > 0), (.actions | length > 0), (.fallback_tier | IN("small", "medium"))] | all' "$spec")" true
  if [ "$(jq -r .input "$spec")" = file ]; then
    err=$("$S/decide" "$id" "$work/none.swift" 2>&1)
    expect "decisions: $id passes validation" "$err" "not a regular file: $work/none.swift"
  fi
  case $id in
    check-*) expect "decisions: $id has a reference per question" "$(jq '[.questions | keys[]] - (.reference | keys) | length' "$spec")" 0 ;;
  esac
done
# Code enforces the Logger redaction rule, so the log check clears at 0.25. Trust-boundary input clears at 0.05.
for row in check-personal-data-in-log:0.25 check-trust-boundary-input:0.05; do
  id=${row%:*}
  expect "decisions: $id is a security or privacy decision" "$(jq -r --argjson no "${row#*:}" '[.fallback_tier == "medium", ([.thresholds[].no] | max <= $no)] | all' "$S/../decisions/$id.json")" true
done

printf '%s passed, %s failed\n' "$pass" "$fail"
[ "$fail" -eq 0 ]
