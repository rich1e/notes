---
title: Kimi K3
category: entities
tags: [llm, open-source, chinese-ai, large-scale-model]
sources:
  - "https://artificialintelligence-news.com/2025/07/kimi-k3-3-trillion-parameters/"
  - "https://the-decoder.com/kimi-k3-first-open-model-with-3-trillion-parameters/"
  - "https://huggingface.co/moonshotai/Kimi-K3"
  - "https://www.kimi.com/"
  - "https://www.kimi.com/blog/kimi-k3"
  - "https://www.youtube.com/watch?v=8_JZehVSRAI"
  - "https://www.douyin.com/video/7664590818786692402"
created: 2026-07-23T08:00:00Z
updated: 2026-07-23T12:00:00Z
summary: >-
  Moonshot AI 发布的全球首个 3T 级开权重 LLM（2.8T 参数，MoE 896 专家）。专为 Agent 编程与知识工作设计，代码评测领先，整体能力接近 Fable 5 但略弱。
lifecycle: draft
lifecycle_changed: 2026-07-23
---

# Kimi K3

## 概览

[[entities/moonshot-ai]]（月之暗面）开发的大型语言模型，于 **2026 年 7 月 27 日**发布开权重。自称"全球首个 3T 级开权重模型"，专为"长程代码、知识工作和推理"设计，口号是"专为智能体编程与知识工作打造"。

## 技术规格

| 参数 | 值 |
|---|---|
| 总参数量 | **~2.8 万亿（2.8T）** |
| 架构 | [[concepts/mixture-of-experts]]（MoE）|
| 专家数 | 896 |
| 每 token 激活专家数 | **16**（稀疏率 ~1.8%）|
| 上下文窗口 | **100 万 token** |
| 推理精度 | 4-bit 量化感知训练（QAT）|
| 权重体积 | ~1.4TB（4-bit）vs ~5.6TB（FP16）|

## 核心技术创新

### Kimi Delta Attention（KDA）
专为长上下文推理设计的 Attention 变体，改进信息在序列长度和模型深度上的流动方式，解决 KV 缓存随上下文增长的内存爆炸问题。
- 声明：100 万 token 上下文下解码速度最高提升 **6.3×**
- 详见：[[concepts/kimi-delta-attention]]

### Attention Residuals（AttnRes）
训练效率优化技术，与 KDA 配合改进信息在模型深度上的流动。
- 声明：以 **<2% 额外成本**提升 **~25% 训练效率**

### Stable LatentMoE
K3 采用的 MoE 框架，与 KDA + AttnRes 结合实现高效专家稀疏激活。
- 有效激活 896 个专家中的 **16 个**
- 整体扩展效率相比 Kimi K2 **提升约 2.5 倍**（官方原文）
- 精细组件：**Quantile Balancing**（路由器分数分位数推导专家分配，消除启发式均衡超参数）、**Per-Head Muon**（按 Attention Head 独立优化）、**SiTU**（激活控制）、**Gated MLA**（Attention 选择性）

### 量化感知训练（QAT）
从微调阶段起采用 4-bit 精度训练（标准为 16-bit），目标是"广泛硬件兼容性"——业界普遍解读为对非 Nvidia 硅片的主动规避。

## 基准测试

| 评测 | 结果 | 备注 |
|---|---|---|
| Chatbot Arena Frontend Code | **1,679 分，排名第一** | 盲测，领先 Claude Fable 5 |
| 整体能力（vs Fable 5/GPT 5.6 Sol）| **落后** | Moonshot 官方承认 |
| SWE Marathon | K3 领先 | ⚠️ Fable 5 有 35% fallback，可能影响对比有效性 |
| DeepSWE v1.1 排行榜 | GPT-5.6-Sol 72% > Claude-Fable-5 68% > GPT-5.5 61% | K3 未进入该榜前列（视频来源）^[extracted] |
| LiveBench 性价比 | 每成功任务成本 **$0.379**，处于中游 | 高于 GPT-5.6-Sol 高效模式（$0.355）^[extracted] |
| Artificial Analysis 综合分 | **56 分，全球第 3**（Fable-5 60，GPT-5.6 Sol 59）| 9 项评测综合，开权重模型第一^[extracted] |

> **重要提示**：权重发布前，所有基准为 Moonshot 第一方声明，尚待独立复现。

## 硬件部署

- **推荐配置：** 64 个以上加速器作为单一内存池
- **已测试平台：** Nvidia H200S、Nvidia L20（出口合规型号）、某"未披露供应商的通用计算 GPU"
- **架构参考：** 与华为 CloudMatrix 内存池化方案兼容
- **部署门槛：** 1.4TB 权重下限 + 长上下文 KV 缓存开销 → 数据中心级承诺，非服务器室部署

## API 定价

| 类型 | 单价 |
|---|---|
| 输入（标准）| $3 / 百万 token |
| 输入（缓存命中）| $0.30 / 百万 token |
| 输出 | $15 / 百万 token |

**定价背景：** 低于 Claude Fable 5（$50/M 输出）；远高于 DeepSeek V4（$0.87/M）和 GLM-5.2（$4.40/M）。K3 标志着 Moonshot 从廉价层主动转向中高端定价。

**注意：** 发布时仅支持最大推理深度模式，低强度模式待后续更新。

## 能力定位

- 设计重点：**Agent 工作流、长程代码理解、知识工作**
- 原生多模态：同一模型内理解文本、图像和视频（官方博客确认）
- 工具调用、浏览、多步规划等 Agent 能力为内置功能

### 代码能力亮点（官方博客案例）

| 任务 | 成果 |
|---|---|
| **GPU 内核优化** | 24 小时内跨 H200 和替代 GPU 优化 4 个内核（KDA/AttnRes/512-head MLA）；与 Fable 5 竞争力相当 |
| **MiniTriton 编译器** | 从零构建类 Triton GPU 编译器，含 MLIR tile IR + PTX 代码生成；部分 roofline 基准超越 Triton |
| **芯片设计** | 48 小时自主运行，Nangate 45nm，< 4mm²，100 MHz，> 8,700 tokens/s，含 INT4 MAC 阵列 |
| **科研代码化** | I-Love-Q 天体物理问题：~2 小时 vs 通常 1-2 周，3,000+ 行 Python + 交互式 HTML 仪表板 |
| **游戏/CAD 开发** | "视觉在回路"：代码与实时截图无缝迭代，用于 3D 游戏开发和 CAD |

### 知识工作能力亮点

| 任务 | 规模 |
|---|---|
| **ASIC 行业报告** | 2,800+ 次搜索，87 份季报，99 份 PDF，11,000+ 页，120+ 轮迭代 |
| **引力波分析** | 20+ 并发子 Agent，391 个事件，7 个科学可视化 |
| **视频编辑** | 从 56 个源素材剪辑宣传视频，帧精确节拍同步 |

### 已知限制（官方披露）
1. 若 Agent harness 未完整传回历史思维链内容，生成质量高度不稳定；推荐 Kimi Code harness，避免会话中途切换
2. 用户意图模糊时可能采取非预期的自主行动；需在系统提示或 `AGENTS.md` 中加入明确约束
3. 整体用户体验与 Fable 5/GPT 5.6 Sol 仍有明显差距

## 实测能力演示（零度解说视频）

来源：YouTube 零度解说（2026-07-20，11.5 万次播放）

### Kimi Agent 内置工具
Kimi 官网界面展示多种模态入口：集群 / PPT 生成 / 深度研究 / 网站创建 / 文档处理 / 表格分析。^[extracted]

Kimi Agent 内置了可运行的虚拟机环境：
- **windows-xp.kimi.site**：浏览器内运行 Windows XP 模拟器，可运行红色警戒 2、QQ 农场等经典软件^[extracted]
- **macos27.kimi.page**：浏览器内运行 macOS 模拟器，FaceTime 等系统应用可正常使用^[extracted]

### 代码生成能力
视频对比了 Kimi K3 和 Claude Fable-5 的代码生成（虽帧画面中展示的主要是 Claude Code）：
- Claude Code 可在 K3 API 下完成 Three.js FPS 射击游戏（5 阶段规划，13 文件，约 2600 行代码，含 AK-47 武器系统、后坐力动画、粒子特效）^[extracted]
- K3 可生成交互式 3D 场景：骑马探索开放世界、四冲程发动机可视化演示、应县木塔数字展览（10,611 件构件）^[extracted]

### 成本对比
仿 Apple 官网代码生成任务：K3 vs Claude 的 API 成本对比，视频字幕"Claude 花了 0.94 美金"，暗示 K3 成本更低^[extracted]

### 越狱情况
视频标题明确提及"模型已被越狱"，描述链接指向 freedidi.com 上的越狱教程（2026-07-20 上线）。表明 K3 的安全对齐在发布时存在薄弱点^[extracted]

## 开源状态

- **类型：** 开权重（Open-weight），而非完全开源
- **License：** 发布时未详细披露
- **发布平台：** Hugging Face（`moonshotai/Kimi-K3`）
- **生态贡献：** Moonshot 向 vLLM 贡献了推理缓存代码；Delta Attention 等特性在发布时标准工具暂不支持

## 市场影响

- Bank of America 分析师：K3 证明"大规模预训练 + 架构创新在算力限制下仍能产生阶跃式提升"
- 开权重模型（K3 所属类别）2026 年 6 月在 Vercel 生产网关占 **29% token 流量**，却仅占 **<4% 支出**
- K3 被视为继 DeepSeek 之后，迫使西方 AI 实验室重新审视"算力护城河"假设的第二个里程碑

## 相关页面

- [[entities/moonshot-ai]] — 开发商
- [[concepts/mixture-of-experts]] — 核心架构模式
- [[concepts/kimi-delta-attention]] — 推理优化技术
- [[concepts/llm-speculative-decoding]] — 相关推理加速技术
- [[concepts/prompt-caching]] — 相关 KV 缓存复用技术
- [[synthesis/Research: Kimi K3]] — 综合研究报告

- [[synthesis/concepts-mixture-of-experts × entities-kimi-k3]] — synthesis
- [[synthesis/concepts-kimi-delta-attention × entities-kimi-k3]] — synthesis
