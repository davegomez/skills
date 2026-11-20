"""Tests for skills/memory-triage/scripts/triage.py.

Run from the repository root:
    python3 -m unittest discover -s supporting/memory-triage/tests
"""
import contextlib
import datetime
import hashlib
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.normpath(os.path.join(HERE, '..', '..', '..', 'skills', 'memory-triage', 'scripts', 'triage.py'))
sys.path.insert(0, os.path.dirname(SCRIPT))
import triage  # noqa: E402

TODAY = datetime.date(2026, 3, 1)
OLD = '2026-01-01T10:00:00.000Z'  # 59 days before TODAY
NEW = '2026-02-27T10:00:00.000Z'
TODAY_ARG = '--today=2026-03-01'

# Planted credentials are built at run time: no committed file holds a literal in a real format.
AWS_KEY = 'AK' + 'IA' + 'ABCDEFGHIJKLMNOP'
PASSWORD = 'pl4nted' + '-' + 'Vq9x' + 'Rw2z'


def note(name, body, typ='feedback', modified=NEW, origin='s-origin'):
    """A note in the shape Claude Code writes; its body starts on line 11."""
    lines = ['---', 'name: ' + name, 'description: "One line about %s."' % name, 'metadata:', '  node_type: memory']
    if typ is not None:
        lines.append('  type: ' + typ)
    lines.append('  originSessionId: ' + origin if origin is not None else '  other: x')
    lines.append('  modified: ' + modified)
    return '\n'.join(lines + ['---', '', body, ''])


def write(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'wb') as f:
        f.write(content if isinstance(content, bytes) else content.encode())


def jl(entry):
    return json.dumps(entry) + '\n'


def tool(name, **inp):
    return {'type': 'assistant', 'timestamp': '2026-01-01T10:05:00Z',
            'message': {'content': [{'type': 'tool_use', 'name': name, 'input': inp}]}}


def typed(text, stamp='2026-01-01T10:00:00Z', **extra):
    return dict({'type': 'user', 'timestamp': stamp, 'message': {'role': 'user', 'content': text}}, **extra)


NEAR = ('The staging deploy needs the feature flag set before the migration runs, '
        'otherwise the worker restarts in a loop and the queue backs up for an hour.')
NOTES = {
    'good.md': note('good', 'Lint from the entry point `src/app.py` before each push.'),
    'no-type.md': note('no-type', 'Reviewers want small pull requests.', typ=None),
    'orphan.md': note('orphan', 'Prefer the standard library for parsing dates.'),
    'stale.md': note('stale', 'The billing rewrite is paused for the audit.', typ='project', modified=OLD),
    'release-2026-01-05.md': note('release', 'Release candidate four passed smoke checks.', typ='project', modified=OLD),
    'deploy_2026_01_02.md': note('deploy', 'Cutover window moved to the weekend slot.', typ='project', modified=OLD),
    'relative.md': note('relative', 'The nightly build broke yesterday after the upgrade.'),
    'dead-path.md': note('dead-path', 'Config lives in `src/missing.py` and `~/no-such-dir-triage-test/`.'),
    'secret.md': note('secret', 'Access key id ' + AWS_KEY + ' for uploads.\nAdmin password: ' + PASSWORD),
    'dup-a.md': note('dup-a', 'Use tabs in the Makefile and spaces elsewhere.'),
    'dup-b.md': note('dup-b', 'Use tabs in the Makefile and spaces elsewhere.'),
    'near-a.md': note('near-a', NEAR),
    'near-b.md': note('near-b', NEAR.replace('an hour', 'two hours')),
    'empty.md': note('empty', ''),
    'broken.md': '---\nname: broken\nno closing marker\n',
}
INDEXED = [n for n in NOTES if n not in ('orphan.md', 'secret.md')] + ['folder.md', 'outside.md', 'binary.md']


def build_fixture(root):
    """Make repo/ and projects/p/memory/ with planted defects and 3 transcripts; return (memory dir, repo dir)."""
    repo = os.path.join(root, 'repo')
    mem = os.path.join(root, 'projects', 'p', 'memory')
    write(os.path.join(repo, 'src', 'app.py'), 'print(1)\n')
    for name, text in NOTES.items():
        write(os.path.join(mem, name), text)
    os.makedirs(os.path.join(mem, 'folder.md'))
    write(os.path.join(root, 'outside.md'), note('outside', 'Outside the memory folder.'))
    os.symlink(os.path.join(root, 'outside.md'), os.path.join(mem, 'outside.md'))
    write(os.path.join(mem, 'binary.md'), b'\x00\x01\x02')
    index = ['# Memory'] + ['- [%s](%s) - pointer' % (n[:-3], n) for n in INDEXED]
    index += ['- [gone](gone.md) - dead pointer', '- [site](https://example.com/a.md) - a link', '- ' + 'x' * 160]
    write(os.path.join(mem, 'MEMORY.md'), '\n'.join(index) + '\n')
    p = os.path.dirname(mem)
    write(os.path.join(p, 's-origin.jsonl'), ''.join([
        jl(typed('first typed message', '2026-01-01T09:00:00Z')),
        jl(typed('meta text must not show', isMeta=True)),
        jl(typed('sidechain text must not show', isSidechain=True)),
        jl({'type': 'user', 'message': {'content': [{'type': 'tool_result', 'content': 'tool result must not show'}]}}),
        jl(typed([{'type': 'text', 'text': 'remember the admin password: ' + PASSWORD}], '2026-01-01T09:30:00Z')),
        jl({'type': 'api-request-blob', 'data': 'memory/secret.md blob must not show ' + AWS_KEY}),
        'not json memory/secret.md\n',
        '\n',
    ]).encode() + b'\xff\xfe memory/ bad utf-8\n' + ''.join([
        jl(tool('Write', file_path=os.path.join(mem, 'secret.md'), content='key ' + AWS_KEY)),
        jl(typed('after the write must not show')),
        jl(tool('Read', file_path=os.path.join(mem, 'release-2026-01-05.md'))),
        jl(tool('Edit', file_path=os.path.join(mem, 'secret.md'), old_string='a', new_string='b')),
    ]).encode())
    write(os.path.join(p, 's-reader1.jsonl'), jl(tool('Read', file_path=os.path.join(mem, 'deploy_2026_01_02.md')))
          + jl(tool('Bash', command='cat ~/.claude/projects/p/memory/stale.md')))
    write(os.path.join(p, 's-reader2.jsonl'), jl(tool('Read', file_path=os.path.join(mem, 'stale.md')))
          + jl(tool('Edit', file_path=os.path.join(mem, 'good.md'), old_string='a', new_string='b')))
    return mem, repo


def run(*args):
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        try:
            code = triage.main(list(args))
        except SystemExit as e:
            code = e.code
    return code, out.getvalue(), err.getvalue()


def note_lines(output):
    return [l for l in output.splitlines() if l.count(' | ') > 1 and l.split(' | ')[1] != 'MEMORY.md']


def rows(output):
    """Map each note to (class, its row)."""
    return {l.split(' | ')[1]: (l.split(' | ')[0], l) for l in note_lines(output)}


def snapshot(root):
    state = {}
    for d, dirs, files in os.walk(root):
        for n in dirs + files:
            p = os.path.join(d, n)
            if os.path.islink(p):
                state[p] = 'link ' + os.readlink(p)
            elif os.path.isfile(p):
                with open(p, 'rb') as f:
                    state[p] = hashlib.sha256(f.read()).hexdigest()
            else:
                state[p] = 'dir'
    return state


class FixtureTest(unittest.TestCase):
    def setUp(self):
        self.root = os.path.realpath(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.root)
        self.mem, self.repo = build_fixture(self.root)

    def scan(self):
        code, out, err = run('--memory-dir', self.mem, '--repo', self.repo, TODAY_ARG)
        self.assertEqual((code, err), (0, ''))
        return out


class ScanTest(FixtureTest):
    def test_each_planted_note_gets_its_class(self):
        got = {n: c for n, (c, _) in rows(self.scan()).items()}
        self.assertEqual(got, {
            'good.md': 'keep', 'dup-a.md': 'keep',
            'no-type.md': 'fix', 'orphan.md': 'fix', 'broken.md': 'fix',
            'stale.md': 'check', 'deploy_2026_01_02.md': 'check', 'relative.md': 'check',
            'dead-path.md': 'check', 'near-a.md': 'check', 'near-b.md': 'check',
            'folder.md': 'check', 'outside.md': 'check', 'binary.md': 'check',
            'release-2026-01-05.md': 'drop', 'dup-b.md': 'drop', 'empty.md': 'drop',
            'secret.md': 'alert',
        })

    def test_rows_come_in_class_order(self):
        classes = [l.split(' | ')[0] for l in note_lines(self.scan())]
        self.assertEqual(classes, sorted(classes, key=triage.CLASSES.index))

    def test_row_shows_type_age_uses_flags_and_origin(self):
        r = rows(self.scan())
        self.assertIn('stale.md | type=project | age=59d | uses=2 | ', r['stale.md'][1])
        self.assertIn('project note 59 days old', r['stale.md'][1])
        self.assertTrue(r['stale.md'][1].endswith('origin=' + os.path.join(os.path.dirname(self.mem), 's-origin.jsonl')))
        self.assertIn('uses=1', r['deploy_2026_01_02.md'][1])
        self.assertIn('uses=0', r['good.md'][1])  # an Edit is not a use
        self.assertIn('uses=0', r['release-2026-01-05.md'][1])  # a read in the origin session is not a use
        self.assertIn('dated file name (check)', r['release-2026-01-05.md'][1])
        self.assertIn('dated file name, project, 0 uses, 59 days old (drop)', r['release-2026-01-05.md'][1])
        self.assertIn('exact duplicate of dup-a.md', r['dup-b.md'][1])
        self.assertIn('near duplicate of near-b.md', r['near-a.md'][1])
        self.assertIn('dead path: line 11 `src/missing.py`', r['dead-path.md'][1])
        self.assertIn('`~/no-such-dir-triage-test/`', r['dead-path.md'][1])
        self.assertIn('relative date: line 11 "yesterday"', r['relative.md'][1])
        self.assertIn('symlink out of the memory folder', r['outside.md'][1])
        self.assertIn('not a regular file', r['folder.md'][1])
        self.assertEqual('check | binary.md | type=- | age=- | uses=- | flags: unreadable: binary content (check) | origin=none',
                         r['binary.md'][1])

    def test_alert_note_lists_every_flag_and_no_value(self):
        out = self.scan()
        line = rows(out)['secret.md'][1]
        self.assertIn('credential-like value: line 11 (aws-access-key)', line)
        self.assertIn('credential-like value: line 12 (keyword=value)', line)
        self.assertIn('not in the index (fix)', line)
        self.assertNotIn(AWS_KEY, out)
        self.assertNotIn(PASSWORD, out)

    def test_index_rows_and_summary_count_hidden_fix_flags(self):
        lines = self.scan().splitlines()
        index = [l for l in lines if l.startswith('fix | MEMORY.md | ')]
        self.assertEqual(len(index), 2)
        self.assertIn('points to missing file gone.md', index[0] + index[1])
        self.assertIn('has 162 characters, limit 150', index[0] + index[1])
        self.assertEqual(lines[-1], 'summary: 18 notes: alert 1, drop 3, check 9, fix 3, keep 2; '
                                    'flags: alert 2, drop 3, check 13, fix 6, of which 2 on the index')

    def test_line_numbers_count_newline_characters_only(self):
        # perl -ne counts $. by newline; str.splitlines() also splits on U+2028, form feed and others
        body = 'Wrapped\u2028text\x0cwith a feed\rand a carriage return.\nAccess key id ' + AWS_KEY + ' for uploads.'
        write(os.path.join(self.mem, 'feed.md'), note('feed', body))
        text = note('feed', body)
        line = text[:text.index(AWS_KEY)].count('\n') + 1
        self.assertIn('credential-like value: line %d (aws-access-key)' % line, rows(self.scan())['feed.md'][1])

    def test_scan_changes_no_file(self):
        before = snapshot(self.root)
        self.scan()
        run('--memory-dir', self.mem, '--origin', 'secret.md')
        self.assertEqual(snapshot(self.root), before)

    def test_unreadable_transcripts_give_unknown_uses_and_no_drop(self):
        p = os.path.dirname(self.mem)
        for n in os.listdir(p):
            if n.endswith('.jsonl'):
                os.remove(os.path.join(p, n))
        write(os.path.join(p, 'junk.jsonl'), 'not json\n')
        r = rows(self.scan())
        self.assertIn('uses=unknown', r['release-2026-01-05.md'][1])
        self.assertEqual(r['release-2026-01-05.md'][0], 'check')
        self.assertIn('origin=none', r['release-2026-01-05.md'][1])

    def test_note_without_origin_has_unknown_uses(self):
        write(os.path.join(self.mem, 'good.md'), note('good', 'Body text here.', origin=None))
        self.assertIn('uses=unknown', rows(self.scan())['good.md'][1])

    def test_unreadable_note_does_not_stop_the_scan(self):
        os.chmod(os.path.join(self.mem, 'good.md'), 0)
        self.addCleanup(os.chmod, os.path.join(self.mem, 'good.md'), 0o644)
        if os.access(os.path.join(self.mem, 'good.md'), os.R_OK):
            self.skipTest('running as a user who can read any file')
        r = rows(self.scan())
        self.assertIn('unreadable: not readable: Permission denied', r['good.md'][1])
        self.assertEqual(r['secret.md'][0], 'alert')

    def test_missing_index_is_a_fix_row(self):
        os.remove(os.path.join(self.mem, 'MEMORY.md'))
        out = self.scan()
        self.assertIn('fix | MEMORY.md | index missing', out)
        self.assertEqual(rows(out)['good.md'][0], 'fix')

    def test_unreadable_index_is_a_fix_row(self):
        os.remove(os.path.join(self.mem, 'MEMORY.md'))
        os.makedirs(os.path.join(self.mem, 'MEMORY.md'))
        self.assertIn('fix | MEMORY.md | index not a regular file', self.scan())


class OriginTest(FixtureTest):
    def origin(self, name):
        code, out, err = run('--memory-dir', self.mem, '--origin', name)
        self.assertEqual((code, err), (0, ''))
        return out

    def test_extract_holds_typed_messages_before_first_write_and_write_times(self):
        out = self.origin('secret.md')
        self.assertIn('first typed message', out)
        self.assertIn('2026-01-01T09:30:00Z remember the admin password: [credential-like value removed]', out)
        self.assertIn('write: 2026-01-01T10:05:00Z Write', out)
        self.assertIn('write: 2026-01-01T10:05:00Z Edit', out)
        for hidden in ('must not show', PASSWORD, AWS_KEY):
            self.assertNotIn(hidden, out)

    def test_unknown_when_transcript_absent(self):
        write(os.path.join(self.mem, 'lost.md'), note('lost', 'Body.', origin='no-such-session'))
        self.assertEqual(self.origin('lost.md'), 'origin: unknown\n')
        write(os.path.join(self.mem, 'bad.md'), note('bad', 'Body.', origin='../escape'))
        self.assertEqual(self.origin('bad.md'), 'origin: unknown\n')

    def test_unknown_when_no_line_parses(self):
        write(os.path.join(os.path.dirname(self.mem), 's-origin.jsonl'), 'garbage\n')
        self.assertEqual(self.origin('secret.md'), 'origin: unknown\n')

    def test_extract_is_bounded(self):
        lines = [jl(typed('message %d ' % i + 'w ' * 3000)) for i in range(50)]
        lines += [jl(tool('Edit', file_path='/m/memory/good.md')) for _ in range(30)]
        write(os.path.join(os.path.dirname(self.mem), 's-origin.jsonl'), ''.join(lines))
        out = self.origin('good.md')
        self.assertLessEqual(len(out), triage.ORIGIN_MAX_CHARS + 1)
        self.assertIn('message 49 ', out)
        self.assertNotIn('message 46 ', out)
        self.assertIn('write: 20 more', out)

    def test_extract_skips_slash_command_wrappers(self):
        wrappers = ['<command-name>/clear</command-name>', '  <command-message>clear</command-message>',
                    '<local-command-stdout>done</local-command-stdout>', '\n<local-command-caveat>x</local-command-caveat>']
        lines = [jl(typed('typed %d' % i)) for i in range(4)] + [jl(typed(w)) for w in wrappers]
        lines += [jl(typed([{'type': 'text', 'text': '<command-name>/memory</command-name>'}]))]
        lines += [jl(tool('Write', file_path='/m/memory/good.md'))]
        write(os.path.join(os.path.dirname(self.mem), 's-origin.jsonl'), ''.join(lines))
        out = self.origin('good.md')
        self.assertIn('typed 1', out)
        self.assertIn('typed 3', out)
        self.assertNotIn('typed 0', out)
        self.assertNotIn('command-', out)

    def test_no_write_in_transcript(self):
        self.assertIn('write: none in this transcript', self.origin('orphan.md'))

    def test_usage_errors(self):
        for name in ('../secret.md', 'nope.md', 'secret.txt', 'binary.md', 'MEMORY.md'):
            code, _, err = run('--memory-dir', self.mem, '--origin', name)
            self.assertEqual(code, 2)
            self.assertIn(name, err)
            self.assertNotIn('Traceback', err)


class CliTest(unittest.TestCase):
    def test_missing_memory_folder_exits_1_with_message(self):
        p = subprocess.run([sys.executable, SCRIPT, '--memory-dir', '/no/such/memory'], capture_output=True, text=True)
        self.assertEqual(p.returncode, 1)
        self.assertEqual(p.stderr, 'triage.py: memory folder /no/such/memory: does not exist\n')

    def test_bad_date_is_a_usage_error(self):
        code, _, err = run('--today', 'March')
        self.assertEqual(code, 2)
        self.assertIn('YYYY-MM-DD', err)

    def test_bad_repo_is_a_usage_error(self):
        code, _, err = run('--repo', '/no/such/repo')
        self.assertEqual(code, 2)
        self.assertIn('/no/such/repo', err)

    def test_git_roots_use_the_main_work_tree(self):
        root = os.path.realpath(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, root)
        main, wt = os.path.join(root, 'main.repo'), os.path.join(root, 'wt')
        git = ['git', '-c', 'user.name=t', '-c', 'user.email=t@t', '-c', 'commit.gpgsign=false']
        subprocess.run(git + ['init', '-q', main], check=True)
        subprocess.run(git + ['-C', main, 'commit', '-q', '--allow-empty', '-m', 'x'], check=True)
        subprocess.run(git + ['-C', main, 'worktree', 'add', '-q', wt], check=True, capture_output=True)
        os.makedirs(os.path.join(main, 'sub'))
        self.assertEqual(triage.git_roots(os.path.join(main, 'sub')), (main, main))
        self.assertEqual(triage.git_roots(wt), (wt, main))
        self.assertEqual(triage.git_roots(root), (root, root))
        self.assertEqual(triage.default_memory_dir('/a/b.c d'), os.path.expanduser('~/.claude/projects/-a-b-c-d/memory'))

    def test_default_memory_dir_comes_from_the_current_directory(self):
        root = os.path.realpath(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, root)
        cwd = os.getcwd()
        os.chdir(root)
        self.addCleanup(os.chdir, cwd)
        code, _, err = run()
        self.assertEqual(code, 1)
        self.assertIn(triage.default_memory_dir(root), err)


class FrontmatterTest(unittest.TestCase):
    def test_nested_and_top_level_type(self):
        meta, body, problem = triage.parse_frontmatter(note('a', 'Body.', typ='user'))
        self.assertIsNone(problem)
        self.assertEqual(triage.field(meta, 'type'), 'user')
        self.assertEqual(meta['description'], 'One line about a.')
        self.assertEqual(body.strip(), 'Body.')
        meta, _, _ = triage.parse_frontmatter("---\nname: a\ntype: 'reference'\n# comment\n\n---\nx")
        self.assertEqual(triage.field(meta, 'type'), 'reference')

    def test_folded_scalar_continues(self):
        meta, _, problem = triage.parse_frontmatter('---\ndescription: >\n  first\n  second\nmetadata:\n  type: user\n---\n')
        self.assertIsNone(problem)
        self.assertEqual(meta['description'], 'first second')

    def test_defects(self):
        self.assertEqual(triage.parse_frontmatter('no frontmatter')[2], 'frontmatter missing')
        self.assertEqual(triage.parse_frontmatter('---\nname: a\n')[2], 'frontmatter not parseable')
        self.assertEqual(triage.parse_frontmatter('---\njust words\n---\n')[2], 'frontmatter not parseable')
        self.assertEqual(triage.parse_frontmatter('---\n  indented: first\n---\n')[2], 'frontmatter not parseable')
        flags = triage.frontmatter_flags({'name': ' ', 'type': 'Project'}, None)
        self.assertEqual(flags, [('fix', 'no name'), ('fix', 'no description'),
                                 ('fix', 'type Project not one of user, feedback, project, reference')])
        self.assertEqual(triage.frontmatter_flags({'name': 'a', 'description': 'b'}, None), [('fix', 'no type')])
        self.assertEqual(triage.frontmatter_flags({}, 'frontmatter missing'), [('fix', 'frontmatter missing')])

    def test_age_from_modified_else_mtime(self):
        self.assertEqual(triage.age_days({'metadata': {'modified': OLD}}, 0, TODAY), 59)
        mtime = datetime.datetime(2026, 2, 20, 12).timestamp()
        self.assertEqual(triage.age_days({'metadata': {'modified': 'soon'}}, mtime, TODAY), 9)
        self.assertEqual(triage.age_days({}, mtime, TODAY), 9)


class DetectorTest(unittest.TestCase):
    def test_name_flags(self):
        self.assertEqual(triage.name_flags('deploy-2026-01-02.md'), [('check', 'dated file name')])
        self.assertEqual(triage.name_flags('deploy_2026_01_02.md'), [('check', 'dated file name')])
        self.assertEqual(triage.name_flags('deploy-2026_01-02.md'), [])
        self.assertEqual(triage.name_flags('run-tests-first.md'), [])

    def test_relative_dates(self):
        text = ('Fixed today.\nDue tomorrow, then next week.\nSeen 3 days ago and 2 months ago.\n'
                'This year it moved.\nThis weekend, todays, weekday, someday, last-minute, a week ago: none.')
        found = [d for _, d in triage.relative_date_flags(text)]
        self.assertEqual(found, ['relative date: line 1 "today"', 'relative date: line 2 "tomorrow"',
                                 'relative date: line 2 "next week"', 'relative date: line 3 "3 days ago"',
                                 'relative date: line 3 "2 months ago"', 'relative date: line 4 "This year"'])

    def test_dead_paths(self):
        root = os.path.realpath(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, root)
        write(os.path.join(root, 'src', 'a.py'), '')
        text = ('`src/a.py` `src/a.py:12` `src/` `./src/a.py` `src/gone.py:3` `docs/old/`\n'
                '`https://x.org/a.md` `<dir>/a.md` `$HOME/a.md` `src/*.py` `--flag/x.md` `a.md` `v1.2/3.4` '
                '`and/or` `x y/z.md`\n'
                '`' + os.path.join(root, 'src', 'a.py') + '` `/no/such/file.txt` `/api/users` `~/no/such/dir/`')
        found = [d for _, d in triage.path_flags(text, root)]
        self.assertEqual(found, ['dead path: line 1 `src/gone.py`', 'dead path: line 1 `docs/old/`',
                                 'dead path: line 3 `/no/such/file.txt`', 'dead path: line 3 `~/no/such/dir/`'])

    def test_credentials(self):
        cases = {
            'aws-access-key': AWS_KEY,
            'github-token': 'gh' + 'p_' + 'a' * 36,
            'sk-api-key': 's' + 'k-' + 'b' * 24,
            'stripe-key': 's' + 'k_live_' + 'c' * 24,
            'google-api-key': 'AI' + 'za' + 'd' * 35,
            'slack-token': 'xo' + 'xb-' + '1' * 12,
            'jwt': 'ey' + 'J' + 'e' * 16 + '.ey' + 'J' + 'f' * 12,
            'private-key': '-----BEGIN RSA ' + 'PRIVATE KEY-----',
            'keyword=value': 'api_key = "' + PASSWORD + '"',
        }
        for kind, text in cases.items():
            flags = triage.credential_flags('intro\nvalue ' + text)
            self.assertEqual(flags, [('alert', 'credential-like value: line 2 (%s)' % kind)], kind)
            self.assertNotIn(text, triage.redact('value ' + text))
        for text in ('password: <your password>', 'token: $GITHUB_TOKEN', 'api_key: your-key-here',
                     'secret: ~/.config/app/key', 'password: keychain-item-name', 'token: short',
                     'tokenizer: a-long-value', 'secret: ********', 'password: REDACTED-VALUE'):
            self.assertEqual(triage.credential_flags(text), [], text)
            self.assertEqual(triage.redact(text), text)

    def test_duplicates(self):
        flags = triage.duplicate_flags({'a.md': NEAR, 'b.md': ' %s\n' % NEAR, 'c.md': NEAR.replace('hour', 'day'),
                                        'd.md': 'Unrelated words about release notes and tags.', 'e.md': ''})
        self.assertEqual(flags['b.md'], [('drop', 'exact duplicate of a.md')])
        self.assertEqual(flags['a.md'], [('check', 'near duplicate of c.md (ratio 0.96)')])
        self.assertEqual(flags['c.md'], [('check', 'near duplicate of a.md (ratio 0.96)')])
        self.assertEqual(flags['d.md'], [])
        self.assertEqual(flags['e.md'], [])
        same_topic = triage.duplicate_flags({'a.md': NEAR, 'b.md': 'The staging deploy needs a flag; '
                                             'set it first or the queue backs up and workers restart.'})
        self.assertEqual(same_topic['a.md'], [])

    def test_index_rows(self):
        lines = ['- [a](a.md)', '- [b](./b.md#part)', '- [u](https://x.org/c.md)', '- [m](mailto:x@y)', '- [g](gone.md)']
        rows_, targets = triage.index_rows('\n'.join(lines + ['line'] * 200), 30000, lambda t: t in ('a.md', 'b.md'))
        self.assertEqual(targets, {'a.md', 'b.md', 'gone.md'})
        self.assertEqual(rows_, [('fix', 'index has 205 lines, limit 200'), ('fix', 'index has 30000 bytes, limit 25000'),
                                 ('fix', 'line 5 points to missing file gone.md')])
        rows_, _ = triage.index_rows('- token: ' + PASSWORD, 10, lambda t: True)
        self.assertEqual(rows_, [('alert', 'credential-like value: line 1 (keyword=value)')])

    def test_line_numbers_count_newline_characters_only(self):
        above = 'a\u2028b\x0cc\x1cd\x85e\rf\n'
        text = above + 'yesterday `src/gone.py`\n'
        self.assertEqual(triage.relative_date_flags(text), [('check', 'relative date: line 2 "yesterday"')])
        self.assertEqual(triage.path_flags(text, '/no/such/root'), [('check', 'dead path: line 2 `src/gone.py`')])
        self.assertEqual(triage.index_rows(above * 200, 10, lambda t: True), ([], set()))
        self.assertEqual(triage.index_rows(above * 200 + '- [g](gone.md)', 10, lambda t: False)[0],
                         [('fix', 'index has 201 lines, limit 200'), ('fix', 'line 201 points to missing file gone.md')])

    def test_classify_takes_highest_class(self):
        self.assertEqual(triage.classify([]), 'keep')
        self.assertEqual(triage.classify([('fix', 'a'), ('check', 'b')]), 'check')
        self.assertEqual(triage.classify([('check', 'a'), ('drop', 'b')]), 'drop')
        self.assertEqual(triage.classify([('drop', 'a'), ('alert', 'b')]), 'alert')


class TranscriptTest(unittest.TestCase):
    def test_parse_line_skips_blob_bad_json_and_untyped(self):
        self.assertIsNone(triage.parse_line(b'{"type":"api-request-blob","x":1}'))
        self.assertIsNone(triage.parse_line(b'{"type":'))
        self.assertIsNone(triage.parse_line(b'[1, 2]'))
        self.assertIsNone(triage.parse_line(b'{"message": {}}'))
        self.assertEqual(triage.parse_line(b'{"type":"user"}'), {'type': 'user'})

    def test_tool_uses_need_an_assistant_list(self):
        self.assertEqual(triage.tool_uses({'type': 'assistant', 'message': 'text'}), [])
        self.assertEqual(triage.tool_uses({'type': 'user', 'message': {'content': [{'type': 'tool_use'}]}}), [])

    def test_count_uses_counts_any_tool_but_a_write_of_the_note(self):
        root = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, root)
        good = os.path.join(root, 's1.jsonl')
        write(good, jl(tool('Grep', pattern='x', path='/p/memory/a.md')) + jl(tool('Write', file_path='/p/memory/a.md'))
              + jl(tool('Write', file_path='/p/other.md', content='see memory/b.md')))
        uses, readable = triage.count_uses([os.path.join(root, 'missing.jsonl'), good], ['a.md', 'b.md', 'c.md'])
        self.assertTrue(readable)
        self.assertEqual(uses, {'a.md': {'s1'}, 'b.md': {'s1'}, 'c.md': set()})

    def test_typed_text(self):
        self.assertEqual(triage.typed_text(typed([{'type': 'text', 'text': 'a'}, {'type': 'text', 'text': 'b'}])), 'a b')
        self.assertIsNone(triage.typed_text(typed([{'type': 'image'}])))
        self.assertIsNone(triage.typed_text(typed([])))
        self.assertIsNone(triage.typed_text({'type': 'user', 'message': None}))


if __name__ == '__main__':
    unittest.main()
