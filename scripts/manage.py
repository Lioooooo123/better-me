#!/usr/bin/env python3
"""Local skill installation, scoped migration and reversible journal. Stdlib only."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import time

ROOT = Path(__file__).resolve().parents[1]
# Keep the legacy state directory so existing migration backups remain recoverable.


def exists(path):
    return path.exists() or path.is_symlink()


def fingerprint(path):
    if path.is_symlink():
        return hashlib.sha256(('link:' + os.readlink(path)).encode()).hexdigest()
    digest = hashlib.sha256()
    if not path.is_dir():
        return hashlib.sha256(path.read_bytes()).hexdigest()
    for item in sorted(path.rglob('*')):
        if item.name in {'.DS_Store', '__pycache__'} or '__pycache__' in item.parts:
            continue
        digest.update(str(item.relative_to(path)).encode() + b'\0')
        if item.is_symlink():
            digest.update(b'L' + os.readlink(item).encode())
        elif item.is_file():
            digest.update(b'F' + item.read_bytes())
        else:
            digest.update(b'D')
    return digest.hexdigest()


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix('.tmp')
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')
    temporary.replace(path)


def safe_path(home, relative):
    rel = Path(relative)
    if rel.is_absolute() or '..' in rel.parts:
        raise ValueError(f'Unsafe path: {relative}')
    path = home / rel
    for parent in path.parents:
        if parent == home:
            break
        if parent.is_symlink():
            raise ValueError(f'Symlink parent: {parent}')
    return path


def plan(home, root=ROOT):
    catalog = json.loads((root / 'catalog/skills.json').read_text())['skills']
    baseline = json.loads((root / 'catalog/migration-baseline.json').read_text())['skills']
    originals = {item['original_path']: item for item in baseline}
    desired = {f'.agents/skills/{item["name"]}': str(root / 'skills' / item['name']) for item in catalog}
    actions = []
    for relative in sorted(set(originals) | set(desired)):
        path = safe_path(home, relative)
        target = desired.get(relative)
        if target and path.is_symlink() and os.readlink(path) == target:
            continue
        present = exists(path)
        if present:
            expected = originals.get(relative, {}).get('tree_sha256')
            if not expected or fingerprint(path) != expected:
                raise ValueError(f'Unrecognized or changed skill; untouched: {path}')
        if present or target:
            actions.append({'path': relative, 'target': target, 'had_original': present,
                            'before_hash': fingerprint(path) if present else None})
    return actions, catalog, baseline


def extension_plan(home, journal, root=ROOT):
    """Adopt new catalog skills without replacing an existing managed link."""
    catalog = json.loads((root / 'catalog/skills.json').read_text())['skills']
    installed = set(journal['new_entries'])
    names = {item['name'] for item in catalog}
    if not installed <= names:
        raise ValueError('Catalog removed an installed skill; rollback or migrate it explicitly')
    actions = []
    for item in catalog:
        name = item['name']
        path = safe_path(home, f'.agents/skills/{name}')
        target = str(root / 'skills' / name)
        if name in installed:
            if not path.is_symlink() or os.readlink(path) != target:
                raise ValueError(f'Managed skill changed; untouched: {path}')
            continue
        present = exists(path)
        if present and (not path.is_dir() or path.is_symlink() or fingerprint(path) != fingerprint(root / 'skills' / name)):
            raise ValueError(f'Unrecognized or changed skill; untouched: {path}')
        actions.append({'path': f'.agents/skills/{name}', 'target': target,
                        'had_original': present, 'before_hash': fingerprint(path) if present else None})
    return actions, catalog


def extend_install(home, state, journal, actions, catalog, root):
    lock = safe_path(home, '.agents/.skill-lock.json')
    if lock.is_symlink():
        raise ValueError('Refusing symlink lock file')
    original_lock = lock.read_text() if lock.exists() else None
    lock_data = json.loads(original_lock) if original_lock else {'version': 3, 'skills': {}}
    for name, entry in journal['new_entries'].items():
        if lock_data['skills'].get(name) != entry:
            raise ValueError(f'Managed lock entry changed; untouched: {name}')
    backup = Path(journal['backup'])
    if not backup.is_relative_to(safe_path(home, '.codex/skill-hub/backups')):
        raise ValueError('Invalid backup location')
    for action in actions:
        if exists(backup / action['path']):
            raise ValueError(f'Backup already exists: {action["path"]}')
    original_state = state.read_text()
    moved = []
    try:
        for action in actions:
            path = safe_path(home, action['path'])
            if exists(path) != action['had_original'] or (action['had_original'] and fingerprint(path) != action['before_hash']):
                raise ValueError(f'Concurrent change: {path}')
            dest = backup / action['path']
            if action['had_original']:
                dest.parent.mkdir(parents=True, exist_ok=True)
                path.rename(dest)
            moved.append(action)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.symlink_to(action['target'], target_is_directory=True)
        if (lock.read_text() if lock.exists() else None) != original_lock or state.read_text() != original_state:
            raise ValueError('Concurrent lock or journal change')
        additions = {item['name']: {'source': 'Lioooooo123/better-me', 'sourceType': 'local',
                     'sourceUrl': str(root), 'skillPath': f'skills/{item["name"]}/SKILL.md'}
                     for item in catalog if item['name'] not in journal['new_entries']}
        for name in additions:
            if name in lock_data['skills']:
                journal['old_entries'][name] = lock_data['skills'][name]
        journal['actions'].extend(actions)
        journal['new_entries'].update(additions)
        journal['managed_names'] = sorted(set(journal['managed_names']) | set(additions))
        lock_data['skills'].update(additions)
        save(lock, lock_data)
        save(state, journal)
    except Exception:
        if original_lock is None:
            lock.unlink(missing_ok=True)
        else:
            lock.write_text(original_lock)
        state.write_text(original_state)
        for action in reversed(moved):
            path = safe_path(home, action['path'])
            if path.is_symlink() and os.readlink(path) == action['target']:
                path.unlink()
            saved = backup / action['path']
            if exists(saved):
                saved.rename(path)
        raise
    return {'status': 'installed', 'count': len(catalog), 'added': len(actions), 'backup': str(backup)}


def install(home, apply=False, root=ROOT):
    home = home.resolve()
    state_root = safe_path(home, '.codex/skill-hub')
    if state_root.is_symlink():
        raise ValueError('Symlink state directory')
    state = state_root / 'active.json'
    if state.exists():
        journal = json.loads(state.read_text())
        if journal['status'] != 'installed':
            raise ValueError('Existing journal needs recovery before a new migration')
        actions, catalog = extension_plan(home, journal, root)
        if not actions:
            return {'status': 'already-installed', 'journal': str(state)}
        if not apply:
            return {'status': 'dry-run', 'actions': actions}
        return extend_install(home, state, journal, actions, catalog, root)
    actions, catalog, baseline = plan(home, root)
    if not apply:
        return {'status': 'dry-run', 'actions': actions}
    if not actions:
        return {'status': 'unchanged'}
    lock = safe_path(home, '.agents/.skill-lock.json')
    if lock.is_symlink():
        raise ValueError('Refusing symlink lock file')
    old_lock = lock.read_text() if lock.exists() else None
    lock_data = json.loads(old_lock) if old_lock else {'version': 3, 'skills': {}}
    names = {item['name'] for item in baseline} | {item['name'] for item in catalog}
    old_entries = {name: lock_data['skills'][name] for name in names if name in lock_data['skills']}
    new_entries = {item['name']: {'source': 'Lioooooo123/better-me', 'sourceType': 'local',
                   'sourceUrl': str(root), 'skillPath': f'skills/{item["name"]}/SKILL.md'} for item in catalog}
    backup = safe_path(home, f'.codex/skill-hub/backups/{time.time_ns()}')
    backup.mkdir(parents=True)
    journal = {'status': 'installing', 'actions': actions, 'backup': str(backup),
               'old_entries': old_entries, 'new_entries': new_entries, 'managed_names': sorted(names),
               'lock_existed': old_lock is not None, 'lock_written': False}
    if old_lock is not None:
        (backup / 'skill-lock.json').write_text(old_lock)
    save(state, journal)
    try:
        for action in actions:
            path = safe_path(home, action['path'])
            if exists(path) != action['had_original'] or (action['had_original'] and fingerprint(path) != action['before_hash']):
                raise ValueError(f'Concurrent change: {path}')
            dest = backup / action['path']
            if action['had_original']:
                dest.parent.mkdir(parents=True, exist_ok=True)
                path.rename(dest)
            if action['target']:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.symlink_to(action['target'], target_is_directory=True)
        if (lock.read_text() if lock.exists() else None) != old_lock:
            raise ValueError('Concurrent lock change')
        for name in names:
            lock_data['skills'].pop(name, None)
        lock_data['skills'].update(new_entries)
        journal['lock_written'] = True
        save(state, journal)
        save(lock, lock_data)
        journal['status'] = 'installed'
        save(state, journal)
    except Exception:
        rollback(home, apply=True, recovering=True)
        raise
    return {'status': 'installed', 'count': len(catalog), 'backup': str(backup)}


def rollback(home, apply=False, recovering=False):
    home = home.resolve()
    state = safe_path(home, '.codex/skill-hub/active.json')
    journal = json.loads(state.read_text())
    backup = Path(journal['backup'])
    # Preflight everything before changing anything. Also handles an interrupted install.
    for action in journal['actions']:
        path = safe_path(home, action['path'])
        saved = backup / action['path']
        if exists(saved) and fingerprint(saved) != action['before_hash']:
            raise ValueError(f'Backup changed; untouched: {saved}')
        if exists(path):
            is_link = action['target'] and path.is_symlink() and os.readlink(path) == action['target']
            untouched = action['had_original'] and not exists(saved) and fingerprint(path) == action['before_hash']
            if not is_link and not untouched:
                raise ValueError(f'Rollback conflict; untouched: {path}')
    lock = safe_path(home, '.agents/.skill-lock.json')
    if lock.is_symlink():
        raise ValueError('Refusing symlink lock file')
    current = json.loads(lock.read_text()) if lock.exists() else {'version': 3, 'skills': {}}
    if journal['lock_written']:
        entries = {name: current['skills'][name] for name in journal['managed_names'] if name in current['skills']}
        if entries not in (journal['new_entries'], journal['old_entries']):
            raise ValueError('Managed lock entries changed; rollback stopped')
    if not apply:
        return {'status': 'dry-run', 'restore': str(backup)}
    for action in reversed(journal['actions']):
        path = safe_path(home, action['path'])
        saved = backup / action['path']
        if path.is_symlink() and action['target'] and os.readlink(path) == action['target']:
            path.unlink()
        if exists(saved):
            path.parent.mkdir(parents=True, exist_ok=True)
            saved.rename(path)
    if journal['lock_written']:
        for name in journal['managed_names']:
            current['skills'].pop(name, None)
        current['skills'].update(journal['old_entries'])
        if not journal['lock_existed'] and not current['skills']:
            lock.unlink(missing_ok=True)
        else:
            save(lock, current)
    journal['status'] = 'rolled-back'
    save(backup / 'journal.json', journal)
    state.unlink()
    return {'status': 'rolled-back', 'backup': str(backup)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['install', 'status', 'rollback'])
    parser.add_argument('--home', type=Path, default=Path.home())
    parser.add_argument('--apply', action='store_true', help='Apply install or rollback; default is preview')
    args = parser.parse_args()
    try:
        if args.command == 'rollback':
            result = rollback(args.home, args.apply)
        elif args.command == 'install':
            result = install(args.home, args.apply)
        else:
            home = args.home.resolve()
            state = safe_path(home, '.codex/skill-hub/active.json')
            if state.exists():
                actions, catalog = extension_plan(home, json.loads(state.read_text()))
            else:
                actions, catalog, _ = plan(home)
            result = {'status': 'installed' if not actions else 'pending', 'skill_count': len(catalog), 'pending_actions': len(actions)}
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except (ValueError, OSError, KeyError) as error:
        parser.exit(1, f'{error}\n')


if __name__ == '__main__':
    main()
