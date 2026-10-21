# Jupyter Notebook 配置

> 通常使用 Conda 虚拟环境或者 WSL。


- **“jlab”** 通常是指 **JupyterLab**，它是 Jupyter Notebook 的下一代交互式开发环境
- 当启动 JupyterLab 时，会指定一个**起始目录**，这个目录就是 **jlab 的根目录**

在 `~/.jupyter/` 目录下有一个 `jupyter_notebook_config.py` 文件。


在`.bashrc`中添加如下函数，使用函数名`jn`输入，代替两行命令行代码
这里是`no-browser`，不过在运行成功后会有URL，`Ctrl + 单击`就能打开windows的默认浏览器
```bash
jn() {
    conda activate jupyter_learn
    jupyter notebook --notebook-dir="$HOME/jupyter_notebook/" --port=8888 --no-browser
}
```

## 安装

[Jupyter notebook--配置与使用【安装过程+环境配置+运行实例】-CSDN博客](https://blog.csdn.net/2301_80637569/article/details/142071630?ops_request_misc=elastic_search_misc&request_id=15c5de922cc34e3e924fa1cecaab20b6&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~top_positive~default-1-142071630-null-null.142^v102^pc_search_result_base9&utm_term=jupyter%20notebook&spm=1018.2226.3001.4187)

需要环境：
参见 [Conda 环境配置](conda.md)。

安装过程：
1. 启动虚拟环境
2. `conda install jupyter notebook`
3. 安装内核，``
	- Jupyter 是一个**网页编辑器**
	- 它自己**不能运行 Python**
	- 必须靠 **ipykernel** 这个 “翻译 + 执行器” 才能让代码跑起来
	- 没有它，Jupyter 会报错：**找不到内核 / 无法运行代码**

`python -m ipykernel install --user --name=myenv --display-name="ipykernel_name"`
- `--user` 表示安装是针对当前用户的；
- `--name=myenv` 指定了内核的名称，应与你的 Conda 环境名称一致；
- `--display-name="My Environment"` 设置了在 Jupyter Notebook 或 JupyterLab 的下拉菜单中显示的内核名称。
