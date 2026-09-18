# WSL2 共通指引

阅读概念并完成自检，实践按设备条件安排：

- 使用 Windows 且设备条件允许：完成 WSL2 实践。
- 使用 macOS、原生 Linux，或 Windows 设备条件受限：完成概念学习和自检。

编程项目可在支持其工具链的 Windows、WSL2、macOS 或 Linux 环境中完成。

## 资料与学习目标

从微软的 [WSL 介绍](https://learn.microsoft.com/windows/wsl/about)与[安装指南](https://learn.microsoft.com/windows/wsl/install)开始，根据自己的系统版本确认条件。

需要区分 Windows、WSL、WSL2、Linux 内核和发行版，理解两侧的软件、用户目录、路径与运行环境分别存在。

## Windows 设备实践

1. 安装并启动一个 Linux 发行版；已有环境可直接启动。确认当前终端运行在哪个环境。
2. 定位当前目录和用户目录，练习创建、复制、移动和读取普通文件。
3. 在 Windows 创建文本文件，从 WSL 找到并读取；再反向练习。
4. 判断同一个工具在 Windows 与 WSL 中是否都已安装。
5. 理解退出 shell、关闭终端窗口与关闭 WSL 的区别，练习正常退出和关闭环境。

## 自检与项目应用

- 为什么 Windows 已安装 Python，WSL 中仍可能找不到？
- Windows 盘符与 Linux 路径如何对应？
- 项目依赖应在运行项目的哪一侧安装？
- 退出 shell、关闭终端窗口与关闭 WSL 分别会发生什么？

运行项目时，先确认终端所在环境，再安装工具和依赖。

完成后按[仓库首页](../README.md)选择编程项目。
