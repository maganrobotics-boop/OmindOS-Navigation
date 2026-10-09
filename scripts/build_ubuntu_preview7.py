#!/usr/bin/env python3
"""Assemble one Ubuntu installer from a verified runtime and compiled update."""
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import shlex
import subprocess
import tarfile
import time
import urllib.error
import urllib.request

VERSION = '0.2.0-preview.7'
TAG = 'v' + VERSION
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'build/ubuntu-preview7'
ASSETS = ROOT / 'assets' / TAG
BASE_SHA = 'af2cc32308c0ffc0a14b26cd71f454b8b9566096573ee09fb09f191ec7eedbd8'
BASE_NAME = 'omindos-control-preview-0.2.0-preview.5-size-candidate.1-linux-amd64.tar'
BASE_URL = 'https://github.com/maganrobotics-boop/OmindOS-Navigation-Release/releases/download/v0.2.0-preview.6/' + BASE_NAME
IMAGE = 'omindos/navigation:' + VERSION
NAME = 'omindos-navigation-' + VERSION + '-ubuntu-amd64'


def sha(path):
    with Path(path).open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()


def run(*args, **kw):
    return subprocess.run(args, check=True, **kw)


def request(path, data=None):
    req=urllib.request.Request('http://127.0.0.1:8085'+path,
        data=None if data is None else json.dumps(data).encode(),headers={'Content-Type':'application/json'})
    with urllib.request.urlopen(req,timeout=15) as r:
        return json.load(r) if 'application/json' in r.headers['Content-Type'] else r.read()


def docker_capture(*args):
    return subprocess.check_output(['docker',*args],text=True).strip()


def validate_image(archive, image):
    with tarfile.open(archive, 'r:gz') as t:
        manifest=json.load(t.extractfile('manifest.json'))
        assert len(manifest)==1 and image in manifest[0]['RepoTags']
        exported=json.load(t.extractfile(manifest[0]['Config']))
    actual=json.loads(docker_capture('image','inspect',image))[0]
    assert actual['RootFS']['Layers']==exported['rootfs']['diff_ids']
    assert actual['Architecture']==exported['architecture']=='amd64'
    assert actual['Os']==exported['os']=='linux'
    for key in ('Env','Entrypoint','Cmd','WorkingDir','User','Labels'):
        assert (actual['Config'].get(key) or None)==(exported['config'].get(key) or None),key
    return actual


def main():
    OUT.mkdir(parents=True,exist_ok=True);ASSETS.mkdir(parents=True,exist_ok=True)
    summary=json.loads((ASSETS/'UPDATE_SUMMARY.json').read_text())
    update=ASSETS/summary['filename']
    assert summary['status']=='PASS' and update.stat().st_size==summary['bytes'] and sha(update)==summary['sha256']
    assert summary['compiled_modules']==16 and summary['compiled_regression_tests']==79 and summary['reference_asset_tests']==3
    with tarfile.open(update,'r:gz') as t:t.extractall(OUT/'patch',filter='data')
    patch=OUT/'patch/update';patch_info=json.loads((patch/'WORKBENCH_UPDATE.json').read_text())
    assert patch_info['source_commit']==summary['source_commit'] and not patch_info['backend_source_included']
    for name,digest in patch_info['files'].items():assert sha(patch/name)==digest,name
    base_archive=OUT/BASE_NAME
    if not base_archive.exists() or sha(base_archive)!=BASE_SHA:
        run('curl','--fail','--location','--retry','3','--output',str(base_archive),BASE_URL)
    assert sha(base_archive)==BASE_SHA and base_archive.stat().st_size==540416000
    with tarfile.open(base_archive) as t:t.extractall(OUT/'base',filter='data')
    baseline=next((OUT/'base').glob('omindos-control-preview-*'))
    baseline_image=re.search(r"^image='([^']+)'",(baseline/'omindos').read_text(),re.M).group(1)
    run('sha256sum','-c','SHA256SUMS-image.txt',cwd=baseline)
    run('docker','load','-i',str(baseline/'runtime.image.tar.gz'))
    base_info=validate_image(baseline/'runtime.image.tar.gz',baseline_image)
    context=OUT/'context';context.mkdir(exist_ok=True)
    shutil.copytree(patch,context/'update',dirs_exist_ok=True)
    dockerfile=f'''FROM {baseline_image} AS updated
RUN /opt/omindos-runtime/bin/python -m pip install --no-cache-dir --only-binary=:all: --timeout 30 --retries 2 --index-url https://pypi.org/simple numpy==1.26.4 scipy==1.14.1
COPY update/scripts /opt/omindos/scripts
COPY update/web /opt/omindos/web
COPY update/config /opt/omindos/config
COPY update/LICENSES /opt/omindos/LICENSES
COPY update/WORKBENCH_UPDATE.json /opt/omindos/WORKBENCH_UPDATE.json
RUN find /opt/omindos-runtime -type d -name __pycache__ -prune -exec rm -rf '{{}}' +
FROM scratch
COPY --from=updated / /
ENV PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin LANG=C.UTF-8 LC_ALL=C.UTF-8 ROS_DISTRO=humble PYTHONDONTWRITEBYTECODE=1 ROS_LOCALHOST_ONLY=1 OMP_NUM_THREADS=1
LABEL org.opencontainers.image.version="{VERSION}" org.opencontainers.image.source="https://github.com/maganrobotics-boop/OmindOS-Navigation-Release" org.opencontainers.image.revision="{summary['source_commit']}"
WORKDIR /opt/omindos
ENTRYPOINT ["/ros_entrypoint.sh", "/usr/local/bin/omindos-runtime"]
CMD ["--help"]
'''
    (context/'Dockerfile').write_text(dockerfile)
    run('docker','build','--network=host','--progress','plain','-t',IMAGE,str(context))
    info=json.loads(docker_capture('image','inspect',IMAGE))[0]
    audit_code="""from pathlib import Path
import hashlib,json,importlib,sys
sys.path.insert(0,'/opt/omindos/scripts')
r=Path('/opt/omindos')
bad=[str(p) for p in (r/'scripts').rglob('*') if p.is_file() and p.suffix in {'.py','.pyc','.pyo','.c','.h','.cpp'}]
assert not bad,bad
assert not list(r.rglob('*.customer-record.json'))
m=json.loads((r/'WORKBENCH_UPDATE.json').read_text())
for n,h in m['files'].items():assert hashlib.sha256((r/n).read_bytes()).hexdigest()==h,n
for n in m['compiled_modules']:assert importlib.import_module(n).__file__.endswith('.so'),n
import numpy,scipy,torch,mujoco
assert numpy.__version__=='1.26.4' and scipy.__version__=='1.14.1'
assert float(torch.tensor([2.,3.]).sum())==5
print(json.dumps({'compiled_modules':len(m['compiled_modules']),'numpy':numpy.__version__,'scipy':scipy.__version__,'torch':torch.__version__,'mujoco':mujoco.__version__,'business_source_files':len(bad)}))
"""
    audit=json.loads(docker_capture('run','--rm','--network','none','--entrypoint','bash',IMAGE,'-lc',
        'source /opt/ros/humble/setup.bash; /opt/omindos-runtime/bin/python -c ' + shlex.quote(audit_code)))
    # Verify inherited simulation/model files were not changed by the workbench update.
    hash_code="""from pathlib import Path
import hashlib,json
r=Path('/opt/omindos');changed={'robot_workbench','robot_assets','robot_kinematics','robot_parameter_api','workbench_state','robot_connections','robot_runtime_client','robot_sequence','robot_planning','robot_navigation','dual_task_planner','navigation_kernel','navigation_guard','robot_profile_runtime_core','robot_profile_runtime','native_entry'}
files=list((r/'reference').rglob('*'))+[p for p in (r/'scripts').glob('*.so') if p.name.split('.')[0] not in changed]
print(json.dumps({str(p.relative_to(r)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(files) if p.is_file()}))
"""
    unchanged=json.loads(docker_capture('run','--rm','--network','none','--entrypoint','/opt/omindos-runtime/bin/python',baseline_image,'-c',hash_code))
    inherited=json.loads(docker_capture('run','--rm','--network','none','--entrypoint','/opt/omindos-runtime/bin/python',IMAGE,'-c',hash_code))
    assert unchanged==inherited,'Simulation or reference model changed'
    package=OUT/NAME;package.mkdir(exist_ok=False)
    for name in ['config','LICENSES']:shutil.copytree(baseline/name,package/name)
    shutil.copytree(patch/'config',package/'config',dirs_exist_ok=True)
    shutil.copytree(patch/'LICENSES',package/'LICENSES',dirs_exist_ok=True)
    for name in ['THIRD_PARTY.md','THIRD_PARTY_PACKAGES.txt']:shutil.copy2(baseline/name,package/name)
    (package/'THIRD_PARTY_PYTHON.json').write_text(docker_capture('run','--rm','--network','none','--entrypoint','/opt/omindos-runtime/bin/python',IMAGE,'-m','pip','list','--format=json')+'\n')
    (package/'IMAGE_ID.txt').write_text(info['Id']+'\n')
    (package/'IMAGE_LAYERS.txt').write_text('\n'.join(info['RootFS']['Layers'])+'\n')
    template='{{json .Config.Env}}|{{json .Config.Entrypoint}}|{{json .Config.Cmd}}|{{.Config.WorkingDir}}|{{.Config.User}}'
    (package/'IMAGE_RUNTIME.txt').write_text(docker_capture('image','inspect','--format',template,IMAGE)+'\n')
    launcher=(ROOT/'scripts/ubuntu_preview7_launcher.sh').read_text()
    (package/'omindos').write_text(launcher);(package/'omindos').chmod(0o755)
    installer="""#!/bin/sh
set -eu
cd "$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
sha256sum -c SHA256SUMS-files.txt
./omindos --version
printf '\\n安装完成。运行 ./omindos workbench，再打开 http://127.0.0.1:8085/\\n'
"""
    (package/'install.sh').write_text(installer);(package/'install.sh').chmod(0o755)
    readme='''# OmindOS Navigation · Ubuntu 完整安装包

工作台、四足模型、参数 API、ROS 2、PyTorch CPU 和 MuJoCo 已集成，无需分别下载算法包。
适用 Ubuntu 22.04 / 24.04、Intel / AMD 64 位电脑，需要 Docker Engine。

完整解压后，在该目录运行：

```bash
./install.sh
./omindos workbench
```

浏览器打开 http://127.0.0.1:8085/，无需账号登录。左侧修改参数，中间预览完整模型，右侧试运行和保存。
配置保存在 data/；用户可导入自己的 URDF / JSON，并按客户硬件设置参数。

`./omindos validate-dynamics` 可运行四组四足动力学仿真；`./omindos ros-preview` 启动 ROS 2 关节预览。
模型与策略仿真使用固定版本 MEVIUS2 参考模型。工作台点动是运动学预览，不驱动真实电机。
真实机器人和 DM-MC02/RS04 电气联调尚未验收，本包不包含可烧录固件。

后端业务程序以编译形式交付；模型、网页与第三方许可证保留。
'''
    (package/'README.zh-CN.md').write_text(readme)
    with (package/'runtime.image.tar.gz').open('wb') as f:
        save=subprocess.Popen(['docker','save',IMAGE],stdout=subprocess.PIPE)
        zipped=subprocess.run(['gzip','-1'],stdin=save.stdout,stdout=f)
        save.stdout.close();assert save.wait()==0 and zipped.returncode==0
    validate_image(package/'runtime.image.tar.gz',IMAGE)
    (package/'SHA256SUMS-image.txt').write_text(sha(package/'runtime.image.tar.gz')+'  runtime.image.tar.gz\n')
    manifest={'version':VERSION,'platform':'ubuntu-amd64','source_commit':summary['source_commit'],
              'baseline_archive_sha256':BASE_SHA,'image_id':info['Id'],'backend_source_included':False,
              'hardware_validated':False,'reference_model_commit':'4f09680bb575574377b903bbc971bdb2695d507b',
              'single_installer':True,'files':{str(p.relative_to(package)):sha(p) for p in sorted(package.rglob('*')) if p.is_file()}}
    (package/'MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
    checksums={str(p.relative_to(package)):sha(p) for p in sorted(package.rglob('*')) if p.is_file()}
    (package/'SHA256SUMS-files.txt').write_text(''.join(h+'  '+n+'\n' for n,h in checksums.items()))
    archive=ASSETS/(NAME+'.tar')
    with tarfile.open(archive,'w') as t:t.add(package,arcname=NAME)
    fresh=OUT/'fresh-unpack'
    with tarfile.open(archive) as t:t.extractall(fresh,filter='data')
    installed=fresh/NAME
    run('docker','image','rm',IMAGE)
    run(str(installed/'install.sh'))
    assert docker_capture('run','--rm','--network','none',IMAGE,'--version')==VERSION
    server_log=(OUT/'installed-workbench.log').open('w')
    server=subprocess.Popen([str(installed/'omindos'),'workbench'],cwd=installed,stdout=server_log,stderr=subprocess.STDOUT)
    try:
        for attempt in range(60):
            try:profile=request('/example.json');break
            except (OSError,urllib.error.URLError):time.sleep(.5)
        else:raise RuntimeError((OUT/'installed-workbench.log').read_text())
        assert profile['robot_id']=='mevius2-reference'
        result=request('/v1/robot-model',{'urdf_xml':profile['kinematics']['urdf_xml']})
        assert len(result['pose']['positions'])==12 and not result['model']['warnings']
        meshes=[g for l in result['model']['links'] for g in l['visuals'] if g['type']=='mesh']
        assert len(meshes)==13 and all(g['url'].startswith('/meshes/mevius2/') for g in meshes)
        for mesh in meshes:assert len(request(mesh['url']))>1000
        applied=request('/v1/workbench-active-profile',profile)
        assert applied['workbench_applied'] and not applied['runtime_applied'] and not applied['hardware_connected']
        registered=request('/v1/robot-profiles',profile)
        assert request('/v1/robot-profiles/'+registered['profile_id'])==profile
        jog=request('/v1/robot-jog',{'joint':'FL_collar_joint','direction':1})
        assert not jog['runtime_applied'] and jog['step_deg']==.1
        stopped=request('/v1/workbench-stop',{'engaged':True})
        try:request('/v1/robot-jog',{'joint':'FL_collar_joint','direction':1});raise AssertionError('stop bypassed')
        except urllib.error.HTTPError as e:assert e.code==423
        request('/v1/workbench-stop',{'engaged':False,'expected_epoch':stopped['motion_epoch']})
        # Capture from a fresh empty store so the initial UI matches first installation.
        for p in (installed/'data').rglob('*'):
            if p.is_file():p.unlink()
    finally:
        server.terminate();server.wait(20);server_log.close()
    # Relaunch a clean installation for actual browser validation and screenshot.
    clean_store=OUT/'browser-install';shutil.copytree(installed,clean_store,ignore=shutil.ignore_patterns('data'))
    browser_log=(OUT/'browser-workbench.log').open('w')
    browser_server=subprocess.Popen([str(clean_store/'omindos'),'workbench'],cwd=clean_store,stdout=browser_log,stderr=subprocess.STDOUT)
    try:
        for attempt in range(60):
            try:request('/');break
            except (OSError,urllib.error.URLError):time.sleep(.5)
        run('node',str(ROOT/'scripts/capture_ubuntu_preview7.cjs'),str(ROOT/'docs/media'))
    finally:
        browser_server.terminate();browser_server.wait(20);browser_log.close()
    dynamics=OUT/'dynamics';dynamics.mkdir()
    run('docker','run','--rm','--network','none','-v',str(dynamics)+':/qa',IMAGE,
        'validate-dynamics','--source','/opt/omindos/reference','--output','/qa/dynamics.json',timeout=600)
    dynamics_report=json.loads((dynamics/'dynamics.json').read_text())
    assert dynamics_report.get('status')=='PASS',dynamics_report
    browser=json.loads((ROOT/'docs/media/CAPTURE.json').read_text())
    browser.update(stage='installed-ubuntu-package',installer_updated=True,source_commit=summary['source_commit'],
        image_id=info['Id'],package_version=VERSION,capture_workflow_run=os.environ.get('GITHUB_RUN_ID'))
    (ROOT/'docs/media/CAPTURE.json').write_text(json.dumps(browser,indent=2)+'\n')
    validation={'status':'PASS','version':VERSION,'image_id':info['Id'],'compiled_tests':79,'reference_tests':3,
        'audit':audit,'unchanged_simulation_and_model_files':len(unchanged),'browser':browser,'dynamics':dynamics_report,
        'checks':['full_archive_manifest','independent_unpack','install_script_imports_image','version_matches_release',
            'complete_13_mesh_reference','12_joints','local_api_save_reload','apply_configuration','point_one_degree_jog',
            'stop_latches_motion','actual_browser_capture','four_dynamics_scenarios'],
        'hardware_validated':False,'backend_source_included':False,'windows_built':False}
    (ASSETS/'VALIDATION.json').write_text(json.dumps(validation,indent=2)+'\n')
    release_summary={'release_tag':TAG,'version':VERSION,'platform':'ubuntu-amd64','filename':archive.name,
        'bytes':archive.stat().st_size,'sha256':sha(archive),'image_id':info['Id'],'source_commit':summary['source_commit'],
        'backend_source_included':False,'single_installer':True,'hardware_validated':False,
        'files':[{'filename':archive.name,'bytes':archive.stat().st_size,'sha256':sha(archive)}]}
    (ASSETS/'RELEASE_SUMMARY.json').write_text(json.dumps(release_summary,indent=2)+'\n')
    (ASSETS/'SHA256SUMS-release.txt').write_text(release_summary['sha256']+'  '+archive.name+'\n')
    notes=f'''# OmindOS Navigation {VERSION} · Ubuntu 完整安装包

**[下载 Ubuntu 安装包](https://github.com/maganrobotics-boop/OmindOS-Navigation-Release/releases/download/{TAG}/{archive.name})** · {archive.stat().st_size/1e6:.2f} MB

只下载这一份。工作台、完整四足外观模型、参数 API、ROS 2、PyTorch CPU、MuJoCo 与四足策略仿真均已集成。
适用 Ubuntu 22.04 / 24.04、Intel / AMD 64 位电脑；需要 Docker Engine。完整解压后运行 `./install.sh`，再运行 `./omindos workbench`。

新版默认加载完整四足参考外观，替换方块示意模型。用户可导入自己的 URDF / JSON，并根据客户硬件修改参数。
无需登录；配置保存在本机 data/。开发者可调用本地参数 API。

软件验收通过：79 项编译模块测试、3 项固定资源测试；完整包独立解压、安装与启动；13/13 网格和 12 关节；参数应用、保存回读、点动和软件停止；实际浏览器截图；四组 MuJoCo 动力学场景。
修正不同 Docker 版本的镜像编号差异，按镜像层与启动配置识别实际内容。

当前为软件预览发行，真实机器人尚未验收；不使能真实电机。本次仅发布 Ubuntu，不新增 Windows 包。后端业务源码不随包提供。

SHA256：`{release_summary['sha256']}`
'''
    (ASSETS/'RELEASE_NOTES.zh-CN.md').write_text(notes)
    print(json.dumps(release_summary),flush=True)


if __name__=='__main__':main()
