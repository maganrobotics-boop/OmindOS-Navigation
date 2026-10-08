"""Publish immutable, hash-verified software preview assets; resume drafts only."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import time

TAG = 'v0.2.0-arm64-preview.2'
ROOT = Path('assets')/TAG
REPO = os.environ['GH_REPO']
NAMES = ['omindos-control-arm64-candidate.tar', 'SHA256SUMS-release.txt',
         'VALIDATION.json', 'RELEASE_SUMMARY.json', 'DM_MC02_VALIDATION.json']


def gh(*args):
    return subprocess.check_output(['gh', *args], text=True)


def api(path):
    return json.loads(gh('api', 'repos/'+REPO+'/'+path))


def main():
    summary = json.loads((ROOT/'RELEASE_SUMMARY.json').read_text())
    expected = {}
    for name in NAMES:
        p = ROOT/name
        with p.open('rb') as stream:
            digest = hashlib.file_digest(stream, 'sha256').hexdigest()
        expected[name] = (p.stat().st_size, 'sha256:'+digest)
    assert expected[NAMES[0]] == (521543680, 'sha256:3c110db4b626082a7a88fa1c5b10c1791d6ae1b52ae307cbd921b2890173e0d4')
    assert summary['size'] == expected[NAMES[0]][0]
    assert 'sha256:'+summary['sha256'] == expected[NAMES[0]][1]
    assert (ROOT/'SHA256SUMS-release.txt').read_text().split() == [summary['sha256'], NAMES[0]]
    releases = [r for r in api('releases?per_page=100') if r['tag_name'] == TAG]
    assert len(releases) <= 1
    if not releases:
        gh('release', 'create', TAG, '--target', os.environ['GITHUB_SHA'],
           '--draft', '--prerelease', '--title', 'OmindOS 四足 ARM64 软件预览 0.2.0-arm64-preview.2',
           '--notes-file', str(ROOT/'RELEASE_NOTES.zh-CN.md'))
        releases = [r for r in api('releases?per_page=100') if r['tag_name'] == TAG]
    assert len(releases) == 1
    release = releases[0]
    assert release['prerelease']
    existing = {a['name']: a for a in release['assets']}
    assert set(existing) <= set(NAMES), 'Unexpected asset; no changes made'
    for name, asset in existing.items():
        assert (asset['size'], asset['digest']) == expected[name], 'Immutable asset mismatch: '+name
    missing = [name for name in NAMES if name not in existing]
    assert release['draft'] or not missing, 'Do not modify an already published release'
    if missing:
        gh('release', 'upload', TAG, *[str(ROOT/name) for name in missing])
    for attempt in range(6):
        release = api('releases/'+str(release['id']))
        assets = {a['name']: a for a in release['assets']}
        if set(assets) == set(NAMES) and all(assets[n].get('digest') for n in NAMES):
            break
        time.sleep(5)
    assert set(assets) == set(NAMES)
    for name in NAMES:
        assert (assets[name]['size'], assets[name]['digest']) == expected[name], name
    if release['draft']:
        gh('api', '--method', 'PATCH', 'repos/'+REPO+'/releases/'+str(release['id']),
           '-F', 'draft=false', '-F', 'prerelease=true', '-f', 'make_latest=false')
    result = api('releases/'+str(release['id']))
    assert not result['draft'] and result['prerelease']
    print(json.dumps({'url':result['html_url'], 'verified_assets':len(NAMES),
                      'prerelease':True}, ensure_ascii=False))


if __name__ == '__main__':
    main()
