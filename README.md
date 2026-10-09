# OmindOS Navigation

[最新预览 v0.2.0-preview.6](https://github.com/maganrobotics-boop/OmindOS-Navigation-Release/releases/tag/v0.2.0-preview.6) · [安装与兼容性](docs/CONTROL_PREVIEW_6.zh-CN.md)

四足软件提供独立轻量工作台和完整 ROS 2／仿真运行包。后端业务程序以编译形式交付，业务源码不随包提供。

| 下载 | 大小 | 适用场景 |
| --- | ---: | --- |
| [Linux x64 轻量工作台](https://github.com/maganrobotics-boop/OmindOS-Navigation-Release/releases/download/v0.2.0-preview.6/omindos-quadruped-workbench-0.2.0-size-candidate.1-linux-x64.tar.gz) | 21.99 MB | 独立三维调参、URDF 与运动学预览 |
| [Windows x64 轻量工作台](https://github.com/maganrobotics-boop/OmindOS-Navigation-Release/releases/download/v0.2.0-preview.6/omindos-quadruped-workbench-0.2.0-size-candidate.1-windows-x64.zip) | 8.23 MB | 同上；未签名 |
| [Linux amd64 完整包](https://github.com/maganrobotics-boop/OmindOS-Navigation-Release/releases/download/v0.2.0-preview.6/omindos-control-preview-0.2.0-preview.5-size-candidate.1-linux-amd64.tar) | 540.42 MB | ROS 2 Humble、策略推理与 MEVIUS2 闭环仿真；需 Docker |

完整包相较 preview.5 的 820.45 MB 减少 **34.13%**，保留既有业务与仿真功能。轻量包无需另装 Python、ROS 或 Docker，默认是 12 关节合成教学模型，可导入实际 URDF；动力学仿真使用完整包。Jetson、Windows ROS/WSL 和真实电机未在此版本验收。

本次原样发布已验收候选，安装包名仍含 `size-candidate.1`，完整包内业务版本仍为 preview.5。包内旧 README 为构建时快照，当前状态与联调结果见 [preview.6 说明](docs/CONTROL_PREVIEW_6.zh-CN.md) 和 [验证记录](assets/v0.2.0-preview.6/VALIDATION.json)。[SHA256 校验值](assets/v0.2.0-preview.6/SHA256SUMS-release.txt)

## DM-MC02 禁使能台架固件

[固件预发布 0.1.0-preview.1](https://github.com/maganrobotics-boop/OmindOS-Navigation-Release/releases/tag/dm-mc02-bench-v0.1.0-preview.1) · [上板条件与完整说明](docs/DM_MC02_BENCH_PREVIEW_1.zh-CN.md) · [SHA256](assets/dm-mc02-bench-v0.1.0-preview.1/SHA256SUMS-release.txt)

2026-10-09：开发 PR #18 已合并。47 项测试、44 个 Cortex-M7 对象完整编译与链接、179 个向量检查通过，ELF/HEX/BIN 已生成并验证重复构建一致；BIN 31,392 字节。三路 CAN 始终为只读 BUS_MONITORING，TX 分配为零，不包含电机使能或运动发送。

**真实板卡尚未验收**。可烧录格式生成不代表已经刷写或实机可用：启动地址暂按 `0x08000000`，板卡 revision、bootloader、时钟/RNG、USB/CAN、实际 ID 和任务栈余量都需实测。首次仅限动力断开、限流供电、有 SWD 备份恢复与物理断电条件的台架。该独立固件包不更新桌面工作台或 ARM64 安装包。

[固件 ZIP（865,091 字节）](https://github.com/maganrobotics-boop/OmindOS-Navigation-Release/releases/download/dm-mc02-bench-v0.1.0-preview.1/omindos-dm-mc02-bench-0.1.0-preview.1.zip) 包含 ELF/HEX/BIN、静态验证证据、重建说明和许可证；开发源码与 overlay 需访问授权开发仓。[验证记录](assets/dm-mc02-bench-v0.1.0-preview.1/VALIDATION.json)

## 保留版本：控制预览 0.2.0-preview.5

[发行页](https://github.com/maganrobotics-boop/OmindOS-Navigation-Release/releases/tag/v0.2.0-preview.5) · [安装与使用](docs/CONTROL_PREVIEW_5.zh-CN.md)

Linux amd64 编译运行包，包含参数 API、三维调参、ROS 2 关节预览与原版 MEVIUS2 四足闭环仿真。需安装 Docker Engine，Python、ROS 2 和仿真依赖已打包。模型、参数及网页资源保留，后端业务源码不随包提供。

| 功能 | 状态 |
| --- | --- |
| URDF 与电机参数提交、校验、版本保存 | 已提供 |
| 三维运动学调参 | 已提供 |
| ROS 2 参数加载和关节轨迹预览 | 已验证 |
| 原版 MEVIUS2 四足闭环仿真及 ROS 接口 | 已验证 |
| Jetson ARM64 安装包 | 软件候选包已发布；Jetson 实测待完成 |
| DM-MC02 固件、RS04 角度适配、客户实机验收 | 待完成 |

三维调参轨迹预览与四足策略进程为独立功能。本包不包含旧版统一导航 Docker 镜像。

[验证记录](assets/v0.2.0-preview.5/VALIDATION.json)：110 项编译模块回归、4 项动力学场景及 18 项四足 ROS 检查通过。[安装验证](assets/v0.2.0-preview.5/INSTALLATION_CHECK.json)

[完整安装包（约 820 MB）](https://omindos.cn/downloads/navigation/v0.2.0-preview.5/omindos-control-preview-0.2.0-preview.5-linux-amd64.tar) · [SHA256](assets/v0.2.0-preview.5/SHA256SUMS-release.txt)

GitHub 自动生成的 Source code 压缩包包含发行资料与固件二进制，不含后端业务源码。第三方软件保留各自许可，见 [THIRD_PARTY.md](THIRD_PARTY.md) 与安装包内许可证。

## 四足 ARM64 软件预览

[ARM64 Release](https://github.com/maganrobotics-boop/OmindOS-Navigation-Release/releases/tag/v0.2.0-arm64-preview.2) · [ARM64 安装与范围](docs/ARM64_PREVIEW_2.zh-CN.md)

原生 ARM64 软件验证通过；Jetson 实机安装与 RS04 实机联调仍待完成。此 ARM64 预览不启用电机输出，也不包含上述独立 DM-MC02 台架固件。

2026-10-08 更新：PR #10 的三路 CAN 只读接收、USB STATUS 与故障锁存代码已合并（6bcc8ad）。ARM64 preview.2 更新编译版主机协议模块，并附通信软件验证结果：42 项测试、8 个 Cortex-M7 对象编译/可重定位链接及 ARM64 镜像验证通过。安装包不含可烧录 DM-MC02 固件，尚缺板级 RNG、RTOS 接线、完整链接和实机验收；禁止电机使能。详见 [preview.2 安装与验收范围](docs/ARM64_PREVIEW_2.zh-CN.md)。原 [ARM64 preview.1](https://github.com/maganrobotics-boop/OmindOS-Navigation-Release/releases/tag/v0.2.0-arm64-preview.1) 及 amd64 preview.5 保持不变。

## 历史发行版

以下版本从 Omind-Robotics 原发行仓保留，原版本号、附件与 SHA256 保留；说明按原发行时的功能范围保存。

| 版本 | 内容与适用范围 | 使用说明 |
| --- | --- | --- |
| [v0.2.0-preview.2](https://github.com/maganrobotics-boop/OmindOS-Navigation-Release/releases/tag/v0.2.0-preview.2) | 统一导航预览＋参数注册 API、URDF／电机配置与版本保存；约 265 MB 离线包 | [完整说明](history/v0.2.0-preview.2/README.md) |
| [v0.2.0-preview.1](https://github.com/maganrobotics-boop/OmindOS-Navigation-Release/releases/tag/v0.2.0-preview.1) | 轮式／四足统一导航接口与平面运动学预览；约 265 MB 离线包 | [完整说明](history/v0.2.0-preview.1/README.md) |

历史 preview.1／preview.2 的完整安装包沿用原下载服务器链接；原 GitHub 附件同步保留。两版不含四足步态和平衡控制，详细范围见各自发行说明。同名标签指向本仓库的归档文档快照，原始标签提交记录在各版 `ORIGIN.json` 和发行页中。
