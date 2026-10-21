# Codex 配置

## 客户端五次重连问题
1. 在 `~/.codex/.env`文件，如果没有就在命令行创建一个`New-Item -Path .env -ItemType File`
2. 在notepad中编辑，注意这里的端口号`7897`（一般都是），填自己的网络代理端口号

```
HTTP_PROXY=http://127.0.0.1:7897
HTTPS_PROXY=http://127.0.0.1:7897
```

3. 重启电脑或者在任务管理器中结束“ChatGPT”进程
