---
title: "RPC Drift Hot-Patch — 应对未公开 API 的悄然轮换"
category: concepts
tags:
  - api-stability
  - undocumented-apis
  - resilience
  - mcp
summary: 当供应商在不通知的情况下轮换内部 RPC 方法 ID 时,应该大声检测出这种漂移、允许通过环境变量热修复新 ID,并在被限流时自动重试——而不必强行发一个新版本。
sources:
  - https://github.com/jacob-bd/gemini-notebook-mcp-cli/blob/main/CLAUDE.md
  - https://github.com/jacob-bd/gemini-notebook-mcp-cli/blob/main/docs/KNOWN_ISSUES.md
created: 2026-08-06
updated: 2026-08-06
tier: supporting
lifecycle: reviewed
lifecycle_changed: "2026-08-06"
base_confidence: 0.80
provenance:
  extracted: 0.75
  inferred: 0.20
  ambiguous: 0.05
relationships:
  - target: "[[entities/gemini-notebook-mcp-cli]]"
    type: uses
  - target: "[[references/gemini-notebook-mcp-cli-known-issues]]"
    type: related_to
  - target: "[[concepts/cdp-cookie-extraction]]"
    type: related_to
---

# RPC Drift Hot-Patch — 应对未公开 API 的悄然轮换

> 当你的代码依赖某个供应商内部的 `batchexecute` RPC ID(例如"列出笔记本"对应的 `wXbhsf`),而 Google 在毫无通知的情况下把它轮换掉时,你会同时面对三个问题:要大声检测出这种漂移、要让运维人员能在不发版的情况下修复它、还要在瞬时故障时优雅降级。`NOTEBOOKLM_RPC_OVERRIDES` 就是这个问题的教科书式解法。

## 故障表现

```
NOTICE: NotebookLM (internal API) rotated wXbhsf → aBcD12
        (no announcement, no version bump visible to clients)

SYMPTOM: every notebook_list call returns empty / parsing error
          / silently returns wrong shape
```

如果你的客户端悄悄返回一个空列表,用户会以为"我一个笔记本都没有"——这是一种严重的数据丢失假象。第一要务就是**大声地检测出这种漂移**。

## 检测:`RPCDriftError`

一个设计正确的客户端,会检查响应中是否包含它所请求的那个 RPC ID。如果服务器返回的 `wrb.fr` RPC ID 和请求的**不一致**,客户端就会抛出:

```python
class RPCDriftError(Exception):
    """The server returned different RPC IDs than requested."""
```

这不是一个泛泛的异常,而是一个调用方代码可以捕获并呈现出来的、有类型的错误。而空响应仍然会静默返回(因为没有可比对的点),所以运维人员必须开 `--debug` 才能查出这种情况。

## 发现问题:`--debug` 日志

打开 `--debug` 后,客户端会记录 `RPC IDs in response: [...]`。该调用对应的新 ID 就会出现在这里。这是运维人员察觉到某个 ID 发生了轮换的信号。接下来他们需要一种方式去覆盖它。

## 热修复:`NOTEBOOKLM_RPC_OVERRIDES`

这是一个环境变量,值为一个 JSON 对象,把客户端的 RPC 属性名映射到新 ID:

```bash
export NOTEBOOKLM_RPC_OVERRIDES='{"RPC_LIST_NOTEBOOKS": "aBcD12"}'
```

重启 MCP server(环境变量只在客户端初始化时读取一次,不是每次调用都读)。CLI 会在下一次调用时自动生效。**不需要发版。**

覆盖的格式使用的是 `BaseClient` 的 RPC 属性名(例如 `RPC_LIST_NOTEBOOKS`),而不是旧的 ID 值。这意味着即便新 ID 再次轮换,这个覆盖配置仍然有效——只需要改动映射关系即可。

## 自动重试:限流

`RESOURCE_EXHAUSTED`(RPC 错误码 8)是 Google 对"你调用太频繁了"的响应。客户端会用指数回退自动重试这类错误——运维人员在遇到瞬时限流时不需要做任何操作。

来自 [[references/gemini-notebook-mcp-cli-known-issues]] 的更广泛的限流建议:

> 用 ID 去轮询一个已知的 Studio 产物,而不是反复列出整个笔记本。
> 把操作间隔拉开。
> 遇到 Studio 限流错误后,等待 1-2 分钟再重试。

## 为什么"不发版也能热修复"很重要

对于一个不承诺 API 稳定性的闭源供应商来说,不做热修复的替代方案是:

1. 供应商轮换 ID → 客户端崩了
2. 用户提交 bug 报告
3. 维护者排查、找出新 ID、切一个新版本
4. 用户执行 `uv tool upgrade`
5. 重启 MCP server

这个流程要花上几个小时到几天。而有了热修复:

1. 供应商轮换 ID → `RPCDriftError` 立刻大声报错
2. 运维人员(或社区里的热心人)打开 `--debug`,看到新 ID
3. 运维人员设置环境变量、重启 MCP → 几分钟内修复
4. 维护者从容地提交 issue / PR,把新 ID 落地为永久修复

正是这种"卸掉发版压力"的能力,让集成一个未公开 API 的方案变得可持续。

## 这个模式是什么、不是什么

✅ **是:**
- 一种"错误优先、按类型命名"的设计哲学("大声地、有名字地失败")
- 一个只针对某个配置项的环境变量应急通道
- 面向瞬时限流的自动重试
- 一条 debug 模式下的内省路径

❌ **不是:**
- 一种通用的 API 稳定性抽象方案(这是针对 Google 的特化方案)
- 供应商提供稳定 API 的长期替代品
- 修复响应结构性变化的手段(只能应对 ID 轮换)

## 泛化

这个模式适用于任何依赖未公开/内部 API 的消费者:

1. **给每一次 RPC 调用包一层**能捕获"ID 不匹配"的、有类型的错误
2. **始终在 debug 模式下记录**实际的 ID
3. **让 ID 映射可以通过环境变量、JSON 或本地文件配置**
4. **对瞬时错误(限流、网络问题)自动重试**并做指数回退
5. **把覆盖语法写清楚**,让运维人员可以自行处理

结合 [[concepts/auth-status-semantics]](用于呈现上游认证问题),这为运维未公开 API 集成的人提供了一套完整的生存工具箱。

## 相关

- [[entities/gemini-notebook-mcp-cli]] — 生产环境实现
- [[references/gemini-notebook-mcp-cli-known-issues]] — 更广泛的故障目录
- [[concepts/cdp-cookie-extraction]] — 另一个主要的脆弱面
