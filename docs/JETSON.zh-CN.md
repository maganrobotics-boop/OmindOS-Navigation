# Jetson / ARM64：四足软件环境

[返回首页](../README.md)

**ARM64 运行包用于准备 Jetson 等 ARM64 Linux 主机上的软件环境。** 普通 Intel / AMD Ubuntu 电脑应选择首页的 x64 包。

## 下载

**[下载 ARM64 运行包（521.54 MB）](https://github.com/maganrobotics-boop/OmindOS-Navigation-Release/releases/download/v0.2.0-arm64-preview.2/omindos-control-arm64-candidate.tar)**

[SHA256 校验文件](../assets/v0.2.0-arm64-preview.2/SHA256SUMS-release.txt) · [发行记录](https://github.com/maganrobotics-boop/OmindOS-Navigation-Release/releases/tag/v0.2.0-arm64-preview.2)

需要 ARM64 Linux 和 Docker Engine。`uname -m` 应显示 `aarch64`。原生 ARM64 软件验证已通过；**Jetson 实机安装尚未验收**，GPU / JetPack 组合也未因此获得验证。

## 安装

```bash
sha256sum -c SHA256SUMS-release.txt
tar -xf omindos-control-arm64-candidate.tar
cd omindos-control-arm64-candidate
./omindos workbench
```

浏览器访问 `http://localhost:8085/`。参数和关节预览使用 `./omindos ros-preview`；仿真按包内说明启动 `quadruped` 和 `quadruped-ros`。

## 与板卡固件的关系

这个包运行在主机上，包含编译后的主机通信协议模块；**不包含 DM-MC02 板卡固件，不启用电机输出**。启动器默认不映射 USB / CAN 电机设备。

DM-MC02 的 ELF / HEX / BIN 已单独发布，见[台架固件与首次上板条件](DM_MC02_BENCH_PREVIEW_1.zh-CN.md)。主机运行包和板卡固件有各自版本，两者均不代表 Jetson—DM-MC02—RS04 实物联调已经通过。

[ARM64 包的精确构建与验收说明](ARM64_PREVIEW_2.zh-CN.md)
