#!/usr/bin/env python3
"""Aggregate Claude Code token usage from ~/.claude/projects JSONL logs (last N days)."""
import json, os, sys, glob, collections, pickle
from datetime import datetime, timedelta, timezone

ROOT = os.path.expanduser('~/.claude/projects')
SINCE = (datetime.now(timezone.utc) - timedelta(days=int(sys.argv[1]) if len(sys.argv) > 1 else 7)).isoformat()

def z(): return collections.Counter()
calls = []          # one row per API response
toolres = []        # one row per tool result
toolcalls = []      # one row per tool_use
sessions = {}

def usage_row(o, proj, sess, agent, meta):
    m = o['message']; u = m.get('usage') or {}
    cc = u.get('cache_creation') or {}
    return dict(proj=proj, sess=sess, agent=agent, atype=meta.get('agentType', 'main') if agent else 'main',
                amodel=meta.get('model'), aeffort=meta.get('effort'), desc=meta.get('description'),
                model=m.get('model'), ts=o.get('timestamp', ''), effort=o.get('effort'),
                inp=u.get('input_tokens', 0) or 0, out=u.get('output_tokens', 0) or 0,
                think=(u.get('output_tokens_details') or {}).get('thinking_tokens', 0) or 0,
                cr=u.get('cache_read_input_tokens', 0) or 0, cw=u.get('cache_creation_input_tokens', 0) or 0,
                cw1h=cc.get('ephemeral_1h_input_tokens', 0) or 0, cw5m=cc.get('ephemeral_5m_input_tokens', 0) or 0)

def scan(path, proj, sess, agent, meta):
    seen = {}; idmap = {}
    try: fh = open(path)
    except OSError: return
    for line in fh:
        if '"timestamp"' not in line: continue
        try: o = json.loads(line)
        except Exception: continue
        ts = o.get('timestamp', '')
        if ts and ts < SINCE: continue
        t = o.get('type')
        if t == 'assistant':
            m = o.get('message') or {}
            key = o.get('requestId') or m.get('id')
            if m.get('model') == '<synthetic>': continue
            seen[key] = usage_row(o, proj, sess, agent, meta)  # last record per request holds final usage
            for c in m.get('content') or []:
                if isinstance(c, dict) and c.get('type') == 'tool_use':
                    inp = c.get('input') or {}
                    idmap[c.get('id')] = c.get('name')
                    toolcalls.append(dict(proj=proj, sess=sess, agent=agent, name=c.get('name'), ts=ts,
                        file=inp.get('file_path'), cmd=(inp.get('command') or '')[:200],
                        skill=inp.get('skill'), sub=inp.get('subagent_type'), model=inp.get('model'),
                        plen=len(inp.get('prompt') or '')))
        elif t == 'user':
            m = o.get('message') or {}
            cont = m.get('content')
            if isinstance(cont, list):
                for c in cont:
                    if isinstance(c, dict) and c.get('type') == 'tool_result':
                        r = c.get('content'); n = len(json.dumps(r)) if not isinstance(r, str) else len(r)
                        toolres.append(dict(proj=proj, sess=sess, agent=agent, name=idmap.get(c.get('tool_use_id'), '?'), chars=n))
        elif t == 'system' and o.get('subtype') == 'compact_boundary':
            sessions.setdefault((proj, sess), z())['compactions'] += 1
    calls.extend(seen.values())

for pdir in glob.glob(os.path.join(ROOT, '*')):
    proj = os.path.basename(pdir)
    for f in glob.glob(os.path.join(pdir, '*.jsonl')):
        sess = os.path.basename(f)[:-6]
        if os.path.getmtime(f) < datetime.fromisoformat(SINCE).timestamp(): pass  # mtime check below
        scan(f, proj, sess, None, {})
    for f in glob.glob(os.path.join(pdir, '*', 'subagents', '*.jsonl')):
        sess = f.split(os.sep)[-3]; agent = os.path.basename(f)[:-6]
        meta = {}
        mp = f[:-6] + '.meta.json'
        if os.path.exists(mp):
            try: meta = json.load(open(mp))
            except Exception: pass
        scan(f, proj, sess, agent, meta)

pickle.dump(dict(calls=calls, toolres=toolres, toolcalls=toolcalls, sessions=sessions, since=SINCE),
            open('./data.pkl', 'wb'))
print('calls', len(calls), 'toolcalls', len(toolcalls), 'toolres', len(toolres), 'since', SINCE)
