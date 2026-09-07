#!/usr/bin/env python3
"""Read upstream branch tips. Does not install, merge or modify any skill."""
from concurrent.futures import ThreadPoolExecutor
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


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
    state = json.loads((ROOT / 'catalog/upstream-state.json').read_text())
    with ThreadPoolExecutor(max_workers=5) as pool:
        results = list(pool.map(check_repository, state['repositories']))
    print(json.dumps({'reviewed_at': state['reviewed_at'], 'repositories': results,
                      'untracked_skills': [item for item in state['skills'] if item['status'] != 'reviewed'],
                      'note': 'repository_changed only means the branch moved; compare the recorded skill tree before applying updates.'},
                     ensure_ascii=False, indent=2))
    return 2 if any(item['status'] == 'error' for item in results) else 0


if __name__ == '__main__':
    sys.exit(main())
