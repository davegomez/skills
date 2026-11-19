#!/usr/bin/env python3
import pickle, collections, sys
d = pickle.load(open('./data.pkl', 'rb'))
C = d['calls']
# Weighted "input-equivalent" units (ESTIMATE): Anthropic list-price ratios.
W = dict(inp=1.0, cw5m=1.25, cw1h=2.0, cr=0.1, out=5.0)
def weight(r): return r['inp']*W['inp'] + r['cw5m']*W['cw5m'] + r['cw1h']*W['cw1h'] + (r['cw']-r['cw5m']-r['cw1h'])*1.25 + r['cr']*W['cr'] + r['out']*W['out']
def M(n): return f"{n/1e6:8.1f}M"
def agg(rows, key):
    a = collections.defaultdict(collections.Counter)
    for r in rows:
        k = key(r); x = a[k]
        x['n'] += 1; x['inp'] += r['inp']; x['cr'] += r['cr']; x['cw'] += r['cw']; x['out'] += r['out']; x['think'] += r['think']; x['w'] += weight(r)
        x['ctx'] += r['inp'] + r['cr'] + r['cw']
    return a
def table(title, a, top=15, tot=None):
    tot = tot or sum(x['w'] for x in a.values())
    print(f"\n## {title}\n{'key':48} {'calls':>6} {'input':>9} {'cacheRd':>9} {'cacheWr':>9} {'output':>9} {'weighted':>9} {'w%':>5}")
    for k, x in sorted(a.items(), key=lambda kv: -kv[1]['w'])[:top]:
        print(f"{str(k)[:48]:48} {x['n']:6} {M(x['inp'])} {M(x['cr'])} {M(x['cw'])} {M(x['out'])} {M(x['w'])} {100*x['w']/tot:5.1f}")

costo = lambda r: 'costo' in r['proj']
table('By project (all)', agg(C, lambda r: r['proj'].replace('-Users-dave-', '')), 12)
CC = [r for r in C if costo(r)]
T = sum(weight(r) for r in CC)
table('costo: by model', agg(CC, lambda r: r['model']), tot=T)
table('costo: main vs subagent type', agg(CC, lambda r: r['atype']), tot=T)
table('costo: subagent model/effort', agg([r for r in CC if r['agent']], lambda r: (r['atype'], r['model'], r['aeffort'])), tot=T)
table('costo: main-session effort', agg([r for r in CC if not r['agent']], lambda r: (r['model'], r['effort'])), tot=T)
table('costo: by day', agg(CC, lambda r: r['ts'][:10]), 10, tot=T)
s = agg(CC, lambda r: (r['sess'][:8], 'sub' if r['agent'] else 'main'))
table('costo: top session parts', s, 25, tot=T)
ss = agg(CC, lambda r: r['sess'])
ws = sorted((x['w'] for x in ss.values()), reverse=True)
print(f"\nsessions={len(ws)} top5 share={sum(ws[:5])/T:.1%} top10={sum(ws[:10])/T:.1%} top20={sum(ws[:20])/T:.1%}")
tot = collections.Counter()
for r in CC:
    for k in ('inp', 'cr', 'cw', 'cw1h', 'cw5m', 'out', 'think'): tot[k] += r[k]
tot['w'] = T
print('\ncosto totals:', {k: f"{v/1e6:.1f}M" for k, v in tot.items()}, 'calls', len(CC))
print('weighted share: input %.1f%% cacheRead %.1f%% cacheWrite %.1f%% output %.1f%%' % (
    100*tot['inp']/T, 10*tot['cr']/T, 100*(1.25*tot['cw5m']+2*tot['cw1h']+1.25*(tot['cw']-tot['cw1h']-tot['cw5m']))/T, 500*tot['out']/T))
# context size per call
import statistics
ctx = sorted(r['inp']+r['cr']+r['cw'] for r in CC if not r['agent'])
ctxs = sorted(r['inp']+r['cr']+r['cw'] for r in CC if r['agent'])
q = lambda v, p: v[int(p*(len(v)-1))] if v else 0
print(f"main ctx/call p50={q(ctx,.5):,} p90={q(ctx,.9):,} max={ctx[-1] if ctx else 0:,} | sub ctx/call p50={q(ctxs,.5):,} p90={q(ctxs,.9):,}")
big = [r for r in CC if not r['agent'] and r['inp']+r['cr']+r['cw'] > 200_000]
print(f"main calls with ctx>200k: {len(big)} weighted {sum(map(weight,big))/T:.1%}")
cwrows = [r for r in CC if r['cw'] > 100_000]
print(f"calls with cache write >100k (cache rebuilds): {len(cwrows)}, cw tokens {sum(r['cw'] for r in cwrows)/1e6:.1f}M, weighted {sum(map(weight,cwrows))/T:.1%}")
pickle.dump(dict(W=W), open('./w.pkl', 'wb'))
