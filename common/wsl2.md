# WSL2 共通指引

无论选择哪个项目，使用 Windows 且设备条件允许的候选人都应理解并实践本指引。macOS 和原生 Linux 使用者无需安装 WSL2。已经配置好者不必重装；设备受限时可先理解概念，项目也不强制在 WSL 中完成。

## 资料与学习目标

从微软的 [WSL 介绍](https://learn.microsoft.com/windows/wsl/about)与[安装指南](https://learn.microsoft.com/windows/wsl/install)开始，根据自己的系统版本确认条件。

需要区分 Windows、WSL、WSL2、Linux 内核和发行版，理解两侧的软件、用户目录、路径与运行环境分别存在。

## 实践

1. 安装并启动一个 Linux 发行版，知道当前终端运行在哪个环境。
2. 定位当前目录和用户目录，练习创建、复制、移动和读取普通文件。
3. 在 Windows 创建文本文件，从 WSL 找到并读取；再反向练习。
4. 判断同一个工具在 Windows 与 WSL 中是否都已安装。
5. 理解退出 shell、关闭终端窗口与关闭 WSL 的区别，能正常退出和关闭环境。

自检：为什么 Windows 已安装 Python，WSL 中仍可能找不到？Windows 盘符与 Linux 路径如何对应？项目依赖应在运行项目的哪一侧安装？

不要求配置 Vim、Docker、systemd、复杂权限或 shell 脚本，不单独收集截图、日志或仓库。
