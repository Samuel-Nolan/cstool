>[!note] Hermes运行在VPS上，Debian13系统


## Hermes介绍
1. `hermes`本体
2. `hermes dashboard`：hermes自带的控制台
3. `hermes desktop`：对话型APP，无控制台
4. `hermes studio`或`hermes web-ui`：自带hermes镜像本体 + 改良版的hermes控制台


## 架构设计

```
/home/nolan/
│
├── docker/
│   └── hermes/
│       ├── compose.yml
│       └── .env                        保存隐私数据
│
├── .hermes/
│   ├── config/
│   ├── skills/
│   ├── memory/
│   ├── sessions/
│   └── workspace/
│
├──  backups/
│   └── hermes/
│
└── Tailscale（系统服务） 
	├── tailscale 
	└── tailscaled
```


#### 生成密码
> dashboard需要，使用hermes studio不需要

进入容器：
```bash
docker exec -it hermes bash
python -c "from plugins.dashboard_auth.basic import hash_password; print(hash_password('你的密码'))"
```
复制hash值，`exit`退出容器


### compose.yml
> Docker Compose 的配置文件

可以用bash命令
```bash
cat > ~/docker/hermes/compose.yaml <<'EOF'
YAML内容
EOF

```
或手动填写
```bash
cd ~/docker/hermes
nano compose.yaml\
docker compose down
docker compose up -d
```


```YAML fold group:compose tab:hermes
services:	
# 纯hermes的compose.yaml
  hermes:
    image: nousresearch/hermes-agent:latest
#    dns:
#      - 223.5.5.5
#      - 1.1.1.1
    container_name: hermes
    restart: unless-stopped

    command: gateway run

    ports:
      - "100.71.251.7:8642:8642"

    volumes:
      - /home/nolan/.hermes:/opt/data
      - /home/nolan/obsidian:/obsidian

    environment:
      HERMES_DASHBOARD: "0"
      HERMES_DASHBOARD_HOST: "0.0.0.0"
      HERMES_DASHBOARD_BASIC_AUTH_USERNAME: "nolan"
      HERMES_DASHBOARD_BASIC_AUTH_PASSWORD_HASH: '你的密码的hash值'
    deploy:
      resources:
        limits:
          memory: 1536M
          cpus: "1.8"
  hermes-studio:
    image: ekkoye8888/hermes-web-ui:latest
    container_name: hermes-studio
    restart: unless-stopped

    ports:
      - "100.71.251.7:6060:6060"      # Web UI 主端口（跟随你的内网绑定策略）
      - "100.71.251.7:8651:8651"      # 预览前端端口
      - "100.71.251.7:56121:56121"    # xAI OAuth 回调端口

    volumes:
      - /home/nolan/.hermes:/home/agent/.hermes
      - /home/nolan/.hermes/hermes-web-ui:/home/agent/.hermes-web-ui
      - /home/nolan/obsidian:/obsidian

    environment:
      - PORT=6060
      - HERMES_HOME=/home/agent/.hermes
      - HERMES_BIN=/opt/hermes/.venv/bin/hermes
      - HERMES_WEB_UI_MANAGED_GATEWAY=1
      - HERMES_WEB_UI_AUTH_JWT_EXPIRES_IN=30d
      - HERMES_WEB_UI_XAI_CALLBACK_BIND_HOST=0.0.0.0
      - PATH=/opt/hermes/.venv/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
      - HERMES_ALLOW_ROOT_GATEWAY=1
    stdin_open: true
    tty: true

    cpus: "1.8"
    mem_limit: 1400m           # 硬上限 = --memory
    memswap_limit: 2680m       # 内存+swap 总量 = --memory-swap（1400+1280）
    mem_reservation: 1024m     # 软限        = --memory-reservation    
```
```yaml fold group:compose tab:hermes-studio
services:
# 使用hermes studio的compose.yaml
  hermes-studio:
    image: ekkoye8888/hermes-web-ui:latest
    container_name: hermes
    restart: unless-stopped

    ports:
      - "100.71.251.7:6060:6060"      # Web UI 主端口（跟随你的内网绑定策略）
      - "100.71.251.7:8651:8651"      # 预览前端端口
      - "100.71.251.7:56121:56121"    # xAI OAuth 回调端口

    volumes:
      - /home/nolan/.hermes:/home/agent/.hermes
      - /home/nolan/.hermes/hermes-web-ui:/home/agent/.hermes-web-ui
      - /home/nolan/obsidian:/obsidian

    environment:
      - PORT=6060
      - HERMES_HOME=/home/agent/.hermes
      - HERMES_BIN=/opt/hermes/.venv/bin/hermes
      - HERMES_WEB_UI_MANAGED_GATEWAY=1
      # 关键：跳过 gateway 自动启动，微信连接由 hermes 容器独占，避免双 gateway 抢连接
      - HERMES_WEB_UI_DISABLE_GATEWAY_AUTOSTART=1
      - HERMES_WEB_UI_AUTH_JWT_EXPIRES_IN=30d
      - HERMES_WEB_UI_XAI_CALLBACK_BIND_HOST=0.0.0.0
      - PATH=/opt/hermes/.venv/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
      - HERMES_ALLOW_ROOT_GATEWAY=1
    stdin_open: true
    tty: true
    deploy:
      resources:
        limits:
          memory: 1024M
          cpus: "1.8"

```

`volumes`
这是整个配置最重要的一行之一：
```yaml
    volumes:
      - /home/nolan/.hermes:/home/agent/.hermes
    # 宿主机目录 : 容器目录
```

也就是：
```
Debian VPS

/home/nolan/.hermes
        │
        │ bind mount
        ▼
Docker

/opt/data
```
Hermes 官方 Docker 镜像规定：
```
/opt/data
```
是持久化数据目录，包括配置、API Key、Session、Skills、Memory 等。

**注意**：Compose 解析 `$` 导致 scrypt hash 被截断，用`$$`表示


## 一、安装Docker
[安装 Docker 软件教程](../01-环境配置/docker.md#二-从官方安装-docker-软件)


## 二、并建立 Hermes 的目录
```bash
sudo usermod -aG docker nolan   # 把用户加入docker组，以后不需要sudo权限使用docker
newgrp docker   # 让当前 Shell 立即加载新权限
docker ps       # 测试docker命令，不加sudo
```

```bash
mkdir -p ~/docker/hermes  # 创建 Hermes 部署目录
mkdir -p ~/.hermes        # 创建持久化数据目录
ls -ld ~/docker/hermes ~/.hermes    # 确认目录
```

理论上应该类似：
```text
drwxr-xr-x ... nolan nolan ... /home/nolan/docker/hermes
drwxr-xr-x ... nolan nolan ... /home/nolan/.hermes
```

检查一下 Docker 是否会开机自动启动：
```bash
systemctl is-enabled docker
# enable
```



## 三、初始化
```bash
docker run -it --rm \
  -v ~/.hermes:/opt/data \
  nousresearch/hermes-agent setup
```
- 这里创建了临时container，进入一个交互式终端运行，运行结束后自动rm
- 并把交互式配置读到的内容保存到Hermes的config中
- 把宿主机（阿里云 VPS）上的 `~/.hermes` 目录映射到容器内部的 `/opt/data`，就算删除container，`~/.hermes`这里的文件也不会丢
- 这里容器路径`/opt/dat`不是实际地址的，只是镜像作者选择的数据目录
容器内部文件结构：**程序代码** 和 **用户数据** 分离。
```
/opt
├── data         ~/.hermes的映射，完全一样，用户配置、数据库、聊天记录
└── hermes       Docker镜像内部自带的程序代码目录
```

## 四、下载Docker镜像
```bash
cd ~/docker/hermes
docker compose pull
docker compose up -d
docker ps
```

## Hermes文件结构
```fold
/.hermes
├── config.yaml                  # 主配置文件（7.8K）
├── config.yaml.bak.20260807_193448  # 配置备份
├── .env                         # 环境变量（密钥）
├── auth.json                    # 认证凭据
├── SOUL.md                      # 人设/灵魂文件
├── gateway.pid / gateway.lock   # 网关进程文件
├── gateway_state.json           # 网关运行状态（weixin 已连接）
├── gateway-starts.log           # 启动记录
│
├── 📁 skills/                   # 技能库（13 大类）
│   ├── autonomous-ai-agents/    #   hermes-agent、claude-code、codex 等
│   ├── creative/                #   ascii-art、manim-video、p5js 等
│   ├── email/  github/  media/  #   邮件、GitHub、媒体
│   ├── mlops/                   #   vllm、llama-cpp、evaluation
│   ├── note-taking/             #   obsidian
│   ├── productivity/            #   docx、xlsx、pdf、airtable 等
│   ├── research/                #   arxiv、blogwatcher 等
│   ├── smart-home/  social-media/  software-development/
│   └── apple/
│
├── 📁 sessions/                 # 会话记录
│   ├── sessions.json
│   └── request_dump_*.json      # 请求转储
│
├── 📁 memories/                 # 持久记忆
│   └── USER.md                  # 用户画像
│
├── 📁 cron/                     # 定时任务
│   ├── executions.db            # 执行记录库
│   ├── output/                  # 输出
│   └── ticker_heartbeat
│
├── 📁 logs/                     # 日志
│   ├── agent.log / errors.log / gateway.log
│   ├── container-boot.log / gui.log
│   └── gateways/
│
├── 📁 state/                    # 运行状态
│   ├── gateway.heartbeat
│   └── gateway.lifecycle.json
│
├── state.db (+wal/shm)          # SQLite 状态库（692K）
├── kanban.db                    # 看板库（118K）
├── projects.db                  # 项目库（45K）
├── models_dev_cache.json        # 模型缓存（3.6M）
│
├── 📁 platforms/                # 平台配置（weixin 等）
├── 📁 weixin/accounts           # 微信账号
├── 📁 hooks/  plans/  skins/    # 钩子、计划、主题
├── 📁 sandboxes/  workspace/    # 沙箱、工作区
├── 📁 image_cache/  images/     # 图片缓存
├── 📁 audio_cache/              # 音频缓存
├── 📁 bin/                      # uv / uvx 工具
├── 📁 lazy-packages/            # 延迟加载包（82 个）
├── 📁 cache/  .cache/  .local/  # 缓存
├── 📁 desktop/  pairing/        # 桌面、配对
└── 📁 pending_messages/         # 待发消息
```

| 文件          | 你宿主机上的位置                       | 容器内位置                          | 主要作用                        |
| ----------- | ------------------------------ | ------------------------------ | --------------------------- |
| `SOUL.md`   | `~/.hermes/SOUL.md`            | `/opt/data/SOUL.md`            | **定义 Hermes 是谁**            |
| `MEMORY.md` | `~/.hermes/memories/MEMORY.md` | `/opt/data/memories/MEMORY.md` | **Hermes 学到了什么 / 需要长期记住什么** |
| `USER.md`   | `~/.hermes/memories/USER.md`   | `/opt/data/memories/USER.md`   | **你是谁、你的偏好是什么**             |

- **可能需要执行**：`docker exec -u root hermes chown hermes:hermes /opt/data/memories/MEMORY.md`，把mermory.md的权限归还给hermes


## 问题

### 1. 内存不够了
最显著的特征就是打卡 Hermes Web 变卡了
1. **Resident Set Size（常驻集大小）**：RSS 是进程当前实际驻留在物理内存中的大小，包含私有内存和共享内存，但不包括已换出到磁盘的部分。**
2. **OOM （Out Of Memory）**：在 Linux 和容器场景里，会kill 进程 。当物理内存和 Swap 几乎耗尽、内核又回收不到足够内存时，内核会选一个进程强制杀掉，释放内存，防止整个系统崩溃
