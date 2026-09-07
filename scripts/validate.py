#!/usr/bin/env python3
"""Validate maintained skill metadata, local references and required dependency graph."""
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote
import yaml

ROOT = Path(__file__).resolve().parents[1]


def validate(root=ROOT):
    errors = []
    items = json.loads((root / 'catalog/skills.json').read_text())['skills']
    names = {item['name'] for item in items}
    actual = {p.parent.name for p in (root / 'skills').glob('*/SKILL.md')}
    if len(names) != len(items) or names != actual:
        errors.append('Catalog and skill directories differ or contain duplicates')
    upstream = json.loads((root / 'catalog/upstream-state.json').read_text())
    repositories = {item['repository']: item for item in upstream['repositories']}
    tracked = upstream['skills']
    if {item['name'] for item in tracked} != names or len(tracked) != len(names):
        errors.append('Upstream state and skill catalog differ')
    for repository in repositories.values():
        if not re.fullmatch(r'[0-9a-f]{40}', repository['reviewed_commit']):
            errors.append(f'Invalid upstream revision: {repository["repository"]}')
    for item in tracked:
        if item['status'] == 'reviewed':
            if item['repository'] not in repositories or '..' in Path(item['path']).parts or Path(item['path']).is_absolute():
                errors.append(f'Invalid upstream mapping: {item["name"]}')
            if not re.fullmatch(r'[0-9a-f]{40}', item['tree_oid']) or not re.fullmatch(r'[0-9a-f]{64}', item['entry_sha256']):
                errors.append(f'Invalid upstream fingerprint: {item["name"]}')
    for item in items:
        name = item['name']
        base = root / 'skills' / name
        entry = base / 'SKILL.md'
        text = entry.read_text()
        try:
            if not text.startswith('---\n'):
                raise ValueError('Missing YAML frontmatter')
            metadata = yaml.safe_load(text.split('---', 2)[1])
            if metadata['name'] != name or not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', name) or len(name) > 64:
                raise ValueError('Invalid skill name')
            if not isinstance(metadata['description'], str) or not 1 <= len(metadata['description']) <= 1024:
                raise ValueError('Invalid description')
            if '<' in metadata['description'] or '>' in metadata['description']:
                raise ValueError('Description contains angle brackets')
            if len(text.splitlines()) > 500:
                raise ValueError('Entry exceeds 500 lines')
            config = base / 'agents/openai.yaml'
            implicit = yaml.safe_load(config.read_text()).get('policy', {}).get('allow_implicit_invocation', True) if config.exists() else True
            if implicit == item['explicit_only']:
                raise ValueError('Explicit invocation policy differs from catalog')
        except (ValueError, KeyError, TypeError, yaml.YAMLError) as error:
            errors.append(f'{entry.relative_to(root)}: {error}')
        for dependency in item['requires'] + item['companions']:
            if dependency not in names:
                errors.append(f'{name}: unknown dependency {dependency}')
        for doc in base.rglob('*.md'):
            # Fenced examples are not repository references.
            content = re.sub(r'^```[^\n]*\n.*?^```[ \t]*$', '', doc.read_text(), flags=re.S | re.M)
            for link in re.findall(r'\[[^\]]*\]\(([^\s)]+)(?:\s+"[^"]*")?\)', re.sub(r'(`+).*?\1', '', content)):
                link = unquote(link.strip('<>').split('#')[0])
                if not link or ':' in link or link.startswith('/') or any(c in link for c in '{}*'):
                    continue
                if not (doc.parent / link).exists():
                    errors.append(f'{doc.relative_to(root)}: missing {link}')
            if doc == entry:
                for path in re.findall(r'`((?:scripts|references|assets)/[^`\s]+)`', content):
                    if not (base / path).exists():
                        errors.append(f'{name}: missing resource {path}')
    graph = {item['name']: item['requires'] for item in items}
    def visit(node, stack):
        if node in stack:
            errors.append('Required dependency cycle: ' + ' -> '.join(stack + [node]))
            return
        for child in graph.get(node, []):
            visit(child, stack + [node])
    for name in names:
        visit(name, [])
    return errors


if __name__ == '__main__':
    errors = validate()
    print('\n'.join(errors) if errors else 'Validated catalog, metadata, references and required dependency graph.')
    sys.exit(bool(errors))
