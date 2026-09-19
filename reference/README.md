# HTTP 参考程序

参考程序用于替换通信的一端，验证请求和服务端行为。它用 Rust 实现完整 HTTP 用户文本服务，包括候选人需要完成的接口和令牌过期。

## 当前版本

本仓库提供 [Windows x86-64 可执行文件](bin/rm-http-reference-windows-x86_64.exe)，版本 0.2.0。旧 reference-v1.0.0 使用 TCP JSON 行协议，与本项目不兼容。

当前未提供 Linux/macOS 原生 HTTP 参考程序；这些平台可先用[HTTP 自查工具](../common/check_http.py)验证服务端。自查工具不提供参考服务端功能。

## 参考服务端

在本目录打开终端：

```powershell
.\bin\rm-http-reference-windows-x86_64.exe --version
.\bin\rm-http-reference-windows-x86_64.exe server --bind 127.0.0.1:7878
```

启动自己的客户端并连接 `http://127.0.0.1:7878`，验证注册、登录和后续操作。参考服务端在内存中保存数据，重启后清空。默认令牌有效期 300 秒；验证过期时使用 `--token-ttl-seconds 2`。

服务端支持并发，请求读取期限 30 秒，Ctrl-C 后最多等待在途请求 2 秒。每个 HTTP 连接处理一个请求后关闭，HTTP 客户端库会按需重新连接。

## 参考客户端

先启动自己的服务端，再使用参考客户端指定 HTTP 方法和路径：

```powershell
.\bin\rm-http-reference-windows-x86_64.exe client GET /ping
```

带 JSON 请求体时，可以将内容保存为 UTF-8 文件。例如 `account.json`：

```json
{"username":"alice","password":"password1"}
```

```powershell
.\bin\rm-http-reference-windows-x86_64.exe client POST /users --body-file account.json
.\bin\rm-http-reference-windows-x86_64.exe client POST /sessions --body-file account.json
.\bin\rm-http-reference-windows-x86_64.exe client GET /texts --token "复制登录响应里的令牌"
```

可用 `--url http://127.0.0.1:7878` 指定服务地址；也支持 `--body` 直接传 JSON 字符串，具体转义遵循所用终端。客户端显示 HTTP 状态码和响应体，完整操作期限为 12 秒。

## 验证方式

- 自己的客户端连接参考服务端，验证操作入口、请求构造和结果显示。
- 参考客户端连接自己的服务端，验证各接口及错误响应。
- 按所选项目的协议构造请求，再结合阶段自查和验收清单补充测试。

起始服务端的六个待实现接口返回 501；参考服务端提供完整实现。参考源码不属于候选人交付内容。
