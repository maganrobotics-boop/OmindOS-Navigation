# OmindOS DM-MC02 禁使能台架固件 0.1.0-preview.1

[返回首页](../README.md)

**仅供嵌入式开发者进行禁使能台架验证，普通电脑体验无需下载。** 这是烧入 DM-MC02 板卡的固件，不是 Ubuntu 桌面安装包；先阅读下方首次上板条件。

**[下载完整固件 ZIP（0.87 MB）](https://github.com/maganrobotics-boop/OmindOS-Navigation-Release/releases/download/dm-mc02-bench-v0.1.0-preview.1/omindos-dm-mc02-bench-0.1.0-preview.1.zip)**

ZIP 包含 ELF / HEX / BIN、静态验证证据、重建说明和许可证。[SHA256 校验](../assets/dm-mc02-bench-v0.1.0-preview.1/SHA256SUMS-release.txt) · [发行页和单文件下载](https://github.com/maganrobotics-boop/OmindOS-Navigation-Release/releases/tag/dm-mc02-bench-v0.1.0-preview.1)

这是 STM32H723 / DM-MC02 的只读观察台架预发布，**真实硬件尚未验收**。
三路 FDCAN 从首次初始化起使用 BUS_MONITORING；TX 分配为零，不发送数据帧，也不提供 ACK。
不包含电机使能、运动目标发送或厂家电机测试任务。软件 STOP 仅锁存本机会话，不能替代硬件断电。

| 阶段 | 结果 |
|---|---|
| 软件编译与完整链接 | 47 项单元测试、44 个 Cortex-M7 对象、179 个向量检查通过；无未解析符号或禁用发送符号；固件和 ARM64 CI 均通过 |
| 可烧录格式生成 | 已生成 ELF/HEX/BIN 和 SHA256；本地重复构建三种格式逐字节一致；BIN 31,392 字节，AXI 静态 RAM 29,128 字节，MSP 预留 8 KiB |
| 真实硬件验收 | 未进行；无刷写、USB 枚举、CAN 收帧、时钟/RNG或任务栈实测记录 |

源码合并：[开发 PR #18](https://github.com/Omind-Robotics/OmindOS-Navigation/pull/18)，
合并提交 `3293dfc83e32b8e56f1f185b80e19e56a2fe600d`；构建目标提交 `f7d4fcad30622e6e1fc71ff1702fa894c1fe0c57`。
[完整构建 CI](https://github.com/Omind-Robotics/OmindOS-Navigation/actions/runs/37918128866)
与 [ARM64/协议 CI](https://github.com/Omind-Robotics/OmindOS-Navigation/actions/runs/37918128745)。
开发仓可能需要授权访问。本公开包提供二进制、校验值、静态验证证据和许可证；重建需要对应开发源码。

厂家工程固定为 `dmBots/DM-MC02@d65a3688981405dc205f628f1a026bde8cf8303e`，原始工程未修改。
RNG HAL 固定 `b716379524ba3549e4db11804889776ffeb239d1`；FreeRTOS GCC port 固定 `88e32327e975ddde97c390bc5b6c1f8e7d9d239e`。
ARM GCC 13.2.1；具体重建命令、内存布局、已知限制见 ZIP 中 README.zh-CN.md 与 VALIDATION.json。

首次上板条件：

1. 核对实际 MCU、板卡 revision、24 MHz HSE、Flash/RAM 与 SWD 电平；备份并核验厂家 Flash、option bytes、bootloader，确认恢复流程。
2. 核实应用入口确为 `0x08000000`。存在 bootloader 或保留区时，先修改启动/链接布局并重建；不能直接使用本包覆盖。
3. 断开全部电机动力/输出，使用限流控制板供电和物理断电手段；核对电源开关、CAN 收发器供电与使能极性。
4. 先通过 SWD 验证时钟、RNG/nonce、TIM23、FreeRTOS tick/任务循环与栈余量，再验证 USB 查询及失败锁存。本包没有独立硬件 watchdog。
5. 使用能提供 ACK 的 CAN 测试节点逐路注入已知帧，核对终端/接地/1 Mbit/s和本板无发送；通过后再接一个禁使能 RS04并核对实际 ID。

默认三路各四个 ID 仅是预期路由，尚未验收；无标定、限位或整机运动控制保证。
固件预发布不替换现有桌面工作台或 ARM64 软件版本。
