# windows

## Junction

|对比|Junction|快捷方式（`.lnk`）|
|---|---|---|
|使用方式|程序访问这个目录时，会直接进入目标目录|通常要用户点击快捷方式打开目标|
|对软件是否透明|大多数程序会把它当作普通目录使用|程序通常只会看到一个 `.lnk` 文件，不会自动读取目标|
|Git / 终端|通常可按目录访问和处理|通常不会把它当成目录|
|适用场景|让 Obsidian、Git、构建工具都访问同一份文件|桌面上放一个方便打开文件夹的图标|
比如，在文件夹`A`是一个Repo，文件夹`B`里有文件需要提交到 Repo，如 Obsidian 的 Vault 中的部分文件，可以通过 Junction 的方式同步。

```bash
cmd /c mklink /J 'A路径''B路径'
Get-Item 'A' | Select-Object FullName, LinkType, Target
```

1. A 指向 B，B 是上游文件夹
2. 使用绝对路径
