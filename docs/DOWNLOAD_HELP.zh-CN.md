# 下载、版本与常见问题

[返回首页](../README.md)

## 为什么有多个包？

**普通用户只下载首页的 Ubuntu 完整安装包，工作台和四足算法环境已经包含。** 轻量工作台保留给只做调参的历史用户；早期统一导航包、ARM64 包和板卡固件用于专业开发场景，见[专业指南](DEVELOPER.zh-CN.md)，无需全部下载。

## 当前版本如何校验？

preview.7 的文件名与应用版本均为 `0.2.0-preview.7`。下载后可用[SHA256 清单](https://github.com/maganrobotics-boop/OmindOS-Navigation-Release/releases/download/v0.2.0-preview.7/SHA256SUMS-release.txt)核对；解压后运行 `./omindos verify` 验证运行镜像。

## 历史包为什么下载名与发行版本不一样？

preview.6 原样发布已验收的构建，文件名保留 `size-candidate.1`；完整包内业务版本仍是 preview.5。这些文件就是公开发行资产，名称、内容和 SHA256 没有重新打包改变。版本号属于各自用途，不能只按数字大小选择。

完整仿真包从 820.45 MB 缩小到 540.42 MB，减少 34.13%；保留原有业务与仿真功能。约 22 MB 的轻量包没有完整 ROS / MuJoCo / PyTorch 环境，功能范围不同。

## x64、amd64 与 ARM64 怎么选？

| 电脑 / 输出 | 应选架构 |
| --- | --- |
| Intel / AMD 普通 Ubuntu PC；`uname -m` 为 `x86_64` | Linux x64 / amd64 |
| Jetson 等 ARM64 Linux；`uname -m` 为 `aarch64` | ARM64；Jetson 实机仍待验收 |

当前开发与交付以 Ubuntu 为主。历史 Windows 下载移至[历史版本页](RELEASE_HISTORY.zh-CN.md)。

## 下载失败怎么办？

当前 preview.7 请从[发行页](https://github.com/maganrobotics-boop/OmindOS-Navigation-Release/releases/tag/v0.2.0-preview.7)重试下载。以下镜像属于历史 preview.6，尚不包含新版界面：

- [Ubuntu 轻量工作台镜像](https://omindos.cn/downloads/navigation/v0.2.0-preview.6/omindos-quadruped-workbench-0.2.0-size-candidate.1-linux-x64.tar.gz)
- [完整仿真包镜像](https://omindos.cn/downloads/navigation/v0.2.0-preview.6/omindos-control-preview-0.2.0-preview.5-size-candidate.1-linux-amd64.tar)
- [镜像 SHA256 清单](https://omindos.cn/downloads/navigation/v0.2.0-preview.6/SHA256SUMS-release.txt)

按清单校验文件；若下载中断或哈希不符，请重新下载，不要继续启动。不要下载 GitHub 自动生成的 **Source code** ZIP / TAR 来安装应用：它们是本发行仓的资料快照，不能替代安装包。

## 软件和硬件验证分别到哪一步？

| 交付内容 | 已完成 | 仍待完成 |
| --- | --- | --- |
| 轻量工作台 / 完整仿真包 | 编译、功能回归、Ubuntu 浏览器和 ROS 联调、四组参考模型动力学场景 | 客户模型和真实整机验收 |
| 统一导航包 | 三平台配置、目标到达、限速和超时逻辑的软件预览 | 真实底盘驱动、定位、避障及任务验收 |
| ARM64 包 | 原生 ARM64 软件验证 | Jetson 实机安装与 RS04 联调 |
| DM-MC02 固件 | 完整编译链接、ELF / HEX / BIN、SHA256 和静态检查 | 实际刷写、USB / CAN / RNG / RTOS 台架验收 |

DM-MC02 只读模式不发送 CAN 数据帧，也不提供 ACK；STOP 仅锁存软件会话，不是物理急停。首次上板条件见[固件指南](DM_MC02_BENCH_PREVIEW_1.zh-CN.md)。

## 校验与技术记录

| 交付 | 校验值 | 验证记录 / 技术说明 |
| --- | --- | --- |
| 当前 Ubuntu 完整包 | [preview.7 SHA256](https://github.com/maganrobotics-boop/OmindOS-Navigation-Release/releases/download/v0.2.0-preview.7/SHA256SUMS-release.txt) | [完整包验收](https://github.com/maganrobotics-boop/OmindOS-Navigation-Release/releases/download/v0.2.0-preview.7/VALIDATION.json) · [浏览器验收](https://github.com/maganrobotics-boop/OmindOS-Navigation-Release/releases/download/v0.2.0-preview.7/BROWSER_VALIDATION.json) |
| 历史轻量工作台 / 完整仿真包 | [preview.6 SHA256](../assets/v0.2.0-preview.6/SHA256SUMS-release.txt) | [验证记录](../assets/v0.2.0-preview.6/VALIDATION.json) · [安装说明](CONTROL_PREVIEW_6.zh-CN.md) |
| 统一导航包 | [导航 SHA256](https://omindos.cn/downloads/navigation/v0.2.0-preview.2/SHA256SUMS-release.txt) | [原版安装和验证说明](../history/v0.2.0-preview.2/README.md) |
| ARM64 包 | [ARM64 SHA256](../assets/v0.2.0-arm64-preview.2/SHA256SUMS-release.txt) | [验证记录](../assets/v0.2.0-arm64-preview.2/VALIDATION.json) · [精确构建](ARM64_PREVIEW_2.zh-CN.md) |
| DM-MC02 固件 | [固件 SHA256](../assets/dm-mc02-bench-v0.1.0-preview.1/SHA256SUMS-release.txt) | [完整固件验证](../assets/dm-mc02-bench-v0.1.0-preview.1/VALIDATION.json) |

轻量工作台、完整四足包及 ARM64 包的后端业务程序以编译形式交付；后端业务源码不随包提供。早期统一导航包的源码范围按其历史发行说明保留。第三方软件许可证见[第三方说明](../THIRD_PARTY.md)和包内通知。
