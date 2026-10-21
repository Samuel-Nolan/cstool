> [!note]
> 以下操作以学习 Stanford-CS336 为例

## 一、新建new repo
1. Repository name: Stanford-CS336
2. Description: Learning material for Stanford-CS336: Language Modeling From Scratch
	- 会显示在repo简介、Readme第一行、右侧About栏
3. Readme: 
	- 勾一下开启
4. license:
	- 可不选


## 二、在本地文件夹
```bash
git init      # 成为一个git仓库
git branch -M main 
git remote add origin https://github.com/你的用户名/仓库.git # 连接推送仓库地址
```

- 因为 GitHub 现在默认主分支叫 main，而旧版 Git 初始化时可能默认叫 master。所以执行 git branch -M main 可以确保本地主分支也叫 main，后面推送时不会因为分支名不一致报错。

```bash
git remote -v
```
- 输出里会出现 `(fetch)` 和 `(push)`：
    - `(fetch)` 表示从这个地址拉取代码；
    - `(push)` 表示向这个地址推送代码。
- origin 指向你自己的仓库，你可以往这里 push；
- upstream 指向课程官方仓库，你主要从这里 fetch 最新代码。


接下来可以在本地修改并提交了，如果是以学习为目的，还需要克隆部分项目源码
## 三、clone
```bash
git clone https://github.com/stanford-cs336/assignment1-basics.git assignment1
```
- 这里只克隆了assignment1
- **注意：** 克隆的文件夹中有隐藏的.git，需要整个删掉

````bash
git pull --rebase origin main
````
- 从远程仓库 origin 的 main 分支拉取最新代码，并把你的本地提交“搬到”最新远程提交之后，保持提交历史是一条直线
- 之后就可以add assignment1了


**以上一切都可以在 VScode 中完成，更加方便** 😉

---

## 合作项目

1. 先fork到自己的github
2. 在本地文件夹中直接克隆，不需要新建repo和git init
3. 添加upstream `git remote add upstream <https>`







## 日常修改commit

```bash
git add .     # 将所有更改提交到暂存区
git add <文件名>  # 或者这种方法

git commit -m “描述”
git push origin main # 推送到远程仓库
```


### commit规范
`动作(文件): 改变内容`

|type|什么时候用|示例|
|---|---|---|
|`feat`|新增功能/完成作业主体内容|`feat: add assignment1 solution`|
|`fix`|修复错误、测试失败|`fix: correct gradient computation`|
|`docs`|改 README、注释、报告|`docs: update assignment1 report`|
|`refactor`|重构代码，不改变功能|`refactor: simplify data loader`|
|`test`|新增或修改测试|`test: add unit tests for tokenizer`|
|`chore`|配置、依赖、脚本等杂项|`chore: add .gitignore`|
|`style`|只改格式，不影响逻辑|`style: fix indentation`|
|`perf`|性能优化|`perf: reduce memory usage in training`|


```bash
git status   # 暂存区有哪些文件
git diff --cached # 查看暂存区的修改
```

## log & rest

```bash
git log
```
有commit的唯一id，作为版本回退

```bash
git rest <commit id>
```