#!/bin/sh
set -eu
cd "$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
test "$(uname -s)" = Linux && test "$(uname -m)" = x86_64 || { echo '需要 Ubuntu x86_64 电脑。' >&2; exit 2; }
command -v docker >/dev/null 2>&1 || { echo '请先安装 Docker Engine。' >&2; exit 2; }
docker info >/dev/null 2>&1 || { echo '请确认 Docker 服务已启动，当前账户有访问权限。' >&2; exit 2; }
image='omindos/navigation:0.2.0-preview.7'
image_known() {
    layers=$(docker image inspect --format '{{join .RootFS.Layers "\n"}}' "$image" 2>/dev/null) || return 1
    test "$layers" = "$(cat IMAGE_LAYERS.txt)" || return 1
    runtime=$(docker image inspect --format '{{json .Config.Env}}|{{json .Config.Entrypoint}}|{{json .Config.Cmd}}|{{.Config.WorkingDir}}|{{.Config.User}}' "$image" 2>/dev/null) || return 1
    test "$runtime" = "$(cat IMAGE_RUNTIME.txt)"
}
if ! image_known; then
    sha256sum -c SHA256SUMS-image.txt
    docker load -i runtime.image.tar.gz
fi
image_known || { echo '镜像内容或启动配置校验失败。' >&2; exit 2; }
mkdir -p data
if [ "$#" -eq 0 ]; then set -- workbench; fi
case "$1" in
  workbench|parameter-api) set -- "$@" --store /data/profiles ;;
  ros-preview) set -- "$@" --store /data/profiles ;;
  quadruped|quadruped-ros) set -- "$@" --token-file /data/quadruped.token ;;
  validate-dynamics) set -- "$@" --source /opt/omindos/reference --output /data/dynamics.json ;;
esac
exec docker run --rm --init --network host --user "$(id -u):$(id -g)" \
    --cap-drop ALL --security-opt no-new-privileges \
    -e HOME=/tmp -e ROS_LOCALHOST_ONLY=1 -e ROS_DOMAIN_ID="${ROS_DOMAIN_ID:-42}" \
    -v "$(pwd)/data:/data" "$image" "$@"
