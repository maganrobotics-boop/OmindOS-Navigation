# OmindOS 四足 ARM64 软件预览 0.2.0-arm64-preview.2

更新到已合并的三路 CAN 只读接收与 USB 状态诊断开发基线。安装包内包含更新后的编译版主机协议模块；STM32 接收代码保留在私有开发仓，**本包不包含可烧录 DM-MC02 固件，不启用电机输出**。

软件验证通过：20 个 ARM64 编译模块导入、ROS 2、CPU Torch、MuJoCo 步进；42 项通信测试（含 39 个 CAN HAL 故障模拟场景），8 个 Cortex-M7 对象编译及可重定位链接。所有结果均为软件验证。

三路接收开发采用 BUS_MONITORING，无 CAN 发送或 ACK；可解析 RS04 类型 2/17/21，并区分未收到、新鲜、过期和故障锁存。参数帧仅是被动观察，尚未完成实机参数请求—应答验收。

仍待完成：板级 RNG 初始化、RTOS 任务接线、完整固件链接/刷写、Jetson 实机安装、三路 CAN 电气验收及 RS04 联调。控制频率、客户整机步态和平衡尚未实测。

[安装与范围说明](https://github.com/maganrobotics-boop/OmindOS-Navigation-Release/blob/main/docs/ARM64_PREVIEW_2.zh-CN.md)

完整安装包 `omindos-control-arm64-candidate.tar`：521,543,680 字节；SHA256：`3c110db4b626082a7a88fa1c5b10c1791d6ae1b52ae307cbd921b2890173e0d4`。

需 Linux ARM64 + Docker Engine。后端业务源码和客户记录不随包提供；第三方许可证保留在包内。安装包保留 candidate 名称和原控制预览版本信息，以 MANIFEST.json 的 source_commit 与 IMAGE_ID.txt 识别精确构建。GitHub 自动生成的 Source code 附件仅包含发行资料。

构建快照 `e9caaf904553380609836c03f02be8df8ab982e4` 与合并提交 `6bcc8ad5e22e26bab869b48a849b31cf63f8afeb` 的源码树相同（`b3f308ba0486712c0aa92bb6481c48a5c1761b12`）。preview.1 和 amd64 preview.5 保持不变。
