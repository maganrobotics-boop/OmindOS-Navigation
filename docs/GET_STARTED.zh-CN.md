# Ubuntu 安装包：下载一次，打开工作台

[返回首页](../README.md)

**普通用户只需下载这一个完整安装包。** 工作台、参数 API、ROS 2、PyTorch CPU、MuJoCo 与四足策略 / 参考模型都在包内，无需另外下载工作台或算法包。

## 1. 确认电脑

Ubuntu 22.04 / 24.04，Intel / AMD 64 位电脑。在终端执行 `uname -m`，应显示 `x86_64`。文件名中的 `amd64` 和 `x64` 都指这类架构，不要求 AMD 品牌处理器。Jetson 的 `aarch64` 架构属于[高级部署](DEVELOPER.zh-CN.md)，不要下载 PC 包。

**需要预先安装 Docker Engine。** 工作台及算法环境运行在包内 Docker 镜像中；无需另外安装 Python、ROS、PyTorch 或 MuJoCo。没有 Docker 时，按 [Docker 官方 Ubuntu 安装说明](https://docs.docker.com/engine/install/ubuntu/)完成基础环境安装，再继续。用 `docker info` 确认当前账户可以访问 Docker 服务。

## 2. 下载并完整解压

**[下载 Ubuntu 完整安装包（540.42 MB）](https://github.com/maganrobotics-boop/OmindOS-Navigation-Release/releases/download/v0.2.0-preview.6/omindos-control-preview-0.2.0-preview.5-size-candidate.1-linux-amd64.tar)**

用文件管理器完整解压，或在下载目录执行：

```bash
tar -xf omindos-control-preview-0.2.0-preview.5-size-candidate.1-linux-amd64.tar
```

不要只复制其中的启动文件，配套镜像、模型和目录必须保留。需检查下载完整性时见[校验指南](DOWNLOAD_HELP.zh-CN.md)。

## 3. 打开工作台

进入解压后的目录，找到 `omindos` 文件，在该目录打开终端，运行：

```bash
./omindos workbench
```

首次启动会导入随包 Docker 镜像，需等待完成。在浏览器打开：

**http://127.0.0.1:8085/**

无需注册或登录。保持终端运行；结束时在终端按 `Ctrl+C`。工作台配置保存在包内 `data/`，升级前保留和备份该目录。

## 4. 设置自己的机器人

左侧导入 URDF / 完整配置，选择关节或连杆并修改参数。点击“将以上参数写入程序”，再保存版本和导出备份。具体字段、单位及按钮作用见[图文操作指南](WORKBENCH_USAGE.zh-CN.md)。

工作台根据导入的 URDF 显示机器人；示例参数不等于客户硬件标定值。修改参数只作用于当前工作台配置，不表示已写入真实电机。

## 5. 按需运行包内算法

只调参时，无需启动下面的功能。另开终端，在同一安装目录运行：

| 用途 | 命令 |
| --- | --- |
| ROS 2 关节与参数预览 | `./omindos ros-preview` |
| 四组动力学验证 | `./omindos validate-dynamics` |
| 四足策略进程 | `./omindos quadruped` |
| 四足 ROS 桥，需与策略同时运行 | `./omindos quadruped-ros` |

四足策略与 ROS 桥分别在两个终端运行。按[仿真使用指南](QUADRUPED_SIMULATION.zh-CN.md)体验待机、起身、站立、行走和停止。工作台的运动学按钮与策略进程是独立功能，前者不会自动启动后者。

## 当前范围

完整包不包含旧版统一导航 Docker 镜像，也不包含 DM-MC02 可烧录固件。真实底盘、Jetson、RS04 和客户整机仍需独立验收。需要这些开发用途时进入[专业指南](DEVELOPER.zh-CN.md)。

[精确版本、功能与兼容性](CONTROL_PREVIEW_6.zh-CN.md)
