---

title: Alienware HX 平台 BIOS UnderVolt 解锁
category: concept
tags: [alienware, bios, undervolt-protection, smokeless-umaf, m16-r1, 13代hx]
relationships:
  - target: "[[references/techpowerup-m16-r1-undervolt-thread]]"
    type: related_to
  - target: "[[references/dell-kb-alienware-high-cpu-temp]]"
    type: related_to

summary: Dell 在 Alienware H/HX 平台默认把 UnderVolt Protection（setup 变量）锁住，使 ThrottleStop 看到 "Locked"。通过 Smokeless UMAF U 盘刷写可在 1.12.1 BIOS 显示该选项；1.13.0+ 选项消失，需 grubx64 改 setup var。
sources:
  - https://notebooktalk.net/topic/2310-m16r1m18r1-smokeless-umaf-bios-options
  - https://www.techpowerup.com/forums/threads/how-to-unlock-alienware-m16-r1-undervolt-for-throttlestop.319229/
created: 2026-08-23
updated: 2026-08-23T08:45:00Z
base_confidence: 0.6
lifecycle: draft
lifecycle_changed: 2026-08-23
provenance:
  extracted: 0.5
  inferred: 0.3
  ambiguous: 0.2

---
# Alienware HX 平台 BIOS UnderVolt 解锁

## 背景

Alienware M16 R1、M18 R1、X17 R2 等使用 Intel 13 代 HX 平台。Dell 出厂 BIOS 默认 **UnderVolt Protection = Enabled**，导致：

- ThrottleStop 进 FIVR 后 "Unlock Adjustable Voltage" 灰显
- 切换到 "Locked" 提示，offset 控件消失
- Intel XTU 也无法降压
- 直接表现：CPU 长时负载撞 100°C → thermal throttle → 频率跌到 1 GHz

## 原理

UnderVolt Protection 是 BIOS setup 中的一个 flag。Intel ME / BIOS code check 这个变量决定是否对 MSR 0x150 写入 RO 锁。原生 BIOS 界面（按 F2）看不到这个 hidden 选项。

Dell 通过隐藏选项保留对 OEM/工程师的访问但屏蔽普通用户。社区工具 **Smokeless UMAF**（基于 UEFI 的 setup var 编辑器）可以暴露 Advanced Menu。

## 解锁流程（BIOS ≤ 1.12.1）

1. **准备 U 盘**：
   - FAT32 格式化
   - 写入 Smokeless_UMAF 全部文件
2. **重置 BIOS 默认项**：
   - 重启按 **F2** 进 BIOS
   - 关 Secure Boot（**必须**，否则不能启动 U 盘）
   - Save & Exit
3. **U 盘启动**：
   - F12 选择从 USB 启动
   - 进 UEFI Shell 或 Smokeless UI
4. **修改 UnderVolt Protection**：
   - Intel Advanced Menu → **OverClocking Performance Menu**
   - 找到 **UnderVolt Protection**
   - **改成 Disabled**
5. **保存退出**，重启
6. （可选）F2 重新打开 Secure Boot

进系统后，ThrottleStop FIVR 应能正常使用 "Unlock Adjustable Voltage" 和 offset 控件。

## BIOS 1.13.0+ 的坑

- UnderVolt Protection 选项**直接从菜单消失**（不是被禁用，是菜单项一并隐藏）
- Smokeless UMAF 的 GUI 也读不到该选项
- 需要走 grubx64 + setup_var 直接修改非易失变量名 ^[ambiguous]（社区报告，未完整文档化）
- 或退守到 1.12.1 并用备份刷回
- 操作前**务必备份原 BIOS dump**（Smokeless UMAF 的 "Backup" 功能）

## 跨型号推广性

社区用户已验证：

- M16 R1 (i7-13700HX / i9-13900HX / i9-13980HX)：✅
- M18 R1：✅ 同流程
- M15 R7（12 代 H）：⚠️ 部分锁，部分不锁 ^[ambiguous]
- X 系列：取决于具体 BIOS 版本

## 备份策略

- **刷前必备份 BIOS**（原厂 DUMP）
- Secure Boot 默认开；解锁完成后建议重新开 Secure Boot（验证完整启动链）
- 修改仅针对 setup var，不动 boot block，安全等级比刷 ME 固件高

## 相关 wiki 页面

- [[throttlestop-alienware-thermals]]
- [[cpu-undervolting]]
- [[throttlestop-fivr-undervolting]]
- [[smokeless-umaf]]
- [[research-throttlestop-alienware-thermals]]

## Related

- [[references/techpowerup-m16-r1-undervolt-thread|Techpowerup M16 R1 Undervolt Thread]] — shares #alienware (references)
- [[references/dell-kb-alienware-high-cpu-temp|Dell Kb Alienware High Cpu Temp]] — shares #alienware (references)

