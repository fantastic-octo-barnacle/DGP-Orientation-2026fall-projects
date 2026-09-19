# HTTP 阶段自查

工具使用 Python 3.12 标准库，通过 HTTP 检查服务端，不导入任何路线的项目代码。两条路线都可以用 uv 运行。

先在另一个终端启动要验证的服务端，再从**候选人项目仓库根目录**执行相应阶段：

```bash
uv run --no-project --python 3.12 python common/check_http.py baseline
uv run --no-project --python 3.12 python common/check_http.py business
uv run --no-project --python 3.12 python common/check_http.py expiry --ttl 2
uv run --no-project --python 3.12 python common/check_http.py concurrency
```

| 阶段 | 何时运行 |
| --- | --- |
| `baseline` | 起始代码，应通过。 |
| `business` | 基础服务端业务完成后。 |
| `expiry --ttl 2` | 完成令牌过期功能后，先以 `--token-ttl-seconds 2` 重启服务端。自查参数只声明预期期限，不会修改服务端配置。 |
| `concurrency` | 异步服务端完成后，只检查 delay 不阻塞 ping，不覆盖全部状态竞争。 |

每条命令可追加 `--url http://127.0.0.1:7878` 指定地址。前三个阶段创建随机账号，未注销的账号保留到服务端重启。

PASS 仅表示当前检查通过。客户端交互、完整输入边界、慢请求和退出仍需按[验收清单](acceptance.md)验证。客户端须与[参考服务端](reference-programs.md)实际交互，不能只靠服务端自查工具验收。
