同一个 Linux amd64 离线包提供差速轮式、全向轮式和四足机身速度三种配置，共用 ROS 2 Humble 导航接口、速度限制与超时停机逻辑。

**本版为导航接口与平面运动学预览，不含四足步态、平衡或真实硬件驱动，未完成实机验收。**

[下载完整离线安装包（约 265 MB）](https://omindos.cn/downloads/navigation/v0.2.0-preview.1/omindos-navigation-0.2.0-preview.1-linux-amd64.tar) · [SHA256 校验文件](https://omindos.cn/downloads/navigation/v0.2.0-preview.1/SHA256SUMS-release.txt)

完整 Docker 安装包托管在 OmindOS 下载服务器；下方 GitHub 附件提供应用源码、校验文件及验证报告。GitHub 自动生成的 Source code 压缩包不是离线安装包。

在已安装 Docker 的 Linux x86_64 主机执行：

```bash
sha256sum -c SHA256SUMS-release.txt
tar -xf omindos-navigation-0.2.0-preview.1-linux-amd64.tar
cd omindos-navigation-0.2.0-preview.1
./omindos install
./omindos test
./omindos preview quadruped
```

轮式使用 `wheeled_diff` 或 `wheeled_omni`。完整使用说明、实际应用源码、许可证、测试结果和校验文件均在包内。

验证：20 项测试通过；三种平台均完成目标到达并持续输出零指令超过 1 秒；独立解压、Docker 导入、镜像 ID 校验通过；篡改文件在 Docker 调用前被拒绝。全部 16 层路径检查未发现本次排除的历史应用目录。

完整包：265,287,680 字节。
SHA256：`cb5977638d80635bc0bc8002bfdfae9e431f723fdf9e151c8c8a9e51c84e1a3f`。

项目负责人已于 2026-10-08 确认继承代码可对外发行；保留 Apache-2.0 声明、原维护者和修改说明。旧 v0.1 资产未修改。
