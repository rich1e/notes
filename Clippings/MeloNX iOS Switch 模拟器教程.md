---
title: MeloNX iOS Switch 模拟器教程
source: https://www.onmyodev.com/2026/05/melonx/
author:
  - "[[杏川铭心]]"
published: 2026-05-02
created: 2026-07-02
description: 本文介绍了如何使用 MeloNX 模拟器在 iOS 系统上运行 Switch 游戏。模拟器对系统有特殊要求，因此配置起来较复杂。还介绍了一款叫做 MeloVertex 的改版，该改版重点针对人森进行了优化，同时降低了内存使用量。
tags:
  - clippings
  - MeloNX
  - Switch
  - game
---
![[assets/Clippings/MeloNX iOS Switch 模拟器教程/IMG-20260702164637956.png]]

发表于 2026年5月2日

MeloNX 是 iOS 平台的一款 Switch 模拟器。因为模拟的平台很新，对设备和安装方式都有很高的要求。

**2026.05.24 更新：** 目前出现了一款改版叫 MeloVertex，主要是解决人森（朋友收集：梦想生活）闪退的问题，并且增加了一点额外的优化，想玩人森的记得下这个改版。

## 设备要求

对于无法安装 TrollStore 的设备，如果你使用的是 iPhone，那么你 **必须** 拥有 4GB 以上的内存。如果使用的是 iPad，那么 **必须** 有 8GB 以上的内存，除非你拥有一个付费开发者账户。注意是账户，货真价实的开发者账户，网上买一个证书是没有用的！

对于可以安装 TrollStore 的设备，那么对内存的要求会少很多，不过仍然不建议在过于老旧的设备上安装。由于这些设备安装起来非常容易，下文只会介绍不支持 TrollStore 设备的安装流程。

## 下载 MeloNX

MeloNX 托管在自建的 Forgejo 实例上，可以从这里下载： [版本发布 – projects/MeloNX – Ryubing Forgejo](https://git.ryujinx.app/projects/MeloNX/releases)

**2026.05.24 更新：** MeloVertex 改版下载地址： [Releases · VertexSelection/MeloVertex](https://github.com/VertexSelection/MeloVertex/releases)

注意手机和电脑上都要下载一份。

## 安装 MeloNX

官方推荐的侧载工具是 [PlumeImpactor](https://www.onmyodev.com/2026/05/plumeimpactor/) ，原因是该工具可以正常签出 Increased Memory Limit 这个 Entitlement。但不管使用什么工具，还是需要在设备上安装 [SideStore](https://www.onmyodev.com/2025/12/sidestore-ios-%e4%be%a7%e8%bd%bd%e6%95%99%e7%a8%8b/) 作为续签工具。

另外虽然官方说不支持 LiveContainer，但笔者实际测试下来是可以正常使用的。

### 使用 PlumeImpactor

已经迁移至独立教程： [PlumeImpactor 侧载工具](https://www.onmyodev.com/2026/05/plumeimpactor/)

### 仅使用 SideStore

仅使用 SideStore 的话也是可以的，首先正常安装 MeloNX。

由于 SideStore 无法签出 Increased Memory Limit 这个 Entitlement，因此 MeloNX 无法正确运行，需要参考 [使用 Get More RAM 解决 LiveContainer 运行内存不足](https://www.onmyodev.com/2026/04/livecontainer-increased-memory/) 中的方法，为 MeloNX 启用该 Entitlement。

只需要确保你选择的包是 com.stossy11.MeloNX.XXXXXXXXXX 即可。

![[assets/Clippings/MeloNX iOS Switch 模拟器教程/IMG-20260702164637962.jpeg|300]]

接下来需要在 SideStore 中再安装一次 MeloNX，才能正确使模拟器获取更多内存。同样，只要保证 MeloNX 不掉签，就可以一直保留该 Entitlement。如果忘记续签导致掉签，那么需要重做一遍上面的流程。

### 仅使用 LiveContainer

官方不太推荐这种方法，但很神奇的是我手机上只有 LiveContainer 是正常的，直接安装的版本反而有问题……

首先需要安装 [LiveContainer](https://www.onmyodev.com/2025/12/livecontainer-%e6%95%99%e7%a8%8b/) 。

接下来在 LiveContainer 中安装 MeloNX，并且启用“带 JIT 启动”和“修复文件导入”。

![[assets/Clippings/MeloNX iOS Switch 模拟器教程/IMG-20260702164637969.jpeg|300]]

同样这个时候你的 LiveContainer 很可能没有大内存权限，参考 [使用 Get More RAM 解决 LiveContainer 运行内存不足](https://www.onmyodev.com/2026/04/livecontainer-increased-memory/) 即可。

操作完不要忘记使用 SideStore 或 iLoader 重装一遍 LiveContainer。

iOS 26+ 的用户可能会看到 JIT 脚本的选项，这个东西不能省略，后面我们会讲解如何添加这个 JIT 脚本。

## 配置 StikDebug

目前只有这款 JIT 启用工具还能用一用了，别的死的很彻底。

参考 [新版 StikDebug 启用 JIT 教程，支持 iOS 26](https://www.onmyodev.com/2026/04/stikdebug-jit-new/) 即可。

### 配置 JIT 脚本

iOS 26+ 需要配置 JIT 脚本，对于独立安装的 MeloNX（使用 PlumeImpactor 或 SideStore），直接使用内置的 universal.js 即可，如图。

![[assets/Clippings/MeloNX iOS Switch 模拟器教程/IMG-20260702164637974.jpeg|300]]

如果使用的是 LiveContainer 中的 MeloNX，那么需要在 MeloNX 的设置中导入这个脚本以进行传递。

『来自123云盘VIP会员杏川铭心的分享』JIT 脚本  
链接： [https://1818749673.share.123865.com/123pan/EzfHjv-FCAKh?pwd=UHI3#](https://1818749673.share.123865.com/123pan/EzfHjv-FCAKh?pwd=UHI3#)  
提取码：UHI3

## 获取密钥和固件

这里推荐一个网站，prodkeys.net，注意识别诈骗广告。

下载密钥： [https://prodkeys.net/ryujinx-prod-keys-update/](https://prodkeys.net/ryujinx-prod-keys-update/)

下载固件： [https://prodkeys.net/firmwares/](https://prodkeys.net/firmwares/)

就不打超链接了，毕竟不是什么光彩的东西 ，请手动复制到浏览器打开。

目前最新版的固件是 v22.1.0。本人下载的是 v19.0.1，没有别的原因，而是我作为国行烈士，主机永远地停在了这个版本……表示缅怀……

注意不是让你去下载 v19.0.1！比较新的游戏这个版本肯定就玩不了啦，建议选择最新的可以正常工作的版本。

## 导入密钥和固件

启动 MeloNX，会提示你导入这两个东西。

![[assets/Clippings/MeloNX iOS Switch 模拟器教程/IMG-20260702164637995.jpeg|300]]

注意导入密钥的时候需要同时勾选 prod.keys 和 title.keys 两个文件，如图。

![[assets/Clippings/MeloNX iOS Switch 模拟器教程/IMG-20260702164637998.jpeg|300]]

然后导入固件，注意固件不要解压，直接导入整个.zip 文件即可。

全部完成后两个选项右侧都会显示一个绿色的勾，此时就可以点击 Finish Setup。

![[assets/Clippings/MeloNX iOS Switch 模拟器教程/IMG-20260702164638002.jpeg|300]]

## 向 MeloNX 导入游戏

直接把游戏 ROM 放入 MeloNX 数据文件夹的“roms”文件夹中即可。

如果有游戏更新、DLC 等附加数据，那么只需要长按游戏，点击对应的选项，例如“Update Manager”，即可导入。

![[assets/Clippings/MeloNX iOS Switch 模拟器教程/IMG-20260702164638005.jpeg|300]]

另外如果你是在 LiveContainer 中安装的 MeloNX，那么数据文件夹不一定好找。此时可以在 LiveContainer 中长按，点击“打开数据文件夹”，然后打开“Documents”。

![[assets/Clippings/MeloNX iOS Switch 模拟器教程/IMG-20260702164638007.jpeg|300]]

![[assets/Clippings/MeloNX iOS Switch 模拟器教程/IMG-20260702164638010.jpeg|300]]

注意我这个是全部设置完成之后的状态，如果你是刚刚安装好那么可能会长得不太一样。

也可以在 MeloNX 设置中添加额外的 ROM 文件夹，不过不推荐这么做。

以及 ROM 自己找，我可不会告诉你哪里有 ROM 可以下，不然真的要寄了 

## 测试 MeloNX

尝试启动 ~~马里奥没课吐~~ 马里奥制造二：

![[assets/Clippings/MeloNX iOS Switch 模拟器教程/IMG-20260702164638019.jpeg|450]]

可以看到正常启动，安装成功。

## 常见问题

### 模拟器闪退/运行不了

请首先检查是否已经启用了 Increased Memory Limit。与许多软件不同，该 Entitlement 对 MeloNX 来说是必需品，无法绕过。MeloNX 的设置页会显示你是否已经启用了这个 Entitlement：

![[assets/Clippings/MeloNX iOS Switch 模拟器教程/IMG-20260702164638022.jpeg|300]]

如果已经启用了该 Entitlement，但还是无法运行游戏，那么请检查设备内存是否足够。如果你 iPhone 的内存低于 4GB，或者 iPad 的内存低于 8GB，那么是无法使用的，除非你拥有付费开发者账户。在这种情况下，请确保你签名的时候还启用了 Extended Virtual Addressing 这个 Entitlement。

如果设备性能足够，而且必要的权限也全部开启，那么请检查是不是密钥和固件的版本太低。

### 卡在 Waiting for JIT

如果是独立的 MeloNX，那么请检查是否是从 StikDebug 中启动的 MeloNX。iOS 26 用户请检查自己的 JIT 脚本是否正确。如果是 LiveContainer 中的 MeloNX，那么请确保已经勾选了“带 JIT 启动”，iOS 26 用户请保证在 LiveContainer 中的对应设置里导入了正确的 JIT 脚本。

![[assets/Clippings/MeloNX iOS Switch 模拟器教程/IMG-20260702164638024.jpeg|300]]

不从 StikDebug 中启动 MeloNX 则无法运行游戏。同样 JIT 的要求是无法绕过的。

### 游戏卡在 40 帧

我甚至不知道会不会有人遇到和我一样的问题。但总之，如果你通过 [Nugget](https://www.onmyodev.com/2026/02/ios-nugget/) 或者 [Pocket Poster](https://www.onmyodev.com/2026/03/pocket-poster/) 配置了动态壁纸的话，那么 iOS 会分一部分性能给动态壁纸。然后你的游戏就会只剩下 40 帧。当然我的手机是只有 60 帧的，如果 120 帧的手机可能会卡在 80 帧？总之如果你感觉你的帧率没跑满，那么可以检查一下是不是动态壁纸的锅。

### 文件导入不了

这个主要是 LiveContainer 比较常见，导入前请确保已经在 LiveContainer 中勾选修复文件导入。

### 游戏是英文

检查 MeloNX 设置中是否已经将系统语言设置为简体中文（Simplified Chinese）。

转到“System”设置页，往下翻，然后将“System Language”修改为“Simplified Chinese”。

![[assets/Clippings/MeloNX iOS Switch 模拟器教程/IMG-20260702164638027.jpeg|300]]
