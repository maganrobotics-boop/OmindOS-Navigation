#!/usr/bin/env python3
"""Publish verified Ubuntu assets; never replace an existing public attachment."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import time

TAG='v0.2.0-preview.7'
REPO=os.environ['GH_REPO']
ROOT=Path('assets')/TAG
NAME='omindos-navigation-0.2.0-preview.7-ubuntu-amd64.tar'
NAMES=[NAME,'SHA256SUMS-release.txt','RELEASE_SUMMARY.json','VALIDATION.json','RELEASE_NOTES.zh-CN.md']


def gh(*args):return subprocess.check_output(['gh',*args],text=True)
def api(path):return json.loads(gh('api','repos/'+REPO+'/'+path))


def main():
    summary=json.loads((ROOT/'RELEASE_SUMMARY.json').read_text())
    validation=json.loads((ROOT/'VALIDATION.json').read_text())
    assert summary['release_tag']==TAG and summary['single_installer'] and not summary['backend_source_included']
    assert validation['status']=='PASS' and not validation['hardware_validated'] and not validation['windows_built']
    expected={}
    for name in NAMES:
        p=ROOT/name
        with p.open('rb') as f:digest=hashlib.file_digest(f,'sha256').hexdigest()
        expected[name]=(p.stat().st_size,'sha256:'+digest)
    assert expected[NAME]==(summary['bytes'],'sha256:'+summary['sha256'])
    assert (ROOT/'SHA256SUMS-release.txt').read_text()==summary['sha256']+'  '+NAME+'\n'
    try:
        release=api('releases/tags/'+TAG)
    except subprocess.CalledProcessError:
        gh('release','create',TAG,'--draft','--prerelease','--target',os.environ['GITHUB_SHA'],
           '--title','OmindOS Navigation 0.2.0-preview.7 · Ubuntu 完整安装包',
           '--notes-file',str(ROOT/'RELEASE_NOTES.zh-CN.md'))
        release=api('releases/tags/'+TAG)
    assert release['tag_name']==TAG and release['prerelease']
    assets={x['name']:x for x in release['assets']}
    assert set(assets)<=set(NAMES),'Unexpected existing asset; do not overwrite'
    for name,asset in assets.items():assert (asset['size'],asset.get('digest'))==expected[name],name
    missing=[name for name in NAMES if name not in assets]
    assert release['draft'] or not missing,'Never mutate a published release'
    if missing:gh('release','upload',TAG,*[str(ROOT/name) for name in missing])
    for attempt in range(6):
        release=api('releases/'+str(release['id']))
        assets={x['name']:x for x in release['assets']}
        if set(assets)==set(NAMES) and all(x.get('digest') for x in assets.values()):break
        time.sleep(5)
    assert set(assets)==set(NAMES)
    for name in NAMES:assert (assets[name]['size'],assets[name]['digest'])==expected[name],name
    if release['draft']:
        gh('api','--method','PATCH','repos/'+REPO+'/releases/'+str(release['id']),
           '-F','draft=false','-F','prerelease=true','-f','make_latest=false')
    result=api('releases/'+str(release['id']))
    assert not result['draft']
    print(json.dumps({'published':True,'url':result['html_url'],'verified_assets':len(NAMES),
        'installer_bytes':summary['bytes'],'installer_sha256':summary['sha256']}),flush=True)


if __name__=='__main__':main()
