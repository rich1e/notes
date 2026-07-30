---
title: "傅里叶级数 × 缓动函数"
category: synthesis
tags: [mathematics, signal-processing, animation, javascript, design-patterns]
sources:
  - "[[concepts/fourier-series]]"
  - "[[concepts/animation-easing-functions]]"
created: 2026-07-30
updated: 2026-07-30
summary: "频域合成(傅里叶/本轮链)与时域参数化(缓动函数)是构造复杂波形的两条正交路线,前者调"哪些频率存在",后者调"时间如何插值"——维度不同但目标同构。"
provenance:
  extracted: 0.20
  inferred: 0.70
  ambiguous: 0.10
base_confidence: 0.65
lifecycle: draft
lifecycle_changed: 2026-07-30
relationships:
  - target: "[[concepts/fourier-series]]"
    type: related_to
  - target: "[[concepts/animation-easing-functions]]"
    type: related_to
---

# 傅里叶级数 × 缓动函数

## The Connection

两条看似无关的曲线构造路径实际上正交地分解了"任意波形"这一目标。**傅里叶/本轮链** 在频域空间工作:把目标函数分解为若干旋转圆(频率成分),每圆半径=振幅,转速=角频率,初角=相位。**缓动函数** 在时域空间工作:把 0→1 的归一化进度映射为非线性时间曲线,通过参数化或反馈控制实现 ease、elastic、bounce 等效果。

读 [[concepts/fourier-series]] 的页时人会想"任意曲线都能用圆链拼",读 [[concepts/animation-easing-functions]] 时人会想"任意时序都能用缓动函数控制"——但两页各自只说了一半。**合起来的洞察是:频域和时域的曲线构造是同一道菜的两刀切法,选哪一刀取决于你控制的是"哪些频率要存在"还是"时间如何插值"**。

## Where They Co-occur

- **音频合成** — 傅里叶分析反推滤波器响应,缓动函数不直接出场(音频波形本身是物理振动的结果,不需插值)
- **UI 动画** — 缓动函数主战场;傅里叶极少出场,但 circular motion 类动效用"本轮链"实现会很自然
- **信号处理** — 频域(傅里叶)主场,时域缓动只在窗函数/采样时机层面以参数化形式出现
- **数据可视化** — 两条路都出现:折线图轴变换用傅里叶(去噪/特征提取),动画过渡用缓动(时间插值)

## Cross-cutting Insight

**控制维度的正交性是这两者的核心。**

| | 傅里叶/本轮链 | 缓动函数 |
|---|---|---|
| 域 | 频域(频率轴) | 时域(时间轴) |
| 控制量 | 振幅/角频率/相位 | ease 参数/Penner 类型 |
| 表达对象 | 周期或类周期函数 | 单调或限定的 0→1 进度 |
| 工程入口 | FFT、谐波叠加 | CSS `cubic-bezier`、Penner 公式 |
| 适合形态 | 振铃、混合、特征明显的曲线 | UI 过渡、用户操作反馈 |

**为什么看似不同**:缓动函数默认输入单调(0→1),且关心"加速度突变"对用户体验的影响;傅里叶默认输入周期,且关心"哪些频率有"对信号特征的贡献。前者优化主观感受,后者优化数学分解。

**真正的合流点**:`[concepts/animation-easing-functions]` 的 **PD/PID 反馈控制** 路线在数学上等价于傅里叶级数中"低频本轮占主导"的情况——摆轮/擒纵机构的 [[references/mechanical-watch-mechanics]] 物理实现就是这一点的工程印证(见 `concepts-mechanical-watch-mechanics × concepts-animation-easing-functions`)。

## Tensions and Trade-offs

- **性能**:傅里叶的 IFFT/FFT 在 N>1024 时 O(N log N),缓动函数每个关键帧 O(1) — 频域合成贵得多
- **直觉**:缓动函数对设计师友好(可视化试错),傅里叶对工程师/数学家友好(可推理)
- **数据假设**:傅里叶假设周期性,缓动函数假设单调性——两者都依赖前提假设
- **参数化粒度**:傅里叶粒度=谐波数,缓动函数粒度=Penner 类型/贝塞尔控制点;粒度增加都增加自由度但增加调参成本

## Strongest Objection

> "你把它们并提是 category error:傅里叶是分析工具(把已有信号拆解),缓动函数是构造工具(凭空设计一条曲线)。一个 reduce、一个 generate,方向相反。"

**反驳路径**:在 [[concepts/fourier-series]] 的"应用方向"段,作者明确把傅里叶级数当**合成**工具("任意周期函数都可用一组旋转圆链机械图像合成")——构造。缓动函数虽然有 reduce(从运动轨迹反推缓动类型),但日常用法也是构造。所以两者**在工程用法上**都是构造工具,只是构造空间不同。

**可检验查询**:`> test: 能否用傅里叶合成一个 cubic-bezier(0.4, 0, 0.2, 1) 形状的缓动曲线?如果能精确合成到 N 谐波,这对"维度正交"是更强证据;如果不能,说明时域缓动有傅里叶难以表达的成分(如单调约束)。`

## Open Questions

- **频域缓动** 是不是有意义?——傅里叶合成出一条不单调的曲线,在 UI 动画里几乎不可用(用户期待单调进度)。但**若用绝对值|sin 振幅|做反馈控制的目标轨迹**,就回到 PID 控制路线
- **时域特征 vs 频域特征哪个对用户更敏感?** 同一段动画,改变一个 cubic-bezier 控制点 vs 改变一个 FFT 频段,人眼哪个更先察觉?
- **DCT(离散余弦变换)是不是两者的天然桥?** —— DCT 的输入不必周期性,输出系数可类比"Penner 参数"。这条线如果成立,会有新的"频域缓动"领域

## Related

- [[concepts/fourier-series]] — 频域合成/本轮链
- [[concepts/animation-easing-functions]] — 时域缓动函数
- [[references/mechanical-watch-mechanics]] — 摆轮+擒纵的物理 PID 实现
- [[concepts/javascript-event-loop]] — 周期信号与离散事件循环的"轮转"对应
