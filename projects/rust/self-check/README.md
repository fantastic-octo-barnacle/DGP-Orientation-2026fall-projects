# HTTP 阶段自查

先启动要验证的服务端，在本目录执行（自查工具使用 Python 标准库，需要 Python 3.12，可用 uv 获取）：

```bash
uv run --no-project --python 3.12 python ../../../common/check_http.py baseline
uv run --no-project --python 3.12 python ../../../common/check_http.py business
uv run --no-project --python 3.12 python ../../../common/check_http.py expiry --ttl 2
uv run --no-project --python 3.12 python ../../../common/check_http.py concurrency
```

可加 `--url http://127.0.0.1:7878` 指定地址。工具只用 Python 标准库，通过 HTTP 验证，无需导入项目代码。

`baseline` 应在起始代码上通过；`business` 在完成基础服务端任务后执行；`expiry` 放在令牌过期任务阶段；`concurrency` 仅用于异步端。每次自查创建随机账号，未注销的账号会保留到服务端重启。

客户端层级不能只靠这个工具验证。请启动 Releases 中的完整参考服务端，使用客户端逐项验证请求、输入和输出；服务端层级可以使用自己的客户端或 Releases 中的完整参考客户端。

PASS 只代表当前检查通过。完整输入边界、客户端交互、慢请求与退出仍需按[统一验收清单](../../../common/acceptance.md)验证。
