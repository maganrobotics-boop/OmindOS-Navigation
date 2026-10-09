# 四足动力学仿真：Ubuntu 完整运行包

[返回首页](../README.md)

**要观察四足起身、站立、行走、转向或受到扰动后的表现，选择完整仿真包。** 它包含 ROS 2 Humble、PyTorch CPU、MuJoCo 和固定版本的 MEVIUS2 模型 / 策略，需先安装 Docker Engine。

| 想体验的功能 | 轻量工作台 | 完整仿真包 |
| --- | --- | --- |
| 三维查看、URDF 和关节参数编辑 | 有 | 有 |
| 关节运动学预览 | 有 | 有 |
| ROS 2 参数和关节预览 | 需另行启动独立服务 | 有 |
| 足端接触、步态与扰动动力学场景 | 无 | 有，使用 MEVIUS2 仿真 |
| 客户真实整机验收 | 尚未完成 | 尚未完成 |

## 下载

**[下载 Ubuntu 完整仿真包（540.42 MB）](https://github.com/maganrobotics-boop/OmindOS-Navigation-Release/releases/download/v0.2.0-preview.6/omindos-control-preview-0.2.0-preview.5-size-candidate.1-linux-amd64.tar)**

[SHA256 校验文件](../assets/v0.2.0-preview.6/SHA256SUMS-release.txt) · [发行记录](https://github.com/maganrobotics-boop/OmindOS-Navigation-Release/releases/tag/v0.2.0-preview.6)

适用于 Intel / AMD 64 位 Ubuntu 电脑。Ubuntu 22.04 构建、Ubuntu 24.04 浏览器和 ROS 联调已有软件验证；Jetson 使用[独立 ARM64 包](JETSON.zh-CN.md)。

## 启动工作台与验证

```bash
sha256sum -c SHA256SUMS-release.txt --ignore-missing
tar -xf omindos-control-preview-0.2.0-preview.5-size-candidate.1-linux-amd64.tar
```

进入解压后的目录（包含 `omindos` 启动器），运行：

```bash
./omindos workbench
```

浏览器访问 `http://127.0.0.1:8085/`。动力学验证另开终端执行：

```bash
./omindos validate-dynamics
```

闭环仿真的策略进程和 ROS 桥分别启动：

```bash
# 终端一
./omindos quadruped

# 终端二
./omindos quadruped-ros
```

按[四足闭环仿真使用说明](CONTROL_PREVIEW_5.zh-CN.md#四足闭环仿真)操作待机、起身、站立与行走。三维调参轨迹预览与四足策略进程是独立功能，工作台按钮不会自动启动该策略。

软件验证已有前向、横向、转向和站立横向扰动四组动力学场景。仿真使用 MEVIUS2 参考模型；客户机器人的尺寸、惯量、电机与控制参数仍须按实际硬件设置和验证。本包不含旧版统一导航 Docker 镜像，也不含 DM-MC02 可烧录固件。

[完整安装与版本说明](CONTROL_PREVIEW_6.zh-CN.md) · [软件验证记录](../assets/v0.2.0-preview.6/VALIDATION.json)
