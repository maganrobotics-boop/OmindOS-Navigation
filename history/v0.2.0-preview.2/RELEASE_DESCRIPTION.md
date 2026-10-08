参数注册 API 已发布：客户提交 URDF 与电机参数，即可校验、保存并获得配置编号；按编号读取，重复提交幂等，更新保留旧版本，无需修改系统源码。

[完整 Linux amd64 安装包（约 265 MB）](https://omindos.cn/downloads/navigation/v0.2.0-preview.2/omindos-navigation-0.2.0-preview.2-linux-amd64.tar) · [SHA256 校验文件](https://omindos.cn/downloads/navigation/v0.2.0-preview.2/SHA256SUMS-release.txt)

完整包包含原 preview.1 导航镜像、三平台预览、新参数 API、客户说明、配置与合成调用样例。导航镜像保持原样；这是参数接口与统一导航预览更新。开发 PR #1 已合并，合并提交 `6c6b7cdabc4af63bf4dc1c570b58a775a0d3b626`，参数源码提交 `71d10388982139a06dc0d8722a68a2efc6e0f7e1`。

```bash
tar -xf omindos-navigation-0.2.0-preview.2-linux-amd64.tar
cd omindos-navigation-0.2.0-preview.2
./omindos verify
./omindos install
./omindos test
./omindos api --store "$HOME/omindos-robot-configurations" --port 8085
```

需要 Linux x86_64、Docker、Python 3.10+ 和 Bash。API 使用标准库，仅监听 127.0.0.1；客户配置目录独立于安装目录，升级时沿用。API 调用字段见仓库 docs/ROBOT_PARAMETER_API.zh-CN.md。附件 `parameter-api-source.tar.gz` 是可单独运行 API 的源码包，不含导航 Docker 环境；GitHub 自动生成的 Source code 也不是完整离线安装包。

验证：13 项参数/配置测试、20 项导航测试通过；差速、全向、四足机身速度预览均完成到达和连续零指令；完整包独立解压/镜像导入、HTTP 参数提交、幂等、服务重启后读取新旧配置，以及篡改拒绝检查通过。MEVIUS2 的既有 20 秒原版仿真记录与复现脚本包含在包内，未当作本次 API 联调结果。

**本版尚未接通 ROS 2 控制端配置激活，不包含三维调参界面，也未完成真实机器人运动控制验收。** `runtime_applied` 与 `hardware_validated` 保持 false。MEVIUS2 模型、策略权重、MuJoCo/PyTorch 依赖未打入此包。

完整包：265492480 字节；SHA256：`b08c5dd9e0f65ec278d1c9fea68254af3c687c260d74ebe52d92d774ee68a03b`。
参数源码 SHA256：`da52a43e29895467469a548f18d2c01ecddc66f3f97d978385f1309c8a82e2da`。
旧版标签、镜像和资产未改动。

下载核验补充：源站 HTTPS 全量文件校验通过，公开地址 HEAD 与首/中/末字节范围核验通过。GitHub 托管节点连接外部下载服务器时发生 TLS 重置，因此参数源码直接作为 GitHub 附件提供；完整安装包仍由 OmindOS 下载服务器提供。见附件 DOWNLOAD_CHECK.json。
