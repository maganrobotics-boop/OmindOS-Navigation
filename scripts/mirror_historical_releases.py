"""Mirror pinned public releases; verify immutable assets before publication."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import time
import urllib.error
import urllib.request


def run(*args):
    return subprocess.check_output(args, text=True).strip()


def api(path, payload=None, method=None):
    request = urllib.request.Request(
        'https://api.github.com/' + path,
        data=None if payload is None else json.dumps(payload).encode(),
        headers={'Authorization': 'Bearer ' + os.environ['GH_TOKEN'],
                 'Accept': 'application/vnd.github+json',
                 'X-GitHub-Api-Version': '2022-11-28',
                 'Content-Type': 'application/json'},
        method=method)
    with urllib.request.urlopen(request, timeout=90) as response:
        return json.load(response)


def digest(path):
    with path.open('rb') as stream:
        return 'sha256:' + hashlib.file_digest(stream, 'sha256').hexdigest()


def check_assets(actual, expected, complete=True):
    found = {a['name']: a for a in actual}
    want = {a['name']: a for a in expected}
    assert len(found) == len(actual), 'Duplicate asset names'
    assert set(found) <= set(want), 'Unexpected destination assets'
    if complete:
        assert set(found) == set(want), 'Missing destination assets'
    for name, asset in found.items():
        assert (asset['size'], asset.get('digest')) == (
            want[name]['size'], want[name]['digest']), 'Asset mismatch: ' + name


def prepare_release(item, source, output):
    original = api('repos/' + source + '/releases/' + str(item['source_release_id']))
    assert not original['draft']
    assert original['tag_name'] == item['tag']
    assert original['name'] == item['title']
    assert original['prerelease'] == item['prerelease']
    assert hashlib.sha256(original['body'].encode()).hexdigest() == item['source_body_sha256']
    check_assets(original['assets'], item['assets'])
    target = output / item['tag']
    target.mkdir(parents=True, exist_ok=True)
    for asset in item['assets']:
        name = asset['name']
        assert Path(name).name == name and name not in ('.', '..')
        path = target / name
        if not path.exists() or (path.stat().st_size, digest(path)) != (asset['size'], asset['digest']):
            partial = target / (name + '.partial')
            subprocess.run(['curl', '--fail', '--location', '--silent', '--show-error',
                            '--retry', '5', '--retry-all-errors', '--connect-timeout', '30',
                            '--max-time', '900', '--proto', '=https', '--output', str(partial),
                            asset['browser_download_url']], check=True)
            assert (partial.stat().st_size, digest(partial)) == (asset['size'], asset['digest']), name
            partial.replace(path)
        print('Verified source asset:', item['tag'], name, path.stat().st_size, flush=True)
    return target


def mirror(item, source, destination, target):
    tag = item['tag']
    temporary_ref = 'refs/history-import/' + tag
    subprocess.run(['git', 'fetch', '--no-tags', 'https://github.com/' + source + '.git',
                    'refs/tags/' + tag + ':' + temporary_ref], check=True)
    assert run('git', 'rev-parse', temporary_ref) == item['tag_sha'], 'Source tag changed'
    existing_tag = run('git', 'ls-remote', '--refs', 'origin', 'refs/tags/' + tag)
    if existing_tag:
        assert existing_tag.split()[0] == item['tag_sha'], 'Destination tag conflicts'
    else:
        subprocess.run(['git', 'push', 'origin', temporary_ref + ':refs/tags/' + tag], check=True)
    try:
        release = api('repos/' + destination + '/releases/tags/' + tag)
    except urllib.error.HTTPError as exc:
        if exc.code != 404:
            raise
        release = api('repos/' + destination + '/releases', {
            'tag_name': tag, 'name': item['title'], 'body': item['body'],
            'draft': True, 'prerelease': item['prerelease'], 'make_latest': 'false'})
    assert release['name'] == item['title']
    assert release['body'] == item['body'], 'Destination notes differ; no overwrite'
    assert release['prerelease'] == item['prerelease']
    check_assets(release['assets'], item['assets'], complete=not release['draft'])
    existing = {a['name'] for a in release['assets']}
    missing = [str(target / a['name']) for a in item['assets'] if a['name'] not in existing]
    if missing:
        assert release['draft'], 'Never modify published assets'
        subprocess.run(['gh', 'release', 'upload', tag, '--repo', destination, *missing], check=True)
    endpoint = 'repos/' + destination + '/releases/' + str(release['id'])
    for attempt in range(12):
        release = api(endpoint)
        if all(a.get('digest') for a in release['assets']):
            break
        time.sleep(5)
    check_assets(release['assets'], item['assets'])
    if release['draft']:
        api(endpoint, {'draft': False, 'prerelease': item['prerelease'], 'make_latest': 'false'}, 'PATCH')
    release = api(endpoint)
    assert not release['draft']
    assert release['body'] == item['body']
    assert release['prerelease'] == item['prerelease']
    check_assets(release['assets'], item['assets'])
    print(json.dumps({'published': release['html_url'], 'assets_verified': len(item['assets']),
                      'original_tag_sha': item['tag_sha']}, ensure_ascii=False), flush=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--manifest', default='history/manifest.json')
    args = parser.parse_args()
    manifest = json.loads(Path(args.manifest).read_text())
    assert os.environ['GITHUB_REPOSITORY'] == manifest['destination']
    output = Path(os.environ.get('RUNNER_TEMP', '/tmp')) / 'omindos-history-assets'
    # Complete downloads and source checks before creating any release.
    prepared = [(item, prepare_release(item, manifest['source'], output))
                for item in manifest['releases']]
    for item, target in prepared:
        mirror(item, manifest['source'], manifest['destination'], target)


if __name__ == '__main__':
    main()
