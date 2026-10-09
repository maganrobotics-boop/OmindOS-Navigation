# 开发者 API：用自己的程序提交和读取参数

[返回首页](../README.md) · [工作台操作](WORKBENCH_USAGE.zh-CN.md)

**可以不经过图形界面调用 API。** 启动 Ubuntu 安装包的 `./omindos workbench` 后，本地 API 与工作台使用同一服务和配置存储。默认地址为 `http://127.0.0.1:8085`；当前本地接口不要求用户账号登录。

## 支持的配置接口

| 接口 | 用途 |
| --- | --- |
| `POST /v1/robot-profiles` | 提交 URDF 和电机参数，校验后保存版本 |
| `GET /v1/robot-profiles/{profile_id}` | 按完整配置编号读取已保存版本 |

相同参数重复提交得到相同编号；修改参数生成新的版本，旧编号仍可读取。服务重启后沿用同一数据目录即可继续读取。

## 最快的调用方式

先在工作台填写自己的参数，点击“导出完整配置”，获得 `robot-parameters.json`。这样无需手写整个 URDF JSON。

```bash
curl --fail-with-body \
  -X POST http://127.0.0.1:8085/v1/robot-profiles \
  -H 'Content-Type: application/json' \
  --data-binary @robot-parameters.json
```

用响应中的 `profile_id` 读取版本：

```bash
curl --fail-with-body \
  http://127.0.0.1:8085/v1/robot-profiles/PROFILE_ID
```

将 `PROFILE_ID` 替换为实际返回的完整配置编号。

## Python 示例

```python
import json
from pathlib import Path
from urllib.request import Request, urlopen

payload = Path('robot-parameters.json').read_bytes()
request = Request(
    'http://127.0.0.1:8085/v1/robot-profiles',
    data=payload,
    headers={'Content-Type': 'application/json'},
    method='POST',
)
with urlopen(request, timeout=10) as response:
    result = json.load(response)
print(result)
```

保存失败时，查看返回的校验错误，先补齐或修正字段。常见结构包含 `robot_id`、`kinematics.urdf_xml` 和 `dynamics.joints`；单位须与工作台字段一致。

## 调用范围

这些接口用于参数配置、版本保存和软件预览，不直接使能真实电机。配置保存成功不代表真实硬件已加载，也不代表客户整机动力学已验证。

当前接口默认只供**本机程序**使用；跨机器访问和云端用户认证没有在这个本地包中自动提供。导航和四足 ROS 2 运行接口的范围分别见[导航指南](NAVIGATION.zh-CN.md)与[四足仿真指南](QUADRUPED_SIMULATION.zh-CN.md)。

[完整参数字段说明](../history/v0.2.0-preview.2/docs/ROBOT_PARAMETER_API.zh-CN.md) · [客户硬件参数填写指南](../history/v0.2.0-preview.2/docs/CUSTOMER_ROBOT_CONFIGURATION.zh-CN.md)
