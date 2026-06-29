---
title: 浏览器层面优化前端性能(1):Chrom组件与进程/线程模型分析 - webkit - 周陆军的个人网站
source: https://www.zhoulujun.cn/html/webfront/browser/webkit/2020_0610_8455.html
author:
  - "[[周陆军]]"
published: 2020-06-10
created: 2026-06-03
description: Chrome支持以下几种进程模型：Process-per-site-instance Process-per-site Process-per-tab Single Process。Browser只有一个，主控整个系统的运行，管理Chrome大部分的日常事务；而Renderer则可以有多个，主要负责页面的渲染和显示。
tags:
  - clippings
  - Chrome
  - WebKit
---
现阶段的浏览器运行在一个单用户，多合作，多任务的操作系统中。一个糟糕的网页同样可以让一个现代的浏览器崩溃。其原因可能是一个插件出现bug,最终的结果是整个浏览器以及其他正在运行的标签被销毁。

现代操作系统已经非常健壮了，它让应用程序在各自的进程中运行和不会影响到其他程序。一个进程崩溃不会损害到其他进程以及操作系统。同时系统会严格的限制一个用户访问另外一个用户空间的数据。

关于进程、线程、多线程等相关知识回顾，参看《 [同步与异步：并发/并行/进程/线程/多cpu/多核/超线程/管程](https://www.zhoulujun.cn/html/theory/ComputerScienceTechnology/Constitution/2020_0619_8474.html) 》

浏览器属于一个应用程序，而应用程序的一次执行，可以理解为计算机启动了一个进程，进程启动后，CPU会给该进程分配相应的内存空间，当我们的进程得到了内存之后，就可以使用线程进行资源调度，进而完成我们应用程序的功能。

而在应用程序中，为了满足功能的需要，启动的进程会创建另外的新的进程来处理其他任务，这些创建出来的新的进程拥有全新的独立的内存空间，不能与原来的进程内向内存，如果这些进程之间需要通信，可以通过IPC机制（Inter Process Communication）来进行。

![[assets/Clippings/浏览器层面优化前端性能(1)Chrom组件与进程线程模型分析 - webkit - 周陆军的个人网站/IMG-20260629165307514.png|IPC机制（Inter Process Communication）]]

假如我们去开发一个浏览器，它的架构可以是一个单进程多线程的应用程序，也可以是一个使用IPC通信的多进程应用程序。

以chrome为例，使用IPC通信的多进程应用程序

chrome浏览器与其他浏览器不同，chrome使用多个渲染引擎实例，每个Tab页一个，即每个Tab都是一个独立进程。

## 浏览器组件

浏览器大体上由以下几个组件组成，各个浏览器可能有一点不同。

![[assets/Clippings/浏览器层面优化前端性能(1)Chrom组件与进程线程模型分析 - webkit - 周陆军的个人网站/IMG-20260629165307522.png|浏览器组件.png]] ![[assets/Clippings/浏览器层面优化前端性能(1)Chrom组件与进程线程模型分析 - webkit - 周陆军的个人网站/IMG-20260629165307527.png|20200610161237613310758.png]]

- 界面控件 – 包括地址栏，前进后退，书签菜单等窗口上除了网页显示区域以外的部分
- 浏览器引擎 – 查询与操作渲染引擎的接口
- 渲染引擎 – 负责显示请求的内容。比如请求到HTML, 它会负责解析HTML、CSS并将结果显示到窗口中
- 网络 – 用于网络请求, 如HTTP请求。它包括平台无关的接口和各平台独立的实现
- UI后端 – 绘制基础元件，如组合框与窗口。它提供平台无关的接口，内部使用操作系统的相应实现
- JS解释器 - 用于解析执行JavaScript代码
- 数据存储持久层 - 浏览器需要把所有数据存到硬盘上，如cookies。新的HTML5规范规定了一个完整（虽然轻量级）的浏览器中的数据库web database

## Chrome的并发模型

chrome的进程，chrome没有采用一般应用程序的单进程多线程的模型，而是采用了多进程的模型，按照他的文字说明，主界面框架下的一个TAB就对应这个一个进程。但实际上，一个进程不仅仅包含一个页面，实际上同类的页面在共用一个进程。

Google在宣传的时候一直都说，Chrome是one tab one process的模式。实际上，Chrome支持的进程模型远比宣传丰富，简单的说，Chrome支持以下几种进程模型：

- **Process-per-site-instance** ：就是你打开一个网站，然后从这个网站链开的一系列网站都属于一个进程。这是Chrome的默认模式。
- **Process-per-site** ：同域名范畴的网站放在一个进程，比如www.google.com和www.google.com/bookmarks就属于一个域名内（google有自己的判定机制），不论有没有互相打开的关系，都算作是一个进程中。用命令行–process-per-site开启。
- **Process-per-tab** ：这个简单，一个tab一个process，不论各个tab的站点有无联系，就和宣传的那样。用–process-per-tab开启。
- **Single Process** ：这个很熟悉了吧，即传统浏览器的模式：没有多进程只有多线程，用–single-process开启。

### 多进程有好处：

把渲染放到另外个进程防止崩溃了影响主进程。webkit最初时候很多内存泄露。多进程能很大程度避免。一个进程关了，所有内存就回收了。其次，多进程安全性更好。如果blink被发现什么提权漏洞，例如写一段js就能控制整个chromium进程做任何事情，显然多进程可以把损失限制在渲染线程。渲染线程拿不到主进程的各种私密信息，例如别的域名下的密码。

![[assets/Clippings/浏览器层面优化前端性能(1)Chrom组件与进程线程模型分析 - webkit - 周陆军的个人网站/IMG-20260629165307531.png|多进程架构的好处]]

## 多线程模型

chrome进程模型下有

- **Browser进程只有一个，主控整个系统的运行，管理Chrome大部分的日常事务；**
	负责浏览器页面的显示，各个页面的管理，所有其他类型进程的祖先，负责他们的创建和销毁。
- UI thread：
- 负责浏览器界面显示，与用户交互。如前进，后退等
		- 将Renderer进程得到的内存中的Bitmap，绘制到用户界面上
	- network thread：网络资源的管理，下载等（这个和网络进程间？？？）
	- storage thread： 控制文件等的访问；
- **Renderer 浏览器渲染进程（浏览器内核），** 主要负责页面的渲染和显示： **页面渲染，脚本执行，事件处理等** 。
	默认每个Tab页面一个Renderer进程（Renderer进程，内部是多线程的）
- Utility Network:网络进程，负责页面网络资源的加载
- GPU进程：最多只有一个，GPU硬件加速打开时才会被创建，用于3D绘制等。
- NPAPI或PPAPI插件进程，每种类型的插件对应一个进程，仅当使用该插件时才创建。
	1995 年 Netscape 发明了NPAPI (Netscape plugin API)这个种架构，来帮助浏览器渲染一些HTML没有的东西。比如 PDF, 比如 视频， 以及等等。NPAPI不限制插件自由访问系统所有的API，而且和浏览器是平级运行的。现在已被禁用。 [PPAPI](https://code.google.com/p/ppapi/) 是谷歌提出的架构。
- Pepper插件进程
- 其他类型的进程，比如Linux的Zygote进程；Sandbox进程。
![[assets/Clippings/浏览器层面优化前端性能(1)Chrom组件与进程线程模型分析 - webkit - 周陆军的个人网站/IMG-20260629165307536.jpg|chrome进程架构图]]

chrome进程架构图

Browser作为主进程最先启动，Browser包含一个主线程mainthread，在mainthread中对整个系统进行初始化，并启动为另外几个线程，看下面的代码：

void CreateChildThreads(BrowserProcessImpl\* process) {

process->db\_thread(); //负责数据库处理

process->file\_thread(); // 负责文件管理

process->process\_launcher\_thread();

process->cache\_thread(); //负责管理缓存

process->io\_thread(); //负责管理进程间通信和所有I/O行为。

}

io\_thread不仅负责Browser进程的I/O，而且其他Renderer的I/O请求也会通过进程间通信发送到这个线程，由该线程进行处理，最后把结果在返回给各个Renderer进程。各个线程的功能不一样，但设计模式是一样的

对于Renderer进程，它们通常有两个线程：一个是Main thread，负责与主线程联系。另一个是Render thread，它们负责页面的渲染和交互

![[assets/Clippings/浏览器层面优化前端性能(1)Chrom组件与进程线程模型分析 - webkit - 周陆军的个人网站/IMG-20260629165307541.png|20200610161318112145652.png]]

当我们是要浏览一个网页，我们会在浏览器的地址栏里输入URL，这个时候Browser Process会向这个URL发送请求，获取这个URL的HTML内容，然后将HTML交给Renderer Process，Renderer Process解析HTML内容，解析遇到需要请求网络的资源又返回来交给Browser Process进行加载，同时通知Browser Process，需要Plugin Process加载插件资源，执行插件代码。解析完成后，Renderer Process计算得到图像帧，并将这些图像帧交给GPU Process，GPU Process将其转化为图像显示屏幕。

## Chrome的线程模型

Chrome的线程模型极力规避锁的存在，将锁限制了极小的范围内（仅仅在将Task放入消息队列的时候才存在…），并且使得上层完全不需要关心锁的问题（当然，前提是遵循它的编程模型，将函数用Task封装并发送到合适的线程去执行…），大大简化了开发的逻辑。它用到了消息循环的手段。每一个Chrome的线程，入口函数都差不多，都是启动一个消息循环（参见MessagePump类），等待并执行任务。

根据线程处理事务类别的不同，所起的消息循环有所不同。比如

- 处理进程间通信的线程（注意，在Chrome中，这类线程都叫做IO线程）
- 启用的是MessagePumpForIO类，处理UI的线程用的是MessagePumpForUI类，
- 一般的线程用到的是MessagePumpDefault类（只讨论windows）。

不同的消息循环类，主要差异有两个，一是消息循环中需要处理什么样的消息和任务，第二个是循环流程（比如是死循环还是阻塞在某信号量上…）。

### 浏览器通常由以下常驻线程组成：

- **GUI 渲染线程**  
	GUI渲染线程负责渲染浏览器界面HTML元素,当界面需要重绘(Repaint)或由于某种操作引发回流(reflow)时，该线程就会执行。在Javascript引擎运行脚本期间,GUI渲染线程都是处于挂起状态的，也就是说被 **冻结** 了.
- 一个主线程（main thread）
	- 多个工作线程（work thread）
	- 一个合成器线程（compositor thread）
	- 多个光栅化线程（raster thread）
- **JavaScript引擎线程**  
	JS为处理页面中用户的交互，以及操作DOM树、CSS样式树来给用户呈现一份动态而丰富的交互体验和服务器逻辑的交互处理。如果JS是多线程的方式来操作这些UI DOM，则可能出现UI操作的冲突；如果JS是多线程的话，在多线程的交互下，处于UI中的DOM节点就可能成为一个临界资源，假设存在两个线程同时操作一个DOM，一个负责修改一个负责删除，那么这个时候就需要浏览器来裁决如何生效哪个线程的执行结果，当然我们可以通过锁来解决上面的问题。但为了 **避免因为引入了锁而带来更大的复杂性** (多线程的话会使浏览器的效率降低。多线程必然会引入的锁，信号量的一类操作，大大增加了复杂性) **，JS在最初就选择了单线程执行** 。  
	GUI渲染线程与JS引擎线程互斥的，是由于JavaScript是可操纵DOM的，如果在修改这些元素属性同时渲染界面（即JavaScript线程和UI线程同时运行），那么渲染线程前后获得的元素数据就可能不一致。当JavaScript引擎执行时GUI线程会被挂起，GUI更新会被保存在一个队列中等到引擎线程空闲时立即被执行。  
	由于GUI渲染线程与JS执行线程是互斥的关系，当浏览器在执行JS程序的时候，GUI渲染线程会被保存在一个队列中，直到JS程序执行完成，才会接着执行。因此如果JS执行的时间过长，这样就会造成页面的渲染不连贯，导致页面渲染加载阻塞的感觉。
- **定时触发器线程**  
	浏览器定时计数器并不是由JS引擎计数的, 因为JS引擎是单线程的, 如果处于阻塞线程状态就会影响记计时的准确, 因此通过单独线程来计时并触发定时是更为合理的方案。
- **事件触发线程**  
	当一个事件被触发时该线程会把事件添加到待处理队列的队尾，等待JS引擎的处理。这些事件可以是当前执行的代码块如定时任务、也可来自浏览器内核的其他线程如鼠标点击、AJAX异步请求等，但由于JS的单线程关系所有这些事件都得排队等待JS引擎处理。
- **异步http请求线程**  
	在XMLHttpRequest在连接后是通过浏览器新开一个线程请求，将检测到状态变更时，如果设置有回调函数，异步线程就产生状态变更事件放到JS引擎的处理队列中等待处理。

对于普通的前端操作来说，最终要的是什么呢？答案是渲染进程

可以这样理解，页面的渲染，JS的执行，事件的循环，都在这个进程内进行。

## Browser Process进程：

- tab以外的大部分工作由浏览器进程Browser Process负责，Browser Process 划分出不同的工作线程
- UI thread：控制浏览器上的按钮及输入框；
- network thread：处理网络请求，从网上获取数据（Chrome72以后，已将network thread单独摘成network service process，当然也可以通过 chrome://flags/#network-service-in-process修改配置，将其其作为线程运行在Browser Process中，感谢 @Popeye-Wz 的提出）；
- storage thread： 控制文件等的访问；

![[assets/Clippings/浏览器层面优化前端性能(1)Chrom组件与进程线程模型分析 - webkit - 周陆军的个人网站/IMG-20260629165307545.png|Browser Process 划分出不同的工作线程]]

### 网页加载过程-导航过程

- UI thread：控制浏览器上的按钮及输入框；
- network thread：处理网络请求，从网上获取数据（Chrome72以后，已将network thread单独摘成network service process，当然也可以通过 chrome://flags/#network-service-in-process修改配置，将其其作为线程运行在Browser Process中
- storage thread： 控制文件等的访问；

处理过程解析

#### 处理输入

当我们在浏览器的地址栏输入内容按下回车时， **UI thread会判断输入的内容是搜索关键词（search query）还是URL** ，如果是搜索关键词，跳转至默认搜索引擎对应都搜索URL，如果输入的内容是URL，则开始请求URL。

#### 开始导航

回车按下后， **UI thread将关键词搜索对应的URL或输入的URL交给网络线程Network thread** ，此时UI线程使Tab前的图标展示为加载中状态，然后网络进程进行一系列诸如DNS寻址，建立TLS连接等操作进行资源请求，如果收到服务器的301重定向响应，它就会告知UI线程进行重定向然后它会再次发起一个新的网络请求。

#### 读取响应

**network thread接收到服务器的响应后，开始解析HTTP响应报文** ，然后根据响应头中的Content-Type字段来确定响应主体的媒体类型（MIME Type）， **如果媒体类型是一个HTML文件，则将响应数据交给渲染进程（renderer process）来进行下一步的工作** ，如果是 zip 文件或者其它文件，会把相关数据传输给下载管理器。

与此同时， **浏览器会进行 Safe Browsing 安全检查** ，如果域名或者请求内容匹配到已知的恶意站点，network thread 会展示一个警告页。除此之外，网络线程还会做 CORB（Cross Origin Read Blocking）检查来确定那些敏感的跨站数据不会被发送至渲染进程。

#### 查找渲染进程

各种检查完毕以后，network thread 确信浏览器可以导航到请求网页， **network thread 会通知 UI thread 数据已经准备好，UI thread 会查找到一个 renderer process 进行网页的渲** 染。

浏览器为了对查找渲染进程这一步骤进行优化，考虑到网络请求获取响应需要时间，所以在第二步开始， **浏览器已经预先查找和启动了一个渲染进程** ，如果中间步骤一切顺利，当 network thread 接收到数据时，渲染进程已经准备好了，但是如果遇到重定向，这个准备好的渲染进程也许就不可用了，这个时候会重新启动一个渲染进程。

#### 提交导航

到了这一步，数据和渲染进程都准备好了，Browser Process 会向 Renderer Process 发送IPC消息来确认导航，此时，浏览器进程将准备好的数据发送给渲染进程，渲染进程接收到数据之后，又发送IPC消息给浏览器进程，告诉浏览器进程导航已经提交了，页面开始加载。

这个时候导航栏会更新，安全指示符更新（地址前面的小锁），访问历史列表（history tab）更新，即可以通过前进后退来切换该页面。

#### 初始化加载完成

当导航提交完成后，渲染进程开始加载资源及渲染页面（详细内容下文介绍），当页面渲染完成后（页面及内部的iframe都触发了onload事件），会向浏览器进程发送IPC消息，告知浏览器进程，这个时候UI thread会停止展示tab中的加载中图标。

## 渲染进程

1. GUI渲染线程
- 负责渲染浏览器界面，解析HTML，CSS，构建DOM树和RenderObject树，布局和绘制等。
	- 当界面需要重绘（Repaint）或由于某种操作引发回流(reflow)时，该线程就会执行
	- 注意， **GUI渲染线程与JS引擎线程是互斥的** ，当JS引擎执行时GUI线程会被挂起（相当于被冻结了），GUI更新会被保存在一个队列中 **等到JS引擎空闲时** 立即被执行。
- 由于JavaScript是可操纵DOM的，如果在修改这些元素属性同时渲染界面（即JS线程和UI线程同时运行），那么渲染线程前后获得的元素数据就可能不一致了。因此 **为了防止渲染出现不可预期的结果，浏览器设置GUI渲染线程与JS引擎为互斥的关系** ，当JS引擎执行时GUI线程会被挂起，GUI更新则会被保存在一个队列中等到JS引擎线程空闲时立即被执行。
	- 注意composite概念，浏览器渲染的图层一般包含两大类：普通图层以及复合图层。
- **普通文档流内可以理解为一个复合图层** （这里称为默认复合层，里面不管添加多少元素，其实都是在同一个复合图层中，哪怕是absolute布局（fixed也一样），即使脱离普通文档流，但它仍然属于默认复合层）
- absolute虽然可以脱离普通文档流，但是无法脱离默认复合层。就算absolute中信息改变时不会改变普通文档流中render树，但是，浏览器最终绘制时，是整个复合层绘制的，所以absolute中信息的改变，仍然会影响整个复合层的绘制。
		- 可以通过硬件加速的方式—GPU线程，声明一个新的复合图层(最常用的方式：translate3d、translateZ)，它会单独分配资源，会脱离普通文档流，不管这个复合图层中怎么变化，也不会影响默认复合层里的回流重绘。
- GPU中，各个复合图层是单独绘制的，所以互不影响，这也是为什么某些场景硬件加速效果一级棒
			- 如果a是一个复合图层，而且b在a上面，那么b也会被隐式转为一个复合图层，这点需要特别注意
	- css加载是否会阻塞dom 渲染进程
- css加载不会阻塞DOM树解析（异步加载时DOM照常构建——css是由单独的下载线程异步下载的）
		- 但会阻塞render树渲染（渲染时需等css加载完毕，因为render树需要css信息——这可能也是浏览器的一种优化机制）

因为加载css的时候，可能会修改下面DOM节点的样式，如果css加载不阻塞render树渲染的话，那么当css加载完之后，render树可能又得重新重绘或者回流了，这就造成了一些没有必要的损耗。所以干脆就先把DOM树的结构先解析完，把可以做的工作做完，然后等你css加载完之后，在根据最终的样式来渲染render树，这种做法性能方面确实会比较好一点。
3. JS引擎线程
- 也称为JS内核，负责处理Javascript脚本程序。（例如V8引擎）
	- JS引擎线程负责解析Javascript脚本，运行代码。
	- JS引擎一直等待着任务队列中任务的到来，然后加以处理，一个Tab页（renderer进程）中无论什么时候都只有一个JS线程在运行JS程序
	- 同样注意， **GUI渲染线程与JS引擎线程是互斥的** ，所以如果JS执行的时间过长，这样就会造成页面的渲染不连贯，导致页面渲染加载阻塞。
	- 要尽量避免JS执行时间过长，这样就会造成页面的渲染不连贯，导致页面渲染加载阻塞的感觉。Web Worker 异步优化下
- **创建Worker时，JS引擎向浏览器申请开一个子线程** （子线程是浏览器开的，完全受主线程控制，而且不能操作DOM）
		- **JS引擎线程与worker线程间通过特定的方式通信（postMessage API** ，需要通过序列化对象来与线程交互特定的数据）
	JS引擎是单线程的，这一点的本质仍然未改变，Worker可以理解是浏览器给JS引擎开的外挂，专门用来解决那些大量计算问题。
	- [SharedWorker](https://developer.mozilla.org/en-US/docs/Web/API/SharedWorker) 是浏览器所有页面共享的，不能采用与Worker同样的方式实现，因为它不隶属于某个Render进程，可以为多个Render进程共享使用。所以Chrome **浏览器为SharedWorker单独创建一个进程来运行JavaScript程序** ，在浏览器中每个相同的JavaScript只存在一个SharedWorker进程，不管它被创建多少次。
- 页面A发送数据给worker：window.worker.port.postMessage('get')，然后打开页面B，调用window.worker.port.postMessage('get')，即可收到页面A发送给worker的数据。
5. 事件触发线程
- 归属于浏览器而不是JS引擎，用来控制事件循环（可以理解，JS引擎自己都忙不过来，需要浏览器另开线程协助）
	- 当JS引擎执行代码块如setTimeOut时（也可来自浏览器内核的其他线程,如鼠标点击、AJAX异步请求等），会将对应任务添加到事件线程中.
	- 当对应的事件符合触发条件被触发时，该线程会把事件添加到待处理队列的队尾，等待JS引擎的处理
	- 注意， **由于JS的单线程关系，所以这些待处理队列中的事件都得排队等待JS引擎处理** （当JS引擎空闲时才会去执行）
- 为什么有时候setTimeout推入的事件不能准时执行？因为可能在它推入到事件列表时，主线程还不空闲，正在执行其它代码，
7. 定时触发器线程
- 传说中的 `setInterval` 与 `setTimeout` 所在线程
	- 浏览器定时计数器并不是由JavaScript引擎计数的,（因为JavaScript引擎是单线程的, 如果处于阻塞线程状态就会影响记计时的准确）
	- 因此通过单独线程来计时并触发定时（计时完毕后，添加到事件队列中，等待JS引擎空闲后执行）
	- 注意，W3C在HTML标准中规定，规定要求setTimeout中低于4ms的时间间隔算为4ms。
9. 异步http请求线程
- 在XMLHttpRequest在连接后是通过浏览器新开一个线程请求
	- 将检测到状态变更时，如果设置有回调函数，异步线程就 **产生状态变更事件** ，将这个回调再放入事件队列中。再由JavaScript引擎执行。

## 事件循环机制进与线程关系

之前也写过《 [弄懂javascript的执行机制:事件轮询|微任务和宏任务](https://www.zhoulujun.cn/html/webfront/ECMAScript/js6/2015_1110_345.html) 》，但是还是没有从本质去阐述。

JavaScript事件队列等原因还是JavaScript线程与 定时触发器线程、事件触发线程、异步http请求线程等IO通信问题。《》

- 主线程运行时会产生执行栈
- 栈中的代码调用某些api时，它们会在事件队列中添加各种事件（当满足触发条件后，如ajax请求完毕）
- 而栈中的代码执行完毕，就会读取事件队列中的事件，去执行那些回调

如此循环，如下图

![[assets/Clippings/浏览器层面优化前端性能(1)Chrom组件与进程线程模型分析 - webkit - 周陆军的个人网站/IMG-20260629165307548.png|20200610173447689929215.png]]

注意，总是要 **等待栈中的代码执行完毕后才会去读取事件队列中的事件**

有执行栈与任务队列，引发，宏任务-macrotask与微任务-microtask等相关概念

在ECMAScript中，microtask称为jobs，macrotask可称为task

- macrotask（又称之为宏任务）， **macrotask中的事件都是放在一个事件队列中的，而这个队列由事件触发线程维护**
	可以理解是 **每次执行栈执行的代码就是一个宏任务** （包括每次从事件队列中获取一个事件回调并放到执行栈中执行），（\`task->渲染->task->...\`）
- 每一个task会从头到尾将这个任务执行完毕，不会执行其它
	- 浏览器为了能够使得JS内部task与DOM任务能够有序的执行，会在一个task执行结束后，在下一个 task 执行开始前，对页面进行重新渲染
- microtask（又称为微任务）， **microtask中的所有微任务都是添加到微任务队列（Job Queues）中，等待当前macrotask执行完毕后执行，而这个队列由JS引擎线程维护** **可**
	可以理解 **是在当前 task 执行结束后立即执行的任务**
- 也就是说，在当前task任务后，下一个task之前，在渲染之前
	- 所以它的响应速度相比setTimeout（setTimeout是task）会更快，因为无需等渲染
	- 也就是说，在某一个macrotask执行完后，就会将在它执行期间产生的所有microtask都执行完毕（在渲染前）

### 分别很么样的场景会形成macrotask和microtask呢？

- macrotask：主代码块，setTimeout、postMessage、setImmediat、MessageChannel(优先级高于setTimeout)等（可以看到，事件队列中的每一个事件都是一个macrotask）、requestAnimationFrame 、I/O、UI Rendering
- microtask：Promise，MutationObserver(优先级小于Promise—监听一个DOM变动)，process.nextTick(process.nextTick的优先级高于Promise) 、Object.observe(废弃)等
	注意promise的polyfill与官方版本的区别：
- 官方版本中，是标准的microtask形式
	- polyfill，一般都是通过setTimeout模拟的，所以是macrotask形式

关于vue的$nextTick 2.5+由 MutationObserver 改为MessageChannel，这方面的内容，具体参看《 [web messaging与Woker分类：漫谈postMessage跨线程跨页面通信](https://www.zhoulujun.cn/html/webfront/SGML/html5/2020_0615_8465.html) 》

## 定时器

上述事件循环机制的核心是：JS引擎线程和事件触发线程

但事件上，里面还有一些隐藏细节，譬如调用setTimeout后，是如何等待特定时间后才添加到事件队列中的？

是JS引擎检测的么？当然不是了。它是由定时器线程控制（因为JS引擎自己都忙不过来，根本无暇分身）

为什么要单独的定时器线程？因为JavaScript引擎是单线程的, 如果处于阻塞线程状态就会影响记计时的准确，因此很有必要单独开一个线程用来计时。

什么时候会用到定时器线程？ **当使用setTimeout或setInterval时，它需要定时器线程计时，计时完成后就会将特定的事件推入事件队列中** 。

### setTimeout与setInterval

- setTimeout计时到到后触发事件触发器，插入一个任务到 事件队列
	延缓事件为：setTimeout触发是设置的等待事件+等待到任务执行时间）
- setInterval则是每次都精确的隔一段时间推入一个事件

而且setInterval有一些比较致命的问题就是：累计效应

如果setInterval代码在（setInterval）再次添加到队列之前还没有完成执行，就会导致定时器代码连续运行好几次，而之间没有间隔。

JS引擎会对setInterval进行优化， **如果当前事件队列中有setInterval的回调，不会重复添加** 。但是，有错过了延迟的事件。

一般认为的最佳方案是： **用setTimeout模拟setInterval，或者特殊场合直接用requestAnimationFrame** 。

## Node.js事件循环与线程

Node.js也是单线程的Event Loop，但是它的运行机制不同于浏览器（和浏览器中的是完全不相同的东西，关键还是线程架构不同）

Node.js 采用 V8 作为 js 的解析引擎，而 I/O 处理方面使用了自己设计的 libuv，libuv 是一个基于事件驱动的跨平台抽象层，封装了不同操作系统一些底层特性，对外提供统一的 API，事件循环机制也是它里面的实现

![[assets/Clippings/浏览器层面优化前端性能(1)Chrom组件与进程线程模型分析 - webkit - 周陆军的个人网站/IMG-20260629165307552.png|Node.js也是单线程的Event Loop]]

根据上图，Node.js的运行机制如下

- V8引擎解析JavaScript脚本
- 解析后的代码，调用Node API
- libuv库负责Node API的执行。它将不同的任务分配给不同的线程，形成一个Event Loop（事件循环），以异步的方式将任务的执行结果返回给V8引擎
- V8引擎再将结果返回给用户

### Node.js 的运行机制

- V8 引擎解析 JavaScript 脚本。
- 解析后的代码，调用 Node API。
- libuv 库负责 Node API 的执行。它将不同的任务分配给不同的线程，形成一个 Event Loop（事件循环），以异步的方式将任务的执行结果返回给 V8 引擎。
- V8 引擎再将结果返回给用户。

libuv 引擎中的事件循环6个阶段

libuv 引擎中的事件循环分为 6 个阶段，它们会按照顺序反复运行。每当进入某一个阶段的时候，都会从对应的回调队列中取出函数去执行。当队列为空或者执行的回调函数数量到达系统设定的阈值，就会进入下一阶段。

![[assets/Clippings/浏览器层面优化前端性能(1)Chrom组件与进程线程模型分析 - webkit - 周陆军的个人网站/IMG-20260629165307554.png|libuv 引擎中的事件循环分为 6 个阶段]]

从上图中，大致看出 node 中的事件循环的顺序：

外部输入数据–>轮询阶段(poll)–>检查阶段(check)–>关闭事件回调阶段(close callback)–>定时器检测阶段(timer)–>I/O 事件回调阶段(I/O callbacks)–>闲置阶段(idle, prepare)–>轮询阶段（按照该顺序反复运行）…

- timers 阶段：这个阶段执行 timer（setTimeout、setInterval）的回调
- timers 阶段会执行 setTimeout 和 setInterval 回调，并且是由 poll 阶段控制的。
	- 同样，在 Node 中定时器指定的时间也不是准确时间，只能是尽快执行。
- I/O callbacks 阶段：处理一些上一轮循环中的少数未执行的 I/O 回调
- idle, prepare 阶段：仅 node 内部使用
- poll 阶段：获取新的 I/O 事件, 适当的条件下 node 将阻塞在这里
	poll 是一个至关重要的阶段，这一阶段中，系统会做两件事情
- 回到 timer 阶段执行回调
	- 执行 I/O 回调

并且在进入该阶段时如果没有设定了 timer 的话，会发生以下两件事情

- 如果 poll 队列不为空，会遍历回调队列并同步执行，直到队列为空或者达到系统限制
	- 如果 poll 队列为空时，会有两件事发生
- 如果有 setImmediate 回调需要执行，poll 阶段会停止并且进入到 check 阶段执行回调
		- 如果没有 setImmediate 回调需要执行，会等待回调被加入到队列中并立即执行回调，这里同样会有个超时时间设置防止一直等待下去
- check 阶段：执行 setImmediate() 的回调
	setImmediate()的回调会被加入 check 队列中，从 event loop 的阶段图可以知道，check 阶段的执行顺序在 poll 阶段之后。
- setImmediate 设计在 poll 阶段完成时执行，即 check 阶段；
	- setTimeout 设计在 poll 阶段为空闲时，且设定时间到达后执行，但它在 timer 阶段执行
- close callbacks 阶段：执行 socket 的 close 事件回调

注意：上面六个阶段都不包括 process.nextTick()

> process.nextTick 这个函数其实是独立于 Event Loop 之外的，它有一个自己的队列，当每个阶段完成后，如果存在 nextTick 队列，就会清空队列中的所有回调函数，并且优先于其他 microtask 执行。

浏览器环境下，microtask 的任务队列是每个 macrotask 执行完之后执行。而在 Node.js 中，microtask 会在事件循环的各个阶段之间执行，也就是一个阶段执行完毕，就会去执行 microtask 队列的任务。

> 每个阶段都有一个先进先出的回调函数队列。只有一个阶段的回调函数队列清空了，该执行的回调函数都执行了，事件循环才会进入下一个阶段。

![[assets/Clippings/浏览器层面优化前端性能(1)Chrom组件与进程线程模型分析 - webkit - 周陆军的个人网站/IMG-20260629165307557.png|Node 与浏览器的 Event Loop 差异]]

nodejs 写的少，没有过多深入

```javascript
function f () {
  console.log('start')
  setTimeout(() => {
    console.log('timer1')
    Promise.resolve().then(function() {
      console.log('promise1')
    })
  }, 0)
  setTimeout(() => {
    console.log('timer2')
    Promise.resolve().then(function() {
      console.log('promise2')
    })
  }, 0)
  Promise.resolve().then(function() {
    console.log('promise3')
  })

  console.log('end')

}
f()
```

现在，浏览器和node12，输出顺序是一样的。推荐阅读软老师的《 [Node 定时器详解](https://www.ruanyifeng.com/blog/2018/02/node-event-loop.html) 》

从文章的 浏览器通常由以下常驻线程组成 里面的 渲染进程 已知， **GUI渲染线程与JS引擎线程是互斥的** ，他们会阻塞页面渲染。所以我们从浏览器的去分析下，怎么优化前端的性能呢？

下篇《 [浏览器层面优化前端性能(2):Reader引擎线程与模块分析优化点](https://www.zhoulujun.cn/html/webfront/browser/webkit/2020_0615_8464.html) 》

参考文章：

前端都该懂的浏览器工作原理，你懂了吗？ [https://segmentfault.com/a/1190000022633988](https://segmentfault.com/a/1190000022633988)

从浏览器多进程到JS单线程，JS运行机制最全面的一次梳理 https://www.cnblogs.com/cangqinglang/p/8963557.html

Chrome源码剖析、上--多线程模型、进程通信、进程模型 [https://www.cnblogs.com/v-July-v/archive/2011/04/02/2036008.html](https://www.cnblogs.com/v-July-v/archive/2011/04/02/2036008.html)

Chrome源代码分析之进程和线程模型（三） [https://blog.csdn.net/namelcx/article/details/6582730](https://blog.csdn.net/namelcx/article/details/6582730)

[http://dev.chromium.org/developers/design-documents/multi-process-architecture](http://dev.chromium.org/developers/design-documents/multi-process-architecture)

chrome渲染机制浅析 [https://www.jianshu.com/p/99e450fc04a5](https://www.jianshu.com/p/99e450fc04a5)

浅析浏览器渲染原理 https://segmentfault.com/a/1190000012960187

javascript宏任务和微任务 [https://www.cnblogs.com/fangdongdemao/p/10262209.html](https://www.cnblogs.com/fangdongdemao/p/10262209.html)

浏览器与Node的事件循环(Event Loop)有何区别? https://blog.csdn.net/Fundebug/article/details/86487117

转载 [本站](https://www.zhoulujun.cn/) 文章《 [浏览器层面优化前端性能(1):Chrom组件与进程/线程模型分析](https://www.zhoulujun.cn/html/webfront/browser/webkit/2020_0610_8455.html) 》,  
请注明出处： [https://www.zhoulujun.cn/html/webfront/browser/webkit/2020\_0610\_8455.html](https://www.zhoulujun.cn/html/webfront/browser/webkit/2020_0610_8455.html)