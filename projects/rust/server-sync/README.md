# Rust 同步服务端

完成内容见[公共同步服务端任务](../../../common/tasks.md#同步服务端)，开发检查见 [Rust 工具链](../README.md#工具链与检查)。

在本目录启动：

```bash
cargo run --locked -- --address 127.0.0.1:7878
```

从 `src/lib.rs` 的同步业务开始，更新其中的 `ROUTES`、`route_error` 和 `Service::handle` 来扩展接口。`src/main.rs` 提供同步命令行入口，`src/http.rs` 提供同步的应用组装与启动接口。增加令牌期限时，在 `main.rs` 解析参数、构造带配置的 `Service`，再传给 `http::run`；HTTP 测试可通过 `http::with_service` 传入业务实例。业务配置与有效期逻辑留给候选人实现。

`tests/http.rs` 使用 Rocket 的同步测试客户端。完成本层任务无需编写 `async/await`，也无需修改基础设施模块 `src/infrastructure.rs`；它负责 Rocket 的异步运行时、HTTP 适配、请求体读取与日志。业务直接在 Rocket 工作线程上同步执行，不保证请求串行执行，仍须保护共享状态；异步层进一步学习隔离阻塞工作。HTTP 验证见[验收清单](../../../common/acceptance.md)。
