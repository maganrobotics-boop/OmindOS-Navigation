"""Publish immutable, hash-verified software preview assets; resume drafts only."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import time

TAG = 'v0.2.0-preview.6'
ROOT = Path('assets')/TAG
REPO = os.environ['GH_REPO']
NAMES = ["omindos-control-preview-0.2.0-preview.5-size-candidate.1-linux-amd64.tar","omindos-quadruped-workbench-0.2.0-size-candidate.1-linux-x64.tar.gz","omindos-quadruped-workbench-0.2.0-size-candidate.1-windows-x64.zip","SHA256SUMS-release.txt","VALIDATION.json","RELEASE_SUMMARY.json","RELEASE_NOTES.zh-CN.md"]


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
    assert summary['release_tag'] == TAG
    assert not summary['backend_source_included']
    assert json.loads((ROOT/'VALIDATION.json').read_text())['status'] == 'PASS'
    for item in summary['files']:
        assert expected[item['filename']] == (item['bytes'], 'sha256:'+item['sha256'])
    assert (ROOT/'SHA256SUMS-release.txt').read_text() == ''.join(
        item['sha256']+'  '+item['filename']+'\n' for item in summary['files'])
    # Use the exact draft returned by the first publication attempt. The
    # collection endpoint can lag immediately after creating a release.
    release = api('releases/407308147')
    assert release['tag_name'] == TAG
    assert release['target_commitish'] == 'd4969eb8ba38601ac2fdb01142462968a5952b61'
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
