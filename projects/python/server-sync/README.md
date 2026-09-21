# Python 同步服务端

完成内容见[公共同步服务端任务](../../../common/tasks.md#同步服务端)。开发环境、检查命令和启动命令见 [Python 路线](../README.md)，必须在本目录执行。

## 代码结构

| 路径 | 职责 |
| --- | --- |
| `src/text_service/service.py` | 路由表、业务规则、用户状态和文本状态 |
| `src/text_service/server.py` | 命令行参数、`Service` 构造和 FastAPI 应用组装 |
| `src/text_service/_http.py` | FastAPI/Uvicorn 适配、请求体读取与日志 |
| `tests/test_service.py` | 业务逻辑测试 |
| `tests/test_http.py` | HTTP 层测试 |

## 开发说明

主要从 `service.py` 的 `ROUTES`、`route_error()` 和 `Service.handle()` 开始扩展接口。增加令牌期限时，在 `server.py` 解析配置并构造带配置的 `Service`，再传入 `create_app(service)`；业务配置与有效期逻辑由候选人实现。

`tests/test_http.py` 使用同步 `TestClient`，上下文管理器负责应用启动与关闭。完成本层任务无需编写 `async/await`，通常也不需要修改 `_http.py`。同步业务在线程池中执行，仍须保护共享状态。HTTP 验证见[验收清单](../../../common/acceptance.md)。
