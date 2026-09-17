# Python 阶段自查

先在另一个终端启动待验证服务端。在项目目录运行：

```text
uv run python self-check/check.py baseline
uv run python self-check/check.py text
uv run python self-check/check.py numbers
uv run python self-check/check.py store
```

可追加 `--port 其他端口`。baseline 和 text 验证基线服务端；numbers、store 仅在相应阶段完成后运行。它们不随默认 pytest 执行。

成功显示 PASS；断言失败会显示请求结果或差异。先核对是否启动了正确的服务端、是否完成当前动作，再检查 id、响应结构和数值。store 使用并清理 `__self_check__` 键，运行前确保该键未保存你自己的内容。

这些脚本验证服务端的少量正常场景，不能替代客户端功能演示，也不包含所有异常测试。其余要求见[验收清单](../acceptance.md)。
