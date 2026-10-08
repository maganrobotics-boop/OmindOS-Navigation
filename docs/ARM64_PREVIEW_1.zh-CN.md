# OmindOS 四足 ARM64 软件预览

Linux ARM64 编译候选包，供 ARM64 Docker 环境进行软件验证。后端业务源码和客户参数记录不随包提供。

已验证：原生 ARM64 编译模块导入、ROS 2 rclpy 导入、Torch CPU 运算和 MuJoCo 仿真步进。DM-MC02 便携通信核心通过 20 项测试及 Cortex-M7 编译，但本附件不包含可烧录的完整板卡固件。

Jetson ARM64 真机安装、DM-MC02 USB/CAN 板级适配及 RS04 实机联调仍待完成。电机输出未启用；步态、平衡及控制频率未经实机验收。

规划接口：Jetson 经 USB 下发关节目标，DM-MC02 经三路 CAN 控制 12 个 RS04，初步每路 4 个关节；频率待带宽核算及实测。

附件 omindos-control-arm64-candidate.tar 为完整安装候选包（521,502,720 字节）。SHA256：`32066d2b5baf3830a75d0ac099a76b892ddc21f585881e1cfbcc9bec253d1a46`。

安装包保留构建时的 candidate 名称及原控制预览版本信息。GitHub 的 Source code 附件仅包含发行资料。

## 安装与验证

需要 Linux ARM64 主机和 Docker Engine。下载 TAR 与 SHA256SUMS-release.txt 后运行：

```bash
sha256sum -c SHA256SUMS-release.txt
tar -xf omindos-control-arm64-candidate.tar
cd omindos-control-arm64-candidate
cat README.zh-CN.md
```

按包内说明使用 `./omindos` 启动软件仿真。启动器核对主机架构、镜像校验值及镜像 ID；默认不映射电机设备。此版本不支持实机电机输出。
