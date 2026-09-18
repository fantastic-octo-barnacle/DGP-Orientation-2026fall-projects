# Python 阶段自查

先在另一个终端启动待验证服务端。如果交互客户端还连接着该服务端，先输入 `q` 退出，让服务端能够接收自查连接。在 `projects/python/` 目录按当前阶段选择命令：

```text
uv run python self-check/check.py baseline
uv run python self-check/check.py text
uv run python self-check/check.py numbers
uv run python self-check/check.py store
```

可追加 `--port 其他端口`。baseline 和 text 验证基线服务端；numbers、store 仅在相应阶段完成后运行。它们不随默认 pytest 执行。

成功显示 `PASS`；结果不符时显示 `FAIL`、检查项、请求、预期 data 和实际响应，退出码为 1。连接失败、超时或响应格式错误会显示对应原因。先核对服务端、端口和当前阶段，再检查 id、响应结构和数值。`store` 使用专用键 `__self_check__`，成功结束时删除该键；运行前确认该键没有个人数据，失败后可能需要手动清理。

这些脚本验证服务端的少量正常场景，不能替代客户端功能演示，也不包含所有异常测试。其余要求见[验收清单](../acceptance.md)。
