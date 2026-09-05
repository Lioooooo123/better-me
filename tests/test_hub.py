import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

SPEC = importlib.util.spec_from_file_location('hub', Path(__file__).resolve().parents[1] / 'scripts/hub.py')
hub = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(hub)


class InstallationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.home = Path(self.temp.name) / 'home'
        self.root = Path(self.temp.name) / 'repo'
        (self.root / 'catalog').mkdir(parents=True)
        (self.root / 'skills/keep').mkdir(parents=True)
        baseline = []
        for name, kept in [('keep', True), ('retire', False)]:
            path = self.home / '.agents/skills' / name
            path.mkdir(parents=True)
            (path / 'SKILL.md').write_text('original ' + name)
            baseline.append({'name': name, 'kept': kept, 'original_path': f'.agents/skills/{name}', 'tree_sha256': hub.fingerprint(path)})
        hub.save(self.root / 'catalog/skills.json', {'skills': [{'name': 'keep'}]})
        hub.save(self.root / 'catalog/migration-baseline.json', {'skills': baseline})
        self.lock = self.home / '.agents/.skill-lock.json'
        hub.save(self.lock, {'version': 3, 'skills': {'keep': {'source': 'old'}, 'other': {'source': 'untouched'}}})

    def test_install_preview_idempotency_and_restore(self):
        self.assertEqual(hub.install(self.home, root=self.root)['status'], 'dry-run')
        self.assertFalse((self.home / '.agents/skills/keep').is_symlink())
        hub.install(self.home, True, self.root)
        self.assertEqual(hub.install(self.home, True, self.root)['status'], 'already-installed')
        self.assertFalse((self.home / '.agents/skills/retire').exists())
        lock = json.loads(self.lock.read_text())
        lock['skills']['other']['updated'] = True
        hub.save(self.lock, lock)
        hub.rollback(self.home, True)
        self.assertEqual((self.home / '.agents/skills/keep/SKILL.md').read_text(), 'original keep')
        self.assertTrue((self.home / '.agents/skills/retire').is_dir())
        self.assertTrue(json.loads(self.lock.read_text())['skills']['other']['updated'])
        self.assertEqual(json.loads(self.lock.read_text())['skills']['keep'], {'source': 'old'})

    def test_changed_reference_blocks_before_mutation(self):
        (self.home / '.agents/skills/keep/new.md').write_text('concurrent edit')
        with self.assertRaisesRegex(ValueError, 'changed skill'):
            hub.install(self.home, True, self.root)
        self.assertTrue((self.home / '.agents/skills/retire').exists())

    def test_symlink_parent_rejected(self):
        outside = Path(self.temp.name) / 'outside'
        outside.mkdir()
        (self.home / '.codex').symlink_to(outside, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, 'Symlink parent'):
            hub.install(self.home, True, self.root)
        self.assertEqual(list(outside.iterdir()), [])

    def test_rollback_conflict_preserves_everything(self):
        hub.install(self.home, True, self.root)
        installed = self.home / '.agents/skills/keep'
        installed.unlink()
        installed.mkdir()
        (installed / 'custom').write_text('new')
        with self.assertRaisesRegex(ValueError, 'Rollback conflict'):
            hub.rollback(self.home, True)
        self.assertEqual((installed / 'custom').read_text(), 'new')

    def test_mid_install_failure_restores_originals(self):
        with patch.object(Path, 'symlink_to', side_effect=OSError('injected failure')):
            with self.assertRaisesRegex(OSError, 'injected failure'):
                hub.install(self.home, True, self.root)
        self.assertEqual((self.home / '.agents/skills/keep/SKILL.md').read_text(), 'original keep')
        self.assertEqual(json.loads(self.lock.read_text())['skills']['keep'], {'source': 'old'})

    def test_lock_conflict_blocks_rollback(self):
        hub.install(self.home, True, self.root)
        lock = json.loads(self.lock.read_text())
        lock['skills']['keep'] = {'source': 'someone-else'}
        hub.save(self.lock, lock)
        with self.assertRaisesRegex(ValueError, 'Managed lock entries changed'):
            hub.rollback(self.home, True)
        self.assertTrue((self.home / '.agents/skills/keep').is_symlink())

    def test_backup_mutation_blocks_restore(self):
        result = hub.install(self.home, True, self.root)
        saved = Path(result['backup']) / '.agents/skills/keep/SKILL.md'
        saved.write_text('tampered')
        with self.assertRaisesRegex(ValueError, 'Backup changed'):
            hub.rollback(self.home, True)
        self.assertTrue((self.home / '.agents/skills/keep').is_symlink())

    def test_state_directory_symlink_rejected(self):
        outside = Path(self.temp.name) / 'outside'
        outside.mkdir()
        (self.home / '.codex').mkdir()
        (self.home / '.codex/skill-hub').symlink_to(outside, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, 'Symlink state'):
            hub.install(self.home, True, self.root)
        self.assertEqual(list(outside.iterdir()), [])


if __name__ == '__main__':
    unittest.main()
