"""Publish the pinned receive-only firmware; verify drafts before publication."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import time
import zipfile

TAG = 'dm-mc02-bench-v0.1.0-preview.1'
ROOT = Path('assets') / TAG
PACKAGE = 'omindos-dm-mc02-bench-0.1.0-preview.1.zip'
NAMES = [PACKAGE, 'dm-mc02-observer.elf', 'dm-mc02-observer.hex',
         'dm-mc02-observer.bin', 'SHA256SUMS-release.txt', 'VALIDATION.json',
         'RELEASE_SUMMARY.json', 'RELEASE_NOTES.zh-CN.md']
FIRMWARE_HASHES = {
    'dm-mc02-observer.elf': 'aa268dc34da5e0f889d8dedda5c9598d4545648b8e35ca3aca5b76d66f777e3f',
    'dm-mc02-observer.hex': '66996f78875be484c31662b98a13ad19f747f48f9f555efc740165b518947e83',
    'dm-mc02-observer.bin': '736e19dd709d38b19933b3ae874fa03ee03c184da804e3b197536b71671452ec',
}


def gh(*args):
    return subprocess.check_output(['gh', *args], text=True)


def api(path):
    return json.loads(gh('api', '--header', 'Cache-Control: no-cache',
                         'repos/' + os.environ['GH_REPO'] + '/' + path))


def prepare():
    summary = json.loads((ROOT / 'RELEASE_SUMMARY.json').read_text())
    assert summary['tag'] == TAG and summary['hardware_tested'] is False
    assert summary['source_merge_commit'] and summary['source_head_commit']
    with zipfile.ZipFile(ROOT / PACKAGE) as archive:
        assert archive.testzip() is None
        members = archive.namelist()
        assert not any(Path(n).is_absolute() or '..' in Path(n).parts for n in members)
        assert not any(Path(n).suffix.lower() in ('.py', '.c', '.h', '.s', '.cpp') for n in members)
        validation = json.loads(archive.read('VALIDATION.json'))
        assert validation['complete_firmware_link'] is True
        assert validation['hardware_tested'] is False
        assert validation['unit_tests_passed'] == 47
        assert validation['undefined_symbols'] == []
        assert validation['forbidden_linked_symbols'] == []
        for name, digest in FIRMWARE_HASHES.items():
            data = archive.read(name)
            assert hashlib.sha256(data).hexdigest() == digest, name
            (ROOT / name).write_bytes(data)
        assert archive.read('VALIDATION.json') == (ROOT / 'VALIDATION.json').read_bytes()
    expected = {name: (ROOT / name).stat().st_size for name in NAMES}
    hashes = {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in NAMES}
    for line in (ROOT / 'SHA256SUMS-release.txt').read_text().splitlines():
        digest, name = line.split()
        assert hashes[name] == digest, name
    assert summary['package_sha256'] == hashes[PACKAGE]
    assert summary['package_bytes'] == expected[PACKAGE]
    return {n: (expected[n], 'sha256:' + hashes[n]) for n in NAMES}


def main():
    expected = prepare()
    if os.environ.get('CHECK_ONLY') == '1':
        print(json.dumps({'verified_assets': len(expected), 'hardware_tested': False}))
        return
    releases = [r for r in api('releases?per_page=100') if r['tag_name'] == TAG]
    assert len(releases) <= 1
    if not releases:
        gh('release', 'create', TAG, '--target', os.environ['GITHUB_SHA'],
           '--draft', '--prerelease', '--title', 'OmindOS DM-MC02 禁使能台架固件 0.1.0-preview.1',
           '--notes-file', str(ROOT / 'RELEASE_NOTES.zh-CN.md'))
        for attempt in range(12):
            releases = [r for r in api('releases?per_page=100') if r['tag_name'] == TAG]
            if releases:
                break
            time.sleep(5)
    assert len(releases) == 1
    release = releases[0]
    assert release['prerelease']
    existing = {a['name']: a for a in release['assets']}
    assert set(existing) <= set(NAMES), 'Unexpected release asset'
    for name, asset in existing.items():
        assert (asset['size'], asset.get('digest')) == expected[name], name
    missing = [name for name in NAMES if name not in existing]
    assert release['draft'] or not missing, 'Published releases are immutable'
    if missing:
        gh('release', 'upload', TAG, *[str(ROOT / name) for name in missing])
    for attempt in range(12):
        release = api('releases/' + str(release['id']))
        assets = {a['name']: a for a in release['assets']}
        if set(assets) == set(NAMES) and all(assets[n].get('digest') for n in NAMES):
            break
        time.sleep(5)
    assert set(assets) == set(NAMES)
    for name in NAMES:
        assert (assets[name]['size'], assets[name]['digest']) == expected[name], name
    if release['draft']:
        result = json.loads(gh('api', '--method', 'PATCH',
                               'repos/' + os.environ['GH_REPO'] + '/releases/' + str(release['id']),
                               '-F', 'draft=false', '-F', 'prerelease=true', '-f', 'make_latest=false'))
    else:
        result = release
    assert not result['draft'] and result['prerelease']
    print(json.dumps({'url': result['html_url'], 'verified_assets': len(NAMES),
                      'prerelease': True, 'hardware_tested': False}, ensure_ascii=False))


if __name__ == '__main__':
    main()
