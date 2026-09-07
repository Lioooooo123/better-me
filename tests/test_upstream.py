import importlib.util
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

SPEC = importlib.util.spec_from_file_location('upstream', Path(__file__).resolve().parents[1] / 'scripts/check_upstream.py')
upstream = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(upstream)


class UpstreamTests(unittest.TestCase):
    def test_skill_changes_ignore_unrelated_repository_changes(self):
        records = [dict(name=name, repository='owner/repo', path='skills/' + name,
                        tree_oid='old', status='reviewed') for name in ['same', 'changed', 'removed']]
        result = dict(repository='owner/repo', current_commit='tip', status='repository_changed')
        with patch.object(upstream, 'fetch_tree', return_value={'skills/same': 'old', 'skills/changed': 'new'}) as fetch:
            checked = upstream.check_skills(result, records)
        fetch.assert_called_once_with('owner/repo', 'tip')
        self.assertEqual([item['status'] for item in checked], ['unchanged', 'skill_changed', 'path_missing'])
        self.assertEqual(records[1]['tree_oid'], 'old')

    def test_api_failure_is_not_unchanged(self):
        records = [dict(name='test', repository='owner/repo', path='skills/test', tree_oid='old', status='reviewed')]
        result = dict(repository='owner/repo', current_commit='tip', status='unchanged')
        with patch.object(upstream, 'fetch_tree', side_effect=OSError('offline')):
            self.assertEqual(upstream.check_skills(result, records)[0]['status'], 'error')
        with patch.object(upstream, 'fetch_tree') as fetch:
            result['status'] = 'error'
            self.assertEqual(upstream.check_skills(result, records)[0]['status'], 'error')
            fetch.assert_not_called()

    def test_truncated_tree_cannot_report_missing_skills(self):
        from io import BytesIO
        with patch.object(upstream, 'urlopen', side_effect=[BytesIO(b'{"tree": {"sha": "root-tree"}}'), BytesIO(b'{"truncated": true, "tree": []}')]):
            with self.assertRaises(ValueError):
                upstream.fetch_tree('owner/repo', 'tip')

    def test_repository_root_is_a_skill_folder(self):
        from io import BytesIO
        payload = b'{"sha": "root-tree", "truncated": false, "tree": [{"path": "references", "type": "tree", "sha": "child-tree"}]}'
        with patch.object(upstream, 'urlopen', side_effect=[BytesIO(b'{"tree": {"sha": "root-tree"}}'), BytesIO(payload)]):
            self.assertEqual(upstream.fetch_tree('owner/repo', 'tip'), {'.': 'root-tree', 'references': 'child-tree'})

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
