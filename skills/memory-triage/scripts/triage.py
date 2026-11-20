#!/usr/bin/env python3
"""Sort each Claude Code auto memory note into 1 class: alert, drop, check, fix, or keep.

Usage: triage.py [--memory-dir DIR] [--repo DIR] [--today YYYY-MM-DD] [--origin NOTE]

Read-only and offline: it opens files only to read them and checks a path that a note names
for existence only. Standard library only, Python 3.9 or later. The transcript format is
undocumented: what the script cannot read there, it reports as 'unknown'.
"""
from __future__ import annotations

import argparse
import datetime
import difflib
import glob
import json
import os
import re
import subprocess
import sys
from collections import deque

INDEX = 'MEMORY.md'
INDEX_MAX_LINES = 200
INDEX_MAX_BYTES = 25000  # the docs say "25KB": take the smaller reading
INDEX_MAX_ENTRY_CHARS = 150
STALE_DAYS = 30
NEAR_DUPLICATE_RATIO = 0.8  # difflib ratio on the words of 2 bodies
NOTE_TYPES = ('user', 'feedback', 'project', 'reference')
WRITE_TOOLS = ('Write', 'Edit')
BLOB_PREFIX_BYTES = 400
ORIGIN_MAX_CHARS = 4000
ORIGIN_MESSAGES = 3
ORIGIN_MESSAGE_CHARS = 600
ORIGIN_MAX_WRITES = 10
CLASSES = ('alert', 'drop', 'check', 'fix', 'keep')  # highest first
REMOVED = '[credential-like value removed]'

DATED_NAME = re.compile(r'\d{4}([-_])\d{2}\1\d{2}')
RELATIVE_DATE = re.compile(
    r'(?i)\b(?:yesterday|today|tomorrow|(?:last|next|this) (?:week|month|year)|\d+ (?:days?|weeks?|months?) ago)\b')
BACKTICKED = re.compile(r'`([^`\s]+)`')
PATH_END = re.compile(r'(?:\.[A-Za-z][A-Za-z0-9]{0,7}|/)$')
LINE_SUFFIX = re.compile(r':\d+(?::\d+)?$')
LINK = re.compile(r'\]\(([^)\s]+)\)')
SESSION_ID = re.compile(r'^[A-Za-z0-9_-]+$')
CRED_FORMATS = (
    ('aws-access-key', r'AKIA[0-9A-Z]{16}'),
    ('github-token', r'gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,}'),
    ('sk-api-key', r'sk-[A-Za-z0-9_-]{20,}'),
    ('stripe-key', r'[rs]k_live_[A-Za-z0-9]{16,}'),
    ('google-api-key', r'AIza[0-9A-Za-z_-]{35}'),
    ('slack-token', r'xox[baprs]-[A-Za-z0-9-]{10,}'),
    ('jwt', r'eyJ[A-Za-z0-9_-]{15,}\.eyJ[A-Za-z0-9_-]{10,}'),
    ('private-key', r'-----BEGIN [A-Z ]*PRIVATE KEY-----'),
)
CRED_FORMAT = re.compile('|'.join('(?P<%s>%s)' % (k.replace('-', '_'), p) for k, p in CRED_FORMATS))
CRED_KEYWORD = re.compile(
    r'(?i)(?:pass(?:word|wd|phrase)?|secret|token|api[_-]?key|private[_ -]?key|keystore|credential)s?\b'
    r'[^\n]{0,40}?[:=]\s*[`"\']?([^\s`"\']{8,})')
HARNESS_TEXT = ('<command-', '<local-command-')  # slash-command wrappers, not typed text
PLACEHOLDER = re.compile(r'(?i)^(?:<|\$|\{|\[|~|/|your|xxx|\*+|redacted|example|keychain|1password|env)')


# Detection: pure functions from text to flags. A flag is (class, detail).

def is_placeholder(value):
    return bool(PLACEHOLDER.match(value))


def redact(text):
    """Return text with each credential-like value replaced."""
    text = CRED_FORMAT.sub(REMOVED, text)
    return CRED_KEYWORD.sub(
        lambda m: m.group(0) if is_placeholder(m.group(1)) else m.group(0)[:m.start(1) - m.start(0)] + REMOVED, text)


def numbered_lines(text):
    """Return the lines of text as perl -ne counts them with $.: split on the newline character only."""
    lines = text.split('\n')
    return lines[:-1] if lines[-1] == '' else lines


def credential_flags(text):
    """Flag each line that holds a credential-like value, by line number and kind only."""
    flags = []
    for n, line in enumerate(numbered_lines(text), 1):
        kinds = [m.lastgroup.replace('_', '-') for m in CRED_FORMAT.finditer(line)]
        kinds += ['keyword=value' for m in CRED_KEYWORD.finditer(line) if not is_placeholder(m.group(1))]
        flags += [('alert', 'credential-like value: line %d (%s)' % (n, k)) for k in dict.fromkeys(kinds)]
    return flags


def name_flags(name):
    """Flag a file name that marks a single event: a date."""
    stem = name[:-3] if name.endswith('.md') else name
    return [('check', 'dated file name')] if DATED_NAME.search(stem) else []


def relative_date_flags(text):
    return [('check', 'relative date: line %d "%s"' % (n, m.group(0)))
            for n, line in enumerate(numbered_lines(text), 1) for m in RELATIVE_DATE.finditer(line)]


def is_path(span):
    if '://' in span or span.startswith('-') or any(c in span for c in '<$*{'):
        return False
    return span.startswith('~/') or ('/' in span and bool(PATH_END.search(span)))


def path_flags(text, repo, exists=os.path.exists):
    """Flag each backticked path that does not exist; a relative path counts from the repo root."""
    flags = []
    for n, line in enumerate(numbered_lines(text), 1):
        for span in BACKTICKED.findall(line):
            path = LINE_SUFFIX.sub('', span)
            if is_path(path) and redact(path) == path and not exists(os.path.join(repo, os.path.expanduser(path))):
                flags.append(('check', 'dead path: line %d `%s`' % (n, path)))
    return flags


def duplicate_flags(bodies):
    """Flag exact duplicates (drop; the first by name survives) and near duplicates (check)."""
    flags = {name: [] for name in bodies}
    first = {}
    for name in sorted(bodies):
        key = bodies[name].strip()
        if key in first:
            flags[name].append(('drop', 'exact duplicate of ' + first[key]))
        elif key:
            first[key] = name
    unique = sorted(first.values())
    words = {name: bodies[name].split() for name in unique}
    for i, a in enumerate(unique):
        for b in unique[i + 1:]:
            m = difflib.SequenceMatcher(None, words[a], words[b], autojunk=False)
            if min(m.real_quick_ratio(), m.quick_ratio()) >= NEAR_DUPLICATE_RATIO and m.ratio() >= NEAR_DUPLICATE_RATIO:
                flags[a].append(('check', 'near duplicate of %s (ratio %.2f)' % (b, m.ratio())))
                flags[b].append(('check', 'near duplicate of %s (ratio %.2f)' % (a, m.ratio())))
    return flags


def unquote(value):
    value = value.strip()
    if len(value) > 1 and value[0] == value[-1] and value[0] in '"\'':
        return value[1:-1]
    return '' if value in ('>', '|', '>-', '|-') else value


def parse_frontmatter(text):
    """Return (fields, body, problem) for the YAML subset notes use: scalars and 1 level of maps."""
    lines = text.split('\n')
    if lines[0].strip() != '---':
        return {}, text, 'frontmatter missing'
    end = next((i for i, line in enumerate(lines) if i and line.strip() == '---'), None)
    if end is None:
        return {}, text, 'frontmatter not parseable'
    meta, parent, last = {}, None, None
    for line in lines[1:end]:
        if not line.strip() or line.lstrip().startswith('#'):
            continue
        indented = line[0] in ' \t'
        key, colon, value = line.strip().partition(':')
        key = key.strip()
        if indented and parent is not None and colon:
            parent[key] = unquote(value)
            last = (parent, key)
        elif indented and last:  # continuation of a folded scalar
            last[0][last[1]] = (last[0][last[1]] + ' ' + line.strip()).strip()
        elif not indented and colon and key:
            if value.strip():
                meta[key], parent, last = unquote(value), None, (meta, key)
            else:
                meta[key] = parent = {}
                last = None
        else:
            return {}, text, 'frontmatter not parseable'
    return meta, '\n'.join(lines[end + 1:]), None


def field(meta, key):
    """Return metadata.<key>, else the top-level <key>, when it is a non-empty string."""
    nested = meta.get('metadata')
    value = (nested.get(key) if isinstance(nested, dict) else None) or meta.get(key)
    return value if isinstance(value, str) and value else None


def frontmatter_flags(meta, problem):
    if problem:
        return [('fix', problem)]
    flags = [('fix', 'no ' + k) for k in ('name', 'description') if not str(meta.get(k) or '').strip()]
    typ = field(meta, 'type')
    if typ is None:
        flags.append(('fix', 'no type'))
    elif typ not in NOTE_TYPES:
        flags.append(('fix', 'type %s not one of %s' % (redact(typ)[:30], ', '.join(NOTE_TYPES))))
    return flags


def age_days(meta, mtime, today):
    """Days since metadata.modified, else since the file mtime."""
    try:
        day = datetime.date.fromisoformat(str(field(meta, 'modified'))[:10])
    except ValueError:
        day = datetime.date.fromtimestamp(mtime)
    return (today - day).days


def index_rows(text, size, exists):
    """Return (rows, targets): the defects of the index, and the normalized paths its links point to."""
    lines = numbered_lines(text)
    rows, targets = [], set()
    if len(lines) > INDEX_MAX_LINES:
        rows.append(('fix', 'index has %d lines, limit %d' % (len(lines), INDEX_MAX_LINES)))
    if size > INDEX_MAX_BYTES:
        rows.append(('fix', 'index has %d bytes, limit %d' % (size, INDEX_MAX_BYTES)))
    for n, line in enumerate(lines, 1):
        if len(line) > INDEX_MAX_ENTRY_CHARS:
            rows.append(('fix', 'line %d has %d characters, limit %d' % (n, len(line), INDEX_MAX_ENTRY_CHARS)))
        for target in LINK.findall(line):
            target = target.split('#')[0]
            if not target or ':' in target:  # a URL, mailto, or anchor
                continue
            target = os.path.normpath(target)
            targets.add(target)
            if not exists(target):
                rows.append(('fix', 'line %d points to missing file %s' % (n, redact(target))))
    return rows + credential_flags(text), targets


def classify(flags):
    return next((c for c in CLASSES if any(f[0] == c for f in flags)), 'keep')


# Transcripts: undocumented JSON lines; every reader tolerates any line.

def parse_line(raw):
    """Return the entry on a raw transcript line, or None for a blob, bad JSON, or an entry without type."""
    if b'api-request-blob' in raw[:BLOB_PREFIX_BYTES]:
        return None
    try:
        entry = json.loads(raw.decode('utf-8', 'replace'))
    except (ValueError, RecursionError):
        return None
    return entry if isinstance(entry, dict) and 'type' in entry else None


def tool_uses(entry):
    message = entry.get('message')
    content = message.get('content') if isinstance(message, dict) else None
    if entry.get('type') != 'assistant' or not isinstance(content, list):
        return []
    return [b for b in content if isinstance(b, dict) and b.get('type') == 'tool_use']


def writes_note(block, name):
    inp = block.get('input')
    path = inp.get('file_path') if isinstance(inp, dict) else None
    return block.get('name') in WRITE_TOOLS and isinstance(path, str) and path.endswith('memory/' + name)


def used_notes(block, names):
    text = json.dumps(block.get('input'), ensure_ascii=False)
    return [n for n in names if 'memory/' + n in text and not writes_note(block, n)]


def count_uses(paths, names):
    """Return ({note: ids of sessions with a tool call naming it}, whether any transcript line parsed)."""
    uses = {name: set() for name in names}
    readable = False
    for path in paths:
        session = os.path.basename(path)[:-len('.jsonl')]
        try:
            with open(path, 'rb') as f:
                for raw in f:
                    if readable and b'memory/' not in raw:  # cheap test before the JSON parse
                        continue
                    entry = parse_line(raw)
                    if entry is None:
                        continue
                    readable = True
                    for block in tool_uses(entry):
                        for name in used_notes(block, names):
                            uses[name].add(session)
        except OSError:
            continue
    return uses, readable


def typed_text(entry):
    """Return the text a person typed, or None for any other entry."""
    message = entry.get('message')
    if entry.get('type') != 'user' or entry.get('isMeta') or entry.get('isSidechain') or not isinstance(message, dict):
        return None
    content = message.get('content')
    if isinstance(content, str):
        text = content
    elif isinstance(content, list) and content and all(isinstance(b, dict) and b.get('type') == 'text' for b in content):
        text = ' '.join(str(b.get('text', '')) for b in content)
    else:
        return None
    return None if text.lstrip().startswith(HARNESS_TEXT) else text


def clip(text, limit):
    text = ' '.join(text.split())
    return text if len(text) <= limit else text[:limit] + '...'


def origin_extract(path, name):
    """Return a bounded extract of a transcript: typed messages before the first write of the note, and write times."""
    writes, before, readable = [], deque(maxlen=ORIGIN_MESSAGES), False
    try:
        with open(path, 'rb') as f:
            for raw in f:
                entry = parse_line(raw)
                if entry is None:
                    continue
                readable = True
                stamp = clip(redact(str(entry.get('timestamp') or 'no timestamp')), 40)
                writes += ['%s %s' % (stamp, b.get('name')) for b in tool_uses(entry) if writes_note(b, name)]
                text = None if writes else typed_text(entry)
                if text:
                    before.append('  %s %s' % (stamp, clip(redact(text), ORIGIN_MESSAGE_CHARS)))
    except OSError:
        return 'origin: unknown'
    if not readable:
        return 'origin: unknown'
    lines = ['origin: ' + path, 'typed messages before the first write, oldest first:']
    lines += list(before) or ['  none']
    lines += ['write: ' + w for w in writes[:ORIGIN_MAX_WRITES]] or ['write: none in this transcript']
    if len(writes) > ORIGIN_MAX_WRITES:
        lines.append('write: %d more' % (len(writes) - ORIGIN_MAX_WRITES))
    return '\n'.join(lines)[:ORIGIN_MAX_CHARS]


# Edges: files, git, clock, and output.

def read_regular(path, root):
    """Return (bytes, mtime, problem); read only a regular file whose real path is inside root."""
    real = os.path.realpath(path)
    if os.path.commonpath([real, root]) != root:
        return None, None, 'symlink out of the memory folder'
    if not os.path.isfile(real):
        return None, None, 'not a regular file'
    try:
        with open(real, 'rb') as f:
            data, mtime = f.read(), os.fstat(f.fileno()).st_mtime
    except OSError as e:
        return None, None, 'not readable: %s' % (e.strerror or 'error')
    if b'\0' in data:
        return None, None, 'binary content'
    return data, mtime, None


def decode(data):
    return data.decode('utf-8', 'replace').replace('\r\n', '\n')


def origin_path(memory_dir, meta):
    """Return the transcript of the session that wrote the note, when it exists."""
    session = field(meta, 'originSessionId')
    if not session or not SESSION_ID.match(session):
        return None
    path = os.path.join(os.path.dirname(memory_dir), session + '.jsonl')
    return path if os.path.isfile(path) else None


def scan(memory_dir, repo, today):
    """Return the report: 1 line per note, then the index rows, then the summary."""
    root = os.path.realpath(memory_dir)
    names = sorted(n for n in os.listdir(memory_dir) if n.endswith('.md') and n != INDEX)
    index_path = os.path.join(memory_dir, INDEX)
    index, targets = [('fix', 'index missing')], set()
    if os.path.lexists(index_path):
        data, _, problem = read_regular(index_path, root)
        index, targets = ([('fix', 'index ' + problem)], set()) if problem else index_rows(
            decode(data), len(data), lambda t: os.path.exists(os.path.join(memory_dir, t)))
    parent = os.path.dirname(memory_dir)
    transcripts = [p for p in sorted(glob.glob(os.path.join(glob.escape(parent), '*.jsonl')))
                   if os.path.isfile(p) and not os.path.islink(p)]
    uses, readable = count_uses(transcripts, names)
    notes, bodies = {}, {}
    for name in names:
        data, mtime, problem = read_regular(os.path.join(memory_dir, name), root)
        if problem:
            notes[name] = ('-', '-', '-', [('check', 'unreadable: ' + problem)], 'none')
            continue
        text = decode(data)
        meta, body, fm_problem = parse_frontmatter(text)
        typ, age, session = field(meta, 'type'), age_days(meta, mtime, today), field(meta, 'originSessionId')
        count = len(uses[name] - {session}) if readable and session else None
        flags = (frontmatter_flags(meta, fm_problem) + name_flags(name) + relative_date_flags(text)
                 + path_flags(text, repo) + credential_flags(text))
        if name not in targets:
            flags.append(('fix', 'not in the index'))
        if typ == 'project' and age >= STALE_DAYS:
            flags.append(('check', 'project note %d days old' % age))
        if not body.strip():
            flags.append(('drop', 'empty body'))
        if name_flags(name) and typ == 'project' and count == 0 and age >= STALE_DAYS:
            flags.append(('drop', 'dated file name, project, 0 uses, %d days old' % age))
        bodies[name] = body
        notes[name] = (typ if typ in NOTE_TYPES else '-', '%dd' % age, 'unknown' if count is None else count,
                       flags, origin_path(memory_dir, meta) or 'none')
    for name, extra in duplicate_flags(bodies).items():
        notes[name][3].extend(extra)
    out = ['scan: memory %s, repo %s, today %s' % (memory_dir, repo, today)]
    for name in sorted(notes, key=lambda n: (CLASSES.index(classify(notes[n][3])), n)):
        typ, age, count, flags, origin = notes[name]
        shown = '; '.join('%s (%s)' % (detail, c) for c, detail in flags) or 'none'
        out.append(' | '.join([classify(flags), name, 'type=' + typ, 'age=' + age, 'uses=%s' % count,
                               'flags: ' + shown, 'origin=' + origin]))
    out += ['%s | %s | %s' % (c, INDEX, detail) for c, detail in index]
    classes = [classify(n[3]) for n in notes.values()]
    flagged = [c for n in notes.values() for c, _ in n[3]] + [c for c, _ in index]
    out.append('summary: %d notes: %s; flags: %s, of which %d on the index' % (
        len(notes), ', '.join('%s %d' % (c, classes.count(c)) for c in CLASSES),
        ', '.join('%s %d' % (c, flagged.count(c)) for c in CLASSES[:-1]), len(index)))
    return out


def git_roots(start):
    """Return (work tree top level, main work tree root) of start; both are start outside git."""
    try:
        done = subprocess.run(['git', '-C', start, 'rev-parse', '--path-format=absolute', '--show-toplevel',
                               '--git-common-dir'], capture_output=True, text=True, timeout=10)
    except (OSError, subprocess.SubprocessError):
        return start, start
    lines = done.stdout.splitlines()
    if done.returncode != 0 or len(lines) != 2:
        return start, start
    top, common = lines
    return top, os.path.dirname(common) if os.path.basename(common) == '.git' else top


def default_memory_dir(root):
    """Claude Code names the project folder after the main work tree root."""
    return os.path.join(os.path.expanduser('~/.claude/projects'), re.sub(r'[^A-Za-z0-9]', '-', root), 'memory')


def date_arg(value):
    try:
        return datetime.date.fromisoformat(value)
    except ValueError:
        raise argparse.ArgumentTypeError('expected YYYY-MM-DD, got %s' % value)


def main(argv=None):
    parser = argparse.ArgumentParser(prog='triage.py', description=__doc__.split('\n')[0])
    parser.add_argument('--memory-dir', help='memory folder (default: the folder Claude Code uses for --repo)')
    parser.add_argument('--repo', help='repository root for relative paths (default: git top level of the current directory)')
    parser.add_argument('--today', type=date_arg, default=datetime.date.today(), help='current date, YYYY-MM-DD')
    parser.add_argument('--origin', metavar='NOTE', help='print a bounded extract of the transcript that wrote NOTE')
    args = parser.parse_args(argv)
    if args.repo and not os.path.isdir(args.repo):
        parser.error('--repo %s: not a directory' % args.repo)
    repo, main_root = git_roots(os.path.abspath(args.repo or os.getcwd()))
    memory = os.path.abspath(os.path.expanduser(args.memory_dir)) if args.memory_dir else default_memory_dir(main_root)
    if not os.path.isdir(memory):
        print('triage.py: memory folder %s: does not exist' % memory, file=sys.stderr)
        return 1
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(errors='backslashreplace')  # a file name with bad bytes must not stop the output
    if args.origin is None:
        try:
            print('\n'.join(scan(memory, repo, args.today)))
        except OSError as e:
            print('triage.py: memory folder %s: %s' % (memory, e.strerror), file=sys.stderr)
            return 1
        return 0
    name = args.origin
    if os.path.basename(name) != name or not name.endswith('.md') or name == INDEX:
        parser.error('--origin %s: give the file name of a note in the memory folder' % name)
    if not os.path.lexists(os.path.join(memory, name)):
        parser.error('--origin %s: no such note in %s' % (name, memory))
    data, _, problem = read_regular(os.path.join(memory, name), os.path.realpath(memory))
    if problem:
        parser.error('--origin %s: %s' % (name, problem))
    path = origin_path(memory, parse_frontmatter(decode(data))[0])
    print(origin_extract(path, name) if path else 'origin: unknown')
    return 0


if __name__ == '__main__':
    sys.exit(main())
