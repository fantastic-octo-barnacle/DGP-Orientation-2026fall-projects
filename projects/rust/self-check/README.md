# Rust 阶段自查

先启动待验证的服务端。在 `projects/rust/` 目录执行：

```text
cargo run --locked --manifest-path client-sync/Cargo.toml --example self_check -- baseline 127.0.0.1:7878
cargo run --locked --manifest-path client-sync/Cargo.toml --example self_check -- actions 127.0.0.1:7878
```

baseline 可用于起始服务端；actions 仅在 echo/delay 完成后运行。自查通过输出 PASS，失败会显示响应或断言位置。这个 example 是显式使用的验证工具，不会在 cargo test 中执行阶段动作。

工具每个样例使用新连接，仅覆盖少量正常消息；不证明连续交互、候选人客户端入口、并发或退出已完成。其余要求见[验收清单](../acceptance.md)。

可使用[参考程序](../../../reference/README.md)替换通信一端。本项目的动作范围以[协议](../protocol.md)为准。
