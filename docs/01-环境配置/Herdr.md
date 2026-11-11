# Herdr

Herdr 是一款专为 AI 编码智能体（如 Claude Code、Codex、Pi 等）打造的终端复用与管理工具（Agent Multiplexer）。它支持多会话隔离、窗口后台保持（关闭终端后智能体仍继续工作）、远程 SSH 穿透以及智能体工作状态监控。

官方网站：[Herdr 官网](https://herdr.dev/)  
官方文档：[Herdr Documentation](https://herdr.dev/tui/docs/install/)


## Windows 安装

### 1. 脚本安装

在 Windows 上，推荐使用官方提供的 PowerShell 无文件（in-memory）安装脚本。为了避免占用 C 盘空间，可以通过设置环境变量将 Herdr 的工作目录和安装目录重定向至数据盘（如 `E:` 盘）。

```powershell
$env:HERDR_HOME = "E:\development\herdr"
$env:HERDR_INSTALL_DIR = "E:\development\herdr\bin"
irm https://herdr.dev/install.ps1 | iex
```


| 环境变量名                    | 默认值                                     | 作用说明                                                                                                           |
| ------------------------ | --------------------------------------- | -------------------------------------------------------------------------------------------------------------- |
| `$env:HERDR_HOME`        | `~/.herdr`（即 `$env:USERPROFILE\.herdr`） | Herdr 的核心运行与版本管理根目录。用于存放所有版本的释放文件（`packages\standalone\releases`）、多版本切换软链接（`packages\standalone\current`）和安装锁。 |
| `$env:HERDR_INSTALL_DIR` | `%LOCALAPPDATA%\Programs\Herdr\bin`     | 外部可执行程序的暴露目录。安装脚本会在此目录下创建指向当前激活版本的目录联接（Junction），并自动将该路径前置插入到用户环境变量 `PATH`（注册表 `HKCU\Environment`）中。           |

> [!note]
> 上述环境变量仅在当前 PowerShell 会话临时生效用于安装引导。安装脚本会将最终确定的可执行文件路径（即 `$env:HERDR_INSTALL_DIR`）永久写入到用户的 `PATH` 注册表中。新开终端即可在任意路径运行 `herdr`。


### 2. 验证与更新

安装完成后，打开新的终端会话验证安装：

```powershell
herdr --version  # 查看版本
herdr  # 启动 Herdr

herdr update # 后续可以升级到最新稳定版
```


### 3. 常用命令

| 操作场景 | 命令 / 快捷键 | 说明 |
| --- | --- | --- |
| **启动 / 附加会话** | `herdr` | 启动并连接本地后台会话；若会话已存在则直接接入（Attach） |
| **客户端分离（Detach）** | `Ctrl + b` 紧接着按 `q` | 仅退出前端 TUI 渲染界面，**后台 Server、窗格和 Agent 继续运行** |
| **停止后台服务器** | `herdr server stop` | **彻底终止后台服务**，强制关闭所有窗格、销毁当前会话及正在运行的进程 |
| **更新客户端与服务** | `herdr update` | 升级到最新发布版本；默认保持旧版会话服务运行，重新运行 `herdr` 自动接入新客户端 |


## herdr.exe vs herdr-app

Herdr 体系目前主要提供两种使用形态：**终端版本（Herdr TUI / `herdr.exe`）** 和 **桌面原生应用（Herdr Desktop App / `herdr-app`）**，底层由通用运行时引擎 **`herdr-core`（`hc`）** 驱动。

> **名称澄清**：
> - 在命令或提示中常见的 `herd.exe` 为拼写笔误（或易与 Laravel 的本地开发环境 Herd 混淆）；在 Herdr 工具体系中，Windows 终端端的可执行程序为 **`herdr.exe`**。
> - 桌面端应用则称为 **Herdr App**（项目名为 `herdr-app`）。

| 对比维度            | Herdr TUI (`herdr.exe`)               | Herdr Desktop App (`herdr-app`)          |
| --------------- | ------------------------------------- | ---------------------------------------- |
| **产品定位**        | 终端复用器（类似针对 Agent 增强的现代 tmux）          | 现代化原生桌面窗口应用（AI Agent 工作台）                |
| **可执行文件**       | `herdr.exe`                           | 桌面安装包 / 安装至系统的桌面应用                       |
| **架构与进程模型**     | 单一后台服务管理所有 PTY 进程与状态                  | 分离式架构：`Holder`（持有 PTY）+ `Core`（处理业务逻辑）   |
| **Agent 状态感知**  | 屏幕抓取正则匹配（内置支持 20+ 款 Agent）            | 标准协议驱动（仅识别通过 `OSC 7501` 转义上报的状态）         |
| **重启恢复能力**      | 重启电脑后可恢复受支持 Agent 的历史上下文              | 重启电脑后仅保留工作区目录并打开全新 Shell                 |
| **界面与功能定制**     | 配置文件 + Plugins（插件体系）                  | Mods 体系（使用 JavaScript / GPUI 编写并支持实时热重载） |
| **远程 / SSH 支持** | 极佳。**原生支持纯 SSH**、手机端 SSH（如 Moshi）无缝接入 | 支持连接远程机器（通过 `hc connect`），但需桌面客户端环境      |
| **适用环境**        | 纯命令行、远程 VPS、低配环境、手机端查看                | 本地开发机、多任务桌面分屏协同、视觉看板需求                   |


## 远程连接 VPS（Tailscale）

借助 Tailscale 的虚拟内网（Tailnet），无需公网 IP 或云服务商开放端口，即可通过 Herdr 远程纳管 VPS 并持久化运行 AI 智能体。

### 1. 前置准备

1. 本地电脑与 VPS 均已安装并登录同一个 Tailscale 账号。
2. 在 Tailscale 控制台或运行 `tailscale status`，获取 VPS 的 **MagicDNS 主机名**或 **Tailscale 虚拟 IP**

### 2. SSH 密钥配置

Linux 云服务器默认通常关闭密码登录、仅允许公钥认证（`publickey`）。需要确保本地公钥已正确部署到 VPS，且 Windows 本地私钥权限受控。

#### 1. 获取本地公钥
在 Windows 本地 PowerShell 中查看已有公钥：

```powershell
# 若使用 RSA 密钥
Get-Content $env:USERPROFILE\.ssh\id_rsa.pub

# 若使用 ED25519 密钥（推荐）
Get-Content $env:USERPROFILE\.ssh\id_ed25519.pub
```

若提示文件不存在，可使用 `ssh-keygen -t ed25519` 命令生成一对新密钥。复制输出的整行公钥文本。

#### 2. 添加公钥到 VPS
通过云服务商网页控制台（VNC / WebShell）登录 VPS，将公钥写入目标用户的免密授权列表，并严格修正 Linux 权限（权限过宽会导致 SSH 静默拒绝）：

```bash
# 确保 .ssh 目录存在
mkdir -p ~/.ssh

# 将本地复制的公钥追加到 authorized_keys
echo "<your-public-key-content>" >> ~/.ssh/authorized_keys

# 严格修正 Linux 权限
chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys
chown -R <username>:<username> ~/.ssh
```

#### 3. 修复私钥权限 (Windows)
在 Windows 上发起连接时，若提示 `WARNING: UNPROTECTED PRIVATE KEY FILE! Bad permissions ... Permissions are too open`，说明私钥包含了 `Everyone` 等非受限权限，Windows OpenSSH 会出于安全考虑主动忽略该私钥。

在本地 PowerShell 中执行以下两条命令收紧私钥权限：

```powershell
# 1. 禁用权限继承并清除多余的继承权限（如 Everyone）
icacls "$env:USERPROFILE\.ssh\id_rsa" /inheritance:r

# 2. 仅向当前 Windows 用户授予读写权限
icacls "$env:USERPROFILE\.ssh\id_rsa" /grant:r "$($env:USERNAME):(R,W)"
```

> [!tip]
> 若使用的私钥是 `id_ed25519`，只需将上述命令中的 `id_rsa` 替换为 `id_ed25519` 即可。

#### 4. 验证连通
在本地终端测试登录：

```powershell
ssh <username>@<vps-tailscale-ip>
```

终端打印出系统的登录欢迎信息（MOTD）即代表 SSH 密钥认证已配置完成。


### 3. 配置 SSH Config

在本地 `~/.ssh/config`（Windows 为 `C:\Users\<username>\.ssh\config`）中添加主机别名：

```ssh
Host <vps-alias>
    HostName <vps-tailscale-ip>  # 也可以直接填 Tailscale 的 MagicDNS 主机名
    User <username>              # 远程登录用户名
    # IdentityFile ~/.ssh/id_rsa # 若有多个私钥，可显式指定路径
```

配置后可直接在终端使用别名连通测试：`ssh <vps-alias>`。


### 4. VPS 安装 Herdr

若通过本地执行 `herdr machine add` 触发的远程自动下载失败（提示 `error: download failed`），可直接登录 VPS 终端手动执行安装：

```bash
# 1. 安装 curl 工具（Debian 最小化系统通常未预装）
sudo apt update && sudo apt install -y curl

# 2. 确保本地可执行程序目录存在
mkdir -p ~/.local/bin

# 3. 执行官方一键安装脚本
curl -fsSL https://herdr.dev/install.sh | sh
```

安装完成后验证：`~/.local/bin/herdr --version`。确认成功后即可退出 VPS（执行 `exit`），回到本地继续纳管。


### 5. Herdr 远程纳管

#### 安装

将 Tailscale 上的 VPS 固化到本地 Herdr 客户端中：

```powershell
herdr machine add <vps-alias> --label "<vps-label>"
```

- **自动化部署**：若 VPS 上尚未安装 Herdr，首次添加时会交互式引导并自动在 VPS 上部署兼容的 Herdr 服务端，无需在 VPS 端手动执行安装命令。
- **多空间平滑切换**：本地终端打开 `herdr` 后，侧边栏会同时展示 `Local` 与 `<vps-label>`。通过快捷键 `Ctrl + b` 然后按 `w`（或直接点击侧边栏）即可在本地环境与远程 VPS 之间无缝切换。
- **抗网络抖动与后台持久化**：VPS 上的 Agent 在其独立的后台进程中运行。即使本地电脑休眠或 Tailscale 网络因切换 Wi-Fi/热点产生波动，重连后会话依然完整保留。


#### 删除
```powershell
# 查看已保存的机器列表（获取 profile-id）
herdr machine list

# 删除指定 VPS 配置（仅解绑本地连接，不影响 VPS 进程）
herdr machine remove <profile-id>

# 临时禁用 / 恢复连接
herdr machine disable <profile-id>
herdr machine enable <profile-id>

herdr server stop # 在 VPS 终端直接停止
```
