## 初始化环境

1. 申请机器；
2. 连接 `\\192.168.91.253`，获取安装文件；
    - `MOPassiveSetup` 安装程序
    - `MaxOpticsStudio__SetLocalServer` 设置 `License` 服务 `bitanswer.max.com`
3. 关闭防火墙；
    - 命令行执行：Win + R，打开CMD，运行 `netsh advfirewall set allprofiles state off`
    - Windows Defender 防火墙：Win + R，运行 `Firewall.cpl`

## 防火墙

```powershell
# 查看当前防火墙状态
netsh advfirewall show allprofiles
# 关闭防火墙
netsh advfirewall set allprofiles state off
# 开启防火墙
netsh advfirewall set allprofiles state on
# 恢复初始防火墙设置
netsh advfirewall reset
# 显示操作系统信息，例如：系统版本、内存等
systeminfo
```

![[assets/work-records/windows-settings/IMG-20260430171340362.png]]

Ref

[cmd命令行配置windows防火墙 - 熊未泯 - 博客园](https://www.cnblogs.com/xiongweimin/articles/14192710.html)
[cmd怎么打开i防火墙-百度经验](https://jingyan.baidu.com/article/36d6ed1f22d3c25ace48835a.html)

## Scoop

> 安装Scoop报错：Running the installer as administrator is disabled by default

```shell
iex "& {$(irm get.scoop.sh)} -RunAsAdmin"
```

[安装Scoop报错](https://blog.csdn.net/test_write/article/details/129089494)

## 相关笔记

- [[work-records/mac-tips]] — Mac 环境设置（对比参考）
- [[work-records/shell-scripts]] — Shell 脚本（含 PowerShell 示例）
