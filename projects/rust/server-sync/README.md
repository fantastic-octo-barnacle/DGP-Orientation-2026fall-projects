# Rust 同步服务端

完成内容见[公共同步服务端任务](../../../common/tasks.md#同步服务端)。开发环境、检查命令和启动命令见 [Rust 路线](../README.md)，必须在本目录执行。

## 代码结构

| 路径 | 职责 |
| --- | --- |
| `src/lib.rs` | 路由表、业务规则、用户状态和文本状态 |
| `src/main.rs` | 命令行参数、`Service` 构造和启动入口 |
| `src/http.rs` | 同步应用组装、启动接口和 HTTP 测试接口 |
| `src/infrastructure.rs` | Rocket 异步运行时、HTTP 适配、请求体读取与日志 |
| `tests/service.rs` | 业务逻辑测试 |
| `tests/http.rs` | HTTP 层测试 |

## 开发说明

主要从 `lib.rs` 的 `ROUTES`、`route_error()` 和 `Service::handle` 开始扩展接口。增加令牌期限时，在 `main.rs` 解析配置并构造带配置的 `Service`，再传给 `http::run`；业务配置与有效期逻辑由候选人实现。

`tests/http.rs` 通过 `http::with_service` 传入业务实例。完成本层任务无需编写 `async/await`，通常也不需要修改 `infrastructure.rs`。业务直接在 Rocket 工作线程上同步执行，仍须保护共享状态。HTTP 验证见[同步服务端](../../../common/tasks.md#同步服务端)。
