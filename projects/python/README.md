# Python 本地工具服务

本项目难度较低，适合编程基础较弱、刚学完变量、分支、循环和函数等基础语法的同学。你将从已有程序开始，学习阅读代码、添加功能、校验输入和验证修改。项目采用同步通信，围绕文本统计、数值统计和内存键值存取展开。

## 基线和任务

| 阶段 | 已提供 | 你需要完成 |
|---|---|---|
| 运行与理解 | 完整通信、文字客户端、ping/echo、环境及检查配置 | 运行两端，追踪一次请求 |
| 基础：文本统计 | 服务端 text_stats 和测试 | 客户端多行输入、请求构造、结果显示及测试 |
| 标准：数值统计 | 协议要求与少量样例 | 两端 number_stats、参数校验、错误显示和测试 |
| 进阶：键值存取 | 协议要求与少量样例 | 两端 set/get/delete/list，验证跨请求状态 |

详细字段和边界见[协议](protocol.md)，完成要求见[验收清单](acceptance.md)。保留错误处理，由服务端完成业务计算，客户端负责输入、发送请求和显示结果。

## 配置环境并检查起始代码

安装 [uv](https://docs.astral.sh/uv/getting-started/installation/)。在个人仓库根目录打开终端，执行 `cd projects/python`，再运行：

```text
uv sync --locked
uv run pytest
uv run ruff format --check .
uv run ruff check .
uv run pyright
```

项目指定 Python 3.12，uv 可获取对应解释器。清单声明依赖，uv.lock 固定解析版本，.venv 是本机可重建环境。依赖变更后应更新锁文件，.venv 通过忽略规则保留在本机。

## 第一次运行

终端 A：从个人仓库根目录执行 `cd projects/python`，启动服务端：

```text
uv run rm-server --port 7878
```

看到 `LISTENING 127.0.0.1:7878` 后，保持终端 A 运行。终端 B：同样进入 `projects/python`，启动客户端：

```text
uv run rm-client --port 7878
```

在终端 B 输入 `1` 并回车，应看到包含 `"ok": true` 和 `"data": "pong"` 的响应。再输入 `2`，按提示输入 `hello`，应收到 `"data": "hello"`。JSON 字段顺序可以不同。

输入 `q` 退出客户端。保持服务端运行，在终端 B 执行：

```text
uv run python self-check/check.py baseline
uv run python self-check/check.py text
```

看到两项 `PASS` 表示起始服务端自查通过。最后在终端 A 按 Ctrl-C 停止服务端。

服务端在当前客户端退出后才处理下一个连接。端口被占用时换一个端口，并同步修改服务端、客户端和自查命令的 `--port`。

## 读代码的路线

- `client.py`：菜单、请求构造、响应显示。
- `transport.py`：按行读取和长度边界。
- `protocol.py`：请求处理、响应解析与字段检查。
- `server.py`：接受连接与循环收发。
- `tests/`：已有能力的测试。
- `self-check/`：[阶段自查](self-check/README.md)。

先追踪一次 echo，再研究 text_stats 的服务端输入和返回值。新增功能怎样组织、修改哪些文件，由你依据行为目标决定。

## 验证与成果

基线检查应全部通过。每个阶段在保留基线行为的基础上增加测试，结合[通用参考程序](../../reference/README.md)替换一端排查问题。[成果说明](../../common/deliverables.md)列出需要保留的材料。

可选 CI：运行 pytest、Ruff 和 Pyright。
