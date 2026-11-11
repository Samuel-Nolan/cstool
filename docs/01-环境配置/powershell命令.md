# powershell命令


PowerShell 是 Windows 及跨平台环境下的强大命令行 Shell 和脚本语言。与传统的 Bash 或 CMD 不同，PowerShell 的核心特性是**基于 .NET 对象管道**，而不是纯文本流；命令命名大多遵循标准的 **`Verb-Noun`（动词-名词）** 规范，并提供了大量常用的别名（Alias）以便快速输入。

## 1. 核心网络请求与脚本执行（Invoke 家族）

在 PowerShell 中，`Invoke` 是用于执行操作、发起调用或运行脚本的标准动词。在日常配置开发环境（如安装 Scoop、Oh My Posh、uv、Rust 等工具）时，最常接触到以下命令与别名：

| 命令 (Cmdlet) | 常用别名 | 功能说明 | 常见场景 |
| :--- | :--- | :--- | :--- |
| `Invoke-RestMethod` | `irm` | 发送 HTTP/HTTPS 请求并自动解析响应内容（JSON/XML/纯文本） | 下载在线安装脚本、调用 REST API |
| `Invoke-Expression` | `iex` | 将传入的字符串当作 PowerShell 表达式在当前作用域执行 | 搭配 `irm` 执行一键安装、载入 Profile |
| `Invoke-WebRequest` | `iwr` / `curl` / `wget`* | 发起完整 HTTP 请求，获取响应对象与状态码 | 下载文件到本地、网页抓取 |
| `Invoke-Item` | `ii` | 调用系统关联的默认程序打开文件、目录或 URL | 类似 macOS 的 `open`、Linux 的 `xdg-open` |
| `Invoke-Command` | `icm` | 在本地或远程计算机上执行指定的脚本块或命令 | 批量自动化运维、并发执行 |

> 注：在 Windows PowerShell 5.1 中 `curl` 和 `wget` 是 `Invoke-WebRequest` 的别名；而在现代 PowerShell 7+ 中，默认优先调用系统原生的 `curl.exe`。

### 1.1 `irm` (`Invoke-RestMethod`)

`irm` 会自动反序列化响应内容。如果目标 URL 返回的是纯文本脚本或 JSON 数据，它会直接转换为字符串或 PowerShell 对象，因此非常适合用于自动化脚本中管道传值。

```powershell
# 示例 1：获取在线脚本内容（最常见场景）
irm https://get.scoop.sh

# 示例 2：请求 JSON API，自动转为对象并直接访问属性
$data = irm https://api.github.com/repos/PowerShell/PowerShell/releases/latest
$data.tag_name
```

### 1.2 `iex` (`Invoke-Expression`)

`iex` 会将传入的文本作为代码执行，功能类似于其他语言中的 `eval`。

```powershell
# 经典搭配：下载并直接执行安装脚本（以 Scoop 为例）
irm https://get.scoop.sh | iex

# 初始化 Oh My Posh 主题配置（通常写在 $PROFILE 中）
oh-my-posh init pwsh | iex
```

> **安全提醒**：`irm ... | iex` 属于无确认直接执行远程代码的操作，在运行未知来源的脚本前，建议先单独使用 `irm <URL>` 查看脚本内容。

### 1.3 `iwr` (`Invoke-WebRequest`)

需要将远程文件下载并保存到本地磁盘时，使用 `iwr` 的 `-OutFile` 参数：

```powershell
# 下载文件并保存为本地文件
iwr -Uri "https://example.com/file.zip" -OutFile "file.zip"

# 包含自定义请求头
iwr -Uri "https://httpbin.org/headers" -Headers @{ "Authorization" = "Bearer token" }
```

### 1.4 `ii` (`Invoke-Item`)

快速调用资源管理器或默认应用打开文件：

```powershell
# 在 Windows 资源管理器中打开当前目录
ii .

# 打开当前用户的 PowerShell 配置文件
ii $PROFILE
```

---

## 2. 脚本执行策略管理（ExecutionPolicy）

在 Windows 新环境中运行 `.ps1` 脚本时，常遇到类似错误：`因为在此系统上禁止运行脚本，无法加载文件...`。这是由于默认的安全执行策略限制。

```powershell
# 查看当前执行策略
Get-ExecutionPolicy -List

# 解决报错：为当前用户开启远程签名脚本执行权限（最推荐，安全且免管理员权限）
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser

# 仅为当前终端窗口临时解除限制
Set-ExecutionPolicy Bypass -Scope Process
```

---

## 3. 环境与配置文件（$PROFILE 与环境变量）

### 3.1 配置文件（Profile）

PowerShell 启动时会自动加载 `$PROFILE` 脚本，用于定义别名、函数和初始化工具环境。

```powershell
# 检查配置文件是否存在
Test-Path $PROFILE

# 如果不存在，创建配置文件
if (!(Test-Path $PROFILE)) { New-Item -Type File -Path $PROFILE -Force }

# 使用记事本或 VS Code 编辑配置文件
notepad $PROFILE
code $PROFILE

# 修改后重新加载生效
. $PROFILE
```

### 3.2 环境变量管理

```powershell
# 查看环境变量（如 PATH）
$env:PATH

# 临时设置当前会话的环境变量（终端关闭后失效）
$env:HTTP_PROXY = "http://127.0.0.1:7890"
$env:HTTPS_PROXY = "http://127.0.0.1:7890"

# 清除会话环境变量
$env:HTTP_PROXY = $null

# 永久设置用户级环境变量（利用 .NET API）
[Environment]::SetEnvironmentVariable('MY_VAR', 'my_value', 'User')

# 永久读取环境变量
[Environment]::GetEnvironmentVariable('MY_VAR', 'User')
```

---

## 4. 命令与别名查询机制

不确定某个命令的原型或别名时，可以使用内置的查询体系：

```powershell
# 1. 查询别名对应的真实命令（例如查询 irm、iex）
Get-Alias irm
Get-Alias iex

# 2. 反查某个命令拥有的所有别名
Get-Alias -Definition Invoke-RestMethod

# 3. 查找命令位置或可执行文件（类似 Linux 的 which / whereis）
Get-Command node
gcm git

# 4. 查看命令文档与使用示例
Get-Help Invoke-RestMethod -Examples

# 5. 核心探针：查看管道对象的属性和方法（极其重要）
Get-Process | Get-Member
```

---

## 5. 常用文件与目录操作

PowerShell 为许多传统 CMD / Linux 常用命令预置了别名，便于跨平台习惯平滑迁移：

| 操作类型 | PowerShell 原型 (Cmdlet) | 常见别名 | 说明与常用参数 |
| :--- | :--- | :--- | :--- |
| 切换目录 | `Set-Location` | `cd`, `chdir`, `sl` | `cd ..` 返回上一级，`cd ~` 回家目录 |
| 列出目录 | `Get-ChildItem` | `ls`, `dir`, `gci` | `-Hidden` 显示隐藏项，`-Recurse` 递归 |
| 获取当前路径 | `Get-Location` | `pwd`, `gl` | 输出当前绝对路径 |
| 新建文件/目录 | `New-Item` | `ni`, `md`, `mkdir` | `-ItemType File` 或 `-ItemType Directory` |
| 复制文件 | `Copy-Item` | `cp`, `copy`, `cpi` | `-Recurse` 递归复制目录 |
| 移动/重命名 | `Move-Item` | `mv`, `move`, `mi` | 跨目录移动或本地重命名 |
| 删除文件 | `Remove-Item` | `rm`, `del`, `ri` | `-Recurse` 递归删除，`-Force` 强制删除 |
| 读取文本 | `Get-Content` | `cat`, `type`, `gc` | `-Tail 20 -Wait` 实时监听（等同 `tail -f`） |
| 写入文本 | `Set-Content` / `Add-Content` | `sc`, `ac` | `Set-Content` 覆盖，`Add-Content` 追加 |
| 路径检测 | `Test-Path` | 无 | 返回布尔值 `$true` 或 `$false` |

### 实用小技巧

```powershell
# 替代 Linux 的 touch 命令新建空文件
New-Item test.txt -ItemType File -Force
# 或者更快捷的写法：
"" > test.txt

# 实时监听日志输出（类似 tail -f app.log）
Get-Content app.log -Tail 10 -Wait

# 递归搜索所有 .md 文件
Get-ChildItem -Recurse -Filter *.md
```

---

## 6. 进程管理与端口排查

```powershell
# 1. 查看正在运行的进程
Get-Process -Name node

# 2. 终止进程（强制结束）
Stop-Process -Name node -Force
Stop-Process -Id 12345 -Force

# 3. 排查本地端口占用（例如排查 8080 端口被谁占用）
Get-NetTCPConnection -LocalPort 8080 | Select-Object LocalAddress, LocalPort, OwningProcess, State

# 4. 根据端口占用的 PID 查出对应进程名称
Get-Process -Id (Get-NetTCPConnection -LocalPort 8080).OwningProcess

# 5. 以管理员权限启动新的 PowerShell 终端
Start-Process pwsh -Verb RunAs
```

---

## 7. 管道对象处理与文本搜索

PowerShell 管道传递的是对象，通过属性进行过滤与提取非常精确：

```powershell
# 1. 条件过滤（Where-Object，别名 ? 或 where）
# 找出内存占用大于 200MB 的进程
Get-Process | Where-Object WorkingSet64 -gt 200MB

# 2. 选择属性与截取（Select-Object，别名 select）
# 按 CPU 降序排序并取前 5 个进程
Get-Process | Sort-Object CPU -Descending | Select-Object -First 5 -Property Name, CPU, WorkingSet64

# 3. 文本正则匹配（Select-String，别名 sls，相当于 grep）
cat app.log | Select-String "ERROR" -CaseSensitive:$false

# 在当前目录下所有文本文件中搜索关键字
Select-String -Path ".\*.md" -Pattern "PowerShell"

# 4. JSON 数据转换
# 将对象转为 JSON 格式
Get-Process -Name pwsh | Select-Object Name, Id, CPU | ConvertTo-Json

# 将 JSON 字符串解析为可交互的对象
'{"name": "cstool", "author": "Samuel"}' | ConvertFrom-Json
```

---

## 8. 常见比较运算符速查

PowerShell 使用字母符号作为比较运算符，避免与重定向符号（`<`、`>`）冲突：

| 运算符 | 含义 | 示例 |
| :--- | :--- | :--- |
| `-eq` | 等于 (Equal) | `$a -eq 10` |
| `-ne` | 不等于 (Not Equal) | `$a -ne 0` |
| `-gt` | 大于 (Greater Than) | `$a -gt 5` |
| `-ge` | 大于等于 (Greater or Equal) | `$a -ge 5` |
| `-lt` | 小于 (Less Than) | `$a -lt 10` |
| `-le` | 小于等于 (Less or Equal) | `$a -le 10` |
| `-like` | 通配符匹配（支持 `*`、`?`） | `$str -like "*test*"` |
| `-match` | 正则表达式匹配 | `$str -match "^\d+$"` |
| `-contains` | 集合是否包含元素 | `@(1, 2, 3) -contains 2` |
