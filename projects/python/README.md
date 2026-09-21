# Python 路线

任务范围与推进顺序见[公共任务说明](../../common/tasks.md)。本页是 Python 项目的开发说明，集中说明同语言项目共用的工具链、目录结构、检查命令和启动方式。

语言学习和资料查询方法见 [Python 学习指引](learning.md)。

## 开发环境

- 使用 Python 3.13 与 uv。
- 每个任务目录都是独立项目，各有 `pyproject.toml`、`uv.lock` 和本地环境。
- 依赖和开发工具由锁文件固定；除非任务明确要求，不要手工改锁文件或混用不同任务目录的环境。
- 以下命令都必须在具体任务目录中运行。

安装依赖：

```bash
uv sync --locked
```

提交前依次执行检查：

```bash
uv run pytest
uv run ruff check .
uv run ruff format --check .
uv run pyright
```

## 代码结构

所有 Python 项目都使用 `src/text_service` 包和 `tests/` 测试目录：

| 路径 | 职责 |
| --- | --- |
| `src/text_service/client.py` | 客户端命令行参数、HTTP 请求和交互循环 |
| `src/text_service/server.py` | 服务端命令行参数、应用组装和启动入口 |
| `src/text_service/service.py` | 服务端业务规则、用户状态和文本状态 |
| `src/text_service/_http.py` | 同步服务端的 FastAPI/Uvicorn 适配层 |
| `tests/` | 单元测试和 HTTP 测试 |

服务端项目共享同一个基本分层：`service.py` 实现业务和状态，`server.py` 负责应用组装与启动。同步服务端通过 `_http.py` 把 HTTP 请求转成同步业务调用；异步服务端在 `server.py` 中使用 `async def` 处理请求，并用 `asyncio.to_thread` 隔离密码计算等阻塞工作。两层都必须保护共享状态，不能假设请求会串行执行。

## 运行命令

先在对应任务目录执行 `uv sync --locked`，再使用下表命令：

| 目录 | 启动命令 |
| --- | --- |
| `client-sync/` | `uv run rm-client --url http://127.0.0.1:7878` |
| `server-sync/` | `uv run rm-server --host 127.0.0.1 --port 7878` |
| `server-async/` | `uv run rm-server --host 127.0.0.1 --port 7878` |

启动后的操作见[共通交互](../../common/tasks.md#共通交互)，完成情况按[公共任务说明](../../common/tasks.md#收尾与交付)验证。
