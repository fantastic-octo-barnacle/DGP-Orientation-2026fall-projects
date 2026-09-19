# Rust 同步客户端

完成内容见[公共同步客户端任务](../../../common/tasks.md#同步客户端)，开发检查见 [Rust 工具链](../README.md#工具链与检查)。

在本目录启动：

```bash
cargo run --locked -- --url http://127.0.0.1:7878
```

`src/main.rs` 提供命令行入口，`src/lib.rs` 实现请求与交互逻辑。启动后的操作见[共通交互](../../../common/tasks.md#共通交互)。
