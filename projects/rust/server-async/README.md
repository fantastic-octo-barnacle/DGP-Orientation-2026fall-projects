# Rust 异步服务端

完成内容见[公共异步服务端任务](../../../common/tasks.md#异步服务端)，开发检查见 [Rust 工具链](../README.md#工具链与检查)。

在本目录启动：

```bash
cargo run --locked -- --address 127.0.0.1:7878
```

`src/main.rs` 提供命令行入口，`src/lib.rs` 使用 Tokio/Axum 处理 HTTP，通过 `tokio::task::spawn_blocking` 调用同步业务。HTTP 验证见[阶段自查](../../../common/self-check.md)。
