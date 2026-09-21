# Rust 学习指引

通用学习方法见[前言](../../common/preface.md)。本页只补充 Rust 路线的常用资料入口，以及查询语法、标准库、Cargo、Clippy 和本项目依赖 API 的方法；不要求从第一页读到最后一页。

## 资料入口

| 需要查询的内容 | 推荐入口 | 用途 |
| --- | --- | --- |
| 系统入门和语言心智模型 | [The Rust Programming Language](https://doc.rust-lang.org/book/) | 理解所有权、借用、模块、错误处理和常用模式 |
| 语法与用法示例 | [Rust by Example](https://doc.rust-lang.org/rust-by-example/) | 快速对照某种写法怎么写 |
| 标准库 API | [Standard Library Reference](https://doc.rust-lang.org/std/) | 查类型、方法、trait、错误和模块文档 |
| Cargo、锁文件和命令 | [The Cargo Book](https://doc.rust-lang.org/cargo/) | 理解 `Cargo.toml`、`Cargo.lock`、`cargo check` 和 `--locked` |
| 编译器错误码 | [Rust Compiler Error Index](https://doc.rust-lang.org/error_codes/) | 查完整错误说明和修复思路 |
| Clippy 诊断 | [Clippy 文档](https://doc.rust-lang.org/clippy/) | 理解 lint 含义和更推荐的写法 |
| 格式化工具 | [rustfmt 文档](https://rust-lang.github.io/rustfmt/) | 理解格式化检查和配置 |
| Web 框架 | [Rocket Guide](https://rocket.rs/guide/v0.5/)、[Rocket API](https://api.rocket.rs/v0.5/rocket/) | 查路由、请求、响应、状态和测试用法 |
| JSON 处理 | [`serde_json` 文档](https://docs.rs/serde_json/latest/serde_json/) | 查 `Value`、序列化和反序列化 |
| 命令行参数 | [`clap` 文档](https://docs.rs/clap/latest/clap/) | 查参数定义、解析和帮助信息 |
| HTTP 客户端 | [`reqwest` 文档](https://docs.rs/reqwest/latest/reqwest/) | 查请求、JSON、超时和错误处理 |

这些入口以官方文档和本项目直接使用的 crate 文档为主。看到博客、教程或讨论时，可以把它当作理解路径，但结论应回到当前版本的官方文档、crate 文档和项目测试验证。

## 如何查文档

1. 先判断问题属于哪一层：Rust 语言规则、标准库、Cargo、Clippy、第三方 crate，还是项目自身逻辑。
2. 初学概念优先看 The Rust Programming Language；查具体写法优先看 Rust by Example；确认精确 API 时看 Standard Library Reference 或 crate 文档。
3. 查 API 时至少看五件事：函数签名、参数和返回值、trait bound、生命周期、错误类型。示例代码不能替代这些约束。
4. 编译失败时读完整错误输出，包括 `help`、`note` 和错误码；不要只看第一行。Clippy 提示也应先理解原因，再决定是否重写。
5. 本项目使用 Cargo 锁文件和 2024 edition。查资料时注意版本，必要时在 docs.rs 选择与 `Cargo.lock` 对应的版本，而不是直接假设最新 API 可用。
6. 文档结论回到项目验证：用 `cargo check`、`cargo clippy`、`cargo test` 或一个最小测试确认行为，再决定是否采用。

## 与项目的对应关系

| 项目内容 | 优先查阅 |
| --- | --- |
| 所有权、借用和错误处理 | The Rust Programming Language、Rust by Example |
| `String`、`Vec`、`BTreeMap` 和锁 | Standard Library Reference |
| crate、锁文件和模块组织 | The Cargo Book |
| Rocket 路由、请求和测试 | Rocket Guide、Rocket API |
| JSON 请求和响应 | `serde_json` 文档 |
| 命令行参数 | `clap` 文档 |
| 同步客户端请求 | `reqwest` 文档 |
| Clippy 和 rustfmt 诊断 | Clippy 文档、rustfmt 文档 |

工具链、检查命令和启动命令见 [Rust 路线](README.md)。
