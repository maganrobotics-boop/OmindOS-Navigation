# OmindOS 四足 ARM64 软件预览 0.2.0-arm64-preview.2

更新到已合并的三路 CAN 只读接收与 USB 状态诊断开发基线。安装包内包含更新后的编译版主机协议模块；STM32 接收代码保留在私有开发仓，**本包不包含可烧录 DM-MC02 固件，不启用电机输出**。

软件验证通过：20 个 ARM64 编译模块导入、ROS 2、CPU Torch、MuJoCo 步进；42 项通信测试（含 39 个 CAN HAL 故障模拟场景），8 个 Cortex-M7 对象编译及可重定位链接。所有结果均为软件验证。

三路接收开发采用 BUS_MONITORING，无 CAN 发送或 ACK；可解析 RS04 类型 2/17/21，并区分未收到、新鲜、过期和故障锁存。参数帧仅是被动观察，尚未完成实机参数请求—应答验收。

本包发行时，板级 RNG、RTOS 接线和完整固件链接仍待完成。**2026-10-09 项目进展：这些软件缺口已在独立 DM-MC02 台架固件中补齐，ELF/HEX/BIN 已发布**，见[固件说明与上板条件](DM_MC02_BENCH_PREVIEW_1.zh-CN.md)。本 ARM64 安装包不包含该固件，附件及 SHA256 保持原样。

仍待完成：实际刷写、Jetson 实机安装、三路 CAN 电气验收及 RS04 联调。控制频率、客户整机步态和平衡尚未实测。

[安装与范围说明](https://github.com/maganrobotics-boop/OmindOS-Navigation-Release/blob/main/docs/ARM64_PREVIEW_2.zh-CN.md)

完整安装包 `omindos-control-arm64-candidate.tar`：521,543,680 字节；SHA256：`3c110db4b626082a7a88fa1c5b10c1791d6ae1b52ae307cbd921b2890173e0d4`。

需 Linux ARM64 + Docker Engine。后端业务源码和客户记录不随包提供；第三方许可证保留在包内。安装包保留 candidate 名称和原控制预览版本信息，以 MANIFEST.json 的 source_commit 与 IMAGE_ID.txt 识别精确构建。GitHub 自动生成的 Source code 附件仅包含发行资料。

构建快照 `e9caaf904553380609836c03f02be8df8ab982e4` 与合并提交 `6bcc8ad5e22e26bab869b48a849b31cf63f8afeb` 的源码树相同（`b3f308ba0486712c0aa92bb6481c48a5c1761b12`）。preview.1 和 amd64 preview.5 保持不变。

## 安装

```bash
sha256sum -c SHA256SUMS-release.txt
tar -xf omindos-control-arm64-candidate.tar
cd omindos-control-arm64-candidate
cat README.zh-CN.md
./omindos workbench
```

浏览器访问 http://localhost:8085；ROS 参数预览使用 `./omindos ros-preview`。原版 MEVIUS2 仿真按包内说明使用 `./omindos quadruped` 与 `./omindos quadruped-ros`。启动器默认不映射 USB/CAN 电机设备。

## 首次硬件验收顺序

1. 核对 DM-MC02 revision、RS04 固件/协议/ID，建立可恢复刷写工程，保持电机不使能。
2. 先独立验证板卡时钟、RNG nonce、HAL tick、RTOS 栈和任务调度，再测试 Jetson USB PROBE/STATUS、拔插及超时。
3. 核对三路 CAN 引脚、共地、收发器和终端；由另一正常 CAN 节点提供测试帧与 ACK，逐路确认板卡只监听。
4. 注入已知状态、错误帧、队列积压及断流，对照 CAN/USB 抓包；再用保持不使能的单个 RS04 验证真实状态和参数回复，逐步扩至 12 个。
5. 验证硬件看门狗、掉电/断连行为，并根据总线占用和最坏延迟确定控制周期。

这些步骤均尚未记录为通过。通过非使能通信验收后，仍须独立开展单关节标定、使能和整机运动验收。
