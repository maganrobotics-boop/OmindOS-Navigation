OmindOS 0.2.0-preview.5 提供参数 API、三维调参、ROS 2 关节预览与原版 MEVIUS2 四足闭环仿真。

[完整 Linux amd64 安装包（约 820 MB）](https://omindos.cn/downloads/navigation/v0.2.0-preview.5/omindos-control-preview-0.2.0-preview.5-linux-amd64.tar) · [详细使用说明](https://github.com/maganrobotics-boop/OmindOS-Navigation-Release/blob/main/docs/CONTROL_PREVIEW_5.zh-CN.md)

需要 Linux x86_64 和 Docker Engine。Python、ROS 2 Humble、MuJoCo 与 PyTorch 已打包。

```bash
sha256sum -c SHA256SUMS-release.txt
tar -xf omindos-control-preview-0.2.0-preview.5-linux-amd64.tar
cd omindos-control-preview-0.2.0-preview.5-linux-amd64
./omindos workbench
```

浏览器访问 http://127.0.0.1:8085，按“URDF → 电机 → 其他参数”配置并保存。可选 ./omindos ros-preview 加载 ROS 2 关节轨迹预览；./omindos validate-dynamics 运行四项原版 MEVIUS2 动力学仿真。三维调参轨迹预览和四足策略进程是独立功能。

验证：110 项编译模块回归、9 项 ROS 参数加载、10 项浏览器检查、4 项动力学场景、18 项四足 ROS 检查通过。新包独立解压、镜像导入和启动验证通过；源站全量 SHA256 与公开下载首/中/末范围核验通过。

后端业务程序以编译模块交付，模型、参数、网页资源与第三方依赖保留。包内不包含私人客户配置。当前包不包含旧版统一导航 Docker 镜像。

**本版是 Linux amd64 开发预览；Jetson ARM64、DM-MC02 通信固件、RS04 角度协议适配和客户整机步态、平衡及实机验收仍未完成。** 未连接或使能真实电机，工作台默认不启动 ROS 控制进程。

完整包：820449280 字节。
SHA256：276b666a8fee186ba839c30bda8676baba4125a7c9e51408f07ed596cc9db5cc。
业务构建快照：df829a312dd571e19a3f0d65dcdc2b576f6d4a6d。
GitHub 自动生成的 Source code 压缩包仅包含发行资料；请使用完整安装包。
