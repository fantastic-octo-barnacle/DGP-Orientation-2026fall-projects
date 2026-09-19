# Rust 同步服务端

完成内容见[公共同步服务端任务](../../../common/tasks.md#同步服务端)，开发检查见 [Rust 工具链](../README.md#工具链与检查)。

在本目录启动：

```bash
cargo run --locked -- --address 127.0.0.1:7878
```

`src/main.rs` 提供命令行入口，`src/http.rs` 使用 Rocket 读取请求后直接调用 `src/lib.rs` 的同步业务。Rocket 本身使用异步运行时，这一层以同步业务调用作为过渡练习，不保证请求串行执行；异步层进一步隔离阻塞工作。HTTP 验证见[验收清单](../../../common/acceptance.md)。
