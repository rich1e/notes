---

title: Smokeless_UMAF
category: entity
tags: [smokeless-umaf, bios, uefi, tool, alienware, undervolt-protection]
relationships:
  - target: "[[synthesis/research-throttlestop-alienware-thermals]]"
    type: related_to

summary: UEFI 模式下运行的 BIOS setup var 编辑器，常用于解锁 OEM 隐藏选项（如 Alienware HX 的 UnderVolt Protection）。基于 AMD 平台 Project UMAF 框架，Intel 平台通过临时镜像形式可用。
sources:
  - https://notebooktalk.net/topic/2310-m16r1m18r1-smokeless-umaf-bios-options
  - https://www.techpowerup.com/forums/threads/how-to-unlock-alienware-m16-r1-undervolt-for-throttlestop.319229/
created: 2026-08-23
updated: 2026-08-23T08:45:00Z
base_confidence: 0.5
lifecycle: draft
lifecycle_changed: 2026-08-23
provenance:
  extracted: 0.4
  inferred: 0.4
  ambiguous: 0.2

---
# Smokeless_UMAF

## 身份

- **类型**：UEFI Shell / USB 启动镜像
- **起源**：基于 AMD Project UMAF（Universal Motherboard Access Framework），由社区移植 Intel 平台 ^[inferred]
- **目的**：在不开盖 / 不拆机 / 不改硬件的前提下访问 OEM 隐藏的 BIOS setup 变量
- **分发**：NotebookTalk、TechPowerUp foruma、GitHub

## 在 Alienware HX 上的用法

1. 把 Smokeless_UMAF 文件拷到 FAT32 U 盘
2. BIOS 关 Secure Boot → F12 从 USB 启动
3. 进 Smokeless UI → 暴露 Intel Advanced Menu
4. OverClocking Performance Menu → UnderVolt Protection → Disabled
5. Save & Exit

## 安全边界

- 仅修改 setup var（BIOS 非易失变量），不动 boot block、不动 ME
- 修改前可以选定 "Backup" 把原 dump 存到 U 盘
- 比刷 ME 固件风险低得多，但仍属"超出普通用户操作"水平
- Secure Boot 解锁属于官方允许的 OEM 维护操作，不会失效的 TPM 不应被攻击

## BIOS 1.13.0+ 兼容性

- 选项显示依赖 BIOS 自身是否输出菜单项
- 1.13.0 起 UnderVolt Protection 完全从菜单移除，Smokeless_UMAF 默认抓不到
- 社区提示：**grubx64 + setup_var** 直接读写非易失变量，可绕过菜单 ^[ambiguous]（操作细节未必在所有机器通用）

## 相关 wiki 页面

- [[throttlestop-alienware-thermals]]
- [[alienware-bios-undervolt-unlock]]
- [[throttlestop]]

## Related

- [[synthesis/research-throttlestop-alienware-thermals|Research Throttlestop Alienware Thermals]] — shares #alienware (synthesis)

