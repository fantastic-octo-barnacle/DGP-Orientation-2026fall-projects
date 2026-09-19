# HTTP 阶段自查

先启动要验证的服务端，在本目录执行（需要 Python 3.12，可用 uv 获取）：

```text
uv run --no-project --python 3.12 python ../../../common/check_http.py baseline
uv run --no-project --python 3.12 python ../../../common/check_http.py business
uv run --no-project --python 3.12 python ../../../common/check_http.py expiry --ttl 2
uv run --no-project --python 3.12 python ../../../common/check_http.py concurrency
```

可加 `--url http://127.0.0.1:7878` 指定地址。工具只用 Python 标准库，通过 HTTP 验证，无需导入项目代码。

baseline 应在起始代码上通过；其余阶段在完成对应任务后执行。expiry 要求服务端以 `--token-ttl-seconds 2` 启动；concurrency 仅用于异步端。每次自查创建随机账号，未注销的账号会保留到服务端重启。

PASS 只代表当前检查通过。完整输入边界、客户端交互、慢请求与退出仍需按[验收清单](../acceptance.md)验证。
