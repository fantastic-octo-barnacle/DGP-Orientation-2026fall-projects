# Python 学习指引

通用学习方法见[前言](../../common/preface.md)。本页只补充 Python 路线的常用资料入口，以及查询语法、标准库、工具和框架 API 的方法；不要求从第一页读到最后一页。

## 资料入口

| 需要查询的内容 | 推荐入口 | 用途 |
| --- | --- | --- |
| Python 入门和常用语法 | [Python Tutorial](https://docs.python.org/3/tutorial/) | 通过小例子了解语法、数据结构和标准用法 |
| 语义、作用域、异常等语言规则 | [Language Reference](https://docs.python.org/3/reference/) | 查清楚某个语言行为为什么要这样执行 |
| 标准库模块和内置函数 | [Standard Library Reference](https://docs.python.org/3/library/) | 查模块、函数、类、异常和版本变化 |
| 类型标注 | [`typing` 文档](https://docs.python.org/3/library/typing.html) | 理解起始代码和 pyright 检查中的类型写法 |
| 依赖、环境和锁文件 | [uv 文档](https://docs.astral.sh/uv/) | 理解 `uv sync`、`uv run`、`uv.lock` 和项目环境 |
| HTTP 客户端 | [httpx 文档](https://www.python-httpx.org/) | 查客户端请求、JSON、超时和异常处理 |
| Web 框架 | [FastAPI 文档](https://fastapi.tiangolo.com/) | 查路由、请求体、响应和测试客户端用法 |
| ASGI 服务器 | [Uvicorn 项目](https://github.com/encode/uvicorn) | 查项目 README、配置说明和运行行为 |
| 测试 | [pytest 文档](https://docs.pytest.org/en/stable/) | 查测试函数、参数化、断言和失败输出 |
| 代码检查与格式化 | [Ruff 文档](https://docs.astral.sh/ruff/) | 理解 lint 规则、格式化行为和自动修复建议 |
| 静态类型检查 | [Pyright 文档](https://microsoft.github.io/pyright/) | 理解类型错误、配置和诊断 |

这些入口以官方文档和本项目直接使用的工具文档为主。看到博客、教程或讨论时，可以把它当作理解路径，但结论应回到当前版本的官方文档和项目测试验证。

## 如何查文档

1. 先判断问题属于哪一层：Python 语法、标准库、第三方库、测试工具，还是项目自身逻辑。查错层级能减少无效检索。
2. 检索时带上准确的符号名、函数名和完整报错，例如 `httpx.Client request timeout`、`pytest parametrize`，不要只搜笼统的“Python 报错”。
3. 查 API 时至少看四件事：函数或类签名、参数默认值、返回值或异常、示例代码。不要只复制示例而不确认适用条件。
4. 本项目使用 Python 3.13。阅读资料时注意版本差异，避免混用 Python 2 或旧版本的写法。
5. 遇到 `pyright` 或 `ruff` 报告时，先看诊断信息和规则名，再查对应工具文档；不要只为了消除提示而改变类型或关闭检查。
6. 文档结论回到项目验证：用一个最小测试、REPL 或现有测试确认行为，再决定是否采用。

## 与项目的对应关系

| 项目内容 | 优先查阅 |
| --- | --- |
| `argparse`、`getpass` 和交互循环 | Python Tutorial、Standard Library Reference |
| httpx 请求、超时和异常 | httpx 文档 |
| FastAPI 请求、路由和响应 | FastAPI 文档 |
| Uvicorn 启动参数 | Uvicorn 项目 |
| 类型标注和 pyright 诊断 | `typing` 文档、Pyright 文档 |
| pytest 测试组织与断言 | pytest 文档 |
| 锁、线程和异步阻塞隔离 | Python Standard Library Reference 中 `threading`、`asyncio` 相关章节 |

工具链、检查命令和启动命令见 [Python 路线](README.md)。
