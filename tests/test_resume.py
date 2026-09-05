"""Regression coverage for resumable QA and non-destructive workspace creation."""
import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / 'skills/html-resume-builder/scripts'
spec = importlib.util.spec_from_file_location('resume_qa', SCRIPTS / 'export_and_qa.py')
qa = importlib.util.module_from_spec(spec)
spec.loader.exec_module(qa)


class ResumeTests(unittest.TestCase):
    def test_missing_poppler_is_incomplete_in_both_modes(self):
        with tempfile.TemporaryDirectory() as temporary:
            html = Path(temporary) / 'resume.html'
            html.write_text('<p>Public commit and patch contributions</p>')
            checks = []
            with patch.object(qa.shutil, 'which', return_value=None):
                qa.check_pdfinfo(Path('resume.pdf'), checks)
                qa.check_fonts(Path('resume.pdf'), checks, 'ExampleFont')
                qa.check_text(Path('resume.pdf'), html, checks, qa.DEFAULT_FORBIDDEN_TERMS)
                qa.render_screenshot(Path('resume.pdf'), Path(temporary) / 'page', checks)
                qa.check_bottom_whitespace(Path('resume.pdf'), checks, max_ratio=.15, main_content_right_ratio=.85)
            self.assertEqual(sum(check['skipped'] for check in checks), 5)
            for strict, expected_code in ((False, 0), (True, 2)):
                result, code = qa.summarize_checks(checks, strict)
                self.assertEqual(code, expected_code)
                self.assertEqual(result['status'], 'incomplete')
                self.assertFalse(result['ok'])

    def test_diagnostic_words_do_not_decide_skip_status(self):
        checks = []
        qa.add_check(checks, 'page size', False, 'Page size not found.')
        result, code = qa.summarize_checks(checks, True)
        self.assertEqual((result['status'], code), ('failed', 1))
        checks = []
        qa.add_check(checks, 'dependency', False, 'Unavailable executable', skipped=True)
        result, code = qa.summarize_checks(checks, True)
        self.assertEqual((result['status'], code), ('incomplete', 2))

    def test_public_engineering_terms_are_allowed_by_default(self):
        self.assertEqual(qa.find_forbidden_terms('Public commit and patch contributions', qa.DEFAULT_FORBIDDEN_TERMS), [])
        self.assertEqual(qa.find_forbidden_terms('PrivateProject', ['PrivateProject']), ['PrivateProject'])

    def test_workspace_creation_preserves_existing_destination(self):
        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary) / 'resume'
            command = [sys.executable, str(SCRIPTS / 'create_workspace.py'), '--output', str(destination)]
            first = subprocess.run(command, text=True, capture_output=True)
            self.assertEqual(first.returncode, 0, first.stderr)
            marker = destination / 'keep.txt'
            marker.write_text('user content')
            second = subprocess.run(command, text=True, capture_output=True)
            self.assertNotEqual(second.returncode, 0)
            self.assertEqual(marker.read_text(), 'user content')
            self.assertIn('existing content is preserved', second.stderr)

    def test_template_name_cannot_escape_template_root(self):
        with tempfile.TemporaryDirectory() as temporary:
            result = subprocess.run([sys.executable, str(SCRIPTS / 'create_workspace.py'), '--template', '../basic-a4', '--output', str(Path(temporary) / 'new')], text=True, capture_output=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('directly under', result.stderr)


if __name__ == '__main__':
    unittest.main()
