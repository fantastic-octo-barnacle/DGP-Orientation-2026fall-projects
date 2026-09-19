# Python 同步服务端

完成内容见[公共同步服务端任务](../../../common/tasks.md#同步服务端)，开发检查见 [Python 工具链](../README.md#工具链与检查)。

在本目录启动：

```bash
uv sync --locked
uv run rm-server --host 127.0.0.1 --port 7878
```

`src/text_service/server.py` 使用 Flask 处理 HTTP，`service.py` 管理业务状态。HTTP 验证见[阶段自查](../../../common/self-check.md)。
