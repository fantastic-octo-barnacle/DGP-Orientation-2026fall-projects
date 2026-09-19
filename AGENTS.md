# 候选人项目维护指引

本仓库面向候选人公开，维护任务说明、起始代码与自查工具。修改前检查 `git status --short --branch`，保留已有改动。

## 文档归属

- 调整路线、层级或推进顺序时，阅读并修改 [common/tasks.md](common/tasks.md)。
- 调整接口、状态、边界或生命周期时，阅读 [common/protocol.md](common/protocol.md)，同步检查[验收清单](common/acceptance.md)与 `common/check_http.py`。
- 调整语言工具链或启动方式时，修改对应 [Python](projects/python/README.md) 或 [Rust](projects/rust/README.md) 入口及任务目录说明；共同要求使用链接引用。
- 调整自查命令、成果要求或参考程序说明时，分别修改 [self-check.md](common/self-check.md)、[deliverables.md](common/deliverables.md)、[reference-programs.md](common/reference-programs.md)。

公共文档对两条语言路线共同生效。语言目录不维护另一份任务或协议；验收清单组织验证场景，数值和接口定义以协议为准。

## 公开边界与起始代码

保持本仓库独立可用，文档链接不依赖其他仓库的私有文件。这里提供可运行的起始代码；未经明确要求，不把留给候选人的任务补成完整答案。参考程序从公开 Release 分发，源代码和构建产物不作为起始代码提交。

公开内容不包含个人信息、凭据、隐藏测试、内部评分或面试记录。引用下载内容时区分实际可用资产和计划支持的平台，不把规划写成已发布事实。

## 验证

文档变更检查相对链接、锚点、命令工作目录和公开边界。代码变更按对应语言入口的检查命令验证，并检查公共规范与起始能力描述是否仍准确；起始状态使用 baseline，自查的后续阶段按[适用条件](common/self-check.md)运行。Python 使用 uv，Rust 使用 Cargo，维护各独立项目的锁文件。
