---
title: 外星人笔记本 ThrottleStop 降压降温
category: skill
tags: [throttlestop, undervolt, alienware, laptop, intel, 散热, 降压]
summary: 通过 ThrottleStop 的 FIVR 负压（offset voltage）对 Dell Alienware 笔记本进行 CPU 降压，以降低温度、缓解 thermal throttling 并延长续航。涵盖 BIOS 解锁、配置流程、稳定性验证、风险。
sources:
  - https://ultrabookreview.com/31385-the-throttlestop-guide
  - https://maketecheasier.com/reduce-cpu-temperature-undervolting/
  - https://www.dell.com/support/article/en-us/sln308057
  - https://www.dell.com/support/kbdoc/en-us/000131532
  - https://notebooktalk.net/topic/2310-m16r1m18r1-smokeless-umaf-bios-options
  - https://www.techpowerup.com/forums/threads/how-to-unlock-alienware-m16-r1-undervolt-for-throttlestop.319229/
created: 2026-08-23
updated: 2026-08-23
base_confidence: 0.7
lifecycle: draft
lifecycle_changed: 2026-08-23
provenance:
  extracted: 0.6
  inferred: 0.3
  ambiguous: 0.1
---

# 外星人笔记本 ThrottleStop 降压降温

## 适用场景

Dell Alienware 笔记本（M15 R6/R7、M16 R1、X15、X17 等 Intel H/HX 平台）默认电压冗余度高，CPU 在长时间负载下容易撞到 100°C TCC 阈值触发 thermal throttling。ThrottleStop 通过 MSR 0x150 写入负向 offset voltage，让 CPU 在同频下功耗降低、温度下降。

## 推荐路线

1. **先用 Alienware Command Center（AWCC）的 TCC Offset** — 无损、可逆。Fusion 页面把 TCC Offset 调到 5–15（对应最高 95–85°C），是零门槛的降温办法。
2. **再走 ThrottleStop 降压** — 需要解锁 BIOS UnderVolt Protection 位（HX 平台），通过 FIVR 写入 -80 ~ -150 mV offset，可叠加 TCC。
3. **搭配措施**：抬高机身（散热底座）、限制 PL1/PL2（[[throttlestop-options]]）、关闭 BD PROCHOT、HWInfo64 监控。

## 详细流程

### 0. 前置条件

- ThrottleStop 9.x（从 TechPowerUp 下载）
- 管理员权限运行
- 关闭 VBS（Memory Integrity），否则 MSR 0x150 写入会被静默屏蔽，右侧电压表显示 0.000V
- 卸载 Intel XTU（避免 register 冲突）。若之前用过 XTU，必须先恢复默认再卸载

### 1. 解锁 BIOS UnderVolt Protection（关键）

Alienware H/HX 默认在 **Intel Advanced Menu → OverClocking Performance Menu** 下隐藏 **UnderVolt Protection** 开关。需要在 1.12.1 及更早 BIOS 里通过 **Smokeless UMAF** U 盘刷写才能显示。^[extracted]

**步骤**：

1. FAT32 格式 U 盘，放入 Smokeless_UMAF 全部文件
2. 重启按 F2 进 BIOS → 关闭 Secure Boot → 保存退出
3. F12 选 USB 启动
4. 进 Intel Advanced Menu → OverClocking Performance Menu
5. **UnderVolt Protection 设为 Disabled**
6. 保存重启；之后可以重新打开 Secure Boot

**注意**：1.13.0 及之后 BIOS 直接隐藏此选项，需用 grubx64 改 setup 变量，或停留在 1.12.1。

### 2. FIVR 配置

打开 ThrottleStop → **FIVR** 按钮：

| 选项 | 值 |
|---|---|
| Unlock Adjustable Voltage（CPU Core） | ✅ |
| 模式 | Adaptive（非 Override） |
| **CPU Core offset** | **−100 mV**（保守起点；常见落地 -120 ~ -150） |
| CPU Cache offset | 与 Core 同值 |
| E-Cache offset | 0（unclewebb 建议） |
| **mV Boost @ 800 MHz** | **+100 mV**（关键技巧：避免 idle 饿死） |
| iGPU / System Agent | 0 |
| Speed Shift EPP | AC 0 / Battery 128 |

**"mV Boost @ 800 MHz = +100 mV" 是 m16 R1 社区验证的稳定秘诀**：纯 -100 mV 会拉低 idle/低频电压，导致从休眠恢复黑屏、低负载崩溃；+100 mV 在 800 MHz 处补回电压，turbo 高频区仍享受全幅降压。

**点击 Apply → "Save voltages immediately"**。关掉 ThrottleStop 再打开检查电压是否真的写入（验证持久性）。

### 3. 稳定性验证

按此顺序递增压力：

1. **TS Bench** 内置（5 分钟）
2. **Cinebench R23 多核循环** 15-30 分钟
3. **Prime95 Small FFTs** 1 小时
4. **实际游戏** 1-2 小时
5. **睡眠唤醒测试**（黑屏 = mV Boost 抬高或减小 offset）
6. **Windows 事件查看器 → 系统日志 → 事件 ID 19 (WHEA Logger)**：任何错误 = 退回 10–15 mV

确认稳定后：

- 勾选 main 窗口 **"Turn On"**
- 把 ThrottleStop.exe 写入 Task Scheduler（"At log on" + 最高权限）确保每次开机生效
- save profile 到 ThrottleStop.ini

### 4. 与其他工具配合

- **HWInfo64 / HWiNFO**：监控 CPU Package 温度、最高频、Package Power，作为对比基线
- **MSI Afterburner**：GPU 侧降压（独立 CPU FIVR 之外的事）
- **AWCC TCC Offset**：CPU 温度天花板，与降压正交，可叠加

## 预期效果

- **CPU Package 温度**：典型 -8 ~ -15°C @ 全核负载（m16 R1 / m15 R7 等）
- **持续 turbo 时长**：因为不再撞 thermal throttle，全核频率能维持更久，等价性能不降反升
- **续航**：idle 电压降低，电池使用延长（视场景 5-15%）

## 风险与边界

- **必读警告**：
  - VBS / Memory Integrity 未关：写入看起来生效实则被屏蔽（电压表显示 0.000V）
  - 在锁定 BIOS 下强行降压：PROCHOT 假触发，CPU 被锁到 0.997 GHz（Acer Swift X 案例）
  - 修改 1.13.0+ BIOS：选项缺失，老司机走 grubx64 改 setup var
- **CPU 体质差异**：i7-13700HX 有人只能 -80 mV，好的 i9-13980HX 体质可冲 -150 mV。慢慢推
- **核显降压**：iGPU 单独降压容易在 GPU 基准测试时翻车，初学者不动
- **过降压症状**：
  - 蓝屏 / 死机 → 退回 5-10 mV
  - 黑屏唤醒 → 抬高 mV Boost
  - WHEA Logger 19 → 退回 10-15 mV
- **不推荐禁用 BD PROCHOT**：Dell 笔记本 dGPU 过热会拉 CPU 一起降频，关掉 BD PROCHOT 后 CPU 可能顶到 100°C+ 持续运行

## 外星人特有的优化点（不仅是降压）

1. **BIOS 1.1.0+**：PL1 从 115W 降到 75W，本身就是 Dell 的官方降温动作
2. **AWCC 性能模式**：Full Speed 会提升风扇转数但也拉高功耗；日常用 Balanced/Quiet 反而更凉
3. **散热底座 + 抬高机身**：物理辅助 5-10°C
4. **Undervolting 与 TCC Offset 协同**：TCC 控制硬上限，Undervolt 控制平均温度，两者收益正交

## 相关 wiki 页面

- [[throttlestop-fivr-undervolting]] — 原理层：MSR 0x150 / FIVR / P=C×V²×f
- [[alienware-bios-undervolt-unlock]] — BIOS 解锁的具体路径
- [[throttlestop-options]] — FIVR / Speed Shift / BD PROCHOT 等各 option 速查
- [[throttlestop]] — 工具本体与作者 UncleWebb
- [[kevin-glynn]] — ThrottleStop 作者
- [[research-throttlestop-alienware-thermals]] — 完整 research synthesis
