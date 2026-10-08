# OmindOS 控制预览 0.2.0-preview.5

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

GitHub 自动生成的 Source code 压缩包只包含发行资料。第三方软件保留各自许可，见 [THIRD_PARTY.md](THIRD_PARTY.md) 与安装包内许可证。

## 四足 ARM64 软件预览

[ARM64 Release](https://github.com/maganrobotics-boop/OmindOS-Navigation-Release/releases/tag/v0.2.0-arm64-preview.2) · [ARM64 安装与范围](docs/ARM64_PREVIEW_2.zh-CN.md)

原生 ARM64 软件验证通过；Jetson 实机安装、DM-MC02 完整通信固件与 RS04 实机联调仍待完成。此预览不启用电机输出。

2026-10-08 更新：PR #10 的三路 CAN 只读接收、USB STATUS 与故障锁存代码已合并（6bcc8ad）。ARM64 preview.2 更新编译版主机协议模块，并附通信软件验证结果：42 项测试、8 个 Cortex-M7 对象编译/可重定位链接及 ARM64 镜像验证通过。安装包不含可烧录 DM-MC02 固件，尚缺板级 RNG、RTOS 接线、完整链接和实机验收；禁止电机使能。详见 [preview.2 安装与验收范围](docs/ARM64_PREVIEW_2.zh-CN.md)。原 [ARM64 preview.1](https://github.com/maganrobotics-boop/OmindOS-Navigation-Release/releases/tag/v0.2.0-arm64-preview.1) 及 amd64 preview.5 保持不变。

## 历史发行版

以下版本从 Omind-Robotics 原发行仓保留，原标签、附件与 SHA256 不变；说明按原发行时的功能范围保存。

| 版本 | 内容与适用范围 | 使用说明 |
| --- | --- | --- |
| [v0.2.0-preview.2](https://github.com/maganrobotics-boop/OmindOS-Navigation-Release/releases/tag/v0.2.0-preview.2) | 统一导航预览＋参数注册 API、URDF／电机配置与版本保存；约 265 MB 离线包 | [完整说明](history/v0.2.0-preview.2/README.md) |
| [v0.2.0-preview.1](https://github.com/maganrobotics-boop/OmindOS-Navigation-Release/releases/tag/v0.2.0-preview.1) | 轮式／四足统一导航接口与平面运动学预览；约 265 MB 离线包 | [完整说明](history/v0.2.0-preview.1/README.md) |

历史 preview.1／preview.2 的完整安装包沿用原下载服务器链接；原 GitHub 附件同步保留。两版不含四足步态和平衡控制，详细范围见各自发行说明。
