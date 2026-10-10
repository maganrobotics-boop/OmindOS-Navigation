# OmindOS Navigation · Ubuntu 0.2.0-preview.8

本版默认打开 OriginMind 四足机器狗 V1.1 装配 R1，更新 12 轴几何零位、运动映射和可导出的标定表。

- 补齐两条前腿的摇臂、压盖、螺栓及传动杆轴承组件；修正右后摇臂组件。共 988 个显示实例，保留原 STEP/GLB，用可追溯变换复用源几何。
- 全部 12 轴可做几何联动预览；支持逐腿调角、转轴显示、停止和恢复修正零位。
- 标定表含模型版本与逐轴几何定义。电机方向、编码器零位和机械限位保留待真机回读，未完成硬件标定。
- 参数页保留当前 URDF、配置版本及原 MEVIUS2 参考功能。CAD 操作不下发电机命令。
- Ubuntu 完整包重新编译后端，包含工作台、ROS 2、PyTorch CPU、MuJoCo 与四足参考环境。无需登录。

## 安装

适用 Ubuntu 22.04 / 24.04、Intel/AMD x86_64；需要预先安装 Docker Engine，且当前用户可以执行 docker。

下载并完整解压 `omindos-navigation-0.2.0-preview.8-ubuntu-amd64.tar`，执行：

```bash
./install.sh
"$HOME/.local/opt/omindos-navigation/0.2.0-preview.8/omindos" workbench
```

打开 http://127.0.0.1:8085/ 。既有配置保存在 `~/.local/share/omindos-navigation/data`，沿用；旧包内 data 可通过 OMINDOS_DATA_DIR 指定。

## 验证范围

编译态 79 项工作台回归、3 项参考资源回归；完整包重新解压到新目录、全新导入镜像并启动。安装后 CAD 浏览器 21 项检查，原参数页点动/停止回归，以及 4 个 MEVIUS2 动力学场景通过。几何验证覆盖 5,292 组角度与原始网格孔轴变换。

本版属于预览发行。169 个附件归属仍待完整配合复核，整机紧固件 BOM、全行程干涉、V1.1 接触动力学和真实电机未验收。MEVIUS2 的参考动力学结果不代表 V1.1 的实机结果。后端业务源代码不包含在安装包内。

校验哈希见 SHA256SUMS-release.txt；安装、浏览器、几何及参考动力学报告随发行提供。旧版本附件保留。
