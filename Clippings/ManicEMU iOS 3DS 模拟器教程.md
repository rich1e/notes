---
title: ManicEMU iOS 3DS 模拟器教程
source: https://www.onmyodev.com/2026/05/manicemu/
author:
  - "[[杏川铭心]]"
published: 2026-05-19
created: 2026-07-02
description: 本文介绍了如何通过侧载安装 ManicEMU 模拟器的方式，在 iOS 上模拟 3DS 游戏，并介绍如何在侧载安装的 ManicEMU 中通过启用 JIT 的方式来优化 3DS 游戏的体验，如何导入 NAND 以解决缺失 Mii 的问题。
tags:
  - clippings
  - game
  - ManicEMU
  - 3DS
---
![[assets/%E6%88%AA%E5%B1%8F2026-05-19-21.50.36.png]]

最后编辑于 2026年5月19日

ManicEMU 是 iOS 上的一款模拟器，支持非常多的平台，什么 PS1、DC、J2ME、GBA……通通支持，也支持“导入” MeloNX 和 XeniOS 里的游戏，虽然这个所谓的导入功能只是在 ManicEMU 里显示一个游戏封面，点击之后就自动跳转那俩模拟器……其中一大亮点在于支持模拟 3DS 游戏，同时还支持通过导入真机 ROM 后，使用 Pretendo 网络进行联机，功能十分强大。

由于 3DS 很吃性能，且配置起来比较复杂，本文就着重以 3DS 平台来展开介绍。

## 安装 ManicEMU

ManicEMU 可以通过 App Store 和侧载安装。

### App Store 安装

这里要提醒一下，写 App Store 安装方式只是为了文章的全面性，并不是真的让你去商店安装。使用商店安装的 ManicEMU 无法启用 JIT，模拟老旧平台时够用，但模拟 3DS 平台时会遇到严重的性能问题。

[Manic EMU – 游戏模拟器 App – App Store](https://apps.apple.com/cn/app/manic-emu-%E6%B8%B8%E6%88%8F%E6%A8%A1%E6%8B%9F%E5%99%A8/id6743335790)

### 侧载安装

侧载安装时，软件会直接解锁除了 iCloud 同步外的所有功能，在 App 内显示为永久会员。不解锁 iCloud 不是因为软件恶心人，而是因为免费开发者没权限。虽然 App 内也会显示相关功能，但是无法使用。

在 GitHub 上下载最新版本： [Releases · Manic-EMU/ManicEMU](https://github.com/Manic-EMU/ManicEMU/releases)

也可以添加 AltSource，然后使用对应的侧载工具直接下载安装： [AltDirect](https://stikstore.app/altdirect/?url=https://apps.manicemu.site/altstore)

**不是说用了侧载安装就可以使用 JIT。用网上购买的证书侧载一样用不了 JIT。**

官方表明只支持 SideStore、AltStore 等直接安装，不支持 LiveContainer，但实际测试中发现 LiveContainer 一样可以运行。

## 带 JIT 启动 ManicEMU

参考： [新版 StikDebug 启用 JIT 教程，支持 iOS 26](https://www.onmyodev.com/2026/04/stikdebug-jit-new/)

其中 ManicEMU 使用的脚本叫做 manic.js。

## 修改 3DS 核心设置

ManicEMU 默认使用的是 Citra 核心，该核心不支持 JIT，因此需要切换成 Azahar 核心。

打开 ManicEMU 的设置，往下拉，找到模拟器核心这一项。

![[assets/Clippings/ManicEMU iOS 3DS 模拟器教程/IMG-20260702164712742.jpeg|300]]

然后把核心改成 Azahar。

![[assets/Clippings/ManicEMU iOS 3DS 模拟器教程/IMG-20260702164712745.jpeg|300]]

另外在这个设置页里还可以看见 JIT 的启用状态，就在模拟器核心入口的上面。如果显示的不是绿色的 JIT 可用，而是红色的 JIT 不可用，则说明操作有误，请检查你是否是从 StikDebug 中启动的 ManicEMU 而不是从桌面上直接打开。

## 向 ManicEMU 导入 3DS 游戏

接下来我们来导入一些 3DS 游戏吧！

需要注意的是，ManicEMU 只能支持解密好的游戏，或者自制软件（Homebrew）。如果一个游戏的 ROM 的安装说明里有关于“在 FBI 中导入 xxxx 密钥文件”的步骤则该游戏无法在 ManicEMU 上运行。

另外，如果你导入过真机的 NAND，那么可能会造成部分尽管是已经解密的游戏却依然无法游玩；但不导入 ROM 会使得需要 Mii 的游戏无法运行，因此需要自行取舍。

## 修改游戏高级设置

接下来需要实际启用 JIT。

点击一个游戏，打开菜单之后，往后翻找到高级设置。如果你点击游戏之后直接运行了那么说明你可能打开了快速启动这个选项，关掉即可。如果还是不行，那么需要注意的是，Home Menu 没有这个菜单，也不支持 JIT，请选择别的什么游戏进行操作。

![[assets/Clippings/ManicEMU iOS 3DS 模拟器教程/IMG-20260702164712748.jpeg|300]]

最上方有一个 use\_cpu\_jit，打开，然后保存。 **每个游戏都要这样操作一遍。**

![[assets/Clippings/ManicEMU iOS 3DS 模拟器教程/IMG-20260702164712750.jpeg|300]]

下方的 cpu\_scale 设置，请根据实际情况选择，不是说越高越好。你调成 400%，但是手机没有 400% 的性能，那也没有用。

## 其他注意事项

### 不要使用即时存档

3DS 因为算是比较近的一个世代了，模拟器不稳定，加上游戏相关的反作弊技术都比较成熟， **切记不要依赖于模拟器的即时存档。** ManicEMU 官方社区里每天都能看见人们在那里哀嚎，称自己的 3DS 游戏今天突然就打不开了，里面无一例外全是用的即时存档。一定要记得使用游戏内的存档，游戏内的存档永远是安全的。

### App Store 上的 ManicEMU

虽然上面已经提过一次了，但是我还是想再说一遍。

**App Store 上下载的 ManicEMU 无法用于开启 JIT。** 虽然你可以在 StikDebug 的 Other 这个标签页里找到 ManicEMU，但是没有用。那个东西点了只能让你启动 ManicEMU，但无法为其启用 JIT。如果要启用 JIT 则必须使用侧载安装的形式。

**不是说从 App Store 安装 ManicEMU 就玩不了 3DS 游戏了。** 只是你的体验会非常糟糕，轻轻松松达到电竞级帧率。

### 缺失 Mii、Mii 显示不正常

这种情况需要使用 Artic Base 功能向你的 ManicEMU 中传输一份真机的数据。如果你没有真机，那么就需要在网上寻找 nand.zip，并且直接解压并覆盖 ManicEMU 文件夹中的 3DS 文件夹。

![[assets/Clippings/ManicEMU iOS 3DS 模拟器教程/IMG-20260702164712752.png|300]]

最后放一张马造 3DS 的截图：

![[assets/Clippings/ManicEMU iOS 3DS 模拟器教程/IMG-20260702164712754.png|300]]

恭喜你！你可以在 iOS 上游玩你喜爱的 3DS 游戏了。