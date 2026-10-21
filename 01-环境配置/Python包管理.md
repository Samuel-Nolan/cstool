### 1. pip

### 2. conda
参见 [Conda 环境配置](conda.md)。

### 3. uv
|维度|uv|conda|
|:--|:--|:--|
|开发语言|Rust（极致性能）|Python / C++|
|核心定位|极速 Python 包管理器 + 项目管理器|跨语言环境管理器 + 包管理器|
|包来源|PyPI（纯 Python 生态）|Anaconda/conda-forge 频道（预编译二进制）|
|非Python依赖|❌ 不支持（仅管理 Python 包）|✅ 支持（C/C++库、CUDA、R、系统工具等）|
|速度|🚀 极快（比 pip 快 10-100x）|🐢 较慢（解析复杂依赖时尤为明显）|
|磁盘占用|轻量，全局缓存去重|较重，每个环境独立存储|

配置清华源：`setx UV_INDEX_URL "https://pypi.tuna.tsinghua.edu.cn/simple"`
