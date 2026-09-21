# Rust 路线

任务范围与推进顺序见[公共任务说明](../../common/tasks.md)。本页是 Rust 项目的开发说明，集中说明同语言项目共用的工具链、目录结构、检查命令和启动方式。

语言学习和资料查询方法见 [Rust 学习指引](learning.md)。

## 开发环境

- 使用稳定版 Rust 和 Cargo。
- 每个任务目录都是独立 crate，各有 `Cargo.toml` 和 `Cargo.lock`。
- 这些项目没有 Cargo workspace，也没有共享 crate；不要用一个任务目录的锁文件或构建产物服务另一个任务。
- 以下命令都必须在具体任务目录中运行。

提交前依次执行检查：

```bash
cargo fmt -- --check
cargo check --locked
cargo clippy --locked --all-targets -- -D warnings
cargo test --locked
cargo build --release --locked
```

## 代码结构

| 路径 | 职责 |
| --- | --- |
| `src/main.rs` | 命令行入口和参数解析 |
| `src/lib.rs` | 业务规则、用户状态和文本状态 |
| `src/http.rs` | 服务端应用组装、HTTP 适配和启动接口 |
| `src/infrastructure.rs` | 同步服务端的 Rocket 异步运行时适配层 |
| `tests/` | 集成测试和 HTTP 测试 |

服务端项目共享同一个基本分层：`lib.rs` 实现业务和状态，`main.rs` 负责命令行入口，`http.rs` 负责应用组装与启动。同步服务端通过 `infrastructure.rs` 隐藏 Rocket 的异步运行时，让业务和 HTTP 测试保持同步接口；异步服务端在 `http.rs` 中处理请求，并用 `rocket::tokio::task::spawn_blocking` 隔离密码计算等阻塞工作。两层都必须保护共享状态，不能假设请求会串行执行。

## 运行命令

在对应任务目录使用下表命令：

| 目录 | 启动命令 |
| --- | --- |
| `client-sync/` | `cargo run --locked -- --url http://127.0.0.1:7878` |
| `server-sync/` | `cargo run --locked -- --address 127.0.0.1:7878` |
| `server-async/` | `cargo run --locked -- --address 127.0.0.1:7878` |

启动后的操作见[共通交互](../../common/tasks.md#共通交互)，完成情况按[验收清单](../../common/acceptance.md)验证。
