---

title: ThrottleStop
category: entity
tags: [throttlestop, tool, undervolt, intel, unclewebb, techpowerup, fivr, windows, freeware]
relationships:
  - target: "[[references/techpowerup-m16-r1-undervolt-thread]]"
    type: related_to
  - target: "[[references/ultrabookreview-throttlestop-guide-2026]]"
    type: related_to
  - target: "[[references/dell-kb-alienware-high-cpu-temp]]"
    type: related_to
  - target: "[[synthesis/research-throttlestop-alienware-thermals]]"
    type: related_to
  - target: "[[concepts/throttlestop-options]]"
    type: related_to
  - target: "[[concepts/throttlestop-fivr-undervolting]]"
    type: related_to
summary: Kevin "UncleWebb" Glynn 开发的 Windows 笔记本 CPU 调参工具（2009 起 / 当前 v9.7 / freeware）。通过 MSR 0x150 写 FIVR Offset Voltage 实现降压，配套 FIVR / TPL / Speed Shift / BD PROCHOT 等开关控制 thermal throttling。是 Intel XTU 受限情况下的事实标准替代品。
sources:
  - https://www.techpowerup.com/throttlestop/
  - https://www.techpowerup.com/forums/threads/throttlestop-official-thread.255311/
  - https://ultrabookreview.com/31385-the-throttlestop-guide
  - https://maketecheasier.com/reduce-cpu-temperature-undervolting/
  - https://throttlestop.en.lo4d.com/windows
  - https://www.bleepingcomputer.com/news/security/avast-norton-and-other-avs-are-removing-the-winring0-driver/
  - https://m.kaspersky.co.uk/about/press-releases/kaspersky-uncovers-throttlestop-flaw-in-brazil-ransomware-attack
created: 2026-08-23
updated: 2026-08-23T08:45:00Z
base_confidence: 0.8
lifecycle: draft
lifecycle_changed: 2026-08-23
provenance:
  extracted: 0.6
  inferred: 0.2
  ambiguous: 0.2

---
# ThrottleStop

## 身份

- **作者**：Kevin Glynn（论坛化名 UncleWebb）
- **首发**：2009 年 ^[extracted]（lo4d 列 "Initial Release" 为 2009 年）
- **当前稳定版**：9.7（2024-12-28 发布）^[extracted]
- **类型**：Freeware（免费） / 闭源 / 便携式 ZIP
- **体积**：约 1.71 MB（v9.7 zip）
- **SHA256**（v9.7 zip）：d83d3edbd037a926d9319c6f4db62f84657a39d47bd4fae5fa26f692790e800d ^[extracted]
- **平台**：Windows 11 / 10 / 8 / 7，32+64 位
- **CPU 支持**：Intel Core 2 → 14 代 Arrow Lake；部分 ARM/AMD 不支持
- **分发**：TechPowerUp（官方）；Notebookcheck / UltrabookReview 是公告转载；lo4d 是镜像分发（SHA256 公开）

## 主要功能

### 核心调参

| 功能 | 实现层 | 目的 |
|---|---|---|
| **FIVR** | MSR 0x150 | 负 offset → CPU 降压 |
| **TPL (Turbo Power Limits)** | MSR 0x610 / 0x618 | PL1 / PL2 / PL4 限制 |
| **Speed Shift EPP** | IA32_HWP_REQUEST | CPU 调频响应曲线 (0-128) |
| **BD PROCHOT** | MSR 0x1FC | 关闭 dGPU 反向触发的 CPU throttle |
| **C States** | ACPI | 控制低功耗 C-state 进出 |
| **TjMax Control** | MSR 0x1A2 | 自定义 thermal throttle 阈值（默认 100°C） |

### 辅助功能

- **TS Bench**：内置压力测试（5-15 分钟）
- **温度监控**：实时显示 Package / Core 温度
- **Multiplier Control**：手动锁定 / 解锁倍频
- **Clock Modulation**：旧式降频兼容
- **Profiled Persistence**：FIVR offsets 写 ThrottleStop.ini，重启后重新应用
- **Task Scheduler 集成**：开机自动加载，附带 admin 权限
- **GPU Clock Control**（部分 beta）：显卡侧 Clock/Memory 微调

## 优势

- **跳过 Intel XTU 的 OEM 屏蔽**：XTU 在 Dell / HP / Lenovo 部分 SKU 上无法写入 MSR，ThrottleStop 直接调用 `wrmsr` 绕过
- **OEM 不一致 BIOS 兼容性**：未签 OEM 定制 BIOS 仍能用
- **持久化 vs XTU**：offset 写 ini 文件而不是注册表，重装系统保留友好
- **独立开发者维护 16 年**：跨 6 代到 14 代 Intel 实际口碑
- **多场景 profile**：每 profile 独立存 offset（Gaming / Battery / Office 等）

## 局限

### 平台限制

- **仅 Windows**：Linux 用户走 intel-undervolt、pstate-frequency、coreboot patch 或直接 msr-safe
- **仅 Intel**：AMD 用户走 Ryzen Controller / Curve Optimizer 或 AMD CBS（BIOS 层）
- **依赖 MSR 0x150 写入权限**：VBS / Memory Integrity 未关会屏蔽写入；BIOS 锁 UnderVolt Protection 时完全失效
- **不支持笔记本 dGPU / 外接显卡**：不在目标场景

### 安全与审计

- **完全闭源**：无 SBoM / 第三方审计
- **CVE-2025-7771**：ThrottleStop.sys 在 2025 年被 Kaspersky 报告的漏洞；MedusaLocker 勒索软件团伙在巴西攻击中利用此漏洞作 LOLBin / driver ^[extracted][来自 kaspersky.co.uk 公告]
- **WinRing0.sys AV 误报**：Avast / Norton / Kaspersky / Windows Defender 等曾把 ThrottleStop 配套的 WinRing0 驱动标记为风险；属启发式误报（驱动有 IOCTL 写 MSR 权限）
- **Admin 权限强制**：必须以管理员身份运行；ini 文件可被改 → 写入设置时需注意文件完整性

### 已知约束

- **9.7 在 14500HX 上选项灰显**（社区报告）^[ambiguous]
- **12 代 K/KF 后部分 SKU 被 Intel 收回 offset 支持**：不在 TS 修复范围
- **多 profile 同时运行会冲突**：只应启用一个 profile 的 Voltages

## 替代品对比

| 工具 | 平台 | 优势 | 何时不用 TS |
|---|---|---|---|
| **Intel XTU** | Windows | Intel 官方 | OEM MSR 屏蔽后失效 |
| **XTU + ThrottleStop 共存会冲突** | — | — | 二选一，迁前必须 reset |
| **Ryzen Controller** | Windows / AMD | AMD V/F 曲线下移 | AMD 用，Intel 不可用 |
| **AMD Ryzen Master** | Windows / AMD | AMD 官方 | 同上 |
| **intel-undervolt** | Linux | Linux 命令行 | 必须非 Windows |
| **coreboot Patch** | BIOS | 改 ME / FIVR 默认 | 不愿刷 BIOS 时不用 |

## 安装与配置流程（精简）

1. 下载 `ThrottleStop_9.7.zip`（TechPowerUp / lo4d 等渠道，注意 SHA256 比对）
2. 解压到非系统盘文件夹
3. 右键 `ThrottleStop.exe` → **以管理员身份运行**
4. 默认 profile 是 "Gaming"，可改名 / 新建 `Battery` `Office` 等
5. 关闭 VBS / Memory Integrity（先决条件 — 否则写入被静默屏蔽）
6. 进 FIVR → Unlock Adjustable Voltage → CPU Core / Cache 改 -100 mV → Save
7. Task Scheduler → At log on + Highest privileges → 启动 ThrottleStop.exe

详见 [[throttlestop-alienware-thermals]]。

## 关联人物 / 工具

- **作者**：[[kevin-glynn]]（UncleWebb）
- **BIOS 解锁搭档**：[[smokeless-umaf]]
- **官方支持线程**：TechPowerUp Forums（255311）
- **官方教程**：Notebookcheck 2017 + UltrabookReview 2026 升级版（[[ultrabookreview-throttlestop-guide-2026]]）

## 相关 wiki 页面

- [[throttlestop-options]] — 选项速查
- [[throttlestop-fivr-undervolting]] — 原理层
- [[cpu-undervolting]] — 概念层
- [[throttlestop-alienware-thermals]] — Alienware 完整流程
- [[kevin-glynn]]
- [[research-throttlestop-alienware-thermals]]

## Related
- [[concepts/throttlestop-fivr-undervolting]]
- [[concepts/throttlestop-options]]
- [[synthesis/research-throttlestop-alienware-thermals]]
- [[references/dell-kb-alienware-high-cpu-temp]]
- [[references/ultrabookreview-throttlestop-guide-2026]]

- [[references/techpowerup-m16-r1-undervolt-thread|Techpowerup M16 R1 Undervolt Thread]] — shares #throttlestop/#undervolt (references)

