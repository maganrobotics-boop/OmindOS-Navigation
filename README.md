# OmindOS 控制预览 0.2.0-preview.5

[发行页](https://github.com/maganrobotics-boop/OmindOS-Navigation-Release/releases/tag/v0.2.0-preview.5) · [安装与使用](docs/CONTROL_PREVIEW_5.zh-CN.md)

Linux amd64 编译运行包，包含参数 API、三维调参、ROS 2 关节预览与原版 MEVIUS2 四足闭环仿真。需安装 Docker Engine，Python、ROS 2 和仿真依赖已打包。模型、参数及网页资源保留，后端业务源码不随包提供。

| 功能 | 状态 |
| --- | --- |
| URDF 与电机参数提交、校验、版本保存 | 已提供 |
| 三维运动学调参 | 已提供 |
| ROS 2 参数加载和关节轨迹预览 | 已验证 |
| 原版 MEVIUS2 四足闭环仿真及 ROS 接口 | 已验证 |
| Jetson ARM64 安装包 | 待完成 |
| DM-MC02 固件、RS04 角度适配、客户实机验收 | 待完成 |

三维调参轨迹预览与四足策略进程为独立功能。本包不包含旧版统一导航 Docker 镜像。

[验证记录](assets/v0.2.0-preview.5/VALIDATION.json)：110 项编译模块回归、4 项动力学场景及 18 项四足 ROS 检查通过。[安装验证](assets/v0.2.0-preview.5/INSTALLATION_CHECK.json)

[完整安装包（约 820 MB）](https://omindos.cn/downloads/navigation/v0.2.0-preview.5/omindos-control-preview-0.2.0-preview.5-linux-amd64.tar) · [SHA256](assets/v0.2.0-preview.5/SHA256SUMS-release.txt)

GitHub 自动生成的 Source code 压缩包只包含发行资料。第三方软件保留各自许可，见 [THIRD_PARTY.md](THIRD_PARTY.md) 与安装包内许可证。
