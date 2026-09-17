# 通用协议参考程序

参考程序作为已知可工作的通信对端，帮助验证自己的客户端或服务端。它实现 ping、echo、delay、text_stats、number_stats、set/get/delete/list，按所选项目范围使用；不需要实现所有动作。

## 获取与校验

从本仓库的 [reference-v1.0.0 Release](https://github.com/fantastic-octo-barnacle/DGP-Orientation-2026fall-projects/releases/tag/reference-v1.0.0) 下载对应平台：

- Windows x86-64：`rm-recruit-reference-windows-x86_64.exe`
- Linux x86-64：`rm-recruit-reference-linux-x86_64`
- macOS Apple Silicon：`rm-recruit-reference-macos-arm64`

同时下载 SHA256SUMS。Windows 可用 Get-FileHash，Linux 用 sha256sum，macOS 用 shasum -a 256，核对文件名与校验值。Unix 系统需赋予执行权限。macOS 若阻止下载的程序，先核实来源、架构与校验值，依据系统官方说明处理。

当前只发布可执行文件，完整参考源码不在本仓库。程序可离线运行，只监听本机地址。具体可用版本以 Release 为准。

## 启动

以下以 Linux 文件名示意；Windows 使用 `.\rm-recruit-reference-windows-x86_64.exe`，macOS 使用对应文件名。

```text
./rm-recruit-reference-linux-x86_64 --version
./rm-recruit-reference-linux-x86_64 server --bind 127.0.0.1:7878
./rm-recruit-reference-linux-x86_64 client --address 127.0.0.1:7878
```

服务端支持连续交互及多个连接；Ctrl-C 触发有界退出。客户端从标准输入读取原始 JSON，每行发送一个请求并显示一个响应，EOF 退出。它不会替你构造协议请求。查看 `server --help`、`client --help` 获取配置。

```json
{"id":1,"action":"ping"}
{"id":2,"action":"echo","data":"hello"}
{"id":3,"action":"text_stats","text":"hi\nRM"}
```

默认客户端响应期限 12,000 ms、服务端完整请求读取期限 30,000 ms、退出宽限 2,000 ms；均支持命令行配置。等待期间超时会关闭该连接。

## 如何定位问题

- 自己的客户端连接参考服务端：验证请求构造、错误显示和响应处理。
- 参考客户端连接自己的服务端：直接输入所选项目协议中的请求，验证处理结果。
- 起始服务端仅支持已有动作；未完成动作返回 unknown_action 是预期状态。
- 协议结果以所选项目 protocol.md 为准；错误说明文字不必逐字相同。
- 自查脚本与参考程序都不是完整测试答案，仍需自行验证边界和界面。
