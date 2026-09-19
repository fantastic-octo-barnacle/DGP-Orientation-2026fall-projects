# RM 软件组个人项目

这是 2026 秋季软件组招新的候选人项目仓库。项目主题是用一种自己选择的语言完成 HTTP 用户文本服务：你需要阅读已有代码和协议，自学缺少的知识，在起始代码上补齐功能、测试和说明。

## 选择路线

Python 和 Rust 是两条等价路线。除语言和工具链不同外，任务层级、协议、验收要求和最终行为完全一致。

| 路线 | 入口 | 工具链 |
| --- | --- | --- |
| Python | [Python 项目](projects/python/README.md) | Python 3.12、uv |
| Rust | [Rust 项目](projects/rust/README.md) | 稳定版 Rust、Cargo |

每条路线都包含三个同名层级：`client-sync`、`server-sync`、`server-async`。

## 项目层级

| 层级 | 要求 |
| --- | --- |
| 客户端 | 必做。完成同步交互式 HTTP 客户端，可以使用 Release 中的完整服务端进行对接。 |
| 同步服务端 | 可选的中间层。可以先完成它再进入异步版本；如果认为自己能直接处理异步代码，也可以跳过。 |
| 异步服务端 | 必做的最终服务端。可以使用自己的客户端或 Release 中的完整客户端进行对接。 |

服务端基础业务完成后，再实现令牌过期。异步服务端还需要处理并发、非阻塞等待和有界退出。完整任务见[统一协议](common/protocol.md)和[统一验收清单](common/acceptance.md)。

本仓库只提供候选人可见的任务说明和起始代码。完整参考程序通过 [GitHub Releases](https://github.com/fantastic-octo-barnacle/DGP-Orientation-2026fall-projects/releases) 提供，不公开参考实现源码。

## 开始与交付

1. 点击 GitHub 的 **Use this template → Create a new repository**，创建个人仓库。
2. 完成 [Git/GitHub](common/git-github.md) 与 [WSL2](common/wsl2.md) 共通任务。
3. 选择 Python 或 Rust，阅读对应入口说明，运行起始代码和基线测试。
4. 下载参考程序：完整服务端用于客户端层级，完整客户端用于两个服务端层级。
5. 按层级完善功能、测试和文档，保留自然的 Git 提交历史。
6. 对照[统一验收清单](common/acceptance.md)和[成果说明](common/deliverables.md)整理项目。

最终至少应完成客户端和异步服务端。同步服务端可以完成，也可以在成果说明中注明跳过。

## 仓库地图

- `common/`：两条路线共用的协议、验收、工程指引和 HTTP 自查工具。
- `projects/python/`：Python 三个层级的起始代码和运行说明。
- `projects/rust/`：Rust 三个层级的起始代码和运行说明。

## 参考程序

参考程序是与协议兼容的完整可执行程序，不是候选人的代码模板：

- `rm-client-sync`：用于测试 Python 或 Rust 服务端；
- `rm-server-async`：用于测试 Python 或 Rust 客户端。

当前只提供 Windows x86_64 构建。参考程序不能替代你对所选语言项目的测试、理解和说明。
