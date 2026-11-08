# Node.js

### Node.js 是什么？
- Node.js 是一个基于 Chrome V8 引擎的 JavaScript 运行时环境。
- 它允许你在服务器端（而不是浏览器中）运行 JavaScript 代码。
- 提供了丰富的内置模块（如 `fs`、`http`、`path` 等），用于构建网络应用、文件操作、API 服务等。
### npm 是什么?
- npm（全称：Node Package Manager）是 Node.js 的**包管理器**。
- 它有两个主要含义：
    1. 命令行工具（CLI）：用于安装、更新、卸载和管理第三方 JavaScript 包。
    2. 在线仓库（Registry）：世界上最大的开源软件注册表之一（[https://www.npmjs.com](https://www.npmjs.com/)），托管了数百万个可重用的代码包。
- cnpm是由阿里云提供的 npm 的镜像版本，加速包安装下载


## 安装
> [!note]
> 如果需要多个 node.js 版本，推荐使用 fnm 版本控制 [[#fnm]]
> 若仅需一个，可直接使用官网[node.js](https://nodejs.org/zh-cn/download) 的.msi 或者 .zip 安装包，更新直接覆盖

### 报错
```
npm : 无法加载文件 D:\nodejs\npm.ps1，因为在此系统上禁止运行脚本。有关详细信息，请参阅 https:/go.microsoft.com/fwlink/?  
LinkID=135170 中的 about_Execution_Policies。  
所在位置 行:1 字符: 1 
~~~  
    + CategoryInfo          : SecurityError: (:) []，PSSecurityException  
    + FullyQualifiedErrorId : UnauthorizedAccess
```
Windows PowerShell 默认的安全策略设置为 Restricted（受限），这会阻止运行任何 `.ps1` 脚本文件。而 npm 在 Windows 上会调用 `npm.ps1` 脚本来执行命令，因此被系统阻止了。
以管理员身份运行powershell
```
Get-ExecutionPolicy        # Restricted  
Set-ExecutionPolicy RemoteSigned   # 修改
```



## fnm

```bash
winget install Schniz.fnm
fnm --version 
where.exe fnm
```

由于 fnm 默认数据目录是 C 盘，需要改到其他盘的位置
这里改到 `E:\Development\fnm`

1. 在 系统环境变量 - 用户变量 - 新建

![[picture/Pasted image 20261107213214.png|600]]

2. 修改 powershell 启动设置
```bash
notepad $PROFILE
# 如果文件不存在就新建一个
New-Item -ItemType File -Path $PROFILE -Force           

# 在文件中写入
fnm env --use-on-cd --shell powershell | Out-String | Invoke-Expression

# 检查
$env:FNM_DIR               # 期望输出 E:\Development\fnm
```

| 参数                   | 作用                        |
| -------------------- | ------------------------- |
| `fnm env`            | 生成当前 Shell 所需的环境配置        |
| `--use-on-cd`        | 进入不同项目目录时，自动检查 Node.js 版本 |
| `--shell powershell` | 生成 PowerShell 专用配置        |
| `Out-String`         | 转换为 PowerShell 字符串        |
| `Invoke-Expression`  | 执行生成的配置                   |

3. 安装 node.js
```bash
fnm install 22
fnm use 22     # 切换到该版本

# 验证
node -v
npm -v
where.exe node
```