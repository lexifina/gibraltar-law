"""Checks the git repository against the official text: every version of every act on the Gibraltar Laws site, read back
from git on the day it took effect, must equal that version's PDF.

    python -X utf8 scripts/gibraltar-law/check_repo.py [--repo ../gibraltar-law] [--no-record]

Two checks per version, from the cached PDFs (no network):
1. File by file: the act's files in git on that day are exactly the files the build's parser makes from that PDF (same
   set of files, same bytes).
2. Word for word: the whole act printed by tools/on_date.py has the same words in the same order as PyMuPDF's own word
   list for the PDF (header, footer and the table of amending enactments aside), read without the parser.
The result is written to verification.json next to this script (unless --no-record), for REPRODUCE.md.
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import build  # noqa: E402


def commit_on(repo: str, day: str, slug: str) -> str:
    out = subprocess.run(['git', 'log', '--format=%H%x09%(trailers:key=In-force,valueonly,separator=)', 'main', '--', slug],
                         cwd=repo, capture_output=True, text=True, encoding='utf-8').stdout
    best = ('', '')
    for line in out.splitlines():
        h, _, d = line.partition('\t')
        d = d.strip()
        if d and d <= day and d > best[1]:
            best = (h, d)
    return best[0]


def files_at(repo: str, commit: str, slug: str) -> dict[str, str]:
    """The act's files at a commit, read with one ls-tree and one cat-file --batch."""
    out = subprocess.run(['git', 'ls-tree', '-r', commit, f'{slug}/'], cwd=repo, capture_output=True, text=True,
                         encoding='utf-8').stdout.split('\n')
    blobs = []
    for line in out:
        if not line:
            continue
        info, f = line.split('\t', 1)
        if f.endswith('.md') and not f.endswith('/README.md'):
            blobs.append((f[len(slug) + 1:-3], info.split()[2]))
    data = subprocess.run(['git', 'cat-file', '--batch'], cwd=repo, input=''.join(f'{sha}\n' for _, sha in blobs).encode(),
                          capture_output=True).stdout
    res, pos = {}, 0
    for name, _ in blobs:
        nl = data.index(b'\n', pos)
        size = int(data[pos:nl].split()[2])
        res[name] = data[nl + 1:nl + 1 + size].decode('utf-8')
        pos = nl + 1 + size + 1
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', default=str(build.ROOT.parent / 'gibraltar-law'))
    ap.add_argument('--no-record', action='store_true')
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding='utf-8')
    versions = files = bad = wbad = nwords = 0
    per_act = {}
    for act in build.ACTS:
        page = build.act_page(act, offline=True)
        for v in page['versions']:
            raw = build.fetch(v['pdf'], offline=True)
            parsed = build.read_version(raw, act['kind'])
            expected = {k: u['text'] for k, u in parsed['units'].items()}
            commit = commit_on(args.repo, v['from'], act['slug'])
            got = files_at(args.repo, commit, act['slug']) if commit else {}
            versions += 1
            per_act[act['slug']] = per_act.get(act['slug'], 0) + 1
            files += len(expected)
            if got != expected:
                bad += 1
                diff = sorted(set(got) ^ set(expected)) or [k for k in expected if got.get(k) != expected[k]]
                print(f'MISMATCH {act["slug"]} {v["from"]}: {diff[:5]}')
            whole = subprocess.run([sys.executable, '-X', 'utf8', 'tools/on_date.py', v['from'], act['slug']], cwd=args.repo,
                                   capture_output=True, text=True, encoding='utf-8')
            ow, rw = build.official_words(raw, act['kind']), whole.stdout.split()
            nwords += len(ow)
            if whole.returncode or ow != rw:
                wbad += 1
                i = next((i for i, (a, b) in enumerate(zip(ow, rw)) if a != b), min(len(ow), len(rw)))
                print(f'WORDS {act["slug"]} {v["from"]}: official {len(ow)} vs repo {len(rw)}; first difference at {i}: '
                      f'{ow[max(0, i - 4):i + 4]} / {rw[max(0, i - 4):i + 4]}')
    print(f'{versions} versions checked ({files} files), {bad} mismatches; {versions} versions word for word '
          f'({nwords} words), {wbad} mismatches')
    print('per act:', per_act)
    if not args.no_record:
        p = HERE / 'verification.json'
        rec = json.loads(p.read_text(encoding='utf-8')) if p.exists() else {}
        rec['check'] = {'versions': versions, 'files': files, 'mismatches': bad, 'wordcheck': versions, 'words': nwords,
                        'word_mismatches': wbad, 'per_act': per_act}
        p.write_text(json.dumps(rec, indent=1, sort_keys=True) + '\n', encoding='utf-8', newline='\n')
    raise SystemExit(1 if bad or wbad else 0)


if __name__ == '__main__':
    main()
