# Python 同步客户端

完成内容见[公共同步客户端任务](../../../common/tasks.md#同步客户端)。开发环境、检查命令和启动命令见 [Python 路线](../README.md)，必须在本目录执行。

## 代码结构

| 路径 | 职责 |
| --- | --- |
| `src/text_service/client.py` | 解析 `--url`、维护登录令牌、发送 HTTP 请求并处理交互循环 |
| `tests/test_client.py` | 客户端请求与响应处理测试 |

## 开发说明

从 `client.py` 的 `exchange()` 和 `main()` 开始。`exchange()` 负责构造请求并解析 JSON 响应；`main()` 负责命令输入、登录令牌保存和错误提示。实现任务时优先扩展命令分派和请求体构造，保持 HTTP 细节集中在 `exchange()`。

本项目使用同步 httpx 客户端，不需要引入异步代码。启动后的操作见[共通交互](../../../common/tasks.md#共通交互)。
