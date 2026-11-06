# gcloud

## 一、安装 Google Cloud SDK

### 1. 下载与启动安装程序

最初尝试通过远程脚本自动配置 ADC（`powershell -c "iex (irm https://storage.googleapis.com/cloud-samples-data/adc/setup_adc.ps1)"`），但因本机尚未安装 `gcloud` CLI，需先下载官方安装包进行安装。

在 PowerShell 中执行以下命令下载并启动官方安装程序：

```powershell
(New-Object Net.WebClient).DownloadFile("https://dl.google.com/dl/cloudsdk/channels/rapid/GoogleCloudSDKInstaller.exe", "$env:Temp\GoogleCloudSDKInstaller.exe")
& $env:Temp\GoogleCloudSDKInstaller.exe
```

安装路径选择自定义目录：`E:\Google\Cloud SDK`（勾选安装 Bundled Python 并添加到环境变量 `PATH`）。

### 2. 验证安装

安装完成后，**新开一个 PowerShell 终端**，执行以下命令验证：

```powershell
gcloud --version
```

---

## 二、初始化与核心配置流程

### 1. 初始化与登录账号

```powershell
# 启动初始化向导（包含网络诊断与浏览器 OAuth 登录）
gcloud init

# 若需单独重新登录账号
gcloud auth login
```

浏览器会弹出 Google 账号授权页面，使用你的 Google 账号登录并完成授权。

### 2. 创建项目并设为默认项目

Google Cloud 要求 `PROJECT_ID` 全局唯一（不可与全球任何已有项目重名）：

```powershell
# 创建新项目（指定全局唯一的 PROJECT_ID 与显示名称）
gcloud projects create my-google-cloud-project --name="My Google Cloud Project"

# 将该项目设为全局默认项目
gcloud config set project my-google-cloud-project

# 查看当前配置与项目列表
gcloud config list
gcloud projects list
```

### 3. 绑定结算账户（Billing Account）

调用 Vertex AI 等云服务前，必须将项目关联到处于开启状态（`OPEN=True`）的结算账户：

```powershell
# 1. 查询当前账号下的结算账户 ID（ACCOUNT_ID）
gcloud billing accounts list

# 2. 将项目绑定到结算账户（替换为实际的 ACCOUNT_ID）
gcloud billing projects link my-google-cloud-project --billing-account=YOUR_BILLING_ACCOUNT_ID

# 3. 验证项目结算绑定状态（确认 billingEnabled: true）
gcloud billing projects describe my-google-cloud-project
```

### 4. 启用 Vertex AI API

```powershell
gcloud services enable aiplatform.googleapis.com --project=my-google-cloud-project
```

### 5. 配置本地应用默认凭据（ADC）

为了让本地 SDK、Magpie 或各类 AI 客户端直接通过 Google Cloud 鉴权调用模型，需配置 Application Default Credentials (ADC)：

```powershell
# 1. 登录并生成本地 ADC 凭据文件
gcloud auth application-default login

# 2. 为 ADC 绑定配额项目（Quota Project）
gcloud auth application-default set-quota-project my-google-cloud-project

# 3. 测试能否正常获取 Access Token
gcloud auth application-default print-access-token
```

成功后，凭据文件保存在当前 Windows 用户的 Google Cloud 配置目录中。

---

## 三、遇到的问题与解决办法

### 问题 1：安装过程中组件下载失败（`SSLError` / `IncompleteRead`）

- **报错现象**：
  - 第一次安装（默认 C 盘路径）拉取 `gsutil` 时中断：

    ```text
    ERROR: (gcloud.components.update) The component [gsutil] failed to download.
    HTTPSConnectionPool(host='dl.google.com', port=443): Max retries exceeded ... Caused by SSLError(SSLEOFError(8, '[SSL: UNEXPECTED_EOF_WHILE_READING]'))
    ```

  - 第二次安装（改到 `E:\Google\Cloud SDK`）拉取 `bq` 时中断：

    ```text
    ERROR: (gcloud.components.update) The component [bq] failed to download.
    ('Connection broken: IncompleteRead(1762634 bytes read, 505068 more expected)')
    ```

- **原因**：`GoogleCloudSDKInstaller.exe` 只是引导程序，实际安装会调用 `gcloud components update` 从 `dl.google.com` 下载 `gsutil`、`bq` 等大体积 `.tar.gz` 组件包。若本地代理连接不稳定或未走代理，极易中途断流。
- **解决办法**：确保本地代理（如 `127.0.0.1:7897`）节点稳定后，重新运行 `& $env:Temp\GoogleCloudSDKInstaller.exe` 覆盖安装，组件可断点续装并完成 Python 预编译。

---

### 问题 2：安装后执行 `gcloud` 提示找不到命令或参数错误

- **报错现象**：
  - 在原 PowerShell 窗口执行 `gcloud` 提示不是内部或外部命令。
  - 误输 `gcloud gcloud` 报 `ERROR: (gcloud) Invalid choice: 'gcloud'`。
- **原因**：安装器修改系统 `PATH`（添加 `E:\Google\Cloud SDK\google-cloud-sdk\bin`）后，已打开的旧终端会话不会自动刷新环境变量。
- **解决办法**：关闭旧终端，重新打开新的 PowerShell 窗口，使用 `gcloud --version`（或 `gcloud -v`）验证。

---

### 问题 3：创建项目报 `Project ID already in use` 及 `403 Forbidden`

- **报错现象**：
  - 执行 `gcloud projects create ai-research-2026 --name="AI Research"` 时报错：

    ```text
    ERROR: (gcloud.projects.create) Project creation failed. The project ID you specified is already in use by another project. Please try an alternative ID.
    ```

  - 紧接着执行 `gcloud projects describe ai-research-2026` 报错：

    ```text
    ERROR: (gcloud.projects.describe) [ACCOUNT_EMAIL] does not have permission to access projects instance [ai-research-2026] (or it may not exist): The caller does not have permission
    ```

- **原因**：Google Cloud 的 `PROJECT_ID` 是**全球唯一**的（非账号内唯一）。`ai-research-2026` 已被全球其他用户抢先注册，因此既无法创建同名 ID，也无权查看别人的项目详情。
- **解决办法**：为 `PROJECT_ID` 设置一个全局唯一的名称，例如 `my-google-cloud-project-2026`。

---

### 问题 4：执行 `gcloud services list` 报 `The required property [project] is not currently set`

- **报错现象**：

  ```text
  ERROR: (gcloud.services.list) The required property [project] is not currently set.
  ```

- **原因**：首次运行 `gcloud init` 时，最后一步交互式创建项目因 ID 冲突失败退出，导致本地 `[default]` 配置中尚未写入默认 `project`。
- **解决办法**：创建好新项目后，显式执行一次全局默认项目绑定：

  ```powershell
  gcloud config set project my-google-cloud-project
  ```

---

### 问题 5：ADC 登录报 `cloud-platform scope is required but not consented`

- **报错现象**：
  执行 `gcloud auth application-default login` 并在浏览器点击登录后，终端报错：

  ```text
  ERROR: There was a problem with web authentication. Try running again with --no-browser.
  ERROR: (gcloud.auth.application-default.login) https://www.googleapis.com/auth/cloud-platform scope is required but not consented. Please run the login command again and consent in the login page.
  ```

- **原因**：在浏览器弹出的 Google OAuth 细分权限授权页中，漏勾了「查看、编辑、配置和删除您的 Google Cloud 数据」复选框，导致颁发的 Token 只有 `openid` 和 `userinfo.email` 权限，缺少核心的 `cloud-platform` 权限范围（Scope）。
- **解决办法**：重新运行 `gcloud auth application-default login`，在浏览器授权页面**勾选所有权限复选框**后再点击继续。

---

### 问题 6：CLI 创建的项目在 Google Cloud Console 网页端看不到

- **现象**：`gcloud projects list` 能看到新建项目和 `My First Project`，但打开网页控制台只看得到 `My First Project`。
- **原因**：
  1. 账号下可能存在组织资源，网页端初始项目 `My First Project` 归属在该组织下。
  2. 使用 `gcloud projects create` 创建项目时未传 `--organization` 参数，新项目默认归属于**无组织（No organization）**。
  3. 网页端项目选择器默认按某个组织过滤（或停留在 `Recent` 最近列表），将无组织项目隐藏了。
- **解决办法**：
  - **临时查看**：在网页端左上角项目选择器的下拉框中切换为 **无组织 (No organization)** -> **全部 (All)**。
  - **彻底解决（将项目迁入组织下）**：

    ```powershell
    # 1. 查看组织 ID
    gcloud organizations list

    # 2. 为当前账号补充项目 IAM 管理员权限
    gcloud projects add-iam-policy-binding my-google-cloud-project --member="user:ACCOUNT_EMAIL" --role="roles/resourcemanager.projectIamAdmin"

    # 3. 安装 beta 组件并将项目移动到组织下
    gcloud components install beta
    gcloud beta projects move my-google-cloud-project --organization=ORGANIZATION_ID

    # 4. 验证项目的 parent 已变为指定组织
    gcloud projects describe my-google-cloud-project
    ```

---

### 问题 7：能否通过 `gcloud` 查询 $300 新人赠金（Credit）余额？

- **结论**：**不能直接通过 `gcloud` 查询剩余赠金。**
- **原因与排查方法**：
  1. `Cloud Billing API` 与 `gcloud billing` 目前仅支持查看结算账户开关状态（`gcloud billing accounts list`），未开放 Promotional Credits / Free Trial 剩余额度的查询接口。
  2. **查看剩余赠金**：需前往网页端 [Google Cloud Console - Billing](https://console.cloud.google.com/billing) 的 **概览 (Overview)** 或 **赠金 (Credits)** 页面查看 **Remaining value**。
  3. **多轮对话后 Credit 余额未减少的原因**：Billing 账单抵扣通常有数小时至 24 小时延迟，或单次请求成本低于 `$0.01`。若需实时确认请求是否打到该项目，可在网页端 **APIs & Services -> Dashboard** 查看 `Vertex AI API` 的实时请求曲线。
