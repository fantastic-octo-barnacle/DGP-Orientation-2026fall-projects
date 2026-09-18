# 通用协议参考程序

参考程序作为已知可工作的通信对端，帮助验证自己的客户端或服务端。它实现 ping、echo、delay、text_stats、number_stats、set/get/delete/list，按所选项目范围使用；不需要实现所有动作。

## 获取与校验

从原始交付仓库的 [reference-v1.0.0 Release](https://github.com/fantastic-octo-barnacle/DGP-Orientation-2026fall-projects/releases/tag/reference-v1.0.0) 下载对应平台：

- Windows x86-64：`rm-recruit-reference-windows-x86_64.exe`
- Linux x86-64：`rm-recruit-reference-linux-x86_64`
- macOS Apple Silicon：`rm-recruit-reference-macos-arm64`

同时下载 `SHA256SUMS`，与可执行文件放在同一目录。在该目录打开终端，执行适合当前环境的命令：

Windows PowerShell：

```powershell
Get-FileHash .\rm-recruit-reference-windows-x86_64.exe -Algorithm SHA256
Get-Content .\SHA256SUMS
```

Linux / WSL2 x86-64：

```sh
sha256sum rm-recruit-reference-linux-x86_64
cat SHA256SUMS
chmod +x rm-recruit-reference-linux-x86_64
```

macOS Apple Silicon：

```sh
shasum -a 256 rm-recruit-reference-macos-arm64
cat SHA256SUMS
chmod +x rm-recruit-reference-macos-arm64
```

计算结果应与 `SHA256SUMS` 中同名文件的值一致，十六进制字母大小写不影响比较。WSL2 中使用 Linux 版本，Windows PowerShell 中使用 Windows 版本。其他系统或架构目前没有对应的预编译文件。macOS 若阻止下载的程序，先核实来源、架构与校验值，再依据系统提示处理。

Release 位于原始交付仓库，个人模板仓库中不会自动出现这些下载文件。

当前只发布可执行文件，完整参考源码不在本仓库。程序可离线运行，只监听本机地址。具体可用版本以 Release 为准。

## 启动

以下以 Linux 文件名示意；Windows 使用 `.\rm-recruit-reference-windows-x86_64.exe`，macOS 使用对应文件名。

```text
./rm-recruit-reference-linux-x86_64 --version
./rm-recruit-reference-linux-x86_64 server --bind 127.0.0.1:7878
./rm-recruit-reference-linux-x86_64 client --address 127.0.0.1:7878
```

服务端支持连续交互及多个连接；Ctrl-C 触发有界退出。客户端从标准输入读取原始 JSON，每行发送一个请求并显示一个响应。请自行输入下面的 JSON 请求。结束输入时，Windows 终端按 Ctrl-Z 后回车，Linux/macOS 在空行按 Ctrl-D；也可用 Ctrl-C 结束程序。查看 `server --help`、`client --help` 获取配置。

```json
{"id":1,"action":"ping"}
{"id":2,"action":"echo","data":"hello"}
{"id":3,"action":"text_stats","text":"hi\nRM"}
```

第一次验证可以在终端 A 启动参考服务端，再在同一目录的终端 B 启动参考客户端。输入第一条 ping 请求并回车，应收到 `{"id":1,"ok":true,"data":"pong"}`，字段顺序可以不同。随后退出客户端，在终端 A 按 Ctrl-C 停止服务端。

验证个人代码时，用参考服务端替换自己的服务端，或用参考客户端替换自己的客户端。同一端口只启动一个服务端。起始服务端的连接行为以所选项目说明为准。

默认客户端响应期限 12,000 ms、服务端完整请求读取期限 30,000 ms、退出宽限 2,000 ms；均支持命令行配置。服务端在等待下一条请求时也会计时，输入停顿超过期限后需要重新连接。手动练习时可提高读取期限，例如 Linux 下执行：

```text
./rm-recruit-reference-linux-x86_64 server --bind 127.0.0.1:7878 --read-timeout-ms 120000
```

Windows/macOS 使用相应文件名和启动方式，其余参数相同。验收默认行为时使用协议规定的默认值。

## 如何定位问题

- 自己的客户端连接参考服务端：验证请求构造、错误显示和响应处理。
- 参考客户端连接自己的服务端：直接输入所选项目协议中的请求，验证处理结果。
- 起始服务端仅支持已有动作；未完成动作返回 unknown_action 是预期状态。
- 协议结果以所选项目 protocol.md 为准；错误说明文字不必逐字相同。
- 自查脚本与参考程序都不是完整测试答案，仍需自行验证边界和界面。
