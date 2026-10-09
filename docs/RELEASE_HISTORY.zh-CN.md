# 历史版本与下载记录

[返回首页](../README.md)

首次使用请按首页用途选择。这里保留版本追溯、旧包兼容和历史 Windows 下载；旧版本号、附件及 SHA256 均保持原样。

## 按用途查看发行

| 类别 | 发行版本 | 说明 |
| --- | --- | --- |
| 当前轻量工作台与完整仿真包 | [v0.2.0-preview.6](https://github.com/maganrobotics-boop/OmindOS-Navigation-Release/releases/tag/v0.2.0-preview.6) | [功能、安装与兼容性](CONTROL_PREVIEW_6.zh-CN.md)；完整包约 540 MB |
| ARM64 软件环境 | [v0.2.0-arm64-preview.2](https://github.com/maganrobotics-boop/OmindOS-Navigation-Release/releases/tag/v0.2.0-arm64-preview.2) | [构建与验收范围](ARM64_PREVIEW_2.zh-CN.md)；约 522 MB |
| DM-MC02 独立台架固件 | [dm-mc02-bench-v0.1.0-preview.1](https://github.com/maganrobotics-boop/OmindOS-Navigation-Release/releases/tag/dm-mc02-bench-v0.1.0-preview.1) | [固件说明](DM_MC02_BENCH_PREVIEW_1.zh-CN.md)；三路 CAN 只读 |
| 统一导航与参数 API | [v0.2.0-preview.2](https://github.com/maganrobotics-boop/OmindOS-Navigation-Release/releases/tag/v0.2.0-preview.2) | [原版说明](../history/v0.2.0-preview.2/README.md)；约 265 MB，仍用于三平台导航预览 |
| 旧完整四足控制预览 | [v0.2.0-preview.5](https://github.com/maganrobotics-boop/OmindOS-Navigation-Release/releases/tag/v0.2.0-preview.5) | [原版说明](CONTROL_PREVIEW_5.zh-CN.md)；约 820 MB |
| 旧 ARM64 软件环境 | [v0.2.0-arm64-preview.1](https://github.com/maganrobotics-boop/OmindOS-Navigation-Release/releases/tag/v0.2.0-arm64-preview.1) | [原版说明](ARM64_PREVIEW_1.zh-CN.md) |
| 早期三平台导航接口 | [v0.2.0-preview.1](https://github.com/maganrobotics-boop/OmindOS-Navigation-Release/releases/tag/v0.2.0-preview.1) | [原版说明](../history/v0.2.0-preview.1/README.md)；约 265 MB |

## 保留的轻量工作台

仅需三维调参、希望不使用 Docker 的用户可保留使用旧轻量包。普通用户已下载首页完整包时，无需再下载它。

[Ubuntu 轻量工作台（21.99 MB）](https://github.com/maganrobotics-boop/OmindOS-Navigation-Release/releases/download/v0.2.0-preview.6/omindos-quadruped-workbench-0.2.0-size-candidate.1-linux-x64.tar.gz) · [轻量包解压与启动说明](CONTROL_PREVIEW_6.zh-CN.md#轻量工作台启动)

## Windows 历史下载

**Windows 暂不继续开发。** 既有包保留下载，未签名；Windows ROS / WSL 联调尚未验收。

[旧 Windows x64 轻量工作台（8.23 MB）](https://github.com/maganrobotics-boop/OmindOS-Navigation-Release/releases/download/v0.2.0-preview.6/omindos-quadruped-workbench-0.2.0-size-candidate.1-windows-x64.zip) · [旧版安装范围](CONTROL_PREVIEW_6.zh-CN.md) · [SHA256](../assets/v0.2.0-preview.6/SHA256SUMS-release.txt)

## 从原发行仓迁移的记录

preview.1 / preview.2 来自 Omind-Robotics 原发行仓。归档说明按原发行范围保存；完整安装包沿用原下载服务器，原 GitHub 附件也保留。两版不包含客户真实四足的步态、平衡或硬件验收。

同名标签指向本仓库的归档文档快照，原始标签提交记录保存在各版 `ORIGIN.json`：[preview.1 来源](../history/v0.2.0-preview.1/ORIGIN.json)、[preview.2 来源](../history/v0.2.0-preview.2/ORIGIN.json)。
