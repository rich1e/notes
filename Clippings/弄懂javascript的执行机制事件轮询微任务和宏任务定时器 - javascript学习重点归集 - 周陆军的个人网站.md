---
title: 弄懂javascript的执行机制:事件轮询|微任务和宏任务|定时器 - javascript学习重点归集 - 周陆军的个人网站
source: https://www.zhoulujun.cn/html/webfront/ECMAScript/js6/2015_1110_345.html
author:
  - "[[周陆军]]"
published: 2015-11-10
created: 2026-06-03
description: javascript是一门单线程语言，Event Loop是javascript的执行机制。主线程从“任务队列”中读取事件，这个过程是循环不断的。所有的同步任务都在主线程上指向，形成一个执行栈，主线程之外，还存在一个任务队列。只要异步任务有
tags:
  - clippings
  - javascript
  - f2e
  - programming
---
浏览器线程与JavaScript异步

想要理解EventLoop，就要从程序的运行模式讲起。运行以后的程序叫做"进程"（process），一般情况下，一个进程一次只能执行一个任务。

如果有很多任务需要执行，不外乎三种解决方法。

（1）排队。因为一个进程一次只能执行一个任务，只好等前面的任务执行完了，再执行后面的任务。

（2）新建进程。使用fork命令，为每个任务新建一个进程。

（3）新建线程。因为进程太耗费资源，所以如今的程序往往允许一个进程包含多个线程，由线程去完成任务。

因为无论什么时候都只有一个JS线程在运行JS程序，一旦遇到大量任务或者遇到一个耗时的任务，网页就会出现假死的状态，因为JavaScript停不下来，也就无法响应用户的行为。

> JavaScript从诞生起就是单线程。原因大概是不想让浏览器变得太复杂，因为多线程需要共享资源、且有可能修改彼此的运行结果，对于一种网页脚本语言来说，这就太复杂了。后来就约定俗成，JavaScript为一种单线程语言。（Worker API可以实现多线程，但是JavaScript本身始终是单线程的。）

未来解决这个问题，JavaScript采用EventLoop 运行机制，就是在程序中设置两个线程：一个负责程序本身的运行，称为"主线程"；另一个负责主线程与其他进程（主要是各种I/O操作）的通信，被称为"EventLoop线程"（可以译为"消息线程"）。

![[assets/Clippings/弄懂javascript的执行机制事件轮询微任务和宏任务定时器 - javascript学习重点归集 - 周陆军的个人网站/IMG-20260629165425842.png|EventLoop程序结构用于等待和发送消息和事件]]

EventLoop程序结构用于等待和发送消息和事件

在《 [浏览器层面优化前端性能(1):Chrom组件与进程/线程模型分析](https://www.zhoulujun.cn/html/webfront/browser/webkit/2020_0610_8455.html) 》里面分析浏览器的线程，这里摘要一些跟本篇相关的：

> ### 浏览器通常由以下常驻线程组成：
> 
> - GUI 渲染线程
> - JavaScript引擎线程
> - 定时触发器线程
> - 事件触发线程
> - 异步http请求线程
> 
> 事件触发线程
> 
> - 归属于浏览器而不是JS引擎，用来控制事件循环（可以理解，JS引擎自己都忙不过来，需要浏览器另开线程协助）
> 	动画帧任务
> 	- 当JS引擎执行代码块如setTimeOut时（也可来自浏览器内核的其他线程,如鼠标点击、AJAX异步请求等），会将对应任务添加到事件线程中.
> 	- 当对应的事件符合触发条件被触发时，该线程会把事件添加到待处理队列的队尾，等待JS引擎的处理
> 	- 注意， **由于JS的单线程关系，所以这些待处理队列中的事件都得排队等待JS引擎处理** （当JS引擎空闲时才会去执行）
> - 为什么有时候setTimeout推入的事件不能准时执行？因为可能在它推入到事件列表时，主线程还不空闲，正在执行其它代码，
> 
> JS引擎一直等待着任务队列中任务的到来，然后加以处理，一个Tab页（renderer进程）中 **无论什么时候都只有一个JS线程在运行JS程序**

event loop是实现异步的一种机制，JavaScript 异步主要靠 事件轮询（Event Loop）

没有经过Win32时代的洗礼，那可能对这个消息循环并不是很清楚，在你眼里只有注册事件，处理事件。

## win32 异步操作 与 消息循环

### Dos的过程驱动与Windows的事件驱动

- DOS程序主要使用顺序的，过程驱动的程序设计方法。 **顺序的，过程驱动的程序有一个明显的开始，明显的过程及一个明显的结束，因此程序能直接控制程序事件或过程的顺序。虽然在顺序的过程驱动的程序中也有很多处理异常的方法，但这样的异常处理也仍然是顺序的，过程驱动的结构** 。
- Windows的驱动方式是事件驱动，就是不由事件的顺序来控制，而是由事件的发生来控制，所有的事件是无序的，所为一个程序员，在你编写程序时，你并不知道用户先按哪个按纽，也不知道程序先触发哪个消息。 **你的任务就是对正在开发的应用程序要发出或要接收的消息进行排序和管理。事件驱动程序设计是密切围绕消息的产生与处理而展开的，一条消息是关于发生的事件的消息** 。

在dos里，程序能直接控制事件的发生顺序，结果等。而在Windows里，应用程序不直接调用任何窗口函数，而是等待Windows调用窗口函数，请求完成任务或返回信息。为保证Windows调用这个窗口函数，这个 **函数必须先向Windows登记，然后在Windows实施相应操作时回调** ，所以窗口函数又称为回调函数。WindowProc是一个主回调函数，Windows至少有一个回调函数。

可以复习下《 [再谈编程范式—程序语言背后的思想](https://www.zhoulujun.cn/html/theory/engineering/model/8139.html) 》,命令式编程 与 事件驱动编程 的差异

> 在Windows通信中，至少一些基本 **Windows通信，几乎都要用到消息** 。如果你想让窗口或控件(实质上，控件是特殊的窗口)执行何种动作，你应该传送一个消息给它；如果另一个窗口想让你执行何种操作，它可以传送一个消息给你。如果一个事件，如敲击键盘、移动鼠标、点击按钮等，系统将消息传送给窗口，如果你是这些窗口之一，你将接收到消息执行相应的操作。

可以用PostMessage()或SendMessage()发送消息。PostMessage()把一个消息放入消息队列(Message Queue)后立即返回，也就是当调用PostMessage()，函数执行完成返回时，很可能消息尚未处理。SendMessage()直接将消息发送到窗口，直到这个消息处理完成才返回。

### 消息队列(Message Queue)

当消息发送过来，将消息加入消息队列，当一个消息被处理时，将其从消息队列移除。这样确保消息不会丢失，当你正在处理一个消息时，其它到来的消息可以加入到消息队列直到被处理。

### 消息循环(Message Loop)

### 响应用户的输入就是靠消息循环，而消息循环就是在当前的线程上，也就是我们所谓的那个UI线程，如果一个耗时操作也同在UI线程上，那么消息循环就“卡着”了，也就无法处理后续的消息，程序也就假死了。

那我们如何处理这种耗时操作呢？当然就是将这个耗时操作放到另外一个线程中，不占用UI线程，让消息循环得以继续的进行下去。

消息循环是响应用户输入的根本

### 几乎所有使用Win32 API编写Windows Application的程序里都有：

```
MSG msg;
while(GetMessage(&msg,NULL,0,0))
{
    TranslateMessage(&msg);
    DispatchMessage(&msg);
}
```

Windows为每个Windows程序都维护了一个消息队列，当有用户输入事件的时候，Windows就把这个事件转换为一个称之为“消息”的东东（也就是上面代码中的MSG结构），在这个消息里包含有一些信息，比如鼠标点击的点啊，消息的类型啊等等。

而上面的while循环中的GetMessage方法就是不断的从这个消息队列里取消息出来，然后处理，这样窗体就能响应用户的输入了。

这里面一篇文章实在讲不完，推荐一篇文章《 [Win32消息循环机制等【转载】](https://blog.csdn.net/u013777351/article/details/49522219) 》——暂时没有找到原创地址，梯子坏了，也不好搜。

因为javascript是一门单线程语言，所以javascript是按照语句出现的顺序执行的。虽然HTML5提出了Web Worker，允许JavaScript脚本创建多个线程，但是子线程完全受主线程控制，且不得操作DOM和BOM。所以，依然没有改变JavaScript是单线程的本质。

## 为什么JavaScript是单线程？

同样的问题也可以问：

- **为什么PHP文件的执行是单线程的** ？
	每个PHP文件的执行是单线程的，但是，服务器（apache/nigix/php-fpm）是多线程的。每次对某个PHP文件的访问服务器都会创建一个新的进程/线程，用来执行对应的PHP文件。也就是说对于一个请求来说PHP是单线程的，但是多个请求间是并发的。
- **为什么是python是多线程是假的多线程** ？
	虽然Python解释器可以运行多个线程，但只有一个线程在解释器中运行。它不管你有几个核，单位时间多个核只能跑一个线程，然后时间片轮转。Python不能做到并行，但可以做到并发。

脚本语言本身效率就不高，设计目的就是应对I/O密集、高开发效率、简单易用……。可以说，脚本语言基本都是单线程的。

### 什么是计算密集型任务，什么是I/O密集型任务？

- **计算密集型任务由于主要消耗CPU资源** ，消耗CPU资源，比如计算圆周率、对视频进行高清解码等等，全靠CPU的运算能力。这种计算密集型任务虽然也可以用多任务完成，但是任务越多，花在任务切换的时间就越多，CPU执行任务的效率就越低，所以，要最高效地利用CPU，计算密集型任务同时进行的数量应当等于CPU的核心数。
- **涉及到网络、磁盘IO的任务都是IO密集型任务，这类任务的特点是CPU消耗很少，任务的大部分时间都在等待IO操作完成** （因为IO的速度远远低于CPU和内存的速度）。对于IO密集型任务，任务越多，CPU效率越高，但也有一个限度。常见的大部分任务都是IO密集型任务，比如Web应用。

IO密集型任务执行期间，99%的时间都花在IO上，花在CPU上的时间很少，因此，用运行速度极快的C语言替换用Python这样运行速度极低的脚本语言，完全无法提升运行效率。对于IO密集型任务，最合适的语言就是开发效率最高（代码量最少）的语言，脚本语言是首选，C语言最差。

注：进程和线程，一个是重量级的，一个轻量级的，重量级的进程有保护区，进程上下文都是操作系统保护的，而线程是自己管理，需要一定的技术，不能保证在并发时的稳定性（多进程也不稳定，但很容易看出来，因为多出了进程容易发现）

> JavaScript的单线程，与它的用途有关。作为浏览器脚本语言，JavaScript的主要用途是与用户互动，以及操作DOM。这决定了它只能是单线程，否则会带来很复杂的同步问题。比如，假定JavaScript同时有两个线程，一个线程在某个DOM节点上添加内容，另一个线程删除了这个节点，这时浏览器应该以哪个线程为准？
> 
> 所以， **为了避免复杂性，从一诞生，JavaScript就是单线程，这已经成了这门语言的核心特征，将来也不会改变** 。

JavaScript的单线程，在于浏览器的reader进程 JavaScript解析与执行线程 主线程只有一个。

起初我的理解，我以为宏任务就是新开一个进程，微任务就是在本线程内执行。比如：setTimeout/setInterval启动定时器、I/O操作、Web Workers等是新开一个线程，当然是宏任务。

其是不完全是这样的：

> JavaScript中，大多数宏任务并不会启动新的线程来执行。这些宏任务在JavaScript的单线程事件循环中被排队和处理。下面是一些不会启动新线程的宏任务示例：
> 
> 1. 整体脚本（全局代码）: 当浏览器开始执行一个JavaScript脚本时，整个脚本作为一个宏任务被执行。
> 2. setTimeout/setInterval: 这些函数会将回调函数延迟执行或定期执行，但 **回调函数的执行仍然在JavaScript的主线程中** 。
> 3. DOM事件处理器: 当用户与页面交互（如点击、键盘输入等）时触发的事件及其对应的处理程序。
> 4. UI渲染: 浏览器的渲染过程（如重排和重绘）也可以看作宏任务，尽管它们实际的渲染操作可能涉及浏览器的布局引擎和合成引擎（这些可能在不同的线程中执行），但是 **它们在事件循环中的调度是在主线程中进行的** 。
> 
> 需要注意的是，虽然setTimeout和setInterval涉及时间延迟，但 **定时器的设置和回调函数的执行仍然是在单线程的主线程上进行的** 。浏览器内部可能使用其他机制来跟踪和管理定时器，但处理它们的回调函数时不会为每个调用新开线程。
> 
> 正如上面提到的，真正意义上的多线程在JavaScript中通常是通过Web Workers来实现的。Web Workers允许开发者在后台线程中运行脚本，这个执行环境与主线程完全独立，使得可以在不影响主线程性能的情况下执行耗时任务。然而，尽管Web Workers是在后台线程中运行的，但我们通常不将其归类为宏任务或微任务，因为它们与主线程的事件循环是隔离的。

那么同一个线程内，宏任务与微任务的执行顺序是什么？总体顺序是什么来的？

## JavaScript任务队列

**单线程就意味着，所有任务需要排队，前一个任务结束，才会执行后一个任务。如果前一个任务耗时很长，后一个任务就不得不一直等着** 。

为了解决单线程导致的线程等待资源，cpu空闲，而其他任务一直等待的问题。将所有的任务分为两种，

- **同步任务（synchronous）** ：指的是，在主线程上排队执行的任务，只有前一个任务执行完毕，才能执行下一个任务。
- **异步任务（asynchronous）** ：指的是，不进入主线程，而进入“任务队列”的任务，自由“任务队列”通知主线程，某个异步任务可以执行了，该任务才会进入主线程执行。

具体来说，异步执行的运行机制如下。（同步执行也是如此，因为它可以被视为没有异步任务的异步执行。

1. 所有的同步任务都在主线程上指向，形成一个执行栈（execution context stack）。
2. 主线程之外，还存在一个“任务队列”（task queue）。只要异步任务有了运行结果，就在“任务队列”之中放置一个事件。
3. 一旦“执行栈”中的所有同步任务执行完毕，系统就会读取“任务队列”，将可执行的任务放在主线程执行。任务队列是一个先进先出的数据结构，排在前面的事件，优先被主线程读取。
4. 主线程不断重复上面的第三步。

![[assets/Clippings/弄懂javascript的执行机制事件轮询微任务和宏任务定时器 - javascript学习重点归集 - 周陆军的个人网站/IMG-20260629165425847.jpg|bg2014100801.jpg]]

**只要主线程空了，就会去读取"任务队列"，这就是JavaScript的运行环境。这个过程会不断重复。**

## 事件和回调函数

事件触发线程 维持一个事件队列 （类似 Message Queue ），IO设备完成一项任务（表示相关的异步任务可以进入"执行栈"了），如果需要回调，就在事件队列中添加一个事件。主线程读取"任务队列"，就是读取里面有哪些事件。

"任务队列"中的事件，除了IO设备的事件以外，还包括一些用户产生的事件（比如鼠标点击、页面滚动等等）。只要指定过回调函数，这些事件发生时就会进入"任务队列"，等待主线程读取。

所谓"回调函数"（callback），就是那些会被主线程“挂起来的代码”——待执行栈里面的代码执行完毕，再读取任务队列。异步任务必须指定回调函数，当主线程开始执行异步任务，就是执行对应的回调函数。

"任务队列"是一个先进先出的数据结构，排在前面的事件，优先被主线程读取。主线程的读取过程基本上是自动的，只要执行栈一清空，"任务队列"上第一位的事件就自动进入主线程。

> JavaScript事件队列等原因还是JavaScript线程与 定时触发器线程、事件触发线程、异步http请求线程等IO通信问题。《》
> 
> - 主线程运行时会产生执行栈
> - 栈中的代码调用某些api时，它们会在事件队列中添加各种事件（当满足触发条件后，如ajax请求完毕）
> - 而栈中的代码执行完毕，就会读取事件队列中的事件，去执行那些回调

注意，总是要等待栈中的代码执行完毕后才会去读取事件队列中的事件

## Event Loop（事件轮询）

事件驱动的的实现过程主要靠事件循环完成。进程启动后就进入主循环。主循环的过程就是不停的从事件队列里读取事件。如果事件有关联的handle(也就是注册的callback)，就执行handle。

![[assets/Clippings/弄懂javascript的执行机制事件轮询微任务和宏任务定时器 - javascript学习重点归集 - 周陆军的个人网站/IMG-20260629165425854.png|javascript执行流程]] ![[assets/Clippings/弄懂javascript的执行机制事件轮询微任务和宏任务定时器 - javascript学习重点归集 - 周陆军的个人网站/IMG-20260629165425858.png|JavaScript任务队列]]

除了放置异步任务的队列，“ **任务队列还放置定时器** ”，即指定某些代码在多长时间之后执行。

定时器功能的主要由setTimeout()和setInterval()这两个函数执行。

- setTimeout()只执行一次
- setInterval()反复执行

> 定时触发器线程
> 
> - 传说中的setInterval与setTimeout所在线程
> - 浏览器定时计数器并不是由JavaScript引擎计数的,（因为JavaScript引擎是单线程的, 如果处于阻塞线程状态就会影响记计时的准确）
> - 因此通过单独线程来计时并触发定时（计时完毕后，添加到事件队列中，等待JS引擎空闲后执行）
> - 定时器事件是靠事件循环不停检查系统时间来判定是否到达时间点来产生事件，到达时间点后，会形成一个事件（timeout事件）。
> 	所以，如果到达时间了，，事件队列不为空或当期执行栈没有执行完毕，定时触发线程产生的事件就会追加在 事件队列末尾，等待被执行。

**Node规定，process.nextTick和Promise的回调函数，追加在本轮循环，即同步任务一旦执行完成，就开始执行它们** 。

**而setTimeout、setInterval、setImmediate的回调函数，追加在次轮循环** 。

所以，需要注意的是

setTimeout()只是将事件插入了"任务队列"，必须等到当前代码（执行栈）执行完，主线程才会去执行它指定的回调函数。 **要是当前代码耗时很长，有可能要等很久，所以并没有办法保** 证，回调函数一定会在setTimeout()指定的时间执行。

setInterval(fn,ms)不是每过ms秒会执行一次fn，而是每过ms秒，会有fn进入Event Queue **。一旦setInterval的回调函数fn执行时间超过了延迟时间ms，那么就完全看不出来有时间间隔了** 。这句话请读者仔细品味。

> HTML5标准规定了setTimeout()的第二个参数的最小值（最短间隔），不得低于4毫秒，如果低于这个值，就会自动增加。在此之前，老版本的浏览器都将最短间隔设为10毫秒。另外，对于那些DOM的变动（尤其是涉及页面重新渲染的部分），通常不会立即执行，而是每16毫秒执行一次。这时使用requestAnimationFrame()的效果要好于setTimeout()。

除了广义的同步任务和异步的任务，更精细的定义为：

**macro-task(宏任务)** ：包括整体代码script、setTimeout，setInterval

**micro-task(微任务)** ：Promise、process.nextTick

![[assets/Clippings/弄懂javascript的执行机制事件轮询微任务和宏任务定时器 - javascript学习重点归集 - 周陆军的个人网站/IMG-20260629165425861.png|JavaScript 宏任务 微任务]] ![[assets/Clippings/弄懂javascript的执行机制事件轮询微任务和宏任务定时器 - javascript学习重点归集 - 周陆军的个人网站/IMG-20260629165425869.gif|JavaScript宏任务微任务动图解析]]

对于JavaScript异步回调，如setTimeout、Promise、Async/Await 。

> settimeout的回调函数放到宏任务队列里，等到执行栈清空以后执行；
> 
> **promise.then里的回调函数会放到相应宏任务的微任务队列里，等宏任务里面的同步代码执行完再执行** ；
> 
> async函数表示函数里面可能会有异步方法，await后面跟一个表达式，async方法执行时，遇到await会立即执行表达式，然后把表达式后面的代码放到微任务队列里，让出执行栈让同步代码先执行。

参看下篇《 [Javascript异步回调细数：promise yield async/await](https://www.zhoulujun.cn/html/webfront/ECMAScript/js/2017_0118_7944.html) 》 —— [https://www.zhoulujun.cn/html/webfront/ECMAScript/js/2017\_0118\_7944.html](https://www.zhoulujun.cn/html/webfront/ECMAScript/js/2017_0118_7944.html)

更多的动图解析，推荐阅读《 [\[译\]JavaScript可视化：Promise和Async/Await](https://zhuanlan.zhihu.com/p/138140285) 》

## Node.js事件循环

Node.js也是单线程的Event Loop，但是它的运行机制不同于浏览器（和浏览器中的是完全不相同的东西）

根据上图，Node.js的运行机制如下

- V8引擎解析JavaScript脚本
- 解析后的代码，调用Node API
- libuv库负责Node API的执行。它将不同的任务分配给不同的线程，形成一个Event Loop（事件循环），以异步的方式将任务的执行结果返回给V8引擎
- V8引擎再将结果返回给用户

![[assets/Clippings/弄懂javascript的执行机制事件轮询微任务和宏任务定时器 - javascript学习重点归集 - 周陆军的个人网站/IMG-20260629165425875.png|Node.js也是单线程的Event Loop]]

跟多深入的，推荐阅读《 [Chrom浏览器组件与进程/线程模型分析—优化前端性能](https://www.zhoulujun.cn/html/webfront/browser/webkit/2020_0610_8455.html) 》

## JS执行顺序笔试题

```javascript
console.log('1');
setTimeout(function() {
    console.log('2');
    process.nextTick(function() { console.log('3');})
    new Promise(function(resolve) {
        console.log('4');
        resolve();
    }).then(function() { console.log('5') })
})
process.nextTick(function() { console.log('6'); })
new Promise(function(resolve) {
    console.log('7');
    resolve();
}).then(function() { console.log('8') })

setTimeout(function() {
    console.log('9');
    process.nextTick(function() { console.log('10');})
    new Promise(function(resolve) {
        console.log('11');
        resolve();
    }).then(function() { console.log('12') })
})
console.log('13');
```

上述事件循环机制的核心是：JS引擎线程和事件触发线程

但事件上，里面还有一些隐藏细节，譬如调用setTimeout后，是如何等待特定时间后才添加到事件队列中的？

## 定时器

定时器是JS引擎检测的么？

当然不是了。它是由定时器线程控制（因为JS引擎自己都忙不过来，根本无暇分身）

为什么要单独的定时器线程？因为JavaScript引擎是单线程的, 如果处于阻塞线程状态就会影响记计时的准确，因此很有必要单独开一个线程用来计时。

什么时候会用到定时器线程？ **当使用setTimeout或setInterval时，它需要定时器线程计时，计时完成后就会将特定的事件推入事件队列中** 。

### setTimeout与setInterval

- setTimeout计时到到后触发事件触发器，插入一个任务到 事件队列
	延缓事件为：setTimeout触发是设置的等待事件+等待到任务执行时间）
- setInterval则是每次都精确的隔一段时间推入一个事件

而且setInterval有一些比较致命的问题就是：累计效应

如果setInterval代码在（setInterval）再次添加到队列之前还没有完成执行，就会导致定时器代码连续运行好几次，而之间没有间隔。

JS引擎会对setInterval进行优化， **如果当前事件队列中有setInterval的回调，不会重复添加** 。但是，有错过了延迟的事件。

> - 毫无压力的情况下setInterval性能更高。
> - 在相同时间，相同压力的情况下，都出现了跳帧超时，不过两人的原因不一样
> - setTimeout压根没有执行，
> 	- setInterval是因为抛弃了相同队列下相同定时器的其他callback也就是只保留了了队列中的第一个挤进来的callback。

一般认为的最佳方案是： **用setTimeout模拟setInterval，或者特殊场合直接用requestAnimationFrame** 。

> 在异步的情况下，比如ajax轮循(websocket不在讨论范围内)，我们只有一种选择就是setTimeout，原因只有一个——天晓得这次ajax要浪多久才肯回来，这种情况下只有setTimeout才能胜任。

## JS不同类型的事件和任务的执行优先级

在 JavaScript 的事件循环机制中，所有的任务都可以归类为宏任务（Macro Task）或微任务（Micro Task）。

**不是微任务，就是宏任务** ！

但在 JavaScript 中， **不同类型的事件和任务的执行优先级受到浏览器的事件循环机制的影响** 。

以下是常见的事件和任务按照执行优先级排列的列表。这个列表帮助我们理解在何时会执行特定类型的任务：

1. **同步任务** （Synchronous Tasks）
- 这些任务在当前调用栈中立即执行。包括常规的 JavaScript 代码。
3. **微任务** （Microtasks）
- Promise 的回调（then，catch，finally）
	- MutationObserver 的回调
	- queueMicrotask
- 微任务会在当前宏任务执行完成后、下一个宏任务开始前执行。微任务队列会在每个宏任务之后清空。
	- **常见的微任务** ：
6. **宏任务** （Macrotasks）
- setTimeout 回调
	- setInterval 回调
	- setImmediate 回调（仅在 Node.js 中）
	- I/O 回调
	- UI rendering 回调
- 宏任务是事件循环中的大块任务，宏任务队列在每次事件循环中执行一个宏任务。
	- **常见的宏任务** ：
9. **动画帧任务** （Animation Frame Tasks）
- requestAnimationFrame 的回调，这些任务通常在每一帧刷新时执行，依赖于屏幕的刷新率（一般为 60Hz）。
- **常见的动画帧任务** ：
- **平滑滚动（Smooth Scrolling）** ： 使用 requestAnimationFrame 逐帧更新滚动位置，创造平滑的滚动效果。
		- **元素移动（Element Movement）** ： 逐帧更新元素的位置，以实现平滑的移动效果。比如在游戏开发中，角色或物体的移动动画。
		- **CSS 属性过渡（CSS Property Transitions）** ： 通过逐帧调整 CSS 属性值，实现平滑的过渡效果。例如，改变元素的透明度、宽度、高度等。
		- **帧动画（Frame Animation）** ： 在一定时间内依次显示一系列图片，形成动画效果。通常用于制作类似 GIF 的效果。
		- **帧率调节（Frame Rate Throttling）** ： 控制动画的帧率，以实现不同的动画速度和效果。
		- **画布绘图（Canvas Drawing）** ： 使用 HTML5 Canvas 进行逐帧绘制，通常用于游戏或复杂的图形动画。
		- **物理模拟（Physics Simulation）** ： 在游戏或动画中，逐帧计算物体的物理属性（如位置、速度、加速度等），并更新显示。
		- **粒子效果（Particle Effects）** ： 创建和控制大量小粒子的动画效果，例如火焰、烟雾、爆炸等。
**循环动画（Looping Animations）** ： 创建无限循环的动画效果，例如旋转的加载图标。
12. **事件任务** （Event Tasks）
- postMessage 的回调
	- 用户交互事件（click, keydown, mousemove 等）
	- 网络事件（onload, onerror 等）
	- 浏览器事件（如用户交互事件、DOM 事件）触发的任务。

可以这么说吗，不是微任务，就是宏任务

### 综合优先级列表

综合考虑以上分类，下面是不同事件和任务类型的优先级排列，从高到低：

1. **同步任务**
2. **微任务**
- Promise 回调
	- MutationObserver 回调
	- queueMicrotask
4. **事件任务**
- postMessage 回调
	- 用户交互事件（click, keydown, mousemove 等）
	- 网络事件（onload, onerror 等）
6. **动画帧任务**
- requestAnimationFrame 回调
8. **宏任务**
- setTimeout 回调
	- setInterval 回调
	- setImmediate 回调（仅在 Node.js 中）
	- I/O 回调
	- UI rendering 回调

#### 注意事项

1. **事件循环** ：浏览器在处理任务时，会按照上述优先级顺序执行。每个宏任务完成后，会检查并执行所有在该宏任务期间添加的微任务。
2. **交互复杂性** ：实际执行顺序还会受到任务添加时机、任务嵌套等因素的影响。浏览器在处理大量微任务时，可能会在微任务执行期间插入宏任务以避免 UI 冻结。

总结：

### js的异步

我们从最开头就说 **javascript是一门单线程语言，不管是什么新框架新语法糖实现的所谓异步，其实都是用同步的方法去模拟的** ，牢牢把握住单线程这点非常重要。

### 事件循环Event Loop

事件循环是js实现异步的一种方法，也是js的执行机制。

### javascript的执行和运行

执行和运行有很大的区别，javascript在不同的环境下，比如node，浏览器，Ringo等等，执行方式是不同的。而运行大多指javascript解析引擎，是统一的。

如果学过java，可以回顾一下java定时任务的实现，可以加深对JavaScript的理解。本人就是从java转JavaScript的

这里也推荐阅读下《 [漫谈Java多线程并发编程](https://www.zhoulujun.cn/html/java/javaBase/8471.html) 》，Java的异步与JavaScript的区别，这里不过多赘述。

## 回顾java定时器

主要有三种方式，new Timer().schedule、使用线程控制。

### 1、使用线程控制

创建一个thread，然后让它在while循环里一直运行着，通过sleep方法来达到定时任务的效果

```java
public class Task1 {
    public static void main(String[] args) {
        // run in a second
        // 每一秒钟执行一次
        final long timeInterval = 1000;
        Runnable runnable = new Runnable() {
            public void run() {
                while (true) {
                    // ------- code for task to run
                    // ------- 要运行的任务代码
                    System.out.println("Hello, stranger");
                    // ------- ends here
                    try {
                        // sleep()：同步延迟数据，并且会阻塞线程
                        Thread.sleep(timeInterval);
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }
                }
            }
        };
        //创建定时器
        Thread thread = new Thread(runnable);
        //开始执行
        thread.start();
    }
}
```

使用线程来控制就更灵活一些，可以根据自己的需要判断什么时候运行，什么时候停止，这需要对java的线程有一定的了解。

### 2、使用Timer的schedule

schedule有3个参数：schedule(TimerTask task, long delay, long period)

启动和去取消任务时可以控制，可以指定你想要的delay（开始执行的等待时间）时间，在实现时，Timer类可以调度任务，TimerTask则是通过在run()方法里实现具体任务。 Timer实例可以调度多任务，它是线程安全的。 当Timer的构造器被调用时，它创建了一个线程，这个线程可以用来调度任务。

```java
// 调用的工具
import java.util.Timer;
import java.util.TimerTask;

public class Task2 {
    public static void main(String[] args) {
        /**
         * Timer：是一个定时器工具，用来执行指定任务
         * TimerTask：是一个抽象类，他的子类可以代表一个被Timer计划的任务
         */
        TimerTask task = new TimerTask() {
            @Override
            public void run() {
                // task to run goes here
                // 执行的输出的内容
                System.out.println("Hello, stranger");
            }
        };
        Timer timer = new Timer();
        // 定义开始等待时间  --- 等待 5 秒
        // 1000ms = 1s
        long delay = 5000;
        // 定义每次执行的间隔时间
        long intevalPeriod = 5 * 1000;
        // schedules the task to be run in an interval
        // 安排任务在一段时间内运行
        timer.scheduleAtFixedRate(task, delay, intevalPeriod);
    } // end of main
}
```

在Timer定时任务中，最主要涉及到了两个类：Timer和TimerTask。他们俩的关系也特别容易理解，TimerTask把我们得业务逻辑写好之后，然后使用Timer定时执行就

Timer在执行定时任务时只会创建一个线程，所以如果存在多个任务，且任务时间过长，超过了两个任务的间隔时间，会发生一些缺陷。

这里和我们的JavaScript事件是一样的。

### 3、使用ScheduledExecutorService ，

ScheduledExecutorService是从Java SE5的java.util.concurrent里，做为并发工具类被引进的，这是最理想的定时任务实现方式。

```typescript
//调用的工具
import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.TimeUnit;

public class Task3 {
    public static void main(String[] args) {
        /**
         * Runnable：实现了Runnable接口，jdk就知道这个类是一个线程
         */
        Runnable runnable = new Runnable() {
            //创建 run 方法
            public void run() {
                // task to run goes here
                System.out.println("Hello, stranger");
            }
        };
        // ScheduledExecutorService:是从Java SE5的java.util.concurrent里，
        // 做为并发工具类被引进的，这是最理想的定时任务实现方式。
        ScheduledExecutorService service = Executors
                .newSingleThreadScheduledExecutor();
        // 第二个参数为首次执行的延时时间，第三个参数为定时执行的间隔时间
        // 10：秒   5：秒
        // 第一次执行的时间为10秒，然后每隔五秒执行一次
        service.scheduleAtFixedRate(runnable, 10, 5, TimeUnit.SECONDS);
    }
}
```

相比于上两个方法，它有以下好处

1.相比于Timer的单线程，它是通过线程池的方式来执行任务的

2.可以很灵活的去设定第一次执行任务delay时间

3.提供了良好的约定，以便设定执行的时间间隔

参考文章：

https://www.WinForm二三事（二）异步操作 cnblogs.com/yuyijq/archive/2009/11/16/1603621.html

事件轮询(Event Loop) https://blog.csdn.net/qq\_21630623/article/details/77946041

JavaScript 运行机制详解：再谈Event Loop [www.ruanyifeng.com/blog/2014/10/event-loop.html](http://www.ruanyifeng.com/blog/2014/10/event-loop.html)

这一次，彻底弄懂 JavaScript 执行机制 [https://juejin.im/post/59e85eebf265da430d571f89](https://juejin.im/post/59e85eebf265da430d571f89)

JavaScript是多线程还是单线程？ [https://blog.csdn.net/qq\_36995542/article/details/80007381](https://blog.csdn.net/qq_36995542/article/details/80007381)

既然Python解释器是单线程的，还有进行多线程编程的必要吗？ [https://www.wukong.com/answer/6584417230828601613/](https://www.wukong.com/answer/6584417230828601613/?iid=39055545733)

为什么有人说 Python 的多线程是鸡肋呢？ [https://www.zhihu.com/question/23474039/answer/269526476](https://www.zhihu.com/question/23474039/answer/269526476)

JAVA：定时器的三种方法（详细注解） [https://blog.csdn.net/qq\_36537546/article/details/83044977](https://blog.csdn.net/qq_36537546/article/details/83044977)

java的几种定时器 [https://blog.csdn.net/coolwindd/article/details/82804189](https://blog.csdn.net/coolwindd/article/details/82804189)

java任务调度之Timer定时器（案例和源码分析） [https://baijiahao.baidu.com/s?id=1645906817252040900&wfr=spider&for=pc](https://baijiahao.baidu.com/s?id=1645906817252040900&wfr=spider&for=pc)

[http://winprog.org/tutorial/message\_loop.html](http://winprog.org/tutorial/message_loop.html)

转载 [本站](https://www.zhoulujun.cn/) 文章《 [弄懂javascript的执行机制:事件轮询|微任务和宏任务|定时器](https://www.zhoulujun.cn/html/webfront/ECMAScript/js6/2015_1110_345.html) 》,  
请注明出处： [https://www.zhoulujun.cn/html/webfront/ECMAScript/js6/2015\_1110\_345.html](https://www.zhoulujun.cn/html/webfront/ECMAScript/js6/2015_1110_345.html)