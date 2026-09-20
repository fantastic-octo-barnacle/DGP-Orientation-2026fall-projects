# Python 同步服务端

完成内容见[公共同步服务端任务](../../../common/tasks.md#同步服务端)，开发检查见 [Python 工具链](../README.md#工具链与检查)。

在本目录启动：

```bash
uv sync --locked
uv run rm-server --host 127.0.0.1 --port 7878
```

从 `src/text_service/service.py` 的同步业务开始，更新其中的 `ROUTES`、`route_error` 和 `Service.handle` 来扩展接口。`src/text_service/server.py` 提供同步的应用组装与命令行入口；增加令牌期限时，在这里解析参数、构造带配置的 `Service`，再传给 `create_app(service)`。业务配置与有效期逻辑留给候选人实现。

`tests/test_http.py` 使用同步的 `TestClient`，上下文管理器负责应用启动与关闭。完成本层任务无需编写 `async/await`，也无需修改基础设施模块 `src/text_service/_http.py`；它负责 FastAPI/Uvicorn 的 HTTP 适配、请求体读取与日志。同步业务在线程池中执行，不保证请求串行执行，仍须保护共享状态。异步层单独学习异步处理与阻塞工作隔离。HTTP 验证见[验收清单](../../../common/acceptance.md)。
