import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

SPEC = importlib.util.spec_from_file_location('validator', Path(__file__).resolve().parents[1] / 'scripts/validate.py')
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)


class ModuleValidationTests(unittest.TestCase):
    def test_module_is_not_an_independent_skill_manifest(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / 'catalog').mkdir()
            module = root / 'skills/lark/modules/lark-doc'
            module.mkdir(parents=True)
            (root / 'skills/lark/SKILL.md').write_text('---\nname: lark\ndescription: 飞书任务\n---\n\n# 飞书\n')
            (module / 'MODULE.md').write_text('---\nname: lark-doc\ndescription: 飞书文档\n---\n\n# 文档\n')
            (root / 'catalog/skills.json').write_text(json.dumps({'skills': [
                {'name': 'lark', 'requires': [], 'companions': [], 'explicit_only': False}]}))
            (root / 'catalog/modules.json').write_text(json.dumps({'modules': [
                {'name': 'lark-doc', 'parent': 'lark', 'path': 'skills/lark/modules/lark-doc',
                 'requires': [], 'companions': [], 'explicit_only': False}]}))
            (root / 'catalog/upstream-state.json').write_text(json.dumps({'repositories': [], 'skills': [
                {'name': 'lark', 'status': 'local'}, {'name': 'lark-doc', 'status': 'local'}]}))

            self.assertEqual(validator.validate(root), [])
            (module / 'SKILL.md').write_text((module / 'MODULE.md').read_text())
            self.assertIn('Nested modules must use MODULE.md, not SKILL.md', validator.validate(root))


if __name__ == '__main__':
    unittest.main()
