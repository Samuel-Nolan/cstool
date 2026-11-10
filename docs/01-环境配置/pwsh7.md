# pwsh7


## 介绍

| 维度     | Windows PowerShell 5.1                       | PowerShell 7+ (pwsh)               |
| ------ | -------------------------------------------- | ---------------------------------- |
| 可执行文件  | `powershell.exe`                             | `pwsh.exe`                         |
| 底层运行时  | .NET Framework 4.x（如 4.8）                    | 现代 .NET（Core 6 / 8 / 9 LTS）        |
| 平台支持   | 仅 Windows                                    | 跨平台（Windows / Linux / macOS）       |
| 维护状态   | 停更（仅随 Windows 提供安全修补）                        | 持续迭代与功能更新                          |
| 安装路径   | `C:\Windows\System32\WindowsPowerShell\v1.0` | `C:\Program Files\PowerShell\7`    |
| 配置文件路径 | `Documents\WindowsPowerShell\profile.ps1`    | `Documents\PowerShell\profile.ps1` |
- 由于大模型数据 coding 数据来源主要是 bash，对 win 的 powershell 的学习不足，导致会输出很多 bash 命令报错（ 大肥鱼大战PowerShell ）


## 安装

[官方教程-建议使用 .msi 方式安装](https://learn.microsoft.com/zh-cn/powershell/scripting/install/install-powershell-on-windows?view=powershell-7.6#msi)

### 1. 下载 .msi 安装包

如果 C 盘紧张，可以安装在其他盘，性能差不多

![[picture/Pasted image 20261110162617.png|400]]

| 选项                                                            | 中文解释                                                          |
| ------------------------------------------------------------- | ------------------------------------------------------------- |
| Add PowerShell to Path Environment Variable                   | 将 PowerShell 7 添加到系统 PATH 环境变量                                |
| Register Windows Event Logging Manifest                       | 注册 PowerShell 的 Windows 事件日志清单，方便系统事件查看器识别和记录 PowerShell 相关事件 |
| Enable PowerShell remoting                                    | 启用 PowerShell 远程管理，允许通过网络远程连接和执行 PowerShell 命令                |
| Disable Telemetry                                             | 禁用 PowerShell 遥测数据收集，例如使用情况和诊断信息                              |
| Add 'Open here' context menus to Explorer                     | 在文件资源管理器右键菜单中添加「Open here」，可以在当前文件夹直接打开 PowerShell 7          |
| Add 'Run with PowerShell 7' context menu for PowerShell files | 在 `.ps1` 脚本文件右键菜单中添加「Run with PowerShell 7」                   |


### 2. 环境变量配置

![[picture/Pasted image 20261110165459.png]]

- 把环境变量-系统环境变量-Path 中的 powershell/7 那条记录一直移到原来 powershell 的上面
- 这样读取 .exe 时先读 pwsh.exe

### 3. 启动配置

![[picture/Pasted image 20261110165950.png|675]]

1. 在原来的 PowerShell 中，"添加新配置文件"
2. 复制 “PowerShell”
3. ”命令行“ 改为刚刚安装的路径，`C:\Program Files\PowerShell\7\pwsh.exe`

### 4. 迁移oh-my-posh

 PowerShell 7 与系统自带 Windows PowerShell 5.1 的配置文件路径不同，不要混淆：
 - PowerShell 7：`~\Documents\PowerShell\Microsoft.PowerShell_profile.ps1`
 - Windows PowerShell 5.1：`~\Documents\WindowsPowerShell\Microsoft.PowerShell_profile.ps1`

1. [[oh-my-posh#3.配置文件]]
2. 在 PowerShell 7 中新建配置文件
3. 打开旧的 Windows PowerShell 5.1 配置文件，`notepad $PROFILE`
4. 复制到 PowerShell 7 中，`notepad $PROFILE`

### 5. Agent配置

根据目前的配置
## 报错

### 1. 关闭 PowerShell 启动时的自动更新检查和更新通知
```
PowerShell 7.6.6
Process terminated.
totalWidth ('-17') must be a non-negative value. (Parameter 'totalWidth')
Actual value was -17.
   at System.Environment.FailFast(System.Runtime.CompilerServices.StackCrawlMarkHandle, System.String, System.Runtime.CompilerServices.ObjectHandleOnStack, System.String)
   at System.Environment.FailFast(System.Threading.StackCrawlMark ByRef, System.String, System.Exception, System.String)
   at System.Environment.FailFast(System.String, System.Exception)
   at Microsoft.PowerShell.UnmanagedPSEntry.Start(System.String[], Int32)
   at Microsoft.PowerShell.ManagedPSEntry.Main(System.String[])
System.ArgumentOutOfRangeException: totalWidth ('-17') must be a non-negative value. (Parameter 'totalWidth')
Actual value was -17.
   at System.ArgumentOutOfRangeException.ThrowNegative[T](T value, String paramName)
   at System.String.PadRight(Int32 totalWidth, Char paddingChar)
   at Microsoft.PowerShell.UpdatesNotification.ShowUpdateNotification(PSHostUserInterface hostUI)
   at Microsoft.PowerShell.ConsoleHost.Start(String bannerText, String helpText, Boolean issProvidedExternally)
   at Microsoft.PowerShell.UnmanagedPSEntry.Start(String[] args, Int32 argc)
```

```shell
[Environment]::SetEnvironmentVariable(
    'POWERSHELL_UPDATECHECK',
    'Off',
    'User'
)

# 验证
[PSCustomObject]@{
    Process = [Environment]::GetEnvironmentVariable('POWERSHELL_UPDATECHECK', 'Process')
    User    = [Environment]::GetEnvironmentVariable('POWERSHELL_UPDATECHECK', 'User')
}
```


- 手动下载 ,msi 文件更新
