---
title: 缓动函数（Easing Functions）
category: concepts
tags: [animation, javascript]
summary: 把线性进度 (0→1) 映射为非线性运动曲线的函数族。传统 Robert Penner 缓动（easeIn/easeOut/easeInOut/elastic/back）来自 2001；Apple 提出参数化运动学函数，学术上有卷积滤波与 PD/PID 反馈控制两条替代路线，各有取舍。
sources:
  - https://www.davepagurek.com/blog/easing-functions/
created: 2026-07-07
updated: 2026-07-07
tier: supporting
lifecycle: draft
lifecycle_changed: "2026-07-07"
base_confidence: 0.50
provenance:
  extracted: 0.85
  inferred: 0.12
  ambiguous: 0.03
---

# 缓动函数（Easing Functions）

## 为什么需要缓动

把一个动画的时间轴归一化到 0→1 的**进度**（progress），再把进度映射到位置——大多数"机械"动画直接用 `lerp(start, end, t)`，结果是匀速的。迪士尼动画师归纳的**12 原则**中，"**slow in, slow out**" 指出静止启动需加速，停止需减速；匀速违反这一物理直觉。

**缓动函数** = 接受线性 progress，返回非线性 progress 的函数，让运动看起来有"性格"。

## 传统 Robert Penner 缓动（2001）

Robert Penner 在 2001 年开源了一套 easing 函数库，主流 p5.js/Three.js/GSAP 等仍以此为基础。

| 类型 | 特性 | 适用 |
|------|------|------|
| `easeInCubic` / `easeOutCubic` / `easeInOutCubic` | 三次方，柔和 | UI 过渡、菜单展开 |
| `easeOutElastic` | 末端振荡衰减 | 通知弹入、强调性入场 |
| `easeInOutBack` | 起手回拉 + 末端微过冲 | 抽屉滑出、模态弹出 |
| `easeOutBounce` | 末端弹跳 | 物理感强的游戏元素 |

### 关键限制

- **选项过少**：写程序时容易在不同场景复用同一个函数，丧失个性
- **time-independent seek 困难**：要"跳到 t=0.7 看一下"，对弹性/反弹类函数要先从头模拟
- **overshoot 的物理直觉**：overshoot 应是"来不及减速"的结果（速度方向不变），但很多函数的 overshoot 是靠"加速"实现的（违反物理）

## 三大 12 原则与缓动的关系

| 原则 | 缓动函数对应 |
|------|--------------|
| **Slow in, slow out** | 所有 easeIn/easeOut 缓动 |
| **Anticipation（预备）** | easeInBack/easeInOutBack（先反方向小幅度） |
| **Follow through（跟入）** | easeOutElastic/easeOutBounce（末端振荡/反弹） |

## 替代方案 1：参数化运动学（Apple）

[Apple 的论文](https://jcgt.org/published/0011/03/02/paper.pdf) 提出单个函数，但**可调参数**：

- 是否包含 anticipation
- overshoot 的振荡次数
- 阻尼

**优点**：覆盖大多数 easing 场景，一个函数搞定。
**缺点**：

- 调参时各参数互相耦合（改振荡次数 → 改 overshoot 幅度 → 需重调加速度）
- 振荡频率与动画时长耦合，参数改完还要重设时长
- 阻尼为 0 时末端曲线有"折角"（视觉跳变）

## 替代方案 2：卷积滤波

[Wang 2006](https://courses.cs.washington.edu/courses/cse464b/18wi/assignments/assignment_1/wang_2006.pdf) 提出用 **Laplacian-of-Gaussian 滤波器** 对原始运动做卷积，自动添加 anticipation + overshoot。

**优点**：可对**任意输入流**（不只 0→1 进度）生效。
**缺点**：

- overshoot 时物体反而**加速**（违反"overshoot 是减速不及"的物理直觉）

## 替代方案 3：反馈控制（PD/PID）

弹簧-阻尼系统用 **PD 控制器**（PD = Proportional + Derivative）让物体跟随目标：

- **P**（比例项）= 当前位置离目标的差距
- **D**（微分项）= 速度
- **I**（积分项）= 累积误差（PID 中的 I，省略以模拟无重力的弹簧+阻尼系统）

```js
// 简化版 PD 控制器示意
acceleration = Kp * (target - position) - Kd * velocity;
velocity += acceleration * dt;
position += velocity * dt;
```

**调参**：

- 阻尼 > 中点 → 平滑 ease-out
- 阻尼 < 中点 → overshoot + 振荡
- 频率 → 移动快慢

**优点**：

- **无需指定时长**：时长是控制器参数的自然结果；目标越远，移动越久，overshoot 越大
- 物理直觉（速度、加速度）直接映射到参数

**缺点**：

- 不自动做 anticipation（需手动把目标先往后拉）
- 需**逐步仿真**，不能 seek 到任意 t 知道位置（除非输入已知，闭式解可用）

## 关键洞见

> "Stock easing functions don't give me enough to work with for procedural animation."

Dave Pagurek（p5.js 贡献者）的判断：

- 传统缓动**够用**于 UI 过渡（响应性 > 个性）
- 对**过程化动画 / 运动图形**，希望参数化、物理化、可控化
- 现有方案各有取舍：参数化（耦合）、卷积（违反物理）、反馈（无 anticipation + 需仿真）
- 未来方向：把"反馈控制对已知输入的响应"做成缓动函数；或拼接两段响应以处理 anticipation + overshoot

## 选择建议

| 场景 | 推荐 |
|------|------|
| Web UI 过渡 / 状态切换 | `easeInOutCubic` / `easeInOutQuad` 足够 |
| 通知 / 模态入场 | `easeOutBack` / `easeOutElastic` |
| 物理感游戏元素 | `easeOutBounce` |
| 复杂程序化动画 | 考虑 PD 控制器 + 闭式解 |
| 实时输入响应 | 反馈控制（仿真） |

## 参考

- [Dave Pagurek: Uneasy about easing functions](https://www.davepagurek.com/blog/easing-functions/)（本文主要来源）
- [Robert Penner easing](https://robertpenner.com/easing/)
- [Apple kinematic easing paper](https://jcgt.org/published/0011/03/02/paper.pdf)
- [Wang 2006 convolution paper](https://courses.cs.washington.edu/courses/cse464b/18wi/assignments/assignment_1/wang_2006.pdf)
- [Disney's 12 principles of animation](https://en.wikipedia.org/wiki/Twelve_basic_principles_of_animation)

## Related

- [[synthesis/concepts-fourier-series × concepts-animation-easing-functions]] — 频域合成的另一条曲线构造路线
- [[synthesis/references-mechanical-watch-mechanics × concepts-animation-easing-functions]] — 反馈控制(PD/PID)的物理实现:摆轮+擒纵
