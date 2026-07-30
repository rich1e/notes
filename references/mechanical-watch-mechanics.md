---
title: 机械表运作原理速查
category: references
tags: [personal, book]
sources:
  - "https://ciechanow.ski/mechanical-watch/"
created: 2026-07-02
updated: 2026-07-02
summary: 机械表七大核心部件：主发条→发条盒→轮系→擒纵机构→摆轮→拨针轮→表盘，能量流动路径与各部件作用。
base_confidence: 0.83
lifecycle: draft
lifecycle_changed: "2026-07-02"
tier: peripheral
provenance:
  extracted: 0.90
  inferred: 0.08
  ambiguous: 0.02
---

# 机械表运作原理

Bartosz Ciechanowski 交互文章 [Mechanical Watch](https://ciechanow.ski/mechanical-watch/) 的知识提炼。

## 七大核心部件（能量链）

```
主发条 → 发条盒 → 轮系（齿轮组）→ 擒纵机构 → 摆轮（调速器）
                                              ↓
                                    拨针轮 → 表盘（显示）
```

## 各部件作用

### 主发条（Mainspring）
- 螺旋扭力弹簧，上弦时储存弹性势能
- 装入**发条盒**（barrel）后被约束，靠摩擦力固定
- 发条盒旋转输出能量；轴固定，盒旋转

### 擒纵机构（Escapement）
- 核心作用：**受控释放**能量，而非直接传输
- 组成：擒纵轮（escape wheel）+ 擒纵叉（pallet fork）
- 工作方式：摆轮每摆动一次，擒纵叉释放一个齿，让轮系前进固定步长

### 摆轮（Balance Wheel）
- 钟表的"心脏"，决定走时精度
- 游丝（hairspring）提供恢复力，使摆轮以固定频率振荡
- 摆轮频率（Hz）= 每秒摆动次数，典型值 3–8 Hz（21600–57600 bph）

### 轮系（Gear Train）
- 将发条盒的慢速大力矩变速为秒针所需的高速小力矩
- 典型齿轮比使秒针每 60 秒转一圈

## 上弦机制

- 手动上弦：旋转表冠 → 通过棘轮单向传递到主发条轴 → 收紧发条
- 自动上弦：摆陀（rotor）随手腕运动旋转 → 通过单向齿轮为发条上弦

## 精度影响因素

- 摆轮游丝的温度膨胀系数
- 姿态（竖放/平放影响摆轮受到的重力）
- 润滑油老化
- 磁场干扰
## 相关页面

- [[journal/fire-emblem-new-mystery-prologue.md]]

## Related

- [[synthesis/references-mechanical-watch-mechanics × concepts-animation-easing-functions]] — 摆轮+擒纵=PD 反馈控制器的物理实现
