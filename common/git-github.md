# Git 与 GitHub 共通指引

## 准备与资料

- 从 [Git 官方网站](https://git-scm.com/downloads)安装 Git，确认能查看版本。
- 学习 [Git/GitHub 入门教程](https://www.bilibili.com/video/BV1Hkr7YYEh8)。
- 其他资料：[Git 基础](https://fantastic-octo-barnacle.github.io/The-Book-of-EC/nodes/engineering/git-basics/intro.html)、[Git 与 GitHub](https://fantastic-octo-barnacle.github.io/The-Book-of-EC/nodes/engineering/git-remote/intro.html)

## 自检与项目应用

学完教程后，应能回答以下问题：

- 工作目录、暂存区、本地提交和远程仓库分别是什么？
- `commit` 与 `push` 有什么区别？
- `.gitignore` 的作用是什么？如何判断哪些文件需要忽略？
- 为什么忽略规则不能删除已有历史？

**在后续项目中持续使用这些操作，保留自然的迭代历史**；通用要求见[公共任务说明](tasks.md#任务顺序)。
提交前检查差异，用忽略规则排除虚拟环境、`target` 和缓存，并将令牌及个人凭证保存在仓库外。排查问题时，结合所用命令、工作目录和原始报错定位原因。
