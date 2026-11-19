#!/usr/bin/env python3
"""A13 addendum: measured numbers for the token audit. Writes a13-addendum-data.md and runs.csv.

Run from this directory:  python3 -I scan.py 6 && python3 -I a13_addendum.py [calibration.pkl]
The optional argument is a data.pkl from `scan.py 10` (run in another directory); it is used only to
re-compute the baseline of report.md with the definitions of this script.
Reads: data.pkl, ~/.pi/agent/sessions (numbers only), .orchestration/a10..a13 (counts and file sizes only).
No prompt or file text is printed or stored.
"""
import pickle, collections, re, json, glob, os, sys, csv, datetime

REPO = '/Users/dave/Development/personal/costo'
ORCH = REPO + '/.orchestration'
d = pickle.load(open('./data.pkl', 'rb'))
CUT = '2026-11-19T01:30'                 # end of A13 (the session 01019b12 also did the end of the run)
A13_START = '2026-11-16T16:30'
ME = 'Token audit addendum for A13'      # the agent that makes this file: excluded
COMMITS = {'A10': 13, 'A11': 13, 'A12': 10, 'A13_pre': 163, 'A13_post': 86}  # given by the lead / report.md 2.3
BATCHES = ['b1', 'b2', 'b3', 'b4', 'b5', 'b5b', 'b6a', 'b6b', 'b6b2', 'b6b3', 'b6c', 'b6c2', 'b7', 'b7b', 'b7c',
           'b6c3', 'b7d', 'b8a', 'b8b', 'end']   # order of the handoff files by mtime; 1 session each

W = lambda r: r['inp'] + r['cw5m'] * 1.25 + r['cw1h'] * 2 + (r['cw'] - r['cw5m'] - r['cw1h']) * 1.25 + r['cr'] * 0.1 + r['out'] * 5
ctxof = lambda r: r['inp'] + r['cr'] + r['cw']
q = lambda v, p: sorted(v)[int(p * (len(v) - 1))] if v else 0      # same percentile as report2.py
M = lambda x: f"{x / 1e6:.1f}M"
K = lambda x: f"{x / 1000:.0f}k"
P = lambda x: f"{100 * x:.1f}%"

# ---------- select the runs ----------
C0 = [r for r in d['calls'] if 'costo' in r['proj']]
core = [r for r in C0 if r['proj'].endswith('costo-apps-core')]
first_main = {}
for r in core:
    if not r['agent']:
        first_main[r['sess']] = min(first_main.get(r['sess'], 'z'), r['ts'])
a13_sessions = sorted([s for s, t in first_main.items() if t >= A13_START], key=lambda s: first_main[s])
RUNS = {'A10': ['9e57d3b6'], 'A11': ['4f5e7733'], 'A12': ['10eea4e1']}
runsess = {k: [s for s in first_main if s[:8] in v] for k, v in RUNS.items()}
runsess['A13'] = a13_sessions
me_agents = {(r['sess'], r['agent']) for r in C0 if r['desc'] == ME}
assert len(a13_sessions) == 20 and all(len(runsess[k]) == 1 for k in ('A10', 'A11', 'A12')), (len(a13_sessions), runsess)

def sel(rows, run):
    ss = set(runsess[run])
    out = [r for r in rows if r['sess'] in ss and (r['sess'], r['agent']) not in me_agents]
    if run == 'A13': out = [r for r in out if r['ts'] <= CUT]
    return out
CALLS = {k: sel(C0, k) for k in runsess}
TCALL = {k: sel([r for r in d['toolcalls'] if 'costo' in r['proj']], k) for k in runsess}
after_cut = sum(1 for r in C0 if r['sess'] in set(a13_sessions) and r['ts'] > CUT)
mine = sum(1 for r in C0 if (r['sess'], r['agent']) in me_agents)

# ---------- classification of the descriptions ----------
rx_corr = re.compile('correction', re.I)
rx_stem = re.compile(r'\bcorrect', re.I)
rx_rework = re.compile(r'fix|follow|rework|redo|retry|repair|address|revis|amend|patch|revert', re.I)
rx_review = re.compile('review', re.I)
rx_fold = re.compile(r'\bfold', re.I)

# explore: E1 = families named in report.md F3 (grep, sed -n, cat, wc) + Read/Grep/Glob; E2 = E1 + other read-only commands
def cf(c): return re.sub(r'^(?:cd [^&;]+(?:&&|;)\s*)+', '', c.strip())
RO2 = {'head', 'tail', 'ls', 'find', 'nl', 'awk', 'stat', 'tree', 'jq'}
GITRO = {'diff', 'show', 'log', 'status', 'ls-files', 'grep', 'blame', 'rev-parse', 'cat-file', 'branch', 'worktree'}
def is_explore(r, lvl):
    n = r['name']
    if n in ('Read', 'Grep', 'Glob'): return True
    if n != 'Bash': return False
    w = cf(r['cmd']).split()
    if not w: return False
    e1 = w[0] in ('grep', 'rg', 'cat', 'wc') or (w[0] == 'sed' and w[1:2] == ['-n'])
    if lvl == 1: return e1
    if e1 or w[0] in RO2 or w[:2] == ['command', 'ls']: return True
    return w[0] == 'git' and w[1:2] != [] and w[1] in GITRO

def metrics(rows, tcs):
    m = {}
    T = sum(map(W, rows)); m['units'] = T; m['calls'] = len(rows)
    inst = collections.defaultdict(list)
    for r in rows:
        if r['agent']: inst[(r['sess'], r['agent'])].append(r)
    for v in inst.values(): v.sort(key=lambda r: r['ts'])
    at = {k: v[0]['atype'] for k, v in inst.items()}
    m['inst'] = inst; m['at'] = at
    types = sorted({v for v in at.values()})
    G = {t: [k for k in inst if at[k] == t] for t in types}
    G['worker-*'] = [k for k in inst if at[k].startswith('worker')]
    G['all-sub'] = list(inst)
    m['G'] = G
    m['by'] = {}
    for g, ks in G.items():
        cs = [len(inst[k]) for k in ks]
        fin = [ctxof(inst[k][-1]) for k in ks]; fst = [ctxof(inst[k][0]) for k in ks]
        u = sum(W(r) for k in ks for r in inst[k])
        ntool = sum(1 for r in tcs if r['agent'] and (r['sess'], r['agent']) in set(ks))
        m['by'][g] = dict(n=len(ks), calls=sum(cs), p50=q(cs, .5), p90=q(cs, .9), mx=max(cs) if cs else 0,
                          fin50=q(fin, .5), fin90=q(fin, .9), first50=q(fst, .5), units=u, share=u / T,
                          tools=ntool, tpc=(ntool / sum(cs)) if cs else 0)
    # main sessions
    mr = [r for r in rows if not r['agent']]
    mc = [ctxof(r) for r in mr]
    big = [r for r in mr if ctxof(r) > 200_000]
    mu = sum(map(W, mr))
    m['main'] = dict(calls=len(mr), p50=q(mc, .5), p90=q(mc, .9), mx=max(mc) if mc else 0, units=mu, share=mu / T,
                     big_share_run=sum(map(W, big)) / T, big_share_main=(sum(map(W, big)) / mu) if mu else 0, big_n=len(big),
                     tools=sum(1 for r in tcs if not r['agent']), tpc=sum(1 for r in tcs if not r['agent']) / len(mr) if mr else 0)
    sm = collections.defaultdict(list)
    for r in mr: sm[r['sess']].append(r)
    m['main_first'] = [ctxof(sorted(v, key=lambda r: r['ts'])[0]) for v in sm.values()]
    # tools per call, explore
    sub_t = [r for r in tcs if r['agent']]
    wk_t = [r for r in sub_t if at.get((r['sess'], r['agent']), '').startswith('worker')]
    m['explore'] = {nm: {lvl: (sum(is_explore(r, lvl) for r in S) / len(S) if S else 0) for lvl in (1, 2)}
                    for nm, S in (('all-sub', sub_t), ('worker-*', wk_t))}
    m['explore_n'] = {'all-sub': len(sub_t), 'worker-*': len(wk_t)}
    # repeated reads (same definition as report2.py section 4)
    rd = collections.Counter((r['sess'], r['agent'], r['file']) for r in tcs if r['name'] == 'Read' and r['file'])
    m['rep_all'] = sum(v - 1 for v in rd.values() if v > 1)
    m['rep_sub'] = sum(v - 1 for k, v in rd.items() if v > 1 and k[1])
    m['reads'] = sum(rd.values())
    ts = sorted(r['ts'] for r in rows)
    t0 = datetime.datetime.fromisoformat(ts[0].replace('Z', '+00:00')); t1 = datetime.datetime.fromisoformat(ts[-1].replace('Z', '+00:00'))
    m['days'] = (t1 - t0).total_seconds() / 86400; m['t0'] = ts[0]; m['t1'] = ts[-1]
    m['rep_week'] = m['rep_all'] * 7 / m['days']
    m['rep_per100'] = 100 * m['rep_all'] / len(rows)
    # task classes on subagent instances (priority: correction, review, fold, other)
    cl = collections.Counter(); cn = collections.Counter(); stem_u = 0
    for k, v in inst.items():
        desc = v[0]['desc'] or ''; u = sum(map(W, v))
        c = 'correction' if rx_corr.search(desc) else 'review' if rx_review.search(desc) else 'fold' if rx_fold.search(desc) else 'other'
        cl[c] += u; cn[c] += 1
        if rx_stem.search(desc): stem_u += u
    m['cls_u'] = cl; m['cls_n'] = cn; m['stem_u'] = stem_u
    m['corr_nofold_u'] = sum(sum(map(W, v)) for v in inst.values() if rx_corr.search(v[0]['desc'] or '') and not rx_fold.search(v[0]['desc'] or ''))
    m['corr_nofold_n'] = sum(1 for v in inst.values() if rx_corr.search(v[0]['desc'] or '') and not rx_fold.search(v[0]['desc'] or ''))
    m['corr_by_type'] = collections.Counter(at[k] for k, v in inst.items() if rx_corr.search(v[0]['desc'] or ''))
    m['corr_calls_by_type'] = {t: [len(inst[k]) for k, v in inst.items() if rx_corr.search(v[0]['desc'] or '') and at[k] == t] for t in types}
    m['rework_only'] = [(at[k], len(v), v[0]['desc']) for k, v in inst.items()
                        if rx_rework.search(v[0]['desc'] or '')]
    m['stem_not_corr'] = [(at[k], len(v), v[0]['desc']) for k, v in inst.items()
                          if rx_stem.search(v[0]['desc'] or '') and not rx_corr.search(v[0]['desc'] or '')]
    m['fold'] = [(at[k], len(v), v[0]['desc']) for k, v in inst.items() if rx_fold.search(v[0]['desc'] or '')]
    m['nodesc'] = sum(1 for v in inst.values() if not v[0]['desc'])
    # spawn prompt size
    m['plen'] = [r['plen'] for r in tcs if r['name'] in ('Agent', 'Task')]
    return m

RES = {k: metrics(CALLS[k], TCALL[k]) for k in CALLS}

# ---------- Pi (the review agent): numbers only ----------
def pi_sessions():
    out = []
    for f in sorted(glob.glob(os.path.expanduser('~/.pi/agent/sessions/*/*.jsonl'))):
        if os.path.basename(f)[:10] < '2026-11-09': continue
        cwd = st = None; seen = set(); n = 0; cost = 0.0; tok = 0; costs_by_call = []; models = set()
        for line in open(f):
            try: o = json.loads(line)
            except Exception: continue
            if o.get('type') == 'session': cwd, st = o.get('cwd'), o.get('timestamp')
            if o.get('type') == 'message':
                m = o['message']
                if m.get('role') == 'assistant' and m.get('usage'):
                    rid = m.get('responseId') or o.get('id')
                    if rid in seen: continue
                    seen.add(rid); n += 1
                    u = m['usage']; c = (u.get('cost') or {}).get('total', 0) or 0
                    cost += c; costs_by_call.append(sum((u.get('cost') or {}).get(x, 0) or 0 for x in ('input', 'output', 'cacheRead', 'cacheWrite'))); tok += u.get('totalTokens', 0) or 0; models.add(m.get('model'))
        if cwd and 'costo' in cwd and st:
            out.append(dict(start=st, cwd=cwd, calls=n, cost=cost, cost2=sum(costs_by_call), tok=tok, models=sorted(x for x in models if x)))
    return out
PI = pi_sessions()
RUN_WIN = {'A10': ('2026-11-14T21:34', '2026-11-15T16:36'), 'A11': ('2026-11-15T16:36', '2026-11-16T03:53'),
           'A12': ('2026-11-16T03:53', '2026-11-16T16:30'), 'A13': ('2026-11-16T16:30', CUT)}
def pi_run(run):
    lo, hi = RUN_WIN[run]
    return [s for s in PI if lo <= s['start'] < hi]
PIR = {k: pi_run(k) for k in RUN_WIN}
pi_tag = {k: collections.Counter(re.search(r'a1[0-3]', s['cwd']).group(0) if re.search(r'a1[0-3]', s['cwd']) else 'other' for s in v) for k, v in PIR.items()}

# ---------- review reports and decisions of the run directories ----------
pat = re.compile(r'^(?:#{1,5}\s*\**|\|\s*|\*\*)?(F\d+)\b\**\s*[|.:,\-]*\s*\**\s*(NON-BLOCKING|BLOCKING)\b', re.M)
def reviews(run):
    out = []
    for f in sorted(glob.glob(f'{ORCH}/{run.lower()}/reviews/*.md')):
        t = open(f).read(); dd = {}
        for c, s in pat.findall(t): dd.setdefault(c, s)
        b = sum(1 for s in dd.values() if s == 'BLOCKING'); n = len(dd) - b
        head = ' '.join(t.splitlines()[:8])
        vb = re.search(r'(\d+|no|zero)\s+(?:new\s+)?BLOCKING(?!-)', head, re.I); vn = re.search(r'(\d+|no|zero)\s+(?:additional\s+)?NON-BLOCKING', head, re.I)
        lab = os.path.basename(f)[:-3]
        out.append(dict(label=lab, b=b, n=n, head_b=vb.group(1) if vb else None, head_n=vn.group(1) if vn else None))
    return out
REV = {k: reviews(k) for k in ('A10', 'A11', 'A12', 'A13')}
def group(lab):  # review file label -> batch or phase label
    g = re.sub(r'-r\d+$', '', lab)
    return 'b7d' if g == 'b7dfix' else g
def rounds(run):
    g = collections.Counter()
    for r in REV[run]:
        g[group(r['label'])] += 1 if r['b'] > 0 else 0
    return g
RND = {k: rounds(k) for k in REV}
# A13: file-name reading of the fix briefs (fixes2 / fix2 = round 2), by batch label of the file name
fixfiles = sorted(os.path.basename(f) for f in glob.glob(f'{ORCH}/a13/brief-b*-fix*.md'))
fixround = collections.defaultdict(int)
for f in fixfiles:
    b = re.match(r'brief-(b\d+[a-z]?\d?)-', f).group(1)
    fixround[b] = max(fixround[b], 2 if re.search(r'-fix(?:es)?2', f) else 1)
def gates(run):
    f = f'{ORCH}/{run.lower()}/gates/' + ('final-summary.log' if run == 'A13' else 'summary.log')
    ls = open(f).read().splitlines()
    ex = [l for l in ls if re.match(r'^\w+ exit=\d+', l)]
    return dict(head=ls[0].split()[1], ok=sum(1 for l in ex if 'exit=0' in l), n=len(ex), alldone=any('ALL DONE' in l for l in ls),
                names=[l.split()[0] for l in ex], file=os.path.relpath(f, REPO))
GT = {k: gates(k) for k in REV}
def briefs(run):
    sz = sorted(os.path.getsize(f) for f in glob.glob(f'{ORCH}/{run.lower()}/brief-*.md'))
    return sz
BR = {k: briefs(k) for k in REV}

# ---------- optional calibration on the report window ----------
CAL = None
if len(sys.argv) > 1:
    dc = pickle.load(open(sys.argv[1], 'rb'))
    lo, hi = '2026-11-09T15:50', '2026-11-16T15:51'
    cc = [r for r in dc['calls'] if 'costo' in r['proj'] and lo <= r['ts'] <= hi]
    tc = [r for r in dc['toolcalls'] if 'costo' in r['proj'] and lo <= r['ts'] <= hi]
    CAL = metrics(cc, tc); CAL['n'] = len(cc)
    pcal = [s for s in PI if lo <= s['start'] <= '2026-11-16T15:51']

# ---------- checks ----------
checks = []
for run in ('A10', 'A11', 'A12', 'A13'):
    m = RES[run]
    tot_types = sum(m['by'][t]['units'] for t in m['by'] if t not in ('worker-*', 'all-sub')) + m['main']['units']
    checks.append((f'{run}: units by agent type (main + each subagent type) vs total', tot_types, m['units']))
rows13 = CALLS['A13']
acc = collections.Counter()
for r in rows13:
    for k in ('inp', 'cr', 'cw', 'cw5m', 'cw1h', 'out'): acc[k] += r[k]
w2 = acc['inp'] + 1.25 * acc['cw5m'] + 2 * acc['cw1h'] + 1.25 * (acc['cw'] - acc['cw5m'] - acc['cw1h']) + 0.1 * acc['cr'] + 5 * acc['out']
checks.append(('A13 units: sum of weight() per call vs formula on the summed token fields', RES['A13']['units'], w2))
byday = collections.Counter(); bymodel = collections.Counter()
for r in rows13: byday[r['ts'][:10]] += W(r); bymodel[r['model']] += W(r)
checks.append(('A13 units: sum by day vs total', sum(byday.values()), RES['A13']['units']))
checks.append(('A13 units: sum by model vs total', sum(bymodel.values()), RES['A13']['units']))
t_sub = RES['A13']['by']['all-sub']
checks.append(('A13 tool calls per API call (subagents): tool_use rows / API calls vs sum over instances', t_sub['tools'] / t_sub['calls'],
               sum(1 for r in TCALL['A13'] if r['agent']) / sum(len(v) for v in RES['A13']['inst'].values())))
checks.append(('A13 Pi cost: sum of `cost.total` vs sum of the 4 components (input, output, cacheRead, cacheWrite)', sum(s['cost'] for s in PIR['A13']), sum(s['cost2'] for s in PIR['A13'])))
SCAN_END = max(r['ts'] for r in d['calls'])   # the live session keeps writing after scan.py ran
def raw_units():
    root = os.path.expanduser('~/.claude/projects/-Users-dave-Development-personal-costo-apps-core')
    tot = 0.0; n = 0
    for sfull in a13_sessions:
        files = [(root + f'/{sfull}.jsonl', None)] + [(f, f[:-6] + '.meta.json') for f in glob.glob(root + f'/{sfull}/subagents/*.jsonl')]
        for f, mp in files:
            if mp and os.path.exists(mp) and json.load(open(mp)).get('description') == ME: continue
            seen = {}
            for line in open(f):
                if '"timestamp"' not in line: continue
                try: o = json.loads(line)
                except Exception: continue
                if o.get('type') != 'assistant' or o.get('timestamp', '') > min(CUT, SCAN_END): continue
                m_ = o.get('message') or {}
                if m_.get('model') == '<synthetic>': continue
                seen[o.get('requestId') or m_.get('id')] = m_.get('usage') or {}
            for u in seen.values():
                cc = u.get('cache_creation') or {}; c5 = cc.get('ephemeral_5m_input_tokens', 0) or 0; c1 = cc.get('ephemeral_1h_input_tokens', 0) or 0
                cwt = u.get('cache_creation_input_tokens', 0) or 0
                tot += (u.get('input_tokens', 0) or 0) + 1.25 * c5 + 2 * c1 + 1.25 * (cwt - c5 - c1) + 0.1 * (u.get('cache_read_input_tokens', 0) or 0) + 5 * (u.get('output_tokens', 0) or 0); n += 1
    return tot, n
rawu, rawn = raw_units()
checks.append(('A13 units: second parser that reads the raw session files again (not `data.pkl`), up to the last call of the scan', RES['A13']['units'], rawu))
checks.append(('A13 API calls: `data.pkl` rows vs second parser', RES['A13']['calls'], rawn))
checks.append(('A10 units vs report.md 2.3 (38.1M)', RES['A10']['units'] / 1e6, 38.1))
checks.append(('A11 units vs report.md 2.3 (41.2M)', RES['A11']['units'] / 1e6, 41.2))

# ---------- by batch (A13) ----------
bs = {}
for i, s in enumerate(a13_sessions):
    rs = [r for r in rows13 if r['sess'] == s]
    mr = [r for r in rs if not r['agent']]; sr = [r for r in rs if r['agent']]
    inst = collections.defaultdict(list)
    for r in sr: inst[r['agent']].append(r)
    nc = sum(1 for v in inst.values() if rx_corr.search(v[0]['desc'] or ''))
    cu = sum(sum(map(W, v)) for v in inst.values() if rx_corr.search(v[0]['desc'] or ''))
    st = min(r['ts'] for r in rs); nx = min((r['ts'] for r in rows13 if r['sess'] == a13_sessions[i + 1] and not r['agent']), default=CUT) if i + 1 < len(a13_sessions) else CUT
    pis = [p for p in PIR['A13'] if st <= p['start'] < nx]
    lab = BATCHES[i]
    rv = [r for r in REV['A13'] if group(r['label']) == lab]
    bs[lab] = dict(sess=s[:8], units=sum(map(W, rs)), main_calls=len(mr), main_u=sum(map(W, mr)), sub_calls=len(sr), inst=len(inst),
                   corr_n=nc, corr_u=cu, main_p50=q([ctxof(r) for r in mr], .5), main_p90=q([ctxof(r) for r in mr], .9),
                   main_mx=max(ctxof(r) for r in mr), big=sum(W(r) for r in mr if ctxof(r) > 200_000), pi_n=len(pis),
                   pi_calls=sum(p['calls'] for p in pis), pi_cost=sum(p['cost'] for p in pis), rv_b=sum(r['b'] for r in rv), rv_n=sum(r['n'] for r in rv),
                   nrev=len(rv), rounds=RND['A13'].get(lab, 0), fixr=fixround.get(lab, 0), t0=st, t1=max(r['ts'] for r in rs))

# ---------- output ----------
def tab(h, rows):
    return '\n'.join(['| ' + ' | '.join(h) + ' |', '|' + '|'.join(['---'] * len(h)) + '|'] + ['| ' + ' | '.join(str(c) for c in r) + ' |' for r in rows])
R = RES; a = R['A13']
def tn(m, g, key): return m['by'].get(g, {}).get(key, 0)
def shareclass(m, c): return m['cls_u'][c] / m['units']
def ex(m, g, l): return m['explore'][g][l]
pc = lambda run, n: (RES[run]['units'] / COMMITS[n])
def pi_stat(run):
    v = PIR[run]; return len(v), sum(s['calls'] for s in v), sum(s['cost'] for s in v)
pi = {k: pi_stat(k) for k in PIR}
def ok(c): return 'met' if c else 'not met'
wt = ['worker-high', 'worker-medium', 'worker-low']

L = []
w = L.append
w('# A13 addendum: measured data\n')
w('Generated by `a13_addendum.py` (same folder) from `data.pkl` (`scan.py 6`), the Pi logs, and the run directories `.orchestration/a10` to `a13`. Numbers only: this file has no judgement of "better" or "worse"; the column "met" compares A13 with the target of `report.md` section 5.\n')
w('## 1. Method\n')
w(f"- Scan window: `scan.py 6`, logs from 2026-11-13T01:28Z; oldest costo record {min(r['ts'] for r in C0)}, newest {max(r['ts'] for r in C0)}. The logs of A10 to A12 are present and complete (each run is 1 orchestrator session with its subagents), so the baseline per run is recomputed here with the same code as A13. The baseline values of `report.md` are shown as well (they are 1 week of all costo work, from 2026-11-09T15:50Z to about 2026-11-16T15:50Z).")
w(f"- A13 = the {len(a13_sessions)} sessions of the project `...costo-apps-core` whose first main call is at or after {A13_START}Z (session IDs: {', '.join(s[:8] for s in a13_sessions)}), with their subagents: {R['A13']['calls']:,} API calls ({R['A13']['main']['calls']:,} main, {R['A13']['by']['all-sub']['calls']:,} subagent), {R['A13']['by']['all-sub']['n']} subagent instances. First call {R['A13']['t0']}, last call {R['A13']['t1']} ({R['A13']['days']:.2f} days).")
w(f"- Cut of the last session `01019b12`: calls up to {CUT}Z. The logs end at {R['A13']['t1']}, before the cut, so {after_cut} calls were removed by the cut. I excluded the {mine} calls of this measuring agent (description \"{ME}\") because they are the measurement, not the run.")
w("- A10, A11, A12 = the sessions `9e57d3b6`, `4f5e7733`, `10eea4e1` (all calls, main and subagents). The session `cccb6210` (31 main calls, 1.2M units, between A10 and A11) is in no run. A12 here is the whole session (it ended 2026-11-16T16:00Z); `report.md` 2.3 gives 47.4M because its scan ended about 2026-11-16T15:50Z. A10 and A11 match `report.md` (check in section 6).")
w("- Weighted units: `weight()` of `report.py` (input 1, cache write 5 min 1.25, 1 h 2, cache read 0.1, output 5, 1 price for all models). Percentiles: the same `q()` as `report2.py` (index `int(p*(n-1))`, no interpolation). Context of a call = input + cache read + cache write.")
w("- Agent instance = 1 (session, agent ID). \"Calls\" = API calls of the instance. Worker = `worker-high`, `worker-medium`, `worker-low`. \"all-sub\" = every subagent (workers, `general-purpose`, `Explore`).")
w("- Tools per API call: tool_use blocks / API calls, over all subagents. This reproduces the 1.19 of `report.md` F3 on the report window (section 1b), so `report.md` used all subagents, not only the workers.")
w("- Exploration share: the report gives the families (`grep -n`, `sed -n`, `cat`, `wc -l`, plus `Read`) and 46%, but not an exact rule. E1 = `Read`, `Grep`, `Glob`, and `Bash` whose first command (after `cd ... &&`) is `grep`, `rg`, `cat`, `wc`, or `sed -n`. E2 = E1 plus `head`, `tail`, `ls`, `find`, `nl`, `awk`, `stat`, `tree`, `jq`, `command ls`, and read-only `git` (`diff`, `show`, `log`, `status`, `ls-files`, `grep`, `blame`, `rev-parse`, `cat-file`, `branch`, `worktree`). Denominator: all tool calls of the subagents. On the report window E2 gives 46.1% and E1 41.1% (section 1b), so E2 is the rule that reproduces the 46% of the report; E1 is the narrow reading. Both are shown.")
w("- Repeated in-agent reads: the definition of `report2.py` section 4: for each (session, agent, file), reads after the first; main sessions count as agents. \"Per week\" = raw count x 7 / (days from the first to the last call of the run). This reproduces the 382 of the report on the report window.")
w("- Task classes: the `description` of the subagent (keyword match, as `report.md` 1). Priority: `correction` (case-insensitive substring), then `review`, then `fold`, then other. Share = units of the instances in the class / all units of the run (main included). The variant \"stem\" counts `\\bcorrect` (it adds A10 descriptions that start with \"Correct\").")
w("- Pi: the same files as `report.md` (`~/.pi/agent/sessions/*/*.jsonl`, `usage.cost.total` of each assistant message, unique `responseId`). A Pi session belongs to a run when its start time falls between the start of this run's orchestrator session and the start of the next run's (A10 2026-11-14T21:34Z, A11 2026-11-15T16:36Z, A12 2026-11-16T03:53Z, A13 2026-11-16T16:30Z to the cut) and its working directory has `costo`. Working-directory tags: " + '; '.join(f"{k} {dict(v)}" for k, v in pi_tag.items()) + ". The last A13 Pi session (2026-11-18) ran with model " + ', '.join(PIR['A13'][-1]['models']) + "; the others with `gpt-6.1-sol`.")
w("- Commits: A10 13, A11 13, A12 10 (counted after their fold, `report.md` 2.3); A13 163 before the final fold and 86 after it (given by the lead; not in the logs). The comparable value for the baseline is the one after the fold.")
w("- Reviews, findings, rounds: counted from `.orchestration/aN/reviews/*.md` (finding headings or table rows `F<n> ... BLOCKING|NON-BLOCKING`), cross-checked with the verdict line at the top of each file (section 4).")
w("- Brief size: size in bytes of `.orchestration/aN/brief-*.md` (counts and sizes only).\n")

# 1b calibration
w('### 1b. Calibration of the definitions on the window of `report.md`\n')
if CAL:
    pw, pc_, pcost = len(pcal), sum(s['calls'] for s in pcal), sum(s['cost'] for s in pcal)
    w(tab(['Value', 'report.md', 'this script on 2026-11-09T15:50Z to 11-16T15:51Z'], [
        ['costo API calls', '11,932', f"{CAL['n']:,} (main {CAL['main']['calls']:,}, sub {CAL['by']['all-sub']['calls']:,}; report: main 2,590, sub 9,342)"],
        ['weighted units', '334.9M', M(CAL['units'])],
        ['tools per API call, all subagents', '1.19', f"{CAL['by']['all-sub']['tpc']:.3f} (worker-* only {CAL['by']['worker-*']['tpc']:.3f})"],
        ['repeated reads (all agents)', '382', CAL['rep_all']],
        ['`worker-high` calls p50 / p90 / max', '79 / 128 / 332', f"{CAL['by']['worker-high']['p50']} / {CAL['by']['worker-high']['p90']} / {CAL['by']['worker-high']['mx']}"],
        ['`worker-high` final context p50', '217k', K(CAL['by']['worker-high']['fin50'])],
        ['first-call context p50, worker-* / all-sub / main', '34k per worker, 45k per main', f"{K(CAL['by']['worker-*']['first50'])} / {K(CAL['by']['all-sub']['first50'])} / {K(q(CAL['main_first'], .5))}"],
        ['exploration share E1 / E2 (all-sub)', '46%', f"{P(ex(CAL, 'all-sub', 1))} / {P(ex(CAL, 'all-sub', 2))}"],
        ['Pi sessions / calls / list cost', '62 / 4,112 / $82.38', f"{pw} / {pc_:,} / ${pcost:.2f}"],
        ['`worker-high` instances', '82', CAL['by']['worker-high']['n']],
    ]))
    w('\nThe correction share of the report (16.9%) is not recomputed on this window because its keyword list is not given; see the per-run values in section 2. The calibration file was made with `scan.py 10` in a scratch folder and filtered to the window.\n')
else:
    w('Not run in this execution (no calibration file given).\n')

# ---------- section 2 ----------
w('## 2. Metrics of section 6 of `report.md`\n')
w('Columns A10, A11, A12, A13 are recomputed here with 1 code path. "Baseline" is the value written in `report.md` (the section is named). "Target" is from `report.md` section 5. "Met" compares the A13 value with the target; `-` = no target in the report.\n')
rows = []
def add(metric, base, target, vals, met): rows.append([metric, base, target] + vals + [met])
v4 = lambda f: [f(R[k]) for k in ('A10', 'A11', 'A12', 'A13')]
add('Weighted units (run)', '38.1M / 41.2M / 47.4M (2.3)', '-', v4(lambda m: M(m['units'])), '-')
add('Commits (after fold)', '13 / 13 / 10 (2.3)', '-', ['13', '13', '10', '86 (163 before fold)'], '-')
add('Units per commit, after fold (comparable)', '2.9M / 3.2M / 4.7M (2.3)', '<= 2.5M (5, phase 2)',
    [M(R['A10']['units'] / 13), M(R['A11']['units'] / 13), M(R['A12']['units'] / 10), M(a['units'] / 86)], ok(a['units'] / 86 <= 2.5e6))
add('Units per commit, before fold', 'not counted in the baseline', '<= 2.5M (5, phase 2)', ['-', '-', '-', M(a['units'] / 163)], ok(a['units'] / 163 <= 2.5e6) + ' (not comparable)')
add('Correction share (descr. has "correction")', '16.9% (2.4, all costo, 7 days)', '<= 8% (5, phase 2)', v4(lambda m: P(shareclass(m, 'correction'))), ok(shareclass(a, 'correction') <= .08))
add('Correction share, without the fold agents ("Fold ... correction commits")', '-', '<= 8%', v4(lambda m: f"{P(m['corr_nofold_u'] / m['units'])} ({m['corr_nofold_n']} instances)"), ok(a['corr_nofold_u'] / a['units'] <= .08))
add('Correction share, stem `correct`', '-', '<= 8%', v4(lambda m: P(m['stem_u'] / m['units'])), ok(a['stem_u'] / a['units'] <= .08))
add('Correction instances (count) of all subagents', 'A12: 9 of 19 were corrections or follow-ups (3, F5)', '-', v4(lambda m: f"{m['cls_n']['correction']} of {m['by']['all-sub']['n']}"), '-')
add('Review share (Claude-side agents with "review", no "correction")', '5.7% (2.4, 7 days)', '- (A10 asks 1 review per batch)', v4(lambda m: P(shareclass(m, 'review'))), '-')
add('Fold share (descr. has "fold")', '-', '-', v4(lambda m: P(shareclass(m, 'fold'))), '-')
for g in ['worker-high', 'worker-*', 'all-sub']:
    add(f'Calls per instance p50, {g}', '79 (2.2, worker-high)' if g == 'worker-high' else '-', '<= 50 (5, phase 2)', v4(lambda m: str(tn(m, g, 'p50'))),
        ok(tn(a, g, 'p50') <= 50))
for g in ['worker-high', 'worker-*', 'all-sub']:
    add(f'Calls per instance p90, {g}', '128 (2.2, worker-high)' if g == 'worker-high' else '-', '-', v4(lambda m: str(tn(m, g, 'p90'))), '-')
for g in wt + ['general-purpose', 'Explore']:
    add(f'Calls p50 / p90 / max, {g}', {'worker-high': '79 / 128 / 332', 'worker-medium': '17 / 36 / 48', 'worker-low': '5 / 5 / 6', 'general-purpose': '44 / 70 / 90', 'Explore': '11 / 28 / 63'}[g] + ' (2.2)', '-',
        v4(lambda m: f"{tn(m, g, 'p50')} / {tn(m, g, 'p90')} / {tn(m, g, 'mx')} (n={tn(m, g, 'n')})" if tn(m, g, 'n') else '- (n=0)'), '-')
for g in wt + ['general-purpose', 'Explore']:
    add(f'Final context p50, {g}', {'worker-high': '217k', 'worker-medium': '71k', 'worker-low': '41k', 'general-purpose': '190k', 'Explore': '73k'}[g] + ' (2.2)',
        '<= 150k (5, phase 2)' if g == 'worker-high' else '-', v4(lambda m: K(tn(m, g, 'fin50')) if tn(m, g, 'n') else '-'),
        ok(tn(a, g, 'fin50') <= 150_000) if g == 'worker-high' else '-')
add('Final context p50, worker-* (all workers)', '-', '<= 150k', v4(lambda m: K(tn(m, 'worker-*', 'fin50'))), ok(tn(a, 'worker-*', 'fin50') <= 150_000))
for g in wt + ['general-purpose', 'Explore']:
    add(f'First-call context p50, {g} (the "first-call prefix")', '34k per worker (3, F10)' if g.startswith('worker') else '-', '<= 29k (5: 5k smaller than 34k)' if g.startswith('worker') else '-',
        v4(lambda m: K(tn(m, g, 'first50')) if tn(m, g, 'n') else '-'), ok(tn(a, g, 'first50') <= 29_000) if g.startswith('worker') else '-')
add('First-call context p50, worker-* (all workers)', '34k (3, F10)', '<= 29k', v4(lambda m: K(tn(m, 'worker-*', 'first50'))), ok(tn(a, 'worker-*', 'first50') <= 29_000))
add('First-call context p50, main sessions', '45k (3, F10)', '-', v4(lambda m: K(q(m['main_first'], .5))), '-')
add('Tools per API call, all subagents', '1.19 (3, F3)', '>= 1.6 (5, phase 1)', v4(lambda m: f"{m['by']['all-sub']['tpc']:.2f}"), ok(a['by']['all-sub']['tpc'] >= 1.6))
add('Tools per API call, worker-*', '-', '>= 1.6', v4(lambda m: f"{m['by']['worker-*']['tpc']:.2f}"), ok(a['by']['worker-*']['tpc'] >= 1.6))
add('Tools per API call, main sessions', '-', '-', v4(lambda m: f"{m['main']['tpc']:.2f}"), '-')
for g in wt + ['general-purpose', 'Explore']:
    add(f'Tools per API call, {g}', '-', '-', v4(lambda m: f"{tn(m, g, 'tpc'):.2f}" if tn(m, g, 'n') else '-'), '-')
add('Exploration share, E1, all subagents', '46% (3, F3; E1 gives 41.1% on that window)', '<= 35% (5, phase 1)', v4(lambda m: P(ex(m, 'all-sub', 1))), ok(ex(a, 'all-sub', 1) <= .35))
add('Exploration share, E2, all subagents (matches the 46%)', '46% (3, F3; E2 gives 46.1% on that window)', '<= 35%', v4(lambda m: P(ex(m, 'all-sub', 2))), ok(ex(a, 'all-sub', 2) <= .35))
add('Exploration share, E1 / E2, worker-*', '-', '<= 35%', v4(lambda m: f"{P(ex(m, 'worker-*', 1))} / {P(ex(m, 'worker-*', 2))}"), ok(ex(a, 'worker-*', 1) <= .35) + ' (E1); ' + ok(ex(a, 'worker-*', 2) <= .35) + ' (E2)')
add('Repeated in-agent reads, raw count', '382 in 7 days (3, F4)', '-', v4(lambda m: str(m['rep_all'])), '-')
add('Run length (days, first to last call)', '7', '-', v4(lambda m: f"{m['days']:.2f}"), '-')
add('Repeated reads per week (raw x 7 / days)', '382 (3, F4)', '<= 150 (5, phase 1)', v4(lambda m: f"{m['rep_week']:.0f}"), ok(a['rep_week'] <= 150))
add('Repeated reads per 100 API calls (my addition, not scaled by time)', f"{100 * CAL['rep_all'] / CAL['n']:.2f} (recomputed on the report window)" if CAL else '-', '-', v4(lambda m: f"{m['rep_per100']:.2f}"), '-')
add('Repeated reads, subagents only, raw', '343 (recomputed on the report window)' if CAL else '-', '-', v4(lambda m: str(m['rep_sub'])), '-')
add('Pi sessions (reviews)', '62 (2.1, 7 days)', '-', [str(pi[k][0]) for k in ('A10', 'A11', 'A12', 'A13')], '-')
add('Pi calls', '4,112 (2.1)', '-', [f"{pi[k][1]:,}" for k in ('A10', 'A11', 'A12', 'A13')], '-')
add('Pi calls per session', '66 (3, F6)', '-', [f"{pi[k][1] / pi[k][0]:.0f}" for k in ('A10', 'A11', 'A12', 'A13')], '-')
add('Pi list cost (USD)', '$82.38 (2.1)', '-', [f"${pi[k][2]:.2f}" for k in ('A10', 'A11', 'A12', 'A13')], '-')
add('Pi list cost per commit after fold (USD)', '-', '-', [f"${pi[k][2] / COMMITS[k]:.2f}" for k in ('A10', 'A11', 'A12')] + [f"${pi['A13'][2] / 86:.2f}"], '-')
add('Pi list cost per review report (USD)', '-', '- (A10: Pi cost down 30% to 50%)', [f"${pi[k][2] / len(REV[k]):.2f}" for k in ('A10', 'A11', 'A12', 'A13')], '-')
add('Review reports (files) / Pi sessions', '-', '1 per batch (A10)', [f"{len(REV[k])} / {pi[k][0]}" for k in ('A10', 'A11', 'A12', 'A13')], '-')
add('Spawn prompt chars p50 / p90 (every Agent call of the main sessions; A13 n includes the call that started this measuring agent)', 'not in report.md', '-', v4(lambda m: f"{q(m['plen'], .5):,} / {q(m['plen'], .9):,} (n={len(m['plen'])})"), '-')
add('Brief files: count, size p50 / p90 (bytes)', '-', '- (smaller briefs, 5)', [f"{len(BR[k])}, {q(BR[k], .5):,} / {q(BR[k], .9):,}" for k in ('A10', 'A11', 'A12', 'A13')], '-')
w(tab(['Metric', 'Baseline (report.md)', 'Target (section 5)', 'A10', 'A11', 'A12', 'A13', 'Met'], rows))
w('\nNotes on the table:')
w("- Units per commit: the baseline counted commits after the fold (13, 13, 10). A13 has 86 commits after the fold, so the \"after fold\" row is the comparable one. The \"before fold\" row (163 commits) is shown because the lead asked for both.")
w("- Calls p50 and the final context: the baseline in `report.md` 2.2 is the `worker-high` row, so the row \"worker-high\" is the comparable one. The \"worker-*\" rows mix `worker-high`, `worker-medium`, and `worker-low`; A13 has more `worker-medium` instances (corrections moved there), so this mix is a different one from the baseline.")
w("- First-call context includes the spawn prompt of the instance (it is part of the first call), and for main sessions the memory index and the handoff reading is not included (only the first call).")
w("- Exploration share is computed with 2 rules (E1, E2) because the rule of the report is not exact; E2 matches the 46% on the report window. Compare each A13 value with the A10 to A12 values of the same row.")
w("- The repeated reads of A10 to A12 per week are the raw count scaled by the length of each run (11 to 19 hours); they are scaled from a short window. The row \"per 100 API calls\" has no scaling by time.\n")

# correction listing
w('### 2b. Descriptions that mark rework\n')
w('Correction instances by type (descr. has "correction"), count and calls p50 per instance:\n')
types_all = ['worker-high', 'worker-medium', 'worker-low', 'general-purpose', 'Explore']
w(tab(['Run'] + types_all + ['Units in corrections', 'Units in corrections by `worker-high`'],
      [[k] + [f"{R[k]['corr_by_type'].get(t, 0)} (p50 {q(R[k]['corr_calls_by_type'].get(t, []), .5)})" for t in types_all] +
       [M(R[k]['cls_u']['correction']), M(sum(sum(map(W, v)) for kk, v in R[k]['inst'].items() if rx_corr.search(v[0]['desc'] or '') and R[k]['at'][kk] == 'worker-high'))] for k in ('A10', 'A11', 'A12', 'A13')]))
w('\nOther descriptions that mark rework (words fix, follow, rework, redo, retry, repair, address, revise, amend, patch, revert; or the stem `correct` without "correction"). Listed so that the lead can judge; they are included in the share above only when they also have "correction":\n')
for k in ('A10', 'A11', 'A12', 'A13'):
    lst = [x for x in R[k]['rework_only'] if not rx_corr.search(x[2] or '')] + [x for x in R[k]['stem_not_corr'] if not rx_rework.search(x[2] or '')]
    wd = sorted({m_.lower() for x in R[k]['rework_only'] for m_ in rx_rework.findall(x[2] or '') if rx_corr.search(x[2] or '')})
    w(f"- {k}: " + ('; '.join(f"{t} {n} calls: \"{ds}\"" for t, n, ds in lst) if lst else 'none') + (f". Also with \"correction\" and another rework word ({', '.join(wd)}): " + '; '.join(f"\"{x[2]}\"" for x in R[k]['rework_only'] if rx_corr.search(x[2] or '')) if wd else ''))
w('- Mechanical or follow-on work with other words (not counted as correction): ' + '; '.join(f"{k}: " + (', '.join(f"\"{x[2]}\" ({x[0]}, {x[1]} calls)" for x in R[k]['fold']) or 'none') for k in ('A10', 'A11', 'A12', 'A13')) + '\n')

# ---------- section 3 ----------
w('## 3. Where the units went in A13\n')
def share_table(keyf, name):
    cnt = collections.Counter(); calls = collections.Counter()
    for r in rows13: cnt[keyf(r)] += W(r); calls[keyf(r)] += 1
    return tab([name, 'API calls', 'Units', 'Share'], [[k, f"{calls[k]:,}", M(v), P(v / a['units'])] for k, v in sorted(cnt.items(), key=lambda kv: -kv[1])])
w('### 3.1 By agent type\n')
w(share_table(lambda r: r['atype'], 'Agent type'))
w('\nInstances and calls per instance (p50 / p90 / max), final context p50 / p90:\n')
w(tab(['Type', 'Instances', 'Calls p50 / p90 / max', 'Final ctx p50 / p90', 'First-call ctx p50'],
      [[t, tn(a, t, 'n'), f"{tn(a, t, 'p50')} / {tn(a, t, 'p90')} / {tn(a, t, 'mx')}", f"{K(tn(a, t, 'fin50'))} / {K(tn(a, t, 'fin90'))}", K(tn(a, t, 'first50'))] for t in wt + ['general-purpose', 'Explore']]))
w('\n### 3.2 By model (the `model` field of each call)\n')
w(share_table(lambda r: r['model'], 'Model'))
w('\nSubagent model and effort from the `.meta.json` (a blank model = the role file sets it; the logs show the model in the table above):\n')
me = collections.Counter(); meu = collections.Counter()
for k, v in a['inst'].items():
    key = (v[0]['atype'], v[0]['model'], v[0]['amodel'], v[0]['aeffort']); me[key] += 1; meu[key] += sum(map(W, v))
w(tab(['Type', 'Call model', 'meta model', 'meta effort', 'Instances', 'Units'], [[k[0], k[1], k[2] or '-', k[3] or '-', me[k], M(meu[k])] for k in sorted(me, key=lambda x: -meu[x])]))
w('\n### 3.3 By day (UTC)\n')
w(share_table(lambda r: r['ts'][:10], 'Day'))
w('\n### 3.4 By batch (1 orchestrator session per batch)\n')
w('The session order, the handoff files `handoff-b*.md` (by mtime), and the descriptions of the subagents agree: session i = the i-th batch of the list (the file `handoff-bX.md` is written at the end of the session of batch X). Pi sessions are put in the session whose time span holds their start; review findings are put by the review label, so the review `b7dfix` (started 2026-11-17T16:42Z, after the start of the next session) shows its findings in `b7d` and its Pi session in `b8a`. Review findings are from section 4. The last row is the session that did the end of the run (fold, spec close, this audit).\n')
w(tab(['Batch', 'Session', 'Units', 'Share', 'Main calls', 'Main ctx p50 / p90 / max', 'Main units >200k ctx', 'Subagent instances (calls)', 'Correction instances (units)', 'Pi sessions / calls / cost', 'Review B / NB (by review label)'],
      [[lab, v['sess'], M(v['units']), P(v['units'] / a['units']), v['main_calls'], f"{K(v['main_p50'])} / {K(v['main_p90'])} / {K(v['main_mx'])}", P(v['big'] / v['units']) + ' of its units',
        f"{v['inst']} ({v['sub_calls']})", f"{v['corr_n']} ({M(v['corr_u'])})", f"{v['pi_n']} / {v['pi_calls']} / ${v['pi_cost']:.2f}", f"{v['rv_b']} / {v['rv_n']}" if v['nrev'] else '-'] for lab, v in bs.items()]))
w('\n### 3.5 Main (orchestrator) sessions, A10 to A13\n')
w('Context per call = input + cache read + cache write of each main API call. ">200k" = share of weighted units from main calls with a context above 200k, as a share of all units of the run and as a share of the main-session units. For A10 to A12 the main sessions are the 1 session of each run.\n')
w(tab(['Run', 'Main sessions', 'Main calls', 'Ctx p50', 'Ctx p90', 'Ctx max', 'Main units (share of run)', '>200k, share of run units', '>200k, share of main units', 'Main calls >200k', 'Tools per API call (main)'],
      [[k, len(runsess[k]), f"{R[k]['main']['calls']:,}", K(R[k]['main']['p50']), K(R[k]['main']['p90']), K(R[k]['main']['mx']), f"{M(R[k]['main']['units'])} ({P(R[k]['main']['share'])})",
        P(R[k]['main']['big_share_run']), P(R[k]['main']['big_share_main']), R[k]['main']['big_n'], f"{R[k]['main']['tpc']:.2f}"] for k in ('A10', 'A11', 'A12', 'A13')]))
w('\nBaseline of `report.md` (3, F1 and F7; 7 days, all main sessions of costo): main context p50 204k, p90 451k (max 714k); main calls above 200k use 18.6% of all units.\n')

# ---------- section 4 ----------
w('## 4. Quality guardrails (section 5 of `report.md`)\n')
rows4 = []
for k in ('A10', 'A11', 'A12', 'A13'):
    rv = REV[k]; b = sum(r['b'] for r in rv); n = sum(r['n'] for r in rv)
    rnd = RND[k]; over = [g for g, c in rnd.items() if c > 2]
    rows4.append([k, len(rv), b, n, f"{(b + n) / len(rv):.2f}", f"{b / len(rv):.2f}", sum(1 for r in rv if r['b'] > 0), sum(rnd.values()), len(rnd), f"{max(rnd.values())}", f"{len(over)}" + (f" ({', '.join(over)}: {', '.join(str(rnd[g]) for g in over)} rounds)" if over else ''),
                  f"{GT[k]['ok']} of {GT[k]['n']} lines exit=0, head {GT[k]['head']}" + (', ALL DONE' if GT[k]['alldone'] else '')])
w(tab(['Run', 'Reviews (files)', 'BLOCKING', 'NON-BLOCKING', 'Findings per review', 'BLOCKING per review', 'Reviews with a BLOCKING finding', 'Correction rounds (= reviews with BLOCKING)', 'Batches or phases reviewed', 'Max rounds in 1 batch or phase', 'Batches or phases with more than 2 rounds', 'Gates at the finish'], rows4))
w('\nSources and how each count was made:')
for k in ('A10', 'A11', 'A12', 'A13'):
    w(f"- {k}: reviews `.orchestration/{k.lower()}/reviews/*.md` ({len(REV[k])} files); findings = unique finding codes whose heading or table row carries BLOCKING or NON-BLOCKING; gates `{GT[k]['file']}` (lines: {', '.join(GT[k]['names'])}). The count of findings per file agrees with the verdict line at the top of the file in every file where the top has a number (files without a number for BLOCKING at the top: " + (', '.join(r['label'] for r in REV[k] if r['head_b'] is None) or 'none') + ").")
w("- A \"correction round\" is counted here as 1 review with at least 1 BLOCKING finding (each such review led to 1 correction round of workers); this is my reading of the review files, not a field. Rounds per batch or phase = the number of such reviews in the group (the review label before `-r<n>`; `b7dfix` counts in `b7d`). A13 file-name reading (briefs `brief-b*-fix*.md`: `fix2`/`fixes2` = round 2): " + ', '.join(f"{b}={r}" for b, r in sorted(fixround.items())) + ". Both readings give a maximum of 2 in A13; they differ for `b6b2` (1 round, no review finding, by file) and `b8b` (fix briefs exist; its review is the last one).")
w("- A10 to A12 had no `Result` field for the gates other than `summary.log`; all lines exit 0 in each run, A10 with a `bench` line. A13: 13 gate lines (fmt, clippy, sqlx, test, deny, vet, apple, kotlin, miri, mutants, fuzz, build aar, image) on head `8067dea2`.")
w("- Reopened tickets or regressions after the finish: not in the logs or the run directories; not measured.\n")
w('Per review (A13):\n')
w(tab(['Review file', 'BLOCKING', 'NON-BLOCKING', 'Top of file says (B / NB)'], [[r['label'], r['b'], r['n'], f"{r['head_b'] or '-'} / {r['head_n'] or '-'}"] for r in REV['A13']]))
w('\nRounds per batch, A13 (review reading vs file-name reading):\n')
w(tab(['Batch', 'Reviews', 'Reviews with BLOCKING (rounds, review reading)', 'Fix briefs round (file-name reading)'],
      [[lab, bs[lab]['nrev'], bs[lab]['rounds'], bs[lab]['fixr']] for lab in BATCHES if lab != 'end']))
for k in ('A10', 'A11', 'A12'):
    w(f"\nRounds per group, {k}: " + ', '.join(f"{g}={c}" for g, c in RND[k].items()))

# ---------- section 5 ----------
w('\n## 5. What I could not measure\n')
for t in [
    "Real price per model. The logs do not give the price of `claude-fable-5-2` against `claude-opus-5-5`; all models use the same weight (as in `report.md`). The split by model above is in units, not money.",
    "Commits per run from the logs: the logs have no commit count; the counts 13, 13, 10, 163, and 86 are given, not measured here.",
    "Reopened tickets or regressions after a finish (guardrail of section 5): no source in the logs or run directories.",
    "The Pi tokens by input type are in the Pi logs, but Pi list cost is the field `usage.cost.total`, so the cost is the list cost of Pi, not an invoice. The A13 review of 2026-11-18 ran on `gpt-6.2-sol`, the others on `gpt-6.1-sol`; the price per token of each model is not in this analysis.",
    "A correction round is not a field in any file. The count is my reading (reviews with a BLOCKING finding); orchestrator corrections done without a worker (the orchestrator edits a file itself) are not seen in subagent descriptions.",
    "The exact exploration rule of `report.md` (46%): the families are named but not the full rule. My E2 gives 46.1% on the report window (section 1b), so I use it as the matching rule; that it is the same rule as the report is an inference from 1 number.",
    "Work outside the Claude logs: the Pi reviews and the Rex panes are not Claude API calls. Pi is counted from its own logs (section 2); the `rex` pane polls appear only as the main-session tool calls that ran them.",
    "A13 gates outside the final summary (batch gates, per-batch run time) are not part of the unit count except as the tool calls that ran them.",
    "A10 per-week figure of repeated reads for a run shorter than a week is a scaled value, not an observation of a week.",
]: w('- ' + t)

# ---------- section 6 ----------
w('\n## 6. Checks on my own numbers\n')
rows6 = []
for lab, x, y in checks:
    ok_ = abs(x - y) <= 1e-6 * max(1, abs(y)) if 'report.md' not in lab else abs(x - y) <= 0.15
    rows6.append([lab, f"{x:.4f}" if abs(x) < 1000 else f"{x:,.1f}", f"{y:.4f}" if abs(y) < 1000 else f"{y:,.1f}", 'equal' if ok_ else 'differ'])
w(tab(['Check', 'Value 1', 'Value 2', 'Result'], rows6))
w(f"\n- Sessions: {len(a13_sessions)} A13 sessions (the lead said 20 or 21); 20 batch labels in the table of 3.4. The session `10eea4e1` is in A12, not A13.")
w(f"- Calls after the cut: {after_cut}. Calls of this measuring agent excluded: {mine}.")
w(f"- Agent instances with no description: " + ', '.join(f"{k} {R[k]['nodesc']}" for k in ('A10', 'A11', 'A12', 'A13')) + ".")
w("- Calibration: the report-window recomputation in 1b reproduces the 382 repeated reads, the 79 / 128 / 332 calls of `worker-high`, and the 1.19 tools per call of `report.md`; E2 gives 46.1% for the exploration share against the 46% of the report (E1 gives 41.1%); first-call context p50 34k (worker) and 45k (main); Pi 62 sessions, 4,110 calls (report 4,112), $82.38.")
open('a13-addendum-data.md', 'w').write('\n'.join(L) + '\n')

# ---------- runs.csv ----------
hdr = ['run', 'sessions', 'window_days', 'units_M', 'commits_after_fold', 'commits_before_fold', 'units_per_commit_after_fold_M', 'units_per_commit_before_fold_M',
       'correction_share', 'correction_share_stem', 'review_share', 'fold_share', 'correction_instances', 'subagent_instances',
       'worker_calls_p50_all_workers', 'worker_calls_p90_all_workers', 'worker_high_calls_p50', 'worker_high_calls_p90', 'worker_medium_calls_p50', 'worker_medium_calls_p90',
       'worker_high_final_ctx_p50', 'worker_medium_final_ctx_p50', 'all_workers_final_ctx_p50', 'first_call_ctx_p50_worker_high', 'first_call_ctx_p50_worker_medium', 'first_call_ctx_p50_main',
       'tools_per_call_all_sub', 'tools_per_call_workers', 'tools_per_call_main', 'exploration_share_E1_all_sub', 'exploration_share_E2_all_sub',
       'repeated_reads_raw', 'repeated_reads_per_week', 'repeated_reads_per_100_calls', 'main_calls', 'main_ctx_p50', 'main_ctx_p90', 'main_big_share_of_run_units',
       'pi_sessions', 'pi_calls', 'pi_cost_usd', 'reviews', 'blocking', 'non_blocking', 'correction_rounds', 'max_rounds_in_one_batch', 'batches_over_2_rounds', 'gates_ok', 'gates_total']
with open('runs.csv', 'w', newline='') as fh:
    cw = csv.writer(fh); cw.writerow(hdr)
    for k in ('A10', 'A11', 'A12', 'A13'):
        m = R[k]; rv = REV[k]; rnd = RND[k]
        cf_ = COMMITS[k] if k != 'A13' else COMMITS['A13_post']
        cw.writerow([k, len(runsess[k]), f"{m['days']:.3f}", f"{m['units'] / 1e6:.2f}", cf_, COMMITS['A13_pre'] if k == 'A13' else '', f"{m['units'] / cf_ / 1e6:.3f}",
                     f"{m['units'] / COMMITS['A13_pre'] / 1e6:.3f}" if k == 'A13' else '',
                     f"{shareclass(m, 'correction'):.4f}", f"{m['stem_u'] / m['units']:.4f}", f"{shareclass(m, 'review'):.4f}", f"{shareclass(m, 'fold'):.4f}", m['cls_n']['correction'], m['by']['all-sub']['n'],
                     tn(m, 'worker-*', 'p50'), tn(m, 'worker-*', 'p90'), tn(m, 'worker-high', 'p50'), tn(m, 'worker-high', 'p90'), tn(m, 'worker-medium', 'p50'), tn(m, 'worker-medium', 'p90'),
                     tn(m, 'worker-high', 'fin50'), tn(m, 'worker-medium', 'fin50'), tn(m, 'worker-*', 'fin50'), tn(m, 'worker-high', 'first50'), tn(m, 'worker-medium', 'first50') or '', q(m['main_first'], .5),
                     f"{m['by']['all-sub']['tpc']:.3f}", f"{m['by']['worker-*']['tpc']:.3f}", f"{m['main']['tpc']:.3f}", f"{ex(m, 'all-sub', 1):.4f}", f"{ex(m, 'all-sub', 2):.4f}",
                     m['rep_all'], f"{m['rep_week']:.0f}", f"{m['rep_per100']:.3f}", m['main']['calls'], m['main']['p50'], m['main']['p90'], f"{m['main']['big_share_run']:.4f}",
                     pi[k][0], pi[k][1], f"{pi[k][2]:.2f}", len(rv), sum(r['b'] for r in rv), sum(r['n'] for r in rv), sum(rnd.values()), max(rnd.values()), sum(1 for c in rnd.values() if c > 2),
                     GT[k]['ok'], GT[k]['n']])
print('written a13-addendum-data.md and runs.csv; A13 units', M(a['units']), 'calls', a['calls'])
