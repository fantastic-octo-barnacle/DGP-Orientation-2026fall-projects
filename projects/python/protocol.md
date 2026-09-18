# Python 工具服务协议

## 通用消息规则（协议 v1）

- 仅在本机 TCP 通信，默认地址为 `127.0.0.1:7878`。每行一个 UTF-8 JSON 对象，接受 LF 或 CRLF；字符串内换行使用 JSON 转义。
- 一条完整消息的 UTF-8 编码最多 65,536 字节，不含行尾分隔符。发送方必须遵守此限制；超长请求尽量返回 `line_too_long` 后关闭连接。
- 同一连接内请求与响应一一对应、顺序处理。不要求同连接请求多路复用。
- `id` 为 0 到 9,007,199,254,740,991 的整数，不能是布尔值、小数或指数形式。`action` 为字符串。
- JSON 必须使用有效 Unicode 标量值和有限数字，不接受 NaN、Infinity 或无法表示为有限数的数字。对象键不应重复。
- 先检查 JSON，再检查对象、id 和 action 类型，再判断动作，最后检查该动作的字段和参数。
- 缺字段、额外字段或参数类型错误返回 `invalid_request`；不存在或当前阶段未实现的动作返回 `unknown_action`。
- 无法取得有效 id 时响应 id 为 null；否则错误响应保留请求 id。错误说明文字不要求逐字一致，代码和结构必须一致。
- 合法连接中的业务/JSON 错误响应后应可继续请求；EOF 正常关闭，只有半条消息的 EOF 直接关闭。超时、异常断开及退出取消不保证返回响应。
- 成功响应恰有 `id/ok/data`；错误响应恰有 `id/ok/error`，error 含 `code/message`。响应过大返回 `response_too_large`，保留连接。

```json
{"id":1,"action":"ping"}
{"id":1,"ok":true,"data":"pong"}
{"id":2,"action":"missing"}
{"id":2,"ok":false,"error":{"code":"unknown_action","message":"action is not supported"}}
```

错误代码：`invalid_json`（含非法 UTF-8）、`invalid_request`、`unknown_action`、`line_too_long`、`response_too_large`。键值动作另有 `not_found` 和 `store_full`。

## 本项目动作

所有请求只允许表中列出的字段；响应的 data 形状固定。

| action | 请求字段（除 id/action） | 成功 data | 完成阶段 |
|---|---|---|---|
| ping | 无 | `"pong"` | 基线已有 |
| echo | data：字符串 | 原字符串 | 基线已有 |
| text_stats | text：字符串 | `{"characters":5,"lines":2}` | 服务端已有；基础任务接入客户端 |
| number_stats | numbers：数值列表 | `{"count":3,"min":1,"max":3,"mean":2}` | 标准层 |
| set | key、value：字符串 | `{}` | 进阶层 |
| get | key：字符串 | `{"value":"robot"}` | 进阶层 |
| delete | key：字符串 | `{}` | 进阶层 |
| list | 无 | 排序后的键数组，如 `["a","b"]` | 进阶层 |

### 文本统计

不去除空白，字符数按 Unicode 标量值计数（普通 Python 字符串长度），不按 UTF-8 字节数或屏幕字形计数。空字符串为 0 行，其他字符串按 LF 数量加 1；CR 本身只计一个字符，不单独分行。尾部 LF 产生一个空行。

```json
{"id":3,"action":"text_stats","text":"hi\nRM"}
{"id":3,"ok":true,"data":{"characters":5,"lines":2}}
```

基础任务的客户端应允许输入多行文本，例如逐行输入后用单独的结束标记完成；在说明中明确标记和如何输入空文本。由服务端统计，客户端显示其结果。

### 数值统计

numbers 长度为 1–10,000，元素为有限数字，绝对值不超过 1e100；不接受布尔值或数值字符串。单元素、负数、小数和重复值均有效。count 为整数；min/max/mean 可用等价整数或浮点表示。比较浮点结果采用相对容差 1e-9、绝对容差 1e-12。

### 内存键值

key 为 1–64 个 Unicode 字符；value 为最多 4096 个字符的字符串，可为空。最多保存 128 个不同键。set 覆盖已有键；容量满时新增键返回 store_full。get/delete 对不存在的键返回 not_found。list 按 Unicode 字符顺序排序。

状态属于服务端进程，跨请求、跨客户端重连保留，服务端重启清空；无需数据库、文件持久化或同时服务多个连接。测试使用专用键，避免覆盖个人数据。

## 本项目连接约定

基线同步服务端每次处理一个连接，同一连接内可连续发送请求；客户端退出后才服务下一个连接。客户端默认等待响应上限为 12 秒。本项目不要求添加并发、delay 动作或复杂退出管理。

使用[通用参考程序](../../reference/README.md)验证本页列出的动作。
