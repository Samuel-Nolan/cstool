>参考文档：
>[安装过程推荐这篇](https://blog.csdn.net/u011119817/article/details/130745551?spm=1001.2014.3001.5506)
>[安装完成后的设置推荐这篇](https://blog.csdn.net/x777777x/article/details/141092913?spm=1001.2014.3001.5506)
>[Windows官方文档-WSL](https://learn.microsoft.com/zh-cn/windows/wsl/)

# 一、什么是WSL
> 适用于 Linux 的 Windows 子系统（WSL）允许开发人员直接在 Windows 上运行 GNU/Linux 环境（包括大多数命令行工具、实用工具和应用程序），无需传统虚拟机或双启动设置的开销。

官方解释很清楚，WSL就是微软提供的一个类似于轻量级虚拟机的功能。比VMwarm更轻量化。

用处

 - 同时，在windows平台下的shell终端内，能运行Linux命令
 - 运行jupyter内核，有的notebook，比如Andrew Ng 吴恩达老师的机器学习课程中的Lab代码会调用Linux的系统命令。

# 二、启用window子系统及虚拟化
这里建议使用命令行方式，因为图形化界面可能每个终端设备不一样

```powershell
Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Windows-Subsystem-Linux
Enable-WindowsOptionalFeature -Online -FeatureName VirtualMachinePlatform
```
`启用服务后需要重启电脑`
# 三、自动安装
这里不推荐手动安装，二者几乎没有区别，手动安装的下载过程，会受国际结点影响，会非常非常非常慢！

```powershell
wsl --list --online
```
查看可以安装的发行版列表

```powershell
wsl --install -d Ubuntu-24.04
```
我安装的这个版本

 - 等待下载
 - 输入账号名
 - 重复两次密码
 - 安装完成

查看是否安装完成

```powershell
wsl -l -v
```
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/b74d3f992c914d5fab9face37b1ffc54.png)
# 四、移动到D盘
默认情况下，WSL 的虚拟硬盘（ext4.vhdx）存在 C 盘，可能占用大量空间。

 1. 导出当前WSL发行版
  > 记住上面的name，在D盘新建一个备份文件夹这里是 `D:\wsl-backup`，存放`tar`文件
  > 再新建一个 `D:\wsl`，用于新的WSL
```bash
wsl --export Ubuntu-24.04 D:\wsl-backup\ubuntu.tar
```
2. 导入安装
```bash
wsl --import Ubuntu D:\wsl\ubuntu D:\wsl-backup\ubuntu.tar --version 2
wsl --import <新的Linux名称> <导入盘的路径> <导入tar包路径> 版本(代表wsl2)
```

3. 检查结果
```powershell
wsl -l -v
```


![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/e3c16c5699a046c7914432862630ff81.png)
新文件夹`D:\wsl\ubuntu`中有一个`ext4.vhdx`。代表移动成功了

4. 删除旧版本

```bash
wsl --unregister Ubuntu-24.04
```

5. 设置默认用户
>因为 --import 一般默认以 root 启动，我们需要恢复原来的用户名（比如 yourname）
这里可以查看一下Ubuntu命令行，如果是之前的账户就不用设置了




# 五、图形化界面
WSL只支持单一图形化界面
由于需要安装的太多，大家按需自取于官方文档
[官方文档——GUI界面](https://learn.microsoft.com/zh-cn/windows/wsl/tutorials/gui-apps)
打开可以使用Linux终端命令
也可以直接在开始菜单的全部中找到相关快捷方式
![在这里插入图片描述|475](https://i-blog.csdnimg.cn/direct/7c89e57b668f4f85b83dd2847aae4064.png)
每次打开太过麻烦，建议右键打开文件所在位置，复制这些快捷方式到，桌面的一个文件夹里。或者将这些快捷方式固定到开始菜单


# 六、一些常用命令
```
以下命令在Powershell中
wsl 或 wsl -d Ubuntu						启动当前发行版	
wsl -l -v	    						    查看目前的版本和状态
wsl --terminate Ubuntu				   		 停止运行当前Linux系统
wsl --shutdown								停止运行wsl，把内存释放给windows
```


# 七、安装miniconda

[Conda](conda.md)
```
conda activate name                 激活虚拟环境
echo $CONDA_DEFAULT_ENV             查看当前环境
```

