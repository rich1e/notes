---
title: "时隔1年零5个月，又一个中国模型震惊全球（哈佛老徐·Reportify）"
category: references
tags: [Deepseek, chinese-ai, geopolitics, semiconductor]
sources:
  - "https://www.douyin.com/video/7664590818786692402"
source_url: "https://www.douyin.com/video/7664590818786692402"
created: 2026-07-23T10:00:00Z
updated: 2026-07-23T10:00:00Z
summary: >-
  哈佛老徐对 Kimi K3 的深度分析（12分钟，2026-07-20）。涵盖官方技术原文、Artificial Analysis 综合排名、Anthropic Fable-5 禁令背景、国产芯片路径图、K3 的四大全球影响。
provenance:
  extracted: 0.80
  inferred: 0.15
  ambiguous: 0.05
base_confidence: 0.68
lifecycle: draft
lifecycle_changed: 2026-07-23
---

# 时隔1年零5个月，又一个中国模型震惊全球（哈佛老徐·Reportify）

**来源：** https://www.douyin.com/video/7664590818786692402  
**创作者：** 哈佛老徐抓AI趋势（徐彬，哈佛统计学硕士，AI找研助手 Reportify 创始人）  
**粉丝：** 58.7 万  
**发布：** 2026-07-20 20:47  
**时长：** 12 分钟（721 秒）  
**互动：** 点赞 3663，评论 219，收藏 1188，分享 654  

> 注：通过帧分析（每40秒一帧，共18帧）提取内容。本视频质量较高，多处直接截图 Kimi 官方原文和 Anthropic 公告。

## 视频四大议题

1. K3 到底有多强？在全球能排第几？
2. 为什么 K3 这么强？
3. 很多人说 K3 会带崩整个半导体行业，真的是这样吗？
4. K3 的发布对全球 AI 产业会带来哪些深远的影响？

---

## 第一部分：K3 有多强？

### Artificial Analysis Intelligence Index 综合排名

截图来源：artificialanalysis.ai（9 项评测综合：GDPVal-AA v2、r²、Banking、Terminal-Bench V2.1、SciCode、Humanity's Last Exam、GPQA Diamond、CritPt、AA-Omniscience、AA-LCR）

| 排名 | 模型 | 分数 |
|---|---|---|
| 1 | Claude Fable-5 | 60 |
| 2 | GPT-5.6 Sol | 59 |
| 3 | **Kimi K3** | **56** |
| 4 | Claude Opus 4.8 (Prev) | 55 |
| 5 | GPT-5.5 (Thinking) | 55 |
| ~6 | Claude Opus 4.7 (Prev) | 54 |

> **K3 综合得分 56，超过 Claude Opus 4.8 的 55.7 分，在全球开权重模型中排名第一**（前两名为闭源模型）。

字幕观点：
- "这种主动承认差距的态度"——对 Moonshot 公开承认不如 Fable-5 的评价为正面
- "这比单独赢下一两个跑分"更有意义——综合排名比单点基准更可信

---

## 第二部分：为什么 K3 这么强？

### Kimi 官方原文（直接截图）

> "Kimi K3 基于 Kimi Delta Attention (KDA) 和 Attention Residuals (AttnRes) 构建，这两项架构更新旨在改进信息在序列长度和模型深度上的流动方式。我们还扩展了专家混合模型 (MoE) 的稀疏性，当与 Stable LatentMoE 框架结合使用时，**能够有效激活 896 位专家中的 16 位**。结合改进的训练和数据处理方法，这些结构性变化使得**整体扩展效率相比 Kimi K2 提升了约 2.5 倍**，从而使模型能够更有效地将计算转化为智能。"

**关键新信息（官方原文）：**
- 架构名称：**KDA（Kimi Delta Attention）** + **AttnRes（Attention Residuals）**
- MoE 框架：**Stable LatentMoE**
- 激活专家：896 个中激活 **16 个**（确认）
- 效率提升：相比 K2 整体扩展效率提升约 **2.5 倍**

### 算力效率公式（博主图解）

```
总算力需求 = 前沿模型的任务量 × 每项任务消耗的基础设施
```

博主观点：K3 的 KDA 技术使"每项任务消耗的基础设施确实下降了"，这是真实技术进步，不是单纯堆算力。

### Kimi 官方原文（发布信息）

> "Kimi K3 现已在 Kimi.com、Kimi Work、Kimi Code 和 Kimi API 上线。发布初期，Kimi K3 将默认采用最大思考强度模式，低强度和高强度模式将在后续更新中推出。我们目前正与推理合作伙伴和开源维护者紧密合作，以协调技术细节，确保在整个生态系统中可靠部署。**完整的模型权重将于 2026 年 7 月 27 日发布**。有关架构、训练和评估的更多详细信息将与 Kimi K3 技术报告一同发布。"

---

## 第三部分：K3 会带崩半导体行业？

### Anthropic Fable-5 禁令（极重要背景）

视频直接截图 Anthropic 官方公告（2026-06-12）：

> **"Statement on the US government directive to suspend access to Fable 5 and Mythos 5"**
>
> "The US government, citing national security authorities, has issued an export control directive to suspend all access to Fable 5 and Mythos 5 by any foreign national, whether inside or outside the United States, including foreign national Anthropic employees. The net effect of this order is that we must abruptly disable Fable 5 and Mythos 5 for all our customers to ensure compliance. **Access to all other Anthropic models will not be affected.**"

**含义：** 2026-06-12 起，美国政府以国家安全为由，强制 Anthropic 对所有外国用户（包括外籍 Anthropic 员工）禁用 Fable 5 和 Mythos 5。其他 Anthropic 模型不受影响。

**博主解读：** K3 的吸引力正在于此——在 Fable-5 被美国政府强制禁止给外国用户使用的背景下，"他们终于多了一个能力足够强"的替代选项。K3 的吸引力不仅来自技术，更来自**不受出口管制的开权重**。

### K3 会带崩半导体？博主结论：不会

`总算力需求 = 任务量 × 单任务基础设施成本`

- K3 降低了单任务成本 ✓
- 但 K3 的发布会**大幅扩大任务总量**——更多用户、更多场景、更低门槛
- 净效果：**总算力需求不会下降，反而可能上升**

---

## 第四部分：K3 对全球 AI 产业的深远影响

### 影响一：模型竞争加剧

> "K3 证明了拥有最多的钱和最多的芯片并不能保证你永远大幅领先。"

### 影响二：K3 对英伟达是短期利好

配套新闻：**OpenAI 与博通合作设计自主 AI 芯片**（将于明年年底开始部署"人工智能加速器"框架），但这属于**长期替代方向**，短期内英伟达仍受益于 K3 带来的算力扩张。

### 影响三：为国产芯片打开全球市场（流程图）

视频展示了一张关键流程图：

```
K3 开放权重 → 低精度格式（4-bit QAT）→ 广泛兼容 → 昇腾/壁仞/摩尔线程 → 前沿推理 → 全球机会
```

> "这就会为国产芯片进入全球市场"

逻辑：K3 以 4-bit 低精度格式开权重，天然适配国产芯片（昇腾 910C、壁仞 BR100、摩尔线程 MTT S80），一旦 K3 被广泛采用，这些芯片随之获得全球曝光机会。

### 最终结论（博主原话）

> "最终的结果应该不是 Kimi 抢走 OpenAI 和 Anthropic 的蛋糕，而是 Kimi 把整块蛋糕做得更大了。"

---

## 关键数据汇总

| 数据点 | 值 | 来源 |
|---|---|---|
| Artificial Analysis 综合分 | **56**（全球第3）| artificialanalysis.ai 截图 |
| K3 vs K2 扩展效率 | **提升约 2.5 倍** | Kimi 官方原文截图 |
| MoE 专家总数/激活数 | 896 / **16** | Kimi 官方原文截图 |
| Fable-5 禁令日期 | 2026-06-12 | Anthropic 官方公告截图 |
| K3 权重发布日 | **2026-07-27** | Kimi 官方原文截图 |

## 局限性

- 视频为分析性内容，非第一手技术披露；部分观点为博主解读
- Anthropic 公告截图是本视频最高价值信息（一手来源，直接截图）
- 国产芯片路径图为博主推论，非 Moonshot 官方声明

## 关联页面

- [[entities/kimi-k3]] — 模型实体页
- [[entities/moonshot-ai]] — 开发商
- [[concepts/kimi-delta-attention]] — KDA 技术详解
- [[concepts/mixture-of-experts]] — Stable LatentMoE
- [[references/kimi-k3-geopolitical-context]] — 地缘政治背景（含 Fable-5 禁令）
- [[synthesis/Research: Kimi K3]] — 综合研究报告
