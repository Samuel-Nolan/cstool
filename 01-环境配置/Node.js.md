### Node.js 是什么？

- **Node.js** 是一个基于 Chrome V8 引擎的 JavaScript 运行时环境。
- 它允许你在服务器端（而不是浏览器中）运行 JavaScript 代码。
- 提供了丰富的内置模块（如 `fs`、`http`、`path` 等），用于构建网络应用、文件操作、API 服务等。

---

### npm 是什么?
- **npm**（全称：**Node Package Manager**）是 Node.js 的**包管理器**。
- 它有两个主要含义：
    1. **命令行工具（CLI）**：用于安装、更新、卸载和管理第三方 JavaScript 包（也叫“模块”或“依赖”）。
    2. **在线仓库（Registry）**：世界上最大的开源软件注册表之一（[https://www.npmjs.com](https://www.npmjs.com/)），托管了数百万个可重用的代码包。
- **cnpm**是由 淘宝 NPM 镜像团队（现为阿里云）提供的 npm 的中国镜像版本，加速包安装下载


```shell
node -v
npm -v
```


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

