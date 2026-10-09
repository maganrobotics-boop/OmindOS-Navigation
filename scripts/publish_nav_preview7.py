"""Publish only the already validated Ubuntu package; never replace release bytes."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import time
import zipfile

TAG = 'v0.2.0-preview.7'
ROOT = Path('assets') / TAG
REPO = os.environ['GH_REPO']
NAMES = ['omindos-navigation-0.2.0-preview.7-ubuntu-amd64.tar', 'VALIDATION.json',
         'DYNAMICS_VALIDATION.json', 'BROWSER_VALIDATION.json', 'RELEASE_SUMMARY.json',
         'SHA256SUMS-release.txt', 'workbench.png', 'RELEASE_NOTES.zh-CN.md']


def sha(path):
    with Path(path).open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()


def gh(*args):
    return subprocess.check_output(['gh', *args], text=True)


def api(path):
    return json.loads(gh('api', 'repos/' + REPO + '/' + path))


def main():
    transfer = json.loads(Path('transfer/nav-preview7.json').read_text())
    ROOT.mkdir(parents=True, exist_ok=True)
    if transfer.get('download_url'):
        download = Path('validated-installer.zip')
        subprocess.run(['curl','--fail','--location','--silent','--show-error','--retry','2',
                        '--output',str(download),transfer['download_url']],check=True)
        assert sha(download) == transfer['archive_sha256'], 'Transfer archive hash mismatch'
        with zipfile.ZipFile(download) as archive:
            for name in NAMES[:-1]:
                matches = [i for i in archive.infolist() if i.filename == name]
                assert len(matches) == 1, ('Missing or duplicate artifact',name)
                with archive.open(matches[0]) as src, (ROOT / name).open('wb') as dst:
                    shutil.copyfileobj(src,dst)
    else:
        gh('release','download',TAG,'--dir',str(ROOT))
    summary = json.loads((ROOT / 'RELEASE_SUMMARY.json').read_text())
    validation = json.loads((ROOT / 'VALIDATION.json').read_text())
    browser = json.loads((ROOT / 'BROWSER_VALIDATION.json').read_text())
    dynamics = json.loads((ROOT / 'DYNAMICS_VALIDATION.json').read_text())
    assert summary['status'] == validation['status'] == dynamics['status'] == 'PASS'
    assert summary['sha256'] == transfer['installer_sha256'] == sha(ROOT / NAMES[0])
    assert summary['bytes'] == (ROOT / NAMES[0]).stat().st_size
    assert summary['source_commit'] == transfer['validated_commit']
    assert browser['stage'] == 'installed-full-package' and browser['installer_updated']
    assert browser['mesh_loaded'] == 13 and browser['mesh_failed'] == 0
    assert not browser['page_errors'] and not browser['mesh_request_errors']
    assert len(dynamics['scenarios']) == 4
    assert not validation['backend_source_included'] and not validation['hardware_validated']
    shutil.copy2('release-notes/nav-preview7.zh-CN.md',ROOT / NAMES[-1])
    expected = {name: ((ROOT/name).stat().st_size,'sha256:'+sha(ROOT/name)) for name in NAMES}
    releases = api('releases?per_page=100')
    matches = [r for r in releases if r['tag_name'] == TAG]
    if not matches:
        gh('release','create',TAG,'--draft','--prerelease','--target',os.environ['GITHUB_SHA'],
           '--title','OmindOS Navigation Ubuntu 完整包 · 0.2.0-preview.7',
           '--notes-file',str(ROOT/NAMES[-1]))
        release = api('releases/tags/'+TAG)
    else:
        assert len(matches) == 1
        release = matches[0]
    existing = {a['name']:a for a in release['assets']}
    assert set(existing) <= set(NAMES), 'Unexpected release asset'
    for name,a in existing.items():
        assert (a['size'],a['digest']) == expected[name], ('Immutable asset mismatch',name)
    missing = [name for name in NAMES if name not in existing]
    assert release['draft'] or not missing, 'Never modify published assets'
    if missing:
        gh('release','upload',TAG,*[str(ROOT/name) for name in missing])
    for _ in range(12):
        release = api('releases/'+str(release['id']))
        assets = {a['name']:a for a in release['assets']}
        if set(assets) == set(NAMES) and all(assets[n].get('digest') for n in NAMES):
            break
        time.sleep(5)
    assert set(assets) == set(NAMES)
    for name in NAMES:
        assert (assets[name]['size'],assets[name]['digest']) == expected[name], name
    if release['draft']:
        gh('api','--method','PATCH','repos/'+REPO+'/releases/'+str(release['id']),
           '-F','draft=false','-F','prerelease=true','-f','make_latest=false')
    release = api('releases/'+str(release['id']))
    assert not release['draft'] and release['prerelease']
    print(json.dumps({'url':release['html_url'],'verified_assets':len(NAMES),
                      'installer_bytes':summary['bytes'],'installer_sha256':summary['sha256']}))


if __name__ == '__main__':
    main()
