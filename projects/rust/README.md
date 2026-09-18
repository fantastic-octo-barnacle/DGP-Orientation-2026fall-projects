# Rust 本地通信服务

本项目难度较高，适合已经能用任意语言独立编写简单程序、希望进一步挑战的同学。你将在可运行的框架上学习 Rust、协议建模、错误处理和异步任务管理，可以在项目过程中学习 Rust。

开始前，完成 [Git/GitHub](../../common/git-github.md) 与 [WSL2](../../common/wsl2.md) 共通任务；已有基础的同学也需要完成，WSL2 按设备条件完成相应内容。

## 三个独立项目

- `client-sync/`：同步客户端，连接后发送一个固定 ping、显示响应。
- `server-sync/`：同步服务端，单连接一条请求，然后关闭并接受下一连接。
- `server-async/`：Tokio 异步读写，仍顺序处理连接，每连接一条请求。

各目录都有独立 Cargo.toml 和 Cargo.lock。没有 workspace，也没有共享协议 crate。协议类型各自维护，需要通过[同一协议](protocol.md)和测试保持一致。

基线已有非法 JSON、未知动作和连接结束等基础处理。完整连续交互、长度限制、超时和任务管理是后续明确的能力扩展。

## 恢复、运行和检查

按 [Rust 官方安装说明](https://www.rust-lang.org/tools/install)安装稳定工具链。Windows 还需要所选工具链对应的链接器和系统库；macOS/Linux 同样需要系统编译工具。依赖由各自锁文件恢复。

在本目录执行：

```text
cargo run --locked --manifest-path server-sync/Cargo.toml -- 127.0.0.1:7878
```

另开一个终端：

```text
cargo run --locked --manifest-path client-sync/Cargo.toml -- 127.0.0.1:7878
```

Ctrl-C 停止服务端，再将第一条命令的 server-sync 换成 server-async，重复验证。两种服务端使用同一端口时，依次启动验证。

分别在三个项目目录执行：

```text
cargo fmt --check
cargo check --locked
cargo clippy --locked --all-targets -- -D warnings
cargo test --locked
```

target 为本机生成内容，通过忽略规则保留在本机。三个 Cargo.lock 都需要保留，三个项目分别完成全部检查。

## 任务递进

1. **运行与理解**：运行三个项目与检查，追踪序列化、连接读写、处理和返回。理解异步等待与跨连接并发的区别。
2. **同步客户端**：新增 echo/delay，接受命令行参数并支持连续交互，显示成功或错误响应，与参考服务端验证。较高层级采用 Clap 组织参数。
3. **同步服务端**：实现新动作、参数校验、连续请求、长度边界和异常断开，补充配置、日志与测试。
4. **异步服务端**：实现相同协议行为，自行设计连接任务，使一个连接的 delay 不阻塞其他连接；隔离单连接失败并及时清理结束的任务。
5. **超时与退出**：同步客户端响应超时、两种服务端完整请求读取超时；异步服务端停止接收、结束空闲连接、限时等待在途请求、取消并回收剩余任务。

三个项目都属于成果，保留同步版本。初始“一条消息后关闭”的测试描述基线能力；完成连续交互时应更新为连续请求、EOF 等行为的测试，而不是机械保留已被新要求替代的关闭断言。

具体规则见[协议](protocol.md)，验证方法见[验收清单](acceptance.md)与[自查说明](self-check/README.md)。不要求硬件、GUI、数据库、加密、公网部署或同连接多路复用。

## 阅读与实现边界

从各自 main.rs 的启动和连接循环进入 lib.rs，再看服务端 protocol.rs。比较同步与异步代码，理解 async 读写与并发任务调度的区别，并通过多个连接验证并发行为。

使用 Serde/Serde JSON，异步项目使用 Tokio。错误处理可选标准库、anyhow 或 thiserror，但需要理解自己的选择。不要求特定 IDE。

[通用参考程序](../../reference/README.md)用于替换通信一端，通过可执行文件运行。使用参考客户端时需自行输入协议请求；你编写的客户端需提供正常使用入口。

## 成果

按[成果说明](../../common/deliverables.md)记录个人改动与验证结果。未完成所有层级不自动否定已有学习成果。CI 可选扩展分别执行三个项目的检查；不要求部署服务。
