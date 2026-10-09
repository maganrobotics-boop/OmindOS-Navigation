# OmindOS Navigation · Ubuntu 完整安装包 0.2.0-preview.7

只需下载 `omindos-navigation-0.2.0-preview.7-ubuntu-amd64.tar`，其中包含工作台、本地参数 API、ROS 2、PyTorch、MuJoCo 和四足策略参考环境。适用于 Ubuntu Intel / AMD 64 位电脑，需要预装 Docker Engine。

本版修复最终运行环境缺少 SciPy 导致的工作台启动失败，以及普通用户无法读取四足仿真参考文件的问题。新界面默认加载完整四足参考外观，包含 13 个网格和 12 个关节，可按客户硬件导入 URDF 并编辑参数。

## 安装和启动

完整解压后执行：

```bash
./install.sh
"$HOME/.local/opt/omindos-navigation/0.2.0-preview.7/omindos" workbench
```

打开 http://127.0.0.1:8085/ ，无需登录。也可在解压目录直接执行 `./omindos workbench`。配置默认保存在 `~/.local/share/omindos-navigation/data`；使用旧版本包内的数据时，通过 `OMINDOS_DATA_DIR` 指向原 `data/`，旧配置不覆盖。

## 验收

- 复用通过 79 项编译工作台回归和 3 项参考资源测试的固定编译模块。
- 最终安装归档重新解压，删除构建镜像后重新安装；含空格路径的安装脚本通过。
- 实际安装包 HTTP 访问、WebGL 完整外观、13/13 网格、12 个关节、参数写入、0.1° 点动与软件停止通过。
- 普通用户运行前进、横移、转向和站立扰动四组接触动力学场景通过。
- 后端业务程序以编译形式交付，应用业务源码和客户私有记录未包含。
- 安装包大小和 SHA256 见 `RELEASE_SUMMARY.json` 与 `SHA256SUMS-release.txt`。

本版仍为软件预览；三维调参与四足策略仿真是独立功能。真实机器人、电机驱动和客户硬件未验收。轮式导航独立环境、Jetson 与板卡固件见专业指南。Windows 暂缓。
