---

title: ThrottleStop 选项速查
category: concept
tags: [throttlestop, fivr, tpl, speed-shift, bd-prochot, undervolt]
relationships:
  - target: "[[synthesis/research-throttlestop-alienware-thermals]]"
    type: related_to
  - target: "[[references/techpowerup-m16-r1-undervolt-thread]]"
    type: related_to
  - target: "[[references/ultrabookreview-throttlestop-guide-2026]]"
    type: related_to
  - target: "[[entities/kevin-glynn]]"
    type: related_to

summary: ThrottleStop 主窗口按按钮划分的功能速查：FIVR（电压） / TPL（功率上限） / Speed Shift（响应曲线） / BD PROCHOT（双向热信号） / C States（休眠）/ Benchmark（压力测试）。每个按钮具体影响与建议配置。
sources:
  - https://ultrabookreview.com/31385-the-throttlestop-guide
  - https://maketecheasier.com/reduce-cpu-temperature-undervolting/
created: 2026-08-23
updated: 2026-08-23T08:45:00Z
base_confidence: 0.8
lifecycle: draft
lifecycle_changed: 2026-08-23
provenance:
  extracted: 0.8
  inferred: 0.1
  ambiguous: 0.1

---
# ThrottleStop 选项速查

> ThrottleStop 主窗口按功能切割成多个按钮。常规降温至少了解 FIVR / TPL / Speed Shift / BD PROCHOT 四个。

## FIVR — 电压轨

**核心战场**。进 FIVR 窗口后有 4 个轨道：

| 轨道 | 推荐 offset | 备注 |
|---|---|---|
| CPU Core | -100 mV（保守起点） | 主战场 |
| CPU Cache | **与 Core 同值** | 不一致几乎必崩 |
| E-Cache | 0 | unclewebb 建议别动 |
| iGPU (Intel GPU) | 0（默认） | 老手可独立降 |
| System Agent | 0（默认） | 影响内存/PCIe 稳定性 |

附加：

- **Unlock Adjustable Voltage**：必须勾
- **Adaptive 模式**：动态减电压；不要选 Override（强制写死风险大）
- **mV Boost @ 800 MHz = +100 mV**：避免 idle / 唤醒崩溃的关键技巧

## TPL — Turbo Power Limits

**最高性价比降温按钮**。把 PL1 / PL2 上限下调即可：

- PL1（长时间功耗）：默认 45-75W；可以降到 35-45W 看散热能否接受
- PL2（短时 boost 上限）：默认 70-115W；可以降到 60-95W
- Tau（保持 PL2 的时长）：默认 ~28s，可缩短
- PL4（绝对上限）：通常不动

## Speed Shift EPP

Speed Shift 是 Intel 自 Skylake 起的硬件调速器，EPP（Energy Performance Preference）：

- **0 = 最激进**（响应快，CPU 愿意随时回 turbo）
- **128 = 最保守**（响应慢，节能倾向）
- **建议**：AC 0 / Battery 128

Dell XPS 15 9550/9560 等老机型默认 BIOS 关闭 Speed Shift，**需手动开启**，否则 ThrottleStop 看不到 EPP 控件。

## BD PROCHOT

BD = **Bi-Directional** PROCHOT。CPU 与 dGPU 共用散热时，Dell/HP 经常让 dGPU 过热时反向触发 CPU 降频。

- **默认应保持开启**：CPU 不被 dGPU 拖累
- **不建议禁用**：会让 CPU 单跑时温度可达 100°C+，因为失去了跨设备保护

## C States

控制 C1/C6/C7 等低功耗 C-state 何时进入。笔记本场景下：

- 关闭 C-states：略升温，但减少 wake latency，benchmark 更稳定
- 默认即可，undervolt 目标用户一般不动这块

## Benchmark（TS Bench）

内置压力测试，验证 offset 是否稳定：

- 5 分钟 TS Bench 不崩 = 起点基本能用
- 更严格的稳定性要靠 Cinebench R23 循环 + Prime95 + 游戏实测

## 主窗口其他开关

- **Turn On / Off**：总开关，关掉就不监控、不调参
- **Memory**：DDR5/XMP 配置相关（部分 OEM 把内存调参放在 TS 里）
- **Notification Area**：把 monitoring 图标塞进任务栏

## 相关 wiki 页面

- [[throttlestop-alienware-thermals]]
- [[throttlestop-fivr-undervolting]]
- [[cpu-undervolting]]
- [[throttlestop]]

## Related

- [[synthesis/research-throttlestop-alienware-thermals|Research: Alienware 笔记本 ThrottleStop 降压降温]] — shares #fivr/#throttlestop/#undervolt (synthesis)
- [[references/techpowerup-m16-r1-undervolt-thread|How to unlock Alienware m16 R1 undervolt for ThrottleStop (TechPowerUp Forum)]] — shares #throttlestop/#undervolt (references)
- [[references/ultrabookreview-throttlestop-guide-2026|ThrottleStop Guide (UltrabookReview, 2026)]] — shares #throttlestop/#undervolt (references)
- [[entities/kevin-glynn|Kevin Glynn (UncleWebb)]] — shares #fivr/#throttlestop (entities)

