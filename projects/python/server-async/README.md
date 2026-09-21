# Python 异步服务端

完成内容见[公共异步服务端任务](../../../common/tasks.md#异步服务端)。开发环境、检查命令和启动命令见 [Python 路线](../README.md)，必须在本目录执行。

## 代码结构

| 路径 | 职责 |
| --- | --- |
| `src/text_service/service.py` | 业务规则、用户状态和文本状态 |
| `src/text_service/server.py` | `async def` 请求处理、应用组装、命令行入口和阻塞工作调度 |
| `tests/test_service.py` | 业务逻辑测试 |
| `tests/test_http.py` | HTTP 层测试 |

## 开发说明

`service.py` 继续承载同步业务逻辑和状态锁；`server.py` 负责异步请求处理，并用 `asyncio.to_thread` 把密码计算等可能阻塞的操作移出事件循环。实现时注意区分“可以直接在事件循环中完成的轻量逻辑”和“必须放到工作线程的阻塞逻辑”，并保持共享状态保护正确。

HTTP 验证见[验收清单](../../../common/acceptance.md)。
