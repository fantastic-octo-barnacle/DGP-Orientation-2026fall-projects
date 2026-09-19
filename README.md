# RM 软件组个人项目

这是 2026 秋季软件组招新的候选人项目仓库。项目主题是 HTTP 用户文本服务：阅读起始代码和协议，自学缺少的知识，补齐功能、测试和说明。

## 从这里开始

1. 使用 GitHub 的 **Use this template → Create a new repository** 创建个人仓库。
2. 完成 [Git/GitHub](common/git-github.md) 与 [WSL2](common/wsl2.md) 共通学习任务。
3. 阅读[公共任务说明](common/tasks.md)，了解路线选择、任务层级与推进顺序。
4. 进入 [Python 路线](projects/python/README.md)或 [Rust 路线](projects/rust/README.md)，安装工具链并运行起始代码。
5. 按[参考程序使用说明](common/reference-programs.md)选择可用的对接程序，逐步实现并验证任务。
6. 对照[验收清单](common/acceptance.md)检查，按[成果说明](common/deliverables.md)整理交付。

## 文档地图

| 内容 | 唯一维护位置 |
| --- | --- |
| 路线选择、任务范围、起始能力、共通交互 | [公共任务说明](common/tasks.md) |
| HTTP 接口、状态、输入边界、并发和生命周期要求 | [统一协议](common/protocol.md) |
| 验证场景与检查方法 | [验收清单](common/acceptance.md) |
| HTTP 自查工具及阶段命令 | [阶段自查](common/self-check.md) |
| 下载、平台选择、版本匹配与运行参考程序 | [参考程序](common/reference-programs.md) |
| 提交历史、测试说明、已知限制与交付文档 | [成果说明](common/deliverables.md) |
| 语言工具链、运行命令与代码入口 | [Python](projects/python/README.md)、[Rust](projects/rust/README.md) |

`common/` 中的要求对两条路线共同适用；语言目录只解释实现环境与运行方式。维护本仓库的 agent 请先阅读 [AGENTS.md](AGENTS.md)。
