---
title: 姚期智 — 图灵奖得主与量子 AI 倡导者
category: entities
tags:
  - person
  - computer-science
  - quantum-computing
  - ai-research
  - academic
summary: Andrew Yao（姚期智），2000 年图灵奖得主（因伪随机数生成与通信复杂度）、清华大学交叉信息研究院院长，2026 年 WAIC 演讲《AI 的第一性原理》提出「AI 边界 + 量子 AI」双论。
sources:
  - "https://www.myzaker.com/article/6a60252f8e9f094b4d106689"
created: "2026-08-13T01:40:00Z"
updated: "2026-08-13T01:40:00Z"
provenance:
  extracted: 0.95
  inferred: 0.04
  ambiguous: 0.01
base_confidence: 0.8
lifecycle: draft
lifecycle_changed: "2026-08-13"
tier: supporting
relationships:
  - target: "[[concepts/ai-research-direction-yao-qizhi]]"
    type: derived_from
  - target: "[[concepts/quantum-computing-foundations]]"
    type: related_to
---

# 姚期智 — 图灵奖得主与量子 AI 倡导者

> Andrew Yao（姚期智），1946 年生，华人唯一图灵奖得主（2000）。理论计算机科学家，伪随机数生成与通信复杂度奠基人。

## 关键贡献

- **Dolev-Yao 攻击者模型**（与 Dolev 合著）：密码学协议分析的标准威胁模型 — 攻击者完全控制网络（可窃听、篡改、注入消息），但无法破解密码原语。这个模型是几乎所有现代协议形式化验证工具（ProVerif、Tamarin）的基础。
- **Yao's Millionaires' Problem**（姚氏百万富翁问题）：两方在不暴露各自财富的前提下比较谁更有钱 — **安全多方计算（MPC）**的开山问题。
- **通信复杂度下界**：Yao 通信复杂度引理，证明 deterministic communication complexity 的 lower bound technique。
- **伪随机数生成**：Yao's XOR lemma 等，理论上证明「弱伪随机」到「强伪随机」的转换。

## 2026 WAIC 演讲核心立场

2026-07-19 WAIC 思想者论坛《AI 的第一性原理：人工智能的威力及其局限》演讲，提出两个核心论断：

1. **AI 有数学/物理边界**：图灵机本质决定 AI 不能解停机问题；选择明文攻击下加密学的可证明安全性；量子密钥分发的物理级安全 — 这些是 AI 不会突破的边界，**反而是 AI 安全的基石**。
2. **量子 AI 是下一个台阶**：AI for Science（已发生）与 Science for AI（未来 5-10 年）两条主轴并行；量子 + 数学 + 物理反过来赋能 AI，会催生量子 AI 新范式。

完整论点见 [[concepts/ai-research-direction-yao-qizhi]]。

## 与中国 AI/量子布局的关系

- **量子科学实验卫星「墨子号」**（2016 发射）：覆盖全国 + 连接海外的量子密钥分发骨干网，长度 >10000 km，服务电子政务 / 跨境金融 / 电网。
- **AlphaQubit 解码器**（Google Willow 论文，~1.5 年前）：量子纠错的解码算法首次用神经网络解决，清华多个团队在跟进。
- 演讲者判断：中国在量子 AI 方向有**先发优势**。

## 对工程师 / 学者的实用建议（演讲节选）

- 写代码的护城河变化：「你的竞争力 =『你 + AI 工具』组成的团队能力」。初级编码工作「未来肯定会消失」，已在 Google / Apple 裁员中显形。
- 核心能力升级：「**抽象问题、创造新概念**」是 AI 短期内做不好的事 — 这是人类研究人员的剩余护城河。
- 对本科生：「**真**」— 不能造假、不逃避、直面问题。物理 / 数学 / 计算机基础打牢，外加艺术修养（音乐 / 名人传记）。

## 相关页面

- [[concepts/ai-research-direction-yao-qizhi]]
- [[concepts/quantum-computing-foundations]]
- [[synthesis/Science for AI × AI for Science]]