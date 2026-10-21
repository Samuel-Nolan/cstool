
[安装文档](https://ohmyposh.dev/docs/installation/prompt)



# oh-my-posh 配置

## 一、Windows

`$PROFILE`，一个自动变量，存储powershell的配置文件的位置
### 1.安装

### 2.安装字体
**Nerd Fonts** 是一个开源项目，旨在为开发者提供**带有大量图标（glyphs）的编程字体**。它通过将流行的字体（如 FiraCode、JetBrains Mono、Cascadia Code 等）与来自 **Font Awesome、Devicons、Octicons、Powerline** 等图标的字符集“打补丁”（patched），从而让终端、编辑器和 shell 提示符能正确显示各种符号（比如 Git 分支图标、文件类型图标、云服务 logo 等）。
`CaskaydiaCove Nerd Font`
1. 在字体官网download一个`.zip`文件
2. 解压缩打开后，选中所有`.tff`字体文件，右键装载
3. 在终端“设置”——“外观”——“字体”选中刚刚的字体名字


### 3.配置文件

1. `notepad $PROFILE`：用记事本打开
2. `New-Item -Path $PROFILE -Type File -Force`：如果没有则需要创建

### 4.下载主题

1. `C:\Users\<你的用户名>\.poshthemes`：在资源管理器中新建一个目录
2. `New-Item -Path "$HOME\.poshthemes" -ItemType Directory -Force`：在PowerShell中指向主题配置文件
3. 
```
   Invoke-WebRequest `  https://raw.githubusercontent.com/JanDeDobbeleer/oh-my-posh/main/themes/paradox.omp.json `  -OutFile "$HOME\.poshthemes\paradox.omp.json"
```
  - 下载主题
  - 去官网只需要，把以上代码中的`paradox`（两个），换成喜欢的主题名称
4. `dir $HOME\.poshthemes`：验证主题是否已经下载
5. 删除不需要的主题：由于主题都是`.json`文件，直接去资源管理器的`C:\Users\<你的用户名>\.poshthemes`删除文件

### 5.装载主题

1. `notepad $PROFILE`
2. `oh-my-posh init pwsh --config "$HOME\.poshthemes\paradox.omp.json" | Invoke-Expression`：写入记事本
`

## 二、Linux

.bashrc 是一个 shell 配置文件，位于你的用户主目录下（~/.bashrc）。

  作用：
  - 当你打开一个新的交互式 bash 终端时，系统会自动执行这个文件里的命令
  - 通常用来设置环境变量、别名、函数等

  快速理解：
  - ~/.bashrc — 为当前用户设置，每次开新终端都生效
  - ~/.bash_profile — 登录时生效（仅登录 shell）
  - /etc/bash.bashrc — 系统范围内，所有用户共享

  常见用途示例：
```bash
export EDITOR=vim            
alias ll='ls -la'
export PATH="$HOME/bin:$PATH"
```


### 1.安装`oh-my-posh`

```bash
curl -s https://ohmyposh.dev/install.sh | bash -s
```
- `-d`：可以指定路径
- 注意看`themes`的位置，一般在`.cache\oh-my-posh`下
- 可能预装了一些themes，不用的可以删除
- 验证是否成功
```bash
oh-my-posh --version
```

- 如果找不到，就新建一个配置文件
```bash
echo 'export PATH=$PATH:~/.local/bin' >> ~/.bashrc
source ~/.bashrc
```
### 2.配置文件

- 打开配置文件，这里用nano，vim，vscode都可以。如果是wsl，直接在windows的资源管理器中打开，文件地址是`wsl/home/(user)/.bashrc`文件
```bash
vim ~/.bashrc
```
- 在最后加入以下代码，导入主题配置
```json
eval "$(oh-my-posh init bash --config ~/.cache/oh-my-posh/themes/hul10.omp.json)"
```
- 加载配置文件
```bash
source ~/.bashrc
```



1. 按 `Win + R`，输入 `intl.cpl` 回车
2. 切换到 **"管理"** 选项卡 → 点击 **"更改系统区域设置"**
3. ✅ 勾选 **"Beta: 使用 Unicode UTF-8 提供全球语言支持"**
4. 千万不要这样！
