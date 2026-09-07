import importlib.util
from pathlib import Path
import subprocess
import tempfile
import unittest

SPEC = importlib.util.spec_from_file_location('upstream', Path(__file__).resolve().parents[1] / 'scripts/check_upstream.py')
upstream = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(upstream)


class UpstreamTests(unittest.TestCase):
    def test_real_git_tips_and_missing_branch(self):
        with tempfile.TemporaryDirectory() as temporary:
            repo = Path(temporary) / 'upstream'
            subprocess.run(['git', 'init', '-q', '-b', 'main', str(repo)], check=True)
            def git(*args):
                return subprocess.check_output(['git', '-C', str(repo), '-c', 'user.name=Test', '-c', 'user.email=test@example.invalid', *args], text=True).strip()
            git('commit', '-q', '--allow-empty', '-m', 'baseline')
            baseline = git('rev-parse', 'HEAD')
            record = {'repository': 'fixture', 'url': str(repo), 'branch': 'main', 'reviewed_commit': baseline}
            self.assertEqual(upstream.check_repository(record)['status'], 'unchanged')
            git('commit', '-q', '--allow-empty', '-m', 'changed')
            result = upstream.check_repository(record)
            self.assertEqual(result['status'], 'repository_changed')
            self.assertEqual(result['current_commit'], git('rev-parse', 'HEAD'))
            record['branch'] = 'missing'
            self.assertEqual(upstream.check_repository(record)['status'], 'error')
            self.assertEqual(git('status', '--porcelain'), '')


if __name__ == '__main__':
    unittest.main()
