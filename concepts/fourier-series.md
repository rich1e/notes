---
title: >-
  傅里叶级数：从单位圆到本轮（Epicycles）
category: concepts
tags:
  - mathematics
  - signal-processing
sources:
  - "https://www.andreinc.net/2024/04/24/from-the-circle-to-epicycles/"
created: 2026-07-25
updated: 2026-07-25
summary: >-
  傅里叶分析：从单位圆与正弦/余弦出发，由 Euler 公式 $e^{ix}=\cos x+i\sin x$ 串联"复数正弦""本轮链"与傅里叶级数。任意周期函数都可用一组旋转圆链机械图像（半径=振幅、转速=角频率、初角=相位）合成。
tier: supporting
lifecycle: reviewed
lifecycle_changed: 2026-09-03
lifecycle_reason: "auto-promoted by wiki-lint --consolidate: age>30d, confidence>0.78"
lifecycle_changed: 2026-07-25
base_confidence: 0.78
provenance:
  extracted: 0.85
  inferred: 0.12
  ambiguous: 0.03
relationships:
  - target: "[[concepts/animation-easing-functions]]"
    type: related_to
---

# 傅里叶级数：从单位圆到本轮（Epicycles）

## 单位圆与三角函数

单位圆 $x^2+y^2=1$ 上的点可参数化为：

$$
z(\theta) = e^{i\theta} = \cos\theta + i\sin\theta
$$

其中 $\theta$ 是弧度（非角度）。$\sin$ 与 $\cos$ 都是 $2\pi$ 周期的"位置追踪器"：圆上一点投影到 $y$ 轴得 $\sin$，投影到 $x$ 轴得 $\cos$。

## Euler 公式

$$
e^{ix} = \cos x + i \sin x
$$

欧拉公式把**复指数**与**三角函数**统一为一个对象。三个特殊结果：

| 公式 | 含义 |
|---|---|
| $e^{i\pi} + 1 = 0$ | "数学最美公式"——五个基本常数合一 |
| $\cos x = \frac{e^{ix}+e^{-ix}}{2}$ | 余弦 = 复指数之和 / 2 |
| $\sin x = \frac{e^{ix}-e^{-ix}}{2i}$ | 正弦 = 复指数之差 / 2i |

## 复正弦（Complex Sinusoid）

把振幅 $A$、角频率 $\omega$、相位 $\varphi$ 引入 Euler 公式：

$$
s(t) = A\, e^{i(\omega t + \varphi)} = A\cos(\omega t + \varphi) + i\, A\sin(\omega t + \varphi)
$$

复正弦是**两个实正弦的合体**——沿实轴投影得余弦，沿虚轴投影得正弦。在 3D 空间中表现为"螺旋钻"轨迹，随时间旋转。

## 正弦波叠加：干涉与抵消

两个正弦波叠加可放大或抵消（**波干涉**）：

| 关系 | 效果 |
|---|---|
| 同频同相 | 振幅相加 |
| 同频反相（相差 $\pi$） | 完全抵消 |
| 不同频 | 形成复杂周期图案 |

任意正弦波可写作 $A \sin(\omega t + \varphi)$，三个参数决定形态：$A$ 控制"高度"，$\omega$ 控制"快慢"，$\varphi$ 控制"起始位置"。

## 本轮（Epicycle）机械图像

在 [[concepts/animation-easing-functions]] 里也用到旋转视角，但本轮是更通用的视觉模型：

> 一根"指挥棒"串接 N 个旋转圆——第二个圆的圆心坐在第一个圆边缘上，第三个坐在第二个圆边缘上…指挥棒末端在 2D 平面上画出轨迹。

每个圆对应一个**复正弦**：

| 圆的参数 | 复正弦参数 |
|---|---|
| 半径 | 振幅 $A$ |
| 角速度 | 角频率 $\omega$ |
| 初始角度 | 相位 $\varphi$ |

> Pink Floyd《The Dark Side of the Moon》封面棱镜比喻：白光是输入的"任意周期函数 $f(x)$"，光谱是输出的"频谱分量"$A_n\cos$ 与 $B_n\sin$。

## 傅里叶级数

任意周期为 $P$ 的函数 $f(x)$ 都可展开为正弦/余弦的无穷和：

$$
f(x) = \frac{A_0}{2} + \sum_{n=1}^{\infty}\left[A_n \cos\!\left(\frac{2\pi n}{P}x\right) + B_n \sin\!\left(\frac{2\pi n}{P}x\right)\right]
$$

**傅里叶系数** $A_0, A_n, B_n$ 通过积分计算：

$$
A_n = \frac{2}{P}\int_{-P/2}^{+P/2} f(x)\cos\!\left(\frac{2\pi n}{P}x\right)dx
$$

$$
B_n = \frac{2}{P}\int_{-P/2}^{+P/2} f(x)\sin\!\left(\frac{2\pi n}{P}x\right)dx
$$

**指数形式**更紧凑：

$$
f(x) = \sum_{n=-N}^{N} C_n\, e^{i 2\pi n x / P},\quad C_n = \frac{1}{P}\int_{-P/2}^{+P/2} e^{-i 2\pi n x / P} f(x)\, dx
$$

注意 $n$ 遍历负数——这引入**负频率**概念，编码"旋转方向"。

## 经典信号的傅里叶展开

| 信号 | 傅里叶展开式（首项） | 关键观察 |
|---|---|---|
| 方波 | $f(x) = \frac{4}{\pi}\sum_{k=1}^{\infty}\frac{\sin((2k-1)\omega x)}{2k-1}$ | **只含奇次谐波** |
| 三角波 | $f(x) = \frac{8}{\pi^2}\sum_{k=1}^{N}\frac{(-1)^{k-1}}{(2k-1)^2}\sin((2k-1)x)$ | 振幅随 $1/n^2$ 衰减，更平滑 |
| 锯齿波 | $f(x) = \frac{2}{\pi}\sum_{k=1}^{N}(-1)^k\frac{\sin(kx)}{k}$ | 含 $1/n$ 衰减 |

方波展开的推导步骤可作为奇偶性利用的范本：
1. $A_0 = 0$（正负面积抵消）
2. $A_n = 0$（奇 × 偶函数在对称区间积分为零）
3. $B_n$ 只在 $n$ 为奇数时存活（$f \cdot \sin = $ 偶函数）

负振幅项的几何处理：把 $s_k(x) = -\frac{8}{3^2\pi^2}\sin(3x)$ 改写为 $s_k(x) = \frac{8}{3^2\pi^2}\sin(3x + \pi)$——吸收进相位避免"负半径"概念。

## 应用方向

| 领域 | 用法 |
|---|---|
| 数字信号处理 | FFT（快速傅里叶变换）算法核心 |
| 音频压缩 | MP3/AAC 频域掩蔽 |
| 图像处理 | JPEG DCT 类似思路 |
| 科学可视化 | "本轮绘图"把 SVG 路径转圆链（3Blue1Brown 风格） |

## 相关页面

- concepts/animation-easing-functions
- concepts/javascript-event-loop
- [[concepts/animation-easing-functions]] — 缓动函数也用曲线合成思路

## Related

- [[synthesis/concepts-fourier-series × concepts-animation-easing-functions]] — 频域合成 vs 时域参数化的正交关系
