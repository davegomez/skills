#!/bin/zsh
# usage: run.sh <version> [case[:n] ...]   n runs per model per case (default 3), 2 cases at a time
#   Existing runs are kept, so T08:5 after T08 adds runs 4 and 5 only. No cases: every frozen case at n=3.
# env: MODELS ("claude pi"), CAP_USD (6.00) hard cap on recorded Claude cost in runs/<version>/ and invalid/,
#   RESERVE_USD (0.60) per Claude run in flight; an unknown recorded cost also counts as one reserve.
# A new version freezes its candidate, rubric, cases, and harness once; a resumed batch must match them.
set -u
(( $# )) || { print -u2 "usage: run.sh <version> [case[:n] ...]"; exit 2; }
V=$1; shift
W=${0:A:h}
OUT=$W/runs/$V
F=$OUT/frozen
LOCK=/tmp/ambition-run.lock
HARNESS=(run.sh validate_grade.py eval/lint.py eval/jev_grade.py)
CAP_USD=${CAP_USD:-6.00}
RESERVE_USD=${RESERVE_USD:-0.60}
models=(${=MODELS:-claude pi})
NUM='^[0-9]+(\.[0-9]+)?([eE][-+]?[0-9]+)?$'
[[ $V =~ '^[A-Za-z0-9][A-Za-z0-9._-]*$' ]] || { print -u2 "bad version $V"; exit 2; }
[[ $CAP_USD =~ $NUM && $RESERVE_USD =~ $NUM ]] || { print -u2 "CAP_USD and RESERVE_USD must be numbers"; exit 2; }
for m in $models; do [[ $m == (claude|pi) ]] || { print -u2 "unknown model $m"; exit 2; }; done
(( ${#models} )) || { print -u2 "MODELS is empty"; exit 2; }
(( ${models[(I)claude]} == 0 )) || command -v jq > /dev/null || { print -u2 "jq is required for Claude runs"; exit 2; }

# one batch at a time: batches share /tmp/ambition-runner and /tmp/ambition-skill
mkdir $LOCK 2>/dev/null || { print -u2 "another batch is running ($LOCK; remove it if no run.sh is alive)"; exit 1; }
pids=()
trap 'rm -f $OUT/.inflight.*(N); rmdir $LOCK 2>/dev/null' EXIT
trap 'for p in $pids; do pkill -TERM -P $p; kill $p; done 2>/dev/null; wait; exit 130' INT TERM

freeze() {
  mkdir -p $F/cases $F/harness/eval || return 1
  cp $W/SKILL.$V.md $F/SKILL.md && cp $W/rubric.md $F/rubric.md && cp $W/cases/*.txt $F/cases/ || return 1
  local h; for h in $HARNESS; do cp $W/$h $F/harness/$h || return 1; done
  (cd $F && shasum -a 256 SKILL.md rubric.md cases/*.txt harness/${^HARNESS} > SHA256)
}
mkdir -p $OUT/invalid
[[ -d $F ]] || freeze || { rm -rf $F; print -u2 "freeze failed"; exit 1; }
(cd $F && shasum -a 256 -c --quiet SHA256) || { print "frozen inputs changed"; exit 1; }
for h in $HARNESS; do [[ ! -f $F/harness/$h ]] || cmp -s $W/$h $F/harness/$h || print "warning: $h differs from frozen/harness/$h"; done

# requested runs: case -> n; a repeated case keeps the largest n
typeset -A want
order=()
if (( $# )); then specs=($@); else specs=(${(f)"$(cd $F/cases && print -l *.txt | sed 's/\.txt$//')"}); fi
for s in $specs; do
  c=${s%%:*}; n=3; [[ $s == *:* ]] && n=${s#*:}
  [[ $c =~ '^T[0-9][0-9]$' && -f $F/cases/$c.txt ]] || { print -u2 "unknown case $c"; exit 2; }
  [[ $n =~ '^[1-9][0-9]?$' ]] || { print -u2 "bad run count in $s"; exit 2; }
  (( ${+want[$c]} )) || order+=($c)
  (( n > ${want[$c]:-0} )) && want[$c]=$n
done

cp $F/SKILL.md /tmp/ambition-runner/.claude/skills/be-ambitious/SKILL.md || exit 1
cp $F/SKILL.md /tmp/ambition-skill/be-ambitious/SKILL.md || exit 1
cmp -s $F/SKILL.md /tmp/ambition-runner/.claude/skills/be-ambitious/SKILL.md && cmp -s $F/SKILL.md /tmp/ambition-skill/be-ambitious/SKILL.md || { print "installed skill differs"; exit 1; }
[[ -f $OUT/MANIFEST ]] || { print "claude $(claude --version)"; print "pi $(pi --version 2>&1 | tail -1)"; } > $OUT/MANIFEST
rm -f $OUT/DONE

claude_cost() { # recorded Claude cost of this batch, valid and invalid attempts; an unknown cost counts as one reserve
  local f v total=0.0
  for f in $OUT/*-claude-*.md.meta(N) $OUT/invalid/*-claude-*.meta(N); do
    v=$(sed -n 's/^cost_usd=\([^ ]*\).*/\1/p' $f | head -1)
    if [[ $v =~ $NUM ]]; then total=$(( total + v )); else total=$(( total + RESERVE_USD )); fi
  done
  print $total
}

USAGE_JQ='"cost_usd=\(.total_cost_usd // .cost_usd // "unknown") input_tokens=\(.usage.input_tokens // "unknown") output_tokens=\(.usage.output_tokens // "unknown") cache_creation_input_tokens=\(.usage.cache_creation_input_tokens // "unknown") cache_read_input_tokens=\(.usage.cache_read_input_tokens // "unknown") num_turns=\(.num_turns // "unknown") is_error=\(if has("is_error") then .is_error else "unknown" end)"'

gen() { # gen <case> <model> <n> <task>; writes to a temp name, publishes only a complete run
  local id=$1-$2-$3 task=$4 t=$OUT/.tmp.$1-$2-$3.$$ rc u
  [[ -f $OUT/$id.md ]] && return 0
  cd /tmp/ambition-runner || return 1
  if [[ $2 == claude ]]; then
    claude -p --setting-sources project --strict-mcp-config --tools "" --no-session-persistence --model claude-opus-5-5 --effort high --output-format json "/be-ambitious${task:+ $task}" > $t.json 2> $t.err; rc=$?
    jq -r 'if .is_error == false and (.result | type) == "string" then .result else empty end' $t.json > $t 2>> $t.err
    print "model=claude-opus-5-5 effort=high tools=none settings=project(empty) mcp=strict output=json" > $t.meta
    u=$(jq -r $USAGE_JQ $t.json 2>/dev/null); print -r -- "${u:-cost_usd=unknown}" >> $t.meta
  else
    PI_CODING_AGENT_DIR=/tmp/pi-clean-agent pi -p --no-session -ne -nc -ns -np --no-tools --model openai/gpt-6.1-sol --thinking high --skill /tmp/ambition-skill/be-ambitious "/skill:be-ambitious${task:+ $task}" > $t 2> $t.err; rc=$?
    print "model=openai/gpt-6.1-sol thinking=high tools=none extensions=none context-files=none agent-dir=/tmp/pi-clean-agent" > $t.meta
  fi
  print "exit=$rc bytes=$(wc -c < $t) skill_sha=$(head -c 64 $F/SHA256)" >> $t.meta
  local -a visible_entries=(*(N))
  print "session (captured by the harness): cwd=$PWD; git rev-parse in cwd: $(git -C $PWD rev-parse --is-inside-work-tree 2>&1 | head -1); visible entries in cwd: ${#visible_entries}; date=$(date -u +%Y-%m-%d); os=$(uname -s)${${2:#pi}:+; Claude Code base prompt includes cwd, git-repo status, platform, and date}" >> $t.meta
  if (( rc != 0 )) || ! grep -q '[^[:space:]]' $t; then
    local s=$(date +%s); mv $t $OUT/invalid/$id.$s.md; mv $t.err $OUT/invalid/$id.$s.err; mv $t.meta $OUT/invalid/$id.$s.meta
    [[ -f $t.json ]] && mv $t.json $OUT/invalid/$id.$s.json
  else
    [[ -f $t.json ]] && mv $t.json $OUT/$id.md.json
    mv $t.err $OUT/$id.md.err; mv $t.meta $OUT/$id.md.meta; mv $t $OUT/$id.md
  fi
  rm -f $OUT/.inflight.$id
}

i=0 skipped=0
for c in $order; do
  task=$(<$F/cases/$c.txt)
  for k in {1..$want[$c]}; do
    for m in $models; do
      id=$c-$m-$k
      [[ -f $OUT/$id.md ]] && continue
      if [[ $m == claude ]]; then
        inflight=($OUT/.inflight.*(N)); spent=$(claude_cost)
        if (( spent + RESERVE_USD * (${#inflight} + 1) > CAP_USD )); then
          printf 'cap reached: skip %s (recorded $%.2f + reserve $%.2f x %d > cap $%.2f)\n' $id $spent $RESERVE_USD $(( ${#inflight} + 1 )) $CAP_USD
          (( ++skipped )); continue
        fi
        : > $OUT/.inflight.$id
      fi
      gen $c $m $k "$task" & pids+=($!)
    done
  done
  (( ++i % 2 == 0 )) && wait
done
wait
missing=0
for c in $order; do for k in {1..$want[$c]}; do for m in $models; do [[ -f $OUT/$c-$m-$k.md ]] || (( ++missing )); done; done; done
v=($OUT/T*.md(N)); x=($OUT/invalid/*.md(N))
print "valid: ${#v}  invalid attempts: ${#x}  skipped at cap: $skipped  requested but missing: $missing"
printf 'claude cost recorded for %s: $%.2f of cap $%.2f (unknown costs counted at $%.2f)\n' $V $(claude_cost) $CAP_USD $RESERVE_USD
(( missing == 0 )) && touch $OUT/DONE
