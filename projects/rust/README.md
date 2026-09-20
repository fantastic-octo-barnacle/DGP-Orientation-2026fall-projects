# Rust 路线

任务范围与推进顺序见[公共任务说明](../../common/tasks.md)。本页只说明 Rust 工具链与代码入口。

## 工具链与检查

使用稳定版 Rust 和 Cargo。每个任务目录有独立的 `Cargo.toml`、`Cargo.lock`，没有 workspace 或共享 crate。在对应目录运行：

```bash
cargo fmt -- --check
cargo check --locked
cargo clippy --locked --all-targets -- -D warnings
cargo test --locked
cargo build --release --locked
```

## 运行入口

| 目录 | 起始代码入口 | 启动说明 |
| --- | --- | --- |
| `client-sync/` | `src/main.rs`、`src/lib.rs` | [同步客户端](client-sync/README.md) |
| `server-sync/` | `src/main.rs`、`src/http.rs`、`src/lib.rs`，Rocket | [同步服务端](server-sync/README.md) |
| `server-async/` | `src/main.rs`、`src/http.rs`、`src/lib.rs`，Rocket | [异步服务端](server-async/README.md) |

同步服务端从 `src/lib.rs` 的业务函数开始，启动入口、`http` 模块和 HTTP 测试均使用同步接口，底层适配无需修改。异步服务端从 HTTP 入口进入业务处理函数，学习异步等待与阻塞工作隔离。两层都需理解身份检查、密码计算与状态锁之间的关系。启动后的操作见[共通交互](../../common/tasks.md#共通交互)，完成情况按[验收清单](../../common/acceptance.md)验证。
