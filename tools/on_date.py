"""Prints an act, or one provision of it, as it stood on a given day, from this repository's history.

    python tools/on_date.py 2018-01-01 stamp-duties 19B        # section 19B of the Stamp Duties Act 2005 on 1 January 2018
    python tools/on_date.py 2023-01-01 stamp-duties sch-1      # Schedule 1
    python tools/on_date.py 2024-01-01 stamp-duties            # the whole act
    python tools/on_date.py 2020-01-01 constitution annex1/8   # section 8 of the Constitution (Annex 1 to the Order)

Each commit carries the day its change took effect in an `In-force:` trailer. The text in force on a day is the last commit
on or before it. Standard library only.
"""
import re
import subprocess
import sys


def git(*args: str) -> str:
    return subprocess.run(['git', *args], capture_output=True, text=True, encoding='utf-8', check=True).stdout


FOLDERS = {'': 0, 'order': 0, 'annex1': 1, 'annex2': 2}
NAMES = {'front': 0, 'arrangement': 1, 'preamble': 2, 'head': 2, 'intro': 3}


def order(path: str) -> tuple:
    parts = path.split('/')[1:]
    name = parts[-1][:-3]
    folder = parts[0] if len(parts) > 1 else ''
    if name in NAMES:
        r = (NAMES[name], 0, '')
    else:
        m = re.fullmatch(r's-(\d+)([A-Z]*)', name)
        r = (4, int(m.group(1)), m.group(2)) if m else (5, int(re.sub(r'\D', '', name) or 0), name)
    return (FOLDERS.get(folder, 9), *r)


def file_for(arg: str) -> str:
    folder, _, name = arg.rpartition('/')
    m = re.fullmatch(r'(\d+)([a-zA-Z]*)', name)
    if m:
        name = f's-{int(m.group(1)):03d}{m.group(2).upper()}'
    return (folder + '/' if folder else '') + (name if name.endswith('.md') else name + '.md')


def commit_on(day: str, act: str) -> str:
    """The commit whose In-force day is the latest one on or before the day."""
    out = git('log', '--format=%H%x09%(trailers:key=In-force,valueonly,separator=)', 'main', '--', act)
    best = ('', '')
    for line in out.splitlines():
        h, _, d = line.partition('\t')
        d = d.strip()
        if d and d <= day and d > best[1]:
            best = (h, d)
    return best[0]


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    if len(sys.argv) < 3 or not re.fullmatch(r'\d{4}-\d{2}-\d{2}', sys.argv[1]):
        sys.exit(__doc__)
    day, act = sys.argv[1], sys.argv[2].strip('/')
    commit = commit_on(day, act)
    if not commit:
        sys.exit(f'{act} is not in the record on {day}.')
    if len(sys.argv) > 3:
        name = file_for(sys.argv[3])
        try:
            sys.stdout.write(git('show', f'{commit}:{act}/{name}'))
        except subprocess.CalledProcessError:
            sys.exit(f'{act}/{name} was not in the text on {day}.')
        return
    files = [f for f in git('ls-tree', '-r', '--name-only', commit, f'{act}/').split('\n')
             if f.endswith('.md') and not f.endswith('/README.md')]
    for f in sorted(files, key=order):
        sys.stdout.write(git('show', f'{commit}:{f}') + '\n')


if __name__ == '__main__':
    main()
