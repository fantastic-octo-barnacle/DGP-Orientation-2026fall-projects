# Python 同步客户端

完成内容见[公共同步客户端任务](../../../common/tasks.md#同步客户端)，开发检查见 [Python 工具链](../README.md#工具链与检查)。

在本目录启动：

```bash
uv sync --locked
uv run rm-client --url http://127.0.0.1:7878
```

请求与交互入口为 `src/text_service/client.py`。启动后的操作见[共通交互](../../../common/tasks.md#共通交互)。
