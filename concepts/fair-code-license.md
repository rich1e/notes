---
title: "Fair-code License（受限源码可用许可）"
category: concepts
tags: [licensing, open-source, fair-code, sustainable-use, n8n]
sources:
  - "https://github.com/n8n-io/n8n"
  - "https://n8n.io/blog/fair-code/"
  - "https://docs.n8n.io/reference/license/"
created: "2026-07-30"
updated: "2026-07-30"
summary: "介于「完全开源」与「完全专有」之间的「源码可见 + 受限商用」许可，代表：n8n 的 Sustainable Use License。可自托管、可改、不可转售同类竞品。"
provenance:
  extracted: 0.60
  inferred: 0.30
  ambiguous: 0.10
base_confidence: 0.65
lifecycle: draft
lifecycle_changed: "2026-07-30"
tier: supporting
---

# Fair-code License（受限源码可用许可）

## 概念

**Fair-code** 是 n8n 创始人 Jan Oberhauser 提出的「介于 OSI 开源与完全专有之间」的许可证定位。代表实现是 n8n 的 **Sustainable Use License**。

核心定位：

> 能用、能改、能自托管——但**不能**用同一份源码做出**同质化竞品**转售。

## 与常见许可证的关系

| 许可证 | 类型 | 可自托管 | 可改 | 可转售/提供 SaaS |
|---|---|---|---|---|
| MIT / Apache-2.0 | OSI 开源 | ✅ | ✅ | ✅ 任意形式 |
| AGPL | OSI 开源（强 copyleft） | ✅ | ✅ | ⚠️ 必须开源你的改动 |
| **Sustainable Use License** (n8n) | **fair-code / source-available** | ✅ | ✅ | ⚠️ 限「非竞争性」 |
| BSL / Business Source License | source-available（time-delayed） | ✅ | ✅ | ⚠️ 限时后转 OSD 开源 |
| 专有许可证 | 私有 | ❌ | ❌ | ❌ |

**关键边界**：Sustainable Use License **不是** OSI 开源——它**禁止**用本软件构建**竞争性商业产品**。常见允许：内部使用、自托管、构建工作流出售、咨询业务、提供 SaaS 但不直接卖 n8n 副本。

## 实务含义 ^[inferred]

- **不能用 n8n 源码**做「白标版 n8n SaaS」与 n8n Cloud 竞争
- **可以在公司内部**用、修改、出售**基于 n8n 的工作流服务**（咨询/集成）
- 完整条款以 [LICENSE.md in n8n repo](https://github.com/n8n-io/n8n/blob/master/LICENSE.md) 为准（本研究 Round 1/2 多次尝试 fetch 文档站 /reference/license/ 路径返回 404；本结论基于 GitHub README 声明 + 创始人 blog + 社区共识，非官方逐条解析）

## 选用时的判断

- **接受 fair-code**：自托管、内部工具、咨询服务、基于工作流的解决方案
- **必须 OSD 开源**：找替代品（如 Apache 2.0 的 Apache Airflow、MPL 2.0 的 Huginn 等）

## 限制与争议

- 边界判断依赖具体条款细节；遇到法务边缘场景需查完整 LICENSE 文本
- 生态工具链可能按 OSI 开源假设打包，构建多依赖项目时需注意传染性
- "fair-code" 这个词本身是 n8n 自创/推广的，不是行业标准术语

## 相关

- [[entities/n8n]]
- [[sources/n8n-github-repo]]
- [[synthesis/Research: n8n]]