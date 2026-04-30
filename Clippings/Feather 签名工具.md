---
title: Feather 签名工具
source: https://www.onmyodev.com/2026/03/feather/
author:
  - "[[杏川铭心]]"
published: 2026-03-20
created: 2026-04-27
description: 本文介绍了 Feather 这款机上签名工具的使用，软件使用起来类似国内的万能签等工具，支持插件注入、随机包名、机上安装等使用功能，还支持 AltStore/SideStore 所使用的软件源，不过只能搭配付费开发者证书进行使用。
tags:
  - clippings
  - Feather
  - iOS
  - sideload
---
![[assets/Clippings/Feather 签名工具/IMG-20260430101511124.jpeg]]

发表于 2026年3月20日

[AltStore](https://www.onmyodev.com/2023/08/ios-altstore%e4%be%a7%e8%bd%bd%e5%b7%a5%e5%85%b7%e4%bd%bf%e7%94%a8%e6%95%99%e7%a8%8b/) ， [SideStore](https://www.onmyodev.com/2025/12/sidestore-ios-%e4%be%a7%e8%bd%bd%e6%95%99%e7%a8%8b/) 都是很有名的 iOS 机上侧载，就算选择完全使用电脑，也有诸如 PlumeImpactor，iLoader 之类的工具供我们选择。不过这些工具都有一个特点，那就是各类功能都是基于“用户正在使用免费开发者账户”这个假设上的。一个后果就是，付费开发者使用这些工具的时候并不算特别方便，至少没有很多付费开发者理应可以享受到的功能。

于是乎一款专为付费开发者设计的签名工具出现了，它就是 Feather。至于为什么是 **签名** 工具而不仅仅说是侧载工具，如果你的屏幕够大的话，或许你已经知道了，不够大那就往下翻一翻。

目录

## Feather 的功能

全能签

好吧说这个东西就是全能签未免有点掉价了，我们还是来看看 Feather 都有什么功能。

### 软件源

和全能签（轻松签、万能签）不同，它们的软件源已经是一条完整的黑灰产产业链了，自带有解锁码的功能来要求付费，Feather 所使用的软件源格式和 AltStore/SideStore 是一样的，都是 AltSource，软件内也可以直接导入 SideStore 的推荐软件源（换句话说，没有绿泡泡之类的玩意）：

[![[assets/Clippings/Feather 签名工具/IMG-20260430101511160.png|在 Feather 中添加和管理软件源。]]](https://www.onmyodev.com/wp-content/uploads/2026/02/IMG_8603.png)

### 插件注入

Feather 有相对完善的 Substrate/ **ElleKit** 插件注入机制，可以直接将.dylib/.deb 格式的插件注入要签名的软件内。注意哦，用的是货真价实的越狱插件注入器，而不是像 LiveContainer 那样，只能用 TweakLoader.dylib 注入独立的.dylib 格式的插件。

因为不玩越狱了，手上没有插件包，很遗憾不能给大伙演示。

### 随机包名

苹果对使用付费开发者账户进行盗版的行为是零容忍的，如果发现了一张证书被用于签名的软件在 App Store 上有一个一模一样的包名，而且该软件还是付费软件，那么证书和 Apple ID 会被直接拉黑。

Feather 有一个功能，称为 PPQ 保护，可以在签名的时候，在包名后加上一段长长的随机字符串，来绕过苹果的监管。可以在设置页的“签名选项”中找到这个功能：

[![[assets/Clippings/Feather 签名工具/IMG-20260430101511189.png|在 Feather 中启用 PPQ 保护。]]](https://www.onmyodev.com/wp-content/uploads/2026/02/IMG_8604.png)

### 强制 Liquid Glass

Feather 还可以在签名的时候修改框架信息来强制软件使用 iOS 26 的 Liquid Glass。同样是在签名选项里，拉到最底下就可以看见了：

[![[assets/Clippings/Feather 签名工具/IMG-20260430101511226.png|启用 Liquid Glass。]]](https://www.onmyodev.com/wp-content/uploads/2026/02/IMG_8605.png)

### 机上安装

Feather 同样支持那个被玩烂的 [Pairing File](https://www.onmyodev.com/2025/12/pairing-file-%e6%95%99%e7%a8%8b/) + 本地回环来实现自己连接自己然后安装的功能，这样在安装软件的时候完全不需要经过外部服务器。

可以在设置页的“安装”里找到这个功能，只需把“安装类型”从“服务器”修改为“idevice”即可。

[![[assets/Clippings/Feather 签名工具/IMG-20260430101511258.png|使用本地回环安装软件。]]](https://www.onmyodev.com/wp-content/uploads/2026/02/IMG_8606.png)

至于其他的功能，是个签名工具应该都有，就不多做介绍了。

## 安装 Feather

要安装肯定是先下载，可以在官方的 [GitHub 发布页](https://github.com/claration/Feather/releases) 或者 [资源下载](https://www.onmyodev.com/2026/01/%e8%b5%84%e6%ba%90%e4%b8%8b%e8%bd%bd/) 处取得。

接下来需要签名。我不管你怎么签名，总之，你需要一个 **付费开发者证书** ，免费的是不能用的！此外切记不要安装在 LiveContainer 中！

[![[assets/Clippings/Feather 签名工具/IMG-20260430101511309.jpeg|对 Feather 安装包签名。]]](https://www.onmyodev.com/wp-content/uploads/2026/02/IMG_8607.jpeg)

签名之后安装，用全能签的就用全能签装，用轻松签的就用轻松签装，富哥（指真的有付费开发者账号的）……富哥直接用 Xcode 装，总之不管怎么装，装上就行了！

## 使用 Feather 进行签名

安装好之后打开。

### 导入证书

不多做介绍，不过 Feather 不能识别压缩包，导入前需要先解压。

### 导入安装包

这里我们就选择 OldOS 这款软件进行演示。

首先 OldOS 在 SideStore Community Picks 源里有，那么就可以点击软件源右上角的加号，选择这个源进行添加。没有的也可以直接输入源地址：

```plain text
https://community-apps.sidestore.io/sidecommunity.json
```

接下来找到 OldOS，点击下载。

[![[assets/Clippings/Feather 签名工具/IMG-20260430101511336.png|下载 OldOS 安装包。]]](https://www.onmyodev.com/wp-content/uploads/2026/02/IMG_8608.png)

下载好之后就会出现在“资源库”中：

[![[assets/Clippings/Feather 签名工具/IMG-20260430101511376.png|下载好的 OldOS 出现在资源库中。]]](https://www.onmyodev.com/wp-content/uploads/2026/02/IMG_8609.png)

如果是不在源里的软件，也可以直接点击资源库页面右上角的加号，导入.ipa 格式的安装包，或者输入网址让 Feather 帮你下载。

### 签名

直接点击对应软件右侧的“签名”按钮，就会打开签名界面。

[![[assets/Clippings/Feather 签名工具/IMG-20260430101511409.jpeg|使用 Feather 签名安装包。]]](https://www.onmyodev.com/wp-content/uploads/2026/02/IMG_8601.jpeg)

签名的时候可以自由修改软件的图标，名称，包名等，也可以选择要使用的证书。此外 Feather 还支持修改部分软件属性：

[![[assets/Clippings/Feather 签名工具/IMG-20260430101511434.png|修改软件的属性。]]](https://www.onmyodev.com/wp-content/uploads/2026/02/IMG_8602.png)

### 安装软件

签名好的软件会显示在资源库上方“已签名”一栏中，同时还会显示剩余天数。

[![[assets/Clippings/Feather 签名工具/IMG-20260430101511471.png|Feather 签名好的安装包列表。]]](https://www.onmyodev.com/wp-content/uploads/2026/02/IMG_8610.png)

点击右侧的剩余天数就会直接开始安装：

[![[assets/Clippings/Feather 签名工具/IMG-20260430101511499.png|安装已签名的软件。]]](https://www.onmyodev.com/wp-content/uploads/2026/02/IMG_8599.png)

不出意外的话软件就装上了。

## 结语

Feather 的出现可谓是……不不不，我可不是要说什么“付费开发者的明灯”，这款软件成功让我对外国的 iOS 工具祛魅了，外国也同样有自己的全能签

- **特别提醒：**
	评论看到就会回，但是不保证速度，有的时候站长忘记看的话就会出现审核好几天也没有动静的情况……
	如果等不及的话，可以加QQ，同样看到就会通过！

QQ: 3146654817，欢迎友好交流:P 曾用名Frank419（现在也是我在很多地方的用户名），网站站长。

### Previous Post

[EnsWilde \[iOS 18.0 – 26.1\]](https://www.onmyodev.com/2026/03/enswilde/)