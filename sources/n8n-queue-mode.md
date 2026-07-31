---
title: "n8n Queue Mode 生产架构与扩展"
category: sources
tags: [n8n, system-architecture, devops, scaling, queue, redis, postgres]
sources:
  - "https://docs.n8n.io/hosting/scaling/queue-mode/"
  - "https://github.com/n8n-io/n8n-hosting"
  - "https://github.com/n8n-io/n8n-kubernetes"
source_url: "https://docs.n8n.io/hosting/scaling/queue-mode/"
created: "2026-07-30"
updated: "2026-07-30"
summary: "n8n 生产部署官方扩展方案：main + webhook + worker 三角色解耦，Redis BullMQ 任务队列，Postgres 元数据，6 类常见可靠性陷阱。"
provenance:
  extracted: 0.75
  inferred: 0.20
  ambiguous: 0.05
base_confidence: 0.83
lifecycle: draft
lifecycle_changed: "2026-07-30"
---

# n8n Queue Mode 生产架构

> 一手来源：[docs.n8n.io/hosting/scaling/queue-mode](https://docs.n8n.io/hosting/scaling/queue-mode/)（官方文档）+ [github.com/n8n-io/n8n-hosting](https://github.com/n8n-io/n8n-hosting)（参考 docker-compose）

## 三角色解耦

n8n 在 queue 模式下拆成 3 个独立角色，每个独立容器/进程：

| 角色 | 职责 |
|---|---|
| `main` | 用户 UI + API；接收请求、入队作业，**永不执行** workflow |
| `webhook` | 专门的 HTTP 入口，承担外部 webhook 流量 |
| `worker` | 无状态进程池，从 Redis 拉作业并执行 |

关键环境变量：`EXECUTIONS_MODE=queue`、`QUEUE_BULL_REDIS_HOST/PORT/DB`、`EXECUTIONS_DATA_PRUNE=true`。

## 组件拓扑

```
User/UI ────────► n8n main (UI + API + RBAC)
                       │ enqueue (BullMQ)
                       ▼
              Redis (任务持久化 + pub/sub + leader election)
                       │ dequeue
                       ▼
External webhooks ──► webhook processor(s)
                            │ enqueue
                            ▼
                  n8n worker(s)（横向扩缩）
                            ▼
                  Postgres（执行历史、凭据、workflow 定义）
```

## Redis 是中枢神经

- 任务 + 任务状态都存 Redis（BullMQ 数据结构）
- `main` 入队；`workers` 出队
- Redis 还做 pub/sub，包括 worker 心跳 → UI 显示在线状态
- 因此 Redis **必须**作为数据库一样对待：AOF 或托管 Redis 持久化；`noeviction` 防静默任务丢失；监控 `used_memory`、复制延迟、驱逐策略

## 生产清单

- [ ] `EXECUTIONS_MODE=queue` 已设置；`EXECUTIONS_DATA_PRUNE=true`
- [ ] Redis 持久化、`noeviction`、内存监控、备份策略
- [ ] webhook ≥ 2 副本，负载均衡 + 健康检查
- [ ] worker 用无状态池部署，HPA 横向扩缩
- [ ] Postgres 自动化备份 + PITR + 执行历史剪裁
- [ ] webhook URL 独立域名、独立 TLS、独立速率限制
- [ ] 集中日志 + 指标：Redis 队列深度、worker 执行时长、Postgres 滞后
- [ ] 上线前压测（`n8n` 博客有基线方法论）

## 6 类常见可靠性陷阱

1. **Redis 重启丢任务** —— 无 AOF/RDB 快照时崩溃即丢作业。开启持久化或用托管 HA Redis
2. **webhook 单点故障** —— 单实例 = 单点瓶颈 + 无 failover。至少 2 副本
3. **执行历史导致 DB 膨胀** —— 长期运行产生数百万行，拖慢 Postgres 与 UI。配置 `EXECUTIONS_DATA_PRUNE` 与 `EXECUTIONS_DATA_MAX_AGE`
4. **Leader election 冲突** —— 部分特性仍需单 leader；多 `main` 实例可能争抢，谨慎
5. **Worker 资源限** —— CPU-bound 节点会饿死其他执行。设 container CPU/memory 限制，让 HPA 加副本而非单点超大
6. **Queue 名硬编码** —— 多 n8n 实例共享同一 Redis 不做 namespace 时会冲突。用专用 DB index 或环境前缀

## 相关

- [[entities/n8n]]
- [[concepts/workflow-automation-platform]]
- [[synthesis/Research: n8n]]