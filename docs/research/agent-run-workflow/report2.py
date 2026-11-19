#!/usr/bin/env python3
import pickle, collections, json, os, glob, re
d = pickle.load(open('./data.pkl', 'rb'))
C = [r for r in d['calls'] if 'costo' in r['proj']]
TR = [r for r in d['toolres'] if 'costo' in r['proj']]
TC = [r for r in d['toolcalls'] if 'costo' in r['proj']]
q = lambda v, p: sorted(v)[int(p*(len(v)-1))] if v else 0
W = lambda r: r['inp'] + r['cw5m']*1.25 + r['cw1h']*2 + (r['cw']-r['cw5m']-r['cw1h'])*1.25 + r['cr']*0.1 + r['out']*5
T = sum(map(W, C))

# 1. per agent instance: first-call context (fixed overhead), calls, final context
inst = collections.defaultdict(list)
for r in C: inst[(r['sess'], r['agent'])].append(r)
first = collections.defaultdict(list); ncalls = collections.defaultdict(list); last = collections.defaultdict(list); fixedcost = collections.Counter()
for (s, a), rows in inst.items():
    rows.sort(key=lambda r: r['ts']); k = rows[0]['atype']
    f = rows[0]['inp'] + rows[0]['cr'] + rows[0]['cw']
    first[k].append(f); ncalls[k].append(len(rows)); last[k].append(rows[-1]['inp'] + rows[-1]['cr'] + rows[-1]['cw'])
    fixedcost[k] += f * len(rows) * 0.1  # re-reading the first-call prefix on every call, cache-read price
print('## per agent instance: count, first-call ctx p50, calls p50/p90/max, final ctx p50/p90')
for k in first:
    print(f"{k:16} n={len(first[k]):4} first p50={q(first[k],.5):>7,} calls p50={q(ncalls[k],.5)} p90={q(ncalls[k],.9)} max={max(ncalls[k])} final p50={q(last[k],.5):>7,} p90={q(last[k],.9):>7,} fixed-prefix share={fixedcost[k]/T:.1%}")

# 2. tool result volume by tool (chars ~ 4 per token, ESTIMATE)
print('\n## tool results by tool (chars; tokens ~= chars/4)')
tv = collections.Counter(); tn = collections.Counter(); tmax = collections.Counter()
for r in TR:
    key = r['name'] if not r['name'].startswith('mcp__') else 'mcp:' + r['name'].split('__')[1]
    tv[key] += r['chars']; tn[key] += 1; tmax[key] = max(tmax[key], r['chars'])
tot = sum(tv.values())
for k, v in tv.most_common(14): print(f"{k:28} n={tn[k]:5} chars={v/1e6:6.2f}M ({100*v/tot:4.1f}%) avg={v//tn[k]:6,} max={tmax[k]:,}")
big = [r for r in TR if r['chars'] > 20000]
print(f"results >20k chars: {len(big)}  chars {sum(r['chars'] for r in big)/1e6:.2f}M of {tot/1e6:.2f}M")

# 3. tool calls by name, main vs sub
print('\n## tool calls by name (main / sub)')
cm = collections.Counter((r['name'], 'sub' if r['agent'] else 'main') for r in TC)
names = collections.Counter(r['name'] for r in TC)
for n, c in names.most_common(16): print(f"{n:34} main={cm[(n,'main')]:5} sub={cm[(n,'sub')]:5}")

# 4. repeated reads of the same file inside one agent instance
rd = collections.Counter((r['sess'], r['agent'], r['file']) for r in TC if r['name'] == 'Read' and r['file'])
rep = {k: v for k, v in rd.items() if v > 1}
print(f"\n## Read: {sum(rd.values())} reads, {len(rd)} unique (agent,file); repeated extra reads = {sum(v-1 for v in rep.values())}")
fr = collections.Counter()
for (s, a, f), v in rd.items(): fr[re.sub(r'.*/costo[^/]*/', '', f)] += v
print('most-read files:', [(f, n) for f, n in fr.most_common(12)])
# same file read across distinct agents in one session
across = collections.defaultdict(set)
for (s, a, f) in rd: across[(s, f)].add(a)
multi = sorted(((len(v), f) for (s, f), v in across.items() if len(v) >= 4), reverse=True)[:10]
print('files read by >=4 agents in one session:', [(n, re.sub(r'.*/costo[^/]*/', '', f)) for n, f in multi])

# 5. bash command families
print('\n## Bash command families')
fam = collections.Counter()
for r in TC:
    if r['name'] != 'Bash': continue
    c = r['cmd'].strip()
    m = re.match(r'(?:cd [^&;]+(?:&&|;)\s*)?([\w./-]+)(?:\s+([\w:-]+))?', c)
    fam[(m.group(1) + ' ' + (m.group(2) or '')).strip() if m else c[:20]] += 1
print(fam.most_common(25))
# Bash result sizes by family
bs = collections.Counter()

# 6. skills and agent spawns
print('\n## Skill calls:', collections.Counter(r['skill'] for r in TC if r['name'] == 'Skill').most_common(15))
sp = [r for r in TC if r['name'] in ('Agent', 'Task')]
print('## Agent spawns by type:', collections.Counter((r['sub'], r['model']) for r in sp).most_common(12))
print('spawn prompt chars p50/p90/max:', q([r['plen'] for r in sp], .5), q([r['plen'] for r in sp], .9), max([r['plen'] for r in sp] or [0]))
print('compactions:', sum(v['compactions'] for (p, s), v in d['sessions'].items() if 'costo' in p))
