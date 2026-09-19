# Python 路线

任务范围与推进顺序见[公共任务说明](../../common/tasks.md)。本页只说明 Python 工具链与代码入口。

## 工具链与检查

使用 Python 3.13 与 uv。每个任务目录都有独立的 `pyproject.toml`、`uv.lock` 和环境。在对应目录运行：

```bash
uv sync --locked
uv run pytest
uv run ruff check .
uv run ruff format --check .
uv run pyright
```

## 运行入口

| 目录 | 起始代码入口 | 启动说明 |
| --- | --- | --- |
| `client-sync/` | `src/text_service/client.py` | [同步客户端](client-sync/README.md) |
| `server-sync/` | `src/text_service/server.py`、`service.py`，FastAPI/Uvicorn | [同步服务端](server-sync/README.md) |
| `server-async/` | `src/text_service/server.py`、`service.py`，FastAPI/Uvicorn | [异步服务端](server-async/README.md) |

从 HTTP 入口进入业务处理函数，理解身份检查、密码计算与状态锁之间的关系。启动后的操作见[共通交互](../../common/tasks.md#共通交互)，完成情况按[验收清单](../../common/acceptance.md)验证。
