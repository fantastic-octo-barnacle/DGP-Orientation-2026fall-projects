# RM 软件组个人项目

完成 [Git/GitHub](common/git-github.md) 与 [WSL2](common/wsl2.md) 共通任务，再选择 Python 或 Rust 项目。两个项目都提供可运行的起始代码，你将在此基础上增加功能、编写测试，并用 Git 记录修改。

## 选择项目

两个项目都实现 HTTP 用户文本服务：注册登录、个人文本存取、令牌过期，以及同步和异步服务端。

| | Python | Rust |
|---|---|---|
| 难度 | 较低，适合刚学完基础语法、项目经验较少的同学 | 较高，适合能独立编写简单程序、希望进一步挑战的同学 |
| 学习重点 | 功能扩展、接口、状态管理和异步编程 | 在相同业务上进一步学习所有权、共享状态和异步生命周期 |
| 入口 | [Python 项目](projects/python/README.md) | [Rust 项目](projects/rust/README.md) |

两者都包含 client-sync、server-sync、server-async 三个独立项目，提供相同的基线功能。只需选择一种语言完成。

## 开始与交付

1. 点击 GitHub 的 **Use this template → Create a new repository**，创建个人仓库。
2. 完成共通任务，阅读所选项目说明和协议，运行起始代码与测试。
3. 按阶段完善功能和测试，在个人仓库提交修改。
4. 对照验收清单，整理[成果说明](common/deliverables.md)要求的代码和文档。

## 仓库地图

- `common/`：工程基础指引、成果要求和通用 HTTP 自查工具。
- `projects/python/`：三个 Python 项目、协议和验收说明。
- `projects/rust/`：三个 Cargo 项目、协议和验收说明。
- `reference/`：[参考程序使用说明](reference/README.md)。
