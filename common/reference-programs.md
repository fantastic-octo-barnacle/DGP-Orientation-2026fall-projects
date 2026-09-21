# 参考程序使用说明

参考程序是供你运行、对接和交叉验证的完整可执行程序，不是起始代码：`rm-client-sync` 用于测试你的服务端，`rm-server-async` 用于测试你的客户端。它们通过[统一 HTTP 协议](protocol.md)交互，对两条语言路线同样适用。

## 下载与平台选择

从本仓库的 [GitHub Releases](https://github.com/fantastic-octo-barnacle/DGP-Orientation-2026fall-projects/releases) 下载。下面是新的参考程序发布规格；**是否已有对应程序，以具体 Release 的资产为准**。旧版单体程序不等同于这里的两个程序，也不保证符合当前协议；没有匹配资产时，请向维护者确认可用版本。

| 运行环境 | 资产中的平台标识 | 压缩格式 |
| --- | --- | --- |
| Windows x86_64 | `windows-x86_64` | `.zip` |
| Linux x86_64 | `linux-x86_64` | `.tar.gz` |
| Linux arm64 | `linux-arm64` | `.tar.gz` |
| macOS Intel | `macos-x86_64` | `.tar.gz` |
| macOS Apple Silicon | `macos-arm64` | `.tar.gz` |

选择实际运行终端所在的系统与架构。macOS/Linux 可用 `uname -m` 查看架构，`aarch64` 对应 arm64。系统版本与运行库要求以 Release 说明为准，不保证旧系统或所有 Linux 发行版可运行。Windows arm64 暂无原生包。

资产命名为 `rm-projects-rust-<平台>-reference-vX.Y.Z`，后接压缩扩展名；同名 `.sha256` 文件记录压缩包的校验值。

## （可选）校验与版本

将压缩包和对应 `.sha256` 文件下载到同一目录，解压前校验。下列命令中的文件名需替换为实际下载的名称：

```powershell
# Windows PowerShell：与 .sha256 中的散列比较，忽略字母大小写
Get-FileHash .\<压缩包文件名>.zip -Algorithm SHA256
Get-Content .\<同名文件>.sha256
```

```bash
# Linux
sha256sum -c <同名文件>.sha256
# macOS
shasum -a 256 -c <同名文件>.sha256
```

不匹配时不要运行，重新下载并向维护者反馈。解压后阅读 `VERSION`、`projects-commit.txt` 和 `target.txt`，分别确认程序版本、对应项目材料版本和编译目标；其他构建追溯信息可用于报告问题。

`projects-commit.txt` 指向本项目仓库的规范版本。自己的实现提交不必与它相同，但所依据的任务与协议应与之匹配。不要混用不同规范版本的参考程序；报告问题时附上版本、平台、复现步骤和相关响应。

## 运行

以下是新参考程序的命令行约定。解压后进入包含可执行文件的目录，以 `--help` 查看所下载版本的实际参数。

Windows PowerShell：

```powershell
.\rm-server-async.exe --address 127.0.0.1:7878
# 另开终端，需要测试自己的服务端时运行参考客户端
.\rm-client-sync.exe --url http://127.0.0.1:7878
```

Linux/macOS：

```bash
./rm-server-async --address 127.0.0.1:7878
# 另开终端，需要测试自己的服务端时运行参考客户端
./rm-client-sync --url http://127.0.0.1:7878
```

参考服务端接受协议规定的 `--token-ttl-seconds`。同一地址和端口只运行一个服务端：验证客户端时启动参考服务端，验证服务端时启动自己的服务端。退出与数据生命周期见[协议](protocol.md#运行与并发)。

参考程序不能替代对自己代码的测试、理解和说明；还需完成[验收清单](acceptance.md)中的场景。
