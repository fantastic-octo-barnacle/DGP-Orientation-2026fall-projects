# Python 同步服务端

完成内容见[公共同步服务端任务](../../../common/tasks.md#同步服务端)，开发检查见 [Python 工具链](../README.md#工具链与检查)。

在本目录启动：

```bash
uv sync --locked
uv run rm-server --host 127.0.0.1 --port 7878
```

`src/text_service/server.py` 使用 FastAPI/Uvicorn 处理 HTTP：异步依赖读取请求体，普通 `def` 处理函数在线程池中调用 `service.py` 的同步业务。不保证请求串行执行。HTTP 验证见[验收清单](../../../common/acceptance.md)。
