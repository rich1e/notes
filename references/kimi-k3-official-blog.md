---
title: Kimi K3 Official Launch Blog
category: references
tags: [llm, open-source, chinese-ai, large-scale-model]
sources:
  - "https://www.kimi.com/blog/kimi-k3"
source_url: "https://www.kimi.com/blog/kimi-k3"
created: 2026-07-23T12:00:00Z
updated: 2026-07-23T12:00:00Z
summary: >-
  Kimi K3 官方发布博客全文：2.8T 参数 MoE 架构详情、代码/知识工作/视频编辑能力演示、完整基准表、API 定价和可用性说明。
provenance:
  extracted: 0.95
  inferred: 0.04
  ambiguous: 0.01
base_confidence: 0.95
lifecycle: reviewed
lifecycle_changed: "2026-08-24"
relationships:
  - target: "[[entities/kimi-k3]]"
    type: derived_from
  - target: "[[concepts/kimi-delta-attention]]"
    type: uses
  - target: "[[entities/claude-code]]"
    type: related_to

---

# Kimi K3 Official Launch Blog

**来源：** https://www.kimi.com/blog/kimi-k3  
**发布时间：** 2026 年 7 月 16 日前后（图片 URL 日期戳）

这是 [[entities/moonshot-ai]] 官方发布的 Kimi K3 介绍，是所有技术细节的权威一手来源。

---

## 核心定位

- 2.8T 参数 MoE 模型，全球首个开权重 3T 级模型
- 基于 [[concepts/kimi-delta-attention]] 和 Attention Residuals（AttnRes）构建
- 原生视觉（native vision）能力，100 万 token 上下文
- 整体性能"仍落后于最强闭源模型 Claude Fable 5 和 GPT 5.6 Sol"（官方原话）
- 权重于 **2026 年 7 月 27 日**发布

---

## 架构细节

### 核心组件

Kimi K3 基于两个主要架构创新叠加：

**1. Kimi Delta Attention（KDA）**
- 提供高效的长序列扩展 Attention 基础
- 解决信息如何跨序列长度流动的问题
- 配合 prefill 缓存，使 K3 可以以有竞争力的 token 价格提供服务

**2. Attention Residuals（AttnRes）**
- 跨模型深度有选择地提取表示
- 与 KDA 构成 K3 的架构主干

### Stable LatentMoE 框架

MoE 实现的精细组件，解决 896 专家级别的路由与优化挑战：

| 组件 | 作用 |
|---|---|
| **Quantile Balancing** | 从路由器分数分位数直接推导专家分配，消除启发式更新和敏感的均衡超参数 |
| **Per-Head Muon** | 将 Muon 优化器扩展至按 Attention Head 独立优化，实现更自适应的大规模学习 |
| **SiTU（Sigmoid Tanh Unit）** | 改进激活控制 |
| **Gated MLA** | 改进 Attention 选择性 |

这些组件联合实现在 2.8T 参数规模下的稳定高效训练。

### 训练量化

- 从 SFT 阶段起应用量化感知训练（QAT）
- MXFP4 权重 + MXFP8 激活
- 目标：广泛硬件兼容性

### 扩展效率

相比 Kimi K2，K3 整体扩展效率提升约 **2.5×**——同等算力可转化为更多"智能"。

---

## 代码能力

### 内核优化基准测试

在内核优化测试中，每个模型在相同沙箱内独立工作最多 24 小时，优化 4 个任务（AttnRes、KDA 和 512 头维度 MLA 内核），跨 NVIDIA H200 和一款替代供应商 GPGPU：

- Kimi K3 与 Fable 5（含 fallback）竞争力相当
- 大幅优于 Opus 4.8、GPT 5.6 Sol、GPT 5.5
- **背景**：K3 开发后期，K3 早期版本处理了团队大多数内核优化工作

### GPU 编译器开发（MiniTriton）

Kimi K3 从零构建了一个 GPU 编程系统 **MiniTriton**：

- 类 Triton 编译器，含自研 tile 级 IR 层（基于 MLIR）
- 优化 passes + PTX 代码生成管道
- 在 roofline 基准测试上性能与 Triton 和 `torch.compile` 持平甚至超越
- 在 nanoGPT 端到端训练中稳定收敛（loss 曲线紧跟参考，仅轻微偏差）
- 自研 Tensor Core 路径已与 Triton 深度优化栈媲美

> 这是一个连贯的端到端编译器（DSL 前端 → IR → PTX 代码生成 → 运行时），而非孤立的内核。

### 芯片设计

K3 在 **单次 48 小时自主运行**中设计了一个纳模型加速芯片（Nangate 45nm 库）：

| 指标 | 值 |
|---|---|
| 面积 | < 4 mm² |
| 时序收敛 | 100 MHz |
| 解码吞吐量 | > 8,700 tokens/s（仿真）|
| 标准单元 | 1.46M |
| SRAM | 0.277 MB |
| 计算单元 | INT4 MAC 阵列，含融合反量化 |

- 使用开源 EDA 工具
- "由模型构建、为模型服务"——体现 K3 的长程 Agent 能力

### 科研代码化

K3 将科学文献转化为可执行代码的能力：

**I-Love-Q 普适关系（计算天体物理）**：
- ~2 小时完成通常需要 1-2 周的工作
- 交叉验证 20+ 篇论文
- 实现完整数值计算管道
- 评估 300+ 状态方程
- 识别发表公式中的不一致之处
- 生成 3,000+ 行 Python 代码
- 输出交互式 HTML 仪表板

### 3D 推理与游戏开发

Kimi K3 结合 3D 推理、代码和视觉能力，将概念、图像和视频转化为可玩的交互体验。实现"视觉在回路"（vision in the loop）——在代码和实时截图之间无缝迭代。

---

## 知识工作能力

### 内部 Agent 知识工作评测

K3（max）在 Moonshot 内部知识工作评测中展示了一致提升，该评测来源于真实用户-Agent 工作流中反复出现的挑战。

### 代表性案例

**案例 1：42 年 AI ASIC 行业研究（120+ 轮迭代）**
- 通过 2,800+ 次网络搜索/抓取完成数据收集
- 1,100+ 次终端数据拉取
- 分析 87 份季报、99 份 PDF 原文（合计 11,000+ 页）
- 产出：交互式研究报告，含自定义图表、动态图解、交互式可视化叙事

**案例 2：核聚变行业研究**
- 咨询风格行业报告
- 含时间线、漏斗图、范围条形图、甘特图
- 出版质量幻灯片

**案例 3：GWTC-5 引力波分析**
- 使用 20+ 个并发子 Agent 分析 391 个引力波事件
- 产出：7 个科学可视化、2 个数据表、10+ 篇文献综合

### Widgets 与 Dashboard

Kimi Work 新功能：
- **Widgets**：在对话中直接生成交互组件，可连接本地数据或外部插件持续更新
- **Dashboard**：围绕主题/项目/目标整合 widgets 的持久化个人视图

---

## 视频编辑能力

Kimi K3 的原生多模态架构（同一模型内理解文本、图像和视频）使其在动态设计、动画和视频编辑方面表现优异：

**案例 1：运动图形教学视频**
- 创作 3Blue1Brown 风格的架构动效说明
- 将技术思路转化为动画图表和转场

**案例 2：预告片剪辑**
- 从 56 个源素材片段剪辑 K3 宣传视频
- 处理：素材选择、运动匹配剪切、帧精确节拍同步、音频处理
- 经多轮修改
- 等效工作量：熟练剪辑师 1-2 个工作日 / 初学者 3-5 天

---

## 完整基准说明

所有 K3 结果均在 reasoning effort = max、temperature = 1.0、top-p = 1.0 下获得。

### 测试 Harness 选择

| 模型 | 主要 Harness |
|---|---|
| Kimi K3 | KimiCode（多数编程测试）/ Claude Code（部分）|
| Claude Opus 4.8 / Fable 5 | Claude Code / Terminus 2 |
| GPT 5.5 / 5.6 Sol | Codex |
| GLM-5.2 | Claude Code |

### 关键测试注意事项

1. **DeepSWE v1.1**：K3 使用 KimiCode；GLM-5.2 分数来自其发布博客；其余来自官方 DeepSWE 排行榜
2. **SWE Marathon**：K3 和 Claude 模型使用 Claude Code harness，评估基于 H20 校准分支；**Claude Fable 5 在 35% 任务中触发 fallback**
3. **FrontierSWE**：K3 使用 KimiCode；GPT-5.6 Sol 使用 Codex；其余来自 frontierswe.com（截至 2026-07-16）
4. **PostTrainBench**：K3 和 Fable 5 使用 Claude Code harness；3 次平均（H20 GPU）
5. **GAIA v2**：采用 [[entities/claude-code.md|claude-code]] 压缩策略（300K token 触发），K3 在 1M 无压缩时得分 **90.4**

### 多模态测试

- ZeroBench：运行 5 次（其余运行 3 次）
- MMMU-Pro：遵循官方协议，图像前置于文本

---

## 可用性

| 渠道 | 说明 |
|---|---|
| Kimi.com / App | iOS、Android、HarmonyOS |
| Kimi Work | 桌面应用 v3.1.0+（Windows + Apple silicon Mac）|
| Kimi Code | 终端 CLI，`/model` 命令选择 K3 |
| Kimi API | `kimi-k3`，定价见下表 |
| 开权重 | **2026-07-27 发布** |

### API 定价

| 类型 | 单价 |
|---|---|
| 缓存命中输入 | $0.30 / MTok |
| 缓存未命中输入 | $3.00 / MTok |
| 输出 | $15.00 / MTok |

**缓存效率**：Mooncake 解耦推理架构驱动，编程工作负载缓存命中率 **>90%**，实际平均输入成本极低。

发布时仅支持最大推理模式，低/高强度模式待后续更新。

---

## 已知限制（官方披露）

1. **思维历史传递**：K3 以保留思维历史模式训练。若 Agent harness 未按要求传回所有历史思维内容，或中途将另一模型的会话切换至 K3，生成质量可能高度不稳定。**推荐使用 Kimi Code 等已验证兼容的 harness，避免会话中途切换至 K3**。
2. **自主决策倾向**：训练重点为长程复杂任务。遇到小问题或意图模糊时，可能替用户做出非预期决策。若需严格边界约束，在系统提示或 `AGENTS.md` 中加入更明确的行为限制。
3. **用户体验差距**：整体用户体验与 Claude Fable 5 和 GPT 5.6 Sol 相比仍有明显差距。

---

## 相关页面

- [[entities/kimi-k3]] — 模型实体与技术规格
- [[entities/moonshot-ai]] — 开发商
- [[concepts/kimi-delta-attention]] — 核心 Attention 创新
- [[concepts/mixture-of-experts]] — MoE 架构基础
- [[synthesis/Research: Kimi K3]] — 综合研究报告
- [[references/kimi-k3-technical-overview]] — AI News 技术报道（第三方）
- [[references/kimi-k3-geopolitical-context]] — 地缘政治背景分析
