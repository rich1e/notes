---
title: iOS 证书、侧载、JIT、SideStore 和 LiveContainer 扫盲
source: https://www.onmyodev.com/2026/05/ios-sideloading-faq/
author:
  - "[[杏川铭心]]"
published: 2026-05-25
created: 2026-07-02
description: 本文介绍了 iOS 侧载中最为常见的诸多问题。为什么我用购买的证书安装软件打不开？SideStore 怎么签名不了这个软件？怎么没有通知/JIT 等我想要的功能？本文会带你一一解开这些疑惑，保证你看完之后不会再面对琳琅满目的证书和工具时犯难。
tags:
  - clippings
  - LiveContainer
  - SideStore
  - ios
---
![[assets/Clippings/iOS 证书、侧载、JIT、SideStore 和 LiveContainer 扫盲/IMG-20260702164745362.jpg]]

最后编辑于 2026年5月25日

SideStore 和 LiveContainer 的原理是什么？不同的证书种类有什么区别？iOS 到底有多少种权限管理机制？本文就带你来理清楚。

## 签名证书

### 什么是调试证书和发布证书

一般来讲，iOS 的证书有两种，一种是调试证书，一种是发布证书；后者往往被统称为企业证书。

两者的区别在于，发布证书中少了很多和开发有关的权限，像调试证书签名的软件，一般里面都会带有一个 get-task-allow，这个权限决定了 iOS 是否允许这个 App 被调试器调试，而允许调试又是启用 JIT 的必须品。发布证书里没有这个权限，因此使用发布证书签名的软件都无法启用 JIT；和 JIT 工具是否使用的和软件同一个证书没有任何关系。

调试证书数量极为稀有，一个开发者同时只能申请两张这样的证书；发布证书的数量则会多不少。免费开发者只能申请调试证书，发布证书只有付费开发者才可以申请。

注意，虽然网上很多会有卖“个人开发者证书”的，但这些证书本质都是发布证书，换句话说功能上和企业证书没有任何的区别；你用免费的企业证书使用不了的软件用这些证书一样使用不了。

### 证书权限

iOS 里面经常可以看到各种各样的授权弹窗，XXX 希望访问照片图库，XXX 希望访问通讯录，XXX 希望访问位置信息……但若是你足够聪明，会发现并不是每个软件上面所有的弹窗都会弹一遍，这和证书本身的权限又有关系。

什么是证书的权限？简单来说，苹果为你颁发证书的时候，会一并提供一份列表，上面记载了所有你可以使用的权限；这些权限不一定会全部继承到你希望签名的 App 上，具体使用哪些权限和你在 Xcode 里的设置有关，但概念上是几乎一样的。

证书权限又分成两种，一种是普通的权限，就是有弹窗允许你控制的那种；另一种稍微特殊一点，叫 Entitlements，这类权限的处理是全自动的，你是看不到任何选项的，如果你平时只是从 App Store 上下载软件的话可能都不知道这个东西的存在。

普通的权限自不必说，下面这些都是普通权限：

- 照片图库
- 定位
- 麦克风
- ……

而下面这几种是 Entitlement：

- Increased Memory Limit
- Extended Virtual Addressing
- Personal VPN
- 上面提到的 get-task-allow
- ……

普通的权限，几乎没什么限制，谁都可以用，但是 Entitlement 就非常好玩了，有一些也是什么人都可以用的，例如 Increased Memory Limit，有一些是必须要求付费开发者证书且需要向苹果申请的，例如 Personal VPN，还有的干脆只给苹果自己用的，例如 com.apple.private.mediaplayer.internal。

### 证书的管理和有效期

可能有人会注意到开发者 App 会显示在 VPN 与设备管理里面，而这个地方正常情况下是显示 VPN 配置和描述文件的，为什么开发者 App 也在里面呢？

事实上开发者 App 和证书管理靠的依然是描述文件。

一个 App，侧载到 iOS 上，iOS 怎么知道这个 App 的有效期还有多久，怎么知道 App 申请的哪些 Entitlement 是有效的？就是靠描述文件。

首先正常情况下证书本身的有效期是一年（除了 Apple iPhoneOS Application Signing 这张 App Store 使用的证书）， **包括免费开发者证书哦！**

那为什么都说免费开发者证书安装出来的软件有效期是七天，这是因为免费开发者签名之后生成的 **那个描述文件的有效期是七天** ；七天之后，描述文件过期，尽管证书还在有效期内，但是 iOS 却不认了。至于续签，就是用你的这张证书重新生成一份新的描述文件安装，这份描述文件又是新的七天有效期，因此完成了续签的效果。

一个侧载的 App 的描述文件要被 iOS 识别为有效，需要同时满足下面三个条件：

- 证书在有效期内
- 描述文件在有效期内
- 描述文件记载的 Entitlements 符合软件实际使用的 Entitlements
![[assets/Clippings/iOS 证书、侧载、JIT、SideStore 和 LiveContainer 扫盲/IMG-20260702164745367.png|300]]

在 StikDebug 中查看描述文件过期情况。第一个就是由于描述文件缺少 Entitlements 导致的。不过在这个例子中并不会真的导致掉签，因为那是一个 TestFlight App~

由于最后那个条件不满足而导致的掉签发生的情况的很少，主要是前面两种。

这也是为什么付费证书没有续签的说法：证书本身的有效期就是一年，不管你怎么生成新的描述文件，其有效期也没办法超过证书本身的有效期；就算新的描述文件的有效期是一年，在证书本体过期的时候，iOS 依然会阻止打开对应的 App。实际操作中，付费开发者证书产生的描述文件，有效期和证书相同。

### 一个开发者可以拥有多少张证书？

两张 iOS 调试证书，两张 macOS 调试证书，两张新版调试证书；一张 iOS 发布证书，一张 macOS 发布证书，一张新版发布证书；不限数量的 APNs（推送服务）证书，两个 APNs 密钥；十个 Apple ID SSO（单点登录）密钥。

注意免费开发者只能申请调试证书，后面那一溜是没有的。

企业开发者不限制数量，只需要向 Apple 申请即可。

### 一张证书可以绑定多少设备？

调试证书 1 台，发布证书 100 台。也就是说网上卖的证书，成本价就是 6.88 元一张（付费开发者订阅一年 688 元），因为一张证书可以共享出去给 100 个人用。

### App ID

简单来说 App ID 就是一个 Bundle ID，但并不是严格意义上的每个 App 一个，比较复杂的 App 会有非常多个；在签名的时候类似于二级域名和三级域名的关系，就像为二级域名签发的 SSL 证书不能直接给三级域名用一样，为主要的 App ID 签名不能涵盖其余的功能，必须分开签名。

### 一位开发者可以申请多少 App ID？

免费开发者每 7 天 10 个，付费开发者不限数量。

### 刚刚提到了描述文件的限制，就不能在本地直接签名吗？

不可以。虽然签名的部分是由你自己完成的，但是描述文件是由苹果开发者服务器生成的。你没有任何办法控制这个过程，也就没有办法绕过描述文件直接签名并安装软件。

## SideStore

**相关文章：**

- [SideStore iOS 侧载教程](https://www.onmyodev.com/2025/12/sidestore-ios-%e4%be%a7%e8%bd%bd%e6%95%99%e7%a8%8b/)
- [iLoader + SideStore + LiveContainer 最强侧载工具教程](https://www.onmyodev.com/2026/04/iloader/)
- [SideStore 登录/刷新不了 The data couldn&#8217;t be read](https://www.onmyodev.com/2026/02/sidestore-nscocoaerrordomain/)

### SideStore 的原理

SideStore 是一个传统的 iOS 侧载工具，它会直接把软件安装到系统里，受上面那一大堆和证书有关系的东西限制。里面有一个很重要的组件，叫做 minimuxer，是对电脑端 usbmuxd 在 iOS 上的重新实现，精简了足够多的功能，以使其能够正常的在 iOS 的沙盒环境下正确工作；有了 minimuxer，才可以实现出设备自己连接自己的功能。

此外 Anisette 服务器也十分重要，它的功能是在远程服务器上模拟 Xcode 的签名服务，生成对应的描述文件，没有它 SideStore 根本就没办法签名；这也是为什么用完 SideStore 之后账户里会多出来一个不认识的 MacBook/iMac。

最后一个组件就是 StosVPN/LocalDevVPN，这个工具通过将发送给指定地址的数据包交换来源和目标后直接发回给 iOS 自己，搭配刚刚提到的 minimuxer，来模拟出真的有一台电脑在监听 iOS 设备的连接的效果。

### SideStore 占用 App ID 吗？

占用的。由于 App ID 不是删除的时候直接释放，如果你的 App ID 已经满了，那么就必须先删除不需要的 App，然后等待 7 天 App ID 过期。

### 为什么 iOS 允许自己连接自己？

首先苹果并没有有意允许这件事情的发生，事实上 iOS 26 对这种行为进行了一次封堵，iOS 26.4 又进行了一次更狠的封堵；但这都不重要，我们直接来看原理。

很多人吐槽 iTunes 难用，事实上是没有搞清楚 iTunes 的定位。iTunes 太高级了（不是反话），它并不是像很多人想象中的那样，是某种“手机驱动”，功能是“手机文件管理器”；事实上 iTunes 的功能更像是一个在你本地运行的 iCloud，其中有一个很重要的组件叫做 iTunes Wi-Fi Sync，它允许你在将设备连接到和电脑相同的 Wi-Fi 时视为连接到电脑。尽管叫这个名字，对普通用户来说这东西也确实就是个无线复制数据的功能，但是对开发者来说不是，它同时还能承担起不接线的情况下调试、管理设备上的 App 的功能。

这时候 SideStore 为什么能工作就豁然开朗了：因为 iOS 本来就有通过 Wi-Fi 连接电脑的功能，自然我们也可以模拟出一台 **通过 Wi-Fi 连接的电脑。** 注意这也是为什么 SideStore 强制要求你在连接到 Wi-Fi 的情况下操作；如果你不连接 Wi-Fi，那么 iOS 底层的无线连接机制根本就不会启动，自然也没办法做到续签。

### 为什么需要配对文件？

相信大家都见过把手机插上电脑时的那个询问你要不要信任该设备的弹窗吧，iOS 在不信任一台电脑的情况下是不会与其连接的；那么 iOS 是怎么识别这台电脑之前有没有信任过？答案就是通过配对文件。iOS 连接到电脑时，先向电脑请求电脑上的配对文件，然后和系统内另一部分作比较（类似公钥和私钥），如果能对上就认为这是一台受信电脑，正常连接。

Minimuxer 没有自己生成配对的功能，所以需要你先到真正的电脑上生成一次配对，导入到手机上之后，才能正常使用。

### iOS 26.4 改了什么？

主要就是封堵基于这种配对文件的连接方式，不是说不要配对文件了，毕竟真的连接上电脑还是要验证配对文件的，只不过苹果 放弃了老旧的 Lockdown 格式，换成了 RPPairing 的格式，这种格式虽说实际应用起来比 Lockdown 稳定，但是在 iOS 26.4 上有两个关键限制：无法使用飞行模式欺骗系统，无法中途关闭回环隧道。对 SideStore 而言并不是大问题，但是对 StikDebug 来说问题很大；当然现在我们介绍的是 SideStore，后面我们再详细介绍 StikDebug。

## LiveContainer

**相关文章：**

- [LiveContainer 教程](https://www.onmyodev.com/2025/12/livecontainer-%e6%95%99%e7%a8%8b/)
- [iLoader + SideStore + LiveContainer 最强侧载工具教程](https://www.onmyodev.com/2026/04/iloader/)
- [使用 Get More RAM 解决 LiveContainer 运行内存不足](https://www.onmyodev.com/2026/04/livecontainer-increased-memory/)
- [多 LiveContainer 教程](https://www.onmyodev.com/2026/04/multiple-livecontainer/)

### LiveContainer 的原理

LiveContainer 和 SideStore 不同，它并不会把软件直接装到系统里面；相反，它是直接把软件解压到自己的数据文件夹中，然后直接在本地签名。运行的时候，通过 LiveProcess，直接绕开自己的主程序，转而执行对应 App 的程序。

这样做的一大好处就是可以绕开描述文件的需求，同时也不占用 App ID，对一些乱七八糟的安装包格式支持也显著比 SideStore 优秀得多。

但这样做不是没有缺点，首先就是，LiveContainer 里面的软件，只能通过 LiveContainer 运行，桌面上是没有图标的。虽然可以手动创建对应的图标，但体验上相较于普通的软件一定是会更加割裂一点。

另外因为里面所有的软件都是使用的 LiveProcess，也就是在 LiveContainer “内”运行（不过注意 LiveContainer 不是虚拟机。可以理解成容器，如果你观察过的话，很容易发现，LiveContainer 里的软件运行的时候，在后台依然显示为 LiveContainer），很多软件会处理不了这种情况，最常见的问题就是文件导入失败，这时需要将 LiveContainer 内对应的修复项打开。

### LiveContainer 占用 App ID 吗？

刚刚已经介绍过了，不占用。

一个结果就是，LiveContainer 中的 App，都是共享的 LiveContainer 本身的权限和 Entitlements，如果要修改 Entitlements，比如很常见的 Increased Memory Limit，那么直接在 LiveContainer 本体上操作就可以了。在 LiveContainer 里面操作不仅没必要还没有用，纯粹的浪费时间。

同样 LiveContainer 里面的 App 也不会有自己的过期时间，LiveContainer 什么时候过期，里面的 App 就什么时候过期；续签的时候，也只需要给 LiveContainer 续签，千万不要傻呵呵的去找怎么给 LiveContainer 里面的软件续签。

### 这是说 LiveContainer 里面的软件不需要签名吗？

是又不是。由于没有了描述文件的限制，LiveContainer 可以直接在本地完成对各个 App 里程序的签名。

不过 LiveContainer 支持使用 JIT 运行软件；使用 JIT 的软件不需要签名，因为 JIT 本身就可以绕过 Code Signing 的限制。

### 相比于 SideStore，具体可以多安装哪些应用？

主要是注入了.dylib 插件的应用，SideStore 没办法处理这些应用，最明显的一个例子是 FilzaJailedDS，用 SideStore 安装会提示你 App 的格式不正确，找不到 App 等。

## JIT

**相关文章：**

- [新版 StikDebug 启用 JIT 教程，支持 iOS 26](https://www.onmyodev.com/2026/04/stikdebug-jit-new/)
- [多 LiveContainer 教程](https://www.onmyodev.com/2026/04/multiple-livecontainer/)

### 什么是 JIT？

JIT，全程 Just-in-time (Compilation)，是一种常见的加速代码执行的方式，像 Chromium 里的 V8 引擎，就使用了 JIT 技术为 JavaScript 解释器加速。

由于 JIT 本身的特点，其安全性相较于普通的静态程序安全性一定会低一些，所以在 iOS 上，苹果只给 WebKit 的 JavaScript 和 WebAssembly 解释器开了绿灯，允许使用 JIT，其它软件则不允许使用。

### 开启 JIT 的原理

由于 JIT 自带可以绕过 code-signing 要求的特性，同时也为了方便开发者调试 App，苹果允许一个 App 在连接调试器的情况下使用 JIT 功能。虽然本意是为了防止调试器修改 App 代码的时候导致 Code Signing 把 App 干死，但的的确确也使得 App 可以使用这 JIT 功能为自己的代码加速。

本质上是一种滥用。

### StikDebug

为什么 StikDebug 的名字里要带个 Debug（调试）就很清楚了：为了上架 App Store，StikDebug 的开发者把这款 App 包装成了一款开发工具，机上调试嘛！遗憾的是苹果后来缓过神来了，把所有用配对文件实现自己连接自己的 App 全给下架了，不过 StikDebug 的名字却留了下来。

原理也很简单，就是模拟一台正在运行调试器的电脑，然后开始“调试”程序。iOS 在检测到调试器后会自动允许软件使用 JIT 功能。

### iOS 26 怎么就影响 JIT 了？

苹果有意识地影响了 JIT 功能，重点就在于这个连接调试器的步骤上。刚刚在 SideStore 的介绍中我们已经提到，iOS 26 更换了配对方法，结果就是，现在如果你只要流量，那么是没办法通过临时打开飞行模式来启用 JIT 的，因为在飞行模式下，iOS 也会判定为不可能无线连接电脑，会直接拒绝连接；然后就是 RPPairing，这种配对方法，不再允许连接一次之后就立刻断开，在 iOS 26 上使用 JIT 时，必须时刻保持打开 LocalDevVPN 和 StikDebug 并连接 Wi-Fi，不然 iOS 将会判定调试器断开连接，然后你的 App 就闪退了。

另一个影响就是对 JIT 脚本的依赖。总的来说就是苹果从一开始就没打算让你用调试的办法获取 JIT 来加速软件运行，这也是为什么想玩机的话永远不建议升级系统，你永远不知道你昨天还在用的工具今天会不会失效。

### StikDebug 之前呢？怎么开启 JIT？

在 StikDebug 之前一般是用的 AltJIT，像 iOS 17.0-17.3.x 就可以用这个办法；再之前那直接越狱了，越狱会把整个 Code Signing 干掉，JIT 随便开，甚至比原生的 JIT 还牛逼。

这种 JIT 一般是直接使用的 get-task-allow，只要有这个 Entitlement 就直接抓进程开启 JIT；苹果在 iOS 18.4 的时候堵上了这个漏洞。

## 不同签名工具对比

现在主流的签名工具，一种是以 SideStore、iLoader 为代表的免费开发者自签工具，另一类是以全能签、Feather 等工具为代表的购买证书签名工具。

其实真说有什么区别，主要还是刚刚提到的证书种类和权限的区别，基本上，如果你要使用的软件有如下特征：

那么全能签之类的工具更适合你。相反，如果你要使用的软件有如下特征：

- 需要 JIT（模拟器、虚拟机）

那么 SideStore 更适合你。

注意这两种情况绝大多数情况下是不能交换的，比如你强行使用 SideStore 签名 LocalDevVPN 这种包含了 VPN 隧道的工具，那么相关的功能是完全无法使用的；又或者你使用全能签签名 MeloNX 这种模拟器，也完全无法使用，部分软件可能还会闪退。
