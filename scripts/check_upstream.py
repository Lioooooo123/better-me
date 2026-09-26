#!/usr/bin/env python3
"""Read upstream branch tips. Does not install, merge or modify any skill."""
from concurrent.futures import ThreadPoolExecutor
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]


def fetch_tree(repository, commit):
    headers = {'Accept': 'application/vnd.github+json', 'User-Agent': 'better-me-upstream-check'}
    with urlopen(Request(f'https://api.github.com/repos/{repository}/git/commits/{commit}',
                         headers=headers), timeout=30) as response:
        root_tree = json.load(response)['tree']['sha']
    request = Request(
        f'https://api.github.com/repos/{repository}/git/trees/{root_tree}?recursive=1',
        headers=headers,
    )
    with urlopen(request, timeout=30) as response:
        payload = json.load(response)
    if payload.get('truncated') or not isinstance(payload.get('tree'), list):
        raise ValueError('Incomplete GitHub tree response')
    trees = {item['path']: item['sha'] for item in payload['tree'] if item['type'] == 'tree'}
    trees['.'] = root_tree
    return trees


def check_skills(repository_result, skills):
    """Compare reviewed folder trees at one fixed tip, never advance the baseline."""
    records = [item for item in skills if item.get('repository') == repository_result['repository']
               and item['status'] == 'reviewed']
    if not records:
        return []
    try:
        if repository_result['status'] == 'error':
            raise ValueError('Cannot resolve upstream branch')
        commit = repository_result['current_commit']
        trees = fetch_tree(repository_result['repository'], commit)
        return [dict(name=item['name'], repository=item['repository'], path=item['path'],
                     reviewed_tree=item['tree_oid'], current_tree=trees.get(item['path']),
                     current_commit=commit,
                     status=('path_missing' if item['path'] not in trees else
                             'unchanged' if trees[item['path']] == item['tree_oid'] else 'skill_changed'))
                for item in records]
    except (OSError, ValueError, KeyError, TypeError) as error:
        return [dict(name=item['name'], repository=item['repository'], status='error',
                     error=type(error).__name__) for item in records]


def check_repository(repository):
    result = {'repository': repository['repository'], 'reviewed_commit': repository['reviewed_commit']}
    try:
        ref = 'refs/heads/' + repository['branch']
        output = subprocess.run(
            ['git', '-c', 'credential.helper=', 'ls-remote', '--exit-code', '--', repository['url'], ref],
            env=dict(os.environ, GIT_TERMINAL_PROMPT='0'),
            capture_output=True, text=True, timeout=30, check=True,
        ).stdout
        matches = [line.split()[0] for line in output.splitlines() if line.split()[1] == ref]
        if len(matches) != 1:
            raise ValueError('Expected one branch tip')
        result.update(current_commit=matches[0], status='unchanged' if matches[0] == repository['reviewed_commit'] else 'repository_changed')
    except (OSError, subprocess.SubprocessError, ValueError, IndexError) as error:
        result.update(status='error', error=type(error).__name__)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--skills', action='store_true', help='Compare each reviewed skill folder via GitHub Trees API')
    args = parser.parse_args()
    state = json.loads((ROOT / 'catalog/upstream-state.json').read_text())
    with ThreadPoolExecutor(max_workers=5) as pool:
        results = list(pool.map(check_repository, state['repositories']))
    skill_results = []
    if args.skills:
        with ThreadPoolExecutor(max_workers=5) as pool:
            for batch in pool.map(lambda result: check_skills(result, state['skills']), results):
                skill_results.extend(batch)
    print(json.dumps({'reviewed_at': state['reviewed_at'], 'repositories': results,
                      'skills': skill_results,
                      'untracked_skills': [item for item in state['skills'] if item['status'] != 'reviewed'],
                      'note': 'repository_changed only means the branch moved; compare the recorded skill tree before applying updates.'},
                     ensure_ascii=False, indent=2))
    return 2 if any(item['status'] == 'error' for item in results + skill_results) else 0


if __name__ == '__main__':
    sys.exit(main())
