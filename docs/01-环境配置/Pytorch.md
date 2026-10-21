# PyTorch 安装

## 安装 PyTorch

1. 安装miniconda
2. 开启虚拟环境

安装GPU版本的pytorch
- 注意检查自己的cuda版本
- 这里从国外源下载，可能会和先前配置的清华源冲突
```bash
nvidia-smi            检查N卡的版本
conda install pytorch torchvision torchaudio pytorch-cuda=12.4 -c pytorch -c nvidia
```
