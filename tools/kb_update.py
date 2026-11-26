"""Small, opt-out, check-only update notices for the knowledge base."""
from __future__ import annotations

import json
import os
from pathlib import Path
import re
import sys
import tempfile
import time
from urllib.parse import urlsplit
from urllib.request import Request, urlopen

CATEGORIES = {'conclusions': '结论', 'structure': '结构', 'tools': '工具'}
VERSION_FILE = 'kb-version.json'
MAX_BYTES = 8192
CHECK_INTERVAL = 24 * 60 * 60
RETRY_INTERVAL = 60 * 60


def read_object(path: Path) -> dict:
    value = json.loads(path.read_text(encoding='utf-8'))
    if not isinstance(value, dict):
        raise ValueError('Expected a JSON object')
    return value


def write_object(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=path.parent, delete=False, mode='w', encoding='utf-8') as file:
        temp = Path(file.name)
        try:
            json.dump(value, file, ensure_ascii=False, indent=2)
            file.write('\n')
        except BaseException:
            file.close()
            temp.unlink(missing_ok=True)
            raise
    try:
        os.replace(temp, path)
    finally:
        temp.unlink(missing_ok=True)


def policy(root: Path) -> dict:
    local = root / '.kb-local'
    try:
        creator = read_object(local / 'creator.json')
    except FileNotFoundError:
        pass
    except (OSError, ValueError):
        return {'role': 'protected', 'automatic_update_checks': False, 'automatic_updates': False}
    else:
        role = 'creator' if creator.get('role') == 'creator' else 'protected'
        return {'role': role, 'automatic_update_checks': False, 'automatic_updates': False}
    try:
        settings = read_object(local / 'update-settings.json')
    except FileNotFoundError:
        settings = {}
    except (OSError, ValueError):
        settings = {'automatic_update_checks': False}
    enabled = settings.get('automatic_update_checks', True) is True and os.getenv('DD_KB_NO_UPDATE') != '1'
    return {'role': 'reader', 'automatic_update_checks': enabled, 'automatic_updates': False}


def validate_version(data: dict) -> dict:
    hashes = data.get('hashes')
    if (data.get('schema_version') != 1 or type(data.get('revision')) is not int
            or data['revision'] < 1 or not isinstance(hashes, dict) or set(hashes) != set(CATEGORIES)
            or any(not isinstance(h, str) or not re.fullmatch(r'[a-f0-9]{64}', h) for h in hashes.values())):
        raise ValueError('Invalid KB version manifest')
    return data


def validate_url(url: str) -> None:
    location = urlsplit(url)
    if location.scheme != 'https' or not location.hostname or location.username or location.password or location.query or location.fragment:
        raise ValueError('Update URL must be a plain HTTPS URL')


def fetch_version(url: str) -> dict:
    validate_url(url)
    request = Request(url, headers={'Accept': 'application/json', 'User-Agent': 'DarkestDungeonKB/1'})
    with urlopen(request, timeout=2) as response:
        validate_url(response.geturl())
        payload = response.read(MAX_BYTES + 1)
    if len(payload) > MAX_BYTES:
        raise ValueError('Version manifest exceeds maximum size')
    return validate_version(json.loads(payload))


def check(root: Path, *, fetch=fetch_version, now=None) -> dict:
    if not policy(root)['automatic_update_checks']:
        return {'status': 'disabled'}
    try:
        installed = validate_version(read_object(root / VERSION_FILE))
        url = installed.get('update_url')
        if not url:
            return {'status': 'unconfigured'}
        validate_url(url)
    except (OSError, ValueError, TypeError, AttributeError):
        return {'status': 'unconfigured'}
    cache_path = root / '.kb-local/update-cache.json'
    try:
        cache = read_object(cache_path)
    except (OSError, ValueError):
        cache = {}
    now = time.time() if now is None else now
    if cache.get('url') != url:
        cache = {'url': url}
    attempted_at = cache.get('attempted_at')
    interval = RETRY_INTERVAL if cache.get('failed', False) else CHECK_INTERVAL
    if type(attempted_at) in (int, float) and 0 <= now - attempted_at < interval:
        return {'status': 'cached'}
    cache.update(attempted_at=now, failed=True)
    try:
        # Prewrite the attempt so a failed connection also receives a cooldown.
        write_object(cache_path, cache)
        remote = validate_version(fetch(url))
    except (OSError, ValueError, TypeError, AttributeError):
        return {'status': 'unavailable'}
    changed = [key for key in CATEGORIES if remote['hashes'][key] != installed['hashes'][key]]
    notice = remote['revision'] > installed['revision'] and changed and cache.get('notified_revision') != remote['revision']
    cache['failed'] = False
    if notice:
        cache['notified_revision'] = remote['revision']
    try:
        write_object(cache_path, cache)
    except OSError:
        pass
    return {'status': 'update_available', 'changed': changed, 'revision': remote['revision']} if notice else {'status': 'checked'}


def notify(root: Path) -> None:
    result = check(root)
    if result['status'] == 'update_available':
        changed = '、'.join(CATEGORIES[key] for key in result['changed'])
        print(f"知识库有更新（第 {result['revision']} 版，{changed}）。本地文件未改动。", file=sys.stderr)
