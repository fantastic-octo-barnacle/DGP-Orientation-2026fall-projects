# Python 异步服务端

完成内容见[公共异步服务端任务](../../../common/tasks.md#异步服务端)，开发检查见 [Python 工具链](../README.md#工具链与检查)。

在本目录启动：

```bash
uv sync --locked
uv run rm-server --host 127.0.0.1 --port 7878
```

`src/text_service/server.py` 使用 FastAPI/Uvicorn 的 `async def` 处理 HTTP，通过 `asyncio.to_thread` 将密码计算等同步业务移出事件循环；`service.py` 管理业务状态。HTTP 验证见[验收清单](../../../common/acceptance.md)。
