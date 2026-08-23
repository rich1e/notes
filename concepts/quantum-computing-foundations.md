---
title: "量子计算基础概念"
category: concepts
tags: [quantum-computing, qubit, superposition, entanglement, foundation]
sources: []
summary: 量子计算的基础概念：qubit（叠加态）、entanglement（纠缠）、量子门（gate）、量子线路模型与经典图灵机的本质差异。基础背景信息。
base_confidence: 0.5
provenance:
  extracted: 0.0
  inferred: 0.0
  ambiguous: 0.0
lifecycle: draft
lifecycle_changed: 2026-08-24
tier: supporting
---

# 量子计算基础

## 占位说明

此页面是 **stub**，由 `/wiki-lint --consolidate` cross-linker 阶段自动创建，用于满足 `[[concepts/quantum-computing-foundations]]` 的 4 处引用（来自 [[synthesis/Science for AI × AI for Science]] 和 [[entities/yao-qizhi]] 等页面）。

## 概要

量子计算利用量子力学现象（叠加、纠缠、干涉）进行信息处理：

- **qubit**：2 态叠加系统，可同时表示 |0⟩ 和 |1⟩
- **superposition（叠加）**：n qubits 可同时编码 2^n 个状态
- **entanglement（纠缠）**：多 qubit 联合态无法分解为独立子系统
- **量子门（gate）**：酉变换操作（Pauli-X/Y/Z、Hadamard、CNOT 等）
- **测量**：投影到计算基态，叠加态坍缩

## 相关

- [[entities/yao-qizhi]] — 姚期智，图灵奖得主，量子计算奠基人之一
- [[synthesis/Science for AI × AI for Science]] — 量子计算 × AI 交叉的合成页