# OmindOS Navigation 0.2.0-preview.6 · 四足轻量工作台与完整仿真包

本次将已验收的构建候选原样晋升为新的公开预览发行版。既有 preview.5 和 ARM64 发行版保持不变。

| 下载 | 精确字节 | 约 MB（十进制） | 功能与安装依赖 |
| --- | ---: | ---: | --- |
| [完整 Linux amd64 包](https://github.com/maganrobotics-boop/OmindOS-Navigation-Release/releases/download/v0.2.0-preview.6/omindos-control-preview-0.2.0-preview.5-size-candidate.1-linux-amd64.tar) | 540,416,000 | 540.42 | 参数 API、工作台、ROS 2 Humble、PyTorch CPU、MuJoCo 和 MEVIUS2 闭环仿真；需 Docker Engine |
| [轻量 Linux x64 工作台](https://github.com/maganrobotics-boop/OmindOS-Navigation-Release/releases/download/v0.2.0-preview.6/omindos-quadruped-workbench-0.2.0-size-candidate.1-linux-x64.tar.gz) | 21,990,166 | 21.99 | 独立三维调参和运动学预览；无需另装 Python、ROS、Node 或 Docker |
| [轻量 Windows x64 工作台](https://github.com/maganrobotics-boop/OmindOS-Navigation-Release/releases/download/v0.2.0-preview.6/omindos-quadruped-workbench-0.2.0-size-candidate.1-windows-x64.zip) | 8,232,521 | 8.23 | 同上；未签名 |

完整包由 820,449,280 字节降至 540,416,000 字节，减少 **34.13%**。清理 pip/apt 缓存和构建用 Cython/wheel，重新生成干净镜像层；ROS、策略推理、动力学依赖及 71 个业务/模型文件保持一致。

轻量工作台复用机械臂桌面的 Nuitka 编译发行机制。默认是明确标注的 12 关节合成教学模型，可导入实际 URDF；不包含接触、步态和平衡仿真。新 Linux 桌面与独立完整包 ROS 2 服务的真实 DDS 联调已通过。

**版本说明：**安装包保留已验收的原始文件名、内容和 SHA256，因此名称仍含 `size-candidate.1`。完整包内业务版本仍显示 `0.2.0-preview.5`，桌面为 `0.2.0-size-candidate.1`。随包 README 的“候选/未发布”及“联调待完成”表述是构建时快照，当前发布状态及验收范围以本发行说明和所附 VALIDATION.json 为准。本次没有重新编译或重打包。

验证：Windows/Linux 各 45 项源码测试、打包前后各 15 项可执行检查；Linux 浏览器预览检查；完整包 110 项编译回归、9 项 ROS 参数检查、18 项四足 ROS 检查和 4 组动力学场景；新桌面与独立 ROS 服务另有 9 项联调检查；完整包解压、21 项文件清单校验、docker load 与启动器验证通过。

未验收：Jetson ARM64、Windows ROS/WSL、客户 RS04 整机动力学及真实电机。此发行不包含可烧录固件或真机驱动验收。

[安装与兼容性](https://github.com/maganrobotics-boop/OmindOS-Navigation-Release/blob/main/docs/CONTROL_PREVIEW_6.zh-CN.md) · [校验值](https://github.com/maganrobotics-boop/OmindOS-Navigation-Release/releases/download/v0.2.0-preview.6/SHA256SUMS-release.txt)

后端业务程序仅以编译形式交付；网页、模型、参数与第三方依赖及许可证保留。GitHub 自动生成的 Source code 附件只包含发行资料和发布脚本。
