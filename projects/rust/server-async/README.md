# Rust 异步服务端

完成内容见[公共异步服务端任务](../../../common/tasks.md#异步服务端)，开发检查见 [Rust 工具链](../README.md#工具链与检查)。

在本目录启动：

```bash
cargo run --locked -- --address 127.0.0.1:7878
```

`src/main.rs` 提供命令行入口，`src/http.rs` 使用 Rocket 处理 HTTP，通过 `rocket::tokio::task::spawn_blocking` 将密码计算等同步业务移出运行时工作线程；`src/lib.rs` 管理业务状态。HTTP 验证见[验收清单](../../../common/acceptance.md)。
