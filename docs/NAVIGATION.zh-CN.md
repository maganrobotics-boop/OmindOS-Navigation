# 差速、全向与四足机身速度导航预览

[返回首页](../README.md)

**要测试三类平台共用的导航接口，选择统一导航预览包 `0.2.0-preview.2`。** 这个包保留 ROS 2 Humble 平面导航示例，并提供参数注册 API。较新的四足仿真发行包服务于另一用途，版本号更高不表示它包含本包的导航环境。

![三类平台：差速、全向、四足](media/platforms.svg)

| 平台 | 速度能力 | 启动配置 |
| --- | --- | --- |
| 差速轮式 | 前后、转向；禁止横移 | `wheeled_diff` |
| 全向轮式 | 前后、横移、转向 | `wheeled_omni` |
| 四足机身速度 | 同一导航核心和机身速度接口；平面预览 | `quadruped` |

这里的全向轮式指主动控制横移的底盘，普通随动脚轮不是独立平台类型。

## 下载

**[下载统一导航完整包（265.49 MB）](https://omindos.cn/downloads/navigation/v0.2.0-preview.2/omindos-navigation-0.2.0-preview.2-linux-amd64.tar)**

[SHA256 校验文件](https://omindos.cn/downloads/navigation/v0.2.0-preview.2/SHA256SUMS-release.txt) · [发行记录](https://github.com/maganrobotics-boop/OmindOS-Navigation-Release/releases/tag/v0.2.0-preview.2)

需要 Ubuntu / Linux x86_64、Docker Engine、Python 3.10+ 和 Bash。完整 Docker 镜像已在包内；验证和测试无需另行拉取镜像。

## 启动

```bash
sha256sum -c SHA256SUMS-release.txt
tar -xf omindos-navigation-0.2.0-preview.2-linux-amd64.tar
cd omindos-navigation-0.2.0-preview.2
./omindos verify
./omindos install
./omindos test
./omindos preview wheeled_diff
```

全向轮式改为 `./omindos preview wheeled_omni`；四足机身速度改为 `./omindos preview quadruped`。预览以日志呈现，`Ctrl+C` 停止；**本包没有三维工作台**。

## 能验证什么

三平台的目标到达、速度限制、超时与连续零指令检查，以及 URDF / 电机配置校验和版本保存。它是平面导航接口预览；不含真实底盘驱动、实测里程计，也不含四足步态、足端接触和平衡控制。参数 API 尚未激活到 ROS 2 控制端。

[完整安装和参数使用说明](../history/v0.2.0-preview.2/README.md) · [三平台配置与硬件验收范围](../history/v0.2.0-preview.2/docs/UNIFIED_CUSTOMER_RELEASE.zh-CN.md)
