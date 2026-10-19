"""Deterministic phrase checks on one be-ambitious output.

usage: python3 -I lint.py <case> <output-file>     prints JSON
       python3 -I lint.py --selftest
<case> is T1..T99 or T01..T99; the case task is read from ../cases/T<NN>.txt.
"""
import json
import re
import sys
from pathlib import Path
from typing import TypedDict

ROOT = Path(__file__).resolve().parent.parent
FENCE = re.compile(r"^(`{3,}|~{3,})[^\n]*\n(.*?)\n?\1[ \t]*$", re.S | re.M)
WRAPPER = "/be-ambitious"
LCP_TARGET_BELOW_S = 2.5
T13_TARGET_MAX_S = 18 * 60
REQUIRED_LITERALS = {"T1": ("—", '"—"'), "T5": ("category,count,evidence_ids",)}
STOPWORDS = frozenset(
    "about after again also and any are because been before being both but can could does doing done each from have into its just more most must only other our over same should some such than that the their them then there these they this those through under until very want what when where which while will with within without would your you not may".split()
)


class Result(TypedDict):
    status: str
    quote: str


class Split(TypedDict):
    prompt: str | None
    before: str
    ledger: str


def case_id(raw: str) -> str:
    m = re.fullmatch(r"T0*(\d{1,2})", raw.strip(), re.I)
    if not m or not 1 <= int(m.group(1)) <= 99:
        raise ValueError(f"unknown case {raw!r}")
    return f"T{int(m.group(1))}"


def split_reply(reply: str) -> Split:
    m = FENCE.search(reply)
    if not m:
        return {"prompt": None, "before": "", "ledger": reply.strip()}
    return {"prompt": m.group(2), "before": reply[: m.start()].strip(), "ledger": reply[m.end() :].strip()}


def strip_wrapper(task: str) -> str:
    task = task.strip()
    return task[len(WRAPPER) :].strip() if task.startswith(WRAPPER) else task


def nonempty(text: str) -> list[str]:
    return [line for line in text.splitlines() if line.strip()]


def unchanged_lines(reply: str) -> list[str]:
    return [line for line in reply.splitlines() if line.startswith("Unchanged:")]


def r(status: str, quote: str = "") -> Result:
    return {"status": status, "quote": quote}


def l1_judge_last(case: str, reply: str) -> Result:
    if case == "T10" or unchanged_lines(reply):
        return r("na")
    prompt = split_reply(reply)["prompt"]
    if prompt is None:
        return r("fail", "no fenced prompt")
    lines = nonempty(prompt)
    if not lines:
        return r("fail", "empty prompt")
    if lines[-1].startswith("Judge:"):
        return r("pass", lines[-1][:120])
    last_para = re.split(r"\n[ \t]*\n", prompt.strip())[-1]
    if last_para.startswith("Judge:"):
        return r("pass", "last paragraph: " + last_para.splitlines()[0][:110])
    return r("fail", lines[-1][:120])


_INFERRED_GOAL = re.compile(r"\b(inferred|assumed)\s+(higher\s+|owner\s+|decision\s+)?(goal|outcome|purpose|aim)\b", re.I)
_LEDGER_ASSUMPTION = re.compile(r"\bassumption lines?\b|\b(inferred|assumed)\s+(higher\s+|owner\s+|decision\s+)?(goal|outcome|purpose|aim)\b", re.I)


def _bare(line: str) -> str:
    return re.sub(r"^\s*(?:[-*]|\d+[.)])?\s*", "", line)


def l2_assumption_prefix(case: str, reply: str) -> Result:
    """Best effort: catches goal lines that say 'inferred/assumed goal' without the prefix, and a ledger
    that cites an inferred goal or Assumption lines while the prompt has none. It cannot see an inferred
    goal written as a plain statement ('Goal: ...'), which is the common B3 failure."""
    parts = split_reply(reply)
    prompt = parts["prompt"]
    if case == "T10" or prompt is None or unchanged_lines(reply):
        return r("na")
    lines = [_bare(line) for line in nonempty(prompt)]
    has_prefix = any(line.startswith("Assumption:") for line in lines)
    unlabeled = [line for line in lines if _INFERRED_GOAL.search(line) and not line.startswith("Assumption:")]
    if unlabeled:
        return r("fail", unlabeled[0][:120])
    cited = _LEDGER_ASSUMPTION.search(parts["ledger"])
    if cited and not has_prefix:
        return r("fail", "ledger cites '" + cited.group(0) + "' but no prompt line starts with Assumption:")
    if has_prefix or cited:
        return r("pass", next((line[:120] for line in lines if line.startswith("Assumption:")), ""))
    return r("na")


def l3_literals(case: str, reply: str) -> Result:
    wanted = REQUIRED_LITERALS.get(case)
    if not wanted:
        return r("na")
    prompt = split_reply(reply)["prompt"] or ""
    missing = [lit for lit in wanted if lit not in prompt]
    return r("fail", "missing: " + " | ".join(missing)) if missing else r("pass", " | ".join(wanted))


def l4_unchanged_shape(case: str, reply: str, task: str) -> Result:
    marks = unchanged_lines(reply)
    if case == "T10" or not marks:
        return r("na")
    m = FENCE.search(reply)
    if not m:
        return r("fail", "Unchanged: line without a fenced block")
    rest = nonempty(reply[: m.start()] + reply[m.end() :])
    if rest != marks[:1] or len(marks) != 1:
        return r("fail", "extra text outside the block: " + " / ".join(x[:60] for x in rest if x not in marks[:1])[:120])
    if strip_wrapper(m.group(2)) != strip_wrapper(task):
        return r("fail", "block differs from the case task")
    return r("pass", marks[0][:120])


def l5_t10_one_line(case: str, reply: str) -> Result:
    if case != "T10":
        return r("na")
    lines = nonempty(reply)
    if len(lines) != 1:
        return r("fail", f"{len(lines)} non-empty lines")
    line = lines[0].strip()
    ok = re.search(r"\bwhich\b.*\b(task|prompt)\b.*\?$", line, re.I)
    return r("pass" if ok else "fail", line[:120])


_TARGET = re.compile(r"(\d+(?:[.,]\d+)?)\s*(ms|milliseconds?|s|sec|seconds?)\b", re.I)


def lcp_target_seconds(line: str) -> float | None:
    at = line.upper().find("LCP")
    if at < 0:
        return None
    m = _TARGET.search(line, at)
    if not m:
        return None
    value = float(m.group(1).replace(",", "." if m.group(2).lower().startswith("s") else ""))
    return value / 1000 if m.group(2).lower().startswith("m") else value


_DURATION = re.compile(r"(\d{1,3}(?:,\d{3})+|\d+(?:\.\d+)?)\s*-?\s*(seconds?|secs?|s|minutes?|mins?|hours?|hrs?|h)\b", re.I)
_UNIT_S = {"s": 1, "m": 60, "h": 3600}


def duration_seconds(line: str) -> float | None:
    """Smallest duration on the line: '15 minutes', '1 hour', '0.3 h', '900 s'."""
    found = [float(m.group(1).replace(",", "")) * _UNIT_S[m.group(2)[0].lower()] for m in _DURATION.finditer(line)]
    return min(found) if found else None


# case -> (target parser, what it parses, pass test, quote label)
AIM_RULES = {
    "T11": (lcp_target_seconds, "LCP number", lambda v: v < LCP_TARGET_BELOW_S, "lcp_target_s"),
    "T13": (duration_seconds, "duration", lambda v: v <= T13_TARGET_MAX_S, "target_s"),
}


def l6_aim(case: str, reply: str) -> Result:
    if case not in AIM_RULES:
        return r("na")
    parse, what, ok, name = AIM_RULES[case]
    prompt = split_reply(reply)["prompt"] or ""
    aims = [line.strip() for line in prompt.splitlines() if re.search(r"\baim for\b", line, re.I)]
    if not aims:
        return r("fail", "no 'Aim for' line in the prompt")
    found = [(parse(line[re.search(r"\baim for\b", line, re.I).start() :]), line) for line in aims]
    parsed = [(v, line) for v, line in found if v is not None]
    if not parsed:
        return r("fail", f"Aim for line has no {what}: " + aims[0][:100])
    best = min(parsed)
    return r("pass" if ok(best[0]) else "fail", f"{name}={best[0]:g}: {best[1][:100]}")


def prohibition_sentences(task: str) -> list[str]:
    sentences = re.split(r"(?<=[.!?])\s+|\n+", strip_wrapper(task))
    pat = re.compile(r"^(Do not|You may not|No )|^Keep\b.*\bunchanged\b", re.S)
    return [s.strip() for s in sentences if pat.search(s.strip())]


def content_words(text: str) -> set[str]:
    return {w for w in re.findall(r"[a-z][a-z-]{3,}", text.lower()) if w not in STOPWORDS}


def l7_approval_overlap(case: str, reply: str, task: str) -> Result:
    """A hint for review, never a failure: approval lines that reuse words of a prohibition."""
    prompt = split_reply(reply)["prompt"] or ""
    approvals = [_bare(line) for line in prompt.splitlines() if _bare(line).startswith("With my approval only:")]
    prohibited = prohibition_sentences(task)
    if not approvals or not prohibited:
        return r("na")
    banned = set().union(*(content_words(s) for s in prohibited))
    hits = []
    for line in approvals:
        shared = sorted(content_words(line.removeprefix("With my approval only:")) & banned)
        if shared:
            hits.append(f"{','.join(shared)} <- {line[22:80].strip()}")
    return r("flag", " || ".join(hits)[:300]) if hits else r("pass")


_ROLE = re.compile(r"\b(reviewer|analyst|coder|auditor|editor|reader|colleague|engineer|expert|panel)s?\b", re.I)


def roles(text: str) -> set[str]:
    return {m.group(1).lower() for m in _ROLE.finditer(text)}


def l8_reviewer_first_check(case: str, reply: str) -> Result:
    """A hint for review, never a failure: a reviewer role in the Judge line with no First check line naming it."""
    prompt = split_reply(reply)["prompt"]
    if case == "T10" or prompt is None or unchanged_lines(reply):
        return r("na")
    lines = [_bare(line) for line in prompt.splitlines()]
    judges = [line for line in lines if line.startswith("Judge:")]
    wanted = roles(judges[-1]) if judges else set()
    if not wanted:
        return r("na")
    checked = set().union(*(roles(line) for line in lines if re.match(r"First checks?:", line)))
    missing = sorted(wanted - checked)
    return r("flag", "no First check for: " + ", ".join(missing)) if missing else r("pass", ", ".join(sorted(wanted)))


def lint(case: str, reply: str, task: str) -> dict[str, Result]:
    case = case_id(case)
    return {
        "L1": l1_judge_last(case, reply),
        "L2": l2_assumption_prefix(case, reply),
        "L3": l3_literals(case, reply),
        "L4": l4_unchanged_shape(case, reply, task),
        "L5": l5_t10_one_line(case, reply),
        "L6": l6_aim(case, reply),
        "L7": l7_approval_overlap(case, reply, task),
        "L8": l8_reviewer_first_check(case, reply),
    }


def case_task(case: str) -> str:
    return (ROOT / "cases" / f"T{int(case_id(case)[1:]):02d}.txt").read_text(encoding="utf-8")


def _selftest() -> None:
    task = 'Fix f. Return "—" for null. Do not add dependencies or contact customers.'
    changed = '```text\nFix f, return "—".\nAssumption: the goal is fewer crashes.\nWith my approval only: add dependencies for parsing.\nJudge: tests go red then green.\n```\n\n- `depth`: inferred goal stated.\n'
    out = lint("T1", changed, task)
    assert out["L1"]["status"] == "pass", out["L1"]
    assert out["L2"]["status"] == "pass", out["L2"]
    assert out["L3"]["status"] == "pass", out["L3"]
    assert out["L4"]["status"] == "na" and out["L5"]["status"] == "na" and out["L6"]["status"] == "na"
    assert out["L7"]["status"] == "flag" and "dependencies" in out["L7"]["quote"], out["L7"]
    assert lint("T1", changed.replace("Judge: tests go red then green.\n", "\nJudge: red/green.\nReport results.\n"), task)["L1"]["status"] == "pass"
    assert lint("T1", changed.replace("Judge: tests go red then green.\n", "Judge: red/green.\nReport results.\n"), task)["L1"]["status"] == "fail"
    assert lint("T1", changed.replace("Judge: tests go red then green.\n", "Judge: red/green.\n\nReport results.\n"), task)["L1"]["status"] == "fail"
    assert lint("T1", changed.replace("Assumption: the goal", "The inferred goal"), task)["L2"]["status"] == "fail"
    assert lint("T1", changed.replace("Assumption:", "Goal:"), task)["L2"]["status"] == "fail"
    assert lint("T1", changed.replace('"—"', "a dash"), task)["L3"]["status"] == "fail"
    same = f"```text\n{task}\n```\n\nUnchanged: already complete.\n"
    out = lint("T01", same, "/be-ambitious " + task)
    assert out["L4"]["status"] == "pass" and out["L1"]["status"] == "na", out
    assert lint("T1", same + "Tell me if you want more.\n", task)["L4"]["status"] == "fail"
    assert lint("T1", same.replace("Fix f.", "Fix g."), task)["L4"]["status"] == "fail"
    assert lint("T10", "Which task should I make more ambitious?\n", "")["L5"]["status"] == "pass"
    assert lint("T10", "Which task should I make more ambitious?\nPaste it here.", "")["L5"]["status"] == "fail"
    assert lint("T10", "What do you mean?", "")["L5"]["status"] == "fail"
    t11 = "```\nMeasure.\nAim for mobile LCP of {} using critical-path work.\nJudge: before/after.\n```\n"
    assert lint("T11", t11.format("2.0 s"), "")["L6"] == {"status": "pass", "quote": "lcp_target_s=2: Aim for mobile LCP of 2.0 s using critical-path work."}
    assert lint("T11", t11.format("1,800 ms"), "")["L6"]["quote"].startswith("lcp_target_s=1.8")
    assert lint("T11", t11.format("≤ 2.5 seconds"), "")["L6"]["status"] == "fail"
    assert lint("T11", t11.replace("LCP of {}", "a 50% cut"), "")["L6"]["status"] == "fail"
    assert prohibition_sentences("A. Do not x. You may not y. No z. Keep a and b unchanged. Use c.") == ["Do not x.", "You may not y.", "No z.", "Keep a and b unchanged."]
    assert split_reply("no fence")["prompt"] is None
    t13 = "```\nProfile the DAG.\nAim for {} end to end using the critical path and EXPLAIN ANALYZE.\nJudge: before/after runtime under 3 hours.\n```\n"
    for target, status in (("15 minutes", "pass"), ("0.3 h", "pass"), ("18-minute", "pass"), ("1,080 seconds", "pass"),
                           ("1 hour", "fail"), ("2 hours, not 3 hours,", "fail"), ("20 min", "fail")):
        assert lint("T13", t13.format(target), "")["L6"]["status"] == status, (target, lint("T13", t13.format(target), "")["L6"])
    assert lint("T13", t13.format("15 minutes"), "")["L6"]["quote"].startswith("target_s=900: Aim for 15 minutes")
    assert lint("T13", t13.format("a big cut"), "")["L6"]["status"] == "fail"
    assert lint("T13", t13.replace("Aim for", "Try"), "")["L6"]["quote"] == "no 'Aim for' line in the prompt"
    assert lint("T12", t13, "")["L6"]["status"] == "na"
    t8 = "```\nEvaluate.\n{}\nJudge: an independent analyst and a domain expert check the rubric. Pass only if every criterion is met.\n```\n"
    assert lint("T8", t8.format("First check: the independent analyst and an expert are available and may see the data."), "")["L8"]["status"] == "pass"
    flag = lint("T8", t8.format("- First checks: the analyst is available."), "")["L8"]
    assert flag == {"status": "flag", "quote": "no First check for: expert"}, flag
    assert lint("T8", t8.format("The expert must be available."), "")["L8"]["status"] == "flag"
    assert lint("T8", t8.replace("an independent analyst and a domain expert check", "I check"), "")["L8"]["status"] == "na"
    assert lint("T8", same, "")["L8"]["status"] == "na" and lint("T10", "Which task?", "")["L8"]["status"] == "na"
    assert case_id("T13") == "T13" and case_id("T14") == "T14"
    assert lint("T14", "```\nFix h.\n```\n\nUnchanged: done.\n", "Fix h.")["L6"]["status"] == "na"
    try:
        case_id("T100")
    except ValueError:
        pass
    else:
        raise AssertionError("accepted T100")
    print("selftest ok")


if __name__ == "__main__":
    if sys.argv[1:] == ["--selftest"]:
        _selftest()
        sys.exit(0)
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    case, path = sys.argv[1], sys.argv[2]
    try:
        result = lint(case, Path(path).read_text(encoding="utf-8"), case_task(case))
    except (OSError, ValueError) as e:
        sys.exit(f"lint: {type(e).__name__}: {e}")
    print(json.dumps({"case": case_id(case), "file": Path(path).name, "checks": result}, ensure_ascii=False))
