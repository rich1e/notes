---
title: "battle-tested-patterns 模式目录（46 条）"
category: references
tags:
  - design-patterns
  - reference
  - catalog
  - data-structures
  - concurrency
sources:
  - "https://github.com/Totoro-jam/battle-tested-patterns"
created: 2026-07-08T07:14:00Z
updated: 2026-07-08T07:14:00Z
summary: 46 个代码级编程模式按"数据结构 / 并发 / 系统 / 内存 / 行为"五类整理，每条带一句话定位 + 2 个生产级源码出处（行号精确）。
tier: core
lifecycle: draft
lifecycle_changed: 2026-07-08
base_confidence: 0.85
provenance:
  extracted: 0.95
  inferred: 0.05
  ambiguous: 0
visibility: public
relationships:
  - target: "[[entities/battle-tested-patterns]]"
    type: related_to
  - target: "[[concepts/programming-pattern-categories]]"
    type: related_to
  - target: "[[skills/pattern-study-method]]"
    type: related_to
---

# battle-tested-patterns 模式目录（46 条）

> 摘自 [Totoro-jam/battle-tested-patterns](https://github.com/Totoro-jam/battle-tested-patterns) 的 `README.md` + `docs/patterns/index.md`（2026-07-08 抓取）。
> 每个模式的完整页面、交互式可视化、4 语言练习在 [文档站](https://totoro-jam.github.io/battle-tested-patterns/)。

## 🧠 数据结构（11）

| 模式 | 一句话 | 出处（精确到行） |
|---|---|---|
| **Bitmask** | N 个标志位压入一个整数，O(1) 测任意组合 | [React Flags](https://github.com/facebook/react/blob/34b78a2897cc208260a88e6b62ecaf9ca2a9dfe4/packages/react-reconciler/src/ReactFiberFlags.js#L14-L36) · [Linux stat.h](https://github.com/torvalds/linux/blob/acb7500801e98639f6d8c2d796ed9f64cba83d3a/include/uapi/linux/stat.h#L25-L33) |
| **Min Heap** | O(1) 看优先级最高项，O(log n) 推/弹 | [React MinHeap](https://github.com/facebook/react/blob/34b78a2897cc208260a88e6b62ecaf9ca2a9dfe4/packages/scheduler/src/SchedulerMinHeap.js#L17-L90) · [Linux CFS](https://github.com/torvalds/linux/blob/acb7500801e98639f6d8c2d796ed9f64cba83d3a/kernel/sched/fair.c#L1407-L1460) |
| **Ring Buffer** | 定长循环队列，零分配 | [LMAX Disruptor](https://github.com/LMAX-Exchange/disruptor/blob/c871ca49826a6be7ada6957f6fbafcfecf7b1f87/src/main/java/com/lmax/disruptor/RingBuffer.java#L84-L130) · [Linux](https://github.com/torvalds/linux/blob/acb7500801e98639f6d8c2d796ed9f64cba83d3a/include/linux/ring_buffer.h#L12-L70) |
| **Trie** | O(k) 前缀查找，共享前缀共享节点 | [Linux FIB](https://github.com/torvalds/linux/blob/acb7500801e98639f6d8c2d796ed9f64cba83d3a/net/ipv4/fib_trie.c#L80-L120) · [Redis rax](https://github.com/redis/redis/blob/df63a65d4d4ee33ae67e9f101885074febe0bccb/src/rax.h#L80-L130) |
| **Skip List** | 概率 O(log n) 有序结构 | [Redis zset](https://github.com/redis/redis/blob/df63a65d4d4ee33ae67e9f101885074febe0bccb/src/t_zset.c#L70-L130) · [LevelDB](https://github.com/google/leveldb/blob/7ee830d02b623e8ffe0b95d59a74db1e58da04c5/db/skiplist.h#L40-L90) |
| **Bloom Filter** | 概率性集合判存，零假阴 | [LevelDB](https://github.com/google/leveldb/blob/7ee830d02b623e8ffe0b95d59a74db1e58da04c5/util/bloom.cc#L17-L80) · [Chromium](https://github.com/chromium/chromium/blob/92b3e1f66aa55921a0ab431b7c17b25ae1f3faef/third_party/blink/renderer/core/css/selector_filter.h#L149-L175) |
| **LRU Cache** | 淘汰最久未用，O(1) get/put | [groupcache](https://github.com/golang/groupcache/blob/2c02b8208cf8c02a3e358cb1d9b60950647543fc/lru/lru.go#L28-L76) · [Linux](https://github.com/torvalds/linux/blob/acb7500801e98639f6d8c2d796ed9f64cba83d3a/include/linux/list_lru.h#L15-L55) |
| **B+ Tree** | 高扇出平衡树，叶链表便于范围扫描 | [PostgreSQL nbtinsert](https://github.com/postgres/postgres/blob/e18b0cb7344cb4bd28468f6c0aeeb9b9241d30aa/src/backend/access/nbtree/nbtinsert.c#L22-L55) · [SQLite](https://github.com/sqlite/sqlite/blob/2cb57d9d4ac7eac3b1d15cfa71511f54817cb3e4/src/btreeInt.h#L190-L198) |
| **Tagged Union** | 类型 tag + union，安全分发 | [Godot Variant](https://github.com/godotengine/godot/blob/ec67cbe92628bdaf979b10594359ba6f02cf8838/core/variant/variant.h#L78-L120) · [PyTorch IValue](https://github.com/pytorch/pytorch/blob/7469c0815567461107545b9cb5278846171ed828/aten/src/ATen/core/ivalue.h#L51-L96) |
| **Merkle Tree** | 自底向上哈希，O(log n) 完整性证明 | [Git tree.c](https://github.com/git/git/blob/1ff279f3404a482a83fb04c7457e41ab26884aea/tree.c#L136-L171) · [ZFS blkptr](https://github.com/openzfs/zfs/blob/7e054b2e7ea80c7c838f7fd44b7d517eea5c9d18/module/zfs/blkptr.c#L30-L77) |
| **Merge Iterator** | K 路合并有序流 | [LevelDB merger](https://github.com/google/leveldb/blob/7ee830d02b623e8ffe0b95d59a74db1e58da04c5/table/merger.cc#L17-L100) · [RocksDB merge_helper](https://github.com/facebook/rocksdb/blob/7affaee1c49ebc80cb213ad86fe7d2a3ad447da2/db/merge_helper.cc#L87-L156) |

## ⚡ 并发（9）

| 模式 | 一句话 | 出处 |
|---|---|---|
| **Semaphore** | 计数器限制并发访问 | [Linux](https://github.com/torvalds/linux/blob/acb7500801e98639f6d8c2d796ed9f64cba83d3a/include/linux/semaphore.h#L15-L55) · [Go x/sync](https://github.com/golang/sync/blob/5071ed6a9f1617117556b66384f765c934de3698/semaphore/semaphore.go) |
| **Actor Model** | 私有 state + 邮箱，无锁仅消息 | [Akka](https://github.com/akka/akka/blob/aded7b67a9dafcb32b8a5dc95f6debce3a97c0e9/akka-actor/src/main/scala/akka/actor/Actor.scala#L476-L547) · [Erlang/OTP](https://github.com/erlang/otp/blob/1f1daf0b156853659106bbf64aa6f9b5b8400c6a/erts/emulator/beam/erl_process.h#L1043-L1205) |
| **Work Stealing** | 闲线程从忙队列偷活 | [Go proc.go](https://github.com/golang/go/blob/f5cdf4745455415c7a43cfc7d925214d4511489b/src/runtime/proc.go#L3836-L3903) · [Tokio](https://github.com/tokio-rs/tokio/blob/bde89678532a8091d958268c0d36eac9362317d8/tokio/src/runtime/scheduler/multi_thread/worker.rs#L1136-L1175) |
| **MVCC** | 时间戳版本，读不阻塞写 | [PostgreSQL](https://github.com/postgres/postgres/blob/e18b0cb7344cb4bd28468f6c0aeeb9b9241d30aa/src/backend/access/heap/heapam_visibility.c#L917-L1096) · [etcd kvstore](https://github.com/etcd-io/etcd/blob/e9b62f804766edf77cfa918d600cb6fb2c56b401/server/storage/mvcc/kvstore.go#L53-L135) |
| **Cooperative Scheduling** | 工作片段间让出控制权保响应性 | [React Scheduler](https://github.com/facebook/react/blob/34b78a2897cc208260a88e6b62ecaf9ca2a9dfe4/packages/scheduler/src/forks/Scheduler.js#L188-L258) · [Go Runtime](https://github.com/golang/go/blob/f5cdf4745455415c7a43cfc7d925214d4511489b/src/runtime/proc.go#L4143-L4200) |
| **Double Buffering** | 交换两份副本做原子更新 | [React Fiber](https://github.com/facebook/react/blob/34b78a2897cc208260a88e6b62ecaf9ca2a9dfe4/packages/react-reconciler/src/ReactFiber.js#L327-L355) · [SDL_render](https://github.com/libsdl-org/SDL/blob/14b0e9d922da78001223e563efd2f54f473a4115/src/render/SDL_render.c) |
| **Backpressure** | 消费跟不上时让生产者减速 | [Node.js Streams](https://github.com/nodejs/node/blob/19c46abbefdb8711b913d7237b3c1299367f87d7/lib/internal/streams/writable.js#L312-L370) · [Reactive Streams](https://github.com/reactive-streams/reactive-streams-jvm/blob/a625d3aba756e9842ad1291a5b73f5db280b6168/api/src/main/java/org/reactivestreams/Subscription.java#L14-L37) |
| **Event Loop** | 单线程循环用 epoll/kqueue 多路复用 I/O | [libuv](https://github.com/libuv/libuv/blob/f6b713398e464a9f166328765be1703fd860981f/src/unix/core.c#L427-L492) · [Redis ae](https://github.com/redis/redis/blob/df63a65d4d4ee33ae67e9f101885074febe0bccb/src/ae.c#L360-L468) |
| **Logical Clock** | 单调计数器为事件排序，不靠墙钟 | [etcd](https://github.com/etcd-io/etcd/blob/e9b62f804766edf77cfa918d600cb6fb2c56b401/server/storage/mvcc/kvstore.go#L53-L72) · [LevelDB](https://github.com/google/leveldb/blob/7ee830d02b623e8ffe0b95d59a74db1e58da04c5/db/dbformat.h#L62-L66) |

## 🏗️ 系统（12）

| 模式 | 一句话 | 出处 |
|---|---|---|
| **Circuit Breaker** | 失败服务停调用，快速失败 | [Hystrix](https://github.com/Netflix/Hystrix/blob/5ce3bc58c38e7ca60ef2fe0e516e390e294ad941/hystrix-core/src/main/java/com/netflix/hystrix/HystrixCircuitBreaker.java#L138-L289) · [gobreaker](https://github.com/sony/gobreaker/blob/fed8e9eb35f9cd3e5c2a67842c924346c3e1fbdd/gobreaker.go#L117-L131) |
| **Rate Limiter** | 令牌桶控制吞吐 | [Go rate](https://github.com/golang/time/blob/812b343c8714c317b0dad633efa6d103e554c006/rate/rate.go#L57-L66) · [Nginx limit_req](https://github.com/nginx/nginx/blob/d994f5b8220847eb8f7e4400be5f7e6eb4538e46/src/http/modules/ngx_http_limit_req_module.c#L405-L532) |
| **Retry Backoff** | 失败时指数退避 + 抖动 | [Kubernetes wait](https://github.com/kubernetes/kubernetes/blob/586cc904093af4fe7492e564908a796f0b107f97/staging/src/k8s.io/apimachinery/pkg/util/wait/backoff.go#L30-L50) · [gRPC connection-backoff](https://github.com/grpc/grpc/blob/19f781499b13a4890bc39d1a0e6a7909d3294de5/doc/connection-backoff.md) |
| **Write-Ahead Log** | 变更先写日志再应用，崩溃可恢复 | [etcd wal](https://github.com/etcd-io/etcd/blob/e9b62f804766edf77cfa918d600cb6fb2c56b401/server/storage/wal/wal.go#L72-L95) · [PostgreSQL xlog](https://github.com/postgres/postgres/blob/e18b0cb7344cb4bd28468f6c0aeeb9b9241d30aa/src/backend/access/transam/xlog.c) |
| **Batch Processing** | 累积操作成组执行 | [Kafka RecordAccumulator](https://github.com/apache/kafka/blob/ab53829feb7280a1d453ebdaad032c4b64bb0f4d/clients/src/main/java/org/apache/kafka/clients/producer/internals/RecordAccumulator.java#L69-L120) |
| **Consistent Hashing** | 增删节点只重映射 ~1/n 键 | [groupcache](https://github.com/golang/groupcache/blob/2c02b8208cf8c02a3e358cb1d9b60950647543fc/consistenthash/consistenthash.go#L28-L81) · [HAProxy chash](https://github.com/haproxy/haproxy/blob/fb38e40ad5751090992cde15d919866b1e91b8aa/src/lb_chash.c#L415-L491) |
| **Dependency Graph** | DAG + 拓扑排序定执行序 | [Cargo dep_cache](https://github.com/rust-lang/cargo/blob/b50aa179d3d1099b53548bc8693dd17ddd019ab4/src/cargo/core/resolver/dep_cache.rs#L1-L50) · [pnpm workspace-sorter](https://github.com/pnpm/pnpm/blob/46fd26afc9926b4391636a851ae32493f9b2c9ff/workspace/projects-sorter/src/index.ts) |
| **Middleware Chain** | 复合处理器，前/后包裹下一层 | [gRPC-Go](https://github.com/grpc/grpc-go/blob/f1864955bbb48efa131f6652933fa8b2189d9305/server.go#L1224-L1260) · [Koa.js](https://github.com/koajs/koa/blob/78efdc87df1f8d49a494f313d478814d67c3f00f/lib/application.js#L152-L204) |
| **Registry** | 组件按名自注册到全局查找表 | [TensorFlow op.h](https://github.com/tensorflow/tensorflow/blob/b4c7e9a660badf8c8c81075fe9f781d23ed6f28a/tensorflow/core/framework/op.h#L258-L290) · [gRPC-Go](https://github.com/grpc/grpc-go/blob/f1864955bbb48efa131f6652933fa8b2189d9305/server.go#L154-L170) |
| **Dirty Flag** | 变更时标脏，延迟到真需要再算 | [Chromium/Blink](https://github.com/chromium/chromium/blob/92b3e1f66aa55921a0ab431b7c17b25ae1f3faef/third_party/blink/renderer/core/layout/layout_object.h#L1425-L1430) · [React](https://github.com/facebook/react/blob/34b78a2897cc208260a88e6b62ecaf9ca2a9dfe4/packages/react-reconciler/src/ReactFiberFlags.js#L18-L22) |
| **LSM Tree** | 写缓冲在内存，按序落盘 | [LevelDB DBImpl](https://github.com/google/leveldb/blob/7ee830d02b623e8ffe0b95d59a74db1e58da04c5/db/db_impl.cc#L1241-L1368) · [RocksDB MemTable](https://github.com/facebook/rocksdb/blob/7affaee1c49ebc80cb213ad86fe7d2a3ad447da2/db/memtable.cc#L458-L534) |
| **Checkpointing** | 周期快照，从 checkpoint 恢复 | [PostgreSQL](https://github.com/postgres/postgres/blob/e18b0cb7344cb4bd28468f6c0aeeb9b9241d30aa/src/backend/postmaster/checkpointer.c#L218-L360) · [Redis RDB](https://github.com/redis/redis/blob/df63a65d4d4ee33ae67e9f101885074febe0bccb/src/rdb.c#L1414-L1529) |

## ♻️ 内存（8）

| 模式 | 一句话 | 出处 |
|---|---|---|
| **Object Pool** | 预分配复用以绕开 GC | [Go sync.Pool](https://github.com/golang/go/blob/f5cdf4745455415c7a43cfc7d925214d4511489b/src/sync/pool.go#L52-L97) · [Godot pooled_list](https://github.com/godotengine/godot/blob/ec67cbe92628bdaf979b10594359ba6f02cf8838/core/templates/pooled_list.h#L35-L100) |
| **Flyweight** | 共享相同对象避免重复 | [Python int cache](https://github.com/python/cpython/blob/7a014f44c393fda6d1c4bd135608ebcfc21d626c/Objects/longobject.c#L61-L75) |
| **Arena Allocator** | 区域式 bump-alloc，一次性释放 | [bumpalo](https://github.com/fitzgen/bumpalo/blob/d2cc4dd0b8830d5b05d44e9decc776823e6a70ea/src/lib.rs#L378-L383) · [Go arena](https://github.com/golang/go/blob/f5cdf4745455415c7a43cfc7d925214d4511489b/src/arena/arena.go#L44-L67) |
| **Free List** | 用已释放槽链表做 O(1) 分配/释放 | [Go mfixalloc](https://github.com/golang/go/blob/f5cdf4745455415c7a43cfc7d925214d4511489b/src/runtime/mfixalloc.go#L31-L109) · [Linux SLUB](https://github.com/torvalds/linux/blob/acb7500801e98639f6d8c2d796ed9f64cba83d3a/mm/slub.c#L530-L551) |
| **Copy-on-Write** | 共享引用，写时再拷贝 | [Git objects](https://github.com/git/git/blob/1ff279f3404a482a83fb04c7457e41ab26884aea/object-file.c#L719-L730) · [Rust Cow](https://github.com/rust-lang/rust/blob/ab26b175979ee7b2cb3302dce204b99df96f7efb/library/alloc/src/borrow.rs#L169-L220) |
| **Reference Counting** | 原子计数追踪所有者，归零即清 | [CPython](https://github.com/python/cpython/blob/7a014f44c393fda6d1c4bd135608ebcfc21d626c/Include/refcount.h#L255-L310) · [Rust Arc](https://github.com/rust-lang/rust/blob/ab26b175979ee7b2cb3302dce204b99df96f7efb/library/alloc/src/sync.rs#L269-L276) |
| **Tombstone** | 删除打墓碑，后台回收 | [LevelDB dbformat](https://github.com/google/leveldb/blob/7ee830d02b623e8ffe0b95d59a74db1e58da04c5/db/dbformat.h#L39-L43) · [Cassandra](https://github.com/apache/cassandra/blob/3831d8265d748c21c0fef9d31d4777b134b20637/src/java/org/apache/cassandra/db/DeletionTime.java#L37-L99) |
| **Interning** | 去重不可变值，指针等价 | [Rust Symbol](https://github.com/rust-lang/rust/blob/ab26b175979ee7b2cb3302dce204b99df96f7efb/compiler/rustc_span/src/symbol.rs#L24-L79) · [CPython](https://github.com/python/cpython/blob/7a014f44c393fda6d1c4bd135608ebcfc21d626c/Objects/unicodeobject.c#L14416-L14472) |

## 🔄 行为（6）

| 模式 | 一句话 | 出处 |
|---|---|---|
| **State Machine** | 显式状态，不可能转移不可表达 | [XState](https://github.com/statelyai/xstate/blob/9d9b9f1439b773979c5120a793215f5aa4568d8f/packages/core/src/StateMachine.ts#L58-L120) · [Linux TCP](https://github.com/torvalds/linux/blob/acb7500801e98639f6d8c2d796ed9f64cba83d3a/net/ipv4/tcp_input.c#L4865-L4920) |
| **Observer** | 订阅事件，解耦生产消费 | [Node EventEmitter](https://github.com/nodejs/node/blob/19c46abbefdb8711b913d7237b3c1299367f87d7/lib/events.js#L456-L520) · [Redux createStore](https://github.com/reduxjs/redux/blob/1d761f471cf58faabe88c50ea16645212d986cd0/src/createStore.ts#L211-L280) |
| **Iterator** | 惰性序列，无中间分配 | [Rust Iterator](https://github.com/rust-lang/rust/blob/ab26b175979ee7b2cb3302dce204b99df96f7efb/library/core/src/iter/traits/iterator.rs#L68-L112) · [Python genobject](https://github.com/python/cpython/blob/7a014f44c393fda6d1c4bd135608ebcfc21d626c/Objects/genobject.c) |
| **Diff / Patch** | 计算两序列最小编辑 | [React Reconciler](https://github.com/facebook/react/blob/34b78a2897cc208260a88e6b62ecaf9ca2a9dfe4/packages/react-reconciler/src/ReactChildFiber.js#L1169-L1340) · [Git diff.c](https://github.com/git/git/blob/1ff279f3404a482a83fb04c7457e41ab26884aea/diff.c#L5020-L5060) |
| **Vtable** | 函数指针结构做多态 | [Linux file_operations](https://github.com/torvalds/linux/blob/acb7500801e98639f6d8c2d796ed9f64cba83d3a/include/linux/fs.h#L2093-L2163) · [CPython PyTypeObject](https://github.com/python/cpython/blob/7a014f44c393fda6d1c4bd135608ebcfc21d626c/Include/cpython/object.h#L250-L340) |
| **Visitor** | 树上节点分发类型化回调 | [LLVM InstVisitor](https://github.com/llvm/llvm-project/blob/7087ea37449027cc4c73a375b542cdc397c4474b/llvm/include/llvm/IR/InstVisitor.h#L45-L107) · [Vue vIf](https://github.com/vuejs/core/blob/48ad452dd61926a59e358da3c74c5ef750ae21c4/packages/compiler-core/src/transforms/vIf.ts#L35-L60) |

## 出现过的项目（"Proven In" 概览）

按出现频次 ^[inferred]：

- **Linux Kernel** — 出现最多（Bitmask, Min Heap, Ring Buffer, Trie, LRU Cache, Semaphore, Cooperative Scheduling, MVCC, Tombstone, Free List, Vtable, State Machine, Checkpointing…）
- **React** — Bitmask, Double Buffering, Cooperative Scheduling, Min Heap, Diff/Patch, Dirty Flag
- **Go** — Object Pool, Arena Allocator, Free List, Semaphore, Work Stealing, Consistent Hashing
- **PostgreSQL** — B+ Tree, MVCC, Write-Ahead Log, Checkpointing
- **LevelDB / RocksDB** — Bloom Filter, Skip List, Logical Clock, LSM Tree, Merge Iterator, Tombstone
- **Redis** — Trie, Skip List, Event Loop, Checkpointing
- **Git** — Copy-on-Write, Merkle Tree, Diff/Patch
- **Chromium** — Dirty Flag, Bloom Filter
- **Rust** — Copy-on-Write, Reference Counting, Interning, Iterator
- **CPython** — Flyweight, Reference Counting, Vtable, Interning
- **其他** — Erlang/OTP, Akka, libuv, Kafka, groupcache, XState, Hystrix, gRPC, Koa, HAProxy, K8s, Nginx, Godot, PyTorch, LLVM, Vue, ZFS, etcd, Node.js

## 案例研究（9 篇）

`docs/case-studies/` 下 ^[extracted]：

- [react-fiber.md](https://totoro-jam.github.io/battle-tested-patterns/case-studies/react-fiber) — 解析 React Fiber 调度器
- [linux-read.md](https://totoro-jam.github.io/battle-tested-patterns/case-studies/linux-read) — Linux read() 系统调用路径
- [go-scheduler.md](https://totoro-jam.github.io/battle-tested-patterns/case-studies/go-scheduler) — Go 调度器与 work stealing
- [git-commit.md](https://totoro-jam.github.io/battle-tested-patterns/case-studies/git-commit) — Git commit 对象的 Merkle tree + COW
- [kafka-log.md](https://totoro-jam.github.io/battle-tested-patterns/case-studies/kafka-log) — Kafka 顺序写盘 + batch
- [leveldb-lsm.md](https://totoro-jam.github.io/battle-tested-patterns/case-studies/leveldb-lsm) — LevelDB 的 LSM + WAL
- [lucene-index.md](https://totoro-jam.github.io/battle-tested-patterns/case-studies/lucene-index) — Lucene 倒排索引
- [nodejs-request.md](https://totoro-jam.github.io/battle-tested-patterns/case-studies/nodejs-request) — Node.js HTTP 请求的事件循环
- [postgres-mvcc.md](https://totoro-jam.github.io/battle-tested-patterns/case-studies/postgres-mvcc) · [redis-single-thread.md](https://totoro-jam.github.io/battle-tested-patterns/case-studies/redis-single-thread) · [sqlite-wal.md](https://totoro-jam.github.io/battle-tested-patterns/case-studies/sqlite-wal) — 三大存储引擎

## 何时用这张表

- **面试前查** — "MVCC 在 PostgreSQL/etcd 是怎么实现的？"
- **Code Review 准备** — "这个 Backpressure 实现对应 Node.js Streams 的哪段？"
- **架构选型** — "我们想要多读少写的存储，LSM 还是 B+ Tree？看 case study。"
- **不要** — 把 46 个模式都学一遍（项目自带的 `learning-paths` 给出分层路径）

## 相关页面

- [[entities/battle-tested-patterns]] — 项目本体、规模、贡献门槛
- [[concepts/programming-pattern-categories]] — 五大分类的思路与 GoF 对照
- [[skills/pattern-study-method]] — 怎样用这个目录系统学习
